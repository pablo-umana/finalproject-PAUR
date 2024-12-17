from typing import List, Dict, Optional
from datetime import datetime
from app.models.template import Template
from app.models.template_components import (
    TemplateVersion,
    TemplateResource,
    TemplatePermission
)
from app.repositories.template_repository import TemplateRepository
from app.services.template_permission_service import TemplatePermissionService
from app.utils.exceptions import ValidationError, NotFoundException
from app.utils.template_validator import TemplateValidator
from app.utils.s3_manager import S3ResourceManager
from app import db

class TemplateService:
    def __init__(self):
        self.repository = TemplateRepository()
        self.permission_service = TemplatePermissionService()
        self.validator = TemplateValidator()
        self.s3_manager = S3ResourceManager()

    def create_template(self, data: dict, user_id: int) -> Template:
        """
        Crea una nueva plantilla con su versión inicial.

        Args:
            data: Datos de la plantilla y su contenido inicial
            user_id: ID del usuario que crea la plantilla

        Returns:
            Template: Nueva plantilla creada

        Raises:
            ValidationError: Si los datos son inválidos
        """
        try:
            # Extraer contenido y recursos
            content = data.pop('content', {})
            resources = data.pop('resources', [])
            permissions = data.pop('permissions', [])

            # Crear plantilla base
            template = Template(
                **data,
                created_by=user_id,
                updated_by=user_id
            )
            template = self.repository.create(template)

            # Gestionar recursos si existen
            if resources:
                self.manage_resources(template.template_id, resources)

            # Crear versión inicial
            if content:
                self.create_version(template.template_id, content, user_id)

            # Asignar permisos
            if permissions:
                self.permission_service.assign_permissions(template.template_id, permissions)

            return template

        except Exception as e:
            db.session.rollback()
            raise ValidationError(f"Error al crear plantilla: {str(e)}")

    def update_template(self, template_id: int, data: dict, user_id: int) -> Template:
        """
        Actualiza los metadatos de la plantilla.

        Args:
            template_id: ID de la plantilla
            data: Datos a actualizar
            user_id: ID del usuario que realiza la actualización

        Returns:
            Template: Plantilla actualizada
        """
        template = self.get_template_with_permissions(template_id, user_id, 'can_edit')

        # Actualizar solo campos permitidos
        allowed_fields = {'name', 'description', 'category_id', 'is_active'}
        update_data = {k: v for k, v in data.items() if k in allowed_fields}

        for key, value in update_data.items():
            setattr(template, key, value)

        template.updated_by = user_id
        template.updated_at = datetime.utcnow()

        return self.repository.update(template)

    def create_version(self, template_id: int, content: dict, user_id: int) -> TemplateVersion:
        """
        Crea una nueva versión de la plantilla.

        Args:
            template_id: ID de la plantilla
            content: Contenido de la nueva versión
            user_id: ID del usuario que crea la versión

        Returns:
            TemplateVersion: Nueva versión creada
        """
        template = self.get_template_with_permissions(template_id, user_id, 'can_edit')
        return self.repository.create_version(template, content, user_id)

    def get_template_versions(self, template_id: int, user_id: int) -> List[TemplateVersion]:
        """
        Obtiene todas las versiones de una plantilla.

        Args:
            template_id: ID de la plantilla
            user_id: ID del usuario que solicita las versiones

        Returns:
            List[TemplateVersion]: Lista de versiones
        """
        self.get_template_with_permissions(template_id, user_id, 'can_view')
        return self.repository.get_template_versions(template_id, user_id)

    def get_template_with_permissions(self, template_id: int, user_id: int, required_permission: str) -> Template:
        """
        Obtiene una plantilla verificando permisos.

        Args:
            template_id: ID de la plantilla
            user_id: ID del usuario
            required_permission: Permiso requerido

        Returns:
            Template: Plantilla si tiene permisos

        Raises:
            NotFoundException: Si la plantilla no existe
            ValidationError: Si no tiene permisos
        """
        template = self.repository.get_by_id(template_id)
        if not template:
            raise NotFoundException(f"Plantilla con ID {template_id} no encontrada")

        if not self.permission_service.check_permission(template_id, user_id, required_permission):
            raise ValidationError(f"No tiene permiso para {required_permission} esta plantilla")

        return template

    def manage_resources(self, template_id: int, resources: List[dict]) -> List[TemplateResource]:
        """
        Gestiona los recursos de una plantilla.

        Args:
            template_id: ID de la plantilla
            resources: Lista de recursos a gestionar

        Returns:
            List[TemplateResource]: Lista de recursos gestionados
        """
        return self.repository.manage_resources(template_id, resources)

    def delete_template(self, template_id: int, user_id: int) -> None:
        """
        Elimina una plantilla y sus recursos.

        Args:
            template_id: ID de la plantilla
            user_id: ID del usuario que elimina

        Raises:
            ValidationError: Si no tiene permisos o hay error en la eliminación
        """
        template = self.get_template_with_permissions(template_id, user_id, 'can_edit')

        try:
            # Eliminar recursos de S3
            for resource in template.resources:
                self.s3_manager.delete_resource(resource.resource_path)

            # Eliminar plantilla y datos relacionados
            self.repository.delete(template)

        except Exception as e:
            db.session.rollback()
            raise ValidationError(f"Error al eliminar plantilla: {str(e)}")

    def get_template_resources(self, template_id: int, user_id: int) -> List[Dict]:
        """
        Obtiene los recursos de una plantilla con URLs temporales.

        Args:
            template_id: ID de la plantilla
            user_id: ID del usuario

        Returns:
            List[Dict]: Lista de recursos con URLs temporales
        """
        template = self.get_template_with_permissions(template_id, user_id, 'can_view')

        resources = []
        for resource in template.resources:
            url = self.s3_manager.get_resource_url(resource.resource_path)
            resources.append({
                'resource_id': resource.resource_id,
                'resource_type': resource.resource_type,
                'original_name': resource.original_name,
                'url': url
            })

        return resources