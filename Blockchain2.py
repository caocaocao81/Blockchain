import time
import json
import hashlib
import math
import socket
import threading
import os
from os.path import join as pjoin
from flask import Flask,jsonify,request
from textwrap import dedent
from uuid import uuid4
from urllib.parse import urlparse
from hashlib import sha256

post1 = 8000
#服务器地址
address = ('127.0.0.1',post1)

client_type = None


class Blockchain(object):
    def __init__(self):
        # 定义两个列表，用于记录区块链交易信息
        self.chain =[]
        self.current_transactions=[]
        self.nodes = set()
        # 客户端名
        self.client_type = self.input_client_type()
        # 创建“创世块”
        self.new_block(previous_hash=1, proof=100)

    def register_node(self, address):
        """
        增加一个新的网络节点到set集合
        :param address: <str>网络地址 'http://127.0.0.1:5001'
        :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
         检查给定的链是否是有效的
        :param chain: <list> 区块链
        :return: <bool>
        """
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            # 检验当前block的previous_hash值和前面block的hash值是否相等
            if block['previous_hash'] != self.hash(last_block):
                return False
            # 验证前面block的工作量证明和当前block的工作量证明拼接起来的字符串的hash是否以'abc'为开头
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        # 验证通过，返回True
        return True

    def resolve_conflicts(self):
        """
        共识算法解决冲突
        使用网络中最长的链.
        :return: <bool> True 如果链被取代, 否则为False
        """
        # 所有的邻居节点
        neighbours = self.nodes
        new_chain = None
        # 在所有邻居中查找比自己链更长的
        max_length = len(self.chain)
        # 遍历并且验证邻居链的有效性
        for node in neighbours:
            response = request.json.get(f'http://{node}/chain')
            print(response)
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                # 检查链是否更长，且有效。更新new_chain,并更新max_length。
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        # 如果new_chain是有定义的，则说明在邻居中找到了链更长的，用new_chain替换掉自己的链
        if new_chain:
            self.chain = new_chain
            return True
        return False

    def new_block(self,proof,previous_hash=None):
        """
        生成新块
        :param proof: <int> 工作量证明，它是一个工作算法对应的一个值
        :param previous_hash: (Optional) <str> 前一个区块的哈希值
        :return: <dict> 返回一个新的块，这个块block是一个字典结构
        """
        block ={
            'index':len(self.chain)+1,
            #时间戳，记录区块创建时间
            'timestamp': time.time(),
            #记录当前的交易记录
            'timesaction':self.current_transactions,
            #工作量证明
            'proof':proof,
            #前一区块的哈希值
            'previous_hash':previous_hash or self.hash(self.chain[-1])
        }
        #重置交易，记录下一次交易
        self.current_transactions = []
        # 将新生成的block添加到block列表中
        self.chain.append(block)
        # 返回新创建的blcok
        return block

    def new_transaction(self,sender,recipient,amount):
        '''
        # 在交易列表中添加一个交易信息
        sender <str>:发送者的地址
        recipient <str>:接收者地址
        amount <int>:交易的数值
        return <int>:返回新的Block的Id值，新产生的交易将会被记录在新的Block中
        '''
        self.current_transactions.append({
            'sender':sender,
            'recipient':recipient,
            'amount':amount,
        })

        return self.last_block['index']+1

    def start_new_thread(self):
        """启动新线程来接收信息"""
        thread = threading.Thread(target=self.recv_msg, args=())
        thread.setDaemon(True)
        thread.start()

    def input_client_type(self):
        return input("注册客户端，请输入名字 :")

    def send_data(self,client, cmd, ):
        jd = {}
        jd['COMMAND'] = cmd
        jd['client_type'] = self.client_type

        jsonstr = json.dumps(jd)
        print(jd)
        print('send: ' + jsonstr)
        client.sendall(jsonstr.encode('utf8'))

    def recv_msg(self):
        print('Waiting for server.')
        while True:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect(address)
                self.send_data(self.client_socket, 'CONNECT')
                self.connect_flag = True
                # 连接成功向服务器发送成功标志'Success'
                self.client_socket.send(b'Success')
                # 连接成功后开始接收服务器信息
                while True:
                    msg_recv = self.client_socket.recv(1024).decode('gbk')
                    if msg_recv == 'Success':
                        print('连接服务器成功')
                    elif msg_recv == 'Fail':
                        print('连接失败')
                    elif not msg_recv:
                        continue
                    else:
                        recv_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        print(recv_time)
            except:
                print('未知错误')
                break
    @staticmethod
    def hash(block):
        '''
        # 通过Hash算法返回区块的Hash值
        #生成 SHA-256 哈希值
        :param block:<dict> Block
        :return:<str>
        '''

        #首先将block字典结构转换成json字符串，再通过sort_keys指定按key排好序
        block_string = json.dumps(block,sort_keys=True).encode()
        #调用sha256函数求摘要
        return hashlib.sha256(block_string).hexdigest()


    @property
    def last_block(self):
        # 返回区块链中最后一个区块
        return self.chain[-1]
    def proof_of_work(self,last_proof):
        '''
        简单工作量证明:
        - 查找一个数 p 使得 hash(p+last_proof) 以'abc'开头
        - last_proof 是上一个块的证明,  p是当前的证明
        :param last_proof: <int>
        :return: <int>
        '''
        proof = 0
        #定义循环，直到valid_proof验证通过
        while self.valid_proof(last_proof,proof) is False:
            proof += math.pi

        return proof

    @staticmethod
    def valid_proof(last_proof,proof):
        """
        验证证明: 是否hash(last_proof, proof)以'abc'开头?
        :param last_proof: <int> 前一个证明
        :param proof: <int> 当前证明
        :return: <bool>
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return  guess_hash[:3] =='abc'

#实例化一个Flask节点
app = Flask(__name__)

#为当前节点生成一个全局唯一的地址，使用uuid4方法
node_identifier = str(uuid4()).replace('-', '')
#初始化区块链
blockchain = Blockchain()

blockchain.start_new_thread()



address1='http://127.0.0.1:'+str(post1)
print(address1)
#接受注册
@app.route('/nodes/register', methods=['GET','POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    print(nodes)
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    #注册节点到blockchain中
    for node in nodes:
        blockchain.register_node(node)
     #构造一个响应
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }

    #201：提示知道新文件的URL
    return jsonify(response), 201

#解决一致性问题的API
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
   #调用resolve_conficts()方法，让网络中的chain协调一致
    replaced = blockchain.resolve_conflicts()
    #如果当前节点的chain被替换掉，返回替换掉的信息；否则返回当前节点的chain是有权威的！
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200

#返回整个区块链，GET接口
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    blockchain.client_socket.sendall(bytes(repr(json.dumps(response)).encode('utf-8')))
    return jsonify(response), 200

# 创建一个交易并添加到区块，POST接口可以给接口发送交易数据
@app.route('/transactions/new', methods=['GET','POST'])
def new_transaction():

    #获取请求的参数，得到参数的json格式数据
    values = request.get_json()
    print('request parameters:%s'%(values))
    #检查请求的参数是否合法，包含sender,recipient,amount几个字段
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # 使用blockchain的new_transaction方法创建新的交易
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    #构建response信息
    response = {'message': f'Transaction will be added to Block {index}'}
    #返回响应信息
    return jsonify(response), 201

#让服务器挖掘新区块
@app.route('/mine', methods=['GET'])
def mine():
    # 获取区块链最后一个block
    last_block = blockchain.last_block
    # 取出最后一个block的proof工作量证明
    last_proof = last_block['proof']
    # 运行工作量的证明和验证算法，得到proof。
    proof = blockchain.proof_of_work(last_proof)

    # 给工作量证明的节点提供奖励.
    # 发送者为 "0" 表明是新挖出的币
    # 接收者是我们自己的节点，即上面生成的node_identifier。实际中这个值可以用用户的账号。
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # 产生一个新的区块，并添加到区块链中
    block = blockchain.new_block(proof)
    print(block)
    # 构造返回响应信息
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['timesaction'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'timestamp': block['timestamp'],
    }
    response1={
        'client-type':blockchain.client_type,
        'SendIp': socket.gethostbyname(socket.gethostname()),
        'SendIndex': block['index'],
        'SendTimestamp': block['timestamp'],
        'ReceiveIp': address1,
        'ReceiveIndex': block['index'],
        'ReceiveTimestamp': time.time(),
        'timeDf': time.time() - block['timestamp'],
    }
    # request1 = {
    #     'ReceiveIp': address1,
    #     'ReceiveIndex': block['index'],
    #     'ReceiveTimestamp': time.time(),
    #     'timeDf':time.time()-block['timestamp'],
    # }

    blockchain.client_socket.sendall(bytes(repr(json.dumps(response1)).encode('utf-8')))
    # blockchain.client_socket.sendall(bytes(repr(json.dumps(request1)).encode('utf-8')))
    path1 = r"C:\Users\cao\Desktop\runoob01\blockchain\Readfile"
    path = r"C:\Users\cao\Desktop\runoob01\blockchain\Readfile\file.json"
    listdir = os.listdir(path1)
    if 'file.json' in listdir:
        f = open(pjoin(path1, 'file.json'), 'a')
        f.write(json.dumps(response1,ensure_ascii=False,indent = 4))
        f.close()
    return jsonify(response), 200


@app.route('/')
def hello():
    blockchain.client_socket.sendall(b'hello, i am wang.')
    return 'hello'



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5002, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='127.0.0.1', port=port)