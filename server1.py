import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox
import sys
import socket
import time
import threading
import json
from threading import Thread

class Server():
    def __init__(self):
        self.server_window = tk.Tk()
        self.font_style = tkfont.Font(family='Microsoft YaHei UI', size=13)
        self.g_conn_pool = {}  # 连接池
        # 记录客户端数量
        self.num =0
        # 服务器本地地址
        self.address = ('127.0.0.1', 8000)
        self.g_socket_server = None
        self.g_conn_pool = []
        # 初始化服务器
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.address)
        self.server_socket.listen(128)


    def init_window(self):
        """初始化客户端窗口"""
        self.server_window.title("Python  Server")

        # 设置窗口大小为480x520px
        self.server_window.geometry('480x520')
        # 接收消息的listbox框
        self.output_frame = tk.Listbox(self.server_window, font=('',9))
        self.output_frame.place(x=10, y=10,relwidth=1,relheight=0.7, anchor='nw')
        # 滚动条
        self.sc = tk.Scrollbar(self.output_frame,command=self.output_frame.yview)
        self.sc.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_frame.config(yscrollcommand=self.sc.set)

        # 关闭按钮
        self.close_button = tk.Button(self.server_window, text='关闭', font=self.font_style,
                                      width=8, command=self.close_window)
        self.close_button.place(x=50, y=475, anchor='nw')


    def close_window(self):
        """关闭窗口"""
        sys.exit()

    def accept_client(self):
        """
            接收新连接
            """
        while True:
            self.client_socket, info = self.server_socket.accept()  # 阻塞，等待客户端连接
            # 给每个客户端创建一个独立的线程进行管理
            thread = threading.Thread(target=self.recv_msg, args=(self.client_socket,info))
            thread.setDaemon(True)
            thread.start()

    def recv_msg(self,client,info):
        # 提示服务器开启成功
        self.output_frame.insert(tk.END, '服务器已准备就绪！')
        client.sendall("connect server successfully!".encode(encoding='utf8'))
        # 持续接受客户端连接
        while True:
            try:
                # self.client_socket, connect_address = self.server_socket.accept()
                while True:
                    msg_recv = self.client_socket.recv(1024).decode('gbk')
                    if not msg_recv:
                        continue
                    elif msg_recv == 'Success':
                        self.output_frame.insert(tk.END, '服务器与客户端成功建立连接...')
                        self.client_socket.send(b'Success')
                    else:
                        recv_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        self.output_frame.insert(tk.END, '客户端 ' + recv_time + ':\n')
                        self.output_frame.insert(tk.END, ' ' + msg_recv + '\n')
            except:
                self.output_frame.insert(tk.END, '客户端断开连接...')
                break;

    def remove_client(self,client_type):
        client = self.g_conn_pool[client_type]
        if None != client:
            client.close()
            self.g_conn_pool.pop(client_type)
            print("client offline: " + client_type)

    def start_new_thread(self):
        """启动新线程来接收信息"""
        thread = threading.Thread(target=self.accept_client, args=())
        thread.setDaemon(True)
        thread.start()

def main():
    py_server = Server()
    py_server.init_window()
    py_server.start_new_thread()
    py_server.server_window.mainloop()


if __name__ == '__main__':
    main()