#! /usr/bin/env python
#coding=utf-8

import time
import os
import sys
import ctypes
import struct

def findstr(filepath, text):
    src = file(filepath,'r')
    for eachline in src:
        if text in eachline:
            src.close()
            return True
    src.close()
    return False

def h2f(s):
    cp = ctypes.pointer(ctypes.c_longlong(s))
    fp = ctypes.cast(cp, ctypes.POINTER(ctypes.c_double))
    return fp.contents.value

def f2h(s):
    fp = ctypes.pointer(ctypes.c_double(s))
    cp = ctypes.cast(fp, ctypes.POINTER(ctypes.c_longlong))
    return hex(cp.contents.value)


if __name__ == '__main__':
#    fi = file('d:/959')
#    for eachline in fi:
#        if eachline.startswith('[1888]'):
#            print eachline[:-1]


    """find string from java source code"""
    basepath = 'D:/decompiled-classes-dex2jar'
    pathlist = list()
    pathlist.append(basepath)
    text = 'setLatitude'
    while True:
        if len(pathlist)==0:
            break
        tmp = pathlist.pop()
        if os.path.isdir(tmp):
            rst = os.listdir(tmp)
            for ele in rst:
                pathlist.append(tmp+'/'+ele)
                #print tmp+'/'+ele
        elif os.path.isfile(tmp):
            if findstr(tmp,text):
                print 'FOUND:'
                print tmp
        else:
            print 'INTERNAL ERROR'
    
#    fi = file('d:/1.csv','rb')
#    import csv
#    reader = csv.reader(fi)
#    idx = 0
#    for line in reader:
#        if idx == 0:
#            index = 0
#            while True:                
#                if index == 0:
#                    print line[index],
#                    index = index+1
#                    continue
#                print line[index],line[index],
#                index = index+1                
#                if index >=len(line):
#                    break                
#        if idx != 0:
#            l = len(line)
#            index = 0
#            while True:
#                if index == 0:
#                    print line[index],
#                    index=index+1
#                    continue
#                if '/' not in line[index]:
#                    line[index] = '-1/-1'
#                tmp = line[index].split('/')
#                print tmp[0],tmp[1],
#                index=index+1
#                if index >= l:
#                    break                
#        idx=idx+1
#        print ''
#    fi.close()
