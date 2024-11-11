from app import db
import datetime

class Payment(db.Model):
    __tablename__ = 'payments'
    # Atributos propios
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id: int = db.Column(db.Integer, nullable=False)
    price: float = db.Column(db.Float, nullable=False)
    payment_method: str = db.Column(db.String(64), nullable=False)
    deleted_at: datetime = db.Column(db.DateTime, nullable=True)