import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase, UserMixin):
    __tablename__ = 'comment'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    nickname = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    mark = sqlalchemy.Column(sqlalchemy.Integer)
