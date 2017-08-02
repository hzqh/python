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
import tools


class   RecvPacket():
    #申请应用密钥反馈报文
    def __init__(self):
        #recv packet header
        self.version=''
        self.encry_alg=''
        self.key_id=''
        self.sess_key_id=''
        self.sess_key=''
        self.msg_len=0
        #recv packet data 
        self.msg_typ=''
        self.req_id=''
        self.status=2
        self.key_num=''
        self.key_len=''
        self.key_id_list=[]
        self.version_2=1
        self.encry_alg_2=1
        self.msg_len_2=0
        self.key_id_2=[]
        self.key_list=[]
        self.data=[]
        self.sess_key_id=''
        self.sess_key=''
        self.sess_id=''
    
    def data_decry_pack(self,data_pack):
        
        key_iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        key_iv_pack = struct.pack('%dB'%len(key_iv), *key_iv)
        key_pack= struct.pack('%dB'%len(self.sess_key), *self.sess_key)
        #print 'sess_key_pack',binascii.hexlify(key_pack)
        ackBody_AES = AES.new(key_pack, AES.MODE_CBC, key_iv_pack)
        print 'rc_Packet_data before decrypt AES',binascii.hexlify(data_pack)
        data_encryed=tools.unpad(ackBody_AES.decrypt(data_pack))
        print 'rc_Packet_data after decrypt AES',binascii.hexlify(data_encryed)
        #self.msg_len=len(data_encryed)
        #print 'rc_genPacket msg_len',self.msg_len
        return data_encryed  
    
    
    def unpack(self,recvData):    
        recv_buf=recvData
        print 'recvData',binascii.hexlify(recvData)
        self.version,self.encry_alg,self.msg_len,right=struct.unpack('!BBH%ds'%(len(recvData)-4),recvData)
        #print 'self.version',self.version
        #print 'self.encry_alg',self.encry_alg
        #print 'self.msg_len',self.msg_len
        #key_id_list_len=self.key_id_len*self.key_num       
        if(self.encry_alg == 0):            
            left,self.data=struct.unpack('!4s%ds'%(self.msg_len),recvData)
        elif(self.encry_alg ==1):
            left,self.key_id,self.data=struct.unpack('!4s16s%ds'%(self.msg_len),recvData)
        
        self.data=array.array('B', self.data)
        self.data=struct.pack('%dB'%self.msg_len, *self.data)
        
        if(self.encry_alg ==1):
            self.data=self.data_decry_pack(self.data)
        
        self.msg_typ,self.req_id,self.status,right=struct.unpack('!BHB%ds'%(len(self.data)-4),self.data)
        print 'rc_packet msg_typ',self.msg_typ
        print 'rc_packet req_id',self.req_id
        print 'rc_packet status：申请创建应用密钥',self.status
        if(self.status == 0):
            left,self.sess_id,self.key_num,self.key_len,right=struct.unpack('!4s16sBB%ds'%(len(self.data)-22),self.data)
            left,self.key_id_list,self.version_2,self.encry_alg_2,self.msg_len_2,self.key_id_2,self.key_list=struct.unpack('!22s%dsBBH16s%ds'%(self.key_num*16,self.key_num*32),self.data)
            self.sess_id=array.array('B',self.sess_id)
            print '**sess_id:申请创建反馈报文中SessionID：**',self.sess_id
            self.key_id_list=array.array('B',self.key_id_list)
            key_id_list = binascii.hexlify(self.key_id_list)
            print 'key_id_list:申请创建应用密钥的密钥id:',binascii.hexlify(self.key_id_list)
            self.key_id_list = self.key_id_list.tolist()
#            return key_id_list
#            self.key_list=array.array('B',self.key_list)
            
        #self.msg_typ,self.req_id,self.status,self.key_typ,self.key_num,self.key_len,self.reserved,self.local_user_id,self.remote_user_id,self.key_id_list=\
        #struct.unpack('!BHBBBBB8s8s%ds'%(len(self.data_decryped)-24),self.data_decryped)
    
    def getResult(self):
        return self.status
    
    def get_key_id_list(self):
        return self.key_id_list
    
    def get_key_list(self):
        if(self.encry_alg_2==2):
            self.sess_key_id=self.key_id_2
            self.key_list=self.data_decry_pack(self.key_list)
        return self.key_list
    
    def get_req_id(self):
        return self.req_id
    
    def get_get_typ(self):
        return self.get_typ
    
    def get_msg_typ(self):
        return self.msg_typ
    
    def get_key_typ(self):
        return self.key_typ
    
    def get_key_num(self):
        return self.key_num
    
    def get_key_len(self):
        return self.key_len
            
    def set_sess_key(self,key):
        self.sess_key=key
    
    def get_userName_len(self):
        return self.userName_len
    
    def get_userName(self):
        return self.userName
    
    def get_sess_id(self):
        return self.sess_id



class   ObtRecvPacket():
    #获取应用密钥反馈报文
    def __init__(self):
        #recv packet header
        self.version=''
        self.encry_alg=''
        self.key_id=''
        self.sess_key_id=''
        self.sess_key=''
        self.msg_len=0
        #recv packet data 
        self.msg_typ=''
        self.req_id=''
        self.status=2
        self.key_num=0
        self.key_len=0
        self.userName=''
        self.userName_len=0
        self.key_id_list=[]
        self.version_2=1
        self.encry_alg_2=1
        self.msg_len_2=0
        self.key_id_2=[]
        self.key_list=[]
        self.data=[]
        self.sess_key_id=''
        self.sess_key=''
 
    
    def data_decry_pack(self,data_pack):
        
        key_iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        key_iv_pack = struct.pack('%dB'%len(key_iv), *key_iv)
        key_pack= struct.pack('%dB'%len(self.sess_key), *self.sess_key)
        #print 'sess_key_pack',binascii.hexlify(key_pack)
        ackBody_AES = AES.new(key_pack, AES.MODE_CBC, key_iv_pack)
        print 'rc_Packet_data before decrypt AES',binascii.hexlify(data_pack)
        data_encryed=tools.unpad(ackBody_AES.decrypt(data_pack))
        print 'rc_Packet_data after decrypt AES',binascii.hexlify(data_encryed)
        #self.msg_len=len(data_encryed)
        #print 'rc_genPacket msg_len',self.msg_len
        return data_encryed  
    
    
    def unpack(self,recvData):    
        recv_buf=recvData
        print 'recvData',binascii.hexlify(recvData)
        self.version,self.encry_alg,self.msg_len,right=struct.unpack('!BBH%ds'%(len(recvData)-4),recvData)
        #print 'self.version',self.version
        #print 'self.encry_alg',self.encry_alg
        #print 'self.msg_len',self.msg_len
        #key_id_list_len=self.key_id_len*self.key_num       
        if(self.encry_alg == 0):            
            left,self.data=struct.unpack('!4s%ds'%(self.msg_len),recvData)
        elif(self.encry_alg ==1):
            left,self.key_id,self.data=struct.unpack('!4s16s%ds'%(self.msg_len),recvData)
        
        self.data=array.array('B', self.data)
        self.data=struct.pack('%dB'%self.msg_len, *self.data)
        
        if(self.encry_alg ==1):
            self.data=self.data_decry_pack(self.data)
        
        self.msg_typ,self.req_id,self.status,right=struct.unpack('!BHB%ds'%(len(self.data)-4),self.data)
        print 'rc_packet msg_typ',self.msg_typ
        print 'rc_packet req_id',self.req_id
        print 'rc_packet status：申请获取应用密钥',self.status
#        if(self.status == 0):
#            left,self.key_num,self.key_len,self.userName_len,right=struct.unpack('!4sBBB%ds'%(len(self.data)-7),self.data)
#            left,self.userName,self.key_id_list,self.version_2,self.encry_alg_2,self.msg_len_2,self.key_id_2,self.key_list= \
#            struct.unpack('!7s%ds%dsBBH16s%ds'%(self.userName_len,self.key_num*16,self.key_num*32),self.data)
#            self.userName=array.array('B',self.userName)
#            self.key_id_list=array.array('B',self.key_id_list)
#            self.key_list=array.array('B',self.key_list)
    
    def getResult(self):
        return self.status
    
    def get_key_id_list(self):
        return self.key_id_list
    
    def get_key_list(self):
        if(self.encry_alg_2==2):
            self.sess_key_id=self.key_id_2
            self.key_list=self.data_decry_pack(self.key_list)
        return self.key_list
    
    def get_req_id(self):
        return self.req_id
    
    def get_get_typ(self):
        return self.get_typ
    
    def get_msg_typ(self):
        return self.msg_typ
    
    def get_key_num(self):
        return self.key_num
    
    def get_key_len(self):
        return self.key_len
            
    def set_sess_key(self,key):
        self.sess_key=key
    
    def get_userName_len(self):
        return self.userName_len
    
    def get_userName(self):
        return self.userName


class   ModifyRecvPacket():
    #修改应用密钥反馈报文
    def __init__(self):
        #recv packet header
        self.version=''
        self.encry_alg=''
        self.key_id=''
        self.sess_key_id=''
        self.sess_key=''
        self.msg_len=0
        #recv packet data 
        self.msg_typ=''
        self.req_id=''
        self.status=2
        self.sess_id=''   #SessionID 创建应用密钥服务时返回
        self.data=[]
        self.sess_key_id=''
        self.sess_key=''
 
    
    def data_decry_pack(self,data_pack):
        
        key_iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        key_iv_pack = struct.pack('%dB'%len(key_iv), *key_iv)
        key_pack= struct.pack('%dB'%len(self.sess_key), *self.sess_key)
        #print 'sess_key_pack',binascii.hexlify(key_pack)
        ackBody_AES = AES.new(key_pack, AES.MODE_CBC, key_iv_pack)
        print 'rc_Packet_data before decrypt AES',binascii.hexlify(data_pack)
        data_encryed=tools.unpad(ackBody_AES.decrypt(data_pack))
        print 'rc_Packet_data after decrypt AES',binascii.hexlify(data_encryed)
        #self.msg_len=len(data_encryed)
        #print 'rc_genPacket msg_len',self.msg_len
        return data_encryed  
    
    
    def unpack(self,recvData):    
        recv_buf=recvData
        print 'recvData',binascii.hexlify(recvData)
        self.version,self.encry_alg,self.msg_len,right=struct.unpack('!BBH%ds'%(len(recvData)-4),recvData)
        #print 'self.version',self.version
        #print 'self.encry_alg',self.encry_alg
        #print 'self.msg_len',self.msg_len
        #key_id_list_len=self.key_id_len*self.key_num       
        if(self.encry_alg == 0):            
            left,self.data=struct.unpack('!4s%ds'%(self.msg_len),recvData)
        elif(self.encry_alg ==1):
            left,self.key_id,self.data=struct.unpack('!4s16s%ds'%(self.msg_len),recvData)
        
        self.data=array.array('B', self.data)
        self.data=struct.pack('%dB'%self.msg_len, *self.data)
        
        if(self.encry_alg ==1):
            self.data=self.data_decry_pack(self.data)
        
        self.msg_typ,self.req_id,self.status,right=struct.unpack('!BHB%ds'%(len(self.data)-4),self.data)
        print 'rc_packet msg_typ',self.msg_typ
        print 'rc_packet req_id',self.req_id
        print 'rc_packet status：修改应用密钥服务',self.status
        if(self.status == 0):
            left,self.sess_id,right=struct.unpack('%dB'%(len(self.data)-7),*self.data)
            self.sess_id=array.array('B',self.sess_id)
            print 'rc_packet sess_id',self.sess_id
    
    def getResult(self):
        return self.status

    def get_req_id(self):
        return self.req_id
    
    def get_msg_typ(self):
        return self.msg_typ
     
    def get_msg_typ(self):
        return self.modify_typ
           
#    def set_sess_key(self,key):
#        self.sess_key=key
    
    def get_sess_id(self):
        return self.sess_id
    
    def set_sess_key(self,key):
        self.sess_key=key


            

        