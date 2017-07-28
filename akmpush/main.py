import threading
from time import sleep, ctime,time
import socket,sys
import akm,qkm,adminPacket,pushPacket
import binascii
global Akm_HOST
global Qkm_HOST
Qkm_HOST='192.168.91.158'
Akm_HOST='192.168.91.113'
BUFSIZE = 4096 
PORT = 5530
UserName_0='client_qh012'
UserName_1='client_qh013'
UserName_2='client_qh001'
UserTyp_0=1
UserTyp_1=1
UserTyp_2=1
KeyID_0=[01,01,01,01,01,01,01,01,01,01,01,01,01,07,01,23]
KeyID_1=[01,01,01,01,01,01,01,01,01,01,01,01,01,07,01,24]
KeyID_2=[01,01,01,01,01,01,01,01,01,01,01,01,01,07,01,04]
UserNum=3

def setUserInfo(num):
    lists=[[] for i in range(num)]
    for i in range(num):
        lists[i].append(eval('UserName_%s'%i))
        lists[i].append(eval('UserTyp_%s'%i))
        lists[i].append(eval('KeyID_%s'%i))
    for i in range(num):
        print  'list %d'%i,lists[i]
    return lists


def clientRun(host_ip,user_name,user_typ,key_id):
    print 'start loop================================================', user_name, 'at:', ctime() 
    host = host_ip
    port = PORT
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print '---line 110---Failed to create socket.Error code: '+ str(msg[0]) + ', Error message: ' + msg[1]
        sys.exit()
    print '---line 112------------------------------------------------------ Socket create',user_name
    s.connect((host, port))    
    
    admin_packet=adminPacket.AdminPacket(user_name,user_typ,key_id)
   
    admin_packet.admin(s)
    ack_key=admin_packet.get_sess_key()
    #print 'thread ack key==========================================================',ack_key
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
            akm.getPushPacket(s,user_name,ack_key,BUFSIZE)
    except socket.error, e:
        print "Error receive data: %s" %e
        sys.exit(1)       
            
#             print '*********Data',binascii.hexlify(data)
#             recvData=data
#             #print '--recive recvData: ',recvData
#             pushReqPacket=pushPacket.PushReqPacket()
#             pushReqPacket.set_sess_key(ack_key)
#             pushReqPacket.unpack(recvData)
#             sessName=pushReqPacket.get_sessName()
#             key_id_list=pushReqPacket.get_key_id_list()
#             key_list=pushReqPacket.get_key_list()
#             msg_typ=pushReqPacket.get_msg_typ()
#             print 'push packet sessName',sessName
#             print 'push packet key_id_list',key_id_list
#             print 'push packet key_list',key_list
#             print 'push packet msg_typ',msg_typ
#             if (msg_typ==131):
#                 print 'get push packet success',user_name
#             else:
#                 print 'push packet error'
#                 sys.exit(1)    
              
def multiThread(attend_num,clientList):

    threads = []           
    #qkm.getQkmKey(Qkm_HOST,clientList[attend_num-1][0],clientList[attend_num-1][1],clientList[attend_num-1][2])    
    #qkm.getQkmKey(Qkm_HOST,clientList[0][0],clientList[0][1],clientList[0][2])
    for i in range(1):  # create all threads attend_num-1
        t = threading.Thread(target=clientRun,args=(Akm_HOST,clientList[i][0],clientList[i][1],clientList[i][2]))
        threads.append(t)   
    for i in range(1):  # start all threads 
        threads[i].start()

def getQkmKeyWhile(histip,userName,userTyp,keyID):
    while True:
        qkm.getQkmKey(histip,userName,userTyp,keyID)
        sleep(5)    
    

if __name__ == '__main__':
    attend_num=UserNum
    clientList=setUserInfo(attend_num)
    
    #t1 = threading.Thread(target=getQkmKeyWhile,args=(Qkm_HOST,clientList[2][0],clientList[2][1],clientList[2][2]))
    #t2 = threading.Thread(target=getQkmKeyWhile,args=(Qkm_HOST,clientList[1][0],clientList[1][1],clientList[1][2]))
    #t3 = threading.Thread(target=getQkmKeyWhile,args=(Qkm_HOST,clientList[0][0],clientList[0][1],clientList[0][2]))
    #t1.start()
    #t2.start()
    #t3.start()
    
    #qkm.getQkmKey(Qkm_HOST,clientList[0][0],clientList[0][1],clientList[0][2])
    #qkm.getQkmKey(Qkm_HOST,clientList[1][0],clientList[1][1],clientList[1][2])   
    #qkm.getQkmKey(Qkm_HOST,clientList[0][0],clientList[0][1],clientList[0][2])   

    
    
    #qkm.getQkmKey(Qkm_HOST,clientList[attend_num-1][0],clientList[attend_num-1][1],clientList[attend_num-1][2])
#    qkm.getQkmKey(Qkm_HOST,clientList[0][0],clientList[0][1],clientList[0][2])

    multiThread(attend_num,clientList)
    akm.getAkmKey(Akm_HOST,clientList[attend_num-1][0],clientList[attend_num-1][1],clientList[attend_num-1][2])
    #multiThread(attend_num,clientList)
    #sleep(5)
    #
    #multiThread(attend_num,clientList)
    #akm.modAkmKey(Akm_HOST,clientList[attend_num-1][0],clientList[attend_num-1][1],clientList[attend_num-1][2])    
    

    
        