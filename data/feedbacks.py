import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Feedback(SqlAlchemyBase, UserMixin):
    __tablename__ = 'feedback'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
