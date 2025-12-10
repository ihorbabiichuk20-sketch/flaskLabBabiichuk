from flask import render_template, request, redirect, url_for

from app.users import bp


@bp.route("/hi/<name>")
def greetings(name):
    """
    Greeting page that shows user name and age (if provided via query string).
    Example: /users/hi/John?age=30
    """
    age = request.args.get("age")
    return render_template("users/hi.html", name=name, age=age)


@bp.route("/admin")
def admin():
    """
    Admin page that redirects to greetings page with hardcoded ADMINISTRATOR user.
    """
    return redirect(url_for("users.greetings", name="ADMINISTRATOR", age=45))
