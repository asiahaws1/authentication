from flask import jsonify, request

from db import db
from models.companies import Companies, company_schema, companies_schema
from models.products import Products
from models.products_categories_xref import ProductsCategoriesXref
from models.warranties import Warranties
from util.reflection import populate_object
from lib.authenticate import authenticate, admin_required


@admin_required
def add_company(auth_info):
    post_data = request.form if request.form else request.json

    new_company = Companies.new_company_obj()
    populate_object(new_company, post_data)

    db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": "company created", "result": company_schema.dump(new_company)}), 201


@authenticate
def get_all_companies():
    companies_query = db.session.query(Companies).all()

    return jsonify({"message": "companies found", "results": companies_schema.dump(companies_query)}), 200


@authenticate
def get_company_by_id(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": "company not found"}), 404

    return jsonify({"message": "company found", "result": company_schema.dump(company_query)}), 200


@admin_required
def update_company(company_id, auth_info):
    put_data = request.form if request.form else request.json

    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": "company not found"}), 404

    populate_object(company_query, put_data)
    db.session.commit()

    return jsonify({"message": "company updated", "result": company_schema.dump(company_query)}), 200


@admin_required
def delete_company(auth_info):
    post_data = request.form if request.form else request.json
    company_id = post_data.get('company_id')

    if not company_id:
        return jsonify({"message": "company_id is required"}), 400

    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": "company not found"}), 404

    dumped = company_schema.dump(company_query)

    products = db.session.query(Products).filter(Products.company_id == company_id).all()
    for product in products:
        db.session.query(ProductsCategoriesXref).filter(ProductsCategoriesXref.product_id == product.product_id).delete()
        db.session.query(Warranties).filter(Warranties.product_id == product.product_id).delete()
        db.session.delete(product)

    db.session.delete(company_query)
    db.session.commit()

    return jsonify({"message": "company deleted", "result": dumped}), 200
