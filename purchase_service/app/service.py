from .model import Purchase
from .repository import PurchaseRepository

repository = PurchaseRepository()

class PurchaseService:

    def save(self, purchase: Purchase) -> Purchase:
        #Save new purchase
        return repository.save(purchase)