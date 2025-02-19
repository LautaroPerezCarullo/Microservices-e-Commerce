from .model import Payment
from app import db
import logging

class PaymentRepository:
    
    def save(self, payment: Payment) -> Payment:
        # Save new payment
        db.session.add(payment)
        db.session.commit()
        logging.info(f"Successful Payment")
        return payment
    
    def delete(self, payment_id: int) -> Payment:
        payment = Payment.query.get(payment_id)
        payment.deleted_at = db.func.now()
        db.session.commit()
        logging.info(f"Successful Payment Compensation")
        return payment