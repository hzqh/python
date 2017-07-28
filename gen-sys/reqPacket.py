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


class ReqPacket(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        #packet header constractor
        self.version=1
        self.encry_alg=0
        self.key_id=[01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01]
        self.msg_len=0
        #packet data constractor
        self.msg_typ=101
        self.req_id=15
        self.username='node_child_p'
        self.username_len=len(self.username)
        self.pwd='node_child_parent'
        self.pwd_len=len(self.pwd)
        self.auth_key_id=[01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01]
        self.auth_key=[01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01]
        self.sess_key_id=[]
        self.sess_key=[]
        self.psdSHA256Hex=''
        self.data=''
        self.header=''
        self.pwdSHA256=''
     
    def set_pwd(self):
        psdSHA256Hex = hashlib.sha256(self.pwd.encode('utf-8')).hexdigest()    # ��sha256��ʽ����
        self.pwdSHA256= binascii.unhexlify(psdSHA256Hex)
        #print 'pwd256hex',self.pwdSHA256
        psdBin = [ord(x) for x in self.pwdSHA256]
# pasBin_pack = ",".join(psdBin)
        self.pwd_len = len(psdBin)
        #print 'pwd_len',self.pwd_len
    
    def set_sess_key_id(self):
        self.sess_key_id=tools.random_int_list(0,255,16)
        #print 'key_id',self.sess_key_id
    
    def set_sess_key(self):
        self.sess_key=tools.random_int_list(0,255,32)
        #print 'key',self.sess_key
    
    def data_pack(self):
        #username and passwd
        user_pwd=struct.pack('!BHB%dsB'%len(self.username),self.msg_typ,self.req_id,self.username_len,self.username, self.pwd_len)+self.pwdSHA256
        #auth key id
        auth_key_id_pack=struct.pack('%dB'%len(self.auth_key_id), *self.auth_key_id)
        #auth key 
        auth_key_pack=struct.pack('%dB'%len(self.auth_key), *self.auth_key)
        req_id_pack=struct.pack('!H',self.req_id)
        authKey_hmac256 = hmac.new(auth_key_pack, req_id_pack, digestmod=hashlib.sha256).digest() 
        # session key id
        sess_key_id_pack=struct.pack('%dB'%len(self.sess_key_id), *self.sess_key_id)
        #session key
        session_key_pack=struct.pack('%dB'%len(self.sess_key), *self.sess_key)
        self.data=user_pwd+auth_key_id_pack+authKey_hmac256+sess_key_id_pack+session_key_pack
        self.msg_len=len(self.data)
        #print user_pwd+auth_key_id_pack+authKey_hmac256+sess_key_id_pack+session_key_pack
      
    
    def head_pack(self):
       
        self.header=struct.pack('!BBH',self.version,self.encry_alg,self.msg_len)
        if(self.encry_alg==0):
            self.header=self.header
        else:
            key_id_pack=struct.pack('%dB'%(len(self.key_id)),*self.key_id)
            self.header=self.header+key_id_pack
        #print 'req self.header',binascii.hexlify(self.header) 
        
    def get_packet(self):
        self.set_pwd()
        self.set_sess_key_id()
        self.set_sess_key()
        self.data_pack()
        self.head_pack()
        return self.header+self.data
    
    def get_sess_key_id(self):
        return self.sess_key_id
    
    def get_sess_key(self):
        return self.sess_key

    


    
        