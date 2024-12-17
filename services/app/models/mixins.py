from datetime import datetime
from app import db

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class UserTrackingMixin:
    created_by = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    updated_by = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=True)