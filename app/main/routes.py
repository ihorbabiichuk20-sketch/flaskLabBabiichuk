from flask import render_template, redirect, url_for, request
from . import main_bp

@main_bp.route("/")
def index():
    return redirect(url_for("main.resume"))

@main_bp.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме — Ігор Бабійчук")

@main_bp.route("/contacts", methods=["GET", "POST"])
def contacts():
    message_sent = False
    if request.method == "POST":
        message_sent = True
    return render_template("contacts.html",
                           title="Контакти — Ігор Бабійчук",
                           message_sent=message_sent)
