from flask import session, Blueprint, redirect, url_for, render_template, request, flash
from flask_login import current_user, login_required


from financial_app.models import ChatRoomModel
from financial_app.models import MessageModel
from .forms import ChatRoomsForm


messages_blueprint = Blueprint("messages", __name__, template_folder="templates")


@messages_blueprint.route("/chatroom", methods=["GET", "POST"])
@login_required
def chatroom():
    form = ChatRoomsForm()
    if request.method == "POST":
        if form.validate_on_submit():
            room_name = form.chatroom.data
            chatroom = ChatRoomModel.find_by_name(room_name)
            if not chatroom:
                chatroom = ChatRoomModel(name=room_name)
                chatroom.save_to_db()
            session["chatroom_id"] = chatroom.id
            session["chatroom"] = room_name
            return redirect(url_for("messages.chat"))
    return render_template("chatroom.html", form=form)


@messages_blueprint.route("/chat")
@login_required
def chat():
    name = current_user.username
    chatroom = session.get("chatroom", "")
    return render_template("chat.html", name=name, chatroom=chatroom)


@messages_blueprint.route("/messages")
@login_required
def messages():
    name = current_user.username
    chatroom_id = session.get("chatroom_id", "")
    chatroom = session.get("chatroom")
    messages = MessageModel.find_by_user_id_and_chat_room_id(
        current_user.id, chatroom_id
    )
    return render_template(
        "messages.html", messages=messages, name=name, chatroom=chatroom
    )
