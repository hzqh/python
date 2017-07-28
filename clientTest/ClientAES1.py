#!/usr/bin/python
# -*- coding: utf8 -*-
# This is for AES Encryption Algorithm
#接入认证AT用例1，本地认证。1、父节点数据库插入子节点node_child的认证信息 2、父节点起realyserve 3、本地自动化代码向父节点发起认证请求
import socket
import sys #for exit
import time
import struct
import hashlib
import binascii
import hmac
import random
from tools import tools
import MySQLdb
# import array
from Crypto.Cipher import AES
import string
from commonUntils import DBConnection
import ConfigParser

class Clienttest1():
     
    def start(self):
        #  AES CBC PKCS7padding
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
        unpad = lambda s : s[0:-ord(s[-1])]
        
        cf = ConfigParser.ConfigParser()
        cf.read('D:/workplace/PyTest-frame/qtec.conf')   
        host = eval(cf.get('node-child', 'host')) 
        BUFSIZE = eval(cf.get('node-child', 'BUFSIZE')) 
        port = eval(cf.get('node-child', 'port'))
        KeyID =  eval(cf.get('client1', 'KeyID'))

#        conn = MySQLdb.connect(host='192.168.91.158',user='root',passwd='Qtec_KSM*',db='QkPool',port=3306,charset='utf8')
        conn = MySQLdb.connect(host=eval(cf.get('db1', 'host')),user=eval(cf.get('db1', 'user')),passwd=eval(cf.get('db1', 'passwd')),db=eval(cf.get('db1', 'db')),port=eval(cf.get('db1', 'port')),charset='utf8')
        cur = conn.cursor()
        hero = DBConnection.DBConn(eval(cf.get('db1', 'db')),conn,cur)        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        except socket.error, msg:
            print 'Failed to create socket. Error code:'+ str(msg[0]) + ', Error message: ' + msg[1]
            sys.exit()
        print 'Socket create'
        
        s.connect((host, port))
        # ---------------------认证报文体Start ---------------------- #
        # Message Type 			   MesType = 101
        # Request ID 				 reqId = 01,01
        # Username :		 		  user = 'node_child_p'
        # Username Length :	 	   userLen = len(user)
        # Password : 			  	   psd = 'node_child_parent'
        # Password Length :   		psdLen = len(psd)
        # Authentication Key’s ID  auth_id = 16 * 01
        # Authentication Key ：    authKey = 32 * 01
        # Session Key’s ID ： 	session_id = 16 * 01
        # Session Key ： 	   session_key = 32 * 01
        # --------------------- 认证报文体End ---------------------- #
        # while True:
        req_id = tools.random_int_list(0, 255, 2)				# Request ID 2字节
        print 'first request id : ', req_id
        user = eval(cf.get('client1', 'UserName')) 
        userLen = len(user)							# 用户名长度 10
        psd = 'node_child'						    # 密码
        psdSHA256 = tools.psd_sha256(psd)
        psdBin = [ord(x) for x in psdSHA256]
        psdLen = len(psdBin)							# 密码长度
        
        body = [101] + req_id + [userLen, user, psdLen]
        
        auth_id = [01] * 16			# 认证密钥ID 16字节
        authKey = [01] * 32             # 认证密钥 32字节
        authKey_hmac256 = tools.hmac_sha256(authKey, req_id)	# 认证密钥ID HMAC-SHA256方式加密
        
        session = tools.random_int_list(0, 255, 48)
        session_id = session[0:16]
        session_key = session[16:48]
        
        body_pack = struct.pack('@4B%dsB'%userLen, *body) + psdSHA256 + tools.pack_bin(auth_id) + authKey_hmac256 + tools.pack_bin(session)
        print '--- --  body_pack: ',len(body_pack)
        # AES 加密
        Encryp_key = [01] * 32	# 加密密钥
        body_AES_pack = tools.aes_encrypt(Encryp_key, body_pack)
        # print '--117----AES pad after: ',len(body_AES_pack)
        # --------------------- 报文头Start -------------------------- #
        # Version = 1 
        # Encryption Algorithm =  0 1:AES, 2: DES, 3: 3DES, 4: Blowfish
        # Message Length : mesLen = 数据长度 
        # Encryption Key ID（Optional）: 加密密钥ID
        # ---------------------- 报文头End --------------------------- #
        
        version = 1
        Encryp_Alg = 1			# 加密方式
#        Encryp_id = [01] * 16	# 加密密钥ID 16字节
        Encryp_id = KeyID
        mesLen = len(body_AES_pack)
        head = [version, Encryp_Alg] + tools.len2bit(mesLen)
        head_pack = struct.pack('@4B', *head) + tools.pack_bin(Encryp_id) if Encryp_Alg == 1 else struct.pack('@4B', *head)
        
        print '---131---AES length: ', len(head_pack + body_AES_pack)
        if Encryp_Alg == 1:
            print u'发送接入认证请求报文'
            s.send(head_pack + body_AES_pack)           # AES加密
        else:
            s.send(head_pack + body_pack)               # 不加密
        
        # while True:
        # 	recvData = s.recv(BUFSIZE)
        # 	if not recvData:
        # 		break
        # 	if len(recvData) == 148 or len(recvData) == 8:
        # 		break
        # print '---145---recive all data: ', recvData
        recvData = s.recv(BUFSIZE)
        # print '---145---recive all data: ',recvData
        print u'接收到的接入认证反馈报文：',len(recvData)
        # # ------------------ 反馈报文信息Start -------------------- #
        if len(recvData):
            if Encryp_Alg == 1:
                recvHead = recvData[0:20]           # 加密为[0:20]
                recvBody = recvData[20:len(recvData)]
                # recvBody = aes_decrypt(Encryp_key, recvBody)
                recvBody = unpad(tools.aes_decrypt(Encryp_key, recvBody))      # padding Or don't need 
            else:
                recvHead = recvData[0:4]           # 不加密为[0:4]
                recvBody = recvData[4:len(recvData)]
            recv_Body = tools.unpack_list(recvBody)
            print u'接入认证反馈报文体：',recv_Body
        
            recvBody_req_id = recv_Body[1:3]        # Request ID
            print u'接入认证反馈报文头-前四个：', recv_Body[0:4]
            if recv_Body[3] == 0:      # 成功且为内部设备
                if recv_Body[5] == 110:      # 内部设备
                    print u'这是内部设备------------'
                    parentUserLen = recv_Body[4]
                    parentUserName = recv_Body[5:5+parentUserLen]
                    print '--- parentUserName --- :',parentUserName
                    print u'中心节点用户名: ',tools.int_list_str(parentUserName)
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
        
                ack_encry_id = tools.listXor(session_id, recv_session_keyID)         # 报文头中的加密密钥ID
                ack_encry_key = tools.listXor(session_key, recv_session_key)      # 加密密钥
                print u'协商会话密钥：',recv_session_key
                # 确认报文体
                # recvBody_req_id = [10,10]
                print u'nihao-----------------------------',session_key
                print recv_session_key
                ackMesType = 103
                ackStatus = 0
                ackBody = [ackMesType] + recvBody_req_id + [ackStatus]
                ackBody_pack = tools.pack_bin(ackBody)
                # AES encrypt
                ackBody_AES_pack = tools.aes_encrypt(ack_encry_key, ackBody_pack)
        
                ack_encry_alg = 1       # 加密算法
                if ack_encry_alg == 1:
                    ack_mesLen = len(ackBody_AES_pack)   # 确认报文长度
                    print 'confirm length: ',ack_mesLen
                    ackHead = [1,ack_encry_alg] + tools.len2bit(ack_mesLen) + ack_encry_id
                    ackHead_pack = tools.pack_bin(ackHead)
                    print u'发送AES 加密接入认证反馈报文'
                    s.send(ackHead_pack + ackBody_AES_pack)
                    while True:
                        print 'parent'
                        time.sleep(0.5)
                        result = hero.select("select * from connection_info where user_name = "+"'client_qh001'")
#                        result = hero.selectname(user)
                        if result:
                            return 1
                        break
#                        time.sleep(10)                                            
                else:
                    ack_mesLen = len(ackBody_pack)
                    ackHead = [1,ack_encry_alg] + tools.len2bit(ack_mesLen)
                    ackHead_pack =  tools.pack_bin(ackHead)
                    print u'发送明文接入认证反馈报文'
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