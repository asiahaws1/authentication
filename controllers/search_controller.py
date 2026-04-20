from flask import jsonify, request

from db import db
from models.app_users import AppUsers, app_users_schema
from lib.authenticate import authenticate



@authenticate
def users_get_by_search():
    search_term = request.args.get('q').lower()


    users_query = db.session.query(AppUsers).filter(db.or_(db.func.lower(AppUsers.first_name).contains(search_term), db.func.lower(AppUsers.last_name).contains(search_term), db.func.lower(AppUsers.email).contains(search_term))).order_by(AppUsers.last_name.asc()).all()


    return jsonify({"message": "users found", "results": app_users_schema.dump(users_query)}), 200

