#!/usr/bin/python
# -*-coding:UTF-8-*- 
import sys
import binascii
import socket
import qkmReqPacket,qkmRcPacket,qkmAckPacket
import adminPacket
import time


#量子密钥，根据传入的ip，username，user_typ,key_id，接入host，并申请量子密钥
def getQkmKey(host_ip,user_name,user_typ,key_id,authid1): 
    host = host_ip
    BUFSIZE = 1024 
    port = 5530
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print '---line 110---Failed to create socket.Error code: '+ str(msg[0]) + ', Error message: ' + msg[1]
        sys.exit()
    print '---line 112--- Socket create'
    s.connect((host, port))    
    #创建接入认证实例，需要传入用户名，用户类型和key_id
    admin_packet=adminPacket.AdminPacket(user_name,user_typ,key_id)
    #传入socket接入认证
    admin_packet.admin(s,authid1)
    #获取接入认证的sess_key和sess_key_id，后面会话使用
    ack_key=admin_packet.get_sess_key()
    ack_key_id=admin_packet.get_sess_key_id()
    print '******ack_key',ack_key
    #time.sleep(30)
    #创建申请密钥请求的实例 
    req_packet=qkmReqPacket.ReqPacket()
    #将会话key和key_id传入，以便后面加密使用
    req_packet.set_sess_key(ack_key)
    req_packet.set_sess_key_id(ack_key_id)
    #设置报文头字段
    req_packet.set_version(1)
    req_packet.set_encry_alg(1)
    req_packet.set_msg_typ(125)
    #设置报文体字段变量
    req_user_name=user_name
    req_reqid=60
    req_get_typ=1
    req_key_typ=0
    req_key_num=3
    req_key_len=32
    req_key_id_list=[]
    peer_num=3
    peer_name_1='client_lq3'
    peer_name_2='client_lq4'
    peer_name_3='node_child'
    peer_name_4='node_child'
    peer_name_5='node_child'
    req_specified=0  
    #将报文体字段变量传入实例，赋值   
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
    #获取请求报文的二进制字节流
    req_packet_pack=req_packet.get_packet()
    print '****************',req_packet_pack
    #发送二进制字节流到socket
    s.send(req_packet_pack)
    #设置socket超时时间
    s.settimeout(10)
    #接收反馈报文
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
    #创建接收反馈报文实例
    rc_packet=qkmRcPacket.RecvPacket()
    #设置反馈报文会话key，以便后续解密
    rc_packet.set_sess_key(ack_key)
    #使用接收数据来填充实例的各成员变量，具体实现见unpack方法
    rc_packet.unpack(recvData)
    #获取反馈报文结果
    rc_status=rc_packet.getResult()
    print 'rc_status',rc_status
    if rc_status==0:      
        #如果反馈成功个，从反馈报文中获取以下字段
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
#        print 'rc_key_id_list',rc_key_id_list
#        print 'rc_key_list',rc_key_list
#        print 'rc_msg_typ',rc_msg_typ
#        print 'rc_req_id',rc_req_id      
        #比对反馈报文的结果是否与预期相符
        if (rc_msg_typ == 126  and  rc_req_id == req_reqid and rc_key_typ == req_key_typ and  rc_key_num == req_key_num and rc_key_len == req_key_len and rc_get_typ == req_get_typ ):
            #如果以上判断为真，发送确认报文
#            print '*****req success***** and status is ',rc_status
            ack_packet=qkmAckPacket.AckPacket()
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
            print '*****ack success***** '
        else:
            '#-------------something is not same with recvData-----------------------#'
    
    else:
        print '*****req failed***** and status is：申请获取量子密钥 ',rc_status
        

        
        