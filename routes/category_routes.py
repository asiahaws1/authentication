from flask import Blueprint, request

import controllers


category = Blueprint('category', __name__)


@category.route('/category', methods=['POST'])
def add_category_route():
    return controllers.add_category()


@category.route('/categories', methods=['GET'])
def get_all_categories_route():
    return controllers.get_all_categories()


@category.route('/category/<category_id>', methods=['GET', 'PUT'])
def category_by_id_route(category_id):
    if request.method == 'PUT':
        return controllers.update_category(category_id)
    return controllers.get_category_by_id(category_id)


@category.route('/category/delete', methods=['DELETE'])
def delete_category_route():
    return controllers.delete_category()
