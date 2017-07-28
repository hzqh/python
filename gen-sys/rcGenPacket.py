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





class   RecvGenPacket():
    def __init__(self):
        #recv packet header
        self.version=''
        self.encry_alg=''
        self.key_id=''
        self.msg_len=0
        self.data=''
        #recv packet data 
        self.msg_typ=''
        self.req_id=''
        self.reserved=''
        self.key_typ=''
        self.key_num=''
        self.key_len=''
        self.key_id_len=16
        self.specif=''
        self.local_user_id=[]
        self.remote_user_id=[]
        self.key_id_list=[]
        self.key_list=[]
        self.data=[]
        self.sess_key_id=''
        self.sess_key=''
    
    def data_decry_pack(self,data_pack):
        
        key_iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        key_iv_pack = struct.pack('%dB'%len(key_iv), *key_iv)
        key_pack= struct.pack('%dB'%len(self.sess_key), *self.sess_key)
        print 'sess_key_pack',binascii.hexlify(key_pack)
        ackBody_AES = AES.new(key_pack, AES.MODE_CBC, key_iv_pack)
        print 'rc_genPacket_data before decrypt AES',binascii.hexlify(data_pack)
        data_encryed=tools.unpad(ackBody_AES.decrypt(data_pack))
        print 'rc_genPacket_data after decrypt AES',binascii.hexlify(data_encryed)
        #self.msg_len=len(data_encryed)
        #print 'rc_genPacket msg_len',self.msg_len
        return data_encryed  
    
    
    def unpack(self,recvData):    
        recv_buf=recvData
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
        data_pack=struct.pack('%dB'%self.msg_len, *self.data)
        
        if(self.encry_alg ==1):
            self.data=self.data_decry_pack(data_pack)
        
        self.msg_typ,self.req_id,self.status,right=struct.unpack('!BHB%ds'%(len(self.data)-4),self.data)
        print 'rc_gen_packet status',self.status
        if(self.status == 0):
            left,self.key_typ,self.key_num,self.key_len,self.reserved,self.local_user_id,self.remote_user_id,self.key_id_list=struct.unpack('!4sBBBB8s8s%ds'%(len(self.data)-24),self.data)
            #print 'self.req_id',self.req_id
            #print 'self.status',self.status
            self.local_user_id=array.array('B', self.local_user_id )
            self.remote_user_id=array.array('B', self.remote_user_id )
            self.key_id_list=array.array('B',self.key_id_list)
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
    
    def get_local_user_id(self):
        return self.local_user_id
    
    def get_remote_user_id(self):
        return self.remote_user_id
    
    def get_msg_typ(self):
        return self.msg_typ
    
    def get_key_typ(self):
        return self.key_typ
    
    def get_key_num(self):
        return self.key_num
    
    def get_key_len(self):
        return self.key_len
    
    def get_reserved(self):
        return self.reserved
            
    def set_sess_key(self,key):
        self.sess_key=key



            

        