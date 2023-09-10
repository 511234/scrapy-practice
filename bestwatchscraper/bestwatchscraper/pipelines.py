import json
from bestwatchscraper.models import WatchItemDB
from bestwatchscraper.models import db_connect, create_table

import psycopg2
from sqlalchemy.orm import sessionmaker
from scrapy.utils.serialize import ScrapyJSONEncoder

class BestwatchscraperPipeline:

    def __init__(self):

        # self._encoder = ScrapyJSONEncoder()
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
            print('------ instance ------')
            print(instance)
            return instance
        else:
            print('********* we are in else ********')


        watch_item_db = WatchItemDB(
            url=item['url'],
            title=item['title'],
            sku=item['sku'],
            currency=item['currency'],
            price=item['price'],
            watch_spec=self._encoder.encode(item['watch_spec'])
        )

        try:
            session.add(watch_item_db)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item

class SaveIntoPostgresPipeline:

    def __init__(self):

        host = 'localhost'
        user = 'user'
        password = 'password'
        dbname = 'pgdb'
        port = '23910'

        self._encoder = ScrapyJSONEncoder()
        self.connection = psycopg2.connect(host=host, user=user, password=password, dbname=dbname, port=port)
        self.cur = self.connection.cursor()

        ## Create quotes table if none exists

        # self.cur.execute("""
        # BEGIN;
        #
        # DO $$
        # BEGIN
        #     IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'task_status') THEN
        #         create type task_status AS ENUM ('todo', 'doing', 'blocked', 'done');
        #     END IF;
        # END
        # $$;
        # """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS bestwatch(
            id serial PRIMARY KEY, 
            url TEXT,
            title TEXT,
            sku TEXT,
            currency VARCHAR(3),
            price FLOAT,
            watch_spec JSONB
        )
        """)



    def process_item(self, item, spider):
        self.cur.execute("""
        INSERT INTO bestwatch (url, title, sku, currency, price, watch_spec)
        VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            item["url"],
            item["title"],
            item["sku"],
            item["currency"],
            float(item["price"]),
            self._encoder.encode(item['watch_spec'])
        ))

        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
