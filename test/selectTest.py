# coding=utf-8
'''
Created on 2017-7-17
@author: qih
Project:测试套件suite，选择执行部分用例
'''
import unittest
import clientAutotest
import gensysAutotest

#构造测试集
suite = unittest.TestSuite()
suite.addTest(clientAutotest.autoTest('test_access1'))
suite.addTest(gensysAutotest.autoTest('test_gensys'))

if __name__=='__main__':
    #执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)