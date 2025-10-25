from flask import Flask, render_template, redirect, url_for, abort, request, make_response
from flask_login import LoginManager, login_required


app = Flask(__name__)

secret_key_file = open("./key.secret", "r")
app.secret_key = secret_key_file.read()
secret_key_file.close()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)



@app.route("/")
def Index():
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
def Login():
    form = LoginForm()
    return render_template("login.html")


@app.route("/home")
@login_required
def Home():
    """
    resp = make_response(f"Hello, {}")
    resp.set_cookie("username", )
    return resp 
    """
    return "Home"


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


