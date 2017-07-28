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
class   ProcPacket():
    def __init__(self,data,sess_key):
        #recv packet header
        self.version=''
        self.encry_alg=''
        self.key_id=''
        self.msg_len=0
        self.data=data
        #recv packet data 
        self.msg_typ=''
        self.req_id=0
        self.status=1
        self.auth_key_id=[]
        self.auth_key=[]
        self.sess_key_id=[]
        self.sess_key=sess_key
       
    def data_encry_pack(self,data_pack):
        
        key_iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        key_iv_pack = struct.pack('%dB'%len(key_iv), *key_iv)
        key_pack= struct.pack('%dB'%len(self.sess_key), *self.sess_key)
        ackBody_AES = AES.new(key_pack, AES.MODE_CBC, key_iv_pack)
        data_encryed=ackBody_AES.encrypt(tools.pad(data_pack))       
        self.msg_len=len(data_encryed)
        return data_encryed  
    
    def data_decry_pack(self,data_pack,sess_key):
        
        key_iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        key_iv_pack = struct.pack('%dB'%len(key_iv), *key_iv)
        key=sess_key
        key_pack= struct.pack('%dB'%len(key), *key)
        #print 'sess_key_pack',binascii.hexlify(key_pack)
        ackBody_AES = AES.new(key_pack, AES.MODE_CBC, key_iv_pack)
        #print 'rc_genPacket_data before decrypt AES',binascii.hexlify(data_pack)
        data_encryed=tools.unpad(ackBody_AES.decrypt(data_pack))
        #print 'rc_genPacket_data after decrypt AES',binascii.hexlify(data_encryed)
        #self.msg_len=len(data_encryed)
        #print 'rc_genPacket msg_len',self.msg_len
        return data_encryed  
    
                
    
    def unpack(self,recvData):          
        recv_buf=recvData
        print '******************recvData',binascii.hexlify(recv_buf)
        #print '*****len recvData',len(recvData)
        self.version,self.encry_alg,self.msg_len,data=struct.unpack('!BBH%ds'%(len(recvData)-4),recvData)
        #print 'self.version',self.version
        #print 'self.encry_alg',self.encry_alg
        print 'self.msg_len',self.msg_len
        #print 'left',right
        if(self.encry_alg == 0):            
            left,self.data=struct.unpack('!4s%ds'%(self.msg_len),recvData)
        else:
            left,self.key_id,self.data=struct.unpack('!4s16s%ds'%(self.msg_len),recvData)
            #print 'proc key_id',self.key_id       
        
        self.data=array.array('B', self.data)
        data_pack=struct.pack('%dB'%self.msg_len, *self.data)
        
        if(self.encry_alg ==1):
            self.data=self.data_decry_pack(data_pack,self.sess_key)
        
        self.msg_typ,data=struct.unpack('!B%ds'%(len(self.data)-1),self.data)       
        
    
    def getMsgType(self):
        self.unpack(self.data)
        return self.msg_typ
    


