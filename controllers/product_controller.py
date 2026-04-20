from flask import jsonify, request

from db import db
from models.products import Products, product_schema, products_schema
from models.companies import Companies
from models.warranties import Warranties
from models.products_categories_xref import ProductsCategoriesXref
from util.reflection import populate_object
from lib.authenticate import authenticate, admin_required


@admin_required
def add_product(auth_info):
    post_data = request.form if request.form else request.json
    company_id = post_data.get('company_id')

    if not company_id:
        return jsonify({"message": "company_id is required"}), 400

    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    if not company_query:
        return jsonify({"message": "company not found"}), 404

    new_product = Products.new_product_obj()
    populate_object(new_product, post_data)

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "product created", "result": product_schema.dump(new_product)}), 201


@authenticate
def get_all_products():
    products_query = db.session.query(Products).all()

    return jsonify({"message": "products found", "results": products_schema.dump(products_query)}), 200


@authenticate
def get_active_products():
    products_query = db.session.query(Products).filter(Products.active == True).all()

    return jsonify({"message": "active products found", "results": products_schema.dump(products_query)}), 200


@authenticate
def get_product_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    return jsonify({"message": "product found", "result": product_schema.dump(product_query)}), 200


@authenticate
def get_products_by_company(company_id):
    products_query = db.session.query(Products).filter(Products.company_id == company_id).all()

    return jsonify({"message": "products found", "results": products_schema.dump(products_query)}), 200


@admin_required
def update_product(product_id, auth_info):
    put_data = request.form if request.form else request.json

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    populate_object(product_query, put_data)
    db.session.commit()

    return jsonify({"message": "product updated", "result": product_schema.dump(product_query)}), 200


@admin_required
def delete_product(auth_info):
    post_data = request.form if request.form else request.json
    product_id = post_data.get('product_id')

    if not product_id:
        return jsonify({"message": "product_id is required"}), 400

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    dumped = product_schema.dump(product_query)

    db.session.query(ProductsCategoriesXref).filter(ProductsCategoriesXref.product_id == product_id).delete()
    db.session.query(Warranties).filter(Warranties.product_id == product_id).delete()

    db.session.delete(product_query)
    db.session.commit()

    return jsonify({"message": "product deleted", "result": dumped}), 200
