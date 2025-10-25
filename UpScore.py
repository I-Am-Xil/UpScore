from flask import Flask, render_template, redirect, url_for,  make_response, abort
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


db = SQLAlchemy()
from models import User

secret_key_file = open("./key.secret", "r")
app.config["SECRET_KEY"] = secret_key_file.read()
secret_key_file.close()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from start import start
app.register_blueprint(start)

from auth import auth
app.register_blueprint(auth)


@app.errorhandler(401)
def unauthorized(e):
    return redirect(url_for("start.index"))

@app.route("/test401")
def Test401():
    abort(401)


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("start.index"))

@app.route("/test404")
def Test404():
    abort(404)



with app.app_context():
    db.create_all()
    print("Base de datos creada.")
