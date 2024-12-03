from .model import Purchase
from .repository import PurchaseRepository
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type
from sqlalchemy.exc import OperationalError
import logging
from app import db

repository = PurchaseRepository()

class PurchaseService:

    @retry(wait=wait_fixed(3), stop=stop_after_attempt(5), retry=retry_if_exception_type(OperationalError))
    def save(self, purchase: Purchase) -> Purchase:
        #Save new purchase
        try:
            return repository.save(purchase)
        except OperationalError as e:
            db.session.rollback()
            raise
    
    @retry(wait=wait_fixed(3), stop=stop_after_attempt(5), retry=retry_if_exception_type(OperationalError))
    def delete(self, purchase_id: int) -> Purchase:
        try:
            return repository.delete(purchase_id)
        except OperationalError as e:
            db.session.rollback()
            raise 