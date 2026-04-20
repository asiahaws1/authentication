from flask import jsonify, request

from db import db
from models.categories import Categories, category_schema, categories_schema
from models.products_categories_xref import ProductsCategoriesXref
from util.reflection import populate_object
from lib.authenticate import authenticate, admin_required


@admin_required
def add_category(auth_info):
    post_data = request.form if request.form else request.json

    new_category = Categories.new_category_obj()
    populate_object(new_category, post_data)

    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "category created", "result": category_schema.dump(new_category)}), 201


@authenticate
def get_all_categories():
    categories_query = db.session.query(Categories).all()

    return jsonify({"message": "categories found", "results": categories_schema.dump(categories_query)}), 200


@authenticate
def get_category_by_id(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": "category not found"}), 404

    return jsonify({"message": "category found", "result": category_schema.dump(category_query)}), 200


@admin_required
def update_category(category_id, auth_info):
    put_data = request.form if request.form else request.json

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": "category not found"}), 404

    populate_object(category_query, put_data)
    db.session.commit()

    return jsonify({"message": "category updated", "result": category_schema.dump(category_query)}), 200


@admin_required
def delete_category(auth_info):
    post_data = request.form if request.form else request.json
    category_id = post_data.get('category_id')

    if not category_id:
        return jsonify({"message": "category_id is required"}), 400

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": "category not found"}), 404

    dumped = category_schema.dump(category_query)

    db.session.query(ProductsCategoriesXref).filter(ProductsCategoriesXref.category_id == category_id).delete()

    db.session.delete(category_query)
    db.session.commit()

    return jsonify({"message": "category deleted", "result": dumped}), 200
