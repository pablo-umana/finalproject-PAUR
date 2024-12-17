import pytest
from app.models.template_components import TemplateVariable
from app.services.variable_service import VariableService
from app.repositories.variable_repository import VariableRepository
from app.utils.exceptions import ValidationError, NotFoundException

@pytest.fixture
def variable_service():
    return VariableService()

@pytest.fixture
def mock_variable():
    return {
        'template_id': 1,
        'name': 'test_variable',
        'variable_type': 'text',
        'required': True,
        'default_value': 'test',
        'validation_rules': [
            {
                'type': 'length',
                'params': {'min': 1, 'max': 100},
                'message': 'Longitud inválida'
            }
        ]
    }

class TestVariableService:
    def test_create_variable_success(self, variable_service, mock_variable):
        """Test creación exitosa de variable."""
        variable = variable_service.create_variable(mock_variable)
        assert variable.name == mock_variable['name']
        assert variable.variable_type == mock_variable['variable_type']

    def test_create_variable_invalid_name(self, variable_service):
        """Test validación de nombre inválido."""
        invalid_variable = {
            'template_id': 1,
            'name': '123invalid',  # Debe empezar con letra
            'variable_type': 'text'
        }
        with pytest.raises(ValidationError):
            variable_service.create_variable(invalid_variable)

    def test_create_variable_duplicate_name(self, variable_service, mock_variable):
        """Test validación de nombre duplicado."""
        variable_service.create_variable(mock_variable)
        with pytest.raises(ValidationError):
            variable_service.create_variable(mock_variable)

    def test_update_variable_success(self, variable_service, mock_variable):
        """Test actualización exitosa de variable."""
        variable = variable_service.create_variable(mock_variable)
        update_data = {'default_value': 'new_value'}
        updated = variable_service.update_variable(variable.variable_id, update_data)
        assert updated.default_value == 'new_value'

    def test_delete_variable_success(self, variable_service, mock_variable):
        """Test eliminación exitosa de variable."""
        variable = variable_service.create_variable(mock_variable)
        variable_service.delete_variable(variable.variable_id)
        with pytest.raises(NotFoundException):
            variable_service.get_variable(variable.variable_id)

    def test_get_predefined_variables(self, variable_service):
        """Test obtención de variables predefinidas."""
        variables = variable_service.get_predefined_variables()
        assert len(variables) > 0
        assert 'fecha_actual' in [v['name'] for v in variables]

    def test_validate_variable_value(self, variable_service, mock_variable):
        """Test validación de valores de variable."""
        variable = variable_service.create_variable(mock_variable)

        # Test valor válido
        assert variable_service.validate_variable_value(variable, 'valid value') == True

        # Test valor requerido
        with pytest.raises(ValidationError):
            variable_service.validate_variable_value(variable, '')

        # Test longitud inválida
        with pytest.raises(ValidationError):
            variable_service.validate_variable_value(variable, 'a' * 101)

class TestVariableRepository:
    def test_find_by_template_id(self, variable_service, mock_variable):
        """Test búsqueda por template_id."""
        variable = variable_service.create_variable(mock_variable)
        variables = variable_service.repository.find_by_template_id(mock_variable['template_id'])
        assert len(variables) > 0
        assert variables[0].template_id == mock_variable['template_id']

    def test_find_by_type(self, variable_service, mock_variable):
        """Test búsqueda por tipo."""
        variable = variable_service.create_variable(mock_variable)
        variables = variable_service.repository.find_by_type(mock_variable['variable_type'])
        assert len(variables) > 0
        assert variables[0].variable_type == mock_variable['variable_type']

    def test_bulk_create(self, variable_service):
        """Test creación en lote."""
        variables_data = [
            {
                'template_id': 1,
                'name': 'var1',
                'variable_type': 'text'
            },
            {
                'template_id': 1,
                'name': 'var2',
                'variable_type': 'number'
            }
        ]
        variables = variable_service.bulk_create_variables(1, variables_data)
        assert len(variables) == 2