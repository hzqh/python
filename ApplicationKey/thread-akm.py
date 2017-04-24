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
import qkmApply
import qkmGet
from commonUntils import adminPacket
from commonUntils import ExcelUntil
#import tools
import datetime,time
#import adminPacket
from commonUntils import adminPacket
from commonUntils import adminPacket
import threading
import unicodedata
import akm
import qkm

global Akm_HOST
global Qkm_HOST
#Qkm_HOST='192.168.91.84'
Qkm_HOST='192.168.94.201'
Akm_HOST='192.168.94.220'
#Qkm_HOST='192.168.126.132'
remote_user_id=7000002
Akm_HOST='192.168.91.183'
BUFSIZE = 1024 
PORT = 5530
UserId_0 = 7000020
UserId_1 = 7000021
UserId_2 = 7000022

UserName_0='thread_qh001'
UserName_1='thread_qh002'
UserName_2='thread_qh003'
UserTyp_0=1
UserTyp_1=1
UserTyp_2=1
KeyID_0=[01,01,01,01,01,01,01,01,01,01,01,01,01,07,01,20]
KeyID_1=[01,01,01,01,01,01,01,01,01,01,01,01,01,07,01,21]
KeyID_2=[01,01,01,01,01,01,01,01,01,01,01,01,01,07,01,22]
UserNum=1
adminNum=1

UserName = 'client_qh001'
UserTyp= 1
KeyID = [01,01,01,01,01,01,01,01,01,01,01,01,01,07,01,04]

k=0
d=0


def setUserInfo1():
    userinfo = ExcelUntil.excel_read_all("D:\\workplace\\PyTest-frame\\data\\userinfo1.xls",index_name='Sheet1',startrow = 1,startcol =0) #读取Excel用户信息，读取起始位置startrow = 1,startcol =0
    lists=[[] for i in range(len(userinfo))]
    for i in range(0,len(userinfo)):
        userinfo[i][0] = int(userinfo[i][0])
        userinfo[i][1] = str(userinfo[i][1])
        userinfo[i][2] = int(userinfo[i][2])
        userinfo[i][3]=ExcelUntil.excel_data_to_list(userinfo[i][3])
        userinfo[i][4]=ExcelUntil.excel_data_to_list(userinfo[i][4])
    return userinfo

def setUserInfo2():
    userinfo = ExcelUntil.excel_read_all("D:\\workplace\\PyTest-frame\\data\\userinfo6.xls",index_name='Sheet1',startrow = 1,startcol =0) #读取Excel用户信息，读取起始位置startrow = 1,startcol =0
    lists=[[] for i in range(len(userinfo))]
    for i in range(0,len(userinfo)):
        userinfo[i][0] = int(userinfo[i][0])
        userinfo[i][1] = str(userinfo[i][1])
        userinfo[i][2] = int(userinfo[i][2])
        userinfo[i][3]=ExcelUntil.excel_data_to_list(userinfo[i][3])
        userinfo[i][4]=ExcelUntil.excel_data_to_list(userinfo[i][4])
    return userinfo
#
    
def admin_thread():

    clientList1=setUserInfo1()
    clientList2=setUserInfo2()
#    clientList1=setUserInfo2()
    #for i in range(0,adminNum):        
    print 'starting at:', time.ctime() 

    threads = [] 
#    nloops = range(adminNum) 
  
    for i in range(0,len(clientList1)):  # create all threads 
       
        t = threading.Thread(target=clientRun,args=(Akm_HOST,clientList1[i][1],clientList1[i][2],clientList1[i][3],clientList1[i][4],clientList2[i][1],clientList2[i][2],clientList2[i][3]))        
#        t = threading.Thread(target=clientRun,args=(Qkm_HOST,UserName,UserTyp,KeyID))
        threads.append(t) 
          
    for i in range(0,len(clientList1)):  # start all threads 
        threads[i].start() 
  
    for i in range(0,len(clientList1)):  # wait for completion 
        threads[i].join() 
  
    print 'all DONE at:', time.ctime()   
#
##�ͻ��˽����ȴ��������������ͱ���    
def clientRun(host_ip,user_name1,user_typ1,key_id1,authid1,user_name2,user_typ2,key_id2,authid2):
#    print '---clientRun----key_id:',key_id
#    print '---clientRun----authid:',authid
    print 'start loop', user_name1, 'at:', time.ctime() 
    host = host_ip
    port = PORT
    global k
    global d
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print '---line 110---Failed to create socket.Error code: '+ str(msg[0]) + ', Error message: ' + msg[1]
        sys.exit()
    print '---line 112--- Socket create'
    s.connect((host, port))    
    #����������֤ʵ������Ҫ�����û������û����ͺ�key_id
    admin_packet=adminPacket.AdminPacket(user_name1,user_typ1,key_id1)
    #����socket������֤
    if admin_packet.admin(s,authid1)==1:
       k=k+1
        
    ack_key=admin_packet.get_sess_key()
    ack_key_id=admin_packet.get_sess_key_id()
    qkm.getQkmKey(Qkm_HOST,UserName1,user_typ1,key_id1,authid1)#接入认证、获取量子密钥
    time.sleep(5)
#    qkmApply.qkmapply(s,ack_key,ack_key_id,user_name) 
#    if qkmGet.qkmget(s,ack_key,ack_key_id,user_name)==1:
#       d=d+1   
#   ' akm.obtAkmKey(Akm_HOST,user_name1, user_typ1,key_id1,akm.getAkmKey(Akm_HOST,user_name2,user_typ2,key_id2))'
    
    akm.obtAkmKey(s,ack_key,ack_key_id,user_name1,akm.getAkmKey(Akm_HOST,user_name2,user_typ2,key_id2,authid2))
 
    
if __name__ == '__main__':
#    attend_num=UserNum
#    clientList=setUserInfo() 
    admin_thread()
    print '----totalclient----',k
    print '----totalget----',d


    
        