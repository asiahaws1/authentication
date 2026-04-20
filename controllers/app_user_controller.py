from flask import jsonify, request
from flask_bcrypt import generate_password_hash


from db import db
from models.app_users import AppUsers, app_user_schema, app_users_schema
from models.organizations import Organizations
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate, admin_required


def add_users():
    post_data = request.form if request.form else request.json
    org_id = post_data.get('org_id')

    password = post_data.get('password')

    new_user = AppUsers.new_user_obj()

    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(password).decode('utf8')

    if org_id:
        org_query = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()

        if org_query == None:
            return jsonify({"message": "org_id is required"}), 400
        
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "user created", "result": app_user_schema.dump(new_user)}), 201
    

@admin_required
def users_get_all(auth_info):
    users_query = db.session.query(AppUsers).all()



    return jsonify({"message": "users founds", "results": app_users_schema.dump(users_query)}), 200


@authenticate_return_auth
def user_get_by_id(user_id, auth_info):
    user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    if auth_info.user.role in ('admin', 'super-admin') or user_id == str(auth_info.user.user_id):
        return jsonify({"message": "user found", "result": app_user_schema.dump(user_query)}), 200



    return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def update_user(user_id, auth_info):
    put_data = request.form if request.form else request.json

    user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404

    is_admin = auth_info.user.role in ('admin', 'super-admin')
    is_self = user_id == str(auth_info.user.user_id)

    if not is_admin and not is_self:
        return jsonify({"message": "not authorized"}), 401

    if 'role' in put_data and not is_admin:
        return jsonify({"message": "not authorized to change role"}), 401

    if 'password' in put_data and put_data.get('password'):
        from flask_bcrypt import generate_password_hash
        user_query.password = generate_password_hash(put_data['password']).decode('utf8')
        put_data = {k: v for k, v in put_data.items() if k != 'password'}

    populate_object(user_query, put_data)
    db.session.commit()

    return jsonify({"message": "user updated", "result": app_user_schema.dump(user_query)}), 200


@authenticate_return_auth
def delete_user(auth_info):
    post_data = request.form if request.form else request.json
    user_id = post_data.get('user_id') if post_data else None

    if not user_id:
        return jsonify({"message": "user_id is required"}), 400

    is_admin = auth_info.user.role in ('admin', 'super-admin')
    is_self = user_id == str(auth_info.user.user_id)

    if not is_admin and not is_self:
        return jsonify({"message": "not authorized"}), 401

    user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404

    dumped = app_user_schema.dump(user_query)

    from models.auth_tokens import AuthTokens
    db.session.query(AuthTokens).filter(AuthTokens.user_id == user_id).delete()

    db.session.delete(user_query)
    db.session.commit()

    return jsonify({"message": "user deleted", "result": dumped}), 200