import unittest, os
from app import create_app, db
from app.model import Product

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

    def __get_product(self) -> Product:
        product = Product()
        product.name = self.NAME_TEST
        product.price = self.PRICE_TEST
        product.is_active = self.IS_ACTIVE_TEST
        
        return product
