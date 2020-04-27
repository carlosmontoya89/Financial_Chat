from flask import Flask, g
from datetime import datetime as dt
import os
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler

from .config import config_by_name
from .extensions import db
from .extensions import migrate


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

    @app.route("/", methods=["GET"])
    def index():
        return "chat api"

    return app


def configure_extensions(app):
    migrate.init_app(app, db)
    db.init_app(app)


def register_blueprints(app):
    """register all blueprints for application
    """
    pass
