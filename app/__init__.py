from flask import Flask
from app.routes.tasks import tasks_bp  # importing blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(tasks_bp)
    return app
