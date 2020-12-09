import sqlite3

class db:
    cursor:''   # 游标
    conn:''     # 数据库连接

    def __init__(self):
        self.conn = sqlite3.connect("chat.db")
        self.cursor = self.conn.cursor()
        # 如果不存在用户表则创建用户表
        sql = "create table if not exists users (id integer primary key autoincrement,username varchar(30),password varchar(30))"
        self.cursor.execute(sql)        # 执行sql语句

    def login(self,username,password):  # 登录
        sql = "select * from users where username='"+username+"' and password='"+password+"'"
        self.cursor.execute(sql)        # 执行sql语句
        results=self.cursor.fetchone()
        return results

    def reg(self,username,password):    # 注册
        sql = "insert into users (username,password) values('"+username+"','"+password+"')"
        try:
            self.cursor.execute(sql)    # 执行sql语句
            self.conn.commit()          # 没有问题执行提交
        except:
            self.conn.rollback()        # 发生问题回滚数据库
        return self.cursor.rowcount     # 返回受影响的行数