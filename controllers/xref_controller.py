from flask import jsonify, request

from db import db
from models.products_categories_xref import ProductsCategoriesXref, xref_schema
from models.products import Products
from models.categories import Categories
from lib.authenticate import admin_required


@admin_required
def add_product_category(auth_info):
    post_data = request.form if request.form else request.json
    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    if not product_id or not category_id:
        return jsonify({"message": "product_id and category_id are required"}), 400

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    if not product_query:
        return jsonify({"message": "product not found"}), 404

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    if not category_query:
        return jsonify({"message": "category not found"}), 404

    new_xref = ProductsCategoriesXref(product_id=product_id, category_id=category_id)

    db.session.add(new_xref)
    db.session.commit()

    return jsonify({"message": "product/category association created", "result": xref_schema.dump(new_xref)}), 201
