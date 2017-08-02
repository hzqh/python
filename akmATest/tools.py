# -*-coding:UTF-8-*- 
import random
import datetime
# 随机数组生成
def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list 

# 异或操作
def listXor(list1,list2):
    orxlist = []
    for i in range(0,len(list2)):
        rst = list1[i] ^ list2[i]
        result = orxlist.append(rst)
    return orxlist

#  AES CBC PKCS7padding
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]

def getTimeStamp():
    dt = datetime.datetime.now()
    return dt.strftime("%Y%j%H%M%S") + str(dt.microsecond)