from .extensions import db
import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class UserModel(db.Model):
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
            "created_at": self.created_at
        }

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


class MessageModel(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    origin = db.relationship("UserModel")

    def json(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at,
            "user_id": self.user_id,
            "origin": self.origin.username if self.origin else None,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    class Meta:
        ordering = ["-created_at"]

    @classmethod
    def find_by_name_id(cls, _name_id):
        return cls.query.filter_by(name_id=_name_id).all()
