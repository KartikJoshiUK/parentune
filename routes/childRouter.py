from flask import Blueprint, jsonify, request
from models.childModel import Child, child_schema, children_schema
from services.db import db
from werkzeug.exceptions import BadRequest

child = Blueprint('child', __name__)
# Create a child
@child.route('/', methods=['POST'])
def add_child():
    req = request.get_json()
    parent_id = req.get('parent_id')
    name = req.get('name')
    age = req.get('age')
    gender = req.get('gender')

    if not parent_id:
        raise BadRequest('Parent id is required')
    if not name:
        raise BadRequest('Name is required')
    if not age:
        raise BadRequest('Age is required')
    if gender not in ['male', 'female']:
        raise BadRequest('Gender should be male or female')

    new_child = Child(parent_id=parent_id, name=name, age=age, gender=gender)
    db.session.add(new_child)
    db.session.commit()
    return child_schema.jsonify(new_child)

# Read all children
@child.route('/', methods=['GET'])
def get_children():
    all_children = Child.query.all()
    result = children_schema.dump(all_children)
    return jsonify(result)

# Update a child
@child.route('/<id>', methods=['PUT'])
def update_child(id):
    child = Child.query.get(id)
    if not child:
        raise BadRequest('Child not found')

    req = request.get_json()
    name = req.get('name')
    age = req.get('age')
    gender = req.get('gender')

    if(name) : child.name = name
    if(age) : child.age = age
    if(gender) : child.gender = gender
    db.session.commit()
    return child_schema.jsonify(child)

# Delete a child
@child.route('/<id>', methods=['DELETE'])
def delete_child(id):
    child = Child.query.get(id)
    if not child:
        raise BadRequest('Child not found')
    db.session.delete(child)
    db.session.commit()
    return child_schema.jsonify(child)



