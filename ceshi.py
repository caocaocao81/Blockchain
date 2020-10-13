import flask
import json
import math
import socket
import threading
import os
import time
from os.path import join as pjoin
from web3 import Web3,HTTPProvider,WebsocketProvider
from web3.auto import w3


class Client():

    def __init__(self,ip,rpcport):
        self.server_address = ('127.0.0.1', 8000)
        self.ww = Web3(HTTPProvider('http://' + ip + ':' + rpcport, request_kwargs={'timeout': 60}))
        self.ad = self.ww.geth.admin.datadir()
        self.info = self.ww.geth.admin.node_info()
        self.num = self.ww.eth.getBlock("latest")['number']
        print(self.ww.geth.admin.datadir())
        self.ip = None
        # 链接标志
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
                            self.client_socket.sendall(bytes(repr(json.dumps(self.info['enode'])).encode('utf-8')))

                            while True:
                                if  self.ww.eth.getBlock('latest')['number'] >self.num:
                                    self.client_socket.sendall(bytes(repr(json.dumps(self.ww.eth.getBlock('latest')['timestamp'])).encode('utf-8')))
                                    self.num = self.ww.eth.getBlock('latest')['number']
                                    transaction = self.ww.eth.getBlock("latest")['transactions']
                                    print(transaction)
                                    # self.client_socket.sendall(bytes(repr(json.dumps(
                                    #     self.ww.eth.getTransaction(
                                    #         "0xac35a4d4511a8c02d45b005880c4865c24516a8c96462312b5475db8eb57fcf4")['from'])).encode('utf-8')))
                                    reponse = {
                                        'block_num':self.num,
                                        'timestamp':self.ww.eth.getBlock('latest')['timestamp'],
                                        'transaction':self.ww.eth.getBlock('latest')['transactions'],
                                        'ip':self.ww.geth.admin.node_info()['ip'],
                                    }
                                    path1 = r"C:\Users\cao\Desktop\runoob01\blockchain\Readfile"
                                    if transaction :
                                        reponse1 = {
                                            'send_ip':self.ip,
                                            'recieve_ip':transaction['to'],
                                            'timestamp':self.ww.eth.getBlock(transaction['blockNumber'])['timestamp'],
                                        }
                                        listdir1 = os.listdir(path1)
                                        if 'transcation.json' in listdir1:
                                            f = open(pjoin(path1, 'transcation.json'), 'a')
                                            f.write(json.dumps(reponse1, ensure_ascii=False, indent=4))
                                            f.close()
                                    listdir = os.listdir(path1)
                                    if 'file.json' in listdir:
                                        f = open(pjoin(path1, 'file.json'), 'a')
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
                print('连接服务器失败')
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

def main():
    ip = input("请输入要输入的ip:")
    rpcport = input("请输入要输入的端口号:")
    wf = Client(ip,rpcport)
    wf.ip = str(ip)+":"+str(rpcport)
    wf.start_new_thread()

if __name__ == '__main__':

    main()

    while True:
        a = input("请输入要发送的信息:")




