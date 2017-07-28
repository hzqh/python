# -*-coding:UTF-8-*- 
import random
import string
import struct
from Crypto.Cipher import AES
import hmac
import hashlib
import binascii
# 产生随机列表
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
    for i in range(0,len(list1)):
        rst = list1[i] ^ list2[i]
        result = orxlist.append(rst)
    return orxlist

#随机y个字符串
def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))

#整形数组转化字符串
def int_list_str(arr):
    return ''.join(chr(x) for x in arr)

#字符转为对应ASCII码
def unpack_list(str):
    return list(struct.unpack('%dB'%len(str), str))

#整形元祖转化为字符串
def pack_bin(arr):
    return struct.pack('%dB'%len(arr), *arr)

def len2bit(length):
    len_low = length & 0xff
    len_high = (length & 0xff00) >> 8
    return [len_high, len_low]

def aes_decrypt(key, data):
    iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]           
    aes_object = AES.new(struct.pack('%dB'%len(key), *key), AES.MODE_CBC, struct.pack('%dB'%len(iv), *iv))         
    return aes_object.decrypt(data)

def aes_encrypt(key, data):
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
    iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]           # 16个0，随机向量
    aes_object = AES.new(struct.pack('%dB'%len(key), *key), AES.MODE_CBC, struct.pack('%dB'%len(iv), *iv))         # AES 创建对象
    return aes_object.encrypt(pad(data))

def hmac_sha256(key, req):
    # print '__algorithm__ :  hmac_sha256 '
    hmac256 = hmac.new(struct.pack('%dB'%len(key), *key), struct.pack('%dB'%len(req), *req), digestmod=hashlib.sha256).digest()
    return hmac256

def psd_sha256(psd):
    psd_sha256_hex = hashlib.sha256(psd).hexdigest()
    return binascii.unhexlify(psd_sha256_hex)

#  AES CBC PKCS7padding
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]

