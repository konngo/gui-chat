import json
import socket
import dbutil
import threading

class server():
    host:''
    port:''
    db:''
    list:[]

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
            # c.close()  # 关闭连接
            list.append(c)                      # 保存所有socket连接

    def deal_method(self,msg,c):                # 处理请求类型
        rest=json.loads(msg)
        method=rest['method']                   # 获取数据要处理的类型
        switch={
                 'login':self.login,
                 'send':self.recive
        }
        switch.get(method,self.default)(rest,c)       # 处理不同请求

    def login(self,rest,c):                     # 处理登录
        user=self.db.login(rest['username'],rest['password'])       # 查询数据库中是否有该用户
        print('数据库用户:',user)
        threading.local().user = user
        c.send(json.dumps({"method":"login","msg":user}).encode())       # 返回登录用户信息

    def recive(self,rest,c):                             # 接收消息
        msg=rest['msg']
        user=threading.local().user
        new_msg=user[1]+"说："+msg+"\n"
        # 拼接要发送的消息
        # 接收新消息后对所有已经连接的socket进行广播
        for c in self.list:
            c.send(json.dumps({"msg":new_msg}).encode())

    def default(self):
        print('method参数为空')


server()









