from .model import Stock
from .repository import StockRepository
from typing import Optional

repository = StockRepository()

class StockService:

    def save(self, stock: Stock) -> Stock:
        #Save new stock
        return repository.save(stock)
    
    def update(self, stock_id: int, updated_data) -> Stock:
        #Update existing stock
        return repository.update(stock_id, updated_data)
    
    def find(self, id: int) -> Optional[Stock]:
        #Return product by id
        return repository.find(id)
               