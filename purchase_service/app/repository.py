from .model import Purchase
from app import db
import logging

class PurchaseRepository:
    
    def save(self, purchase: Purchase) -> Purchase:
        purchase.purchase_date = db.func.now()
        # Save new purchase
        db.session.add(purchase)
        db.session.commit()
        logging.info(f"Successful Purchase")
        return purchase
    
    def delete(self, purchase_id: int) -> Purchase:
        purchase = Purchase.query.get(purchase_id)
        purchase.deleted_at = db.func.now()
        db.session.commit()
        logging.info(f"Successful Purchase Compensation")
        return purchase
    