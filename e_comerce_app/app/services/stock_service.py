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

    def stock_transaction(self, product_id, amount, input_output):
        self.response = requests.post(f"{self.stock_url}/stocks/add", json={"product_id": product_id, "amount": amount, "input_output": input_output})
        if self.response.status_code == 201:
            self.id = self.response.json().get("data", {}).get("id")
            logging.info(f"Stock Transaction <- {self.response.json()}")
            logging.info(f"Succesful stock transaction ID: {self.id}")
        else:
            logging.info("Stock Transaction Error")
            raise Exception("Error Transfering Stock")
        
    def stock_compensation(self, product_id, amount, input_output):
        self.response = requests.post(f"{self.stock_url}/stocks/add", json={"product_id": product_id, "amount": amount, "input_output": input_output})
        if self.response.status_code == 201:
            self.id = self.response.json().get("data", {}).get("id")
            logging.info(f"Stock Compensation <- {self.response.json()}")
            logging.info(f"Succesful stock compensation ID: {self.id}")
        else:
            logging.info("Stock Compensation Error")
            raise Exception("Error Compensating Stock")
    