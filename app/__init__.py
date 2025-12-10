import os
from flask import Flask, render_template
from .config import Config, config_map
from .extensions import db, migrate

def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # Config
    config_name = config_name or os.getenv("FLASK_CONFIG", "development")
    cfg_class = config_map.get(config_name, Config)
    app.config.from_object(cfg_class)

    # Ensure instance dir exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    from .posts import posts_bp
    app.register_blueprint(posts_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    # Auto create tables so project works out-of-the-box
    with app.app_context():
        db.create_all()

    return app
