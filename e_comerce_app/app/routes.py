class RouteApp:
    def init_app(self, app):
        from .resources import e_commerce_bp
        app.register_blueprint(e_commerce_bp, url_prefix='/api/v1')