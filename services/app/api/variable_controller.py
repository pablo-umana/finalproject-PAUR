from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.variable_service import VariableService
from app.schemas.variable_schema import (
    VariableSchema,
    VariableUpdateSchema,
    VariableResponseSchema,
    VariableBulkCreateSchema,
    PredefinedVariableSchema
)
from app.utils.decorators import jwt_required
from app.utils.exceptions import NotFoundException, ValidationError as AppValidationError

# Crear blueprint
variables_bp = Blueprint('variables', __name__)
variable_service = VariableService()

# Schemas
variable_schema = VariableSchema()
variable_response_schema = VariableResponseSchema()
variables_response_schema = VariableResponseSchema(many=True)
bulk_create_schema = VariableBulkCreateSchema()
predefined_schema = PredefinedVariableSchema(many=True)

@variables_bp.route('/variables', methods=['GET'])
@jwt_required()
def get_variables():
    """Obtiene todas las variables, opcionalmente filtradas por plantilla."""
    try:
        template_id = request.args.get('template_id', type=int)
        variables = variable_service.get_all_variables(template_id)
        return jsonify({
            'success': True,
            'data': variables_response_schema.dump(variables)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@variables_bp.route('/variables/<int:variable_id>', methods=['GET'])
@jwt_required()
def get_variable(variable_id):
    """Obtiene una variable específica por su ID."""
    try:
        variable = variable_service.get_variable(variable_id)
        return jsonify({
            'success': True,
            'data': variable_response_schema.dump(variable)
        }), 200
    except NotFoundException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@variables_bp.route('/variables', methods=['POST'])
@jwt_required(['admin', 'template_editor'])
def create_variable():
    """Crea una nueva variable."""
    try:
        data = request.get_json()
        variable = variable_service.create_variable(data)
        return jsonify({
            'success': True,
            'data': variable_response_schema.dump(variable),
            'message': 'Variable creada exitosamente'
        }), 201
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'Error de validación',
            'details': e.messages
        }), 400
    except AppValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@variables_bp.route('/variables/<int:variable_id>', methods=['PUT'])
@jwt_required(['admin', 'template_editor'])
def update_variable(variable_id):
    """Actualiza una variable existente."""
    try:
        data = request.get_json()
        variable = variable_service.update_variable(variable_id, data)
        return jsonify({
            'success': True,
            'data': variable_response_schema.dump(variable),
            'message': 'Variable actualizada exitosamente'
        }), 200
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'Error de validación',
            'details': e.messages
        }), 400
    except (NotFoundException, AppValidationError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404 if isinstance(e, NotFoundException) else 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@variables_bp.route('/variables/<int:variable_id>', methods=['DELETE'])
@jwt_required(['admin', 'template_editor'])
def delete_variable(variable_id):
    """Elimina una variable."""
    try:
        variable_service.delete_variable(variable_id)
        return jsonify({
            'success': True,
            'message': 'Variable eliminada exitosamente'
        }), 200
    except NotFoundException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@variables_bp.route('/templates/<int:template_id>/variables/bulk', methods=['POST'])
@jwt_required(['admin', 'template_editor'])
def bulk_create_variables(template_id):
    """Crea múltiples variables para una plantilla."""
    try:
        data = request.get_json()
        variables = variable_service.bulk_create_variables(template_id, data.get('variables', []))
        return jsonify({
            'success': True,
            'data': variables_response_schema.dump(variables),
            'message': 'Variables creadas exitosamente'
        }), 201
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'Error de validación',
            'details': e.messages
        }), 400
    except AppValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@variables_bp.route('/variables/predefined', methods=['GET'])
@jwt_required()
def get_predefined_variables():
    """Obtiene la lista de variables predefinidas del sistema."""
    try:
        variables = variable_service.get_predefined_variables()
        return jsonify({
            'success': True,
            'data': predefined_schema.dump(variables)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@variables_bp.route('/variables/type/<string:variable_type>', methods=['GET'])
@jwt_required()
def get_variables_by_type(variable_type):
    """Obtiene variables por tipo."""
    try:
        template_id = request.args.get('template_id', type=int)
        variables = variable_service.get_variables_by_type(variable_type, template_id)
        return jsonify({
            'success': True,
            'data': variables_response_schema.dump(variables)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500