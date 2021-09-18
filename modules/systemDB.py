import sqlite3


class DB:
    def __init__(self, db):
        self.db = db

    def create_tb(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def open_db(self):
        self.conn = sqlite3.connect(self.db)
        self.cur = self.conn.cursor()

    def close_db(self):
        self.conn.close()

    def fetch_data(self, query):
        self.cur.execute(query)
        data = self.cur.fetchall()
        return data

    def print_data(self, query):
        self.cur.execute(query)
        records = self.cur.fetchall()
        print("DATA: ", records)

    def has_values(self, query):
        self.cur.execute(query)
        records = self.cur.fetchall()
        if len(records) > 0:
            return True
        else:
            return False

    def insert_data(self, query, data):
        self.cur.execute(query, data)
        self.conn.commit()

    def update_data(self, query, data):
        self.cur.execute(query, data)
        self.conn.commit()
