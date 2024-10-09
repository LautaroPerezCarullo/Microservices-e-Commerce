from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import os

db = SQLAlchemy()

def create_app():
    app_context = os.getenv("FLASK_CONTEXT")
    
    app = Flask(__name__)
    configuration = config[app_context if app_context else 'development']
    app.config.from_object(configuration)

    db.init_app(app)

    return app      