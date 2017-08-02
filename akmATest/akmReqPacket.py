# -*-coding:UTF-8-*- 
import struct
import binascii
from Crypto.Cipher import AES
import tools


class ReqPacket(object):
    #申请应用密钥请求报文

    def __init__(self):
        #报文头
        self.version=1
        self.encry_alg=1
        self.sess_key_id=''
        self.sess_key=''        
        self.msg_len=0
        #报文体
        self.msg_typ=0
        self.req_id=0
        self.reserve=0
        self.key_typ=0
        self.save=0
        self.save_time=16
        self.key_num=0
        self.key_len=0
        self.automatic=0
        self.auto_rate=0
        self.attend_num=0
        self.attend_name1_len=0
        self.attend_name1=0
        self.attend_name2_len=0
        self.attend_name2=0
        self.attend_name3_len=0
        self.attend_name3=0
        self.attend_name4_len=0
        self.attend_name4=0
        self.attend_name5_len=0
        self.attend_name5=0
        self.attend_name6_len=0
        self.attend_name6=0
        self.attend_name7_len=0
        self.attend_name7=0
        self.attend_name8_len=0
        self.attend_name8=0
        self.attend_name9_len=0
        self.attend_name9=0
        self.attend_name10_len=0
        self.attend_name10=0   
        self.attend_name11_len=0
        self.attend_name11=0 
        self.attend_name12_len=0 
        self.attend_name12=0
        self.attend_name13_len=0
        self.attend_name13=0
        self.attend_name14_len=0
        self.attend_name14=0
        self.attend_name15_len=0
        self.attend_name15=0
        self.attend_name16_len=0
        self.attend_name16=0
        self.attend_name17_len=0
        self.attend_name17=0
        self.attend_name18_len=0
        self.attend_name18=0
        self.attend_name19_len=0
        self.attend_name19=0
        self.attend_name20_len=0
        self.attend_name20=0
        self.sess_typ=0
        self.sess_attend_num=0
        self.sess_name_len=0
        self.sess_name=''
     
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
    
    def set_reserved(self,reserved):
        self.reserve=reserved
    
    def set_key_typ(self,key_typ):
        self.key_typ=key_typ
    
    def set_save(self,save):
        self.save=save
    
    def set_save_time(self,save_time):
        self.save_time=save_time
    
    def set_key_num(self,key_num):
        self.key_num=key_num
        
    def set_key_len(self,key_len):
        self.key_len=key_len
    
    def set_automatic(self,automatic):
        self.automatic=automatic
    
    def set_auto_rate(self,auto_rate):
        self.auto_rate=auto_rate 
    
    def set_userName(self,name):
        self.userName=name
    
    def set_userName_len(self,name_len):
        self.userName_len=name_len
    
    def set_attend_num(self,attend_num):
        self.attend_num=attend_num
    
    def set_attend_name_len_1(self,name_len):
        self.attend_name_len_1=name_len
    
    def set_attend_name_1(self,name):
        self.attend_name_1=name
        
    def set_attend_name_len_2(self,name_len):
        self.attend_name_len_2=name_len
    
    def set_attend_name_2(self,name):
        self.attend_name_2=name
    
    def set_attend_name_len_3(self,name_len):
        self.attend_name_len_3=name_len
    
    def set_attend_name_3(self,name):
        self.attend_name_3=name
    
    def set_attend_name_len_4(self,name_len):
        self.attend_name_len_4=name_len
    
    def set_attend_name_4(self,name):
        self.attend_name_4=name
        
    def set_attend_name_5(self,name):
        self.attend_name_5=name    
    def set_attend_name_len_5(self,name_len):
        self.attend_name_len_5=name_len
    
    def set_attend_name_6(self,name):
        self.attend_name_6=name
    def set_attend_name_len_6(self,name_len):
        self.attend_name_len_6=name_len  
              
    def set_attend_name_7(self,name):
        self.attend_name_7=name
    def set_attend_name_len_7(self,name_len):
        self.attend_name_len_7=name_len  
              
    def set_attend_name_8(self,name):
        self.attend_name_8=name
    def set_attend_name_len_8(self,name_len):
        self.attend_name_len_8=name_len        
        
    def set_attend_name_9(self,name):
        self.attend_name_9=name
    def set_attend_name_len_9(self,name_len):
        self.attend_name_len_9=name_len        
        
    def set_attend_name_10(self,name):
        self.attend_name_10=name
    def set_attend_name_len_10(self,name_len):
        self.attend_name_len_10=name_len        
        
    def set_attend_name_11(self,name):
        self.attend_name_11=name
    def set_attend_name_len_11(self,name_len):
        self.attend_name_len_11=name_len        
        
    def set_attend_name_12(self,name):
        self.attend_name_12=name  
    def set_attend_name_len_12(self,name_len):
        self.attend_name_len_12=name_len    
             
    def set_attend_name_13(self,name):
        self.attend_name_13=name  
    def set_attend_name_len_13(self,name_len):
        self.attend_name_len_13=name_len 
                   
    def set_attend_name_14(self,name):
        self.attend_name_14=name 
    def set_attend_name_len_14(self,name_len):
        self.attend_name_len_14=name_len          
        
    def set_attend_name_15(self,name):
        self.attend_name_15=name    
    def set_attend_name_len_15(self,name_len):
        self.attend_name_len_15=name_len          
            
    def set_attend_name_16(self,name):
        self.attend_name_16=name     
    def set_attend_name_len_16(self,name_len):
        self.attend_name_len_16=name_len          
           
    def set_attend_name_17(self,name):
        self.attend_name_17=name      
    def set_attend_name_len_17(self,name_len):
        self.attend_name_len_17=name_len          
          
    def set_attend_name_18(self,name):
        self.attend_name_18=name   
    def set_attend_name_len_18(self,name_len):
        self.attend_name_len_18=name_len          
             
    def set_attend_name_19(self,name):
        self.attend_name_19=name  
    def set_attend_name_len_19(self,name_len):
        self.attend_name_len_19=name_len          
              
    def set_attend_name_20(self,name):
        self.attend_name_20=name
    def set_attend_name_len_20(self,name_len):
        self.attend_name_len_20=name_len          
        
                                                                                
    def set_sess_typ(self,typ):
        self.sess_typ=typ
    
    def set_sess_attend_num(self,num):
        self.sess_attend_num=num
    
    def set_sess_name_len(self,len):
        self.sess_name_len=len
    
    def set_sess_name(self,name):
        self.sess_name=name
          
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
        data_pack=struct.pack('!BHBBBHBBBB',self.msg_typ,self.req_id,self.reserve,self.key_typ,self.save,self.save_time,self.key_num, \
                              self.key_len,self.automatic,self.auto_rate)
        name_pack=struct.pack('!B%dsH'%(self.userName_len),self.userName_len,self.userName,self.attend_num)
        
        attend_pack=''
        for i in range(1,self.attend_num+1):     
            attend_pack_tmp=struct.pack('B%ds'%(eval('self.attend_name_len_%s'%i)),eval('self.attend_name_len_%s'%i),eval('self.attend_name_%s'%i))
            print '**********',i
            print binascii.hexlify(attend_pack_tmp)
            attend_pack=attend_pack+attend_pack_tmp
            
        
        sess_pack=struct.pack('!BHB%ds'%(self.sess_name_len),self.sess_typ,self.sess_attend_num,self.sess_name_len,self.sess_name)
        
        data_pack=data_pack+name_pack+attend_pack+sess_pack
        #data_pack=data_pack+name_pack+sess_pack
        
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
        #print 'req self.header',binascii.hexlify(self.header) 
        return self.header
        
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

    


class ObtReqPacket(object):
    #获取应用密钥请求报文
    
    def __init__(self):
        #报文头
        self.version=1
        self.encry_alg=1
        self.key_id=''
        self.sess_key_id=''
        self.sess_key=''        
        self.msg_len=0
        #报文体
        self.msg_typ=0
        self.req_id=0
        self.key_num=0
        self.key_lem=0
        self.key_userName_len=0
        self.key_userName=0
        self.key_id_list=[]
    
     
    def set_sess_key_id(self,key_id):
        self.sess_key_id=key_id
   
    def set_sess_key(self,key):
        self.sess_key=key

    def set_version(self,version):
        self.version=version
        
    def set_encry_alg(self,encry_alg):
        self.encry_alg=encry_alg
    
    def set_msg_typ(self,msg_typ):
        self.msg_typ=msg_typ
    
    def set_req_id(self,req_id):
        self.req_id=req_id

    def set_key_num(self,key_num):
        self.key_num=key_num
    
    def set_key_len(self,key_len):
        self.key_len=key_len
    
    def set_userName_len(self,userName_len):
        self.userName_len=userName_len
    
    def set_userName(self,userName):
        self.userName=userName
    
    def set_key_id_list(self,key_id_list):
        self.key_id_list=key_id_list  
    
    def data_encry_pack(self,data_pack):
        
        print 'sess key',self.sess_key
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
        print 'self.username',self.userName
        print 'self.key_id_List',self.key_id_list
        data_pack=struct.pack('!BHBBB%ds'%(self.userName_len),self.msg_typ,self.req_id,self.key_num,self.key_len,self.userName_len,self.userName)
        print '**********data_pack',binascii.hexlify(data_pack)
        key_id_list_pack=struct.pack('%dB'%len(self.key_id_list), *self.key_id_list)
        print '*******key_id_list',binascii.hexlify(key_id_list_pack)
        data_pack=data_pack+key_id_list_pack
        print binascii.hexlify(key_id_list_pack)
        
        self.msg_len=len(data_pack)        
        return data_pack
                      
    def head_pack(self):      
        self.header=struct.pack('!BBH',self.version,self.encry_alg,self.msg_len)
        if(self.encry_alg==0):
            self.header=self.header
        else:
            key_id_pack=struct.pack('%dB'%(len(self.sess_key_id)),*self.sess_key_id)
            self.header=self.header+key_id_pack
        #print 'req self.header',binascii.hexlify(self.header) 
        return self.header
        
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



class ModReqPacket(object):
    #修改应用密钥请求报文

    def __init__(self):
        #报文头
        self.version=1
        self.encry_alg=1
        self.sess_key_id=''
        self.sess_key=''        
        self.msg_len=0
        #报文体
        self.msg_typ=0
        self.req_id=0
        self.modify_typ=0
        self.attend_num=0
        self.attend_name1_len=0
        self.attend_name1=0
        self.attend_name2_len=0
        self.attend_name2=0
        self.attend_name3_len=0
        self.attend_name3=0
        self.attend_name4_len=0
        self.attend_name4=0
        self.attend_name5_len=0
        self.attend_name5=0
        self.attend_name6_len=0
        self.attend_name6=0
        self.attend_name7_len=0
        self.attend_name7=0
        self.attend_name8_len=0
        self.attend_name8=0
        self.attend_name9_len=0
        self.attend_name9=0
        self.attend_name10_len=0
        self.attend_name10=0     
     
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
    
    def set_reserved(self,reserved):
        self.reserve=reserved

    def set_modify_typ(self,modify_typ):
        self.modify_typ=modify_typ

    def set_sess_id(self,sess_id):            #SessionID
        self.sess_id=sess_id
                    
    def set_key_typ(self,key_typ):
        self.key_typ=key_typ
    
    def set_save(self,save):
        self.save=save
    
    def set_save_time(self,save_time):
        self.save_time=save_time
    
    def set_key_num(self,key_num):
        self.key_num=key_num
        
    def set_key_len(self,key_len):
        self.key_len=key_len
    
    def set_automatic(self,automatic):
        self.automatic=automatic
    
    def set_auto_rate(self,auto_rate):
        self.auto_rate=auto_rate 
    
    def set_userName(self,name):
        self.userName=name
    
    def set_userName_len(self,name_len):
        self.userName_len=name_len
    
    def set_attend_num(self,attend_num):
        self.attend_num=attend_num
    
    def set_attend_name_len_1(self,name_len):
        self.attend_name_len_1=name_len
    
    def set_attend_name_1(self,name):
        self.attend_name_1=name
        
    def set_attend_name_len_2(self,name_len):
        self.attend_name_len_2=name_len
    
    def set_attend_name_2(self,name):
        self.attend_name_2=name
    
    def set_attend_name_len_3(self,name_len):
        self.attend_name_len_3=name_len
    
    def set_attend_name_3(self,name):
        self.attend_name_3=name
    
    def set_attend_name_len_4(self,name_len):
        self.attend_name_len_4=name_len
    
    def set_attend_name_4(self,name):
        self.attend_name_4=name
    
    def set_attend_name_len_5(self,name_len):
        self.attend_name_len_5=name_len
    
    def set_attend_name_5(self,name):
        self.attend_name_5=name
    
    def set_sess_typ(self,typ):
        self.sess_typ=typ
    
    def set_sess_attend_num(self,num):
        self.sess_attend_num=num
    
    def set_sess_name_len(self,len):
        self.sess_name_len=len
    
    def set_sess_name(self,name):
        self.sess_name=name
          
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
        data_pack=struct.pack('!BHB16B',self.msg_typ,self.req_id,self.modify_typ,*self.sess_id)
#        name_pack=struct.pack('B%dsH'%(self.userName_len),self.userName_len,self.userName,self.attend_num)
        name_pack=struct.pack('!H',self.attend_num)        
        attend_pack=''
        for i in range(1,self.attend_num+1):     
            attend_pack_tmp=struct.pack('B%ds'%(eval('self.attend_name_len_%s'%i)),eval('self.attend_name_len_%s'%i),eval('self.attend_name_%s'%i))
            print '**********',i
            print binascii.hexlify(attend_pack_tmp)
            attend_pack=attend_pack+attend_pack_tmp
            
        
#        sess_pack=struct.pack('BHB%ds'%(self.sess_name_len),self.sess_typ,self.sess_attend_num,self.sess_name_len,self.sess_name)
        
#        data_pack=data_pack+name_pack+attend_pack+sess_pack
        data_pack=data_pack+name_pack+attend_pack
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
        #print 'req self.header',binascii.hexlify(self.header) 
        return self.header
        
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

    
    
        