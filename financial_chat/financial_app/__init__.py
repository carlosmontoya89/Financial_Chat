from flask import Flask, g, render_template
from datetime import datetime as dt
import os
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler

from .config import config_by_name
from .extensions import db, migrate, login_manager, socketio
from financial_app.users.views import users_blueprint
from financial_app.messages.views import messages_blueprint



def create_app(config_name):
    app = Flask(__name__)
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("flask_cors").level = logging.INFO
    handler = RotatingFileHandler("chat_logs.log", maxBytes=10000, backupCount=1)
    app.logger.addHandler(handler)
    app.config.from_object(config_by_name[config_name])
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # api = Api(app)
    configure_extensions(app)
    register_blueprints(app)
    

    return app


def configure_extensions(app):
    migrate.init_app(app, db)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "users.login"
    socketio.init_app(app)


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(users_blueprint)
    app.register_blueprint(messages_blueprint)
    @app.route('/', methods=['GET', 'POST'])
    @app.route('/index', methods=['GET', 'POST'])
    def index():
        return render_template('index.html')
    pass
