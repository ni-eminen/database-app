from flask_login import UserMixin, LoginManager
from os import getenv
from sqlalchemy import create_engine
engine = create_engine(getenv("DATABASE_URL"))

class User(UserMixin):
  def __init__(self, username, id):
    self.username = username
    self.id = id

    id = engine.execute(f"SELECT id FROM users WHERE username='root';").fetchone()[0]

    print("\n\n\n\n\n\n\n", id, "\n\n\n\n\n\n\n")


  @staticmethod
  def get(user_id):
    # get user from database
    print('reload user id\n\n\n\n', user_id)
    db_user = engine.execute(f"SELECT * FROM users WHERE id='{user_id}'").fetchone()
    user = User(db_user[1], db_user[0])
    return user

  def get_id(self):
    # id = engine.execute(f"SELECT id FROM users WHERE username='{self.username}';").fetchone()[0]
    return self.id

  def to_string(self):
    return f'username: {self.username}'