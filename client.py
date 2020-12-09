import socket
from view import login_view


class client():

    def __init__(self):
        print('客户端启动中....')
        # 启动登录界面
        login_view.views()


client()