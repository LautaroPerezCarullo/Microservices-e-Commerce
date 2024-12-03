from .model import Stock
from .repository import StockRepository
from app import db
from .exceptions import InsufficientStockError
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type
from sqlalchemy.exc import OperationalError
import logging

repository = StockRepository()

class StockService:

    @retry(wait=wait_fixed(3), stop=stop_after_attempt(5), retry=retry_if_exception_type(OperationalError))
    def save(self, stock: Stock) -> Stock:
        #Save new stock
        try:
            self.existing_stock = self.calculate_stock(stock)
            if stock.input_output == 2:
                if stock.amount > self.existing_stock:
                    raise InsufficientStockError(f"Insufficient Stock, Product {stock.product_id}")
                else:
                    return repository.save(stock)
            else:
                return repository.save(stock)
            
        except OperationalError as e:
            logging.error(f"Error connecting database: {str(e)}")
            db.session.rollback()
            raise 
    
    def calculate_stock(self, stock: Stock) -> int:
        return repository.calculate_stock(stock)
               