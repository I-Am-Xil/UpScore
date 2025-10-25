from flask import Blueprint, render_template
from flask_login import login_required

start = Blueprint("start", __name__, template_folder="templates")

@start.route("/")
def index():
    return render_template("index.html")


@start.route("/home")
@login_required
def home():
    return "Home"
