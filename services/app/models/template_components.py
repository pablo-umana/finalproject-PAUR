from app import db
from .mixins import TimestampMixin, UserTrackingMixin

class TemplateVersion(TimestampMixin, UserTrackingMixin, db.Model):
    __tablename__ = 'template_versions'

    version_id = db.Column(db.BigInteger, primary_key=True)
    template_id = db.Column(db.BigInteger, db.ForeignKey('templates.template_id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.JSON, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relaciones
    template = db.relationship('Template', back_populates='versions')

    __table_args__ = (
        db.UniqueConstraint('template_id', 'version_number', name='uq_template_version'),
    )

class TemplateResource(TimestampMixin, db.Model):
    __tablename__ = 'template_resources'

    resource_id = db.Column(db.BigInteger, primary_key=True)
    template_id = db.Column(db.BigInteger, db.ForeignKey('templates.template_id'), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)
    resource_path = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    size_bytes = db.Column(db.Integer, nullable=False)

    # Relaciones
    template = db.relationship('Template', back_populates='resources')

class TemplateVariable(db.Model):
    __tablename__ = 'template_variables'

    variable_id = db.Column(db.BigInteger, primary_key=True)
    template_id = db.Column(db.BigInteger, db.ForeignKey('templates.template_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    default_value = db.Column(db.String(255))
    required = db.Column(db.Boolean, default=False, nullable=False)
    variable_type = db.Column(db.String(50), nullable=False)
    validation_rules = db.Column(db.JSON)

    # Relaciones
    template = db.relationship('Template', back_populates='variables')

class TemplatePermission(db.Model):
    __tablename__ = 'template_permissions'

    permission_id = db.Column(db.BigInteger, primary_key=True)
    template_id = db.Column(db.BigInteger, db.ForeignKey('templates.template_id'), nullable=False)
    role_id = db.Column(db.BigInteger, db.ForeignKey('roles.role_id'), nullable=False)
    can_view = db.Column(db.Boolean, default=False, nullable=False)
    can_edit = db.Column(db.Boolean, default=False, nullable=False)
    can_generate = db.Column(db.Boolean, default=False, nullable=False)

    # Relaciones
    template = db.relationship('Template', back_populates='permissions')
    role = db.relationship('Role')

class TemplateSignatureConfig(TimestampMixin, db.Model):
    __tablename__ = 'template_signature_config'

    config_id = db.Column(db.BigInteger, primary_key=True)
    template_id = db.Column(db.BigInteger, db.ForeignKey('templates.template_id'), nullable=False, unique=True)
    signature_count = db.Column(db.Integer, default=0, nullable=False)
    coordinates_json = db.Column(db.JSON)
    require_sequential = db.Column(db.Boolean, default=False, nullable=False)

    # Relaciones
    template = db.relationship('Template', back_populates='signature_config')