#!/usr/bin/python
# -*-coding:UTF-8-*- 
import sys
import binascii
import socket
import akmReqPacket,akmRcPacket
import adminPacket
from pip.locations import src_prefix
import time
BUFSIZE=1024

#应用密钥，根据传入的ip，username，user_typ,key_id，接入host，并申请应用密钥
#def getAkmKey(host_ip,user_name,user_typ,key_id,authid2): 
def getAkmKey(host_ip,user_name,user_typ,key_id): 
    host = host_ip
    BUFSIZE = 4096 
    port = 5530
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print '---line 110---Failed to create socket.Error code: '+ str(msg[0]) + ', Error message: ' + msg[1]
        sys.exit()
    print '---line 112--- Socket create'
    s.connect((host, port))    
    admin_packet=adminPacket.AdminPacket(user_name,user_typ,key_id)
    admin_packet.admin(s)
    ack_key=admin_packet.get_sess_key()
    ack_key_id=admin_packet.get_sess_key_id()
    print '******ack_key',ack_key
    #time.sleep(60)
    #generate part   
    req_packet=akmReqPacket.ReqPacket()
    req_packet.set_sess_key(ack_key)
    #req_packet.set_sess_key(ack_key)
    req_packet.set_sess_key_id(ack_key_id)
    #req_packet.set_sess_key_id(ack_key)
    req_packet.set_version(1)
    req_packet.set_encry_alg(1)
    
    #set req packet message   
    req_msg_typ=119
    req_reqid=60
    req_reserve=0
    req_key_typ=1
    req_save=1
    req_save_time=65535
    req_key_num=10
    req_key_len=32
    req_automatic=0
    req_auto_rate=0
    # set attend information to variable
    req_user_name=user_name
    req_attend_num=19
    req_attend_name_1='client_qh980'
    req_attend_name_2='client_qh981'
    req_attend_name_3='client_qh982'
    req_attend_name_4='client_qh983'
    req_attend_name_5='client_qh984'
    req_attend_name_6='client_qh985'
    req_attend_name_7='client_qh985'
    req_attend_name_8='client_qh987'
    req_attend_name_9='client_qh988'
    req_attend_name_10='client_qh989'
    req_attend_name_11='client_qh990'
    req_attend_name_12='client_qh991'
    req_attend_name_13='client_qh992'
    req_attend_name_14='client_qh993'
    req_attend_name_15='client_qh994'
    req_attend_name_16='client_qh995'
    req_attend_name_17='client_qh996'
    req_attend_name_18='client_qh997'
    req_attend_name_19='client_qh998'
    req_attend_name_20='client_qh999'
    # set sess information to variable
    req_sess_typ=1
    req_sess_attend_num=20
    req_sess_name='test'   
    #set data information
    req_packet.set_msg_typ(req_msg_typ)
    req_packet.set_req_id(req_reqid)
    req_packet.set_reserved(req_reserve)
    req_packet.set_key_typ(req_key_typ)
    req_packet.set_save(req_save)
    req_packet.set_save_time(req_save_time)
    req_packet.set_key_num(req_key_num)
    req_packet.set_key_len(req_key_len)
    req_packet.set_automatic(req_automatic)
    req_packet.set_auto_rate(req_auto_rate)
    # set username information
    req_packet.set_userName(req_user_name)
    req_packet.set_userName_len(len(req_user_name))
    #req_packet.set_userName_len(129)
    
    #set attend member information
    req_packet.set_attend_num(req_attend_num)
    req_packet.set_attend_name_1(req_attend_name_1)
    req_packet.set_attend_name_2(req_attend_name_2)
    req_packet.set_attend_name_3(req_attend_name_3)
    req_packet.set_attend_name_4(req_attend_name_4)
    req_packet.set_attend_name_5(req_attend_name_5)
    req_packet.set_attend_name_6(req_attend_name_6)
    req_packet.set_attend_name_7(req_attend_name_7)
    req_packet.set_attend_name_8(req_attend_name_8)
    req_packet.set_attend_name_9(req_attend_name_9)
    req_packet.set_attend_name_10(req_attend_name_10)
    req_packet.set_attend_name_11(req_attend_name_11)
    req_packet.set_attend_name_12(req_attend_name_12)
    req_packet.set_attend_name_13(req_attend_name_13)
    req_packet.set_attend_name_14(req_attend_name_14)
    req_packet.set_attend_name_15(req_attend_name_15)
    req_packet.set_attend_name_16(req_attend_name_16)
    req_packet.set_attend_name_17(req_attend_name_17)
    req_packet.set_attend_name_18(req_attend_name_18)
    req_packet.set_attend_name_19(req_attend_name_19)
    req_packet.set_attend_name_20(req_attend_name_20)            
    #set attend name length
    req_packet.set_attend_name_len_1(len(req_attend_name_1))
    req_packet.set_attend_name_len_2(len(req_attend_name_2))
    req_packet.set_attend_name_len_3(len(req_attend_name_3))
    req_packet.set_attend_name_len_4(len(req_attend_name_4))
    req_packet.set_attend_name_len_5(len(req_attend_name_5))
    req_packet.set_attend_name_len_6(len(req_attend_name_6))
    req_packet.set_attend_name_len_7(len(req_attend_name_7))
    req_packet.set_attend_name_len_8(len(req_attend_name_8))
    req_packet.set_attend_name_len_9(len(req_attend_name_9))
    req_packet.set_attend_name_len_10(len(req_attend_name_10))
    req_packet.set_attend_name_len_11(len(req_attend_name_11))
    req_packet.set_attend_name_len_12(len(req_attend_name_12))
    req_packet.set_attend_name_len_13(len(req_attend_name_13))
    req_packet.set_attend_name_len_14(len(req_attend_name_14))
    req_packet.set_attend_name_len_15(len(req_attend_name_15))
    req_packet.set_attend_name_len_16(len(req_attend_name_16))
    req_packet.set_attend_name_len_17(len(req_attend_name_17))
    req_packet.set_attend_name_len_18(len(req_attend_name_18))
    req_packet.set_attend_name_len_19(len(req_attend_name_19))
    req_packet.set_attend_name_len_20(len(req_attend_name_20))                
    # set session information
    req_packet.set_sess_typ(req_sess_typ)
    req_packet.set_sess_attend_num(req_sess_attend_num)
    req_packet.set_sess_name(req_sess_name)
    req_packet.set_sess_name_len(len(req_sess_name))
    #req_packet.set_sess_name_len(0)

    req_packet_pack=req_packet.get_packet()
    print '****************',req_packet_pack
    s.send(req_packet_pack)
    s.settimeout(20)
    
    print 'send success'
    
    try: 
        while True:
            #print 'in while receive rc_packet'
            data = s.recv(BUFSIZE)
            print '--recive rc_packet data: ',data
            print '--recive rc_packet data: ',len(data)
            
            if len(data) >= 8:
                break 
    except socket.error, e:
        print "Error receive data: %s" %e
        sys.exit(1)
    print '*********Data',binascii.hexlify(data)
    
    recvData=data
    rc_packet=akmRcPacket.RecvPacket()
    rc_packet.set_sess_key(ack_key)
    rc_packet.unpack(recvData)
    rc_status=rc_packet.getResult()
    print 'rc_status',rc_status
    
    
    
    
    
    if rc_status==0:      
        rc_msg_typ=rc_packet.get_msg_typ()
        rc_req_id=rc_packet.get_req_id()
        rc_sess_id=rc_packet.get_sess_id()
        rc_key_num=rc_packet.get_key_num()
        rc_key_len=rc_packet.get_key_len()
        rc_key_id_list=rc_packet.get_key_id_list()
        rc_key_list=rc_packet.get_key_list()
        print 'rc_key_id_list',rc_key_id_list
        print 'rc_key_list',rc_key_list
        print 'rc_msg_typ',rc_msg_typ
        print 'rc_req_id',rc_req_id 
        
        
        return   rc_key_id_list   
        
    
        if (rc_msg_typ == 120  and  rc_req_id == req_reqid):
            print '*****req success***** and status is：申请创建应用密钥反馈报文 ',rc_status         
        else:
            '#-------------something is not same with recvData-----------------------#'   
    else:
        print '*****req failed***** and status is ',rc_status
    s.close()
        
#应用密钥，根据传入的ip，username，user_typ,key_id，接入host，并获取应用密钥
def obtAkmKey(host_ip,user_name,user_typ,key_id,key_id_list): 
    host = host_ip
    BUFSIZE = 4096 
    port = 5530
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print '---line 110---Failed to create socket.Error code: '+ str(msg[0]) + ', Error message: ' + msg[1]
        sys.exit()
    print '---line 112--- Socket create'
    s.connect((host, port))    
    admin_packet=adminPacket.AdminPacket(user_name,user_typ,key_id)
    admin_packet.admin(s)
    ack_key=admin_packet.get_sess_key()
    ack_key_id=admin_packet.get_sess_key_id()
    print '******ack_key',ack_key 
    #time.sleep(60)
    
    req_packet=akmReqPacket.ObtReqPacket()
    #req_packet.set_sess_key(ack_key)
    req_packet.set_sess_key(ack_key)
    #req_packet.set_sess_key_id(ack_key_id)
    req_packet.set_sess_key_id(ack_key_id)
    req_packet.set_version(1)
    req_packet.set_encry_alg(1)
    
    #set req packet message   
    req_msg_typ=121
    req_reqid=61
    req_key_num=1
    req_key_len=32
    req_user_name=user_name
    print 'req_user_name:',req_user_name
    req_user_name_len=len(req_user_name)
    print 'req_user_name_len:',req_user_name_len
    #req_user_name_len=128
    #print 'req_user_name_len+10:',req_user_name_len
#    req_key_id_list=[133, 120, 24, 243, 87, 167, 75, 78, 142, 187, 35, 240, 232, 237, 72, 111]
    #req_key_id_list=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    #req_key_id_list=''
    req_key_id_list=key_id_list  #申请获取应用密钥反馈报文中带的keyid
    
    req_packet.set_msg_typ(req_msg_typ)
    req_packet.set_req_id(req_reqid)
    req_packet.set_key_num(req_key_num)
    req_packet.set_key_len(req_key_len)
    req_packet.set_userName(req_user_name)
    req_packet.set_userName_len(req_user_name_len)
    req_packet.set_key_id_list(req_key_id_list)
    print '-------------------------------------------------------------------',req_key_id_list
  
    req_packet_pack=req_packet.get_packet()
    print '****************',binascii.hexlify(req_packet_pack)
    s.send(req_packet_pack)
    s.settimeout(20)
    
    print 'send success'
#    time.sleep(10)    
    try: 
        while True:
            print 'in while receive rc_packet'
            data = s.recv(BUFSIZE)
            print '--recive rc_packet data: ',data
            print '--recive rc_packet data: ',len(data)
            
            if len(data) >= 8:
                break 
    except socket.error, e:
        print "Error receive data: %s" %e
        sys.exit(1)
    print '*********Data',binascii.hexlify(data)
    
    recvData=data
    rc_packet=akmRcPacket.ObtRecvPacket()
    rc_packet.set_sess_key(ack_key)
    rc_packet.unpack(recvData)
    rc_status=rc_packet.getResult()
    print 'rc_status',rc_status
#    
#    
    
    
    if rc_status==0:      
        rc_msg_typ=rc_packet.get_msg_typ()
        rc_req_id=rc_packet.get_req_id()
        rc_key_num=rc_packet.get_key_num()
        rc_key_len=rc_packet.get_key_len()
        rc_key_id_list=rc_packet.get_key_id_list()
        rc_key_list=rc_packet.get_key_list()
        print 'rc_key_id_list',rc_key_id_list
        print 'rc_key_list',rc_key_list
        print 'rc_msg_typ',rc_msg_typ
        print 'rc_req_id1',rc_req_id      
        if (rc_msg_typ == 122  and  rc_req_id == req_reqid):
#            return 1
            print '*****req success***** and status is:申请获取应用密钥 ',rc_status
            return 1
          
        else:
            '#-------------something is not same with recvData-----------------------#'
    
    else:
        print '*****req failed***** and status is ',rc_status
    s.close()
        


#修改应用密钥报文，根据传入的ip，username，user_typ,key_id，接入host，并修改应用密钥
def ModAkmKey(host_ip,user_name,user_typ,key_id): 
    host = host_ip
    BUFSIZE = 4096 
    port = 5530
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print '---line 110---Failed to create socket.Error code: '+ str(msg[0]) + ', Error message: ' + msg[1]
        sys.exit()
    print '---line 112--- Socket create'
    s.connect((host, port))    
    admin_packet=adminPacket.AdminPacket(user_name,user_typ,key_id)
    admin_packet.admin(s)
    ack_key=admin_packet.get_sess_key()
    ack_key_id=admin_packet.get_sess_key_id()
    print '******ack_key',ack_key
    #time.sleep(60)
    #generate part   
    rc_packet=akmReqPacket.ModReqPacket()
    rc_packet.set_sess_key(ack_key)
    rc_packet.set_sess_key_id(ack_key_id)
    rc_packet.set_version(1)
    rc_packet.set_encry_alg(1)
    
    #set req packet message   
    rc_msg_typ=123
    rc_reqid=60
    rc_modify_typ=1
    rc_sess_id=[180, 72, 74, 212, 192, 124, 67, 214, 133, 90, 244, 177, 21, 218, 33, 112]    #申请创建应用密钥反馈报文的Session ID
    # set attend information to variable
    rc_user_name='client_lq3'
    rc_attend_num=1
    rc_attend_name_1='client_lq4'
    rc_attend_name_2='client_lq4'
    rc_attend_name_3='node_child'
    rc_attend_name_4='node_child'
    rc_attend_name_5='node_child' 
    #set data information
    rc_packet.set_msg_typ(rc_msg_typ)
    rc_packet.set_req_id(rc_reqid)
    rc_packet.set_modify_typ(rc_modify_typ)
    rc_packet.set_sess_id(rc_sess_id)
    # set username information
    #req_packet.set_userName(req_user_name)
    #req_packet.set_userName_len(len(req_user_name))
    
    #set attend member information
    rc_packet.set_attend_num(rc_attend_num)
    rc_packet.set_attend_name_1(rc_attend_name_1)
    rc_packet.set_attend_name_2(rc_attend_name_2)
    rc_packet.set_attend_name_3(rc_attend_name_3)
    rc_packet.set_attend_name_4(rc_attend_name_4)
    rc_packet.set_attend_name_5(rc_attend_name_5)
    #set attend name length
    rc_packet.set_attend_name_len_1(len(rc_attend_name_1))
    rc_packet.set_attend_name_len_2(len(rc_attend_name_2))
    rc_packet.set_attend_name_len_3(len(rc_attend_name_3))
    rc_packet.set_attend_name_len_4(len(rc_attend_name_4))
    rc_packet.set_attend_name_len_5(len(rc_attend_name_5))

    rc_packet_pack=rc_packet.get_packet()
    print '****************',rc_packet_pack
    s.send(rc_packet_pack)
    s.settimeout(20)
    
    print 'send success'
 
    
    try: 
        while True: 
            data = s.recv(BUFSIZE)
            print '--recive rc_packet data: ',data
            print '--recive rc_packet data: ',len(data)
            
            if len(data) >= 8:
                break 
    except socket.error, e:
        print "Error receive data: %s" %e
        sys.exit(1)
    print '*********Data',binascii.hexlify(data)
    
    recvData=data
    rc_packet=akmRcPacket.ModifyRecvPacket()
    rc_packet.set_sess_key(ack_key)
    rc_packet.unpack(recvData)
    rc_status=rc_packet.getResult()
    print 'rc_status',rc_status
    if rc_status==0:      
        rc_msg_typ=rc_packet.get_msg_typ()
        rc_req_id=rc_packet.get_req_id()
        rc_sess_id=rc_packet.get_sess_id()
        rc_key_num=rc_packet.get_key_num()
        rc_key_len=rc_packet.get_key_len()
        rc_key_id_list=rc_packet.get_key_id_list()
        rc_key_list=rc_packet.get_key_list()
        print 'rc_key_id_list',rc_key_id_list
        print 'rc_key_list',rc_key_list
        print 'rc_msg_typ',rc_msg_typ
        print 'rc_req_id',rc_req_id      
        if (1):
            print '*****req success***** and rc_status is： ',rc_status         
        else:
            '#-------------something is not same with recvData-----------------------#'   
    else:
        print '*****req failed***** and rc_status is ',rc_status
    s.close()    
        
        
        
        
        
        
        