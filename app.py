from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

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
        # Форма-заглушка: дані не зберігаються й нікуди не відправляються
        message_sent = True
    return render_template("contacts.html", title="Контакти — Ігор Бабійчук", message_sent=message_sent)

if __name__ == "__main__":
    app.run(debug=True)
