import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Use environment variable for database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'mysql+pymysql://root:123456@localhost:3306/todo_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

    from app.routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)

    with app.app_context():
        db.create_all()

    return app
