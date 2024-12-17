from typing import List, Optional, Dict
from sqlalchemy import desc
from app.repositories.base_repository import BaseRepository
from app.models.template import Template
from app.models.template_components import (
    TemplateVersion,
    TemplateResource,
    TemplatePermission
)
from app.utils.exceptions import ValidationError, NotFoundException
from app.utils.template_validator import TemplateValidator
from app.utils.s3_manager import S3ResourceManager
from datetime import datetime

class TemplateRepository(BaseRepository[Template]):
    def __init__(self):
        super().__init__(Template)
        self.validator = TemplateValidator()
        self.s3_manager = S3ResourceManager()

    def get_latest_version(self, template_id: int) -> Optional[TemplateVersion]:
        """
        Obtiene la última versión de una plantilla.

        Args:
            template_id: ID de la plantilla

        Returns:
            TemplateVersion o None si no hay versiones
        """
        return TemplateVersion.query.filter_by(
            template_id=template_id
        ).order_by(
            desc(TemplateVersion.version_number)
        ).first()

    def create_version(self, template: Template, content: dict, created_by: int) -> TemplateVersion:
        """
        Crea una nueva versión de la plantilla.

        Args:
            template: Instancia de la plantilla
            content: Contenido de la plantilla
            created_by: ID del usuario que crea la versión

        Returns:
            Nueva versión creada

        Raises:
            ValidationError: Si el contenido no es válido
        """
        # Validar estructura y contenido
        self.validator.validate_all(
            content,
            template.template_id,
            template.resources
        )

        # Obtener número de versión
        latest_version = self.get_latest_version(template.template_id)
        version_number = (latest_version.version_number + 1) if latest_version else 1

        # Crear nueva versión
        version = TemplateVersion(
            template_id=template.template_id,
            version_number=version_number,
            content=content,
            created_by=created_by,
            is_active=True
        )

        try:
            self.db.session.add(version)
            self.db.session.commit()
            return version
        except Exception as e:
            self.db.session.rollback()
            raise ValidationError(f"Error al crear versión: {str(e)}")

    def get_template_versions(self, template_id: int, user_id: int) -> List[TemplateVersion]:
        """
        Obtiene todas las versiones de una plantilla.

        Args:
            template_id: ID de la plantilla
            user_id: ID del usuario que solicita las versiones

        Returns:
            Lista de versiones ordenadas por número de versión descendente
        """
        # Verificar permisos
        if not self.check_permission(template_id, user_id, 'can_view'):
            raise ValidationError("No tiene permisos para ver las versiones de esta plantilla")

        return TemplateVersion.query.filter_by(
            template_id=template_id
        ).order_by(
            desc(TemplateVersion.version_number)
        ).all()

    def get_template_with_permissions(self, template_id: int, user_id: int) -> Optional[Template]:
        """
        Obtiene una plantilla verificando permisos del usuario.

        Args:
            template_id: ID de la plantilla
            user_id: ID del usuario

        Returns:
            Template si tiene permisos, None si no existe

        Raises:
            ValidationError: Si no tiene permisos
        """
        template = self.get_by_id(template_id)
        if not template:
            return None

        if not self.check_permission(template_id, user_id, 'can_view'):
            raise ValidationError("No tiene permisos para ver esta plantilla")

        return template

    def check_permission(self, template_id: int, user_id: int, permission_type: str) -> bool:
        """
        Verifica si un usuario tiene un permiso específico sobre una plantilla.

        Args:
            template_id: ID de la plantilla
            user_id: ID del usuario
            permission_type: Tipo de permiso a verificar

        Returns:
            bool: True si tiene el permiso
        """
        # El administrador siempre tiene todos los permisos
        user_roles = self._get_user_roles(user_id)
        if 'admin' in user_roles:
            return True

        permission = TemplatePermission.query.filter_by(
            template_id=template_id,
            role_id__in=[role.role_id for role in user_roles]
        ).first()

        return permission and getattr(permission, permission_type, False)

    def manage_resources(self, template_id: int, resources: List[dict]) -> List[TemplateResource]:
        """
        Gestiona los recursos de una plantilla.

        Args:
            template_id: ID de la plantilla
            resources: Lista de recursos a gestionar

        Returns:
            Lista de recursos creados/actualizados

        Raises:
            ValidationError: Si hay error en la gestión de recursos
        """
        managed_resources = []
        for resource in resources:
            try:
                # Subir archivo a S3 si es nuevo
                if 'file_data' in resource:
                    resource_path = self.s3_manager.upload_resource(
                        resource['file_data'],
                        template_id,
                        resource['original_name']
                    )
                    resource['resource_path'] = resource_path

                # Crear o actualizar registro de recurso
                template_resource = TemplateResource(
                    template_id=template_id,
                    resource_type=resource['resource_type'],
                    resource_path=resource['resource_path'],
                    original_name=resource['original_name'],
                    size_bytes=len(resource.get('file_data', b''))
                )

                self.db.session.add(template_resource)
                managed_resources.append(template_resource)

            except Exception as e:
                self.db.session.rollback()
                raise ValidationError(f"Error al gestionar recurso: {str(e)}")

        self.db.session.commit()
        return managed_resources

    def _get_user_roles(self, user_id: int) -> List:
        """Obtiene los roles de un usuario."""
        from app.models.auth import User
        user = User.query.get(user_id)
        return user.roles if user else []