# 连接数据库

import MySQLdb


def connect_db(db_name):
    db = MySQLdb.Connect('localhost', 'root', '', db_name, charset='utf8')
    cursor = db.cursor()
    return db, cursor
