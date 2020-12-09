import socket

# 客户端socket连接
class client_socket:
    host:''   # 本地主机名
    port:''                  # 端口号

    def __init__(self):
        print('客户端socket启动')
        self.host=socket.gethostname()
        self.port=12345

    def send(self,msg):                         #  发送消息到服务端
        s = socket.socket()                     # 创建 sockets 对象
        s.connect((self.host, self.port))       # socker连接
        s.send(msg.encode())                    # 发送消息
        recive=s.recv(1024).decode()            # 接收返回消息
        s.close()                               # 关闭socket
        return recive
