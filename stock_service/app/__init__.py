from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config, cache_config
from flask_caching import Cache
from .routes import RouteApp
import os

db = SQLAlchemy()
cache = Cache()

def create_app():
    app_context = os.getenv("FLASK_CONTEXT")
    
    app = Flask(__name__)
    configuration = config[app_context if app_context else 'development']
    app.config.from_object(configuration)

    route = RouteApp()
    route.init_app(app)

    db.init_app(app)
    cache.init_app(app, config=cache_config)

    return app     