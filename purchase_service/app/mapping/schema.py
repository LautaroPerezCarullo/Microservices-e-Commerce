from ..model import Purchase
from marshmallow import validate, fields, Schema, post_load

class PurchaseSchema(Schema):
    id = fields.Integer(dump_only=True)
    product_id = fields.Integer(required=True, validate=validate.Range(min=1, max=5))
    purchase_date = fields.DateTime(required=True)
    delivery_address = fields.String(required=True)
    
    @post_load
    def make_purchase(self, data, **kwargs):
        return Purchase(**data)