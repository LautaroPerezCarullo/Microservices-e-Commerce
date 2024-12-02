from .model import Stock
from .repository import StockRepository
from app import cache, db
from .exceptions import InsufficientStockError
from tenacity import retry, wait_fixed, stop_after_attempt
from sqlalchemy.exc import OperationalError
import logging

repository = StockRepository()

class StockService:

    @retry(wait=wait_fixed(5), stop=stop_after_attempt(5))
    def save(self, stock: Stock) -> Stock:
        #Save new stock
        try:
            self.existing_stock = cache.get(f"existing_stock_product_{stock.product_id}")
            if self.existing_stock is None:
                self.existing_stock = self.calculate_stock(stock)
                cache.set(f"existing_stock_product_{stock.product_id}", self.existing_stock, timeout = 120)
        
            if stock.input_output == 2:
                if stock.amount > self.existing_stock:
                    raise InsufficientStockError(f"Insufficient Stock, Product {stock.product_id}")
                else:
                    self.existing_stock = self.existing_stock - stock.amount
                    cache.set(f"existing_stock_product_{stock.product_id}", self.existing_stock, timeout = 120)
                    return repository.save(stock)
            else:
                self.existing_stock = self.existing_stock + stock.amount
                cache.set(f"existing_stock_product_{stock.product_id}", self.existing_stock, timeout = 120)
                return repository.save(stock)
            
        except OperationalError as e:
            logging.error(f"Error connecting database: {str(e)}")
            db.session.rollback()
            raise 
    
    @retry(wait=wait_fixed(5), stop=stop_after_attempt(5))
    def calculate_stock(self, stock: Stock) -> int:
        try:
            return repository.calculate_stock(stock)
        
        except OperationalError as e:
            logging.error(f"Error connecting database: {str(e)}")
            db.session.rollback()
            raise 
               