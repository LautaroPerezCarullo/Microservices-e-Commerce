import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from .response_message import ResponseBuilder
from .response_schema import ResponseSchema


basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, '.env'))
response_schema = ResponseSchema()

class Orchester:
    def __init__(self):
        self.catalog_url = os.getenv("CATALOG_SERVICE_URL")
        self.payment_url = os.getenv("PAYMENT_SERVICE_URL")
        self.purchase_url = os.getenv("PURCHASE_SERVICE_URL")
        self.stock_url = os.getenv("STOCK_SERVICE_URL")

    def get_catalog(self):
        print(f"{self.catalog_url}/products")
        response = requests.get(f"{self.catalog_url}/products")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error getting catalog")
    
    def get_product(self, product_id):
        response = requests.get(f"{self.catalog_url}/products/{product_id}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error getting product")

    def purchase_processing(self, product_id, purchase_date, delivery_address):
        response = requests.post(f"{self.purchase_url}/purchases/add", json={"product_id": product_id, "purchase_date": purchase_date, "delivery_address": delivery_address})
        if response.status_code == 201:
            return response.json()
        elif response.status_code == 422:
            return response.json()
        else:
            raise Exception("Error processing purchase")


    def payment_processing(self, product_id, price, payment_method):
        response = requests.post(f"{self.payment_url}/payments/add", json={"product_id": product_id, "price": price, "payment_method": payment_method})
        if response.status_code == 201:
            return response.json()
        elif response.status_code == 422:
            return response.json()
        else:
            raise Exception("Error processing payment")

    def update_stock(self, stock_id, transaction_date, amount, input_output):

        response_builder = ResponseBuilder()

        response = requests.put(f"{self.stock_url}/stocks/update/{stock_id}", json={"transaction_date": transaction_date, "amount": amount, "input_output": input_output})
        if response.status_code == 200:
            return response.json()
        else:
            response_builder.add_message("Error updating stock").add_status_code(500)
            return response_schema.dump(response_builder.build()), 500
        

    def purchase(self, product_id, data):
        
        response_builder = ResponseBuilder()

        purchase_date = data['purchase_date']
        delivery_address = data['delivery_address']
        price = data['price']
        payment_method = data['payment_method']
        transaction_date = data['transaction_date']
        amount = data['amount']
        input_output = data['input_output']
        
        try:

            purchase_response = self.purchase_processing(product_id, purchase_date, delivery_address)

            payment_response = self.payment_processing(product_id, price, payment_method)

            stock_response = self.update_stock(product_id,transaction_date, amount, input_output)

            if purchase_response['status_code'] == 201 and payment_response['status_code'] == 201 and stock_response['status_code'] == 100:
                response_builder.add_message("Succesful Transaction").add_status_code(201).add_data(data)
                return response_schema.dump(response_builder.build()), 201
            
            else:
                response_builder.add_message("Fuck").add_status_code(501)
                return response_schema.dump(response_builder.build()), 501
        except Exception as e:
            response_builder.add_message(f"Transaction Error: {str(e)}").add_status_code(500)
            return response_schema.dump(response_builder.build()), 500