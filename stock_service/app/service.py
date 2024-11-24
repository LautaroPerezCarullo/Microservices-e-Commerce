from .model import Stock
from .repository import StockRepository
from typing import Optional

repository = StockRepository()

class StockService:

    def save(self, stock: Stock) -> Stock:
        #Save new stock
        return repository.save(stock)
               