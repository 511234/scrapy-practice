# import datetime
# from scrapy.utils.project import get_project_settings
# from sqlalchemy import (
#     Integer, Text, Float, JSON, DateTime, ForeignKey)
# from sqlalchemy import create_engine, Column
# from sqlalchemy.ext.declarative import declarative_base
#
# DeclarativeBase = declarative_base()
#
# def db_connect():
#     """
#     Performs database connection using database settings from settings.py.
#     Returns sqlalchemy engine instance
#     """
#     return create_engine(get_project_settings().get("CONNECTION_STRING"))
#
#
# def create_table(engine):
#     DeclarativeBase.metadata.create_all(engine)
#
#
# class WatchItemDB(DeclarativeBase):
#     __tablename__ = "bestwatch_products"
#
#     id = Column(Integer, primary_key=True)
#     sku = Column('sku', Text())
#     created_at = Column('created_at', DateTime(), default=datetime.datetime.utcnow)
#
# class WatchDynamicItemDB(DeclarativeBase):
#     __tablename__ = "bestwatch_product_details"
#
#     id = Column(Integer, primary_key=True)
#     product_id = Column(Integer, ForeignKey("bestwatch_products"), nullable=False)
#     url = Column('url', Text())
#     title = Column('title', Text())
#     currency = Column('currency', Text())
#     price = Column('price', Float())
#     watch_spec = Column('watch_spec', JSON())
#     created_at = Column('created_at', DateTime(), default=datetime.datetime.utcnow)
#     updated_at = Column('updated_at', DateTime())
#
