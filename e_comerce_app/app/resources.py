from flask import Blueprint, request
from .ochestrator import Orchester

e_commerce_bp = Blueprint('e_commerce', __name__)
orchester = Orchester()

@e_commerce_bp.route('e_commerce/get_catalog', methods = ['GET'])
def get_catalog():
    orchester = Orchester()
    return orchester.get_catalog()

@e_commerce_bp.route('e_commerce/get_product/<int:id>', methods = ['GET'] )
def get_product(id):
    orchester = Orchester()
    return orchester.get_product(id)

@e_commerce_bp.route('e_commerce/purchase/<int:product_id>', methods = ['POST'])
def purchase(product_id):
    orchester = Orchester()
    data = request.get_json()
    return orchester.purchase(product_id, data)