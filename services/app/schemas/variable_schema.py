from marshmallow import Schema, fields, validate, validates, ValidationError
from typing import List

class ValidationRuleSchema(Schema):
    """Schema para las reglas de validación de variables."""
    type = fields.Str(required=True, validate=validate.OneOf([
        'length', 'range', 'regex', 'enum', 'email', 'rut', 'date', 'currency'
    ]))
    params = fields.Dict(required=True)
    message = fields.Str(required=True)

class VariableSchema(Schema):
    """Schema principal para variables de plantilla."""
    variable_id = fields.Int(dump_only=True)
    template_id = fields.Int(required=True)
    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=50),
            validate.Regexp(
                '^[a-zA-Z][a-zA-Z0-9_]*$',
                error='El nombre debe comenzar con una letra y solo puede contener letras, números y guiones bajos'
            )
        ]
    )
    default_value = fields.Str(allow_none=True)
    required = fields.Bool(default=False)
    variable_type = fields.Str(
        required=True,
        validate=validate.OneOf([
            'text', 'number', 'date', 'email', 'rut', 'currency', 'enum'
        ])
    )
    validation_rules = fields.Nested(
        ValidationRuleSchema,
        many=True,
        allow_none=True
    )

    @validates('validation_rules')
    def validate_rules(self, value: List[dict]) -> None:
        """Valida que las reglas sean consistentes con el tipo de variable."""
        if not value:
            return

        valid_rules = {
            'text': ['length', 'regex', 'enum'],
            'number': ['range'],
            'date': ['range'],
            'email': ['email'],
            'rut': ['rut'],
            'currency': ['range', 'currency'],
            'enum': ['enum']
        }

        variable_type = self.context.get('variable_type')
        if not variable_type:
            return

        allowed_rules = valid_rules.get(variable_type, [])
        for rule in value:
            if rule['type'] not in allowed_rules:
                raise ValidationError(
                    f"La regla '{rule['type']}' no es válida para variables de tipo '{variable_type}'"
                )

class VariableUpdateSchema(VariableSchema):
    """Schema para actualización de variables."""
    template_id = fields.Int(dump_only=True)  # No permitir cambiar el template_id
    name = fields.Str(dump_only=True)  # No permitir cambiar el nombre

class VariableResponseSchema(VariableSchema):
    """Schema para respuestas de API."""
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class VariableBulkCreateSchema(Schema):
    """Schema para creación en lote de variables."""
    variables = fields.Nested(VariableSchema, many=True, required=True)

# Schemas para variables predefinidas
class PredefinedVariableSchema(Schema):
    """Schema para variables predefinidas del sistema."""
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    variable_type = fields.Str(required=True)
    format = fields.Str(allow_none=True)
    example = fields.Str(required=True)