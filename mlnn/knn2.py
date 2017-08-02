#! /usr/bin/env python
#coding=utf-8

import struct
import os
import sys
import numpy
import operator
import time

def readlabel(binaryfile):
    """
    @binaryfile: an unclosed file object
    @endian: '>' mean big-endian, '<' mean little-endian
    @mlen: length of magic number
    @ilen: length of number of items
    @vlen: length of data
    """
    mlen=4
    ilen=4
    vlen=1
    endian='>'
    data = binaryfile.read(mlen+ilen)
    magicnum,itemsnum = struct.unpack('>2i', data)
    
    vlist=list()
    for i in range(itemsnum):
        data = binaryfile.read(vlen)
        value, = struct.unpack('>B',data)
        vlist.append(value)
    return itemsnum,vlist

def readimage(binaryfile):
    """
    @binaryfile: an unclosed file object
    @endian: '>' mean big-endian, '<' mean little-endian
    @mlen: length of 'magic number'
    @ilen: length of 'number of items'
    @rlen: length of 'number of rows'
    @clen: length of 'number of columns'
    @vlen: length of data
    """
    mlen=4
    ilen=4
    rlen=4
    clen=4
    vlen=1
    endian='>'
    data = binaryfile.read(mlen+ilen+rlen+clen)
    magicnum,itemsnum,rows,columns = struct.unpack('>4i',data)
    
    vlist=list()
    for i in range(itemsnum*rows*columns):
        data = binaryfile.read(vlen)
        value, = struct.unpack('>B', data)
        vlist.append(value)

    return itemsnum,rows,columns,vlist

def getidx(items, rows, cols):
    idx = 0
    idx = (items-1)*rows*cols + (cols-1)*rows + rows - 1
    return idx
    
    
def classifyKNN(test, trainset, labels, k=3):
    """
    classify by k-NN
    @test: classify it
    Numpy is better
    Proceduce:
        1.distance calculation, the results will store in numpy.array
        2.sort the results by array.argsort
        3.counting the labels with lowest k distances
        4.sort dictionary by value and pick the key with the biggest value
    """
    
    inx = numpy.array(test)
    dataset = numpy.array(trainset)
    dss = len(labels)
    diffmat = numpy.tile(inx, (dss,1)) - dataset
    sq = diffmat**2
    sqd = sq.sum(axis=1)
    distances=sqd**0.5
    
    sortedDistIdx = distances.argsort()
    
    cc={}
    for i in range(k):
        voteLabel = labels[sortedDistIdx[i]]
        cc[voteLabel] = cc.get(voteLabel,0) + 1
    scc = sorted(cc.iteritems(), key=operator.itemgetter(1),reverse=True)
    return scc[0][0]

if __name__ == '__main__':
    #start time
    starttime = time.clock()
    
    filename = 'd:/__P/data/train-images.idx3-ubyte'
    binfile = file(filename, 'rb')
    i1,r1,c1,v1 = readimage(binfile)
    binfile.close()
    
    filename = 'd:/__P/data/train-labels.idx1-ubyte'
    binfile = file(filename,'rb')
    i3,v3 = readlabel(binfile)
    binfile.close()
    
    filename = 'd:/__P/data/t10k-images.idx3-ubyte'
    binfile = file(filename, 'rb')
    i2,r2,c2,v2 = readimage(binfile)
    binfile.close()
    
    filename = 'd:/__P/data/t10k-labels.idx1-ubyte'
    binfile = file(filename,'rb')
    i4,v4 = readlabel(binfile)
    binfile.close()
    
    tmp=list()
    for i in range(i3):
        tmp.append(v1[i*784:(i+1)*784])
    v1=numpy.array(tmp)

    correctCount = 0
    for i in range(i4):
        test = v2[i*784:(i+1)*784]
        ck = classifyKNN(test,v1,v3)
        if ck == v4[i]:
            correctCount = correctCount+1
            
        print 'Total : %f s' %(time.clock()-starttime)
    print correctCount
    
    
    
    
    #end time
    endtime = time.clock()
    print 'Total : %f s' %(endtime-starttime)
