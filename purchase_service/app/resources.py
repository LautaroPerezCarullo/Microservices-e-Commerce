from flask import Blueprint, request
from marshmallow import ValidationError
from .service import PurchaseService
from .mapping import PurchaseSchema, ResponseSchema, ResponseBuilder


purchase_bp = Blueprint('purchase', __name__)

purchase_schema = PurchaseSchema()
response_schema = ResponseSchema()
purchase_service = PurchaseService()

@purchase_bp.route('/purchases/add', methods=['POST'])
def add():
    response_builder = ResponseBuilder()
    try:
        purchase = purchase_schema.load(request.json)
        data = purchase_schema.dump(purchase_service.save(purchase))
        response_builder.add_message("Purchase added").add_status_code(201).add_data(data)
        return response_schema.dump(response_builder.build()), 201
    except ValidationError as err:
        response_builder.add_message("Validation error").add_status_code(422).add_data(err.messages)
        return response_schema.dump(response_builder.build()), 422
