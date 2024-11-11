import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from ..response_message import ResponseBuilder
from ..response_schema import ResponseSchema
import logging

basedir = os.path.abspath(Path(__file__).parents[3])
load_dotenv(os.path.join(basedir, '.env'))

response_schema = ResponseSchema()

class MS_StockService:
    
    def __init__(self):
        self.stock_url = os.getenv("STOCK_SERVICE_URL")

    def update_stock(self, stock_id, transaction_date, amount, input_output):

        response_builder = ResponseBuilder()

        response = requests.put(f"{self.stock_url}/stocks/update/{stock_id}", json={"transaction_date": transaction_date, "amount": amount, "input_output": input_output})
        if response.status_code == 200:
            logging.info(f"Stock Updated")
        else:
            logging.info("Stock Updating Failed")
            raise Exception("Error Updating Stock")