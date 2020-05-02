from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required


class ChatRoomsForm(Form):
    chatroom = StringField("Room", validators=[Required()])
    submit = SubmitField("Enter to ChatRoom")
