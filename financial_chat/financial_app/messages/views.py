from flask import session, Blueprint, redirect, url_for, render_template, request, flash
from flask_login import current_user, login_user,login_required, logout_user
from .forms import ChatRoomsForm
from werkzeug.security import safe_str_cmp

from financial_app.models import MessageModel
from financial_app.extensions import db

messages_blueprint = Blueprint('messages', __name__, template_folder='templates')


@messages_blueprint.route('/chatroom', methods=['GET', 'POST'])
@login_required
def chatroom():
    form = ChatRoomsForm() 
    if form.validate_on_submit():
        session['chatroom'] = form.chatroom.data
        return redirect(url_for('messages.chat'))    
    return render_template('chatroom.html', form=form)


@messages_blueprint.route('/chat')
@login_required
def chat():   
    name = session.get('name', '')
    chatroom = session.get('chatroom', '')
    if name == '' or chatroom == '':
        return redirect(url_for('users.login'))
    return render_template('chat.html', name=name, chatroom=chatroom)

@messages_blueprint.route('/history')
@login_required
def messages():
    name = session.get('name', '')
    chatroom = session.get('chatroom', '')   
    messages=MessageModel.find_by_name_id(session.get('id')) 
    messages=messages[0:49]   
    return render_template('messages.html', messages=messages, name=name, chatroom=chatroom)
