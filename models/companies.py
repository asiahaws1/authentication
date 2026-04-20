import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Companies(db.Model):
    __tablename__ = 'Companies'

    company_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String())
    phone = db.Column(db.String())
    active = db.Column(db.Boolean(), nullable=False, default=True)

    products = db.relationship('Products', back_populates='company', cascade='all, delete')

    def __init__(self, name, email=None, phone=None, active=True):
        self.name = name
        self.email = email
        self.phone = phone
        self.active = active


    def new_company_obj():
        return Companies('', None, None, True)


class CompaniesSchema(ma.Schema):
    class Meta:
        fields = ['company_id', 'name', 'email', 'phone', 'active', 'products']

    company_id = ma.fields.UUID()
    name = ma.fields.String(required=True)
    email = ma.fields.String(allow_none=True)
    phone = ma.fields.String(allow_none=True)
    active = ma.fields.Boolean(required=True, dump_default=True)

    products = ma.fields.Nested('ProductsSchema', many=True, exclude=['company'])


company_schema = CompaniesSchema()
companies_schema = CompaniesSchema(many=True)
