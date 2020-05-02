from flask import session, Blueprint, redirect, url_for, render_template, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from .forms import LoginForm, RegisterForm
from werkzeug.security import safe_str_cmp

from financial_app.models import UserModel
from financial_app.extensions import db

# from financial_app.commons.utils import login_required


users_blueprint = Blueprint("users", __name__, template_folder="templates")


@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Login form to enter a room."""
    if current_user.is_authenticated:
        return redirect(url_for("messages.chatroom"))
    form = LoginForm()
    if request.method == "POST":
        error = None
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = UserModel.find_by_username(username)
            if user is None or not user.verify_password(form.password.data):
                error = "Invalid credentials"
                return render_template("login.html", form=form, error=error)
            login_user(user, remember=form.remember_me.data)
            # session['logged_in'] = True
            session['name'] = username
            session['id']=user.id
            flash("You are now logged in. Welcome back!", "success")
            return redirect(url_for("messages.chatroom"))
    return render_template("login.html", title="Sign In", form=form)


@users_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """Register form to enter a room."""
    if current_user.is_authenticated:
        return redirect(url_for("messages.chatroom"))
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            lastname = form.lastname.data
            username = form.username.data
            password = form.password.data
            user = UserModel(
                name=name, lastname=lastname, username=username, password=password
            )
            user.save_to_db()
            flash("Congratulations, you are now a registered user!", "success")
            return redirect(url_for("users.login"))
    # elif request.method == 'GET':
    #    form.name.data = session.get('name', '')
    return render_template("register.html", form=form)


@users_blueprint.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for("users.login"))
