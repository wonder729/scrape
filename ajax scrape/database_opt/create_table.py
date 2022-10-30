import pymysql
from config import *


db = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "123456",
    port = 3306,
    db = DATABASE_NAME,
)
cursor = db.cursor()
sql = """
create table if not exists  {TABLE_NAME}
(id INT  UNSIGNED AUTO_INCREMENT,
name VARCHAR(255) NOT NULL,
alias VARCHAR(255) ,
cover VARCHAR(255) ,
categories VARCHAR(255) ,
score FLOAT ,
published_at DATE ,
drama TEXT ,
PRIMARY KEY (id))
""".format(TABLE_NAME=TABLE_NAME)

cursor.execute(sql)
db.close()