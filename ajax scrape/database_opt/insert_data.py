import pymysql
import threading
from config import *


class DataManager():
    # 单例模式，确保每次实例化都调用一个对象。
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(DataManager, "_instance"):
            with DataManager._instance_lock:
                DataManager._instance = object.__new__(cls)
                return DataManager._instance

        return DataManager._instance

    def __init__(self, host, user, password, db, port=3306):
        # 建立连接
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=db
        )

        # 建立游标
        self.cursor = self.conn.cursor()

    def save_data(self, data):

        # (1)准备数据
        keys = ",".join(data.keys())
        values = ",".join(["%s"] * len(data))
        insert_data = tuple(data.values())
        # 数据库操作
        # (2)定义一个格式化的sql语句
        sql = 'insert into {table}({keys}) values({values})'.format(table=TABLE_NAME, keys=keys, values=values)
        # (3)操作
        try:
            self.cursor.execute(sql, insert_data)
            self.conn.commit()
        except Exception as e:
            print('插入数据失败', e)
            self.conn.rollback()  # 回滚

    def __del__(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()
