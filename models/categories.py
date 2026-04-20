import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Categories(db.Model):
    __tablename__ = 'Categories'

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    active = db.Column(db.Boolean(), nullable=False, default=True)

    xref = db.relationship('ProductsCategoriesXref', back_populates='category', cascade='all, delete')

    def __init__(self, name, description=None, active=True):
        self.name = name
        self.description = description
        self.active = active


    def new_category_obj():
        return Categories('', None, True)


class CategoriesSchema(ma.Schema):
    class Meta:
        fields = ['category_id', 'name', 'description', 'active']

    category_id = ma.fields.UUID()
    name = ma.fields.String(required=True)
    description = ma.fields.String(allow_none=True)
    active = ma.fields.Boolean(required=True, dump_default=True)


category_schema = CategoriesSchema()
categories_schema = CategoriesSchema(many=True)
