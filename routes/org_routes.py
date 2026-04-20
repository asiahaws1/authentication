from flask import Blueprint


import controllers



org = Blueprint('org', __name__)



@org.route('/organization', methods=['POST'])
def add_org_route():
    return controllers.add_org()

@org.route('/organizations', methods=['GET'])
def get_all_orgs_route():
    return controllers.get_all_orgs()