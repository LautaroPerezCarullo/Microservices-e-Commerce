from flask import Blueprint, request
from marshmallow import ValidationError
from .exceptions import InsufficientStockError
from .service import StockService
from .mapping import StockSchema, ResponseSchema, ResponseBuilder
from sqlalchemy.exc import OperationalError
import logging


stock_bp = Blueprint('stock', __name__)

stock_schema = StockSchema()
response_schema = ResponseSchema()
stock_service = StockService()

@stock_bp.route('/stocks/add_output', methods=['POST'])
def add_output():
    response_builder = ResponseBuilder()
    try:
        stock = stock_schema.load(request.json)
        data = stock_schema.dump(stock_service.save_output(stock))
        response_builder.add_message("Stock transaction added").add_status_code(201).add_data(data)
        return response_schema.dump(response_builder.build()), 201
        
    except InsufficientStockError as e:
        response_builder.add_message(str(e)).add_status_code(400)
        logging.info("Not Enough Stock")
        return response_schema.dump(response_builder.build()), 400
        
    except ValidationError as e:
        response_builder.add_message("Validation error").add_status_code(422).add_data(e.messages)
        logging.info("Validation Error")
        return response_schema.dump(response_builder.build()), 422
    
    except OperationalError as e:
        response_builder.add_message(str(e)).add_status_code(503)
        logging.info("Can't Connect to Database")
        return response_schema.dump(response_builder.build()), 503
    
    except Exception as e:
        response_builder.add_message(f"An unexpected error occurred adding stock transaction: {str(e)}").add_status_code(500)
        logging.info("Stock Transaction Error")
        return response_schema.dump(response_builder.build()), 500
    
@stock_bp.route('/stocks/add_input', methods=['POST'])
def add_input():
    response_builder = ResponseBuilder()
    try:
        stock = stock_schema.load(request.json)
        data = stock_schema.dump(stock_service.save_input(stock))
        response_builder.add_message("Stock transaction added").add_status_code(201).add_data(data)
        return response_schema.dump(response_builder.build()), 201
        
    except ValidationError as e:
        response_builder.add_message("Validation error").add_status_code(422).add_data(e.messages)
        logging.info("Validation Error")
        return response_schema.dump(response_builder.build()), 422
    
    except OperationalError as e:
        response_builder.add_message(str(e)).add_status_code(503)
        logging.info("Can't Connect to Database")
        return response_schema.dump(response_builder.build()), 503
    
    except Exception as e:
        response_builder.add_message(f"An unexpected error occurred adding stock transaction: {str(e)}").add_status_code(500)
        logging.info("Stock Transaction Error")
        return response_schema.dump(response_builder.build()), 500

# @stock_bp.route('/stocks/current/<int:product_id>', methods=['GET']) 
# def get_current_stock(product_id):
#     response_builder = ResponseBuilder()
#     try:
#         current_stock = stock_service.calculate_stock(product_id)
#         response_builder.add_message("Current Stock").add_status_code(200).add_data(current_stock)
#         return response_schema.dump(response_builder.build()), 200
    
#     except ValidationError as e:
#         response_builder.add_message("Validation error").add_status_code(422).add_data(e.messages)
#         logging.info("Validation Error")
#         return response_schema.dump(response_builder.build()), 422
    
#     except Exception as e:
#         response_builder.add_message(f"An unexpected error occurred adding stock transaction: {str(e)}").add_status_code(500)
#         logging.info("Stock Transaction Error")
#         return response_schema.dump(response_builder.build()), 500