#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on 2017-7-17
@author: qih
Project:数据库增删改查封装
'''
import MySQLdb
import ConfigParser

class DBConn():
    
    def __init__(self, name, conn, cur):  # init class and create a database
        self.name = name
        self.conn = conn
        self.cur = cur
        try:
            cur.execute('create database if not exists ' + name)
            conn.select_db(name)
            conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    def createTable(self, name):   # create a table
        try:
            ex = self.cur.execute
            if ex('show tables') == 0:
                ex('create table ' + name + '(id int, name varchar(20), sex int, age int, info varchar(50))')
                self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
     
    def insert(self, sql):   #插入单个值
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    
    def insertMore(self, name, values): #插入多个值
        try:
            self.cur.executemany('insert into ' + name + ' values(%s,%s,%s,%s,%s)', values)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            

            
    def updateSingle(self, name, value):
        try:
            self.cur.execute('update ' + name + ' set name=%s, sex=%s, age=%s, info=%s where id=%s;', value)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    def update(self, name, values):
        try:
            self.cur.executemany('update ' + name + ' set name=%s, sex=%s, age=%s, info=%s where id=%s;', values)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    def getCount(self, name):
        try:
            count = self.cur.execute('select * from connection_info where user_name = ' + name)
            return count
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
            
    def selectname(self, name):
        try:
            self.cur.execute('select * from connection_info where user_name = ' + name)
            result = self.cur.fetchone()
            return result
        
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])   
            
    def select(self, sql):
        try:
            self.cur.execute(sql)
            result = self.cur.fetchone()
            return result
        
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])      
            
    def selectFirst(self, name):
        try:
            self.cur.execute('select * from ' + name + ';')
            result = self.cur.fetchone()
            return result
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    def selectLast(self, name):
        try:
            self.cur.execute('SELECT * FROM ' + name + ' ORDER BY id DESC;')
            result = self.cur.fetchone()
            return result
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    def selectNRecord(self, name, n):
        try:
            self.cur.execute('select * from ' + name + ';')
            results = self.cur.fetchmany(n)
            return results
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    def selectAll(self, name):
        try:
            self.cur.execute('select * from ' + name + ';')
            self.cur.scroll(0, mode='absolute') # reset cursor location (mode = absolute | relative)
            results = self.cur.fetchall()
            return results
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    def deleteByID(self, name, id):
        try:
            self.cur.execute('delete from ' + name + ' where id=%s;', id)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    def delete(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    def dropTable(self, name):
        try:
            self.cur.execute('drop table ' + name + ';')
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    def dropDB(self, name):
        try:
            self.cur.execute('drop database ' + name + ';')
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    def __del__(self):
        if self.cur != None:
            self.cur.close()
        if self.conn != None:
            self.conn.close()
      
              
    
