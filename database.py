from flask_sqlalchemy import SQLAlchemy
from os import getenv

class Database():
  def __init__(self, app):
      self.db = SQLAlchemy(app)

  def get_db(self):
    return self.db