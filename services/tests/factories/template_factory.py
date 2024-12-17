import factory
from app.models.template import Template
from app import db

class TemplateFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Template
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.Sequence(lambda n: f'Template {n}')
    description = factory.Faker('text')
    content = factory.LazyFunction(lambda: {
        'sections': [
            {
                'type': 'header',
                'content': 'Test Header'
            }
        ]
    })
    is_active = True