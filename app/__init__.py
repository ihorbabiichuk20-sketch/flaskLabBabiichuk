from flask import Flask, render_template
from .extensions import db, login_manager
from .models import User, NotebookBrand, Notebook


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    from .auth.routes import auth_bp
    from .notebooks.routes import notebooks_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(notebooks_bp, url_prefix="/notebooks")

    # Ініціалізуємо БД та наповнюємо бренди одразу при створенні застосунку
    with app.app_context():
        db.create_all()
        if not NotebookBrand.query.first():
            brands = ["Lenovo", "Dell", "HP", "Apple", "Asus", "Acer"]
            for name in brands:
                db.session.add(NotebookBrand(name=name))
            db.session.commit()

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
