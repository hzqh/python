#!/usr/bin/python
# -*-coding:UTF-8-*- 
import struct
import sys
import binascii
import ctypes
import socket
import time
import hashlib
import hmac
import random
import array
from email.base64mime import body_decode
from Crypto.Cipher import AES
import reqPacket,rcPacket,ackPacket
import tools
import adminPacket
import datetime,time
import ConfigParser

class Qkmget():
    def start(self):
         
        cf = ConfigParser.ConfigParser()
        cf.read('D:/workplace/PyTest-frame/qtec.conf')   
        host = eval(cf.get('node-qkms', 'host')) 
        BUFSIZE = eval(cf.get('node-child', 'BUFSIZE')) 
        port = eval(cf.get('node-child', 'port'))
        UserName = eval(cf.get('client1', 'UserName'))
        UserTyp= eval(cf.get('usertyp', 'UserTyp1'))
        KeyID =  eval(cf.get('client1', 'KeyID'))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print '---line 110---Failed to create socket.Error code: '+ str(msg[0]) + ', Error message: ' + msg[1]
            sys.exit()
        print '---line 112--- Socket create'
        s.connect((host, port))    
        admin_packet=adminPacket.AdminPacket()
        admin_packet.admin(s)
        ack_key=admin_packet.get_sess_key()
        ack_key_id=admin_packet.get_sess_key_id()
        print '******ack_key',ack_key
        #time.sleep(300)
        #generate part   
        req_packet=reqPacket.ReqPacket()
        req_packet.set_sess_key(ack_key)
        req_packet.set_sess_key_id(ack_key_id)
        req_packet.set_version(1)
        req_packet.set_encry_alg(1)
        req_packet.set_msg_typ(125)
        #set req packet message
        req_user_name = UserName
        req_reqid=205
        req_get_typ=1
        req_key_typ=0
        req_key_num=10
        req_key_len=32
        req_key_id_list=[]
        peer_name_1=eval(cf.get('peerlist', 'peer_name_1'))
        peer_name_2=eval(cf.get('peerlist', 'peer_name_2'))
        peer_name_3=eval(cf.get('peerlist', 'peer_name_3'))
        peer_name_4=eval(cf.get('peerlist', 'peer_name_4'))
        peer_name_5=eval(cf.get('peerlist', 'peer_name_5'))
        peer_name_6=eval(cf.get('peerlist', 'peer_name_6'))
        peer_name_7=eval(cf.get('peerlist', 'peer_name_7'))
        peer_name_8=eval(cf.get('peerlist', 'peer_name_8'))
        peer_name_9=eval(cf.get('peerlist', 'peer_name_9'))
        peer_name_10=eval(cf.get('peerlist', 'peer_name_10'))
        req_specified=0
        peer_num=10
           
        req_packet.set_req_id(req_reqid)
        req_packet.set_get_typ(req_get_typ)
        req_packet.set_key_typ(req_key_typ)
        req_packet.set_key_num(req_key_num)
        req_packet.set_key_len(req_key_len)
        req_packet.set_specified(req_specified)
        req_packet.set_userName(req_user_name)
        req_packet.set_userName_len(len(req_user_name))
        req_packet.set_key_id_list(req_key_id_list)
        req_packet.set_reserved1(0)
        req_packet.set_reserved2(0)
        req_packet.set_peer_num(peer_num)
        req_packet.set_peer_name_1(peer_name_1)
        req_packet.set_peer_len_1(len(peer_name_1))
        req_packet.set_peer_name_2(peer_name_2)
        req_packet.set_peer_len_2(len(peer_name_2))
        req_packet.set_peer_name_3(peer_name_3)
        req_packet.set_peer_len_3(len(peer_name_3))
        req_packet.set_peer_name_4(peer_name_4)
        req_packet.set_peer_len_4(len(peer_name_4))
        req_packet.set_peer_name_5(peer_name_5)
        req_packet.set_peer_len_5(len(peer_name_5))
        req_packet.set_peer_name_6(peer_name_6)
        req_packet.set_peer_len_6(len(peer_name_6))
        req_packet.set_peer_name_7(peer_name_7)
        req_packet.set_peer_len_7(len(peer_name_7))
        req_packet.set_peer_name_8(peer_name_8)
        req_packet.set_peer_len_8(len(peer_name_8))
        req_packet.set_peer_name_9(peer_name_9)
        req_packet.set_peer_len_9(len(peer_name_9))
        req_packet.set_peer_name_10(peer_name_10)
        req_packet.set_peer_len_10(len(peer_name_10))
     
        req_packet_pack=req_packet.get_packet()
        print '****************',req_packet_pack
        s.send(req_packet_pack)
        s.settimeout(20)
        print'************  Request Packet *************'
        print'Request ID= ',req_reqid
        print'Get Type= ',req_get_typ
        print'Key Type=',req_key_typ
        print'Key Number=',req_key_num
        print'Key Length=',req_key_len
        print'Specified= ',req_specified
        print'User Name Length= ',len(req_user_name)
        print'User Name= ',req_user_name
        print'Key ID List= ',req_key_id_list
        print'************ End *************'
        
#        try: 
#            while True:
#                print 'in while receive rc_packet'
#                data = s.recv(BUFSIZE)
#                print '--recive rc_packet data: ',data
#                print '--recive rc_packet data: ',len(data)
#                
#                if len(data) >= 8:
#                    break 
#        except socket.error, e:
#            print "Error receive data: %s" %e
#            sys.exit(1)
#        print '*********Data',binascii.hexlify(data)
#        recvData=data
#        rc_packet=rcPacket.RecvPacket()
#        rc_packet.set_sess_key(ack_key)
#        rc_packet.unpack(recvData)
#        rc_status=rc_packet.getResult()
#        print 'rc_status',rc_status

        try: 
            while True:
                print 'in while receive rc_packet1'
    #            rc_msg_typ=rc_packet.get_msg_typ()
                data = s.recv(BUFSIZE)
                recvData=data
                rc_packet=rcPacket.RecvPacket()
                rc_packet.set_sess_key(ack_key)
                while len(recvData) != 532:                
                    s.send(req_packet_pack)
                    s.settimeout(20)                                
                    try:                     
                        while True:                       
                            data = s.recv(BUFSIZE)
                            recvData=data
                            rc_packet=rcPacket.RecvPacket()
                            rc_packet.set_sess_key(ack_key)
    #                        print '--recive rc_packet data: ',data
    #                        print '--recive rc_packet data: ',len(data)                
                            if len(data) >= 8:                                                      
                                break 
                    except Exception, e:
                        print "Error receive data1: %s" %e,Exception
                        sys.exit(1) 
                rc_packet.unpack(recvData)                                                                     
                rc_msg_typ=rc_packet.get_msg_typ()
                if rc_msg_typ != 126:                
                    print '-----其他报文类型-----',rc_msg_typ
                    break
                print '--recive rc_packet data1: ',data
                print '--recive rc_packet data1: ',len(data)
    #            if len(data)==0:
    #                break                        
                if len(data) >= 8:
                    break 
        except socket.error, e:
            print "Error receive data: %s" %e
            sys.exit(1)
    #    print '*********Data',binascii.hexlify(data)
    #    recvData=data
    #    rc_packet=rcPacket.RecvPacket()
    #    rc_packet.set_sess_key(ack_key)
    #    rc_packet.unpack(recvData)
        rc_status=rc_packet.getResult()
        if rc_status==0:      
            rc_key_id_list=rc_packet.get_key_id_list()
            rc_msg_typ=rc_packet.get_msg_typ()
            rc_req_id=rc_packet.get_req_id()
            rc_key_typ=rc_packet.get_key_typ()
            rc_key_num=rc_packet.get_key_num()
            rc_key_len=rc_packet.get_key_len()
            rc_get_typ=rc_packet.get_get_typ()
            rc_userName_len=rc_packet.get_userName_len()
            rc_userName=rc_packet.get_userName()
            rc_key_id_list=rc_packet.get_key_id_list()
            rc_key_list=rc_packet.get_key_list()
            print'************  Response Packet *************'
            print 'Message Type= ',rc_msg_typ
            print 'Request ID= ',rc_req_id
            print 'Status= ',rc_status
            print 'Key Type= ', rc_key_typ
            print 'Key Number= ',rc_key_num
            print 'Key Length= ',rc_key_len
            print 'UserName length= ',rc_userName_len
            print 'UserName= ',rc_userName
            print 'Key ID List= ',rc_key_id_list
            print 'Key List= ',rc_key_list
            print'************  Response End *************'
            
            if (rc_msg_typ == 126 and  rc_req_id == req_reqid and rc_key_typ == req_key_typ and  rc_key_num == req_key_num and rc_key_len == req_key_len and rc_get_typ == req_get_typ ):
                print '*****req success***** and status is ',rc_status
                ack_packet=ackPacket.AckPacket()
                ack_packet.set_sess_key(ack_key)
                ack_packet.set_sess_key_id(ack_key_id)
                ack_packet.set_msg_typ(129)
                ack_packet.set_req_id(req_reqid)
                ack_packet.set_status(0)
                ack_packet.set_key_typ(req_key_typ)
                ack_packet.set_key_num(req_key_num)
                ack_packet.set_key_len(req_key_len)
                ack_packet.set_get_typ(req_get_typ)
                ack_packet.set_key_id_list(rc_key_id_list)
                ack_packet_pack=ack_packet.get_packet()
                print '****************',ack_packet_pack
                s.send(ack_packet_pack)
                print'************  ACK Packet *************'
                print'Request ID= ',req_reqid
                print'Get Type= ',req_get_typ
                print'Key Type=',req_key_typ
                print'Key Number=',req_key_num
                print'Key Length=',req_key_len
                print'Specified= ',req_specified
                print'User Name Length= ',len(req_user_name)
                print'User Name= ',req_user_name
                print'Key ID List= ',rc_key_id_list
                print'************ End *************'
                print '*****ack success***** '
            else:
                print'failed'
        else:
            print '*****req failed***** and status is ',rc_status
            
            
            
            
        req_packet.set_req_id(req_reqid+1)   
        req_packet.set_get_typ(1)
        req_packet.set_specified(1)
        req_packet.set_key_id_list(rc_key_id_list)
        req_packet_pack=req_packet.get_packet()
        s.send(req_packet_pack)
        s.settimeout(20)
        print'************  Request Packet -2 *************'
        print'Request ID= ',req_reqid+1
        print'Get Type= ',req_get_typ
        print'Key Type=',req_key_typ
        print'Key Number=',req_key_num
        print'Key Length=',req_key_len
        print'Specified= ',req_specified
        print'User Name Length= ',len(req_user_name)
        print'User Name= ',req_user_name
        print'Key ID List= ',rc_key_id_list
        print'************ End *************'
#        try: 
#            while True:
#                print 'in while receive rc_packet'
#                data = s.recv(BUFSIZE)
#                print '--recive rc_packet data: ',data
#                print '--recive rc_packet data: ',len(data)
#                 
#                if len(data) >= 8:
#                    break 
#        except socket.error, e:
#            print "Error receive data: %s" %e
#            sys.exit(1)
#        print '*********Data',binascii.hexlify(data)
#        recvData=data
#        rc_packet=rcPacket.RecvPacket()
#        rc_packet.set_sess_key(ack_key)
#        rc_packet.unpack(recvData)
#        rc_status=rc_packet.getResult()
#        print 'rc_status',rc_status

        try: 
            while True:
                print 'in while receive rc_packet1'
    #            rc_msg_typ=rc_packet.get_msg_typ()
                data = s.recv(BUFSIZE)
                recvData=data
                rc_packet=rcPacket.RecvPacket()
                rc_packet.set_sess_key(ack_key)
                while len(recvData) != 532:                
                    s.send(req_packet_pack)
                    s.settimeout(20)                                
                    try:                     
                        while True:                       
                            data = s.recv(BUFSIZE)
                            recvData=data
                            rc_packet=rcPacket.RecvPacket()
                            rc_packet.set_sess_key(ack_key)
    #                        print '--recive rc_packet data: ',data
    #                        print '--recive rc_packet data: ',len(data)                
                            if len(data) >= 8:                                                      
                                break 
                    except Exception, e:
                        print "Error receive data1: %s" %e,Exception
                        sys.exit(1) 
                rc_packet.unpack(recvData)                                                                     
                rc_msg_typ=rc_packet.get_msg_typ()
                if rc_msg_typ != 126:                
                    print '-----其他报文类型-----',rc_msg_typ
                    break
                print '--recive rc_packet data1: ',data
                print '--recive rc_packet data1: ',len(data)
    #            if len(data)==0:
    #                break                        
                if len(data) >= 8:
                    break 
        except socket.error, e:
            print "Error receive data: %s" %e
            sys.exit(1)
    #    print '*********Data',binascii.hexlify(data)
    #    recvData=data
    #    rc_packet=rcPacket.RecvPacket()
    #    rc_packet.set_sess_key(ack_key)
    #    rc_packet.unpack(recvData)
        rc_status=rc_packet.getResult()
        if rc_status==0:      
            rc_key_id_list=rc_packet.get_key_id_list()
            rc_msg_typ=rc_packet.get_msg_typ()
            rc_req_id=rc_packet.get_req_id()
            rc_key_typ=rc_packet.get_key_typ()
            rc_key_num=rc_packet.get_key_num()
            rc_key_len=rc_packet.get_key_len()
            rc_get_typ=rc_packet.get_get_typ()
            rc_userName_len=rc_packet.get_userName_len()
            rc_userName=rc_packet.get_userName()
            rc_key_id_list=rc_packet.get_key_id_list()
            rc_key_list=rc_packet.get_key_list()
            print'************  Response Packet -2*************'
            print 'Message Type= ',rc_msg_typ
            print 'Request ID= ',rc_req_id
            print 'Status= ',rc_status
            print 'Get Type= ', rc_get_typ
            print 'Key Number= ',rc_key_num
            print 'Key Length= ',rc_key_len
            print 'UserName length= ',rc_userName_len
            print 'UserName= ',rc_userName
            print 'Key ID List= ',rc_key_id_list
            print 'Key List= ',rc_key_list
            print'************  Response End *************'
            #  
             
            if (rc_msg_typ == 126 and rc_req_id == req_reqid+1 and rc_key_typ == req_key_typ and  rc_key_num == req_key_num and rc_key_len == req_key_len and rc_get_typ == 1 ):
                print '*****req success***** and status is ',rc_status
                ack_packet=ackPacket.AckPacket()
                ack_packet.set_sess_key(ack_key)
                ack_packet.set_sess_key_id(ack_key_id)
                ack_packet.set_msg_typ(129)
                ack_packet.set_req_id(req_reqid+1)
                ack_packet.set_status(0)
                ack_packet.set_key_typ(req_key_typ)
                ack_packet.set_key_num(req_key_num)
                ack_packet.set_key_len(req_key_len)
                ack_packet.set_get_typ(req_get_typ)
                ack_packet.set_key_id_list(rc_key_id_list)
                ack_packet_pack=ack_packet.get_packet()
                print '****************',ack_packet_pack
                s.send(ack_packet_pack)
                print'************  ACK Packet -2*************'
                print'Request ID= ',req_reqid+1
                print'Get Type= ',req_get_typ
                print'Key Type=',req_key_typ
                print'Key Number=',req_key_num
                print'Key Length=',req_key_len
                print'Specified= ',req_specified
                print'User Name Length= ',len(req_user_name)
                print'User Name= ',req_user_name
                print'Key ID List= ',rc_key_id_list
                print'************ End *************'
                print '*****ack success***** '
                return 1
            else:
                print'failed'
        else:
            print '*****req failed***** and status is ',rc_status
         
         