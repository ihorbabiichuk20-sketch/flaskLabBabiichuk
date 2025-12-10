from flask import Blueprint

posts_bp = Blueprint(
    "posts",
    __name__,
    url_prefix="/post",
    template_folder="templates",
    static_folder="static",
)

from . import views  # noqa: E402,F401
