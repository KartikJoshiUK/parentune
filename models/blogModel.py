from services.db import db
from services.marshmello import mm

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    age_from = db.Column(db.Integer, nullable=False)
    age_to = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

class BlogSchema(mm.SQLAlchemyAutoSchema):
    class Meta:
        model = Blog

blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)