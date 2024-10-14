class RouteApp:
    def init_app(self, app):
        from .resources import payment_bp
        app.register_blueprint(payment_bp, url_prefix='/api/v1')