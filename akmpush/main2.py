# -*-coding:UTF-8-*- 
import threading
from time import sleep, ctime,time
import socket,sys,adminPacket,pushPacket
import akm,qkm

import binascii
global Akm_HOST
global Qkm_HOST
Qkm_HOST='192.168.91.112'
Akm_HOST='192.168.91.113'
BUFSIZE = 4096 
PORT = 5530
UserName_0='client_wm1'
UserName_1='client_wm2'
UserName_2='client_wm3'
UserTyp_0=1
UserTyp_1=1
UserTyp_2=1
KeyID_0=[01,01,01,01,01,01,01,01,01,01,01,01,01,01,00,01]
KeyID_1=[01,01,01,01,01,01,01,01,01,01,01,01,01,01,00,02]
KeyID_2=[01,01,01,01,01,01,01,01,01,01,01,01,01,01,00,03]
UserNum=2

def setUserInfo(num):
    lists=[[] for i in range(num)]
    for i in range(num):
        lists[i].append(eval('UserName_%s'%i))
        lists[i].append(eval('UserTyp_%s'%i))
        lists[i].append(eval('KeyID_%s'%i))
    for i in range(num):
        print  'list %d'%i,lists[i]
    return lists

#客户端接入后等待，服务器端推送报文    
def clientRun(host_ip,user_name,user_typ,key_id):
    print 'start loop', user_name, 'at:', ctime() 
    host = host_ip
    port = PORT
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
    admin_packet.admin(s)
    ack_key=admin_packet.get_sess_key()
    ack_key_id=admin_packet.get_sess_key_id()
    try: 
        while True:
            while True:
                #print 'in while',user_name,'at:',ctime()
                data = s.recv(BUFSIZE)
                #print '--recive rc_packet data: ',data
                #print '--recive rc_packet data: ',len(data)           
                if len(data) >= 8:
                    break
            print '*********Data',binascii.hexlify(data)
            recvData=data
            #print '--recive recvData: ',recvData
            pushReqPacket=pushPacket.PushReqPacket()
            pushReqPacket.set_sess_key(ack_key)
            pushReqPacket.unpack(recvData)
            sessName=pushReqPacket.get_sessName()
            key_id_list=pushReqPacket.get_key_id_list()
            key_list=pushReqPacket.get_key_list()
            msg_typ=pushReqPacket.get_msg_typ()
            print 'push packet sessName',sessName
            print 'push packet key_id_list',key_id_list
            print 'push packet key_list',key_list
            print 'push packet msg_typ',msg_typ
            if (msg_typ==131):
                print 'get push packet success',user_name
            else:
                print 'push packet error'
                sys.exit(1)    
        
        
    except socket.error, e:
        print "Error receive data: %s" %e
        sys.exit(1)
    
       
def multiThread(attend_num,clientList):

    threads = []    
    #创建参与者线程，接入后等待
    for i in range(attend_num-1):  # create all threads 
        t = threading.Thread(target=clientRun,args=(Akm_HOST,clientList[i][0],clientList[i][1],clientList[i][2]))
        threads.append(t)   
    for i in range(attend_num-1):  # start all threads 
        threads[i].start()
    
    

if __name__ == '__main__':
    attend_num=UserNum
    clientList=setUserInfo(attend_num)
        
    #申请量子密钥，为后续应用密钥加密，做储备
    #这里定义的atten_num包含了创建者，client[attend_num-1]的信息为创建者信息，其他为参与者信息。
    # qkm.getQkmKey为创建者申请量子密钥
    #qkm.getQkmKey(Qkm_HOST,clientList[attend_num-1][0],clientList[attend_num-1][1],clientList[attend_num-1][2])
      # qkm.getQkmKey为参与者申请量子密钥
    #qkm.getQkmKey(Qkm_HOST,clientList[0][0],clientList[0][1],clientList[0][2])
    ##qkm.getQkmKey(UserName2,UserTyp,KeyID_2)
    #申请应用密钥
    ##akm.getAkmKey(UserName1,UserTyp,KeyID_1)
    #获取应用密钥
    ##akm.obtAkmKey(UserName2,UserTyp,KeyID_2)
    
    #multiThread(attend_num,clientList)
    #akm.getAkmKey(Akm_HOST,clientList[attend_num-1][0],clientList[attend_num-1][1],clientList[attend_num-1][2])
    #修改应用密钥
    multiThread(attend_num,clientList)
    akm.modAkmKey(Akm_HOST,clientList[attend_num-1][0],clientList[attend_num-1][1],clientList[attend_num-1][2])    
    

    
        