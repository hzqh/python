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
from server import qkmApply
from commonUntils import adminPacket
from commonUntils import ExcelUntil
#import tools
import datetime,time
#import adminPacket
from commonUntils import adminPacket
import threading


Qkm_HOST = '192.168.91.158'
PORT = 5530
 
#
##�ͻ��˽����ȴ��������������ͱ���    
def clientRun(host_ip,user_name,user_typ,key_id):
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
    qkmApply.qkmapply(s,ack_key,ack_key_id)   
    
      
if __name__ == '__main__':
    #根据实际Excel确定开始读取位置以及某些单元格数据的类型转换
    userinfo = ExcelUntil.excel_read_all("D:\\workplace\\PyTest-frame\\data\\userinfo.xls",index_name='Sheet1',startrow = 1,startcol =0) #读取Excel用户信息，读取起始位置startrow = 1,startcol =0
    for i in range(0,len(userinfo)):
        userinfo[i][0] = int(userinfo[i][0])
        userinfo[i][2] = int(userinfo[i][2])
    print userinfo
    print 'client i',userinfo[i][1],userinfo[i][2],userinfo[i][3]    
    clientList = userinfo
    #for i in range(0,adminNum):        
    print 'starting at:', time.ctime() 
    threads = [] 
    clientNum = len(clientList)
#    nloops = range(clientNum) 
  
    for i in range(0,clientNum):  # create all threads 
#        print 'client i',clientList[i][0],clientList[i][1],clientList[i][2],clientList[i][3]
#        t = threading.Thread(target=clientRun,args=(Qkm_HOST,clientList[i][0],str(clientList[i][1]),clientList[i][2],str(clientList[i][3])))
        t = threading.Thread(target=clientRun,args=(Qkm_HOST,clientList[i][1],clientList[i][2],clientList[i][3]))
        threads.append(t) 
  
    for i in range(0,clientNum):  # start all threads 
        threads[i].start() 
  
    for i in range(0,clientNum):  # wait for completion 
        threads[i].join() 
        
    print 'all DONE at:', time.ctime()  
        
    
    
    