import unittest, os
from app import create_app, db
from app.model import Stock
from app.service import StockService

stock_service = StockService()

class StockTestCase(unittest.TestCase):
    
    def setUp(self):
        #Stock
        self.PRODUCT_ID_TEST = 1
        self.TRANSACTION_DATE_TEST = '2024-10-08 14:30:00'
        self.AMOUNT_TEST = 5
        self.INPUT_OUTPUT_TEST = 1

        #Stock2 
        self.TRANSACTION_DATE_TEST_2 = '2024-10-09 10:00:00'
        self.AMOUNT_TEST_2 = 4
        self.INPUT_OUTPUT_TEST_2 = 2

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
        self.assertEqual(stock.input_output, self.INPUT_OUTPUT_TEST)

    def test_save_stock(self):
        stock = self.__get_stock()
        saved_stock = stock_service.save(stock)

        self.assertEqual(saved_stock.id, 1)
        self.assertEqual(saved_stock.product_id, self.PRODUCT_ID_TEST)
        self.assertEqual(saved_stock.transaction_date.strftime('%Y-%m-%d %H:%M:%S'), self.TRANSACTION_DATE_TEST)
        self.assertEqual(saved_stock.amount, self.AMOUNT_TEST)
        self.assertEqual(saved_stock.input_output, self.INPUT_OUTPUT_TEST)

    def test_find_stock(self):
        stock = self.__get_stock()
        stock_service.save(stock)

        stock_find = stock_service.find(1)
        self.assertIsNotNone(stock_find)
        self.assertEqual(stock_find.id, stock.id)
        self.assertEqual(stock_find.product_id, stock.product_id)
        self.assertEqual(stock_find.transaction_date, stock.transaction_date)
        self.assertEqual(stock_find.amount, stock.amount)
        self.assertEqual(stock_find.input_output, stock.input_output)

    def test_update_stock(self):
        stock = self.__get_stock()
        saved_stock = stock_service.save(stock)

        updated_data = {
            'transaction_date': self.TRANSACTION_DATE_TEST_2,
            'amount': self.AMOUNT_TEST_2,
            'input_output': self.INPUT_OUTPUT_TEST_2
        }

        updated_stock = stock_service.update(saved_stock.id, updated_data)
        self.assertEqual(updated_stock.id,saved_stock.id)
        self.assertEqual(updated_stock.product_id,saved_stock.product_id)
        self.assertEqual(updated_stock.transaction_date.strftime('%Y-%m-%d %H:%M:%S'), self.TRANSACTION_DATE_TEST_2)
        self.assertEqual(updated_stock.amount, self.AMOUNT_TEST_2)
        self.assertEqual(updated_stock.input_output, self.INPUT_OUTPUT_TEST_2)

    def __get_stock(self) -> Stock:
        stock = Stock()
        stock.product_id = self.PRODUCT_ID_TEST
        stock.transaction_date = self.TRANSACTION_DATE_TEST
        stock.amount = self.AMOUNT_TEST
        stock.input_output = self.INPUT_OUTPUT_TEST
        
        return stock
