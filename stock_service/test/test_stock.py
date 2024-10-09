import unittest, os
from app import create_app, db
from app.model import Stock

class StockTestCase(unittest.TestCase):
    
    def setUp(self):
        # Stock
        self.PRODUCT_ID_TEST = 1
        self.TRANSACTION_DATE_TEST = '2024-10-08 14:30:00'
        self.AMOUNT_TEST = 5
        self.INPUT_OUTPUT_TEST = 1
        
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_stock(self):
        stock = self.__get_stock()

        self.assertEqual(stock.product_id, self.PRODUCT_ID_TEST)
        self.assertEqual(stock.transaction_date, self.TRANSACTION_DATE_TEST)
        self.assertEqual(stock.amount, self.AMOUNT_TEST)
        self.assertEqual(stock.input_ouput, self.INPUT_OUTPUT_TEST)

    def __get_stock(self) -> Stock:
        stock = Stock()
        stock.product_id = self.PRODUCT_ID_TEST
        stock.transaction_date = self.TRANSACTION_DATE_TEST
        stock.amount = self.AMOUNT_TEST
        stock.input_ouput = self.INPUT_OUTPUT_TEST
        
        return stock
