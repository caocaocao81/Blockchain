# 水晶链Blockchain
----
# 用户说明

**使用环境**

IPV6环境下或IPV4环境下，linux里安装docker环境以及geth环境,再在docker拉取部署有python3.7以及flask，web3等相关必备库的镜像。在纯IPV6环境下模拟，我们安装在一台CentOS主机上。

**功能列表**

VisualServer节点程序
1. 连接记录区块链节点的程序。
2. 获取记录区块链节点同步信息。
3. 将区块链节点同步信息通过浏览器作出相应的轨迹图。

Node节点程序  
1. 连接VisualServer节点程序。 
2. 连接区块链节点并持续接收区块链节点区块更新或交易信息。 
3. 记录区块更新或交易信息并将其进行数据转换。 
4. 传输信息到VisualServer节点程序。 

----
## 安装原理
1. 安装docker
2. 拉取visualserver docker镜像
3. 拉取Node节点 docker镜像
----


## 操作原理
1. docker拉取visualserver docker镜像
2. 创建blockchain 网络
3. 启动visualserver节点的容器（自动运行visualserver节点）
4. 再在本机或者其他拥有公网或者局域网IP地址的主机上运行多个Node节点（注意：需要先启动相应的区块链节点）
5. 区块链节点连接后，进行挖矿等区块更新操作。
6. visualserver节点接收Node节点更新区块信息并将其作图
7. 通过浏览器浏览相应visualserver端口查看节点区块所形成的轨迹图。


-----
## 具体安装步骤（从docker hub 拉取镜像及启动步骤，以CentOS 7.4机器为例）
### 安装visualserver镜像：
docker pull ctt291247908/blockchain_python3:vserver 

启动容器：
docker run  -it  -p 6060:6060 -p 3000:3000  --name visualserver ctt291247908/blockchain_python3:vserver   
进入容器后
cd /home/blochchain/x

python3 server2.py

其中server2.py（visualserver程序）以及部分需要的文件放在docker里 /home/blockchain/x 文件内。其中启动容器时候开放的端口中3000是外部访问查看作图的端口，6060是外部node节点连接visualserver节点的端口。templates文件包含了可视视图文件，而static文件包含作图所要用到的css以及js文件。

### 安装区块链节点镜像:
docker hub上提供三个测试容器节点： node1 node2 node3 （环境均已配置好）

拉取测试节点镜像：

docker pull ctt291247908/blockchain_python3:node1

docker pull ctt291247908/blockchain_python3:node2

docker pull ctt291247908/blockchain_python3:node3

启动容器
docker run -p 9912:28010 -it --name node1 ctt291247908/blockchain_python3:node1
其中-p 9912：28010中9912为宿主机端口，28010为容器端口

进入容器后 到geth目录

cd /home/geth 然后命令台输入 bash start.sh 私链节点启动的命令即可以启动私链节点。

然后再在另外一个终端进入该容器 
docker exec -it node /bin/bash

bash startnode.sh 即可以启动节点

以此类似启动node2 node3两个节点
docker run -p 31422:31422 -it --name node1 ctt291247908/blockchain_python3:node2

docker run -p 30002:30002 -it --name node1 ctt291247908/blockchain_python3:node1

重复进入容器后的操作即可。 -p 的端口号如果有所修改需要修改对应的文件 比如修改 -p 9912：28010中的9912则需要修改 /home/geth/static-nodes.json文件中 

注意说明（若要修改visualserver的ip地址）：
vim /home/blockchain/node.py

修改node.py内19行ip地址修改成visualserver节点所在主机的ip 端口号默认为6060 再转到第210行修改ip为0.0.0.0如果私链没在本机启动则修改ip为启动私链节点的ip地址(本例直接在容器内启动则只需要改为0.0.0.0即可)
上述完成后 在当前目录下

python3 node.py -p xxxx (端口号为启动私链节点时候该节点的 --http.port)

其中区块链节点注册在 /home/geth文件内 node.py(node节点程序)放在 /home/blockchain文件内。因为未写启动程序的脚本所以启动python程序时候需要手动输入python3 node.py -p xxxx进行启动程序(其中-p是监听区块链私链节点的端口)而且node节点需要区块链私链节点先启动。

### 私链启动：
若 bash /home/geth/start.sh 脚本命令启动失败则可参考如下来启动节点：

进入相应目录
cd /home/geth

修改节点自动连接的json文件
vim static-nodes.json 将里面类似@127.0.0.1:2377?discport=0形式的代码改成@xxxx.xxxx.xxxx.xxxx:2377?discport=0其中xxxx.xxxx.xxxx.xxxx

启动命令参考：geth --datadir data1 --networkid 15 --port xxxx --http --http.addr 0.0.0.0 --http.port xxxx --http.api  debug,net,eth,web3,admin,miner,personal --ipcdisable --http.corsdomain '*' --nodiscover -nousb console 

目前还未实现自动连接，如果要与其他区块链节点相连则需要自己手动添加节点admin.addPeer（）括号内为该节点的enode信息。需要把末尾的ip改成要连接到的ip地址 例如本例中@127.0.0.1:2377?discport=0
要改成@xxxx.xxxx.xxxx.xxxx:2377?discport=0

其中--http.port 需要和node.py -p 的端口号一致。 --port是主机监听的端口
