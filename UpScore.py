from flask import Flask
from flask import render_template, redirect, url_for, abort, request, make_response

app = Flask(__name__)


@app.route("/")
def Index():
    return render_template("index.html")

@app.route("/login")
def Login():
    username = request.cookies.get("username")
    if username:
        return username
    return render_template("login.html")

@app.route("/home/<username>")
def Home(username):
    resp = make_response(f"Hello, {username}")
    resp.set_cookie("username", username)
    return resp 



@app.errorhandler(401)
def unauthorized(e):
    return redirect(url_for("Login"))

@app.route("/Test401")
def Test401():
    abort(401)
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("Index"))

@app.route("/Test404")
def Test404():
    abort(404)
    return render_template("index.html")


