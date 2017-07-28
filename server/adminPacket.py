#!/usr/bin/python
# -*- coding: utf8 -*-
# This is for AES Encryption Algorithm
import socket
import sys #for exit
import time
import struct
import hashlib
import binascii
import hmac
import random
# import array
from Crypto.Cipher import AES
import string
BUFSIZE = 1024 
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
    for i in range(0,len(list1)):
        rst = list1[i] ^ list2[i]
        result = orxlist.append(rst)
    return orxlist
def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))
def int_list_str(arr):
    return ''.join(chr(x) for x in arr)
def unpack_list(str):
    return list(struct.unpack('%dB'%len(str), str))
def pack_bin(arr):
    return struct.pack('%dB'%len(arr), *arr)
def len2bit(length):
    len_low = length & 0xff
    len_high = (length & 0xff00) >> 8
    return [len_high, len_low]
def aes_decrypt(key, data):
    iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]           
    aes_object = AES.new(pack_bin(key), AES.MODE_CBC, pack_bin(iv))         
    return aes_object.decrypt(data)
def aes_encrypt(key, data):
    iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]           # 16个0，随机向量
    aes_object = AES.new(pack_bin(key), AES.MODE_CBC, pack_bin(iv))         # AES 创建对象
    return aes_object.encrypt(pad(data))
def hmac_sha256(key, req):
    # print '__algorithm__ :  hmac_sha256 '
    hmac256 = hmac.new(pack_bin(key), pack_bin(req), digestmod=hashlib.sha256).digest()
    return hmac256
def psd_sha256(psd):
    psd_sha256_hex = hashlib.sha256(psd).hexdigest()
    return binascii.unhexlify(psd_sha256_hex)

#  AES CBC PKCS7padding
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]

class AdminPacket(object):
    
    def __init__(self):
        #packet header constractor
        self.version=1
        self.encry_alg=1
        self.key_id=[01,01,01,01,01,01,01,01,01,01,01,01,01,07,01,04]
        self.sess_key=''
        self.sess_key_id=''
        self.userType_flag=1
    
    def admin(self,s):
        req_id = random_int_list(0, 255, 2)                # Request ID 2字节
#        print 'first request id : ', req_id       
        user = 'client_qh001'                         # 用户名
        userLen = len(user)                            # 用户名长度 10
        psd = 'node_child'  
                                  # 密码
        psdSHA256 = psd_sha256(psd)
        psdBin = [ord(x) for x in psdSHA256]
        psdLen = len(psdBin)                            # 密码长度
        
        body = [101] + req_id + [userLen, user, psdLen]
        
        auth_id = [01] * 16              # 认证密钥ID 16字节
        authKey = [01] * 32             # 认证密钥 32字节
        authKey_hmac256 = hmac_sha256(authKey, req_id)    # 认证密钥ID HMAC-SHA256方式加密
        
        session = random_int_list(0, 255, 48)
        session_id = session[0:16]
        session_key = session[16:48]
        
        body_pack = struct.pack('@4B%dsB'%userLen, *body) + psdSHA256 + pack_bin(auth_id) + authKey_hmac256 + pack_bin(session)
#        print '--- --  body_pack: ',len(body_pack)
        # AES 加密
        Encryp_key = [01] * 32    # 加密密钥
        body_AES_pack = aes_encrypt(Encryp_key, body_pack)
        # print '--117----AES pad after: ',len(body_AES_pack)
        # --------------------- 报文头Start -------------------------- #
        # Version = 1 
        # Encryption Algorithm =  0 1:AES, 2: DES, 3: 3DES, 4: Blowfish
        # Message Length : mesLen = 数据长度 
        # Encryption Key ID（Optional）: 加密密钥ID
        # ---------------------- 报文头End --------------------------- #
        
        version = 1
        Encryp_Alg = 1            # 加密方式
#         Encryp_id = [01] * 16    # 加密密钥ID 16字节
        Encryp_id = [01,01,01,01,01,01,01,01,01,01,01,01,01,07,01,04]
        mesLen = len(body_AES_pack)
        head = [version, Encryp_Alg] + len2bit(mesLen)
        head_pack = struct.pack('@4B', *head) + pack_bin(Encryp_id) if Encryp_Alg == 1 else struct.pack('@4B', *head)
        
#        print '---131---AES length: ', len(head_pack + body_AES_pack)
        if Encryp_Alg == 1:
#            print u'发送接入认证请求报文'
            s.send(head_pack + body_AES_pack)           # AES加密
        else:
            s.send(head_pack + body_pack)               # 不加密
        
        # while True:
        #     recvData = s.recv(BUFSIZE)
        #     if not recvData:
        #         break
        #     if len(recvData) == 148 or len(recvData) == 8:
        #         break
        # print '---145---recive all data: ', recvData
        recvData = s.recv(BUFSIZE)
        # print '---145---recive all data: ',recvData
#        print u'接收到的接入认证反馈报文：',len(recvData)
        # # ------------------ 反馈报文信息Start -------------------- #
        if len(recvData):
            if Encryp_Alg == 1:
                recvHead = recvData[0:20]           # 加密为[0:20]
                recvBody = recvData[20:len(recvData)]
                # recvBody = aes_decrypt(Encryp_key, recvBody)
                recvBody = unpad(aes_decrypt(Encryp_key, recvBody))      # padding Or don't need 
            else:
                recvHead = recvData[0:4]           # 不加密为[0:4]
                recvBody = recvData[4:len(recvData)]
            recv_Body = unpack_list(recvBody)
#            print u'接入认证反馈报文体：',recv_Body
        
            recvBody_req_id = recv_Body[1:3]        # Request ID
#            print u'接入认证反馈报文头-前四个：', recv_Body[0:4]
            
            if recv_Body[3] == 0:      # 成功
                if self.userType_flag == 0:      # 内部设备
                    print u'这是内部设备------------'
                    parentUserLen = recv_Body[4]
                    parentUserName = recv_Body[5:5+parentUserLen]
                    print '--- parentUserName --- :',parentUserName
                    print u'中心节点用户名: ',int_list_str(parentUserName)
                    parentUserType = recv_Body[5+parentUserLen]
                    print u'父节点用户类型：',parentUserType
                    parentUserId = recv_Body[6+parentUserLen:14+parentUserLen]
                    print u'父节点userID: ',parentUserId
                    recv_auth_keyID = recv_Body[14+parentUserLen:30+parentUserLen]
                    print u'认证密钥ID：',recv_auth_keyID
                    recv_auth_key = recv_Body[30+parentUserLen:62+parentUserLen]
                    print u'认证密钥值：',recv_auth_key
                    recv_session_keyID = recv_Body[62+parentUserLen:78+parentUserLen]
                    recv_session_key = recv_Body[78+parentUserLen:110+parentUserLen]
                else:
                    print u'------------这是外部设备------'
                    recv_auth_keyID = recv_Body[4:20]
                    print u'--182--外部设备-认证密钥ID：',recv_auth_keyID
                    recv_auth_key = recv_Body[20:52]
                    print u'外部设备-认证密钥值：',recv_auth_key
                    recv_session_keyID = recv_Body[52:68]
                    recv_session_key = recv_Body[68:100]
        
                ack_encry_id = listXor(session_id, recv_session_keyID)         # 报文头中的加密密钥ID
                ack_encry_key = listXor(session_key, recv_session_key)      # 加密密钥
                self.sess_key_id=ack_encry_id
                self.sess_key=ack_encry_key
#                print u'协商会话密钥：',recv_session_key
                # 确认报文体
                # recvBody_req_id = [10,10]
                ackMesType = 103
                ackStatus = 0
                ackBody = [ackMesType] + recvBody_req_id + [ackStatus]
                ackBody_pack = pack_bin(ackBody)
                # AES encrypt
                ackBody_AES_pack = aes_encrypt(ack_encry_key, ackBody_pack)
        
                ack_encry_alg = 1       # 加密算法
                if ack_encry_alg == 1:
                    ack_mesLen = len(ackBody_AES_pack)   # 确认报文长度
#                    print 'confirm length: ',ack_mesLen
                    ackHead = [1,ack_encry_alg] + len2bit(ack_mesLen) + ack_encry_id
                    ackHead_pack = pack_bin(ackHead)
#                    print u'发送AES 加密接入认证缺人报文'
                    s.send(ackHead_pack + ackBody_AES_pack)
#                    while True:
#                    time.sleep(2)
#                        print 'ddddddddd'
                else:
                    ack_mesLen = len(ackBody_pack)
                    ackHead = [1,ack_encry_alg] + len2bit(ack_mesLen)
                    ackHead_pack =  pack_bin(ackHead)
#                    print u'发送明文接入认证反馈报文'
                    s.send(ackHead_pack + ackBody_pack)
                # print ackHead_pack + ackBody_AES_pack
            elif recv_Body[3] == 1:
                print u'状态位为 1，用户名或密码错误'
            elif recv_Body[3] == 2:
                print u'状态位为 2，认证密钥错误'
            else:
                print u'未知的错误'
        else:
            print '没有返回值'
        # time.sleep(10)
    
    def get_sess_key(self):
        #print 'sess key',self.sess_key
        return self.sess_key
    
    def get_sess_key_id(self):
        return self.sess_key_id