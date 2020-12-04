import codecs

# b = [
#     {'name': 10, 'value': 0, 'value1': 0},
#     {'name': 20, 'value': 0, 'value1': 0},
#     {'name': 30, 'value': 0, 'value1': 0},
# ]

# 修改信息格式
def change_msg1(msg):
    data = []
    dic = {}
    line = msg.strip()
    line = line.strip('{').strip('},')
    line = line.split(',', 2)
    a = line[0].strip('{}').replace('"', "")
    a1 = a.split(':', 1)
    b = line[1].strip('{}').replace('"', "")
    b1 = b.split(':', 1)
    c = line[2].strip('{}').replace('"', "")
    c1 = c.split(':',1)
    dic[a1[0].strip(" ")] = a1[1].strip(" ")
    dic[b1[0].strip(" ")] = b1[1].strip(" ")
    dic[c1[0].strip(" ")] = c1[1].strip(" ")
    # print(dic)
    data.append(dic)
    return data

# 判断消息数据（是区块数还是更新信息）
def pd(msg):
    data = []
    dic = {}
    line = msg.strip()
    line = line.strip('{').strip('},').replace('"',"'")
    line = line.split(',', 2)
    a = line[0].strip('{}').replace("'", "")
    a1 = a.split(':', 1)
    dic[a1[0].strip(" ")] = a1[1].strip(" ")
    # print(dic)
    data.append(dic)
    return data

# 修改数据格式
def change_msg(path):
    data = []
    with codecs.open(path, 'r','utf-8') as f:
        for line in f:
            dic = {}
            line = line.strip()
            line = line.strip('{').strip('},')
            line = line.split(',', 2)
            a = line[0].strip('{}').replace("'", "")
            a1 = a.split(':', 1)
            b = line[1].strip('{}').replace("'", "")
            b1 = b.split(':', 1)
            c = line[2].strip('{}').replace("'", "")
            c1 = c.split(':', 1)
            dic[a1[0].strip(" ")] = a1[1].strip(" ")
            dic[b1[0].strip(" ")] = b1[1].strip(" ")
            dic[c1[0].strip(" ")] = c1[1].strip(" ")
            # print(dic)
            data.append(dic)
    return data

def put_fnum(b,num):
    b[0]['value1'] = num
    return b

def put_nownum(data,data1):
    # data 记录数据的集合
    # data1 客户端发送的数据
    for i in range(len(data)):
        if data[i]['name'] == data1[0]['name']:
            data[i]['value'] = data1[0]['value']
            data[i]['value1'] = data1[0]['value1']
            return data

# dic = '{"name":10, "value": 20, "value1": 30}'
# data = pd(dic)
# print(data)
# da = change_msg1(dic)
# print(da[0])
# path = r"C:\Users\cao\Desktop\blocknum.txt"
# data = change_msg(path)
# print(data)
# data = put_nownum(b,da)
# print(data)
# # b = put_fnum(data,30)
# print(b)