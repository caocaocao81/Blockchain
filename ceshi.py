import flask
import json
import math
import socket
import threading
import os
import time
import random
from os.path import join as pjoin
from argparse import ArgumentParser
from flask import Flask,render_template
from web3 import Web3,HTTPProvider,WebsocketProvider

server1 = '127.0.0.1:3344'
server2 = '127.0.0.1:5010'
server3 = '127.0.0.1:8545'

class Client():

    def __init__(self,ip,rpcport):
        self.server_address = ('172.20.0.2', 8000)
        self.ww = Web3(HTTPProvider('http://' + ip + ':' + rpcport, request_kwargs={'timeout': 60}))
        self.ad = self.ww.geth.admin.datadir()
        self.info = self.ww.geth.admin.node_info()
        self.num = self.ww.eth.getBlock("latest")['number']
        print(self.ww.geth.admin.datadir())
        self.port = None
        self.ip = None
        # 链接标志pip
        self.connect_flag = False
    def recv_msg(self):
        print("正在连接服务器....")

        # 客户端连接服务器
        while True:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect(self.server_address)
                # 连接成功向服务器发送成功标志'Success'
                self.client_socket.send(b'Success')
                # 连接成功后开始接收服务器信息
                while True:
                    msg_recv = self.client_socket.recv(1024).decode('gbk')


                    if msg_recv == 'Success':
                        print('客户端已与服务器成功建立连接...')

                        if self.ww.isConnected() == True:
                            print('与区块链节点已连接....')
                            # print(self.info['id'])
                            print(self.port)
                            self.client_socket.sendall(bytes(repr(json.dumps(self.info['enode'])).encode('utf-8')))
                            # data1 = []
                            # data = change_rcg(self.port, port1)
                            # data1.append(data)
                            # path1 = r"C:\Users\cao\Desktop\runoob01\blockchain\Readfile\transcation.txt"
                            # text_save(path1,data1)
                            while True:
                                if  self.ww.eth.getBlock('latest')['number']  >self.num :
                                    self.client_socket.sendall(bytes(repr(json.dumps(self.ww.eth.getBlock('latest')['timestamp'])).encode('utf-8')))
                                    if self.ww.eth.getBlock("latest")['miner'] != self.ww.eth.accounts[0]:
                                        re_timestamp = time.time()
                                        se_timestamp = self.ww.eth.getBlock("latest")['timestamp']
                                        data1 = []
                                        port1 = (random.randrange(9) + 1) * 800 + 1000
                                        data = change_rcg(self.port, port1,se_timestamp,re_timestamp)
                                        data1.append(data)
                                        if self.port >=3000 and self.port<5000:
                                            path1 = r"transcation.txt"
                                        elif self.port>=5000 and self.port<8000:
                                            path1 = r"node2.txt"
                                        else:
                                            path1 = r"node3.txt"
                                        text_save(path1, data1)
                                    # self.client_socket.sendall(bytes(repr(json.dumps(self.ww.eth.getBlock('latest')['timestamp'])).encode('utf-8')))
                                    self.num = self.ww.eth.getBlock('latest')['number']

                                    transaction = self.ww.eth.getBlock("latest")['transactions']
                                    reponse = {
                                        'block_num':self.num,
                                        'timestamp':self.ww.eth.getBlock('latest')['timestamp'],
                                        'transaction':self.ww.eth.getBlock('latest')['transactions'],
                                        'ip':self.ww.geth.admin.node_info()['ip'],
                                    }
                                    if transaction :
                                        # 转换数据
                                        data1=[]
                                        port1 = (random.randrange(9)+1) *900 + 1000
                                        data = change_rcg(self.port,port1)
                                        data1.append(data)
                                        reponse1 = {
                                            'send_ip':self.ip,
                                            'recieve_ip':server1,
                                            'timestamp':self.ww.eth.getBlock(transaction['blockNumber'])['timestamp'],
                                        }
                                        path = r"./"
                                        listdir1 = os.listdir(path)
                                        if 'transcation.json' in listdir1:
                                            f = open(pjoin(path, 'transcation.json'), 'a')
                                            f.write(json.dumps(data1, ensure_ascii=False, indent=4))
                                            f.close()
                                    path = r"./"
                                    listdir = os.listdir(path)
                                    if 'file.txt' in listdir:
                                        f = open(pjoin(path, 'file.txt'), 'a')
                                        f.write(json.dumps(reponse, ensure_ascii=False, indent=4))
                                        f.close()
                                    continue
                                else:
                                    continue
                        else:
                            continue
                    elif msg_recv == 'Fail':
                        print('客户端与服务器建立连接失败...')
                    elif not msg_recv:
                        continue
                    else:
                        recv_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        print( '服务器 ' + recv_time + ':\n')
                        print(' ' + msg_recv + '\n')

            except:
                print('与服务器断开连接...')
                break

    def start_new_thread(self):
        """启动新线程来接收信息"""
        thread = threading.Thread(target=self.recv_msg, args=())
        thread.setDaemon(True)
        thread.start()

    # 返回值为区块hash地址
    # 0x6d2629b8693d35ffd735d67d0e823108f1fc168b4162950900e22214732e386c

    def set_trans(self):
        accounts = self.ww.eth.accounts
        self.ww.geth.personal.unlockAccount(self.ww.eth.accounts[0], '123')
        trans_id = self.ww.eth.sendTransaction(
            {'to': self.ww.toChecksumAddress(accounts[1]), 'from': self.ww.eth.coinbase, 'value': 12345})
        print(trans_id)
        return trans_id

    # 如果为None则矿工还没挖到该交易
    # AttributeDict({
    #     'blockHash': HexBytes('0x0000000000000000000000000000000000000000000000000000000000000000'),
    #     'blockNumber': None,
    #     'from': '0xE6829A20492D11A5C84b7B0F3240A99971d1FbFF',
    #     'gas': 121680, 'gasPrice': 18000000000,
    #     'hash': HexBytes('0x6d2629b8693d35ffd735d67d0e823108f1fc168b4162950900e22214732e386c'),
    #     'input': '0x48656c6c6f576f726c64',
    #     'nonce': 0, 'to': '0x2e8AAf37736C4CeAc8d0366Ffa97aA7B62957b72', 'transactionIndex': 0,
    #     'value': 12345, 'v': 56, 'r': HexBytes('0x750bc8a9ef4f20e129c2a71a0c9d496aaacafd49f1d514c0c4d380887590fefc'),
    #     's': HexBytes('0x37bbe55ef6363ee98d66e131fc862d9e8451353c8b1e2a5c8f3533304db72b42')})
    def get_trans_detail(self,trans_id=None):
        information = self.ww.eth.getTransaction(trans_id)
        timestamp = time.time()
        return information,timestamp

def change_rcg(port1,port2,t1,t2):
    date=[]
    name1={}
    name2={}
    city_name = ['包头','福州','海口','乌鲁木齐','保定','兰州','中山','丹东','北海','南京','南宁','南昌','南通','金华','湘潭','秦皇岛','绍兴','衢州']
    value = int(abs(t2-t1)*6)
    if(int(port1)<5000):
        name1['name'] = '北京'
    elif(int(port1)>=5000 and int(port1)<8000):
        name1['name'] = '上海'
    else:
        name1['name'] = '广州'
    # if (int(port2) < 5000):
    #     name2['name'] = '包头'
    #     name2['value'] = value
    # elif (int(port2) >= 5000 and int(port2) < 8000):
    #     name2['name'] = '福建'
    #     name2['value'] = value
    # else:
    #     name2['name'] = '海口'
    #     name2['value'] = value
    num = int((port2 - 1800)/450)
    name2['name'] = city_name[num]
    name2['value'] = value

    date.append(name1)
    date.append(name2)
    return date


def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')+','+'\n'#去除[],这两行按数据不同，可以选择
        # s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存成功",filename)

def main():
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=3965, type=int, help='port to listen on')
    args = parser.parse_args()
    port = str(args.port)
    ip = '192.168.43.188'
    wf = Client(ip,port)
    wf.port = int(port)
    wf.ip = str(ip)+":"+str(port)
    wf.start_new_thread()


if __name__ == '__main__':

    main()

    while True:
        a = input()




