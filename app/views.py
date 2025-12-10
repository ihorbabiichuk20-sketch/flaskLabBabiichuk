from flask import render_template, redirect, url_for, request

from app import app


@app.route("/")
def index():
    return redirect(url_for("resume"))


@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме — Ігор Бабійчук")


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    message_sent = False
    if request.method == "POST":
        # Form stub: we do not store data anywhere
        message_sent = True
    return render_template(
        "contacts.html",
        title="Контакти — Ігор Бабійчук",
        message_sent=message_sent,
    )
