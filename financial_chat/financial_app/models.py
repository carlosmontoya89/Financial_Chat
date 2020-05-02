from flask_login import UserMixin
import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


class UserModel(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    messages = db.relationship(
        "MessageModel", lazy="dynamic", cascade="save-update, merge, delete"
    )

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "username": self.username,
            "created_at": self.created_at,
        }

    @property
    def password(self):
        raise AttributeError("`password` is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


class MessageModel(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    chatroom_id = db.Column(db.Integer, db.ForeignKey("chatrooms.id"))
    origin = db.relationship("UserModel")
    room = db.relationship("ChatRoomModel")

    def json(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "user_id": self.user_id,
            "origin": self.origin.username if self.origin else None,
            "room": self.room.name if self.room else None,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    class Meta:
        ordering = ["-created_at"]

    @classmethod
    def find_by_user_id_and_chat_room_id(cls, _user_id, _chatroom_id):
        return (
            cls.query.filter_by(user_id=_user_id, chatroom_id=_chatroom_id)
            .order_by(cls.created_at.desc())
            .limit(50)
            .all()
        )


class ChatRoomModel(db.Model):
    __tablename__ = "chatrooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    messages = db.relationship(
        "MessageModel", lazy="dynamic", cascade="save-update, merge, delete"
    )

    def json(self):
        return {
            "id": self.id,
            "name": self.content,
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
