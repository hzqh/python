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

class   PushReqPacket():
    #量子密钥密钥服务确认反馈报文    
    def __init__(self):
        #recv packet header
        self.version=''
        self.encry_alg=''
        self.key_id=''
        self.sess_key_id=''
        self.sess_key=''
        #recv packet data 
        self.msg_typ=''
        self.req_id=''
        self.specified=0
        self.key_num=''
        self.key_len=''
        self.sess_len=''
        self.sess_name=''
        self.key_id_list=[]
        self.version_2=1
        self.encry_alg_2=1
        self.msg_len=0
        self.key_id_2=[]
        self.key_list=[]
        self.data=[]
     
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
        #print 'recvData',binascii.hexlify(recvData)
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
        
        self.msg_typ,self.req_id,self.specified,self.key_num,self.key_len,self.sess_len,right=struct.unpack('!BHBBBB%ds'%(len(self.data)-7),self.data)
        left,self.userName,self.key_id_list,self.version_2,self.encry_alg_2,self.msg_len,self.encry_alg_2,self.key_list=struct.unpack('!7s%ds%dsBBH16s%ds'%(self.sess_len,self.key_num*16,self.key_num*32),self.data)
    
        
        #print 'self.key_num',self.key_num
        #print 'self.sess_len',self.sess_len
        self.userName=array.array('B', self.userName)
        self.key_id_list=array.array('B',self.key_id_list)
        self.key_list=array.array('B',self.key_list)
        #self.msg_typ,self.req_id,self.status,self.key_typ,self.key_num,self.key_len,self.reserved,self.local_user_id,self.remote_user_id,self.key_id_list=\
        #struct.unpack('!BHBBBBB8s8s%ds'%(len(self.data_decryped)-24),self.data_decryped)
    
    def getResult(self):
        return self.status
    
    def get_key_id_list(self):
        return self.key_id_list
    
    def get_key_list(self):
        return self.key_list
    
    def get_req_id(self):
        return self.req_id
    
    def get_specified(self):
        return self.specified
    
    def get_key_num(self):
        return self.key_num
    
    def get_key_len(self):
        return self.key_len
    
    def set_sess_key(self,key):
        self.sess_key=key
    
    def get_sessName_len(self):
        return self.sess_len
    
    def get_sessName(self):
        return self.sess_name
    
    def get_version_2(self):
        return self.version_2
    
    def get_encry_alg_2(self):
        return self.encry_alg_2
    
    def get_msg_len(self):
        return self.msg_len
    
    def get_msg_typ(self):
        return self.msg_typ
    
    def get_key_id_2(self):
        return self.key_id_2
    
    



        