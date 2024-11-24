from .model import Stock
from app import db

class StockRepository:
    
    def save(self, stock: Stock) -> Stock:
        stock.transaction_date = db.func.now()
        # Save new stock
        db.session.add(stock)
        db.session.commit()
        return stock