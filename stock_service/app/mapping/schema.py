from ..model import Stock
from marshmallow import validate, fields, Schema, post_load

class StockSchema(Schema):
    id = fields.Integer(dump_only=True)
    product_id = fields.Integer(required=True, validate=validate.Range(min=1, max=5))
    transaction_date = fields.DateTime()
    amount = fields.Integer(required=True, validate=validate.Range(min=1))
    input_output = fields.Integer(required=True, validate=validate.Range(min=0, max=2))  
      
    @post_load
    def make_stock(self, data, **kwargs):
        return Stock(**data)