import json
from tkinter import *
import threading
import tkinter.messagebox as messagebox
from tkinter.font import Font
from tkinter import *
from sockets import client_socket
from sockets import client_socket

class views(object):
    window:''           # 窗口
    page:''             # Frame
    content:''          # 消息框
    send:''             # 发送框

    def __init__(self,master=None,socket=None):
        self.window = master
        self.socket=socket
        self.window.title("聊天窗口")
        self.window.geometry('%dx%d' % (600, 400))
        self.draw()             # 绘制窗口
        self.listenThread = self.listen_thread(self.socket, self)
        self.listenThread.start()

    class listen_thread(threading.Thread):
        """Socket监听线程，对收到的信息作出相应反馈"""
        def __init__(self,socket,master):
            threading.Thread.__init__(self)
            self.master = master
            self.socket = socket

        def run(self):
            print("开启监听服务器信息")
            msg={'method':'send','msg':'已经连接到服务器'}
            msg = json.dumps(msg)
            self.socket.tcpCliSock.send(msg.encode())
            while True:
                recive = self.socket.tcpCliSock.recv(1024).decode()
                if recive is None: continue
                data = json.loads(recive)
                print("接收消息:",recive)
                if data['method'] == 'recive':
                    self.master.content.insert(END, data['msg'])
                    # 消息框到最下
                    self.master.content.see(END)
            self.socket.dis_connect()




    def draw(self):
        self.page = Frame(self.window)  # 创建Frame
        self.page.pack()
        # 消息显示框
        sc=Scrollbar(self.page, orient=VERTICAL)
        self.content=Text(self.page,height =15)
        sc.grid(row=0, column=1, sticky=S + W + E + N)
        self.content.grid(row=0, column=0, sticky=W)
        # 绑定滚动块
        self.content.config(yscrollcommand = sc.set)
        sc['command'] = self.content.yview()
        # 消息框插入
        # self.content.insert(END,'晴明落地犹惆怅8，何况飘零泥土中。:\n\n')

        self.send=Text(self.page,height =7)
        self.send.grid(row=1, column=0)
        Button(self.page, text='发送', command=self.sendMsg).grid(row=2,column=0)


    def sendMsg(self):
        # self.socket = client_socket.conn()
        msg = {'method': 'send', 'msg': self.send.get('1.0', END)}
        msg = json.dumps(msg)
        print("发送消息：" + msg)
        self.socket.tcpCliSock.send(msg.encode())
        self.send.delete('1.0', 'end')