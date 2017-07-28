#!/usr/bin/python
# -*-coding:UTF-8-*- 
import sys
import binascii
import socket
import proPacket,adminPacket
import time,akmReqPacket,akmRcPacket,proPacket,pushPacket
import threading,time

#鎼存梻鏁ょ�靛棝鎸滈敍灞剧壌閹诡喕绱堕崗銉ф畱ip閿涘瘈sername閿涘瘈ser_typ,key_id閿涘本甯撮崗顧畂st閿涘苯鑻熼悽瀹狀嚞鎼存梻鏁ょ�靛棝鎸�
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
    #print '******ack_key',ack_key
    print 'creator is================================================================================================',user_name
    #print 'thread ack key==========================================================',ack_key
    #time.sleep(60)
    #generate part   
    req_packet=akmReqPacket.ReqPacket()
    req_packet.set_sess_key(ack_key)
    req_packet.set_sess_key_id(ack_key_id)
    req_packet.set_version(1)
    req_packet.set_encry_alg(1)
    
    #set req packet message   
    req_msg_typ=119
    req_reqid=5
    req_reserve=0
    req_key_typ=0
    req_save=1
    req_save_time=65535
    req_key_num=1
    req_key_len=32
    req_automatic=1
    req_auto_rate=2
    # set attend information to variable
    req_user_name=user_name
    req_attend_num=2
    req_attend_name_1='client_wm1'
    req_attend_name_2='client_wm2'
    req_attend_name_3='node_child3'
    req_attend_name_4='node_child4'
    req_attend_name_5='node_child5'
    # set sess information to variable
    req_sess_typ=0
    req_sess_attend_num=3
    req_sess_name='liqing01'   
  
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
    #set attend member information
    req_packet.set_attend_num(req_attend_num)
    req_packet.set_attend_name_1(req_attend_name_1)
    req_packet.set_attend_name_2(req_attend_name_2)
    req_packet.set_attend_name_3(req_attend_name_3)
    req_packet.set_attend_name_4(req_attend_name_4)
    req_packet.set_attend_name_5(req_attend_name_5)
    #set attend name length
    req_packet.set_attend_name_len_1(len(req_attend_name_1))
    req_packet.set_attend_name_len_2(len(req_attend_name_2))
    req_packet.set_attend_name_len_3(len(req_attend_name_3))
    req_packet.set_attend_name_len_4(len(req_attend_name_4))
    req_packet.set_attend_name_len_5(len(req_attend_name_5))
    # set session information
    req_packet.set_sess_typ(req_sess_typ)
    req_packet.set_sess_attend_num(req_sess_attend_num)
    req_packet.set_sess_name(req_sess_name)
    req_packet.set_sess_name_len(len(req_sess_name))

    req_packet_pack=req_packet.get_packet()
    #print '****************',req_packet_pack
    s.send(req_packet_pack)
    s.settimeout(20)      
    print 'send success'   
    try: 
        while True:
            #print 'in while receive rc_packet'
            data = s.recv(BUFSIZE)
            #print '--recive rc_packet data: ',data
            #print '--recive rc_packet data: ',len(data)
            
            if len(data) >= 8:
                break 
    except socket.error, e:
        print "Error receive data: %s" %e
        sys.exit(1)
    #print '*********Data',binascii.hexlify(data)
    
    recvData=data
    rc_packet=akmRcPacket.RecvPacket()
    rc_packet.set_sess_key(ack_key)
    rc_packet.set_key_typ(req_key_typ)
    rc_packet.set_automatic(req_automatic)
    rc_packet.unpack(recvData)
    rc_status=rc_packet.getResult()
    #print 'rc_status',rc_status
    if rc_status==0:      
        rc_msg_typ=rc_packet.get_msg_typ()
        rc_req_id=rc_packet.get_req_id()
        rc_sess_id=rc_packet.get_sess_id()
        print 'rc_sess_id',rc_sess_id
        print '***************************************************************************************************************'
        if(req_key_typ==0 and req_automatic==1):
            print 'enter req_key_typ==0 and req_automatic==1'
            if (rc_msg_typ==120 and rc_req_id==req_reqid):
                print '*****req success***** and status is ',rc_status
                         
                #getPushPacket(s,req_user_name,ack_key,BUFSIZE)
                #modAkmKey_2(s,rc_sess_id,ack_key,ack_key_id,BUFSIZE)         
                push_t = threading.Thread(target=getPushPacket,args=(s,req_user_name,ack_key,BUFSIZE))
                push_t.start()
                mod_t=threading.Thread(target=modAkmKey_2,args=(s,rc_sess_id,ack_key,ack_key_id,BUFSIZE))
                mod_t.start()
                
#                 try: 
#                     while True:
#                         while True:
#                             #print 'in while receive rc_packet'
#                             data = s.recv(BUFSIZE)
#                             #print '--recive rc_packet data: ',data
#                             #print '--recive rc_packet data: ',len(data)           
#                             if len(data) >= 8:
#                                 break 
#                         print '*********Data',binascii.hexlify(data)
#                         recvData=data
#                         #print '--recive recvData: ',recvData
#                         pushReqPacket=pushPacket.PushReqPacket()
#                         pushReqPacket.set_sess_key(ack_key)
#                         pushReqPacket.unpack(recvData) 
#                         sessName=pushReqPacket.get_sessName()
#                         key_id_list=pushReqPacket.get_key_id_list()
#                         key_list=pushReqPacket.get_key_list()
#                         msg_typ=pushReqPacket.get_msg_typ()
#                         print 'push packet sessName',sessName
#                         print 'push packet key_id_list',key_id_list
#                         print 'push packet key_id_list',binascii.hexlify(key_id_list)
#                         print 'push packet key_list',key_list
#                         print 'push packet msg_typ',msg_typ
#                         if (msg_typ==131):
#                             print 'get push packet success',user_name
#                         else:
#                             print 'push packet error'  
#                         
#                 except socket.error, e:
#                     print "Error receive data: %s" %e
#                     sys.exit(1)
                               
            else:
                print'#-------------something is not same with recvData-----------------------#' 
        else:
            print 'enter non req_key_typ==0 and req_automatic==1'
            rc_sess_id=rc_packet.get_sess_id()
            rc_key_num=rc_packet.get_key_num()
            rc_key_len=rc_packet.get_key_len()
            rc_key_id_list=rc_packet.get_key_id_list()
            rc_key_list=rc_packet.get_key_list()
            rc_sess_id=rc_packet.get_sess_id()
            print 'rc_key_id_list',rc_key_id_list
            print 'rc_key_list',rc_key_list
            print 'rc_msg_typ',rc_msg_typ
            print 'rc_req_id',rc_req_id
            print 'rc_sess_id',rc_sess_id 
           
            if (rc_msg_typ==120 and rc_key_num==req_key_num and rc_key_len == req_key_len):
                print '*****req success***** and status is ',rc_status         
            else:
                '#-------------something is not same with recvData-----------------------#'   
    else:
        print '*****req failed***** and status is ',rc_status
    #s.close()
        
#鎼存梻鏁ょ�靛棝鎸滈敍灞剧壌閹诡喕绱堕崗銉ф畱ip閿涘瘈sername閿涘瘈ser_typ,key_id閿涘本甯撮崗顧畂st閿涘苯鑻熼懢宄板絿鎼存梻鏁ょ�靛棝鎸�
def obtAkmKey(host_ip,user_name,user_typ,key_id): 
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
    req_packet.set_sess_key(ack_key)
    req_packet.set_sess_key_id(ack_key_id)
    req_packet.set_version(1)
    req_packet.set_encry_alg(1)
    
    #set req packet message   
    req_msg_typ=121
    req_reqid=61
    req_key_num=1
    req_key_len=32
    req_user_name=user_name
    req_user_name_len=len(req_user_name)
    req_key_id_list=[109, 161, 185, 123, 191, 253, 79, 92, 178, 83, 71, 94, 78, 37, 54, 34]
    
    req_packet.set_msg_typ(req_msg_typ)
    req_packet.set_req_id(req_reqid)
    req_packet.set_key_num(req_key_num)
    req_packet.set_key_len(req_key_len)
    req_packet.set_userName(req_user_name)
    req_packet.set_userName_len(req_user_name_len)
    req_packet.set_key_id_list(req_key_id_list)
  
    req_packet_pack=req_packet.get_packet()
    print '****************',binascii.hexlify(req_packet_pack)
    s.send(req_packet_pack)
    s.settimeout(20)
    
    print 'send success'
 
    
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
        print 'rc_req_id',rc_req_id      
        if (rc_msg_typ==122 and rc_req_id==req_reqid and rc_key_num==req_key_num and rc_key_len==req_key_len):
            print '*****req success***** and status is ',rc_status
          
        else:
            '#-------------something is not same with recvData-----------------------#'
    
    else:
        print '*****req failed***** and status is ',rc_status
    s.close()
        

#娣囶喗鏁兼惔鏃傛暏鐎靛棝鎸滈悽瀹狀嚞閹躲儲鏋�
def modAkmKey(host_ip,user_name,user_typ,key_id): 
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
    req_packet=akmReqPacket.ModReqPacket()
    req_packet.set_sess_key(ack_key)
    #req_packet.set_sess_key(ack_key)
    req_packet.set_sess_key_id(ack_key_id)
    #req_packet.set_sess_key_id(ack_key_id)
    req_packet.set_version(1)
    req_packet.set_encry_alg(1)  
    #set req packet message   
    req_msg_typ=123
    req_reqid=51
    req_mod_typ=1
    #req_session_id=SessionID
    req_session_id= [220, 253, 117, 158, 47, 113, 67, 82, 185, 176, 69, 156, 115, 103, 7, 249]  #SessionID
    req_attend_num=1
    req_attend_name_1='client_wm1'
    req_attend_name_2='client_wm3'
    req_attend_name_3='node_child3'
    req_attend_name_4='node_child4'
    req_attend_name_5='node_child5'
    
    req_packet.set_msg_typ(req_msg_typ)
    req_packet.set_req_id(req_reqid)
    req_packet.set_mod_typ(req_mod_typ)
    req_packet.set_sess_id(req_session_id)
    #鐠佸墽鐤嗛崣鍌欑瑢閼帮拷
    req_packet.set_attend_num(req_attend_num)
    req_packet.set_attend_num(req_attend_num)
    req_packet.set_attend_name_1(req_attend_name_1)
    req_packet.set_attend_name_2(req_attend_name_2)
    req_packet.set_attend_name_3(req_attend_name_3)
    req_packet.set_attend_name_4(req_attend_name_4)
    req_packet.set_attend_name_5(req_attend_name_5)
    #鐠佸墽鐤嗛崣鍌欑瑢閼板懘鏆辨惔锟�
    req_packet.set_attend_name_len_1(len(req_attend_name_1))
    req_packet.set_attend_name_len_2(len(req_attend_name_2))
    req_packet.set_attend_name_len_3(len(req_attend_name_3))
    req_packet.set_attend_name_len_4(len(req_attend_name_4))
    req_packet.set_attend_name_len_5(len(req_attend_name_5))
       
    req_packet_pack=req_packet.get_packet()
    s.send(req_packet_pack)
    s.settimeout(20)
   
    print 'send success'  
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
    rc_packet=akmRcPacket.ModRecvPacket()
    rc_packet.set_sess_key(ack_key)
    rc_packet.unpack(recvData)
    rc_status=rc_packet.getResult()
    print 'rc_status:娣囶喗鏁兼惔鏃傛暏鐎靛棝鎸滈張宥呭閸欏秹顩幎銉︽瀮閿涗緤绱�',rc_status
    if rc_status==0:      
        rc_msg_typ=rc_packet.get_msg_typ()
        rc_req_id=rc_packet.get_req_id()
        rc_sess_id=rc_packet.get_sess_id()
        print 'rc_msg_typ',rc_msg_typ
        print 'rc_req_id',rc_req_id
        print 'rc_sess_id:娣囶喗鏁兼惔鏃傛暏鐎靛棝鎸滈張宥呭閸欏秹顩幎銉︽瀮閿涗緤绱�',rc_sess_id      
        if (rc_msg_typ==124 and rc_req_id ==req_reqid and rc_sess_id==req_session_id):
            print '*****req success***** and status is 閿涙矮鎱ㄩ弨鐟扮安閻€劌鐦戦柦顨剘',rc_status
          
        else:
            '#-------------something is not same with recvData-----------------------#'
    
    else:
        print '*****req failed***** and status is ',rc_status
    #s.close()
 
def modAkmKey_2(s,req_session_id,ack_key,ack_key_id,BUFSIZE):
    time.sleep(10)
    req_packet=akmReqPacket.ModReqPacket()
    req_packet.set_sess_key(ack_key)
    req_packet.set_sess_key_id(ack_key_id)
    req_packet.set_version(1)
    req_packet.set_encry_alg(1)  
    req_packet.set_sess_id(req_session_id)
    #set req packet message   
    req_msg_typ=123
    req_reqid=5
    req_mod_typ=2
    req_attend_num=1
    req_attend_name_1='client_wm1'
    req_attend_name_2='client_wm2'
    req_attend_name_3='node_child3'
    req_attend_name_4='node_child4'
    req_attend_name_5='node_child5'
    
    req_packet.set_msg_typ(req_msg_typ)
    req_packet.set_req_id(req_reqid)
    req_packet.set_mod_typ(req_mod_typ)
    #req_session_id=[56, 147, 45, 10, 143, 89, 66, 202, 189, 169, 150, 33, 180, 41, 216, 30]
    req_packet.set_sess_id(req_session_id)
    
    #设置参与者
    req_packet.set_attend_num(req_attend_num)
    req_packet.set_attend_name_1(req_attend_name_1)
    req_packet.set_attend_name_2(req_attend_name_2)
    req_packet.set_attend_name_3(req_attend_name_3)
    req_packet.set_attend_name_4(req_attend_name_4)
    req_packet.set_attend_name_5(req_attend_name_5)
    #设置参与者长度
    req_packet.set_attend_name_len_1(len(req_attend_name_1))
    req_packet.set_attend_name_len_2(len(req_attend_name_2))
    req_packet.set_attend_name_len_3(len(req_attend_name_3))
    req_packet.set_attend_name_len_4(len(req_attend_name_4))
    req_packet.set_attend_name_len_5(len(req_attend_name_5))
       
    req_packet_pack=req_packet.get_packet()
    s.send(req_packet_pack)
    #s.settimeout(20)
   
    print 'send mod packet success==========================================================================================================================================' 
    print 'send mod packet success=========================================================================================================================================='  
    print 'send mod packet success=========================================================================================================================================='   
    
    mod=0
    try: 
        while (mod==0):
            while True:
                data = s.recv(BUFSIZE)
                if not data:     
                    break
                else:
                    recvData=data
                    #print '*********Data',binascii.hexlify(data)
                    tmp_packet=proPacket.ProcPacket(data,ack_key)
                    msg_typ=tmp_packet.getMsgType() 
                    print 'msg_type is ',msg_typ           
                if(msg_typ == 104):
                    print 'enter into sess fresh'
                    #admin.admin(conn, data)
                    break
                elif(msg_typ ==131):
                    pushReqPacket=pushPacket.PushReqPacket()
                    pushReqPacket.set_sess_key(ack_key)
                    pushReqPacket.unpack(recvData) 
                    sessName=pushReqPacket.get_sessName()
                    key_id_list=pushReqPacket.get_key_id_list()
                    key_list=pushReqPacket.get_key_list()
                    msg_typ=pushReqPacket.get_msg_typ()
                    print 'get push packet success ======================================================================================create member at:', time.ctime() 
                    print '==============================================================================================================' 
                elif(msg_typ==124):
                    recvData=data
                    rc_packet=akmRcPacket.ModRecvPacket()
                    rc_packet.set_sess_key(ack_key)
                    rc_packet.unpack(recvData)
                    rc_status=rc_packet.getResult()
                    print 'rc_status',rc_status
                    if rc_status==0:      
                        rc_msg_typ=rc_packet.get_msg_typ()
                        rc_req_id=rc_packet.get_req_id()
                        rc_sess_id=rc_packet.get_sess_id()
                        #print 'rc_msg_typ',rc_msg_typ
                        #print 'rc_req_id',rc_req_id
                        #print 'rc_sess_id',rc_sess_id      
                        if (rc_msg_typ==124 and rc_req_id ==req_reqid and rc_sess_id==req_session_id):
                            print '*****req success***** and status is ',rc_status
                            
                          
                        else:
                            '#-------------something is not same with recvData-----------------------#'
                    
                    else:
                        print '*****req failed***** and status is ',rc_status
                    mod=1
                    break
                else:
                    print 'unknow packets===========================================================',msg_typ
                         
    except socket.error, e:
        print "Error receive data: %s" %e
        sys.exit(1)
                    
   
def getPushPacket(s,user_name,ack_key,BUFSIZE):
    try: 
        while True:
            while True:
                data = s.recv(BUFSIZE)
                #print '--recive rc_packet data: ',data
                #print '--recive rc_packet data: ',len(data)           
                #if len(data) >= 8:
                #    break 
                if not data:     
                    break
                else:
                    recvData=data
                    #print '*********Data',binascii.hexlify(data)
                    tmp_packet=proPacket.ProcPacket(data,ack_key)
                    msg_typ=tmp_packet.getMsgType() 
                    print 'msg_type is ',msg_typ           
                if(msg_typ == 104):
                    print 'enter into sess fresh'
                    #admin.admin(conn, data)
                    break
                elif(msg_typ ==131):
                    pushReqPacket=pushPacket.PushReqPacket()
                    pushReqPacket.set_sess_key(ack_key)
                    pushReqPacket.unpack(recvData) 
                    sessName=pushReqPacket.get_sessName()
                    key_id_list=pushReqPacket.get_key_id_list()
                    key_list=pushReqPacket.get_key_list()
                    msg_typ=pushReqPacket.get_msg_typ()
                    print '===============================get push packet success',user_name,' at:', time.ctime() 
                    print '==============================================================================================================' 
                    
                    #print 'push packet sessName',sessName
                    #print 'push packet key_id_list',key_id_list
                    #print 'push packet key_id_list',binascii.hexlify(key_id_list)
                    #print 'push packet key_list',key_list
                    #print 'push packet msg_typ',msg_typ
                elif(msg_typ==124):
                    break
                else:
                    print 'unknow packets==============================================================================================',msg_typ
                         
    except socket.error, e:
        print "Error receive data: %s" %e
        sys.exit(1)
                    
                 
                 
            
             
             
             
                                  
    
        
        
        
        
        
        
        