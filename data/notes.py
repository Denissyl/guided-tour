import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Note(SqlAlchemyBase, UserMixin):
    __tablename__ = 'note'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    note = sqlalchemy.Column(sqlalchemy.String)
    sight = sqlalchemy.Column(sqlalchemy.String)
    nickname = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    datetime = sqlalchemy.Column(sqlalchemy.String)
