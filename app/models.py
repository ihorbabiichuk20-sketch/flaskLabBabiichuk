from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    notebooks = db.relationship("Notebook", back_populates="owner", lazy="dynamic")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username!r}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class NotebookBrand(db.Model):
    __tablename__ = "notebook_brands"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    notebooks = db.relationship("Notebook", back_populates="brand", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<NotebookBrand {self.name!r}>"


class Notebook(db.Model):
    __tablename__ = "notebooks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    brand_id = db.Column(db.Integer, db.ForeignKey("notebook_brands.id"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    brand = db.relationship("NotebookBrand", back_populates="notebooks")
    owner = db.relationship("User", back_populates="notebooks")

    def __repr__(self) -> str:
        return f"<Notebook {self.name!r}>"
