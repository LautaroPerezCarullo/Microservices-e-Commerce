from ..response_schema import ResponseSchema
from app import cache
from saga import SagaBuilder, SagaError
import logging
from . import MS_CatalogService, MS_PurchaseService, MS_PaymentService, MS_StockService, Response_Management
logging.basicConfig(level=logging.INFO)


response_schema = ResponseSchema()
catalog_service = MS_CatalogService()

class Orchester:
      
    def purchase(self, product_id, data):

        delivery_address = data['delivery_address']
        price = data['price']
        payment_method = data['payment_method']
        amount = data['amount']

        current_stock = cache.get(f"current_stock_product:{product_id}")
        if current_stock is not None:
            if current_stock < amount:
                logging.info(f"Current stock of product {product_id}: {current_stock}")
                logging.info("Not Enough Stock")
                return {"message": f"Insufficient Stock, Product {product_id}"}, 400
        logging.info("Current Stock isn't in cache memory")

        purchase_service = MS_PurchaseService()
        payment_service = MS_PaymentService()
        stock_service = MS_StockService()
            
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