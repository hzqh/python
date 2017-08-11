#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on 2017-7-17
@author: qih
Project:执行qkm秘钥服务用例
'''
import random
import unittest

from qkmATest import qkmApply1
from qkmATest import qkmGet1
from qkmATest import qkmApply2
from qkmATest import qkmGet2
from qkmATest import dianduidian1



class autoTest(unittest.TestCase):   
    def setUp(self):
#        self.seq = range(10)
        
        print '---------------------------------------------------- -----------AT用例开始---------------------------------------------------'

          
    def test_qkmapply1(self):
        # make sure the shuffled sequence does not lose any elements
        print '--------------------------------------------------------------qkm从中继密钥申请用例开始------------------------------------------------------'       
        test = qkmApply1.Qkmapply()
##        test.start()
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
        
    def test_dianduidian1(self):
        # make sure the shuffled sequence does not lose any elements
        print '--------------------------------------------------------------qkm从中心密钥申请用例开始------------------------------------------------------'       
        
        test = dianduidian1.Qkmapply()
#        test.start()
        self.assertEqual( test.start(), 1)
        print '--------------------------------------------------------------qkm从中心密钥申请用例开始-------------------------------------------------------' 
        
#    def test_qkmdianduidian1(self):
#        # make sure the shuffled sequence does not lose any elements
#        print '--------------------------------------------------------------qkm点对点-对端slave用例开始------------------------------------------------------'       
#        test = qkmApply2.Qkmapply()
##        test.start()
#        self.assertEqual( test.start(), 1)
#        print '--------------------------------------------------------------qkm点对点-对端slave用例结束-------------------------------------------------------' 
#        
#    def test_qkmdianduidian2(self):
#        # make sure the shuffled sequence does not lose any elements 
#        print '--------------------------------------------------------------qkm点对点-对端master用例开始-------------------------------------------------------'   
#        test = qkmGet2.Qkmget()
##        test.start()
#        self.assertEqual( test.start(), 1)
#        print '-------------------------------------------------------------qkm点对点-对端master用例结束--------------------------------------------------------' 


#
#        
    def tearDown(self):
        print '----------------------------------------------------------------AT用例结束------------------------------------------------------------'


if __name__ == '__main__':
    unittest.main()
