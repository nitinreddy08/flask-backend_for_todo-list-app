# app/routes/auth.py

from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from app.models.user_model import User
from app import db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'message': 'Username, email, and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(
        username=username, 
        email=email, 
        password_hash=hashed_password
    )
    
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    return jsonify({
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email
    }), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    identifier = data.get('identifier')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({'message': 'Identifier and password are required'}), 400

    user = User.query.filter(or_(User.username == identifier, User.email == identifier)).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/check_session', methods=['GET'])
def check_session():
    if current_user.is_authenticated:
        return jsonify({
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email
        }), 200
    else:
        return jsonify({'message': 'No active session'}), 401
