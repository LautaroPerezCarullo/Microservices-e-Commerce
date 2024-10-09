from app import db

class Product(db.Model):
    __tablename__ = 'products'
    # Atributos propios
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(80), nullable=False)
    price: float = db.Column(db.Float, nullable=False)
    is_active: bool = db.Column(db.Boolean, nullable=False)