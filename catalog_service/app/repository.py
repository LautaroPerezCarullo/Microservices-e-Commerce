from .model import Product
from app import db
from typing import Optional, List

class ProductRepository:
    
    def save(self, product: Product) -> Product:
        # Save new product
        db.session.add(product)
        db.session.commit()
        return product
    
    def find(self, product_id: int) -> Optional[Product]:
        #Find a product by id
        return db.session.query(Product).filter(Product.id == product_id, Product.is_active == True).one_or_none()

    def all(self) -> List[Product]:
        #Show all products
        return db.session.query(Product).filter(Product.is_active == True).all()