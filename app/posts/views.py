from flask import render_template, redirect, url_for, flash, request, session, abort
from sqlalchemy import select, desc
from . import posts_bp
from .models import Post
from .forms import PostForm
from ..extensions import db

@posts_bp.route("/", methods=["GET"])
def list_posts():
    stmt = select(Post).where(Post.is_active.is_(True)).order_by(desc(Post.posted))
    posts = db.session.scalars(stmt).all()
    return render_template("posts/posts.html", posts=posts)

@posts_bp.route("/create", methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        author = session.get("username", "Anonymous")
        post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.publish_date.data,
            category=form.category.data,
            is_active=form.is_active.data,
            author=author,
        )
        db.session.add(post)
        db.session.commit()
        flash("Post added successfully", "success")
        return redirect(url_for("posts.list_posts"))
    return render_template("posts/add_post.html", form=form, title="Create a New Post")

@posts_bp.route("/<int:id>", methods=["GET"])
def detail_post(id: int):
    post = db.get_or_404(Post, id)
    return render_template("posts/detail_post.html", post=post)

@posts_bp.route("/<int:id>/update", methods=["GET", "POST"])
def edit_post(id: int):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        form.populate_obj(post)
        post.posted = form.publish_date.data
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("posts.detail_post", id=post.id))
    # Fix publish_date initial value manually
    if request.method == "GET":
        form.publish_date.data = post.posted
    return render_template("posts/add_post.html", form=form, title=f"Edit Post #{post.id}")

@posts_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id: int):
    post = db.get_or_404(Post, id)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "info")
        return redirect(url_for("posts.list_posts"))
    return render_template("posts/delete_confirm.html", post=post)
