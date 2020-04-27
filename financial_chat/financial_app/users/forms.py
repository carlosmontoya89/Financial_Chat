from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import Required, EqualTo,ValidationError,Length

from financial_app.models import UserModel


class LoginForm(Form):    
    username= StringField('UserName', validators=[Required()])  
    password= PasswordField('PassWord', validators=[Required(),Length(min=6, max=254)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegisterForm(Form):
    name = StringField('Name', validators=[Required()])  
    lastname=StringField('Lastname', validators=[Required()]) 
    username = StringField('Username', validators=[Required()])
    password = PasswordField('PassWord', validators=[Required(),Length(min=6, max=254)])
    confirm = PasswordField('Confirm PassWord',validators=[Required(), EqualTo('password', 'Passwords must match')]) 
    submit = SubmitField('Register')
    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')