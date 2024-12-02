from .model import Purchase
from .repository import PurchaseRepository
from tenacity import retry, wait_fixed, stop_after_attempt
from sqlalchemy.exc import OperationalError
import logging

repository = PurchaseRepository()

class PurchaseService:

    @retry(wait=wait_fixed(5), stop=stop_after_attempt(5))
    def save(self, purchase: Purchase) -> Purchase:
        #Save new purchase
        try:
            return repository.save(purchase)
        except OperationalError as e:
            logging.error(f"Error connecting database: {str(e)}")
            raise 
    
    @retry(wait=wait_fixed(5), stop=stop_after_attempt(5))
    def delete(self, purchase_id: int) -> Purchase:
        try:
            return repository.delete(purchase_id)
        except OperationalError as e:
            logging.error(f"Error connecting database: {str(e)}")
            raise 