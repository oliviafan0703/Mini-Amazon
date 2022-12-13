from urllib import response
from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)



    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .inventory import bp as inventory_bp
    app.register_blueprint(inventory_bp)
    
    from .users import bp as user_bp
    app.register_blueprint(user_bp)


    from .reviews import bp as reviews_bp
    app.register_blueprint(reviews_bp)

    from .sellers import bp as sellers_bp
    app.register_blueprint(sellers_bp)

    from .carts import bp as carts_bp
    app.register_blueprint(carts_bp)

    from .orders import bp as orders_bp
    app.register_blueprint(orders_bp)

    from .product_details import bp as product_details_bp
    app.register_blueprint(product_details_bp)

    from .order_details import bp as order_details_bp
    app.register_blueprint(order_details_bp)

    from .public_view import bp as public_view_bp
    app.register_blueprint(public_view_bp)
    
    
    return app
