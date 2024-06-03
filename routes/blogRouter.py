from queue import Queue
from flask import Blueprint, jsonify, request
from models.blogModel import Blog, blogs_schema, blog_schema
from services.db import db
from werkzeug.exceptions import BadRequest
from helpers.utilities import send_notification
from concurrent.futures import ThreadPoolExecutor

blog = Blueprint('blog', __name__)

notification_queue = Queue()

def notification_worker(app):
    print("Worker Thread started for notification")
    with app.app_context():
        while True:
            notification_data = notification_queue.get()
            if notification_data is None:
                break  # Stop the thread if None is received
            send_notification(**notification_data)
            notification_queue.task_done()

# Create a blog
@blog.route('/', methods=['POST'])
def add_blog():
    req = request.get_json()
    title = req.get('title')
    content = req.get('content')
    age_from = req.get('age_from')
    age_to = req.get('age_to')
    gender = req.get('gender')

    if not title:
        raise BadRequest('Title is required')
    if not content:
        raise BadRequest('Content is required')
    if age_from is None or age_to is None:
        raise BadRequest('Age from and age to are required')
    if age_from > age_to:
        raise BadRequest('Age from should be less than age to')

    new_blog = Blog(title=title, content=content, age_from=age_from, age_to=age_to, gender=gender)
    db.session.add(new_blog)
    db.session.commit()
    new_blog_id = new_blog.id

    # Add notification task to the queue
    notification_queue.put({
        'blogs': new_blog,
        'blogs_id': new_blog_id,
        'age_from': age_from,
        'age_to': age_to,
        'gender': gender
    })

    return blog_schema.jsonify(new_blog)


# Read all blogs
@blog.route('/', methods=['GET'])
def get_blogs():
    all_blogs = Blog.query.all()
    result = blogs_schema.dump(all_blogs)
    return jsonify(result)

# Update a blog
@blog.route('/<id>', methods=['PUT'])
def update_blog(id):
    blog = Blog.query.get(id)
    req = request.get_json()
    title = req.get('title')
    content = req.get('content')
    age_from = req.get('age_from')
    age_to = req.get('age_to')
    gender = req.get('gender')
    if(title) : blog.title = title
    if(content) : blog.content = content
    if(age_from) : blog.age_from = age_from
    if(age_to) : blog.age_to = age_to
    if(gender) : blog.gender = gender
    db.session.commit()
    return blog_schema.jsonify(blog)

# Delete a blog
@blog.route('/<id>', methods=['DELETE'])
def delete_blog(id):
    blog = Blog.query.get(id)
    if not blog:
        raise BadRequest('Blog not found')
    db.session.delete(blog)
    db.session.commit()
    return blog_schema.jsonify(blog)
