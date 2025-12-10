from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Import and register blueprints
from app.users import bp as users_bp  # noqa
from app.products import bp as products_bp  # noqa
from app import views  # noqa  # keep after app definition

app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(products_bp, url_prefix="/products")
