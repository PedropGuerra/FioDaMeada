from flask import Flask, render_template, request
from sql_fiodameada import Parceiros, connect_db, disconnect_db
import feedparser

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def cadastro():
    error = None
    if request.method == "POST":
        connect_db()
        return Parceiros().confirm_tags(request.form["link"])

    else:
        pass

    return render_template("index.html", error=error)


if __name__ == "__main__":
    app.run(debug=True)
