from app import db
from .mixins import TimestampMixin

class GeneratedDocument(TimestampMixin, db.Model):
    __tablename__ = 'generated_documents'

    document_id = db.Column(db.BigInteger, primary_key=True)
    template_id = db.Column(db.BigInteger, db.ForeignKey('templates.template_id'), nullable=False)
    version_id = db.Column(db.BigInteger, db.ForeignKey('template_versions.version_id'), nullable=False)
    generated_by = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    variables_json = db.Column(db.JSON, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    output_path = db.Column(db.String(255))
    completed_at = db.Column(db.DateTime)

    # Relaciones
    template = db.relationship('Template')
    version = db.relationship('TemplateVersion')
    user = db.relationship('User')
    queue_items = db.relationship('DocumentQueue', back_populates='document')

class DocumentQueue(TimestampMixin, db.Model):
    __tablename__ = 'document_queue'

    queue_id = db.Column(db.BigInteger, primary_key=True)
    document_id = db.Column(db.BigInteger, db.ForeignKey('generated_documents.document_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    error_message = db.Column(db.Text)
    retry_count = db.Column(db.Integer, default=0, nullable=False)
    next_retry = db.Column(db.DateTime)

    # Relaciones
    document = db.relationship('GeneratedDocument', back_populates='queue_items')