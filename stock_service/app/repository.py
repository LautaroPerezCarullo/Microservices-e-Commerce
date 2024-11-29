from sqlalchemy import func
from .model import Stock
from app import db

class StockRepository:
    
    def save(self, stock: Stock) -> Stock:
        stock.transaction_date = db.func.now()
        # Save new stock
        db.session.add(stock)
        db.session.commit()
        return stock

    def calculate_stock(self, stock: Stock) -> int:
        input_amount = db.session.query(func.sum(Stock.amount))\
            .filter((Stock.input_output == 1), (Stock.product_id == stock.product_id))\
            .scalar() or 0

        output_amount = db.session.query(func.sum(Stock.amount))\
            .filter((Stock.input_output == 2), (Stock.product_id == stock.product_id))\
            .scalar() or 0

        stock_amount = input_amount - output_amount

        return stock_amount