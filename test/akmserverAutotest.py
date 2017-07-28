#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on 2017-7-17
@author: qih
Project:执行akm秘钥服务用例
'''
import random
import unittest
from ApplicationKey import main1



class autoTest(unittest.TestCase):   
    def setUp(self):
#        self.seq = range(10)
        
        print '---------------------------------------------------- -----------AT用例开始---------------------------------------------------'

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
