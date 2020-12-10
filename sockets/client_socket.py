import socket
import threading
from tkinter import *

# 客户端socket连接
class conn:

    def __init__(self):
        self.isConnect = False

    def connect(self):
        if not self.isConnect:
            self.tcpCliSock = socket.socket()
            self.tcpCliSock.connect((socket.gethostname(), 12345))
            self.isConnect = True
            print ("服务器连接成功")
        else:
            print ("已经连接，不再重新连接")

    def dis_connect(self):
        """断开服务器"""
        self.tcpCliSock.close()

    def showErr(self, info):
        """错误提示界面"""
        errTk = Tk()
        errTk.geometry('200x120')
        errTk.title("Error!")
        Label(errTk, text = info).pack(padx = 5, pady = 20, fill = 'x')
        bt = Button(errTk, text = "确定", command = errTk.destroy).pack()
        errTk.mainloop()


    def send(self,msg):                         #  发送消息到服务端
        print(msg)
        self.connect()
        self.tcpCliSock.send(msg.encode())                    # 发送消息
        recive=self.tcpCliSock.recv(1024).decode()
        return recive


