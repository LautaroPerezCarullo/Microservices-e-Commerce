class RouteApp:
    def init_app(self, app):
        from .resources import product_bp
        app.register_blueprint(product_bp, url_prefix='/api/v1')