import unittest
import os
import json
from app import create_app
from app.extensions import db
from app.models import UserModel

class UserTestCase(unittest.TestCase):
    """This class represents the user test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("test")
        self.client = self.app.test_client
        self.user = {
            "name": "carlos",
            "lastname": "montoya",
            "username": "carlosmontoya89",
            "password": "123456"
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_main_page_response(self):
        response = self.client().get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def register(self, name,lastname,username, password, confirm):
        return self.client().post(
            '/register',
            data=dict(name=name,lastname=lastname,username=username, password=password, confirm=confirm),
            follow_redirects=True
        )
    def login(self, username, password):
        return self.client().post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )
 
    def logout(self):
        return self.client().get(
            '/logout',
            follow_redirects=True
        )
    def create_user(self):
        new_user = UserModel(name='Carlos', lastname='Montoya',username='cmontoya89', password='validpassword')
        new_user.save_to_db()
        #db.session.add(new_user)
        #db.session.commit()

    def test_user_registration_response_displays(self):
        response = self.client().get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register to the Chat Application', response.data)

    def test_correct_user_registration(self):
        self.client().get('/register', follow_redirects=True)
        response = self.register('carlos', 'montoya', 'carlosmontoya89', '123456','123456')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations', response.data)
    
    def test_incorrect_user_registration_with_different_passwords(self):
        self.client().get('/register', follow_redirects=True)
        response = self.register('carlos', 'montoya', 'carlosmontoya89', '123456','12345678')
        self.assertIn(b'Passwords must match', response.data)

    def test_incorrect_user_registration_duplicate_username(self):
        self.client().get('/register', follow_redirects=True)
        response = self.register('carlos', 'montoya', 'carlosmontoya89', '123456','123456')
        self.assertEqual(response.status_code, 200)
        response = self.register('charles', 'montoya', 'carlosmontoya89', '123456','123456')
        self.assertIn(b'Please use a different username', response.data)
    
    def test_missing_field_user_registration_error(self):
        self.client().get('/register', follow_redirects=True)
        response = self.register('carlos', 'montoya','','','')
        self.assertIn(b'This field is required.', response.data)

    def test_login_form_displays(self):
        response = self.client().get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)        
        self.assertIn(b'Home', response.data)

    def test_correct_login(self):
        self.client().get('/register', follow_redirects=True)
        response = self.register('carlos', 'montoya', 'cmontoya89', 'validpassword','validpassword')
        self.assertEqual(response.status_code, 200)
        self.client().get('/login', follow_redirects=True)
        response = self.login('cmontoya89', 'validpassword')
        self.assertIn(b'cmontoya89', response.data)
        self.assertIn(b'You are now logged in', response.data)
    
    def test_login_without_registering(self):
        self.client().get('/login', follow_redirects=True)
        response = self.login('nonexistinguser', 'invalidpassword')
        self.assertIn(b'Invalid credentials', response.data)

    def test_invalid_user_login_wrong_password(self):
        self.client().get('/register', follow_redirects=True)
        response = self.register('carlos', 'montoya', 'cmontoya89', 'validpassword','validpassword')
        self.assertEqual(response.status_code, 200)
        self.client().get('/login', follow_redirects=True)
        response = self.login('cmontoya89', 'invalidpassword')
        self.assertIn(b'Invalid credentials', response.data)

    def test_valid_logout(self):
        self.client().get('/register', follow_redirects=True)
        response = self.register('carlos', 'montoya', 'cmontoya89', 'validpassword','validpassword')
        self.assertEqual(response.status_code, 200)
        self.client().get('/login', follow_redirects=True)
        response = self.login('cmontoya89', 'validpassword')
        self.assertIn(b'You are now logged in', response.data)
        response = self.client().get('/logout', follow_redirects=True)
        response = self.logout()
        self.assertIn(b'You have been logged out', response.data)
    
    def test_invalid_logout_within_being_logged_in(self):
        response = self.client().get('/logout', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

   
       

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
