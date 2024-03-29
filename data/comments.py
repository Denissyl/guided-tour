import sqlalchemy

from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = 'comment'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    sight = sqlalchemy.Column(sqlalchemy.String)
    nickname = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    mark = sqlalchemy.Column(sqlalchemy.Integer)
    datetime = sqlalchemy.Column(sqlalchemy.String)
