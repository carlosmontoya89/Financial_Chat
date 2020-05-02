from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import Required, EqualTo, ValidationError, Length


class ChatRoomsForm(Form):
    chatroom = StringField("Room", validators=[Required()])
    submit = SubmitField("Enter to ChatRoom")
