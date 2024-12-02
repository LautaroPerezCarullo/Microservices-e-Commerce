from flask import Blueprint, request
from marshmallow import ValidationError
from sqlalchemy.exc import OperationalError
from .service import PaymentService
from .mapping import PaymentSchema, ResponseSchema, ResponseBuilder


payment_bp = Blueprint('payment', __name__)

payment_schema = PaymentSchema()
response_schema = ResponseSchema()
payment_service = PaymentService()

@payment_bp.route('/payments/add', methods=['POST'])
def save():
    response_builder = ResponseBuilder()
    try:
        payment = payment_schema.load(request.json)
        data = payment_schema.dump(payment_service.save(payment))
        response_builder.add_message("Payment added").add_status_code(201).add_data(data)
        return response_schema.dump(response_builder.build()), 201
    except OperationalError as e:
        response_builder.add_message("Can't set connection with database").add_status_code(503).add_data(e.messages)
        return response_schema.dump(response_builder.build()), 503
    except ValidationError as err:
        response_builder.add_message("Validation error").add_status_code(422).add_data(err.messages)
        return response_schema.dump(response_builder.build()), 422
    except Exception as e:
        response_builder.add_message(f"An unexpected error occurred adding payment: {str(e)}").add_status_code(500)
        return response_schema.dump(response_builder.build()), 500
    
@payment_bp.route('/payments/<int:id>', methods=['DELETE'])   
def delete(id):
    response_builder = ResponseBuilder()
    try:
        data = payment_service.delete(id)
        response_builder.add_message("Payment soft deleted").add_status_code(200).add_data(data)
        return response_schema.dump(response_builder.build()), 200
    
    except OperationalError as e:
        response_builder.add_message("Can't set connection with database").add_status_code(503).add_data(e.messages)
        return response_schema.dump(response_builder.build()), 503
    
    except Exception as e:
        response_builder.add_message(f"An unexpected error occurred compensating payment: {str(e)}").add_status_code(500)
        return response_schema.dump(response_builder.build()), 500