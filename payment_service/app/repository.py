from .model import Payment
from app import db

class PaymentRepository:
    
    def save(self, payment: Payment) -> Payment:
        # Save new payment
        db.session.add(payment)
        db.session.commit()
        return payment
    
    def delete(self, payment_id: int) -> Payment:
        payment = Payment.query.get(payment_id)
        payment.deleted_at = db.func.now()
        db.session.commit()
        return payment