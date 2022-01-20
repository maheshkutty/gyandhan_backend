import pymysql
import config
from flask import g

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        db=config.MYSQL_DB
        )
        print("Connection established")
    return g.db
    
def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()    