from .model import Payment
from app import db

class PaymentRepository:
    
    def save(self, payment: Payment) -> Payment:
        # Save new payment
        db.session.add(payment)
        db.session.commit()
        return payment