from .model import Payment
from .repository import PaymentRepository

repository = PaymentRepository()

class PaymentService:

    def save(self, payment: Payment) -> Payment:
        #Save new payment
        return repository.save(payment)
    
    def delete(self, payment_id: int) -> Payment:
        return repository.delete(payment_id)