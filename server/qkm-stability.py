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
import qkmApply1
import qkmGet
import dianduidian
from commonUntils import adminPacket
from commonUntils import ExcelUntil
#import tools
import datetime,time
#import adminPacket
from commonUntils import adminPacket
import threading
import unicodedata

global Akm_HOST
global Qkm_HOST
Qkm_HOST='192.168.126.131'
#Qkm_HOST='192.168.91.85'
#Qkm_HOST='192.168.94.201'
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

def setUserInfo():
    userinfo = ExcelUntil.excel_read_all("D:\\workplace\\PyTest-frame\\data\\userinfo1.xls",index_name='Sheet1',startrow = 1,startcol =0) #读取Excel用户信息，读取起始位置startrow = 1,startcol =0
    lists=[[] for i in range(len(userinfo))]
    for i in range(0,len(userinfo)):
        userinfo[i][0] = int(userinfo[i][0])
        userinfo[i][1] = str(userinfo[i][1])
        userinfo[i][2] = int(userinfo[i][2])
        userinfo[i][3]=ExcelUntil.excel_data_to_list(userinfo[i][3])
        userinfo[i][4]=ExcelUntil.excel_data_to_list(userinfo[i][4])
        
    return userinfo

    
def admin_thread():

    clientList=setUserInfo()
#    clientList1=setUserInfo2()
    #for i in range(0,adminNum):        
    print 'starting at:', time.ctime() 
    threads = [] 
#    nloops = range(adminNum) 
  
    for i in range(0,len(clientList)):  # create all threads 

        t = threading.Thread(target=clientRun,args=(Qkm_HOST,clientList[i][1],clientList[i][2],clientList[i][3],clientList[i][4]))
#        t = threading.Thread(target=clientRun,args=(Qkm_HOST,UserName,UserTyp,KeyID))
        threads.append(t) 
  
    for i in range(0,len(clientList)):  # start all threads 
        threads[i].start() 
  
    for i in range(0,len(clientList)):  # wait for completion 
        threads[i].join() 
  
    print 'all DONE at:', time.ctime()   
#
##�ͻ��˽����ȴ��������������ͱ���    
def clientRun(host_ip,user_name,user_typ,key_id,authid):
#    print '---clientRun----key_id:',key_id
    print '---clientRun----authid:',authid
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
    admin_packet.admin(s,authid)
    ack_key=admin_packet.get_sess_key()
    ack_key_id=admin_packet.get_sess_key_id()
#    while True:
        
        
#    qkmApply.qkmapply(s,ack_key,ack_key_id,user_name)
#    qkmGet.qkmget(s,ack_key,ack_key_id,user_name) 
    dianduidian.qkmapply(s,ack_key,ack_key_id,user_name)   
  
         
def multiThread(attend_num,clientList):

    threads = []    
    #�����������̣߳������ȴ�
    for i in range(attend_num-1):  # create all threads 
        t = threading.Thread(target=clientRun,args=(Akm_HOST,clientList[i][0],clientList[i][1],clientList[i][2]))
        threads.append(t)   
    for i in range(attend_num-1):  # start all threads 
        threads[i].start()
##    
    

if __name__ == '__main__':
#    attend_num=UserNum
    while True : 
        clientList=setUserInfo()         
        admin_thread()
#        time.sleep(0.5)


    
        