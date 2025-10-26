from flask import Blueprint, render_template
from flask_login import login_required, current_user
from query import get_account_health_score

start = Blueprint("start", __name__, template_folder="templates")

@start.route("/")
def index():
    return render_template("index.html")


@start.route("/home")
@login_required
def home():
    usr_health_score = get_account_health_score(current_user.id)

    return render_template("home.html", finScore=str(usr_health_score))
