from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.forms import ContactForm
import logging
import os

main_bp = Blueprint("main", __name__)

# Налаштування логування для контактної форми
logger = logging.getLogger("contact_logger")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "contact_form.log")
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


@main_bp.route("/")
def index():
    return render_template("main/index.html")


@main_bp.route("/resume")
def resume():
    return render_template("main/resume.html")


@main_bp.route("/contacts", methods=["GET", "POST"])
@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "email": form.email.data,
            "phone": form.phone.data,
            "subject": form.subject.data,
            "message": form.message.data,
            "ip": request.remote_addr,
        }
        try:
            logger.info("Contact form submitted: %s", data)
            flash(f"Повідомлення від {data['name']} ({data['email']}) успішно надіслано.", "success")
        except Exception as exc:
            logger.error("Error while logging contact form: %s", exc)
            flash("Сталася помилка під час збереження ваших даних. Спробуйте ще раз.", "danger")
        # Post/Redirect/Get
        return redirect(url_for("main.contact"))
    elif request.method == "POST":
        flash("Будь ласка, виправте помилки у формі.", "warning")

    return render_template("main/contacts.html", form=form)