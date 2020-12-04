import codecs

def change_msg1(msg):
    data = []
    data1 = []
    dic = {}
    line = msg.strip()
    line.strip('[]')
    line = line.strip().strip('[],')
    line = line.split(',', 1)
    # print(line)
    if line[0]:
        dic1 = {}
        a = line[0].strip('{}').replace("'", "")
        b = line[1].replace("'", "").replace("{", "").strip('}')
        a1 = a.split(':', 1)
        b1 = b.split(',', 1)
        b2 = b1[0].split(':', 1)
        b3 = b1[1].split(':', 1)
        dic1[b2[0].replace("'",'').strip(" ")] = b2[1].replace("'",'').strip(" ")
        dic1[b3[0].replace("'",'').strip(" ")] = b3[1].replace("'",'').strip(" ")
        # print(dic1)
        if a != '':
            dic[a1[0].strip(" ")] = a1[1].strip(" ")
            data1.append(dic)
        data1.append(dic1)
        #print(str(data1))
        data.append(data1)
        return data

def change_msg(path):
    data = []
    with codecs.open(path, 'r','utf-8') as f:
        for line in f:
            data1 = []
            dic = {}
            line = line.strip()
            line.strip('[]')
            line = line.strip().strip('[],')
            line = line.split(',', 1)
            # print(line)
            if line[0]:
                dic1 = {}
                a = line[0].strip('{}').replace("'", "")
                b = line[1].replace("'", "").replace("{", "").strip('}')
                a1 = a.split(':', 1)
                b1 = b.split(',', 1)
                b2 = b1[0].split(':', 1)
                b3 = b1[1].split(':', 1)
                dic1[b2[0].replace("'",'').strip(" ")] = b2[1].replace("'",'').strip(" ")
                dic1[b3[0].replace("'",'').strip(" ")] = b3[1].replace("'",'').strip(" ")
                # print(dic1)
                if a != '':
                    dic[a1[0].strip(" ")] = a1[1].strip(" ")
                    data1.append(dic)
                data1.append(dic1)
                # print(str(data1))
                data.append(data1)
        return data
def change_msg2(path):
    data = []
    with codecs.open(path, 'r','utf-8') as f:
        for line in f:
            data1 = []
            dic = {}
            line = line.strip()
            line.strip('[]')
            line = line.strip().strip('[],')
            line = line.split('},', 2)
            print(line[1],line[2])
            if line[0]:
                dic1 = {}
                print(line)
                a = line[0].strip('{}').replace("'", "")
                b = line[1].replace("'", "").replace("{", "").strip('}')
                a1 = a.split(':', 1)
                b1 = b.split(',', 1)
                b2 = b1[0].split(':', 1)
                b3 = b1[1].split(':', 1)
                c = line[2].replace("'", "").replace("{", "").strip('}')
                c1 = c.split(':', 1)
                dic1[b2[0].replace("'",'').strip(" ")] = b2[1].replace("'",'').strip(" ")
                dic1[b3[0].replace("'",'').strip(" ")] = b3[1].replace("'",'').strip(" ")
                # print(dic1)
                if a != '':
                    dic[a1[0].strip(" ")] = a1[1].strip(" ")
                    data1.append(dic)
                dic2 = {}
                dic2[c1[0].strip(" ")] = c1[1].strip(" ")
                # print(dic2)
                data1.append(dic1)
                data1.append(dic2)
                data.append(data1)
        return data
# def add_value(data,port1,port2,value):
#     data
def input_data(data):
    data1 = []
    for i in range(len(data)):
        if int(data[i][1]['value']) != 0:
            data1.append(data[i])
    # print(data1)
    return data1

def pd(data,data1):
    for i in range(len(data)):
        if(data[i][0]['name']==data1[0][0]['name'] and data[i][1]['name']==data1[0][1]['name']):
            data[i][1]['value'] = data1[0][1]['value']
    return data



# msg = "{'name': '上海'}, {'name': '广州', 'value': 20},"
# da = change_msg1(msg)
# print(da)
# path2 = r"C:\Users\cao\Desktop\runoob01\blockchain\Readfile\node.txt"
# path2 = r"C:\Users\cao\Desktop\runoob01\blockchain\node3.txt"
# data = change_msg2(path2)
# print(data)
#
# data = pd(data,da)
# print(data)
#
# data1 = input_data(data)
#
#
# print(data1)
