from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort,
)
from flask_login import login_required, current_user

from . import notebooks_bp
from .forms import NotebookForm
from ..extensions import db
from ..models import Notebook, NotebookBrand


@notebooks_bp.route("/", methods=["GET"])
def list_notebooks():
    sort_by = request.args.get("sort_by", "name")
    search = request.args.get("search", "").strip()

    query = Notebook.query

    if search:
        query = query.filter(Notebook.name.ilike(f"%{search}%"))

    if sort_by == "price":
        query = query.order_by(Notebook.price.asc())
    elif sort_by == "created_at":
        query = query.order_by(Notebook.created_at.desc())
    else:
        query = query.order_by(Notebook.name.asc())

    notebooks = query.all()
    return render_template(
        "notebooks/list.html",
        notebooks=notebooks,
        sort_by=sort_by,
        search=search,
    )


@notebooks_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_notebook():
    form = NotebookForm()
    form.brand_id.choices = [
        (b.id, b.name) for b in NotebookBrand.query.order_by(NotebookBrand.name).all()
    ]

    if form.validate_on_submit():
        notebook = Notebook(
            name=form.name.data.strip(),
            description=form.description.data.strip() if form.description.data else "",
            price=float(form.price.data),
            brand_id=form.brand_id.data,
            owner=current_user,
        )
        db.session.add(notebook)
        db.session.commit()
        flash("Ноутбук успішно створено.", "success")
        return redirect(url_for("notebooks.list_notebooks"))

    return render_template("notebooks/form.html", form=form, title="Створити ноутбук")


def get_notebook_or_404(notebook_id: int) -> Notebook:
    notebook = Notebook.query.get_or_404(notebook_id)
    return notebook


def ensure_owner(notebook: Notebook) -> None:
    if notebook.owner_id != current_user.id:
        abort(403)


@notebooks_bp.route("/<int:notebook_id>", methods=["GET"])
def notebook_detail(notebook_id):
    notebook = get_notebook_or_404(notebook_id)
    return render_template("notebooks/detail.html", notebook=notebook)


@notebooks_bp.route("/<int:notebook_id>/edit", methods=["GET", "POST"])
@login_required
def edit_notebook(notebook_id):
    notebook = get_notebook_or_404(notebook_id)
    ensure_owner(notebook)

    form = NotebookForm(obj=notebook)
    form.brand_id.choices = [
        (b.id, b.name) for b in NotebookBrand.query.order_by(NotebookBrand.name).all()
    ]

    if form.validate_on_submit():
        notebook.name = form.name.data.strip()
        notebook.description = form.description.data.strip() if form.description.data else ""
        notebook.price = float(form.price.data)
        notebook.brand_id = form.brand_id.data
        db.session.commit()
        flash("Ноутбук оновлено.", "success")
        return redirect(url_for("notebooks.notebook_detail", notebook_id=notebook.id))

    return render_template(
        "notebooks/form.html",
        form=form,
        title="Редагувати ноутбук",
    )


@notebooks_bp.route("/<int:notebook_id>/delete", methods=["POST"])
@login_required
def delete_notebook(notebook_id):
    notebook = get_notebook_or_404(notebook_id)
    ensure_owner(notebook)

    db.session.delete(notebook)
    db.session.commit()
    flash("Ноутбук видалено.", "info")
    return redirect(url_for("notebooks.list_notebooks"))
