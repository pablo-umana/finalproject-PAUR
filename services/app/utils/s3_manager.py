import boto3
from botocore.exceptions import ClientError
from typing import Optional
import os
from datetime import datetime, timedelta
from app.utils.exceptions import ResourceError

class S3ResourceManager:
    def __init__(self):
        """Inicializa el cliente de S3 con las credenciales de AWS."""
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.bucket_name = os.getenv('AWS_S3_BUCKET')
        self.max_file_size = 1024 * 1024  # 1MB en bytes

    def _generate_resource_path(self, template_id: int, filename: str) -> str:
        """Genera una ruta única para el recurso en S3."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"templates/{template_id}/resources/{timestamp}_{filename}"

    def _validate_file_size(self, file_data: bytes) -> bool:
        """Valida que el archivo no exceda el tamaño máximo permitido."""
        if len(file_data) > self.max_file_size:
            raise ResourceError(f"El archivo excede el tamaño máximo permitido de {self.max_file_size/1024/1024}MB")
        return True

    def upload_resource(self, file_data: bytes, template_id: int, filename: str) -> str:
        """
        Sube un recurso a S3.

        Args:
            file_data: Contenido del archivo en bytes
            template_id: ID de la plantilla
            filename: Nombre original del archivo

        Returns:
            str: Ruta del recurso en S3

        Raises:
            ResourceError: Si hay un error al subir el archivo
        """
        try:
            # Validar tamaño del archivo
            self._validate_file_size(file_data)

            # Generar ruta única
            resource_path = self._generate_resource_path(template_id, filename)

            # Subir archivo a S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=resource_path,
                Body=file_data,
                ContentType=self._get_content_type(filename)
            )

            return resource_path

        except ClientError as e:
            raise ResourceError(f"Error al subir recurso a S3: {str(e)}")
        except Exception as e:
            raise ResourceError(f"Error inesperado al subir recurso: {str(e)}")

    def delete_resource(self, resource_path: str) -> bool:
        """
        Elimina un recurso de S3.

        Args:
            resource_path: Ruta del recurso en S3

        Returns:
            bool: True si se eliminó correctamente

        Raises:
            ResourceError: Si hay un error al eliminar el archivo
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=resource_path
            )
            return True
        except ClientError as e:
            raise ResourceError(f"Error al eliminar recurso de S3: {str(e)}")

    def get_resource_url(self, resource_path: str, expiration: int = 3600) -> str:
        """
        Obtiene una URL temporal para acceder al recurso.

        Args:
            resource_path: Ruta del recurso en S3
            expiration: Tiempo de expiración en segundos (default 1 hora)

        Returns:
            str: URL temporal del recurso

        Raises:
            ResourceError: Si hay un error al generar la URL
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': resource_path
                },
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            raise ResourceError(f"Error al generar URL del recurso: {str(e)}")

    def _get_content_type(self, filename: str) -> str:
        """Determina el content type basado en la extensión del archivo."""
        extension = filename.lower().split('.')[-1]
        content_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'pdf': 'application/pdf'
        }
        return content_types.get(extension, 'application/octet-stream')

    def check_resource_exists(self, resource_path: str) -> bool:
        """
        Verifica si un recurso existe en S3.

        Args:
            resource_path: Ruta del recurso en S3

        Returns:
            bool: True si el recurso existe
        """
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=resource_path
            )
            return True
        except ClientError:
            return False
