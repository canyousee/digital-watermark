
# -*- coding: UTF-8 -*-
from flask_login import UserMixin
import enum
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from extentions import db
from extentions import bcrypt
#class UserRole(enum.Enum):
 #   ADMIN = 'Administrator'
  #  USERS = 'Normal users'


# user models
class User(db.Model, UserMixin):
    __tablename__ = "users"
    __table_args__ = {"useexisting": True, 'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100),unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    _password = db.Column(db.String(512), nullable=False)
    
    def verify_password(self, _password):
       return self._password == _password
    # @hybrid_property
    # def password(self):
    #     return self._password

    # @password.setter
    # def _set_password(self, plaintext):
    #     self._password = bcrypt.generate_password_hash(plaintext)

    # def is_correct_password(self, plaintext):
    #     return bcrypt.check_password_hash(self._password, plaintext)
    
    def __repr__(self):
           return "<User %r>" % self.username
# user models
