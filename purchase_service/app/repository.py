from .model import Purchase
from app import db

class PurchaseRepository:
    
    def save(self, purchase: Purchase) -> Purchase:
        # Save new purchase
        db.session.add(purchase)
        db.session.commit()
        return purchase
    