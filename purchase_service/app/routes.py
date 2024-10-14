class RouteApp:
    def init_app(self, app):
        from .resources import purchase_bp
        app.register_blueprint(purchase_bp, url_prefix='/api/v1')