from flask import session
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
import datetime

from financial_app.extensions import socketio
from financial_app.models import MessageModel
from financial_app.commons.utils import socket_authenticated_required


@socketio.on("joined", namespace="/chat")
@socket_authenticated_required
def joined(message):
    if current_user.is_anonymous:
        return False
    chatroom = session.get("chatroom")
    join_room(chatroom)
    emit(
        "status",
        {"msg": "{user} joined the chatroom.".format(user=current_user.username)},
        room=chatroom,
    )


@socketio.on("text", namespace="/chat")
@socket_authenticated_required
def text(message):
    chatroom = session.get("chatroom")
    chatroom_id = session.get("chatroom_id")
    emit(
        "message",
        {
            "msg": "{user}: {msg} --{datetime}".format(
                user=current_user.username,
                msg=message["msg"],
                datetime=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            )
        },
        room=chatroom,
    )
    user_id = current_user.id
    content = message["msg"]
    msg = MessageModel(content=content, user_id=user_id, chatroom_id=chatroom_id)
    msg.save_to_db()


@socketio.on("left", namespace="/chat")
@socket_authenticated_required
def left(message):
    chatroom = session.get("chatroom")
    leave_room(chatroom)
    emit(
        "status",
        {"msg": "{user} has left the room.".format(user=current_user.username)},
        room=chatroom,
    )
