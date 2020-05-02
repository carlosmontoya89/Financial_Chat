from flask import Flask, g, render_template, session,redirect, url_for
from datetime import datetime as dt
import os
from flask_cors import CORS
from flask_login import current_user
import logging
from logging.handlers import RotatingFileHandler
from flask_socketio import emit, join_room, leave_room, send
import datetime


# from flask_socketio import SocketIO

from financial_app.config import config_by_name
from financial_app.extensions import db, migrate, login_manager, socketio
from financial_app.users.views import users_blueprint
from financial_app.messages.views import messages_blueprint
from financial_app import events
#from models import Message


def create_app(config_name):
    app = Flask(__name__)
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("flask_cors").level = logging.INFO
    handler = RotatingFileHandler("chat_logs.log", maxBytes=10000, backupCount=1)
    app.logger.addHandler(handler)
    app.config.from_object(config_by_name[config_name])
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    configure_extensions(app)
    register_blueprints(app)

    socketio.init_app(app)
    return app


def configure_extensions(app):
    migrate.init_app(app, db)
    db.init_app(app)    
    login_manager.init_app(app)
    login_manager.login_view = "users.login"


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(users_blueprint)
    app.register_blueprint(messages_blueprint)

    @app.route("/", methods=["GET", "POST"])
    @app.route("/index", methods=["GET", "POST"])
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("messages.chatroom"))
        return render_template("index.html")
    