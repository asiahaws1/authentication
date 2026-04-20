from flask import Blueprint, request

import controllers


warranty = Blueprint('warranty', __name__)


@warranty.route('/warranty', methods=['POST'])
def add_warranty_route():
    return controllers.add_warranty()


@warranty.route('/warranty/<warranty_id>', methods=['GET', 'PUT'])
def warranty_by_id_route(warranty_id):
    if request.method == 'PUT':
        return controllers.update_warranty(warranty_id)
    return controllers.get_warranty_by_id(warranty_id)


@warranty.route('/warranty/delete', methods=['DELETE'])
def delete_warranty_route():
    return controllers.delete_warranty()
