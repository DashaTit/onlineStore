import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Shop(SqlAlchemyBase):
    __tablename__ = 'shop_list'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                            primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')

    def __repr__(self):
        return "<id={}, email={}, content={}>".format(self.id, self.email, self.content)