from flask import Blueprint

import controllers


company = Blueprint('company', __name__)


@company.route('/company', methods=['POST'])
def add_company_route():
    return controllers.add_company()


@company.route('/companies', methods=['GET'])
def get_all_companies_route():
    return controllers.get_all_companies()


@company.route('/company/<company_id>', methods=['GET', 'PUT'])
def company_by_id_route(company_id):
    from flask import request
    if request.method == 'PUT':
        return controllers.update_company(company_id)
    return controllers.get_company_by_id(company_id)


@company.route('/company/delete', methods=['DELETE'])
def delete_company_route():
    return controllers.delete_company()
