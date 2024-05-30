from services.db import db
from services.marshmello import mm
from routes.childRouter import Child  # Import the Child model

class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    parent_type = db.Column(db.String(50), nullable=False)
    children = db.relationship('Child', backref='parent', lazy=True)

class ParentSchema(mm.SQLAlchemyAutoSchema):
    class Meta:
        model = Parent
parent_schema = ParentSchema()
parents_schema = ParentSchema(many=True)