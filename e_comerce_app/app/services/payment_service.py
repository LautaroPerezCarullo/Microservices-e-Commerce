import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from .exceptions import ServiceException
import logging

basedir = os.path.abspath(Path(__file__).parents[3])
load_dotenv(os.path.join(basedir, '.env'))

class MS_PaymentService:
    
    def __init__(self):
        self.payment_url = os.getenv("PAYMENT_SERVICE_URL")

    def payment_processing(self, product_id, price, payment_method):
        response = requests.post(f"{self.payment_url}/payments/add", json={"product_id": product_id, "price": price, "payment_method": payment_method})

        if response.status_code == 201:
            self.id = response.json().get("data", {}).get("id")
            logging.info(f"Succesful payment ID: {self.id}")
        else:
            logging.info(response.json().get('message'))
            raise ServiceException(response.json().get('message'), response.status_code)
        
    def cancel_payment(self, payment_id):
        response = requests.delete(f"{self.payment_url}/payments/{payment_id}")
        if response.status_code == 200:
            logging.info(f"Succesful payment compensation. Payment ID: {self.id}")
        else:
            logging.info("Payment Compensation Error")
            raise Exception("Error compensating payment")