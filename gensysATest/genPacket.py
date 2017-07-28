# -*-coding:UTF-8-*- 
import struct
import sys
import binascii
import ctypes
import math
import tools
import array
from base64 import b16encode
from email.base64mime import body_decode
from Crypto.Cipher import AES
import tools
import time



class GenPacket(object):
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
        self.key_id=[01,01,01,01,01,01,01,01,01,01,01,01,01,01,01,01]
        self.msg_len=0
        #packet data constractor
        self.msg_typ=201
        self.req_id=1
        self.reserved=0
        self.key_typ=1
        self.key_num=1
        self.key_len=32
        self.key_id_len=16
        self.specif=1
        self.local_user_id=1003000
        self.remote_user_id=1010000
        self.key_id_list=[]
        self.key_list=[]
        self.data=[]
        self.sess_key=''
        self.sess_key_id=''
        #self.key_id_list_pack=[]   
    #def set_key_id_rand(self):
    #    for i in range(0,self.key_num):
    #        key_id_list=tools.random_int_list(0,255,16)
    #        self.key_id_list.append(key_id_list)
    #    print 'key_id_list',self.key_id_list
    
    def set_key_id_rand(self):
        for i in range(0,self.key_num):
            time.sleep(1)
            now=tools.getTimeStamp()
            key_id=[]
            key_id[0:16]=array.array('B', now)
            print 'key_id %d'%i,key_id[0:16] 
            self.key_id_list.extend(key_id[0:16])
            
        print 'key_id_list',self.key_id_list
        #self.key_id_list=[50, 48, 49, 55, 49, 52, 53, 49, 54, 53, 53, 50, 56, 56, 54, 54, 50, 48, 49, 55, 49, 52, 53, 49, 54, 53, 53, 50, 57, 56, 54, 54]
        #self.key_id_list=[50, 48, 49, 55, 49, 51, 55, 49, 55, 53, 54, 48, 55, 50, 51, 48, 50, 48, 49, 55, 49, 51, 55, 49, 55, 53, 54, 48, 55, 50, 51, 48]                
    
    def set_key_id_list(self,key_id_list):
        self.key_id_list=key_id_list
        
    
    def data_encry_pack(self,data_pack):
        
        key_iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        key_iv_pack = struct.pack('%dB'%len(key_iv), *key_iv)
        key_pack= struct.pack('%dB'%len(self.sess_key), *self.sess_key)
        print '***********sess_key_pack',binascii.hexlify(key_pack)
        ackBody_AES = AES.new(key_pack, AES.MODE_CBC, key_iv_pack)
        print 'genPacket_data before AES',binascii.hexlify(data_pack)
        print 'genPacket msg_len befor AES',len(data_pack)
        data_encryed=ackBody_AES.encrypt(tools.pad(data_pack))
        print 'genPacket_data after AES',binascii.hexlify(data_encryed)
        self.msg_len=len(data_encryed)
        print 'genPacket msg_len after AES',self.msg_len
        return data_encryed  
    
    def data_pack(self):
        #get packet segment autil specif
        local_userid_pack=struct.pack('!Q',self.local_user_id)
        print 'local_userid_pack',binascii.hexlify(local_userid_pack)
        remote_userid_pack=struct.pack('!Q',self.remote_user_id)
        print 'remote_userid_pack',binascii.hexlify(remote_userid_pack)       
        self.local_user_id=array.array('B',local_userid_pack)
        self.remote_user_id=array.array('B',remote_userid_pack)
        pack_tmp=struct.pack('!BHBBBBB',self.msg_typ,self.req_id,self.reserved,self.key_typ,self.key_num,self.key_len,self.specif)
        local_user_pack=struct.pack('%dB'%len(self.local_user_id), *self.local_user_id)
        remote_user_pack=struct.pack('%dB'%len(self.remote_user_id), *self.remote_user_id)
        print 'self.key num',self.key_num
        key_id_list_pack=struct.pack('%dB'%(self.key_id_len*self.key_num),*self.key_id_list)               
        self.data=pack_tmp+local_user_pack+remote_user_pack+key_id_list_pack   
        #print 'gen packet  data t_pack',binascii.hexlify(self.data)       
        self.msg_len=len(self.data)
        return self.data
    
    def head_pack(self):  
        self.header=struct.pack('!BBH',self.version,self.encry_alg,self.msg_len)
        if(self.encry_alg==0):
            self.header=self.header
        else:
            key_id_pack=struct.pack('%dB'%(len(self.sess_key_id)),*self.sess_key_id)
            #print 'gen packet key_id_pack',
            self.header=self.header+key_id_pack
        print 'gen self.header',binascii.hexlify(self.header)
    
    def set_version(self,version):
        self.version=version
        
    def set_encry_alg(self,encry_alg):
        self.encry_alg=encry_alg
    
    def set_sess_key(self,key):
        self.sess_key=key
    
    def set_sess_key_id(self,key_id):
        self.sess_key_id=key_id
    
    def set_msg_typ(self,msg_typ):
        self.msg_typ=msg_typ
    
    def set_req_id(self,req_id):
        self.req_id=req_id
    
    def set_reserved(self,reserved):
        self.reserved=reserved
    
    def set_key_typ(self,typ):
        self.key_typ=typ
    
    def set_key_num(self,num):
        self.key_num=num
    
    def set_key_len(self,len):
        self.key_len=len
    
    def set_specified(self,specified):
        self.specif=specified
    
    def set_local_user_id(self,local_user_id):
        self.local_user_id=local_user_id
    
    def set_remote_user_id(self,remote_user_id):
        self.remote_user_id=remote_user_id
    
    def get_key_id_list(self):
        return self.key_id_list
    
    def get_req_id(self):
        return self.req_id
    
    def get_key_typ(self):
        return self.key_typ
    
    def get_key_num(self):
        return self.key_num
    
    def get_key_len(self):
        return self.key_len
    
    def get_local_user_id(self):
        return self.local_user_id
    
    def get_remote_user_id(self):
        return self.remote_user_id
    
    def get_reserved(self):
        return self.reserved
    
    def get_specified(self):
        return self.specif
    
    def get_msg_len(self):
        return self.msg_len

    def get_packet(self,sys_flag):
        if(sys_flag==0):
            self.set_key_id_rand()
        else:
            print 'sys part'
        self.data=self.data_pack()
        if (self.encry_alg != 0):
            self.data=self.data_encry_pack(self.data)
        #self.msg_len=40
        self.head_pack()
        #print 'gen packet data encryed',binascii.hexlify(self.data)
        return self.header+self.data
        
