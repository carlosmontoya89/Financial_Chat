import unittest
from flask import url_for


from financial_app import create_app
from financial_app.extensions import db
from financial_app.models import UserModel


class UserTestCase(unittest.TestCase):
    """This class represents the user test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("test")
        self.client = self.app.test_client()
        self.user = {
            "name": "carlos",
            "lastname": "montoya",
            "username": "carlosmontoya89",
            "password": "123456",
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def register(self, name, lastname, username, password, confirm):
        return self.client.post(
            url_for("users.register"),
            data=dict(
                name=name,
                lastname=lastname,
                username=username,
                password=password,
                confirm=confirm,
            ),
            follow_redirects=True,
        )

    def login(self, username, password):
        return self.client.post(
            url_for("users.login"),
            data=dict(username=username, password=password),
            follow_redirects=True,
        )

    def logout(self):
        return self.client.get(url_for("users.logout"), follow_redirects=True)

    def create_user(self):
        new_user = UserModel(
            name="Carlos",
            lastname="Montoya",
            username="cmontoya89",
            password="validpassword",
        )
        new_user.save_to_db()

    def test_main_page_response(self):
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_user_registration_response_displays(self):
        response = self.client.get(url_for("users.register"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Register to the Chat Application", response.data)

    def test_correct_user_registration(self):
        response = self.register(
            "carlos", "montoya", "carlosmontoya89", "123456", "123456"
        )
        self.assertEqual(response.status_code, 200)

    def test_incorrect_user_registration_with_different_passwords(self):
        response = self.register(
            "carlos", "montoya", "cmontoya89", "123456", "12345678"
        )
        self.assertIn(b"Passwords must match", response.data)

    def test_incorrect_user_registration_duplicate_username(self):
        self.create_user()
        response = self.register("charles", "montoya", "cmontoya89", "123456", "123456")
        self.assertIn(b"Please use a different username", response.data)

    def test_missing_field_user_registration_error(self):
        response = self.register("carlos", "montoya", "", "", "")
        self.assertIn(b"This field is required.", response.data)

    def test_login_form_displays(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Log In", response.data)
        self.assertIn(b"Home", response.data)

    def test_redirect_to_login(self):
        res = self.client.get("/chatroom")
        self.assertEqual(302, res.status_code)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
