from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, login_user, current_user
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__, template_folder="templates")

@auth.route("/login", methods = ["GET", "POST"])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('start.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('start.home'))
        flash('Login fallido. Verifica tu usuario o contraseña.', 'danger')

    return render_template('login.html')

@auth.route("/register")
def register():
    return "register"

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("start.Index"))



