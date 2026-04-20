from flask import Blueprint, request

import controllers


product = Blueprint('product', __name__)


@product.route('/product', methods=['POST'])
def add_product_route():
    return controllers.add_product()


@product.route('/products', methods=['GET'])
def get_all_products_route():
    return controllers.get_all_products()


@product.route('/products/active', methods=['GET'])
def get_active_products_route():
    return controllers.get_active_products()


@product.route('/product/<product_id>', methods=['GET', 'PUT'])
def product_by_id_route(product_id):
    if request.method == 'PUT':
        return controllers.update_product(product_id)
    return controllers.get_product_by_id(product_id)


@product.route('/product/company/<company_id>', methods=['GET'])
def get_products_by_company_route(company_id):
    return controllers.get_products_by_company(company_id)


@product.route('/product/category', methods=['POST'])
def add_product_category_route():
    return controllers.add_product_category()


@product.route('/product/delete', methods=['DELETE'])
def delete_product_route():
    return controllers.delete_product()
