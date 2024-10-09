from .model import Payment
from .repository import PaymentRepository

repository = PaymentRepository()

class PaymentService:

    def save(self, payment: Payment) -> Payment:
        #Save new payment
        return repository.save(payment)