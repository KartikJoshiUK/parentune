from flask import Blueprint, request
from models.userModel import User
from services.db import db
from flask import session, redirect, url_for

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body.get('email')
    password = body.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        session['user_id'] = user.id
        return {'message': 'Login successful'}


@auth.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        return {'message': 'Logout successful'}
    return {'message': 'User not logged in'}


@auth.route('/protected')
def protected():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return f"Hello, {user.name}!"
    return redirect(url_for('login'))