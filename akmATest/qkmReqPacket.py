# -*-coding:UTF-8-*- 
import struct
import binascii
from Crypto.Cipher import AES
import tools


class ReqPacket(object):
    #量子密钥密钥服务请求报文

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
        self.get_typ=0
        self.key_typ=0
        self.key_num=0
        self.key_len=16
        self.specif=0
        self.userName_len=0
        self.userName='node_child'
        self.key_id_list=[]
        self.peer_num=0
        self.reserved1=0
        self.reserved2=0
        self.peer_len_1=0
        self.peer_name_1=''
        self.peer_len_2=0
        self.peer_name_2=''
        self.peer_len_3=0
        self.peer_name_3=''
        self.peer_len_4=0
        self.peer_name_4=''
        self.peer_len_5=0
        self.peer_name_5=''   
     
    def set_sess_key_id(self,key_id):
        self.sess_key_id=key_id
        #print 'key_id',self.sess_key_id    
    def set_sess_key(self,key):
        self.sess_key=key
        #print 'key',self.sess_key
    def set_version(self,version):
        self.version=version
        
    def set_encry_alg(self,encry_alg):
        self.encry_alg=encry_alg
    
    def set_msg_typ(self,msg_typ):
        self.msg_typ=msg_typ
    
    def set_req_id(self,req_id):
        self.req_id=req_id
    
    def set_get_typ(self,typ):
        self.get_typ=typ
    
    def set_userName(self,name):
        self.userName=name
    
    def set_userName_len(self,name_len):
        self.userName_len=name_len
        
    def set_key_id_list(self,key_id_list):
        self.key_id_list=key_id_list
    
    def set_reserved1(self,reserved):
        self.reserved1=reserved
    
    def set_reserved2(self,reserved):
        self.reserved2=reserved
    
    def set_key_typ(self,key_typ):
        self.key_typ=key_typ
    
    def set_key_num(self,num):
        self.key_num=num
    
    def set_key_len(self,len):
        self.key_len=len
    
    def set_specified(self,specified):
        self.specif=specified
    
    def set_peer_num(self,num):
        self.peer_num=num
    
    def set_peer_name_1(self,name):
        self.peer_name_1=name
    
    def set_peer_name_2(self,name):
        self.peer_name_2=name
    
    def set_peer_name_3(self,name):
        self.peer_name_3=name
    
    def set_peer_name_4(self,name):
        self.peer_name_4=name
    
    def set_peer_name_5(self,name):
        self.peer_name_5=name
    
    def set_peer_len_1(self,len):
        self.peer_len_1=len
    
    def set_peer_len_2(self,len):
        self.peer_len_2=len
    
    def set_peer_len_3(self,len):
        self.peer_len_4=len
    
    def set_peer_len_4(self,len):
        self.peer_len_4=len
    
    def set_peer_len_5(self,len):
        self.peer_len_5=len
          
    def data_encry_pack(self,data_pack):
        
        key_iv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        key_iv_pack = struct.pack('%dB'%len(key_iv), *key_iv)
        key_pack= struct.pack('%dB'%len(self.sess_key), *self.sess_key)
        #print '***********sess_key_pack',binascii.hexlify(key_pack)
        ackBody_AES = AES.new(key_pack, AES.MODE_CBC, key_iv_pack)
        print 'req_Packet_data before AES',binascii.hexlify(data_pack)
        data_encryed=ackBody_AES.encrypt(tools.pad(data_pack))
        print 'req_Packet_data after AES',binascii.hexlify(data_encryed)
        self.msg_len=len(data_encryed)
        #print 'req_Packet msg_len after AES',self.msg_len
        return data_encryed 
    
    def data_pack(self):
        #username and passwd
        data_pack=struct.pack('!BHBBBBBH%ds'%len(self.userName),self.msg_typ,self.req_id,self.get_typ,self.key_typ,self.key_num,self.key_len,self.specif,self.userName_len,self.userName)
        print '** data pack',binascii.hexlify(data_pack)
        if(self.get_typ==1):
            if(self.specif==1):
                key_id_list_pack=struct.pack('%dB'%len(self.key_id_list), *self.key_id_list)
                data_pack=data_pack+key_id_list_pack
            else:
                data_pack=data_pack
        elif(self.get_typ==0):
            if(self.specif==0):
                peer_part_pack=struct.pack('!BBH',self.peer_num,self.reserved1,self.reserved2)
                for i in range(1,self.peer_num+1):     
                    peer_pack_tmp=struct.pack('!H%ds'%(eval('self.peer_len_%s'%i)),eval('self.peer_len_%s'%i),eval('self.peer_name_%s'%i))
                    peer_part_pack=peer_part_pack+peer_pack_tmp
                data_pack=data_pack+peer_part_pack
            elif(self.specif==1):
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
        print 'gen packet data encryed data',binascii.hexlify(self.data)
        print 'gen packet data encryed header',binascii.hexlify(self.header)
        str=self.header+self.data
        return self.header+self.data        
    
    def get_sess_key_id(self):
        return self.sess_key_id
    
    def get_sess_key(self):
        return self.sess_key

    


    
        