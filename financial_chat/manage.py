import os
import unittest
from flask_script import Manager  # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from financial_app import create_app, socketio
from financial_app.extensions import db
from financial_app import models


app = create_app(config_name=os.getenv("ENV", "dev"))
app.app_context().push()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)


@manager.command
def runserver():
    # socketio.run(app)
    app.run()


@manager.command
def tests():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover("tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
