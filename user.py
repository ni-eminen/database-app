"""Module for a user that is used to maintain a \
  session using flask-login"""
import os
from flask_login import UserMixin
from sqlalchemy import create_engine

# print(os.environ)
engine = create_engine(os.getenv("DATABASE_URL"))


class User(UserMixin):
    """The user class, extends UserMixin from flask-login"""

    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id

    @staticmethod
    def get(user_id):
        """Gets a user via id"""
        # get user from database
        db_user = engine.execute(
            f"SELECT * FROM users WHERE id='{user_id}'").fetchone()
        if not db_user:
            return None
        user = User(db_user[1], db_user[0])
        return user

    def get_id(self):
        """Gets this user objects id"""
        # id = engine.execute(f"SELECT id FROM users WHERE
        # username='{self.username}';").fetchone()[0]
        return self.user_id

    def to_string(self):
        """Returns this user in string format"""
        return f'username: {self.username}'
