import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')

    # Use DATABASE_URL from environment for production, fallback to local MySQL for dev
    database_url = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:123456@localhost:3306/todo_db')
    # Render provides a 'postgres://' URL, but SQLAlchemy needs 'postgresql://'
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    # This allows your Next.js app to make requests and send/receive cookies.
    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

    from app.routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/api')
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api')

    # Define the user loader function for Flask-Login
    from .models.user_model import User
    @login_manager.user_loader
    def load_user(user_id):
        print(f"--- [DEBUG] Attempting to load user with ID: {user_id} ---")
        user = User.query.get(int(user_id))
        if user:
            print(f"--- [DEBUG] User '{user.username}' loaded successfully. ---")
        else:
            print("--- [DEBUG] User not found in database. ---")
        return user

    with app.app_context():
        db.create_all()

    return app
