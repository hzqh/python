#!/usr/bin/python
# -*- coding: utf-8 -*- 
'''
Created on 2017-7-17
@author: qih
Project:Excel读取操作
'''
import  xdrlib ,sys

import xlrd
import unicodedata

def open_excel(file= r'C:\Users\lenovo\Desktop\testcase.xlsx'):
    try:
#        data = xlrd.open_workbook(file)
        xlrd.Book.encoding = "gbk"
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)

#读取单行用例
def excel_read_row(file,colnameindex,rownum,by_name):
    try:
        data = xlrd.open_workbook(file)
    except Exception,e:
        print str(e)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数 
    colnames =  table.row_values(colnameindex) #某一行数据 
    row = table.row_values(rownum)
    list =[]
    app = {}
    for i in range(4,len(colnames)):
        app[colnames[i]] = row[i]
    
    list.append(app)
    return list

#读取每行用例
def excel_read_all(file,index_name,startrow,startcol):#参数依次为文件路径、sheet表名、参数起始行、参数起始列
    
    try:  
        data = xlrd.open_workbook(file)
        table = data.sheet_by_name(index_name)
        nrows = table.nrows
        ncols = table.ncols
        colnames =  table.row_values(startrow) #起始行
        lists=[[] for i in range(startrow,nrows)]
        for row in range(startrow,nrows):
            for i in range(startcol,len(colnames)):           
                lists[row-startrow].append(table.cell(row,i).value )
        return  lists             
    except Exception,e:  
        print str(e)
        
def excel_data_to_list(data):
    data = unicodedata.normalize('NFKD', data).encode('utf-8', 'ignore')
    data = data.replace('[', '').replace(']', '')
    data = data.split(',')
    for i in range(len(data)):
        data[i] = data[i].replace("'", '')
        data[i] = int(data[i])
        
    return data
    
    
        



#def main():
##   tables = excel_table_byindex()
##   for row in tables:
##       print row
#
#   tables = excel_read_row()
#   
#   for row in tables:
#       print row['phone'],row['password']
#       print type(tables)
#       print tables
#
#if __name__=="__main__":
#    main()