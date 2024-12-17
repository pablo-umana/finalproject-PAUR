from typing import List, Optional
from app.models.template import Template
from app.repositories.template_repository import TemplateRepository
from app.schemas.template_schema import TemplateSchema
from app.utils.exceptions import NotFoundException

class TemplateService:
    def __init__(self):
        self.repository = TemplateRepository()
        self.schema = TemplateSchema()

    def get_template(self, template_id: int) -> Template:
        template = self.repository.get_by_id(template_id)
        if not template:
            raise NotFoundException(f"Template with id {template_id} not found")
        return template

    def create_template(self, template_data: dict) -> Template:
        template = Template(**template_data)
        return self.repository.create(template)

    def update_template(self, template_id: int, template_data: dict) -> Template:
        template = self.get_template(template_id)
        for key, value in template_data.items():
            setattr(template, key, value)
        return self.repository.update(template)

    def delete_template(self, template_id: int) -> None:
        template = self.get_template(template_id)
        self.repository.delete(template)