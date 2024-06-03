from services.db import db
from services.marshmello import mm

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)
    to = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)


class NotificationSchema(mm.SQLAlchemyAutoSchema):
    class Meta:
        model = Notification

notification_schema = NotificationSchema()
notifications_schema = NotificationSchema(many=True)
