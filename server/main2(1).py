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
import reqPacket
import rcPacket
import ackPacket
import tools
import genPacket, rcGenPacket,adminPacket 
import datetime,time
BUFSIZE=1024



if __name__ == '__main__': 
    host = '192.168.91.183'
    hostID=1100000
    BUFSIZE = 1024 
    port = 5530
    #UserName='client_wm3'
    UserName='node_wm100'
    #UserID=1003000
    UserID=1100100
    UserTyp=0
    #KeyID=[01,01,01,01,01,01,01,01,01,01,01,01,01,01,00,03]
    KeyID='61626364653130300000000000000000'

    print 'KeyID',KeyID
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print '---line 110---Failed to create socket.Error code: '+ str(msg[0]) + ', Error message: ' + msg[1]
        sys.exit()
    print '---line 112--- Socket create'
    s.connect((host, port))    
    admin_packet=adminPacket.AdminPacket(UserName,UserTyp,KeyID)
    admin_packet.admin(s)
    ack_key=admin_packet.get_sess_key()
    ack_key_id=admin_packet.get_sess_key_id()
    print '******ack_key',ack_key
    time.sleep(60)
    #generate part   
    
def gen_sys_key(s,local_user_id,remote_user_id,ack_key,ack_key_id):
    
    UserID=local_user_id
    hostID=remote_user_id
    gen_packet=genPacket.GenPacket()
    gen_packet.set_version(1)
    gen_packet.set_encry_alg(1)
    gen_packet.set_key_num(16)
    gen_packet.set_msg_typ(201)
    gen_packet.set_req_id(10)
    gen_packet.set_reserved(1)
    gen_packet.set_key_typ(1)
    gen_packet.set_key_len(32)
    gen_packet.set_specified(1)
    gen_packet.set_local_user_id(UserID)
    gen_packet.set_remote_user_id(hostID)
   # gen_packet.set_local_user_id(local_user_id)
   # gen_packet.set_remote_user_id(remote_user_id

    gen_packet.set_sess_key(ack_key)
    gen_packet.set_sess_key_id(ack_key_id)
    packet_gen=gen_packet.get_packet(0)
    gen_local_user_id=gen_packet.get_local_user_id()
    gen_remote_user_id=gen_packet.get_remote_user_id()
    gen_key_id_list=gen_packet.get_key_id_list()  
    #print 'genPacket key_id_List',gen_key_id_list
    print 'genPacket local user id',UserID
    print 'genPacket remote user id',hostID
    #print 'gen packet msg_len',gen_packet.get_msg_len()
    s.send(packet_gen)
    #s.settimeout(20)
    
    try: 
        while True:
            #print 'in while receive rc_gen_packet'
            data = s.recv(BUFSIZE)
            #print '--recive rc_gen_packet data: '
            if not data:
                break
            if len(data) == 104 or len(data) >= 8:
                break 
    except socket.error, e:
        print "Error receive data: %s" %e
        sys.exit(1)
    #recvData = list(struct.unpack('!%dB'%len(data), data))
    recvData=data
    #print '--recive recvData: ',recvData
    rc_genPacket=rcGenPacket.RecvGenPacket()
    rc_genPacket.set_sess_key(ack_key)
    #recvData=rc_genPacket.data_decry_pack(recvData)
    rc_genPacket.unpack(recvData)
    rc_gen_res=rc_genPacket.getResult()
    print 'rc_gen_res',rc_gen_res
   
    if rc_gen_res==0:
        rc_gen_key_id_list=rc_genPacket.get_key_id_list()
        rc_gen_msg_typ=rc_genPacket.get_msg_typ()
        rc_gen_req_id=rc_genPacket.get_req_id()
        rc_gen_key_typ=rc_genPacket.get_key_typ()
        rc_gen_key_num=rc_genPacket.get_key_num()
        rc_gen_key_len=rc_genPacket.get_key_len()
        rc_gen_reserved=rc_genPacket.get_reserved()
        rc_gen_local_user_id=rc_genPacket.get_local_user_id()
        rc_gen_remote_user_id=rc_genPacket.get_remote_user_id()
        #print 'rc_genPacket result',rc_gen_res
        #print 'rc_genPacket msg_typ',rc_gen_msg_typ
        print 'rc_genPacket key_id_List',rc_gen_key_id_list
        #print 'rc_genPacket local peer id',rc_gen_local_user_id
        #print 'rc_genPacket remote peer id',rc_gen_remote_user_id
        if (cmp(rc_gen_key_id_list,gen_key_id_list) and rc_gen_msg_typ == 210 and  rc_gen_req_id == gen_packet.get_req_id() and rc_gen_key_typ == gen_packet.get_key_typ() \
            and  rc_gen_key_num == gen_packet.get_key_num()):
            if((rc_gen_local_user_id == gen_local_user_id) and (rc_gen_remote_user_id == gen_remote_user_id)):
                print '#---------------------success------------------------------------#'
            else:
                print'error user id'
                print 'rc_gen_local_user_id',rc_gen_local_user_id
                print 'gen_local_user_id',gen_local_user_id
                print 'rc_gen_remote_user_id',rc_gen_remote_user_id
                print 'gen_remote_user_id',gen_remote_user_id
        else:
            print '#-------------something is not same with gendata-----------------------#'
            sys.exit(1)
    elif rc_gen_res==1:
        dt = datetime.datetime.now()
        print dt.strftime("%Y%j%H%M%S"),'error part generate----#'
        sys.exit(1)
    elif rc_gen_res==2:
        dt = datetime.datetime.now()
        print dt.strftime("%Y%j%H%M%S"),'error generate failed---#' 
        sys.exit(1)
    else:
        dt = datetime.datetime.now()
        print dt.strftime("%Y%j%H%M%S"),'error unknow status %s is wrong...-------#'
        sys.exit(1)
 
    sys_packet=genPacket.GenPacket()
    sys_packet.set_version(1)
    sys_packet.set_encry_alg(1)
    sys_packet.set_key_num(16)
    sys_packet.set_msg_typ(202)
    sys_packet.set_req_id(10)
    sys_packet.set_reserved(0)
    sys_packet.set_key_typ(1)
    sys_packet.set_key_len(32)
    sys_packet.set_specified(1)
    sys_packet.set_local_user_id(UserID)
    sys_packet.set_remote_user_id(hostID)
    sys_packet.set_key_id_list(rc_gen_key_id_list)
    sys_packet.set_sess_key(ack_key)
    sys_packet.set_sess_key_id(ack_key_id)
    packet_sys=sys_packet.get_packet(1)
    s.send(packet_sys)
    s.settimeout(10)
    
    try: 
        while True:
            #print 'in while receive rc_gen_packet'
            data = s.recv(BUFSIZE)
            #print '--recive rc_gen_packet data: '
            if not data:
                break
            if len(data) == 104 or len(data) >= 8:
                break 
    except socket.error, e:
        print "Error receive data: %s" %e
        sys.exit(1)
    #recvData = list(struct.unpack('!%dB'%len(data), data))
    recvData=data
    #print '--recive recvData: ',recvData
    rc_sysPacket=rcGenPacket.RecvGenPacket()
    rc_sysPacket.set_sess_key(ack_key)
    #recvData=rc_sysPacket.data_decry_pack(recvData)
    rc_sysPacket.unpack(recvData)
    rc_sys_res=rc_sysPacket.getResult()
    print 'rc_sys_res',rc_sys_res
   
    if rc_sys_res==0:
        rc_sys_key_id_list=rc_sysPacket.get_key_id_list()
        rc_sys_msg_typ=rc_sysPacket.get_msg_typ()
        rc_sys_req_id=rc_sysPacket.get_req_id()
        rc_sys_key_typ=rc_sysPacket.get_key_typ()
        rc_sys_key_num=rc_sysPacket.get_key_num()
        rc_sys_key_len=rc_sysPacket.get_key_len()
        rc_sys_reserved=rc_sysPacket.get_reserved()
        rc_sys_local_user_id=rc_sysPacket.get_local_user_id()
        rc_sys_remote_user_id=rc_sysPacket.get_remote_user_id()
        #print 'rc_sysPacket result',rc_sys_res
        #print 'rc_sysPacket msg_typ',rc_sys_msg_typ
        #print 'rc_sysPacket key_id_List',rc_sys_key_id_list
        #print 'rc_sysPacket local peer id',rc_sys_local_user_id
        #print 'rc_sysPacket remote peer id',rc_sys_remote_user_id
        if (cmp(rc_sys_key_id_list,gen_key_id_list) and rc_sys_msg_typ == 220 and  rc_sys_req_id == gen_packet.get_req_id() and rc_sys_key_typ == gen_packet.get_key_typ() \
            and  rc_sys_key_num == gen_packet.get_key_num()):
            #print 'success'
            if((rc_sys_local_user_id == gen_local_user_id) and (rc_sys_remote_user_id == gen_remote_user_id)):
                print '#---------------------success------------------------------------#'
            else:
                print'error user id'
                print 'rc_sys_local_user_id',rc_sys_local_user_id
                print 'gen_local_user_id',gen_local_user_id
                print 'rc_sys_remote_user_id',rc_sys_remote_user_id
                print 'gen_remote_user_id',gen_remote_user_id
        else:
            print '#-------------something is not same with gendata-----------------------#'
            sys.exit(1)
    elif rc_sys_res==1:
        dt = datetime.datetime.now()
        print dt.strftime("%Y%j%H%M%S"),'error part generate----#'
        sys.exit(1)
    elif rc_sys_res==2:
        dt = datetime.datetime.now()
        print dt.strftime("%Y%j%H%M%S"),'error generate failed---#'
        sys.exit(1)
    else:
        dt = datetime.datetime.now()
        print dt.strftime("%Y%j%H%M%S"),'error unknow status %s is wrong...-------#'
        sys.exit(1)
    
    #and rc_sys_local_user_id == gen_packet.get_remote_user_id() and rc_sys_remote_user_id == \
    
    #cmp(rc_sys_local_user_id,gen_packet.get_local_user_id()) and cmp(rc_gen_remote_user_id,gen_packet.get_remote_user_id())
    
        
    
    