from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
import datetime
from financial_app.models import UserModel, Message


@socketio.on('joined', namespace='/chat')
def joined(message):    
    chatroom = session.get('chatroom')
    join_room(chatroom)
    emit('status', {'msg': session.get('name') + ' joined the chatroom.'}, chatroom=chatroom)


@socketio.on('text', namespace='/chat')
def text(message):   
    chatroom = session.get('chatroom')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, chatroom=chatroom)
    name_id=session.get('id')
    created_at = datetime.datetime.now()
    content=message['msg']
    msg=Message(content, created_at, name_id)
    msg.save_to_db()

@socketio.on('left', namespace='/chat')
def left(message):    
    chatroom = session.get('chatroom')
    leave_room(chatroom)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, chatroom=chatroom)

