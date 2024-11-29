from .model import Stock
from .repository import StockRepository

repository = StockRepository()

class StockService:

    def save(self, stock: Stock) -> Stock:
        #Save new stock
        return repository.save(stock)
    
    def calculate_stock(self, stock: Stock) -> int:
        return repository.calculate_stock(stock)
               