from .model import Payment
from .repository import PaymentRepository
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type
from sqlalchemy.exc import OperationalError
import logging
from app import db

repository = PaymentRepository()

class PaymentService:

    @retry(wait=wait_fixed(3), stop=stop_after_attempt(5), retry=retry_if_exception_type(OperationalError))
    def save(self, payment: Payment) -> Payment:
        #Save new payment
        try:
            return repository.save(payment)
        except OperationalError as e:
            logging.error(f"Error connecting database: {str(e)}")
            db.session.rollback()
            raise 

    @retry(wait=wait_fixed(3), stop=stop_after_attempt(5), retry=retry_if_exception_type(OperationalError))
    def delete(self, payment_id: int) -> Payment:
        try:
            return repository.delete(payment_id)
        except OperationalError as e:
            logging.error(f"Error connecting database: {str(e)}")
            db.session.rollback()
            raise 