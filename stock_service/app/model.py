from app import db

class Stock(db.Model):
    __tablename__ = 'stocks'
    # Atributos propios
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id: int = db.Column(db.Integer, nullable=False)    
    transaction_date: str = db.Column(db.DateTime, nullable=False)
    amount: int = db.Column(db.Integer, nullable=False)
    input_ouput: int = db.Column(db.Integer, nullable=False)