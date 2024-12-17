from typing import List, Dict, Optional
from app.models.template_components import TemplatePermission
from app.models.auth import Role, User
from app.utils.exceptions import ValidationError, NotFoundException
from app import db

class TemplatePermissionService:
    def __init__(self):
        self.valid_permissions = {'can_view', 'can_edit', 'can_generate'}

    def assign_permissions(self, template_id: int, permissions: List[dict]) -> None:
        """
        Asigna permisos a una plantilla.

        Args:
            template_id: ID de la plantilla
            permissions: Lista de diccionarios con los permisos a asignar
                [
                    {
                        'role_id': int,
                        'can_view': bool,
                        'can_edit': bool,
                        'can_generate': bool
                    }
                ]

        Raises:
            ValidationError: Si hay errores en los datos de permisos
            NotFoundException: Si no existe el rol o la plantilla
        """
        try:
            # Eliminar permisos existentes
            TemplatePermission.query.filter_by(template_id=template_id).delete()

            # Crear nuevos permisos
            for permission_data in permissions:
                # Validar que el rol existe
                role_id = permission_data.get('role_id')
                if not Role.query.get(role_id):
                    raise NotFoundException(f"El rol con ID {role_id} no existe")

                # Validar permisos
                self._validate_permission_data(permission_data)

                # Crear permiso
                permission = TemplatePermission(
                    template_id=template_id,
                    role_id=role_id,
                    can_view=permission_data.get('can_view', False),
                    can_edit=permission_data.get('can_edit', False),
                    can_generate=permission_data.get('can_generate', False)
                )
                db.session.add(permission)

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            if isinstance(e, (ValidationError, NotFoundException)):
                raise e
            raise ValidationError(f"Error al asignar permisos: {str(e)}")

    def check_permission(self, template_id: int, user_id: int, permission_type: str) -> bool:
        """
        Verifica si un usuario tiene un permiso específico sobre una plantilla.

        Args:
            template_id: ID de la plantilla
            user_id: ID del usuario
            permission_type: Tipo de permiso a verificar ('can_view', 'can_edit', 'can_generate')

        Returns:
            bool: True si tiene el permiso

        Raises:
            ValidationError: Si el tipo de permiso no es válido
        """
        # Validar tipo de permiso
        if permission_type not in self.valid_permissions:
            raise ValidationError(f"Tipo de permiso inválido: {permission_type}")

        # Obtener usuario y sus roles
        user = User.query.get(user_id)
        if not user:
            return False

        # Administrador tiene todos los permisos
        if any(role.name == 'admin' for role in user.roles):
            return True

        # Verificar permisos por rol
        role_ids = [role.role_id for role in user.roles]
        permission = TemplatePermission.query.filter(
            TemplatePermission.template_id == template_id,
            TemplatePermission.role_id.in_(role_ids)
        ).first()

        return bool(permission and getattr(permission, permission_type, False))

    def get_template_permissions(self, template_id: int) -> List[Dict]:
        """
        Obtiene todos los permisos asignados a una plantilla.

        Args:
            template_id: ID de la plantilla

        Returns:
            Lista de diccionarios con los permisos
        """
        permissions = TemplatePermission.query.filter_by(template_id=template_id).all()
        return [
            {
                'role_id': p.role_id,
                'role_name': Role.query.get(p.role_id).name,
                'can_view': p.can_view,
                'can_edit': p.can_edit,
                'can_generate': p.can_generate
            }
            for p in permissions
        ]

    def get_user_permissions(self, user_id: int) -> Dict[int, Dict[str, bool]]:
        """
        Obtiene todos los permisos de un usuario sobre todas las plantillas.

        Args:
            user_id: ID del usuario

        Returns:
            Diccionario con los permisos por plantilla
            {
                template_id: {
                    'can_view': bool,
                    'can_edit': bool,
                    'can_generate': bool
                }
            }
        """
        user = User.query.get(user_id)
        if not user:
            return {}

        # Si es admin, tiene todos los permisos
        if any(role.name == 'admin' for role in user.roles):
            return {
                template.template_id: {
                    'can_view': True,
                    'can_edit': True,
                    'can_generate': True
                }
                for template in Template.query.all()
            }

        # Obtener permisos por rol
        role_ids = [role.role_id for role in user.roles]
        permissions = TemplatePermission.query.filter(
            TemplatePermission.role_id.in_(role_ids)
        ).all()

        # Consolidar permisos por plantilla
        template_permissions = {}
        for permission in permissions:
            if permission.template_id not in template_permissions:
                template_permissions[permission.template_id] = {
                    'can_view': False,
                    'can_edit': False,
                    'can_generate': False
                }

            # Actualizar permisos (OR lógico entre roles)
            current = template_permissions[permission.template_id]
            current['can_view'] |= permission.can_view
            current['can_edit'] |= permission.can_edit
            current['can_generate'] |= permission.can_generate

        return template_permissions

    def _validate_permission_data(self, permission_data: dict) -> None:
        """
        Valida los datos de un permiso.

        Args:
            permission_data: Diccionario con los datos del permiso

        Raises:
            ValidationError: Si los datos son inválidos
        """
        required_fields = {'role_id'}
        missing_fields = required_fields - set(permission_data.keys())
        if missing_fields:
            raise ValidationError(f"Faltan campos requeridos: {', '.join(missing_fields)}")

        # Validar que al menos un permiso está establecido
        has_permissions = any(
            permission_data.get(perm, False)
            for perm in self.valid_permissions
        )
        if not has_permissions:
            raise ValidationError("Debe establecer al menos un permiso")
