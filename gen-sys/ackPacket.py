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
        self.key_id=[]
        self.key=[]
        self.msg_len=0
        #packet data constractor
        self.msg_typ=103
        self.req_id=0
        self.status=0
        self.data=[]
        self.header=[]
    
    def data_encry_pack(self):
        self.data=struct.pack('!BHB',self.msg_typ,self.req_id,self.status)
        ack_iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ack_iv_pack = struct.pack('%dB'%len(ack_iv), *ack_iv)
        ack_key_pack= struct.pack('%dB'%len(self.key), *self.key)
        #print 'ack_key_pack',binascii.hexlify(ack_key_pack)
        ackBody_AES = AES.new(ack_key_pack, AES.MODE_CBC, ack_iv_pack)
        #print 'ack_data before AES',binascii.hexlify(self.data)
        self.data=ackBody_AES.encrypt(tools.pad(self.data))
        #print 'ack_data after AES',binascii.hexlify(self.data)
        self.msg_len=len(self.data)
        #print 'ack msg_len',self.msg_len
    
    def head_pack(self):
        
        #print 'ack encry_alg',self.encry_alg
        #print 'msg_len %d' %self.msg_len
        self.header=struct.pack('!BBH',self.version, self.encry_alg, self.msg_len)
        if(self.encry_alg == 0):
            self.header=self.header
        else:
            key_id_pack=struct.pack('%dB'%(len(self.key_id)),*self.key_id)
            #self.header=struct.pack('!BBH',self.version,self.encry_alg,self.msg_len)
            self.header=self.header+key_id_pack
        
        
    def set_req_id(self,req_id):
        self.req_id=req_id
    
    def set_key_id(self,key_id):
        self.key_id=key_id
    
    def set_key(self,key):
        self.key=key
        
    def set_status(self,status):
        self.status=status  
        
    def get_packet(self):
        self.data_encry_pack()
        self.head_pack()
        #print 'ack header',binascii.hexlify(self.header)
        return self.header+self.data
    