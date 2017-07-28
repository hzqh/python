#!/usr/bin/python
# -*- coding: utf-8 -*- 
'''
Created on 2017-7-23
@author: qih
Project:socket收发
'''
def RecvN(socket, n):
    totalContent = ''
    totalRecved = 0
    while totalRecved < n:
        onceContent = socket.recv(n - totalRecved)
#        print("onceContent", onceContent)
        totalContent += onceContent
        totalRecved = len(totalContent)
 
    return totalContent


def RecvN1(socket, n):    

    totalContent = ''

    totalRecved = 0

    while totalRecved < n:

        onceContent = socket.recv(n - totalRecved)        

        totalContent += onceContent

        totalRecved = len(totalContent)



    return totalContent