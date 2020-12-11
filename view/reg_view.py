import json
from tkinter import *
import threading
import tkinter.messagebox as messagebox
from view import chat_view, login_view


class views(object):
    window:''           # 窗口
    username:''         # 用户名
    password:''         # 密码
    page:''
    def __init__(self,master=None,socket=None):
        self.socket=socket
        self.window = master
        self.window.title("注册")
        self.username = StringVar()
        self.password = StringVar()
        self.window.geometry('%dx%d' % (300, 180))
        self.draw()             # 绘制窗口

    def draw(self):
        self.page = Frame(self.window)  # 创建Frame
        self.page.pack()
        # 用户名标签、输入框
        Label(self.page, text='用户名: ').grid(row=1,stick=W,pady=10)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)
        # 密码标签、输入框
        Label(self.page, text='密码: ').grid(row=2,stick=W,pady=10)
        Entry(self.page, textvariable=self.password,show='*').grid(row=2, column=1, stick=E)
        # 按钮
        Button(self.page, text='注册', command=self.reg).grid(row=3,column=2, stick=E, pady=10)
        Button(self.page, text='去登录', command=self.login).grid(row=3,column=1, stick=E, pady=10)

    def login(self):          # 注册
        self.page.destroy()     # 清空当前页面
        login_view.views(self.window, self.socket)

    def reg(self):        # 注册
        msg={'method':'reg','username':self.username.get(),'password':self.password.get()}
        msg=json.dumps(msg)
        self.socket.tcpCliSock.send(msg.encode())
        recive=self.socket.tcpCliSock.recv(1024).decode()
        print(recive)
        arr=json.loads(recive)
        if arr['msg'] == None:
            messagebox.showinfo('提示', '注册失败，请重试')
        else:
            print("注册成功！")
            messagebox.showinfo('提示', '注册成功，请登录')
            # threading.local().user=arr
            self.page.destroy()
            login_view.views(self.window,self.socket)


