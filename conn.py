import pymysql


def conn_db():
    db = pymysql.connect("localhost","root","admin","LIKES")
    return db


class dbconn():
    def __init__(self):
        self.db = conn_db()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()