import socket
import threading
from sockets import client_socket

from view import login_view
import tkinter as tk

class client():

    def __init__(self):
        print('客户端启动中....')
        # 启动登录界面
        root= tk.Tk()
        root.title('chat')
        self.socket=client_socket.conn()
        login_view.views(root,self.socket)
        root.mainloop()

threading.local().msg = []
client()