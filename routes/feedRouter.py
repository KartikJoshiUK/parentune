from flask import Blueprint, jsonify, request
from models.parentModel import Parent
from models.childModel import Child
from models.blogModel import Blog, blogs_schema
from sqlalchemy import and_
from werkzeug.exceptions import BadRequest

feed = Blueprint('feed', __name__)

# Feed of a parent
@feed.route('/<parent_id>', methods=['GET'])
def home_feed(parent_id):
    parent = Parent.query.get(parent_id)
    if not parent:
        return jsonify({"message": "Parent not found"}), 404

    child = Child.query.filter_by(parent_id=parent_id).first()
    if not child:
        return jsonify({"message": "Child not found"}), 404

    blogs = Blog.query.filter(
        (child.age >= Blog.age_from) & (child.age <= Blog.age_to) & (Blog.gender == child.gender)
    ).all()
    return blogs_schema.jsonify(blogs)

# Custom Feed
@feed.route('/', methods=['POST'])
def custom_home_feed():
    preferences = request.json
    age_from = preferences.get('age_from')
    age_to = preferences.get('age_to')
    gender = preferences.get('gender')

    if age_from is not None and age_to is not None and age_from > age_to:
        raise BadRequest('Age from should be less than or equal to age to')

    if gender not in [None, 'male', 'female']:
        raise BadRequest('Gender should be male or female')

    filters = []


    if age_from is not None:
        filters.append(Blog.age_from >= age_from)
        filters.append(Blog.age_to <= age_from)
    if age_to is not None:
        filters.append(Blog.age_from <= age_to)
        filters.append(Blog.age_to >= age_to)
    if gender is not None:
        filters.append(Blog.gender == gender)

    blogs = Blog.query.filter(and_(*filters)).all()
    return blogs_schema.jsonify(blogs)
