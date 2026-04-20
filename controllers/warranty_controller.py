from flask import jsonify, request

from db import db
from models.warranties import Warranties, warranty_schema
from models.products import Products
from util.reflection import populate_object
from lib.authenticate import authenticate, admin_required


@admin_required
def add_warranty(auth_info):
    post_data = request.form if request.form else request.json
    product_id = post_data.get('product_id')

    if not product_id:
        return jsonify({"message": "product_id is required"}), 400

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    if not product_query:
        return jsonify({"message": "product not found"}), 404

    new_warranty = Warranties.new_warranty_obj()
    populate_object(new_warranty, post_data)

    db.session.add(new_warranty)
    db.session.commit()

    return jsonify({"message": "warranty created", "result": warranty_schema.dump(new_warranty)}), 201


@authenticate
def get_warranty_by_id(warranty_id):
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": "warranty not found"}), 404

    return jsonify({"message": "warranty found", "result": warranty_schema.dump(warranty_query)}), 200


@admin_required
def update_warranty(warranty_id, auth_info):
    put_data = request.form if request.form else request.json

    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": "warranty not found"}), 404

    populate_object(warranty_query, put_data)
    db.session.commit()

    return jsonify({"message": "warranty updated", "result": warranty_schema.dump(warranty_query)}), 200


@admin_required
def delete_warranty(auth_info):
    post_data = request.form if request.form else request.json
    warranty_id = post_data.get('warranty_id')

    if not warranty_id:
        return jsonify({"message": "warranty_id is required"}), 400

    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": "warranty not found"}), 404

    dumped = warranty_schema.dump(warranty_query)

    db.session.delete(warranty_query)
    db.session.commit()

    return jsonify({"message": "warranty deleted", "result": dumped}), 200
