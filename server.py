import json
import socket
import subprocess
import sys

import dbutil
import threading
from select import select

class server():
    host:''
    port:''
    list:[]

    def __init__(self):
        self.host = socket.gethostname()        # 获取本地主机名
        self.port = 12345                       # 设置端口

        #self.listener()                        # 开启监听
        s = socket.socket()                     # 创建 sockets 对象
        s.bind((self.host, self.port))          # 绑定端口
        s.listen(5)                             # 等待客户端连接
        self.list=[]
        while True:
            c, addr = s.accept()                # 建立客户端连接
            self.list.append(c)  # 保存所有socket连接
            self.listenThread = self.listen_thread(c, self)
            self.listenThread.start()

    class listen_thread(threading.Thread):
        """Socket监听线程，对收到的信息作出相应反馈"""
        local: ''
        def __init__(self,c,master):
            self.local = threading.local()
            self.db = dbutil.db()
            threading.Thread.__init__(self)
            self.c = c
            self.master = master

        def run(self):
            while True:
                cmd = self.c.recv(1024)
                recive = cmd.decode()  # 获取请求数据
                print(recive)
                self.deal_method(recive, self.c)


        def deal_method(self,msg,c):                # 处理请求类型
            rest=json.loads(msg)
            method=rest['method']                   # 获取数据要处理的类型
            switch={
                    'login':self.login,
                    'send':self.recive,
                    'reg':self.reg
            }
            switch.get(method,self.default)(rest,c) # 处理不同请求

        def reg(self,rest,c):                     # 处理注册
            user=self.db.reg(rest['username'],rest['password'])       # 添加用户信息到数据库
            self.local.val = user
            c.send(json.dumps({"method":"reg","msg":user}).encode())       # 返回用户信息

        def login(self,rest,c):                     # 处理登录
            user=self.db.login(rest['username'],rest['password'])       # 查询数据库中是否有该用户
            self.local.val = user
            c.send(json.dumps({"method":"login","msg":user}).encode())       # 返回登录用户信息

        def recive(self,rest,c):                    # 接收消息
            msg=rest['msg']
            new_msg=self.local.val[1]+"说："+msg+"\n"
            # 拼接要发送的消息
            # 接收新消息后对所有已经连接的socket进行广播
            jdata=json.dumps({"method": "recive", "msg": new_msg})
            for m in self.master.list:
                m.send(jdata.encode())

        def default(self):
            print('method参数为空')


server()









