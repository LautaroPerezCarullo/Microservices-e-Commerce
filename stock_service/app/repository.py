from .model import Stock
from app import db
from typing import Optional

class StockRepository:
    
    def save(self, stock: Stock) -> Stock:
        # Save new stock
        db.session.add(stock)
        db.session.commit()
        return stock
    
    def update(self, stock_id: int, updated_data) -> Stock:
        # Get stock
        stock = self.find(stock_id)
        # Stock exists?
        if not stock:
            raise ValueError(f"Stock with ID {stock_id} not found.")
        
        #Update stock
        stock.transaction_date = updated_data.get('transaction_date', stock.transaction_date)
        stock.amount = updated_data.get('amount', stock.amount)
        stock.input_output = updated_data.get('input_output', stock.input_output)
        db.session.commit()
        return stock

    def find(self, stock_id: int) -> Optional[Stock]:
        #Find a stock by id
        return db.session.query(Stock).filter(Stock.id == stock_id,).one_or_none()