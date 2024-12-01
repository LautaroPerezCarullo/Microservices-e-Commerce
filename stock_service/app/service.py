from .model import Stock
from .repository import StockRepository
from .exceptions import InsufficientStockError

repository = StockRepository()

class StockService:

    def save(self, stock: Stock) -> Stock:
        #Save new stock
        if stock.input_output == 2 and stock.amount > self.calculate_stock(stock):
            raise InsufficientStockError(f"Insufficient Stock, Product {stock.product_id}")
        else:
            return repository.save(stock)
    
    def calculate_stock(self, stock: Stock) -> int:
        return repository.calculate_stock(stock)
               