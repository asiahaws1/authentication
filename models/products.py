import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Products(db.Model):
    __tablename__ = 'Products'

    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Companies.company_id'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    price = db.Column(db.Numeric(10, 2))
    active = db.Column(db.Boolean(), nullable=False, default=True)

    company = db.relationship('Companies', back_populates='products')
    warranty = db.relationship('Warranties', back_populates='product', uselist=False, cascade='all, delete')
    xref = db.relationship('ProductsCategoriesXref', back_populates='product', cascade='all, delete')

    def __init__(self, company_id, name, description=None, price=None, active=True):
        self.company_id = company_id
        self.name = name
        self.description = description
        self.price = price
        self.active = active


    def new_product_obj():
        return Products('', '', None, None, True)


class ProductsSchema(ma.Schema):
    class Meta:
        fields = ['product_id', 'company_id', 'name', 'description', 'price', 'active', 'company', 'warranty', 'xref']

    product_id = ma.fields.UUID()
    company_id = ma.fields.UUID(required=True)
    name = ma.fields.String(required=True)
    description = ma.fields.String(allow_none=True)
    price = ma.fields.Decimal(as_string=True, allow_none=True)
    active = ma.fields.Boolean(required=True, dump_default=True)

    company = ma.fields.Nested('CompaniesSchema', exclude=['products'])
    warranty = ma.fields.Nested('WarrantiesSchema', exclude=['product'])
    xref = ma.fields.Nested('ProductsCategoriesXrefSchema', many=True, exclude=['product'])


product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)
