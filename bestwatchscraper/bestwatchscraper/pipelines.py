import json
from bestwatchscraper.models import WatchItemDB
from bestwatchscraper.models import db_connect, create_table

import psycopg2
from sqlalchemy.orm import sessionmaker
from scrapy.utils.serialize import ScrapyJSONEncoder

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

        self.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS bestwatch_products(
            id SERIAL PRIMARY KEY, 
            sku VARCHAR(255) UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS bestwatch_product_details(
            id SERIAL PRIMARY KEY,
            product_id INTEGER UNIQUE,
            url TEXT,
            title VARCHAR(255),
            currency VARCHAR(3),
            price NUMERIC(15,2),
            watch_spec JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_product_id
                FOREIGN KEY(product_id)
                REFERENCES bestwatch_products(id)
                ON DELETE CASCADE
        )
        """)

        self.cur.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at()
            RETURNS TRIGGER AS $$
            BEGIN
            NEW.updated_at = now();
            RETURN NEW;
            END;
            $$ language 'plpgsql'
        """)

        self.cur.execute("""
            CREATE TRIGGER update_bw_details_updated_at
            BEFORE UPDATE ON bestwatch_product_details
            FOR EACH ROW
            EXECUTE PROCEDURE update_updated_at()
        """)


    def process_item(self, item, spider):
        self.cur.execute("""
        INSERT INTO bestwatch_products (sku)
        VALUES (%s)
        ON CONFLICT (sku) DO NOTHING
        RETURNING id
        """, (
            item["sku"],
        ))

        last_id = self.cur.fetchone()[0]

        self.cur.execute("""
        INSERT INTO bestwatch_product_details (product_id, price, url, title, currency, watch_spec)
        VALUES (%s,%s,%s,%s,%s,%s)
        ON CONFLICT (product_id) DO UPDATE
            SET price = EXCLUDED.price,
                url = EXCLUDED.url,
                title = EXCLUDED.title,
                currency = EXCLUDED.currency,
                watch_spec = EXCLUDED.watch_spec
        """, (
            last_id,
            float(item["price"]),
            item["url"],
            item["title"],
            item["currency"],
            self._encoder.encode(item['watch_spec'])
        ))

        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
