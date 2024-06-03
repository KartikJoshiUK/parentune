from flask import Blueprint, jsonify, request
from models.userModel import User, user_schema, users_schema  # Ensure this file is properly created and imported
from services.db import db
from werkzeug.exceptions import BadRequest

user = Blueprint('user', __name__)

# Create a user
@user.route('/', methods=['POST'])
def add_user():
    req = request.get_json()
    name = req.get('name')
    email = req.get('email')
    password = req.get('password')

    if not name:
        raise BadRequest('Name is required')
    if not email:
        raise BadRequest('Email is required')
    if not password:
        raise BadRequest('Password is required')

    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

# Read all users
@user.route('/', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# Update a user
@user.route('/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        raise BadRequest('User not found')

    req = request.get_json()
    name = req.get('name')
    email = req.get('email')
    password = req.get('password')

    if name:
        user.name = name
    if email:
        user.email = email
    if password:
        user.password = password

    db.session.commit()
    return user_schema.jsonify(user)

# Delete a user
@user.route('/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        raise BadRequest('User not found')
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)
