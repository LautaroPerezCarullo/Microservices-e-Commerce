class RouteApp:
    def init_app(self, app):
        from .resources import stock_bp
        app.register_blueprint(stock_bp, url_prefix='/api/v1')