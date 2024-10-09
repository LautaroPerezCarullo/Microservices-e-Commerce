from app import db

class Payment(db.Model):
    __tablename__ = 'payments'
    # Atributos propios
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id: int = db.Column(db.Integer, nullable=False)
    price: float = db.Column(db.Float, nullable=False)
    payment_method: str = db.Column(db.String(64), nullable=False)