from app import db
from .mixins import TimestampMixin, UserTrackingMixin

class Template(TimestampMixin, UserTrackingMixin, db.Model):
    __tablename__ = 'templates'

    template_id = db.Column(db.BigInteger, primary_key=True)
    category_id = db.Column(db.BigInteger, db.ForeignKey('template_categories.category_id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relaciones
    category = db.relationship('TemplateCategory', back_populates='templates')
    versions = db.relationship('TemplateVersion', back_populates='template', order_by='desc(TemplateVersion.version_number)')
    resources = db.relationship('TemplateResource', back_populates='template')
    variables = db.relationship('TemplateVariable', back_populates='template')
    permissions = db.relationship('TemplatePermission', back_populates='template')
    signature_config = db.relationship('TemplateSignatureConfig', back_populates='template', uselist=False)

class TemplateCategory(db.Model):
    __tablename__ = 'template_categories'

    category_id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relaciones
    templates = db.relationship('Template', back_populates='category')