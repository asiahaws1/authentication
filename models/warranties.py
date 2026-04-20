import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Warranties(db.Model):
    __tablename__ = 'Warranties'

    warranty_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Products.product_id'), nullable=False, unique=True)
    length_months = db.Column(db.Integer())
    description = db.Column(db.String())

    product = db.relationship('Products', back_populates='warranty')

    def __init__(self, product_id, length_months=None, description=None):
        self.product_id = product_id
        self.length_months = length_months
        self.description = description


    def new_warranty_obj():
        return Warranties('', None, None)


class WarrantiesSchema(ma.Schema):
    class Meta:
        fields = ['warranty_id', 'product_id', 'length_months', 'description', 'product']

    warranty_id = ma.fields.UUID()
    product_id = ma.fields.UUID(required=True)
    length_months = ma.fields.Integer(allow_none=True)
    description = ma.fields.String(allow_none=True)

    product = ma.fields.Nested('ProductsSchema', exclude=['warranty'])


warranty_schema = WarrantiesSchema()
warranties_schema = WarrantiesSchema(many=True)
