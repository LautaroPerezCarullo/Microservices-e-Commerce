import unittest, os
from app import create_app, db
from app.model import Purchase
from app.service import PurchaseService

purchase_service = PurchaseService()

class PurchaseTestCase(unittest.TestCase):
    
    def setUp(self):
        # Purchase
        self.PRODUCT_ID_TEST = 1
        self.PURCHASE_DATE_TEST = '2024-10-08 14:30:00'
        self.DELIVERY_ADDRESS_TEST = 'Calle 123'
        
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_purchase(self):
        purchase = self.__get_purchase()

        self.assertEqual(purchase.product_id, self.PRODUCT_ID_TEST)
        self.assertEqual(purchase.purchase_date, self.PURCHASE_DATE_TEST)
        self.assertEqual(purchase.delivery_address, self.DELIVERY_ADDRESS_TEST)

    def test_save_purchase(self):
        purchase = self.__get_purchase()
        saved_pruchase = purchase_service.save(purchase)

        self.assertEqual(saved_pruchase.id, 1)
        self.assertEqual(saved_pruchase.product_id, self.PRODUCT_ID_TEST)
        self.assertEqual(saved_pruchase.purchase_date.strftime('%Y-%m-%d %H:%M:%S'), self.PURCHASE_DATE_TEST)
        self.assertEqual(saved_pruchase.delivery_address, self.DELIVERY_ADDRESS_TEST)


    def __get_purchase(self) -> Purchase:
        purchase = Purchase()
        purchase.product_id = self.PRODUCT_ID_TEST
        purchase.purchase_date = self.PURCHASE_DATE_TEST
        purchase.delivery_address = self.DELIVERY_ADDRESS_TEST
        
        return purchase
