from flask import Blueprint, jsonify, request
from models.notificationModel import Notification, notifications_schema, notification_schema
from services.db import db
from werkzeug.exceptions import BadRequest
from helpers.utilities import send_email

notification = Blueprint('notification', __name__)

# Read all notification
@notification.route('/', methods=['GET'])
def get_notification():
    all_blogs = Notification.query.all()
    result = notification_schema.dump(all_blogs)
    return jsonify(result)

# Read all notification
@notification.route('/<parent_id>', methods=['GET'])
def get_notification_of_parent(parent_id):
    notifications = Notification.query.filter((Notification.to == parent_id)).all()
    return notifications_schema.jsonify(notifications)


