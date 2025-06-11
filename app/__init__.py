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
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql+pymysql://root:123456@localhost:3306/todo_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)  


    from app.routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Define the user loader function for Flask-Login
    from .models.user_model import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app
