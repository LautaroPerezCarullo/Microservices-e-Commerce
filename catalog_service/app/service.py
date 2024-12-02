from .model import Product
from .repository import ProductRepository
from app import cache
from tenacity import retry, wait_fixed, stop_after_attempt
from typing import List, Optional
from sqlalchemy.exc import OperationalError
import logging


repository = ProductRepository()

class ProductService:

    
    def save(self, product: Product) -> Product:
        #Save new product
        saved_product = repository.save(product)
        cache.set(f'product_{saved_product.id}', saved_product, timeout=120)
        return saved_product

    @retry(wait=wait_fixed(5), stop=stop_after_attempt(5))
    def all(self) -> List[Product]:
        #Return all products
        try:
            products = cache.get('all_products')
            if not products:
                products = repository.all()
                if products: cache.set('all_products', products, timeout=120) 
            return products
        except OperationalError as e:
            logging.error(f"Error connecting database: {str(e)}")
            raise 

    @retry(wait=wait_fixed(5), stop=stop_after_attempt(5))
    def find(self, id: int) -> Optional[Product]:
        #Return product by id
        try:
            product = cache.get(f'product_{id}')
            if product is None:
                product = repository.find(id)
                if product: cache.set(f'product_{id}', product, timeout=120)
            return product
        except OperationalError as e:
            logging.error(f"Error connecting database: {str(e)}")
            raise 

    # def save(self, product: Product) -> Product:
    #     #Save new product
    #     return repository.save(product)

    # def all(self) -> List[Product]:
    #     #Return all products
    #     return repository.all()

    # def find(self, id: int) -> Optional[Product]:
    #     #Return product by id
    #     return repository.find(id)