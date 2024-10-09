from .model import Product
from .repository import ProductRepository
from typing import List, Optional

repository = ProductRepository()

class ProductService:

    def save(self, product: Product) -> Product:
        #Save new product
        return repository.save(product)

    def all(self) -> List[Product]:
        #Return all products
        return repository.all()

    def find(self, id: int) -> Optional[Product]:
        #Return product by id
        return repository.find(id)