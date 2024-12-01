import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from .response_message import ResponseBuilder
from .response_schema import ResponseSchema
from saga import SagaBuilder, SagaError
import logging
from app.services import MS_CatalogService, MS_PurchaseService, MS_PaymentService, MS_StockService, Response_Management


basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, '.env'))
response_schema = ResponseSchema()

catalog_service = MS_CatalogService()
purchase_service = MS_PurchaseService()
payment_service = MS_PaymentService()
stock_service = MS_StockService()

class Orchester:
      
    def purchase(self, product_id, data):

        delivery_address = data['delivery_address']
        price = data['price']
        payment_method = data['payment_method']
        amount = data['amount']
        
        try:
            SagaBuilder.create()\
                .action(lambda: purchase_service.purchase_processing(product_id, delivery_address), lambda: purchase_service.cancel_purchase(purchase_service.id)) \
                .action(lambda: payment_service.payment_processing(product_id, price, payment_method), lambda: payment_service.cancel_payment(payment_service.id)) \
                .action(lambda: stock_service.stock_transaction(product_id, amount, 2), lambda: stock_service.stock_compensation(product_id, amount, 1)) \
                .build().execute()
            
            return {"message": "Purchase completed successfully"}, 200    

        except SagaError as e:
            logging.error(e)
            return Response_Management(e).to_response()
        
    def get_catalog(self):
        return catalog_service.get_catalog()
    
    def get_product(self, product_id):
        return catalog_service.get_product(product_id)