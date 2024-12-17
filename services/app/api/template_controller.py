from flask import Blueprint, request, jsonify
from app.services.template_service import TemplateService
from app.schemas.template_schema import TemplateSchema
from app.utils.exceptions import NotFoundException

templates_bp = Blueprint('templates', __name__)
template_service = TemplateService()
template_schema = TemplateSchema()

@templates_bp.route('/templates', methods=['GET'])
def get_templates():
    templates = template_service.get_all_templates()
    return jsonify(template_schema.dump(templates, many=True)), 200

@templates_bp.route('/templates/<int:template_id>', methods=['GET'])
def get_template(template_id):
    try:
        template = template_service.get_template(template_id)
        return jsonify(template_schema.dump(template)), 200
    except NotFoundException as e:
        return jsonify({'error': str(e)}), 404

@templates_bp.route('/templates', methods=['POST'])
def create_template():
    template_data = request.get_json()
    errors = template_schema.validate(template_data)
    if errors:
        return jsonify({'errors': errors}), 400

    template = template_service.create_template(template_data)
    return jsonify(template_schema.dump(template)), 201