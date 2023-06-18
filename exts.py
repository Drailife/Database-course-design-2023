# 放置插件，防止循环引用
import pyodbc
import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

dic = {}

# 连接 MySQL 数据库
conn = pyodbc.connect('DSN=online_order_mysql')
# 创建游标对象
cursor = conn.cursor()
if __name__ == '__main__':
    # 执行 SQL 查询
    try:
        cursor.execute("select * from user where usr_id = 10000")
        # 获取查询结果
        rows = cursor.fetchall()
        print(rows)
        cursor.execute("CALL reset_password(1000, '123*&(7843)');")
        cursor.commit()
    except Exception as e:
        cursor.rollback()
        print(f'error{e}')
    # 遍历结果集
    # 关闭游标和连接
    cursor.close()
    conn.close()
