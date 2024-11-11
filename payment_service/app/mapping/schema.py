from ..model import Payment
from marshmallow import validate, fields, Schema, post_load

class PaymentSchema(Schema):
    id = fields.Integer(dump_only=True)
    product_id = fields.Integer(required=True, validate=validate.Range(min=1, max=5))
    price = fields.Float(required=True, validate=validate.Range(min=0.01))
    payment_method = fields.String(required=True)
    deleted_at = fields.DateTime()
    
    @post_load
    def make_payment(self, data, **kwargs):
        return Payment(**data)