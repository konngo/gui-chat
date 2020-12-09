import json
import tkinter as tk
import threading

from sockets import client_socket

class views:
    window:''           # 窗口
    username:''         # 用户名
    password:''         # 密码
    def __init__(self):
        self.window = tk.Tk()
        self.draw()             # 绘制窗口
        self.window.mainloop()
    def draw(self):
        self.window.title("登录")
        self.window.geometry('600x400')
        self.window.resizable(0, 0)
        # 用户名、密码标签
        tk.Label(self.window, text='用户名: ').place(x=130, y=190)
        tk.Label(self.window, text='密码: ').place(x=130, y=230)
        # 用户名、密码输入框
        entry_usr_name=tk.StringVar()
        self.username = tk.Entry(self.window, textvariable=entry_usr_name)
        entry_usr_name.get()
        entry_usr_pwd=tk.StringVar()
        self.password = tk.Entry(self.window, textvariable=entry_usr_pwd, show='*')
        self.username.place(x=220, y=190)
        self.password.place(x=220, y=230)
        # 登录按钮
        btn_login = tk.Button(self.window, text='登录',command=self.login)
        btn_login.place(x=250, y=290)
    def login(self):        # 登录
        msg={'method':'login','username':self.username.get(),'password':self.password.get()}
        s=client_socket.client_socket()
        recive=s.send(json.dumps(msg))
        print(recive)
        if recive == 'null':
            threading.local().user=recive
            print("if")
        else:
            print("else")
            self.window.messagebox.showinfo('提示', '用户名密码错误，请重试')



