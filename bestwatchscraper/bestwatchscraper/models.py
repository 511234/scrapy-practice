from scrapy.utils.project import get_project_settings
from sqlalchemy import (
    Integer, String, Text)
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class WatchItemDB(DeclarativeBase):
    __tablename__ = "quote_table"

    id = Column(Integer, primary_key=True)
    quote = Column('quote', Text())
    author = Column('author', String(100))
