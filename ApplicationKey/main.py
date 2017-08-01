# -*-coding:UTF-8-*- 

import akm
import akmRcPacket
#from time import sleep

class akmIntime():
    def start(self):
        
        Qkm_HOST='192.168.91.112'
        Akm_HOST='192.168.91.113'
        UserTyp=1
        UserName='client_wm1'
        UserName1='client_wm2'
        UserName2='client_wm3'
        Key_ID_0=[01,01,01,01,01,01,01,01,01,01,01,01,01,01,00,01]
        Key_ID_1=[01,01,01,01,01,01,01,01,01,01,01,01,01,01,00,02]
        Key_ID_2=[01,01,01,01,01,01,01,01,01,01,01,01,01,01,00,03]
        UserNum=2
    #     #用户0
    #     UserName='node_lq'
    #     Key_ID=[01,01,01,01,01,01,01,01,01,01,01,01,01,03,02,01]
    #     #用户1   应用密钥服务的用户A
    #     UserName1='client_lq3'
    #     Key_ID_1=[01,01,01,01,01,01,01,01,01,01,01,01,01,03,01,03]   
    #     #用户2   应用密钥服务的用户B
    #     UserName2='client_lq4'
    #     Key_ID_2=[01,01,01,01,01,01,01,01,01,01,01,01,01,03,01,04]
         
        #申请量子密钥，为后续应用密钥加密，做储备
#        qkm.getQkmKey(Qkm_HOST,UserName1,UserTyp,Key_ID_1)
        #qkm.getQkmKey(Qkm_HOST,UserName2,UserTyp,Key_ID_2)
        #sleep(10)
        #申请创建应用密钥
    #    akm.getAkmKey(Akm_HOST,UserName1,UserTyp,Key_ID_1)
    #    rc_packet=akmRcPacket.RecvPacket()
    #    rc_key_id_list=rc_packet.get_key_id_list()
    #    akm.getAkmKey(Akm_HOST,UserName1,UserTyp,Key_ID_1)
        #获取获取应用密钥
        return akm.obtAkmKey(Akm_HOST,UserName2, UserTyp,Key_ID_2,akm.getAkmKey(Akm_HOST,UserName1,UserTyp,Key_ID_1)) #将申请和获取一起跑
        #修改应用密钥服务
        #akm.ModAkmKey(Akm_HOST,UserName1,UserTyp,Key_ID_1)