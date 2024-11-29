from .model import Product
from .repository import ProductRepository
from app import cache
from typing import List, Optional

repository = ProductRepository()

class ProductService:

    def save(self, product: Product) -> Product:
        #Save new product
        saved_product = repository.save(product)
        cache.set(f'producto_{saved_product.id}', saved_product, timeout=15)
        return saved_product

    def all(self) -> List[Product]:
        #Return all products
        products = cache.get('all_products')
        if not products:
            products = repository.all()
            if products: cache.set('all_products', products, timeout=3600) 
        return products

    def find(self, id: int) -> Optional[Product]:
        print("Producto obtenido del cache")
        #Return product by id
        product = cache.get(f'producto_{id}')
        if product is None:
            product = repository.find(id)
            if product: cache.set(f'producto_{id}', product, timeout=3600)
        else:
            print("Producto obtenido del cache")
        return product

    # def save(self, product: Product) -> Product:
    #     #Save new product
    #     return repository.save(product)

    # def all(self) -> List[Product]:
    #     #Return all products
    #     return repository.all()

    # def find(self, id: int) -> Optional[Product]:
    #     #Return product by id
    #     return repository.find(id)