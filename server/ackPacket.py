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


class AckPacket(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        #packet header constractor
        self.version=1
        self.encry_alg=1
        self.sess_key_id=''
        self.sess_key=''        
        self.msg_len=0
        #packet data constractor
        self.msg_typ=0
        self.req_id=0
        self.status=0
        self.key_typ=0
        self.key_num=0
        self.key_len=16
        self.get_typ=0
        self.userName_len=1
        self.userName='5'
        self.key_id_list=[]
        
     

    def set_sess_key_id(self,key_id):
        self.sess_key_id=key_id
        #print 'key_id',self.sess_key_id    
    def set_sess_key(self,key):
        self.sess_key=key
        #print 'key',self.s
            #print 'key',self.sess_key
    def set_version(self,version):
        self.version=version
        
    def set_encry_alg(self,encry_alg):
        self.encry_alg=encry_alg
    
    def set_msg_typ(self,msg_typ):
        self.msg_typ=msg_typ
    
    def set_req_id(self,req_id):
        self.req_id=req_id
    
    def set_status(self,status):
        self.status=status

    def set_key_typ(self,typ):
        self.key_typ=typ
    
    def set_key_num(self,num):
        self.key_num=num   
    
    def set_key_len(self,len):
        self.key_len=len
    
    def set_get_typ(self,typ):
        self.get_typ=typ
    
    def set_userName(self,name):
        self.userName=name
    
    def set_userName_len(self,name_len):
        self.userName_len=name_len
        
    def set_key_id_list(self,key_id_list):
        self.key_id_list=key_id_list
          
    def data_encry_pack(self,data_pack):
        
        key_iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        key_iv_pack = struct.pack('%dB'%len(key_iv), *key_iv)
        key_pack= struct.pack('%dB'%len(self.sess_key), *self.sess_key)
        #print '***********sess_key_pack',binascii.hexlify(key_pack)
        ackBody_AES = AES.new(key_pack, AES.MODE_CBC, key_iv_pack)
#        print 'ack_Packet_data before AES',binascii.hexlify(data_pack)
        data_encryed=ackBody_AES.encrypt(tools.pad(data_pack))
#        print 'ack_Packet_data after AES',binascii.hexlify(data_encryed)
        self.msg_len=len(data_encryed)
#        print 'ack_Packet msg_len after AES',self.msg_len
        return data_encryed 
    
    def data_pack(self):
        #username and passwd
        data_pack=struct.pack('!BHBBBBBH%ds'%len(self.userName),self.msg_typ,self.req_id,self.status,self.key_typ,self.key_num,self.key_len,self.get_typ,self.userName_len,self.userName)
#        print '** data pack',binascii.hexlify(data_pack) 
        key_id_list_pack=struct.pack('%dB'%len(self.key_id_list), *self.key_id_list)
        data_pack=data_pack+key_id_list_pack               
        self.msg_len=len(data_pack)        
        #print '*****peer_part_pack',binascii.hexlify(peer_part_pack)
        #print '*****peer_tmp_pack',binascii.hexlify(peer_tmp_pack)      
        return data_pack
                      
    def head_pack(self):      
        self.header=struct.pack('!BBH',self.version,self.encry_alg,self.msg_len)
        if(self.encry_alg==0):
            self.header=self.header
        else:
            key_id_pack=struct.pack('%dB'%(len(self.sess_key_id)),*self.sess_key_id)
            self.header=self.header+key_id_pack
        return self.header
        #print 'req self.header',binascii.hexlify(self.header) 
        
    def get_packet(self):
        self.data=self.data_pack()
        if (self.encry_alg != 0):
            self.data=self.data_encry_pack(self.data)
        #self.msg_len=40
        self.header=self.head_pack()
#        print 'gen packet data encryed data',binascii.hexlify(self.data)
#        print 'gen packet data encryed header',binascii.hexlify(self.header)
        str=self.header+self.data
        return self.header+self.data        
    
    def get_sess_key_id(self):
        return self.sess_key_id
    
    def get_sess_key(self):
        return self.sess_key

    


    
        