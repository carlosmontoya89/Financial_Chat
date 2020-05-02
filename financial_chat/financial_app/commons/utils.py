from flask import Flask, session, redirect, url_for, render_template, request, flash
from functools import wraps


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for("users.login"))

    return wrap
