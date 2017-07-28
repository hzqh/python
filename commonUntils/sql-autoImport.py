#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on 2017-7-24
@author: qih
Project:sql数据批量导入
'''
import random
import unittest
from clientTest import ClientAES1

from gensysATest import main
from ApplicationKey import main1

#import ClientAES1
import MySQLdb
from commonUntils import ExcelUntil
from commonUntils import DBConnection

from clientTest import ClientAES2
from clientTest import akmAccess
import ConfigParser



import os,os.path    
import string,base64  
def main():  
#    f=open("inserData.sql",'w')  
    cf = ConfigParser.ConfigParser()
    cf.read('D:/workplace/PyTest-frame/qtec.conf')  
    conn = MySQLdb.connect(host=eval(cf.get('db2', 'host')),user=eval(cf.get('db2', 'user')),passwd=eval(cf.get('db2', 'passwd')),db=eval(cf.get('db2', 'db')),port=eval(cf.get('db2', 'port')),charset='utf8')
    cur = conn.cursor()
    hero = DBConnection.DBConn(eval(cf.get('db2', 'db')),conn,cur)
    i=2000060
    while i<2000160:
        strI = str(i)
        strI2 = strI[4:]
#        sql = "INSERT INTO `authentication_info` VALUES ('" + strI + "'," + "'client_qh" + strI2 + "'," + "'client_qh" + strI2 + "'," + "'client_qh" + strI2 + "','" + "1','" + "091945003b065c0d0a42'," + "0x0101010101010101010101010" + strI + "," + "0x6677206465643565672772622B3E3565652D6532686064605F5F60652B742B68," + "0x0101010101010101010101010" + strI + "," + "0x6677206465643565672772622B3E3565652D6532686064605F5F60652B742B68," + "0x0101010101010101010101010" + strI + "," + "0x6677206465643565672772622B3E3565652D6532686064605F5F60652B742B68);"
        sql = "INSERT INTO `authentication_info` VALUES ('" + strI + "'," + "'client_ligg" + strI2 + "'," + "'client_ligg" + strI2 + "'," + "'client_ligg" + strI2 + "','" + "1','" + "091945003b065c0d0a42'," + "0x3665353933306632646538313" + strI + "," + "0x3032613763383238653738323432623439306662383762383031346130383438," + "0x3665353933306632646538313" + strI + "," + "0x3032613763383238653738323432623439306662383762383031346130383438," + "0x3665353933306632646538313" + strI + "," + "0x3032613763383238653738323432623439306662383762383031346130383438);"
#        hero.insert(sql)
        print sql
        i=i+1
      
       
if __name__=='__main__':    
    main()
        
#cf = ConfigParser.ConfigParser()
#cf.read('D:/workplace/PyTest-frame/qtec.conf')  
#conn = MySQLdb.connect(host=eval(cf.get('db1', 'host')),user=eval(cf.get('db1', 'user')),passwd=eval(cf.get('db1', 'passwd')),db=eval(cf.get('db1', 'db')),port=eval(cf.get('db1', 'port')),charset='utf8')
#cur = conn.cursor()
#hero = DBConnection.DBConn(eval(cf.get('db1', 'db')),conn,cur)
#hero.insert("INSERT INTO `authentication_info` VALUES ('7000004', 'client_qh001', 'client_qh001', 'client_qh001', '1', '091945003b065c0d0a42', 0x01010101010101010101010101070104, 0x6677206465643565672772622B3E3565652D6532686064605F5F60652B742B68, 0x01010101010101010101010101010101, 0x6677206465643565672772622B3E3565652D6532686064605F5F60652B742B68, 0x01010101010101010101010101010101, 0x6677206465643565672772622B3E3565652D6532686064605F5F60652B742B68);")