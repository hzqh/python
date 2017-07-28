#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on 2017-7-17
@author: qih
Project:执行全部用例
'''
import random
import unittest
from clientTest import ClientAES1
from serverATest import qkmApply1
from serverATest import qkmGet1
from gensysATest import main
from ApplicationKey import main1
from serverATest import qkmApply2
from serverATest import qkmGet2
#import ClientAES1
import MySQLdb
from commonUntils import ExcelUntil
from commonUntils import DBConnection

from clientTest import ClientAES2
from clientTest import akmAccess
import ConfigParser


class autoTest(unittest.TestCase):   
    def setUp(self):
#        self.seq = range(10)
        
        print '---------------------------------------------------- -----------AT用例开始---------------------------------------------------'

    def test_access1(self):
        # make sure the shuffled sequence does not lose any elements
        print '-------------------------------------------------------------接入认证-qkm本地认证-用例开始--------------------------------------------'
        cf = ConfigParser.ConfigParser()
        cf.read('D:/workplace/PyTest-frame/qtec.conf')  
        conn = MySQLdb.connect(host=eval(cf.get('db1', 'host')),user=eval(cf.get('db1', 'user')),passwd=eval(cf.get('db1', 'passwd')),db=eval(cf.get('db1', 'db')),port=eval(cf.get('db1', 'port')),charset='utf8')
        cur = conn.cursor()
        hero = DBConnection.DBConn(eval(cf.get('db1', 'db')),conn,cur)
        result = hero.select("select * from connection_info where user_name = "+"'client_qh001'")
        if not result:        
            hero.insert("INSERT INTO `authentication_info` VALUES ('7000004', 'client_qh001', 'client_qh001', 'client_qh001', '1', '091945003b065c0d0a42', 0x01010101010101010101010101070104, 0x6677206465643565672772622B3E3565652D6532686064605F5F60652B742B68, 0x01010101010101010101010101010101, 0x6677206465643565672772622B3E3565652D6532686064605F5F60652B742B68, 0x01010101010101010101010101010101, 0x6677206465643565672772622B3E3565652D6532686064605F5F60652B742B68);")        
        test=ClientAES1.Clienttest1()
#        test.start()
        self.assertEqual( test.start(), 1)
        print '------------------------------------------------------------接入认证-qkm本地认证-用例结束----------------------------------------------'
        
    def test_access2(self):
        # make sure the shuffled sequence does not lose any elements
        cf = ConfigParser.ConfigParser()
        cf.read('D:/workplace/PyTest-frame/qtec.conf')  
        print '------------------------------------------------------------接入认证-qkm代理认证-用例开始-----------------------------------------------'
        conn = MySQLdb.connect(host=eval(cf.get('db1', 'host')),user=eval(cf.get('db1', 'user')),passwd=eval(cf.get('db1', 'passwd')),db=eval(cf.get('db1', 'db')),port=eval(cf.get('db1', 'port')),charset='utf8')
        cur = conn.cursor()
        hero = DBConnection.DBConn(eval(cf.get('db1', 'db')),conn,cur)
        hero.delete("delete from authentication_info where user_name = 'client_qh001'")
        test=ClientAES2.Clienttest2()
#        test.start()
        self.assertEqual( test.start(), 1)
        hero.insert("INSERT INTO `authentication_info` VALUES ('7000004', 'client_qh001', 'client_qh001', 'client_qh001', '1', '091945003b065c0d0a42', 0x01010101010101010101010101070104, 0x6677206465643565672772622B3E3565652D6532686064605F5F60652B742B68, 0x01010101010101010101010101010101, 0x6677206465643565672772622B3E3565652D6532686064605F5F60652B742B68, 0x01010101010101010101010101010101, 0x6677206465643565672772622B3E3565652D6532686064605F5F60652B742B68);")
        print '------------------------------------------------------------接入认证-qkm代理认证-用例结束------------------------------------------------' 
 
 
    def  test_access3(self):

        print '-----------------------------------------------------------------akm接入认证用例开始---------------------------------------------------'     
        test = akmAccess.Clienttest3()
#        test.start()
        self.assertEqual( test.start(), 1)
        print '-----------------------------------------------------------------akm接入认证用例结束---------------------------------------------------'
        
        
    def test_gensys(self):

        print '---------------------------------------------------------------生成同步用例开始------------------------------------------------------'     
        test = main.Gensys()
#        test.start()
        self.assertEqual( test.start(), 1)
        print '---------------------------------------------------------------生成同步用例结束-------------------------------------------------------'  
          
    def test_qkmapply1(self):
        # make sure the shuffled sequence does not lose any elements
        print '--------------------------------------------------------------qkm从中继密钥申请用例开始------------------------------------------------------'       
        test = qkmApply1.Qkmapply()
#        test.start()
        self.assertEqual( test.start(), 1)
        print '--------------------------------------------------------------qkm从中继密钥申请用例开始-------------------------------------------------------' 
        
    def test_qkmget1(self):
        # make sure the shuffled sequence does not lose any elements 
        print '--------------------------------------------------------------qkm从中继密钥获取用例开始-------------------------------------------------------'   
        test = qkmGet1.Qkmget()
#        test.start()
        self.assertEqual( test.start(), 1)
        print '-------------------------------------------------------------qkm从中继密钥获取用例结束--------------------------------------------------------' 
        
    def test_qkmapply2(self):
        # make sure the shuffled sequence does not lose any elements
        print '--------------------------------------------------------------qkm从中心密钥申请用例开始------------------------------------------------------'       
        test = qkmApply2.Qkmapply()
#        test.start()
        self.assertEqual( test.start(), 1)
        print '--------------------------------------------------------------qkm从中心密钥申请用例开始-------------------------------------------------------' 
        
    def test_qkmget2(self):
        # make sure the shuffled sequence does not lose any elements 
        print '--------------------------------------------------------------qkm从中心密钥获取用例开始-------------------------------------------------------'   
        test = qkmGet2.Qkmget()
#        test.start()
        self.assertEqual( test.start(), 1)
        print '-------------------------------------------------------------qkm从中心密钥获取用例结束--------------------------------------------------------' 
#
    def test_akmgetNotIntime(self):
        # make sure the shuffled sequence does not lose any elements 
        print '-----------------------------------------------------------Akm密钥获取非实时用例开始------------------------------------------------------' 
        global expect        
        test = main1.akmIntime()
#        test.start()
        self.assertEqual( test.start(), 1)
        print '-----------------------------------------------------------Akm密钥获取非实时用例结束------------------------------------------------------' 
        
    def tearDown(self):
        print '----------------------------------------------------------------AT用例结束------------------------------------------------------------'


if __name__ == '__main__':
    unittest.main()