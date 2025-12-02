from flask import Flask, render_template, request, redirect, url_for
from .models import init_db, add_user, get_users


def create_app():
    app = Flask(__name__)
    init_db()

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            name = request.form.get("name")
            if name:
                add_user(name)
                return redirect(url_for("index"))
        users = get_users()
        return render_template("index.html", users=users)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
