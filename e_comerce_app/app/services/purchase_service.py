import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

basedir = os.path.abspath(Path(__file__).parents[3])
load_dotenv(os.path.join(basedir, '.env'))

class MS_PurchaseService:
    
    def __init__(self):
        self.purchase_url = os.getenv("PURCHASE_SERVICE_URL")

    def purchase_processing(self, product_id, delivery_address):
        self.response = requests.post(f"{self.purchase_url}/purchases/add", json={"product_id": product_id, "delivery_address": delivery_address})
        if self.response.status_code == 201:
            self.id = self.response.json().get("data", {}).get("id")
            logging.info(f"Purchase <- {self.response.json()}")
            logging.info(f"Succesful purchase ID: {self.id}")
        else:
            logging.info("Purchase Processing Error")
            raise Exception("Error processing purchase")
        
    def cancel_purchase(self, purchase_id):
        response = requests.delete(f"{self.purchase_url}/purchases/{purchase_id}")
        if response.status_code == 200:
            logging.info(f"Succesful purchase compensation. Purchase ID: {self.id}")
        else:
            logging.info("Purchase Compensation Error")
            raise Exception("Error compensating purchase")
        