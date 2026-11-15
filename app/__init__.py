from flask import Flask

app = Flask('app')
app.secret_key = 'my_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

from . import views
from .users import users_bp
from .products import products_bp

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(products_bp, url_prefix='/products')