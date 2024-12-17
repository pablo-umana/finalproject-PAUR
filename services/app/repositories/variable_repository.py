from typing import List, Optional
from sqlalchemy import and_
from app.models.template_components import TemplateVariable
from app.repositories.base_repository import BaseRepository
from app.utils.exceptions import ValidationError

class VariableRepository(BaseRepository[TemplateVariable]):
    def __init__(self):
        super().__init__(TemplateVariable)

    def find_by_template_id(self, template_id: int) -> List[TemplateVariable]:
        """Obtiene todas las variables asociadas a una plantilla."""
        return TemplateVariable.query.filter_by(template_id=template_id).all()

    def find_by_name_and_template(self, name: str, template_id: int) -> Optional[TemplateVariable]:
        """Busca una variable por nombre dentro de una plantilla específica."""
        return TemplateVariable.query.filter_by(
            name=name,
            template_id=template_id
        ).first()

    def find_by_type(self, variable_type: str, template_id: Optional[int] = None) -> List[TemplateVariable]:
        """Busca variables por tipo, opcionalmente filtradas por plantilla."""
        filters = [TemplateVariable.variable_type == variable_type]
        if template_id:
            filters.append(TemplateVariable.template_id == template_id)
        return TemplateVariable.query.filter(and_(*filters)).all()

    def validate_unique_name(self, name: str, template_id: int, variable_id: Optional[int] = None) -> bool:
        """
        Valida que el nombre de la variable sea único en la plantilla.
        Si se proporciona variable_id, excluye esa variable de la validación (útil para updates).
        """
        query = TemplateVariable.query.filter_by(
            name=name,
            template_id=template_id
        )

        if variable_id:
            query = query.filter(TemplateVariable.variable_id != variable_id)

        existing_variable = query.first()

        if existing_variable:
            raise ValidationError(f"Ya existe una variable con el nombre '{name}' en esta plantilla")
        return True

    def bulk_create(self, variables: List[TemplateVariable]) -> List[TemplateVariable]:
        """Crea múltiples variables en una sola transacción."""
        try:
            for variable in variables:
                self.validate_unique_name(variable.name, variable.template_id)
            return super().bulk_create(variables)
        except Exception as e:
            raise ValidationError(f"Error al crear variables en lote: {str(e)}")

    def update_validation_rules(self, variable_id: int, validation_rules: dict) -> TemplateVariable:
        """Actualiza las reglas de validación de una variable."""
        variable = self.get_by_id(variable_id)
        if not variable:
            raise ValidationError(f"Variable con id {variable_id} no encontrada")

        variable.validation_rules = validation_rules
        return self.update(variable)