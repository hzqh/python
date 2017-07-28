#!/usr/bin/python
# -*-coding:UTF-8-*- 
import sys
import binascii
import socket
import qkmReqPacket,qkmRcPacket,qkmAckPacket
import adminPacket
import time



#閲忓瓙瀵嗛挜锛屾牴鎹紶鍏ョ殑ip锛寀sername锛寀ser_typ,key_id锛屾帴鍏ost锛屽苟鐢宠閲忓瓙瀵嗛挜
def getQkmKey(host_ip,user_name,user_typ,key_id): 
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
    #鍒涘缓鎺ュ叆璁よ瘉瀹炰緥锛岄渶瑕佷紶鍏ョ敤鎴峰悕锛岀敤鎴风被鍨嬪拰key_id
    admin_packet=adminPacket.AdminPacket(user_name,user_typ,key_id)
    #浼犲叆socket鎺ュ叆璁よ瘉
    admin_packet.admin(s)
    #鑾峰彇鎺ュ叆璁よ瘉鐨剆ess_key鍜宻ess_key_id锛屽悗闈細璇濅娇鐢�
    ack_key=admin_packet.get_sess_key()
    ack_key_id=admin_packet.get_sess_key_id()
    #print '******ack_key',ack_key
    #time.sleep(300)
    #鍒涘缓鐢宠瀵嗛挜璇锋眰鐨勫疄渚� 
    req_packet=qkmReqPacket.ReqPacket()
    #灏嗕細璇漦ey鍜宬ey_id浼犲叆锛屼互渚垮悗闈㈠姞瀵嗕娇鐢�
    req_packet.set_sess_key(ack_key)
    req_packet.set_sess_key_id(ack_key_id)
    #璁剧疆鎶ユ枃澶村瓧娈�
    req_packet.set_version(1)
    req_packet.set_encry_alg(1)
    req_packet.set_msg_typ(125)
    #璁剧疆鎶ユ枃浣撳瓧娈靛彉閲�
    req_user_name=user_name
    req_reqid=60
    req_get_typ=1
    req_key_typ=0
    req_key_num=10
    req_key_len=32
    req_key_id_list=[]
    peer_num=2
    peer_name_1='node_child1'
    peer_name_2='node_child2'
    peer_name_3='node_child'
    peer_name_4='node_child'
    peer_name_5='node_child'
    req_specified=0  
    #灏嗘姤鏂囦綋瀛楁鍙橀噺浼犲叆瀹炰緥锛岃祴鍊�   
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
    #鑾峰彇璇锋眰鎶ユ枃鐨勪簩杩涘埗瀛楄妭娴�
    req_packet_pack=req_packet.get_packet()
    #鍙戦�佷簩杩涘埗瀛楄妭娴佸埌socket
    s.send(req_packet_pack)
    print "-----------------"
#    time.sleep(10)
    #璁剧疆socket瓒呮椂鏃堕棿
    s.settimeout(20)
    #鎺ユ敹鍙嶉鎶ユ枃
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
    #鍒涘缓鎺ユ敹鍙嶉鎶ユ枃瀹炰緥
    rc_packet=qkmRcPacket.RecvPacket()
    #璁剧疆鍙嶉鎶ユ枃浼氳瘽key锛屼互渚垮悗缁В瀵�
    rc_packet.set_sess_key(ack_key)
    #浣跨敤鎺ユ敹鏁版嵁鏉ュ～鍏呭疄渚嬬殑鍚勬垚鍛樺彉閲忥紝鍏蜂綋瀹炵幇瑙乽npack鏂规硶
    rc_packet.unpack(recvData)
    #鑾峰彇鍙嶉鎶ユ枃缁撴灉
    rc_status=rc_packet.getResult()
    #print 'rc_status',rc_status
    if rc_status==0:      
        #濡傛灉鍙嶉鎴愬姛涓紝浠庡弽棣堟姤鏂囦腑鑾峰彇浠ヤ笅瀛楁
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
        #print 'rc_key_id_list',rc_key_id_list
        #print 'rc_key_list',rc_key_list
        #print 'rc_msg_typ',rc_msg_typ
        #print 'rc_req_id',rc_req_id      
        #姣斿鍙嶉鎶ユ枃鐨勭粨鏋滄槸鍚︿笌棰勬湡鐩哥
        if (rc_msg_typ == 126  and  rc_req_id == req_reqid and rc_key_typ == req_key_typ and  rc_key_num == req_key_num and rc_key_len == req_key_len and rc_get_typ == req_get_typ ):
            #濡傛灉浠ヤ笂鍒ゆ柇涓虹湡锛屽彂閫佺‘璁ゆ姤鏂�
            print '*****req success***** and status is ',rc_status
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
            s.send(ack_packet_pack)
            print '*****ack success***** '
        else:
            '#-------------something is not same with recvData-----------------------#'
    
    else:
        print '*****req failed***** and status is ',rc_status
    
    s.close()  

        
        