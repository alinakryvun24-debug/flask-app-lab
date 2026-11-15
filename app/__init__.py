import os

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from .config import config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('APP_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import register_routes
    register_routes(app)

    from .users import users_bp
    from .products import products_bp

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(products_bp, url_prefix='/products')

    from .posts import post_bp
    app.register_blueprint(post_bp, url_prefix='/post')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    return app