import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Organizations(db.Model):
    __tablename__ = 'Organizations'


    org_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String())
    email = db.Column(db.String(), nullable=False, unique=True)
    active = db.Column(db.Boolean, nullable=False, default=True)

    users = db.relationship("AppUsers", back_populates='org')

    def __init__(self, name, email, phone=None, active=True):
        self.name = name
        self.email = email
        self.phone = phone
        self.active = active


    def new_org_obj():
        return Organizations('', '', None, True)
    

class OrganizationsSchema(ma.Schema):
    class Meta:
        fields = ['org_id', 'name', 'email', 'phone', 'active', 'users']

    org_id = ma.fields.UUID()
    name = ma.fields.String(required=True)
    email = ma.fields.String(required=True)
    phone = ma.fields.String(allow_none=True)
    active = ma.fields.Boolean(required=True, dump_default=True)

    users = ma.fields.Nested('AppUsersSchema', many=True, only=['user_id', 'first_name', 'last_name', 'email', 'active', 'role'])


org_schema = OrganizationsSchema()
orgs_schema = OrganizationsSchema(many=True)