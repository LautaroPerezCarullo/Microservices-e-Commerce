import unittest, os
from app import create_app, db
from app.model import Payment

class PaymentTestCase(unittest.TestCase):
    
    def setUp(self):
        # Payment
        self.PRODUCT_ID_TEST = 1
        self.PRICE_TEST = 99.99
        self.PAYMENT_METHOD_TEST = 'cash'
        
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_payment(self):
        payment = self.__get_payment()

        self.assertEqual(payment.product_id, self.PRODUCT_ID_TEST)
        self.assertEqual(payment.price, self.PRICE_TEST)
        self.assertEqual(payment.payment_method, self.PAYMENT_METHOD_TEST)

    def __get_payment(self) -> Payment:
        payment = Payment()
        payment.product_id = self.PRODUCT_ID_TEST
        payment.price = self.PRICE_TEST
        payment.payment_method = self.PAYMENT_METHOD_TEST
        
        return payment
