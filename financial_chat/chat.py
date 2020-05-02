#!/bin/env python

from financial_app import create_app, socketio
import os

app = create_app(config_name=os.getenv("ENV", "dev"))


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    from financial_app.extensions import db

    db.init_app(app)
    socketio.run(app)
