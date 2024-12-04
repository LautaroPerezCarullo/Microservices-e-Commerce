from flask import Flask
from config import config, cache_config
import os
from .routes import RouteApp
from flask_caching import Cache

cache = Cache()

def create_app():
    app_context = os.getenv("FLASK_CONTEXT")

    app = Flask(__name__)
    configuration = config[app_context if app_context else 'development']
    app.config.from_object(configuration)

    routes = RouteApp()
    routes.init_app(app)
    
    cache.init_app(app, config=cache_config)

    return app   
    