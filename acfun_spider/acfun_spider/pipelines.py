# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import json


class Sqlite3Pipeline(object):

    def __init__(self, db_file, db_table):
        self.db_file = db_file
        self.db_table = db_table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_file=crawler.settings.get('DB_FILE'),
            db_table=crawler.settings.get('DB_TABLE')
        )

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.db_file)
        self.cur = self.conn.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS '{0}' (TITLE TEXT, URL TEXT, TYPE TEXT, INFO TEXT)"
                         .format(self.db_table))
        self.conn.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):

        title, url, type = item['title'], item['url'], item['type']
        info = json.dumps(item['info'])

        select_sql = "SELECT * FROM '{0}' WHERE TITLE = '{1}'".format(self.db_table, title)
        self.cur.execute(select_sql)
        res = self.cur.fetchall()
        if len(res) > 0:
            update_sql = "UPDATE '{0}' SET INFO = '{1}' WHERE TITLE = '{2}'".format(
                self.db_table, info, title
            )
            self.cur.execute(update_sql)
        else:
            insert_sql = "INSERT INTO '{0}' (TITLE, URL, TYPE, INFO) VALUES ('{1}', '{2}', '{3}', '{4}')"\
                .format(self.db_table, title, url, type, info)
            self.cur.execute(insert_sql)

        self.conn.commit()
        return item



