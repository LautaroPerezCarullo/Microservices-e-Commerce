from flask import Blueprint, request
from marshmallow import ValidationError
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
    except ValidationError as err:
        response_builder.add_message("Validation error").add_status_code(422).add_data(err.messages)
        return response_schema.dump(response_builder.build()), 422