from flask import Blueprint, jsonify, request
from models.parentModel import Parent, parent_schema, parents_schema
from services.db import db
from werkzeug.exceptions import BadRequest

parent = Blueprint('parent', __name__)

# Create a parent
@parent.route('/', methods=['POST'])
def add_parent():
    req = request.get_json()
    name = req.get('name')
    email = req.get('email')
    parent_type = req.get('parent_type')

    if not name:
        raise BadRequest('Name is required')
    if not email:
        raise BadRequest('Email is required')
    if not parent_type:
        raise BadRequest('Parent type is required')

    new_parent = Parent(name=name, email=email, parent_type=parent_type)
    db.session.add(new_parent)
    db.session.commit()
    return parent_schema.jsonify(new_parent)

# Read all parents
@parent.route('/', methods=['GET'])
def get_parents():
    all_parents = Parent.query.all()
    result = parents_schema.dump(all_parents)
    return jsonify(result)

# Update a parent
@parent.route('/<id>', methods=['PUT'])
def update_parent(id):
    parent = Parent.query.get(id)
    if not parent:
        raise BadRequest('Parent not found')

    req = request.get_json()
    name = req.get('name')
    email = req.get('email')
    parent_type = req.get('parent_type')

    if(name) : parent.name = name
    if(email) : parent.email = email
    if(parent_type) : parent.parent_type = parent_type
    db.session.commit()
    return parent_schema.jsonify(parent)

# Delete a parent
@parent.route('/<id>', methods=['DELETE'])
def delete_parent(id):
    parent = Parent.query.get(id)
    if not parent:
        raise BadRequest('Parent not found')

    db.session.delete(parent)
    db.session.commit()
    return parent_schema.jsonify(parent)
