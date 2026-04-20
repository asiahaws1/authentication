import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class ProductsCategoriesXref(db.Model):
    __tablename__ = 'ProductsCategoriesXref'

    xref_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Products.product_id'), nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Categories.category_id'), nullable=False)

    product = db.relationship('Products', back_populates='xref')
    category = db.relationship('Categories', back_populates='xref')

    def __init__(self, product_id, category_id):
        self.product_id = product_id
        self.category_id = category_id


    def new_xref_obj():
        return ProductsCategoriesXref('', '')


class ProductsCategoriesXrefSchema(ma.Schema):
    class Meta:
        fields = ['xref_id', 'product_id', 'category_id', 'product', 'category']

    xref_id = ma.fields.UUID()
    product_id = ma.fields.UUID(required=True)
    category_id = ma.fields.UUID(required=True)

    product = ma.fields.Nested('ProductsSchema', exclude=['xref'])
    category = ma.fields.Nested('CategoriesSchema')


xref_schema = ProductsCategoriesXrefSchema()
xrefs_schema = ProductsCategoriesXrefSchema(many=True)
