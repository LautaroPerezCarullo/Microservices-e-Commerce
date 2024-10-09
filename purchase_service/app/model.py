from app import db


class Purchase(db.Model):
    __tablename__ = 'purchases'
    # Atributos propios
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id: int = db.Column(db.Integer, nullable=False)
    purchase_date: str = db.Column(db.DateTime, nullable=False)
    delivery_address: str = db.Column(db.String(64), nullable=False)