import socket
import time
import threading
import codecs
import json
import struct
import os
import data as Da
import change_data as Cd
import re
from flask import Flask,render_template,jsonify
from threading import Thread

data1 = []
blocknum = []
Bnum = 0
path = r"blocknum.txt"
path1 = r"node.txt"
try:
    data = Cd.change_msg(path1)
    blocknum1 = Da.change_msg(path)
except IOError:
    print("Error:没有发现相应文件")
else:
    print("读取数据成功")

class Server():
    def __init__(self):
        self.g_conn_pool = {}  # 连接池
        # 记录客户端数量
        self.num =0
        # 服务器本地地址
        self.address = ('0.0.0.0', 6060)
        self.g_socket_server = None
        self.g_conn_pool = []
        # 初始化服务器
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.address)
        self.server_socket.listen(128)



    def accept_client(self):
        """
            接收新连接
            """
        while True:
            client_socket, info = self.server_socket.accept()  # 阻塞，等待客户端连接
            print(client_socket,port)
            # 给每个客户端创建一个独立的线程进行管理
            thread = threading.Thread(target=self.recv_msg, args=(client_socket,info))
            thread.setDaemon(True)
            thread.start()

    def recv_msg(self,client,info):
        # 提示服务器开启成功
        print('服务器已准备就绪！')
        client.sendall("connect server successfully!".encode(encoding='utf8'))


        # 持续接受客户端连接
        while True:
            try:
                # self.client_socket, connect_address = self.server_socket.accept()
                obj = client.recv(4)
                header_size = struct.unpack('i', obj)[0]
                header_bytes = client.recv(header_size)
                header_json = header_bytes.decode('utf-8')
                header_dic = json.loads(header_json)
                first_num = header_dic['filename']
                # path = r'C:\Users\cao\Desktop\runoob01\blockchain\%s' % (path1)
                print(first_num)
                # 写入区块总数
                global blocknum1
                blocknum1 = Da.put_fnum(blocknum1,int(first_num))

                client.send(b'Success')
                while True:

                    msg = client.recv(1024)
                    msg_recv = msg.decode('utf-8')
                    data_msg = Da.pd(msg_recv)
                    # print(msg_recv)
                    # msg_recv_dic = json.loads(msg_recv)
                    # print(msg_recv)
                    # msg_name = msg_recv_dic['name']
                    # 判断是否为区块数据
                    value = re.compile(r'^[0-9]+$')
                    result = value.match(data_msg[0]['name'])

                    if not msg_recv:
                        continue
                    elif result:
                        global blocknum,Bnum
                        blocknum = Da.change_msg1(msg_recv)
                        # print(blocknum)
                        blocknum1 = Da.put_nownum(blocknum1,blocknum)
                        # print(blocknum1)
                        Bnum = Bnum + 1
                    else:
                        #将传输过来的数据转换格式
                        da = Cd.change_msg1(msg_recv)
                        global data,data1
                        data = Cd.pd(data, da)
                        # data1 = Cd.input_data(data)
                        # with open(path1,'ab') as f:
                        #     # data = self.client_socket.recv(1024)
                        #     f.write(msg)
                        recv_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        print('客户端 ' + recv_time + ':\n')
                        print(' ' + msg_recv + '\n')
            except Exception as e:

                print('客户端断开连接...')
                exit(-1)
                break

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

#实例化一个Flask节点
app = Flask(__name__)



@app.route('/map',methods=["post","get"])
def showmap():
    global data1,data,path1
    data1 = Cd.input_data(data)
    data = Cd.change_msg(path1)
    return render_template('ss.html',result_data=data1)

@app.route('/')
def hello():
    return render_template("/visualserver/地图.html")

# 用来记录每小时出块数量
@app.route('/blocknum',methods=["post","get"])
def showblocknum():

    return render_template("num.html",block_num=blocknum1)

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=3000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    py_server = Server()

    py_server.start_new_thread()
    app.run(host='0.0.0.0',port=port)

