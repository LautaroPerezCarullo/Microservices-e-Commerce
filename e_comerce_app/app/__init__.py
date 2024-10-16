from flask import Flask
from config import config
import os
from .routes import RouteApp

def create_app():
    app_context = os.getenv("FLASK_CONTEXT")

    app = Flask(__name__)
    configuration = config[app_context if app_context else 'development']
    app.config.from_object(configuration)

    routes = RouteApp()
    routes.init_app(app)

    return app   
    