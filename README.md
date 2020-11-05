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
