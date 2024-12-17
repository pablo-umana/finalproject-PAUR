import pytest
from app.services.template_service import TemplateService
from app.utils.exceptions import NotFoundException
from tests.factories.template_factory import TemplateFactory

class TestTemplateService:
    @pytest.fixture
    def service(self):
        return TemplateService()

    def test_get_template_success(self, service, db_session):
        # Arrange
        template = TemplateFactory()

        # Act
        result = service.get_template(template.id)

        # Assert
        assert result.id == template.id
        assert result.name == template.name

    def test_get_template_not_found(self, service):
        # Arrange
        non_existent_id = 99999

        # Act & Assert
        with pytest.raises(NotFoundException) as exc:
            service.get_template(non_existent_id)
        assert str(exc.value) == f"Template with id {non_existent_id} not found"

    def test_create_template_success(self, service, db_session):
        # Arrange
        template_data = {
            'name': 'New Template',
            'description': 'Test description',
            'content': {'sections': []}
        }

        # Act
        result = service.create_template(template_data)

        # Assert
        assert result.name == template_data['name']
        assert result.description == template_data['description']