from ..model import Product
from marshmallow import validate, fields, Schema, post_load

class ProductSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    price = fields.Float(required=True, validate=validate.Range(min=0))
    is_active = fields.Boolean(default = True)
    
    @post_load
    def make_product(self, data, **kwargs):
        return Product(**data)
    