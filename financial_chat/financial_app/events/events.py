from flask import session
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
import datetime

from financial_app.extensions import socketio
from financial_app.models import UserModel, MessageModel


@socketio.on("joined", namespace="/chat")
def joined(message):
    if current_user.is_anonymous:
        return False
    chatroom = session.get("chatroom")
    join_room(chatroom)
    emit(
        "status",
        {"msg": "{user} joined the chatroom.".format(user=current_user.username)},
        chatroom=chatroom
    )


@socketio.on("text", namespace="/chat")
def text(message):
    chatroom = session.get("chatroom")
    emit(
        "message",
        {"msg": "{user}: {msg} --{datetime}".format(user= current_user.username,msg= message["msg"], datetime=datetime.datetime.now())},
        room=chatroom
    )
    user_id = current_user.id
    #created_at = datetime.datetime.now()
    content = message["msg"]
    msg = MessageModel(content=content, user_id=user_id)
    msg.save_to_db()


@socketio.on("left", namespace="/chat")
def left(message):
    chatroom = session.get("chatroom")
    leave_room(chatroom)
    emit(
        "status",
        {"msg": "{user} has left the room.".format(user=current_user.username)},
        room=chatroom
    )
