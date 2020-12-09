import json
import socket
import dbutil

class server():
    host:''
    port:''
    db:''

    def __init__(self):
        self.host = socket.gethostname()  # 获取本地主机名
        self.port = 12345  # 设置端口
        self.db = dbutil.db()
        #self.listener()             # 开启监听
        s = socket.socket()                     # 创建 sockets 对象
        s.bind((self.host, self.port))          # 绑定端口
        s.listen(5)                             # 等待客户端连接
        while True:
            c, addr = s.accept()                # 建立客户端连接
            print('连接地址：', addr)
            recive=c.recv(1024).decode()        # 获取请求数据
            self.deal_method(recive,c)
            print(recive)
            c.close()  # 关闭连接


    def deal_method(self,msg,c):                # 处理请求类型
        rest=json.loads(msg)
        method=rest['method']                   # 获取数据要处理的类型
        switch={
                 'login':self.login,
        }
        switch.get(method,self.default)(rest,c)       # 处理不同请求

    def login(self,rest,c):                     # 处理登录
        user=self.db.login(rest['username'],rest['password'])       # 查询数据库中是否有该用户
        print('数据库用户:',user)
        c.send(json.dumps(user).encode())       # 返回登录用户信息

    def default(self):
        print('method参数为空')


server()









