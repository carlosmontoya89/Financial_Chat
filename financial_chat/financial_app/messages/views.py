from flask import session, Blueprint, redirect, url_for, render_template, request, flash
from flask_login import current_user, login_user, login_required
from .forms import ChatRoomsForm
from flask_login import current_user

from financial_app.models import MessageModel
from financial_app.extensions import db

# from financial_app.commons.utils import login_required

messages_blueprint = Blueprint("messages", __name__, template_folder="templates")


@messages_blueprint.route("/chatroom", methods=["GET", "POST"])
@login_required
def chatroom():
    form = ChatRoomsForm()
    if form.validate_on_submit():
        session["chatroom"] = form.chatroom.data
        return redirect(url_for("messages.chat"))
    return render_template("chatroom.html", form=form)


@messages_blueprint.route("/chat")
@login_required
def chat():
    name = current_user.username
    print(name)
    chatroom = session.get("chatroom", "")
    if name == "" or chatroom == "":
        return redirect(url_for("users.login"))
    return render_template("chat.html", name=name, chatroom=chatroom)


@messages_blueprint.route("/messages")
@login_required
def messages():
    name = current_user.username
    chatroom = session.get("chatroom", "")
    messages = MessageModel.find_by_name_id(current_user.id)
    messages = messages[0:49]
    return render_template(
        "messages.html", messages=messages, name=name, chatroom=chatroom
    )
