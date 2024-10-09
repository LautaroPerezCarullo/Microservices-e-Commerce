import unittest, os
from app import create_app, db
from app.model import Product
from app.service import ProductService

product_service = ProductService()

class ProductTestCase(unittest.TestCase):
    
    def setUp(self):
        # Product
        self.NAME_TEST = 'Test Product'
        self.PRICE_TEST = 99.99
        self.IS_ACTIVE_TEST = True
        
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_product(self):
        product = self.__get_product()

        self.assertEqual(product.name, self.NAME_TEST)
        self.assertEqual(product.price, self.PRICE_TEST)
        self.assertEqual(product.is_active, self.IS_ACTIVE_TEST)

    def test_all_product(self):
        product = self.__get_product()
        product_service.save(product)

        products = product_service.all()
        self.assertEqual(products[0].name, product.name)

    def test_find_product(self):
        product = self.__get_product()
        product_service.save(product)

        product_find = product_service.find(1)
        self.assertIsNotNone(product_find)
        self.assertEqual(product_find.id, product.id)
        self.assertEqual(product_find.name, product.name)

    def __get_product(self) -> Product:
        product = Product()
        product.name = self.NAME_TEST
        product.price = self.PRICE_TEST
        product.is_active = self.IS_ACTIVE_TEST
        
        return product
