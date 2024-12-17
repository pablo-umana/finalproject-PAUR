from typing import List, Optional, Dict
from datetime import datetime
from app.repositories.variable_repository import VariableRepository
from app.models.template_components import TemplateVariable
from app.utils.exceptions import ValidationError, NotFoundException
from app.schemas.variable_schema import VariableSchema, VariableUpdateSchema

class VariableService:
    """Servicio para la gestión de variables de plantillas."""

    # Variables predefinidas del sistema
    PREDEFINED_VARIABLES = {
        'fecha_actual': {
            'name': 'fecha_actual',
            'description': 'Fecha actual del sistema',
            'variable_type': 'date',
            'format': 'DD/MM/YYYY',
            'example': datetime.now().strftime('%d/%m/%Y')
        },
        'hora_actual': {
            'name': 'hora_actual',
            'description': 'Hora actual del sistema',
            'variable_type': 'text',
            'format': 'HH:mm:ss',
            'example': datetime.now().strftime('%H:%M:%S')
        },
        'usuario_nombre': {
            'name': 'usuario_nombre',
            'description': 'Nombre del usuario actual',
            'variable_type': 'text',
            'format': None,
            'example': 'Juan Pérez'
        }
    }

    def __init__(self):
        self.repository = VariableRepository()
        self.schema = VariableSchema()

    def get_all_variables(self, template_id: Optional[int] = None) -> List[TemplateVariable]:
        """Obtiene todas las variables, opcionalmente filtradas por plantilla."""
        if template_id:
            return self.repository.find_by_template_id(template_id)
        return self.repository.get_all()

    def get_variable(self, variable_id: int) -> TemplateVariable:
        """Obtiene una variable por su ID."""
        variable = self.repository.get_by_id(variable_id)
        if not variable:
            raise NotFoundException(f"Variable con ID {variable_id} no encontrada")
        return variable

    def create_variable(self, data: Dict) -> TemplateVariable:
        """Crea una nueva variable."""
        # Validar datos usando el schema
        errors = self.schema.validate(data)
        if errors:
            raise ValidationError(str(errors))

        # Validar nombre único en la plantilla
        self.repository.validate_unique_name(data['name'], data['template_id'])

        # Crear la variable
        variable = TemplateVariable(**data)
        return self.repository.create(variable)

    def update_variable(self, variable_id: int, data: Dict) -> TemplateVariable:
        """Actualiza una variable existente."""
        variable = self.get_variable(variable_id)

        # Validar datos usando el schema de actualización
        update_schema = VariableUpdateSchema()
        errors = update_schema.validate(data)
        if errors:
            raise ValidationError(str(errors))

        # Actualizar campos permitidos
        for key, value in data.items():
            if hasattr(variable, key) and key not in ['template_id', 'name']:
                setattr(variable, key, value)

        return self.repository.update(variable)

    def delete_variable(self, variable_id: int) -> None:
        """Elimina una variable."""
        variable = self.get_variable(variable_id)
        self.repository.delete(variable)

    def bulk_create_variables(self, template_id: int, variables_data: List[Dict]) -> List[TemplateVariable]:
        """Crea múltiples variables para una plantilla."""
        variables = []
        for data in variables_data:
            data['template_id'] = template_id
            errors = self.schema.validate(data)
            if errors:
                raise ValidationError(f"Error en variable '{data.get('name')}': {str(errors)}")
            variables.append(TemplateVariable(**data))

        return self.repository.bulk_create(variables)

    def get_predefined_variables(self) -> List[Dict]:
        """Obtiene la lista de variables predefinidas del sistema."""
        return list(self.PREDEFINED_VARIABLES.values())

    def get_variables_by_type(self, variable_type: str, template_id: Optional[int] = None) -> List[TemplateVariable]:
        """Obtiene variables por tipo."""
        return self.repository.find_by_type(variable_type, template_id)

    def validate_variable_value(self, variable: TemplateVariable, value: str) -> bool:
        """Valida un valor contra las reglas de una variable."""
        if variable.required and not value:
            raise ValidationError(f"La variable '{variable.name}' es requerida")

        if not value:
            return True

        if not variable.validation_rules:
            return True

        for rule in variable.validation_rules:
            rule_type = rule['type']
            params = rule['params']

            if rule_type == 'length':
                if len(value) < params.get('min', 0) or len(value) > params.get('max', float('inf')):
                    raise ValidationError(rule['message'])

            elif rule_type == 'range':
                try:
                    num_value = float(value)
                    if num_value < params.get('min', float('-inf')) or num_value > params.get('max', float('inf')):
                        raise ValidationError(rule['message'])
                except ValueError:
                    raise ValidationError("El valor debe ser numérico")

            # Aquí se pueden agregar más validaciones según los tipos definidos

        return True