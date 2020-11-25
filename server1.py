import socket
import time
import threading
import codecs
import json
import struct
import os
import change_data as Cd
from flask import Flask,render_template,jsonify
from threading import Thread


# def change_msg1(msg):
#     data = []
#
#     data1 = []
#     dic = {}
#     line = msg.strip()
#     line.strip('[]')
#     line = line.strip().strip('[],')
#     line = line.split(',', 1)
#     # print(line)
#     if line[0]:
#         dic1 = {}
#         a = line[0].strip('{}').replace("'", "")
#         b = line[1].replace("'", "").replace("{", "").strip('}')
#         a1 = a.split(':', 1)
#         b1 = b.split(',', 1)
#         b2 = b1[0].split(':', 1)
#         b3 = b1[1].split(':', 1)
#         dic1[b2[0].replace("'",'').strip(" ")] = b2[1].replace("'",'').strip(" ")
#         dic1[b3[0].replace("'",'').strip(" ")] = b3[1].replace("'",'').strip(" ")
#         # print(dic1)
#         if a != '':
#             dic[a1[0].strip(" ")] = a1[1].strip(" ")
#             data1.append(dic)
#         data1.append(dic1)
#         #print(str(data1))
#         data.append(data1)
#         return data
#
# # 数据转换方法
# def change_msg(path):
#     data = []
#     with codecs.open(path, 'r','utf-8') as f:
#         for line in f:
#             data1 = []
#             dic = {}
#             line = line.strip()
#             line.strip('[]')
#             line = line.strip().strip('[],')
#             line = line.split(',', 1)
#             # print(line)
#             if line[0]:
#                 dic1 = {}
#                 a = line[0].strip('{}').replace("'", "")
#                 b = line[1].replace("'", "").replace("{", "").strip('}')
#                 a1 = a.split(':', 1)
#                 b1 = b.split(',', 1)
#                 b2 = b1[0].split(':', 1)
#                 b3 = b1[1].split(':', 1)
#                 dic1[b2[0].replace("'",'').strip(" ")] = b2[1].replace("'",'').strip(" ")
#                 dic1[b3[0].replace("'",'').strip(" ")] = b3[1].replace("'",'').strip(" ")
#                 # print(dic1)
#                 if a != '':
#                     dic[a1[0].strip(" ")] = a1[1].strip(" ")
#                     data1.append(dic)
#                 data1.append(dic1)
#                 #print(str(data1))
#                 data.append(data1)
#         return data
data1 = []
path1 = r"node.txt"
data = Cd.change_msg(path1)


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
                # path1 = header_dic['filename']
                # path = r'C:\Users\cao\Desktop\runoob01\blockchain\%s' % (path1)
                # print(path)
                client.send(b'Success')
                while True:

                    msg = client.recv(1024)
                    msg_recv = msg.decode('utf-8')
                    # msg_recv_dic = json.loads(msg_recv)
                    # print(msg_recv)
                    # msg_name = msg_recv_dic['name']
                    if not msg_recv:
                        continue
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
            except:
                print('客户端断开连接...')
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
    global data1,data
    data1 = Cd.input_data(data)
    return render_template('ss.html',result_data=data1)

@app.route('/')
def hello():
    return render_template("/visualserver/地图.html")


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=3000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    py_server = Server()

    py_server.start_new_thread()
    app.run(host='0.0.0.0',port=port)

