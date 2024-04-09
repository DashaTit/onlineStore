import sqlalchemy
from .db_session import SqlAlchemyBase

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                            primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, 
                                index=True, unique=True, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, 
                                index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    checkbox = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)