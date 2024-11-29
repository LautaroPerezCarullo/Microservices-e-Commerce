from flask import Blueprint, request
from marshmallow import ValidationError
from .service import StockService
from .mapping import StockSchema, ResponseSchema, ResponseBuilder
import logging


stock_bp = Blueprint('stock', __name__)

stock_schema = StockSchema()
response_schema = ResponseSchema()
stock_service = StockService()

@stock_bp.route('/stocks/add', methods=['POST'])
def add():
    response_builder = ResponseBuilder()
    try:
        stock = stock_schema.load(request.json)
        if stock.input_output == 2 and stock.amount > stock_service.calculate_stock(stock):
            response_builder.add_message("Insufficient stock for the requested product").add_status_code(400)
            return response_schema.dump(response_builder.build()), 400
        else: 
            data = stock_schema.dump(stock_service.save(stock))
            response_builder.add_message("Stock added").add_status_code(201).add_data(data)
            return response_schema.dump(response_builder.build()), 201
    
    except ValidationError as e:
        response_builder.add_message("Validation error").add_status_code(422).add_data(e.messages)
        logging.info("Validation Error")
        return response_schema.dump(response_builder.build()), 422
    
    except Exception as e:
        response_builder.add_message(f"An unexpected error occurred adding stock transaction: {str(e)}").add_status_code(500)
        logging.info("Stock Transaction Error")
        return response_schema.dump(response_builder.build()), 500