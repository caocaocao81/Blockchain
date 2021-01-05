# 水晶链Blockchain
----
# 用户说明

**使用环境**

IPV6环境下或IPV4环境下，linux里安装docker环境以及geth环境,再在docker拉取部署有python3.7以及flask，web3等相关必备库的镜像。在纯IPV6环境下模拟，我们安装在一台CentOS主机上。

环境配置：

宿主机内需要开启IPv6环境。docker容器需要支持IPV6。

在docker配置文件添加IPv6配置参数，配置文件路径为 /etc/docker/daemon.json。如果文件不存在，请直接创建.

可直接将docker的默认IPv6网段设置为 fc00:17:1:1::/64,以下是该过程的操作：

vim /etc/docker/daemon.json，进入文件后写入：

{

"ipv6":true,

"fixed-cidr-v6":"fc00:17:1:1::/64"

}

一创建服务器的ipv6网络就不能与外部通信，接着编辑sysctl.conf 文件加入如下语句

vim /etc/sysctl.conf

net.ipv6.conf.eth0.accept_ra = 2

net.ipv6.conf.all.forwarding = 1

net.ipv6.conf.default.forwarding = 1

之后手动将刚刚的IPv6内网地址设置NAT转换（docker在IPv6环境下会自动将内网地址做NAT转换)并通过-L查看NAT是否添加成功。

ip6tables -t nat -A POSTROUTING -s fc00:17:1:1::/64 -j MASQUERADE

service ip6tables save

ip6tables -t nat -L

最后重启docker服务:

systemctl restart docker. 

若docker重启报错，原因可能是之前修改的 daemon.json 文件格式或者里面的数值规范不正确.修改即可.

(此操作可能会导致宿主机ipv6网络无法通信..经测试疑似docker启动了ipv6之后主动将宿主机ipv6路由关闭了...）



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
docker run -p 31422:31422 -it --name node2 ctt291247908/blockchain_python3:node2

docker run -p 30002:30002 -it --name node3 ctt291247908/blockchain_python3:node3

重复进入容器后的操作即可。 -p 的端口号如果有所修改需要修改对应的文件 比如修改 -p 9912：28010中的9912则需要修改 /home/geth/static-nodes.json文件中 

注意说明（若要修改visualserver的ip地址）：
vim /home/blockchain/node.py

修改node.py内19行ip地址修改成visualserver节点所在主机的ip 端口号默认为6060 

上述完成后 在当前目录下

python3 node.py -p xxxx (端口号为启动私链节点时候该节点的 --http.port)

其中区块链节点注册在 /home/geth文件内 node.py(node节点程序)放在 /home/blockchain文件内。启动python程序时候手动输入python3 node.py -p xxxx进行启动程序(其中-p是监听区块链私链节点的端口)或者在最初目录下输入bash startnode.py进行启动程序，不过启动node节点需要先启动区块链私链节点（在 /home/geth目录下 输入 bash start.sh启动区块链私链节点，进入节点后可以输入miner.start()进行挖矿操作，本例目前作图数据得自区块更新所产生的数据)。
