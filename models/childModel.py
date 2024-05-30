from services.db import db
from services.marshmello import mm
class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    
class ChildSchema(mm.SQLAlchemyAutoSchema):
    class Meta:
        model = Child
child_schema = ChildSchema()
children_schema = ChildSchema(many=True)