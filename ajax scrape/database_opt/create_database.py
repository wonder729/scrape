import pymysql
from config import *

db = pymysql.connect(
    host = host,
    user = user,
    password = password,
    port = port,
)
cursor = db.cursor()
sql = """
create database {DATABASE_NAME} default character set utf8mb4
""".format(DATABASE_NAME=DATABASE_NAME)
cursor.execute(sql)
db.close()

