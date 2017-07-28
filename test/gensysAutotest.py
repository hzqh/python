#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on 2017-7-17
@author: qih
Project:执行生成同步用例
'''
import random
import unittest

from gensysATest import main

class autoTest(unittest.TestCase):   
    def setUp(self):
#        self.seq = range(10)
        
        print '---------------------------------------------------- -----------AT用例开始---------------------------------------------------'

        
    def test_gensys(self):

        print '---------------------------------------------------------------生成同步用例开始------------------------------------------------------'     
        test = main.Gensys()
#        test.start()
        self.assertEqual( test.start(), 1)
        print '---------------------------------------------------------------生成同步用例结束-------------------------------------------------------'  
          
          
    def tearDown(self):
        print '----------------------------------------------------------------AT用例结束------------------------------------------------------------'


if __name__ == '__main__':
    unittest.main()
