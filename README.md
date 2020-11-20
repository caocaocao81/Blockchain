# Blockchain
----
# 用户说明

**使用环境**

IPV6环境下或者IPV4环境下，Ubuntu里安装docker环境以及geth环境,再在docker拉取部署有python3.7以及flask，web3等相关必备库的镜像。

**功能列表**
VisualServer节点程序
1. 连接记录区块链节点的程序
2. 获取记录区块链节点同步信息。
3. 将区块链节点同步信息通过浏览器作出相应的轨迹图。

Node节点程序
1.连接VisualServer节点程序
2.连接区块链节点并持续接收区块链节点区块更新或交易信息
3.记录区块更新或交易信息并将其进行数据转换
4.传输信息到VisualServer节点程序

----
## 安装步骤
1. 安装docker
2. 安装visualserver docker镜像
3. 安装Node节点 docker镜像
4. 安装geth 
----


## 操作步骤
1. docker拉取visualserver docker镜像
2. 创建blockchain 网络
3. 启动visualserver节点的容器（自动运行visualserver节点）
4. 再在本机或者其他拥有公网或者局域网IP地址的主机上运行多个Node节点（注意：需要先启动相应的区块链节点）
5. 区块链节点连接后，进行挖矿等区块更新操作。
6. visualserver节点接收Node节点更新区块信息并将其作图
7. 通过浏览器浏览相应visualserver端口查看节点区块所形成的轨迹图。


-----
## 从docker hub 拉取镜像及启动步骤（CentOS为例）
### visualserver镜像：
docker pull ctt291247908/ubuntu-python3.7-geth:visualserver 

其中server1.py（visualserver程序）以及部分需要的文件放在docker里 /home/blockchain/x 文件内。
 
### 节点镜像:
docker pull ctt291247908/ubuntu-python3.7-geth:v3 (该镜像内以及注册好六个区块链私链节点)
docker pull ctt291247908/ubuntu-python3.7-geth:v2 (区块链私链节点还未注册)

其中区块链节点注册在 /home/geth文件内 ceshi.py(node节点程序)放在 /home/blockchain文件内。因为未写启动程序的脚本所以启动python程序时候需要手动输入python3 ceshi.py -p xxxx进行启动程序(其中-p是监听区块链私链节点的端口)而且node节点需要区块链私链节点先启动。

### 私链启动：
启动命令参考：geth --datadir ces1 --networkid 15 --port 2377 --http --http.addr 0.0.0.0 --http.port 9545 --http.api  debug,net,eth,web3,admin,miner,personal --ipcdisable --http.corsdomain '*' --nodiscover -nousb console 

其中--http.port 需要和ceshi.py -p 的端口号一致。
