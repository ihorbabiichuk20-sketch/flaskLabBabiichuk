from datetime import timedelta

from flask import (
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
    make_response,
)

from . import users_bp


# ===== Helper section =====

VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"


def is_authenticated() -> bool:
    return "user" in session


# ===== Lab3 examples (hi/admin) =====

@users_bp.route("/hi/<name>")
def hi(name: str):
    return render_template("users/hi.html", name=name)


@users_bp.route("/admin")
def admin():
    # Simple stub-page to demonstrate blueprint usage
    return render_template("users/admin.html")


# ===== Lab4: login/profile/session/cookies/theme =====

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["user"] = username
            # 30 minutes of "remember me" as a simple example
            session.permanent = True
            flash("Ви успішно увійшли в систему.", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Невірний логін або пароль.", "danger")
            return redirect(url_for("users.login"))

    # GET
    return render_template("users/login.html")


@users_bp.route("/profile")
def profile():
    if not is_authenticated():
        flash("Будь ласка, увійдіть, щоб переглянути профіль.", "warning")
        return redirect(url_for("users.login"))

    username = session.get("user")
    theme = request.cookies.get("profile_theme", "light")

    # Список поточних кукі для відображення у таблиці
    cookies = request.cookies.items()

    return render_template(
        "users/profile.html",
        username=username,
        cookies=cookies,
        current_theme=theme,
    )


@users_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("users.login"))


@users_bp.route("/profile/cookies/add", methods=["POST"])
def add_cookie():
    if not is_authenticated():
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "").strip()
    # Вкажемо тривалість у хвилинах як приклад
    max_age_minutes_raw = request.form.get("max_age_minutes", "").strip()

    resp = make_response(redirect(url_for("users.profile")))

    if not key or not value:
        flash("Ключ і значення обов'язкові для заповнення.", "danger")
        return resp

    if max_age_minutes_raw:
        try:
            minutes = int(max_age_minutes_raw)
            max_age = minutes * 60
        except ValueError:
            max_age = None
            flash("Некоректне значення терміну дії. Кукі буде створено без обмеження часу.", "warning")
    else:
        max_age = None

    if max_age is not None:
        resp.set_cookie(key, value, max_age=max_age)
    else:
        resp.set_cookie(key, value)

    flash(f"Кукі з ключем '{key}' успішно додано.", "success")
    return resp


@users_bp.route("/profile/cookies/delete", methods=["POST"])
def delete_cookie():
    if not is_authenticated():
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    action = request.form.get("action")
    key = request.form.get("key_to_delete", "").strip()

    resp = make_response(redirect(url_for("users.profile")))

    if action == "all":
        # Не видаляємо службові кукі на кшталт session
        for cookie_key in list(request.cookies.keys()):
            if cookie_key != "session":
                resp.delete_cookie(cookie_key)
        flash("Усі користувацькі кукі (окрім службових) видалено.", "info")
    elif action == "one":
        if not key:
            flash("Вкажіть ключ кукі для видалення.", "danger")
        else:
            if key in request.cookies:
                resp.delete_cookie(key)
                flash(f"Кукі з ключем '{key}' видалено.", "info")
            else:
                flash(f"Кукі з ключем '{key}' не знайдено.", "warning")
    else:
        flash("Некоректна дія для видалення кукі.", "danger")

    return resp


@users_bp.route("/profile/theme/<theme_name>")
def set_theme(theme_name: str):
    if not is_authenticated():
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    if theme_name not in ("light", "dark"):
        theme_name = "light"

    resp = make_response(redirect(url_for("users.profile")))
    # Збережемо вибір на 30 днів
    resp.set_cookie("profile_theme", theme_name, max_age=60 * 60 * 24 * 30)
    flash("Кольорову схему змінено.", "info")
    return resp
