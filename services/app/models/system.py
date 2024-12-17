from app import db
from .mixins import TimestampMixin

class SystemSetting(TimestampMixin, db.Model):
    __tablename__ = 'system_settings'

    setting_id = db.Column(db.BigInteger, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    value_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

class AuditLog(TimestampMixin, db.Model):
    __tablename__ = 'audit_logs'

    log_id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'))
    action = db.Column(db.String(100), nullable=False)
    entity_type = db.Column(db.String(100), nullable=False)
    entity_id = db.Column(db.BigInteger, nullable=False)
    details_json = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))

    # Relaciones
    user = db.relationship('User')