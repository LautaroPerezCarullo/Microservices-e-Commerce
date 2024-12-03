from flask import Blueprint, request
from marshmallow import ValidationError
from sqlalchemy.exc import OperationalError
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
    
    except OperationalError as e:
        response_builder.add_message("Can't set connection with database").add_status_code(503).add_data(e.messages)
        return response_schema.dump(response_builder.build()), 503
    
    except ValidationError as e:
        response_builder.add_message("Validation error").add_status_code(422).add_data(e.messages)
        return response_schema.dump(response_builder.build()), 422
    
    except Exception as e:
        response_builder.add_message(f"An unexpected error occurred adding purchase: {str(e)}").add_status_code(500)
        return response_schema.dump(response_builder.build()), 500
    
@purchase_bp.route('/purchases/<int:id>', methods=['DELETE'])   
def delete(id):
    response_builder = ResponseBuilder()
    try:
        data = purchase_schema.dump(purchase_service.delete(id))
        response_builder.add_message("Purchase soft deleted").add_status_code(200).add_data(data)
        return response_schema.dump(response_builder.build()), 200
    
    except OperationalError as e:
        response_builder.add_message("Can't set connection with database").add_status_code(503).add_data(e.messages)
        return response_schema.dump(response_builder.build()), 503
    
    except Exception as e:
        response_builder.add_message(f"An unexpected error occurred compensating purchase: {str(e)}").add_status_code(500)
        return response_schema.dump(response_builder.build()), 500
