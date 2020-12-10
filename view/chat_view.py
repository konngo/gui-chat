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
        # 开启线程
        self.listenThread = self.listen_thread(self.socket, self)

    class listen_thread(threading.Thread):
        """Socket监听线程，对收到的信息作出相应反馈"""
        def __init__(self,socket,master):
            threading.Thread.__init__(self)
            self.master = master
            self.socket = socket

        def run(self):
            while True:
                try:
                    jData = self.socket.recv(1024)
                    data = json.loads(jData)
                except:
                    break
                print ("__receive__" + jData)

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

        self.content.insert(END,'晴明落地犹惆怅8，何况飘零泥土中。:\n\n')

        self.send=Text(self.page,height =7)
        self.send.grid(row=1, column=0)
        Button(self.page, text='发送', command=self.sendMsg).grid(row=2,column=0)

    def sendMsg(self):
        msg = {'method': 'send', 'msg':self.send.get('1.0',END)}
        self.socket.tcpCliSock.send(json.dumps(msg).encode())
        self.send.setvar("")
        # 消息框到最下
        # self.content.see(END)