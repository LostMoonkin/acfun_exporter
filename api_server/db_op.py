import datetime
import sqlite3
import traceback


class SqliteOp():

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cur = None
        self.connected = 0
        self._connect()

    def _connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cur = self.conn.cursor()
            self.connected = 1
        except:
            self.connected = 0
            traceback.print_exc()

    @property
    def is_connected(self):
        return self.connected != 0

    def _check_alive(self):
        if not self.is_connected:
            self._connect()
        if not self.is_connected:
            raise "Can't connect to sqlite3"

    def query(self, sql, warning=1):
        self._check_alive()
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            cur.close()
        except:
            if warning:
                traceback.print_exc()
            return None
        return res

    def is_table_exists(self, table_name):
        self._check_alive()
        query_sql = "SELECT COUNT(*) FROM sqlite_master where type='table' and name='{0}'".format(table_name)
        try:
            cur = self.conn.cursor()
            cur.execute(query_sql)
            res = cur.fetchall()[0][0]
            cur.close()
            if res > 0:
                return True
        except:
            traceback.print_exc()
            return False

    def get_articles(self, date):
        if not self.is_table_exists(date):
            return None
        try:
            cur = self.conn.cursor()
            query_sql = "SELECT * FROM '{0}'".format(date)
            cur.execute(query_sql)
            res = cur.fetchall()
            return res
        except:
            return None

    def get_latest_articles(self):
        date = datetime.datetime.now().strftime('%Y_%m_%d')
        return self.get_articles(date)

    def close(self):
        if self.connected == 0:
            return
        try:
            self.cur.close()
            self.conn.close()
            self.connected = 0
        except:
            pass

    def __del__(self):
        self.close()
