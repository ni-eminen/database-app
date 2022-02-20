from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
import uuid

class User(UserMixin):
  def __init__(self, username):
    self.username = username
    self.id = uuid.getnode()

  @staticmethod
  def get(user_id):
    # get user from database
    print(user_id)
    user = User('test')
    return user

  def get_id(self):
    return f'{self.id}'