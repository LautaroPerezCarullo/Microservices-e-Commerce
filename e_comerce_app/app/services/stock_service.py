import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from .exceptions import ServiceException
from ..response_schema import ResponseSchema
import logging
logging.basicConfig(level=logging.INFO)

basedir = os.path.abspath(Path(__file__).parents[3])
load_dotenv(os.path.join(basedir, '.env'))

response_schema = ResponseSchema()

class MS_StockService:
    
    def __init__(self):
        self.stock_url = os.getenv("STOCK_SERVICE_URL")
        self.id = None

    def stock_transaction(self, product_id, amount, input_output):
        response = requests.post(f"{self.stock_url}/stocks/add", json={"product_id": product_id, "amount": amount, "input_output": input_output})
        if response.status_code == 201:
            self.id = response.json().get("data", {}).get("id")
            logging.info(f"Succesful stock transaction ID: {self.id}")
        else:
            self.id = None
            logging.info(response.json().get('message'))
            raise ServiceException(response.json().get('message'), response.status_code)
        
    def stock_compensation(self, product_id, amount, input_output):
        if self.id:
            response = requests.post(f"{self.stock_url}/stocks/add", json={"product_id": product_id, "amount": amount, "input_output": input_output})
            if response.status_code == 201:
                self.compensation_id = response.json().get("data", {}).get("id")
                logging.info(f"Succesful stock compensation ID: {self.compensation_id}")
            else:
                logging.info(response.json().get('message'))
                raise ServiceException(response.json().get('message'), response.status_code)
    