from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError as SchemaValidationError
from app.services.template_service import TemplateService
from app.schemas.template_schema import (
    TemplateSchema,
    TemplateCreateSchema,
    TemplateUpdateSchema,
    TemplateVersionSchema,
    TemplateResourceSchema
)
from app.utils.exceptions import ValidationError, NotFoundException
from app.utils.decorators import jwt_required
from flask_jwt_extended import get_jwt_identity

templates_bp = Blueprint('templates', __name__)
template_service = TemplateService()

# Schemas
template_schema = TemplateSchema()
templates_schema = TemplateSchema(many=True)
template_create_schema = TemplateCreateSchema()
template_update_schema = TemplateUpdateSchema()
version_schema = TemplateVersionSchema()
versions_schema = TemplateVersionSchema(many=True)
resource_schema = TemplateResourceSchema(many=True)

@templates_bp.route('/templates', methods=['GET'])
@jwt_required()
def get_templates():
    """Lista todas las plantillas a las que el usuario tiene acceso."""
    try:
        user_id = get_jwt_identity()
        templates = template_service.get_templates_for_user(user_id)
        return jsonify({
            'success': True,
            'data': templates_schema.dump(templates)
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error al obtener plantillas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener plantillas'
        }), 500

@templates_bp.route('/templates/<int:template_id>', methods=['GET'])
@jwt_required()
def get_template(template_id):
    """Obtiene una plantilla específica."""
    try:
        user_id = get_jwt_identity()
        template = template_service.get_template_with_permissions(template_id, user_id, 'can_view')
        return jsonify({
            'success': True,
            'data': template_schema.dump(template)
        }), 200
    except NotFoundException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 403
    except Exception as e:
        current_app.logger.error(f"Error al obtener plantilla: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener plantilla'
        }), 500

@templates_bp.route('/templates', methods=['POST'])
@jwt_required(['admin', 'template_editor'])
def create_template():
    """Crea una nueva plantilla."""
    try:
        data = request.get_json()
        errors = template_create_schema.validate(data)
        if errors:
            return jsonify({
                'success': False,
                'error': 'Datos inválidos',
                'details': errors
            }), 400

        user_id = get_jwt_identity()
        template = template_service.create_template(data, user_id)

        return jsonify({
            'success': True,
            'data': template_schema.dump(template),
            'message': 'Plantilla creada exitosamente'
        }), 201
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        current_app.logger.error(f"Error al crear plantilla: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al crear plantilla'
        }), 500

@templates_bp.route('/templates/<int:template_id>', methods=['PUT'])
@jwt_required(['admin', 'template_editor'])
def update_template(template_id):
    """Actualiza una plantilla existente."""
    try:
        data = request.get_json()
        errors = template_update_schema.validate(data)
        if errors:
            return jsonify({
                'success': False,
                'error': 'Datos inválidos',
                'details': errors
            }), 400

        user_id = get_jwt_identity()
        template = template_service.update_template(template_id, data, user_id)

        return jsonify({
            'success': True,
            'data': template_schema.dump(template),
            'message': 'Plantilla actualizada exitosamente'
        }), 200
    except (NotFoundException, ValidationError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404 if isinstance(e, NotFoundException) else 400
    except Exception as e:
        current_app.logger.error(f"Error al actualizar plantilla: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al actualizar plantilla'
        }), 500

@templates_bp.route('/templates/<int:template_id>', methods=['DELETE'])
@jwt_required(['admin', 'template_editor'])
def delete_template(template_id):
    """Elimina una plantilla."""
    try:
        user_id = get_jwt_identity()
        template_service.delete_template(template_id, user_id)
        return jsonify({
            'success': True,
            'message': 'Plantilla eliminada exitosamente'
        }), 200
    except (NotFoundException, ValidationError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404 if isinstance(e, NotFoundException) else 400
    except Exception as e:
        current_app.logger.error(f"Error al eliminar plantilla: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al eliminar plantilla'
        }), 500

@templates_bp.route('/templates/<int:template_id>/versions', methods=['POST'])
@jwt_required(['admin', 'template_editor'])
def create_template_version(template_id):
    """Crea una nueva versión de la plantilla."""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        version = template_service.create_version(template_id, data.get('content'), user_id)

        return jsonify({
            'success': True,
            'data': version_schema.dump(version),
            'message': 'Versión creada exitosamente'
        }), 201
    except (NotFoundException, ValidationError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404 if isinstance(e, NotFoundException) else 400
    except Exception as e:
        current_app.logger.error(f"Error al crear versión: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al crear versión'
        }), 500

@templates_bp.route('/templates/<int:template_id>/versions', methods=['GET'])
@jwt_required()
def get_template_versions(template_id):
    """Obtiene todas las versiones de una plantilla."""
    try:
        user_id = get_jwt_identity()
        versions = template_service.get_template_versions(template_id, user_id)
        return jsonify({
            'success': True,
            'data': versions_schema.dump(versions)
        }), 200
    except (NotFoundException, ValidationError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404 if isinstance(e, NotFoundException) else 400
    except Exception as e:
        current_app.logger.error(f"Error al obtener versiones: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener versiones'
        }), 500

@templates_bp.route('/templates/<int:template_id>/resources', methods=['POST'])
@jwt_required(['admin', 'template_editor'])
def upload_template_resource(template_id):
    """Sube un nuevo recurso para la plantilla."""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ningún archivo'
            }), 400

        file = request.files['file']
        if not file.filename:
            return jsonify({
                'success': False,
                'error': 'Nombre de archivo vacío'
            }), 400

        user_id = get_jwt_identity()
        resource_data = {
            'file_data': file.read(),
            'original_name': file.filename,
            'resource_type': request.form.get('resource_type', 'image')
        }

        resources = template_service.manage_resources(template_id, [resource_data])
        return jsonify({
            'success': True,
            'data': resource_schema.dump(resources),
            'message': 'Recurso subido exitosamente'
        }), 201
    except (NotFoundException, ValidationError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404 if isinstance(e, NotFoundException) else 400
    except Exception as e:
        current_app.logger.error(f"Error al subir recurso: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al subir recurso'
        }), 500

@templates_bp.route('/templates/<int:template_id>/resources', methods=['GET'])
@jwt_required()
def get_template_resources(template_id):
    """Obtiene todos los recursos de una plantilla."""
    try:
        user_id = get_jwt_identity()
        resources = template_service.get_template_resources(template_id, user_id)
        return jsonify({
            'success': True,
            'data': resources
        }), 200
    except (NotFoundException, ValidationError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404 if isinstance(e, NotFoundException) else 400
    except Exception as e:
        current_app.logger.error(f"Error al obtener recursos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error al obtener recursos'
        }), 500