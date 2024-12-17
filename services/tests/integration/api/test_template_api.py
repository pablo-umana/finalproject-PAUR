import json
import pytest
from tests.factories.template_factory import TemplateFactory

class TestTemplateAPI:
    def test_get_templates(self, client, db_session):
        # Arrange
        templates = [TemplateFactory() for _ in range(3)]

        # Act
        response = client.get('/api/templates')
        data = json.loads(response.data)

        # Assert
        assert response.status_code == 200
        assert len(data) == 3
        assert data[0]['name'] == templates[0].name

    def test_create_template(self, client, db_session):
        # Arrange
        template_data = {
            'name': 'API Test Template',
            'description': 'Created via API',
            'content': {'sections': []}
        }

        # Act
        response = client.post(
            '/api/templates',
            data=json.dumps(template_data),
            content_type='application/json'
        )
        data = json.loads(response.data)

        # Assert
        assert response.status_code == 201
        assert data['name'] == template_data['name']