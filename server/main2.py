# -*-coding:UTF-8-*- 
import threading
import time
import socket,sys,adminPacket,pushPacket
import xlrd
from client import main2,genPacket,rcGenPacket

import binascii
global Akm_HOST
global Qkm_HOST
Qkm_HOST='192.168.94.104'
remote_user_id=1100000
Akm_HOST='192.168.91.183'
BUFSIZE = 1024 
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
adminNum=1

def setUserInfo(num):
    lists=[[] for i in range(num)]
    for i in range(num):
        lists[i].append(eval('UserName_%s'%i))
        lists[i].append(eval('UserTyp_%s'%i))
        lists[i].append(eval('KeyID_%s'%i))
    for i in range(num):
        print  'list %d'%i,lists[i]
    return lists

def setUserInfo2():
    
    try:  
        data = xlrd.open_workbook("D:\\workspace\\userInfo.xlsx")
        table = data.sheets()[0] 
        nrows = table.nrows
        ncols = table.ncols
        
        lists=[[] for i in range(nrows)]
        for row in range(0,table.nrows):
            userID=int(table.cell(row,0).value)
            userName=table.cell(row,1).value 
            userTyp=int(table.cell(row,2).value)
            keyID=table.cell(row,3).value 
            #print 'text', userID,  userName, userTyp,keyID
            lists[row].append(userID)
            lists[row].append(userName)
            lists[row].append(userTyp)
            lists[row].append(keyID) 
        #for row in range(0,table.nrows):
            #for col in range(0,table.ncols):
               # print 'list %d %d'%(row,col),lists[row][col]
        return  lists             
    except Exception,e:  
        print str(e)


def admin_thread(adminNum):
    adminNum=adminNum
    clientList=setUserInfo2()
    #for i in range(0,adminNum):        
    print 'starting at:', time.ctime() 
    threads = [] 
    nloops = range(adminNum) 
  
    for i in range(0,adminNum):  # create all threads 
        print 'client i',clientList[i][0],clientList[i][1],clientList[i][2],clientList[i][3]
        t = threading.Thread(target=clientRun,args=(Qkm_HOST,clientList[i][0],str(clientList[i][1]),clientList[i][2],str(clientList[i][3]))) 
        threads.append(t) 
  
    for i in range(0,adminNum):  # start all threads 
        threads[i].start() 
  
    for i in range(0,adminNum):  # wait for completion 
        threads[i].join() 
  
    print 'all DONE at:', time.ctime()   

#�ͻ��˽����ȴ��������������ͱ���    
def clientRun(host_ip,user_id,user_name,user_typ,key_id):
    print 'start loop', user_name, 'at:', time.ctime() 
    host = host_ip
    port = PORT
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print '---line 110---Failed to create socket.Error code: '+ str(msg[0]) + ', Error message: ' + msg[1]
        sys.exit()
    print '---line 112--- Socket create'
    s.connect((host, port))    
    #����������֤ʵ������Ҫ�����û������û����ͺ�key_id
    admin_packet=adminPacket.AdminPacket(user_name,user_typ,key_id)
    #����socket������֤
    admin_packet.admin(s)
    ack_key=admin_packet.get_sess_key()
    ack_key_id=admin_packet.get_sess_key_id()
    #time.sleep(60)
    #s.close()
    #sys.exit(0)
    #����ͬ��
    main2.gen_sys_key(s,user_id,1100000,ack_key,ack_key_id)  
#     try: 
#         while True:
#             while True:
#                 print 'in while',user_name,'at:',time.ctime()
#                 data = s.recv(BUFSIZE)
#                 #print '--recive rc_packet data: ',data
#                 #print '--recive rc_packet data: ',len(data)           
#                 if len(data) >= 8:
#                     break
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
#              
#     except socket.error, e:
#         print "Error receive data: %s" %e
#         sys.exit(1)
#     
         
def multiThread(attend_num,clientList):

    threads = []    
    #�����������̣߳������ȴ�
    for i in range(attend_num-1):  # create all threads 
        t = threading.Thread(target=clientRun,args=(Akm_HOST,clientList[i][0],clientList[i][1],clientList[i][2]))
        threads.append(t)   
    for i in range(attend_num-1):  # start all threads 
        threads[i].start()
    
    

if __name__ == '__main__':
    attend_num=UserNum
    clientList=setUserInfo(attend_num)       
    #����������Կ��Ϊ����Ӧ����Կ���ܣ�������
    #���ﶨ���atten_num�����˴����ߣ�client[attend_num-1]����ϢΪ��������Ϣ������Ϊ��������Ϣ��
    #qkm.getQkmKeyΪ����������������Կ
    #qkm.getQkmKey(Qkm_HOST,clientList[attend_num-1][0],clientList[attend_num-1][1],clientList[attend_num-1][2])
    #qkm.getQkmKeyΪ����������������Կ
    #qkm.getQkmKey(Qkm_HOST,clientList[0][0],clientList[0][1],clientList[0][2]) 
    #multiThread(attend_num,clientList)
    #akm.getAkmKey(Akm_HOST,clientList[attend_num-1][0],clientList[attend_num-1][1],clientList[attend_num-1][2])
    #while True:
    admin_thread(adminNum)
        #time.sleep(60)
    
    #clientRun(Qkm_HOST,'node_wm100',0,'61626364653130300000000000000000')

    
        