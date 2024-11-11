from flask import Blueprint, request
from .service import StockService
from .mapping import StockSchema, ResponseSchema, ResponseBuilder


stock_bp = Blueprint('stock', __name__)

stock_schema = StockSchema()
response_schema = ResponseSchema()
stock_service = StockService()

@stock_bp.route('/stocks/update/<int:id>', methods=['PUT'])
def update(id:int):
    new_data = stock_schema.load(request.json)
    new_stock = stock_service.update(id, new_data)
    response_builder = ResponseBuilder()
    response_builder.add_message("Updated Stock").add_status_code(200).add_data(stock_schema.dump(new_stock))
    return response_schema.dump(response_builder.build()), 200