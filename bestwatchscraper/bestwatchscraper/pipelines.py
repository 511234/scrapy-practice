# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from bestwatchspider.models import db_connect, create_table
# useful for handling different item types with a single interface
from sqlalchemy.orm import sessionmaker

from bestwatchscraper.bestwatchscraper.models import WatchItemDB


class BestwatchscraperPipeline:

    def __init__(self):
        # ## Connection Details
        # hostname = 'localhost'
        # username = 'user'
        # password = 'password'
        # database = 'pgdb'
        #
        # ## Create/Connect to database
        # self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        #
        # ## Create cursor, used to execute commands
        # self.cur = self.connection.cursor()
        #
        # ## Create quotes table if none exists
        # self.cur.execute("""
        # CREATE TABLE IF NOT EXISTS bestwatch(
        #     id serial PRIMARY KEY,
        #     url VARCHAR(255),
        #     title VARCHAR(255),
        #     sku VARCHAR(255),
        #     currency VARCHAR(5),
        #     price DECIMAL,
        #     watch_spec VARCHAR(255)
        # )
        # """)

        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.
        """

        session = self.Session()
        instance = session.query(WatchItemDB).filter_by(**item).one_or_none()
        if instance:
            return instance
        watch_item_db = WatchItemDB(**item)

        try:
            session.add(watch_item_db)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item
