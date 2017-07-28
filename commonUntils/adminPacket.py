#!/usr/bin/python
# -*-coding:UTF-8-*- 
# This is for AES Encryption Algorithm
import socket
import sys #for exit
import time
import struct
import hashlib
import binascii
import hmac
import random


#from tools import tools
# import array
from Crypto.Cipher import AES
import string
import socketUntil
BUFSIZE = 1024 
# �����������
def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list 
# ������
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
    iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]           # 16��0���������
    aes_object = AES.new(pack_bin(key), AES.MODE_CBC, pack_bin(iv))         # AES ��������
    return aes_object.encrypt(pad(data))
def hmac_sha256(key, req):
    # print '__algorithm__ :  hmac_sha256 '
    hmac256 = hmac.new(pack_bin(key), pack_bin(req), digestmod=hashlib.sha256).digest()
    return hmac256
def psd_sha256(psd):
    psd_sha256_hex = hashlib.sha256(psd).hexdigest()
    return binascii.unhexlify(psd_sha256_hex)
def hex2arr(hex):
    list = []
    while len(hex) > 1:
        list.append(int(hex[0:2],16))
        hex = hex[2:len(hex)]
    return list

#  AES CBC PKCS7padding
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
unpad = lambda s : s[0:-ord(s[-1])]
#global userName

class AdminPacket(object):
    def __init__(self,userName,userTyp,key_id):
        #packet header constractor
        self.version=1
        self.encry_alg=1
#        self.key_id=hex2arr(key_id)
        self.key_id = key_id
        self.sess_key=''
        self.sess_key_id=''
        self.userType_flag = userTyp
        self.userName = userName
    
    def admin(self,s,authid):
        req_id = random_int_list(0, 255, 2)                # Request ID 2�ֽ�
        print 'first request id : ', req_id       
        user = self.userName                       # �û���
        userLen = len(user)
        psd='node_child'                            # �û������� 10
    
        # ����
        psdSHA256 = psd_sha256(psd)
        psdBin = [ord(x) for x in psdSHA256]   #����x��һ��ascii�ַ������ض�Ӧ��ʮ��������
        psdLen = len(psdBin)                            # ���볤��
        
        body = [101] + req_id + [userLen, user, psdLen]
        
        auth_id = authid              # ��֤��ԿID 16�ֽ�
#        auth_id = [01,01,01,01,01,01,01,01,01,01,01,01,01,07,01,20]
        authKey = [01] * 32             # ��֤��Կ 32�ֽ�
        authKey_hmac256 = hmac_sha256(authKey, req_id)    # ��֤��ԿID HMAC-SHA256��ʽ����
        
        session = random_int_list(0, 255, 48)
        session_id = session[0:16]
        session_key = session[16:48]
        
        body_pack = struct.pack('@4B%dsB'%userLen, *body) + psdSHA256 + pack_bin(auth_id) + authKey_hmac256 + pack_bin(session)
        print '--- --  body_pack: ',len(body_pack)
        # AES ����
        Encryp_key = [01] * 32    # ������Կ
        body_AES_pack = aes_encrypt(Encryp_key, body_pack)
        # print '--117----AES pad after: ',len(body_AES_pack)
        # --------------------- ����ͷStart -------------------------- #
        # Version = 1 
        # Encryption Algorithm =  0 1:AES, 2: DES, 3: 3DES, 4: Blowfish
        # Message Length : mesLen = ���ݳ��� 
        # Encryption Key ID��Optional��: ������ԿID
        # ---------------------- ����ͷEnd --------------------------- #
        
        version = 1
        Encryp_Alg = 1            # ���ܷ�ʽ
        Encryp_id = self.key_id    # ������ԿID 16�ֽ�
        mesLen = len(body_AES_pack)
        head = [version, Encryp_Alg] + len2bit(mesLen)
        head_pack = struct.pack('@4B', *head) + pack_bin(Encryp_id)
        
        print '---131---AES length: ', len(head_pack + body_AES_pack)
        
        s.send(head_pack + body_AES_pack)            # ������
        
        # while True:
        #     recvData = s.recv(BUFSIZE)
        #     if not recvData:
        #         break
        #     if len(recvData) == 148 or len(recvData) == 8:
        #         break
        # print '---145---recive all data: ', recvData
#        recvData = s.recv(BUFSIZE)
        try: 
            while True:
                print 'in while receive rc_packet'
                recvData = s.recv(BUFSIZE)
                print '--recive rc_packet data: ',recvData
                print '--recive rc_packet data: ',len(recvData)
            
                if len(recvData) >= 8:
                    break 
        except socket.error, e:
            print "Error receive data: %s" %e
            sys.exit(1)
#        print '-------lendata----------------------------------------------------------------------------',len(recvData)#        recvData = socketUntil.RecvN(s, 30*BUFSIZE+14)
        # print '---145---recive all data: ',recvData
        print u'���յ��Ľ�����֤�������ģ�',len(recvData)
        # # ------------------ ����������ϢStart -------------------- #
        if len(recvData):
            if Encryp_Alg == 1:
                recvHead = recvData[0:20]           # ����Ϊ[0:20]
                recvBody = recvData[20:len(recvData)]
                # recvBody = aes_decrypt(Encryp_key, recvBody)
                recvBody = unpad(aes_decrypt(Encryp_key, recvBody))      # padding Or don't need 
            else:
                recvHead = recvData[0:4]           # ������Ϊ[0:4]
                recvBody = recvData[4:len(recvData)]
            recv_Body = unpack_list(recvBody)
            print u'������֤���������壺',recv_Body
        
            recvBody_req_id = recv_Body[1:3]        # Request ID
            print u'������֤��������ͷ-ǰ�ĸ���', recv_Body[0:4]
            
            if recv_Body[3] == 0:      # �ɹ�
                if self.userType_flag == 0:      # �ڲ��豸
                    print u'�����ڲ��豸------------'
                    parentUserLen = recv_Body[4]
                    parentUserName = recv_Body[5:5+parentUserLen]
                    print '--- parentUserName --- :',parentUserName
                    print u'���Ľڵ��û���: ',int_list_str(parentUserName)
                    parentUserType = recv_Body[5+parentUserLen]
                    print u'���ڵ��û����ͣ�',parentUserType
                    parentUserId = recv_Body[6+parentUserLen:14+parentUserLen]
                    print u'���ڵ�userID: ',parentUserId
                    recv_auth_keyID = recv_Body[14+parentUserLen:30+parentUserLen]
                    print u'��֤��ԿID��',recv_auth_keyID
                    recv_auth_key = recv_Body[30+parentUserLen:62+parentUserLen]
                    print u'��֤��Կֵ��',recv_auth_key
                    recv_session_keyID = recv_Body[62+parentUserLen:78+parentUserLen]
                    recv_session_key = recv_Body[78+parentUserLen:110+parentUserLen]
                else:
                    print u'------------�����ⲿ�豸------'
                    recv_auth_keyID = recv_Body[4:20]
                    print u'--182--�ⲿ�豸-��֤��ԿID��',recv_auth_keyID
                    recv_auth_key = recv_Body[20:52]
                    print u'�ⲿ�豸-��֤��Կֵ��',recv_auth_key
                    recv_session_keyID = recv_Body[52:68]
                    recv_session_key = recv_Body[68:100]
        
                ack_encry_id =  listXor(session_id, recv_session_keyID)         # ����ͷ�еļ�����ԿID
                ack_encry_key = listXor(session_key, recv_session_key)        # ������Կ
                self.sess_key_id=ack_encry_id
                self.sess_key=ack_encry_key
                print u'Э�̻Ự��Կ��',recv_session_key
                # ȷ�ϱ�����
                # recvBody_req_id = [10,10]
                ackMesType = 103
                ackStatus = 0
                ackBody = [ackMesType] + recvBody_req_id + [ackStatus]
                ackBody_pack = pack_bin(ackBody)
                # AES encrypt
                ackBody_AES_pack = aes_encrypt(ack_encry_key, ackBody_pack)
                
        
                ack_encry_alg = 1
                if ack_encry_alg == 1:
                    ack_mesLen = len(ackBody_AES_pack)   # 确认报文长度
#                    print 'confirm length: ',ack_mesLen
                    ackHead = [1,ack_encry_alg] + len2bit(ack_mesLen) + ack_encry_id
                    ackHead_pack = pack_bin(ackHead)
#                    print u'发送AES 加密接入认证缺人报文'
                    s.send(ackHead_pack + ackBody_AES_pack)
#                    print '---------client-----user--------------------------------------------------------------------------------',self.userName
                    print '---------client-----length--------------------------------------------------------------------------------',len(ackHead_pack + ackBody_AES_pack)
                    return 1
                    
                    
                    
                    
#                    while True:
#                    time.sleep(2)
#                        print 'ddddddddd'
                else:
                    ack_mesLen = len(ackBody_pack)
                    ackHead = [1,ack_encry_alg] + len2bit(ack_mesLen)
                    ackHead_pack =  pack_bin(ackHead)
#                    print u'发送明文接入认证反馈报文'
                    s.send(ackHead_pack + ackBody_pack)
                    
                    
             
                
                
#                ack_mesLen = len(ackBody_AES_pack)   # ȷ�ϱ��ĳ���
#                print 'confirm length: ',ack_mesLen
#                ackHead = [1,ack_encry_alg] + len2bit(ack_mesLen) + ack_encry_id
#                ackHead_pack = pack_bin(ackHead)
##                print u'����AES ���ܽ�����֤��������'
#                s.send(ackHead_pack + ackBody_AES_pack)
#                while True:
#                        print 'parent'
#                        time.sleep(30)
#
#                                                       
#                else:
#                    ack_mesLen = len(ackBody_pack)
#                    ackHead = [1,ack_encry_alg] + len2bit(ack_mesLen)
#                    ackHead_pack =  pack_bin(ackHead)
#                    print u'发送明文接入认证反馈报文'
#                    s.send(ackHead_pack + ackBody_pack)
#                
                # print ackHead_pack + ackBody_AES_pack
            elif recv_Body[3] == 1:
                print u'״recv_Body[3] == 1'
            elif recv_Body[3] == 2:
                print u'recv_Body[3] == 2'
            else:
                print u'recv_Body[3]'%recv_Body[3] == 2
        else:
            print 'no result'
        # time.sleep(10)
    
    def get_sess_key(self):
        #print 'sess key',self.sess_key
        return self.sess_key
    
    def get_sess_key_id(self):
        return self.sess_key_id