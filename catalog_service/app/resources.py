from flask import Blueprint
from .service import ProductService
from .mapping import ProductSchema, ResponseSchema, ResponseBuilder


product_bp = Blueprint('product', __name__)

product_schema = ProductSchema()
response_schema = ResponseSchema()
product_service = ProductService()

@product_bp.route('/products', methods=['GET'])
def view_catalog():
    response_builder = ResponseBuilder()
    try:
        data = product_schema.dump(product_service.all(), many=True)
        response_builder.add_message("Finded Products").add_status_code(200).add_data(data)
        return response_schema.dump(response_builder.build()), 200
    
    except Exception as e:
        response_builder.add_message(f"Something happended getting catalog: {str(e)}").add_status_code(500)
        return response_schema.dump(response_builder.build()), 500

@product_bp.route('/products/<int:id>', methods=['GET'])
def find_product(id):
    response_builder = ResponseBuilder()
    data = None
    try:
        product = product_service.find(id)
        if product:
            data = product_schema.dump(product)
        if data:
            response_builder.add_message("Finded Product").add_status_code(200).add_data(data)
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Any Product Finded").add_status_code(404)
            return response_schema.dump(response_builder.build()), 404
    
    except Exception as e:
        response_builder.add_message(f"Something happended getting product({id}): {str(e)}").add_status_code(500)
        return response_schema.dump(response_builder.build()), 500