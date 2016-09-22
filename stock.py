#! /usr/bin/env python

import time
import imp
import httplib
import urlparse
import base64
import json

def getStocks(url, useproxy = False, proxy_url=''):
    data = ''
    if useproxy is False:
        urlinfo = urlparse.urlparse(url)
        conn = httplib.HTTPConnection( urlinfo.hostname, (urlinfo.port or 80) )
        conn.request('GET', urlinfo.path+'?'+urlinfo.query)
        response = conn.getresponse()
        data = response.read()
    else:
        proxy=urlparse.urlparse(proxy_url)
    data = data.split('[')[1].split(']')[0][1:-1]
    data = data.split('","')
    stocks=list()
    for ele in data:
        stock = dict()
        tmp = ele.split(',')
        stock['number'] = tmp[0]
        stock['name'] = tmp[1]
        stocks.append(stock)
    stocks = json.dumps(stocks)
    return stocks

def writeStock(stocks, filename):
    """@stocks: should be json"""
    fi = file(filename, 'w')
    fi.write(stocks)
    fi.close()

def readStock(stocks, filename):
    """@stocks: return as json"""
    fi = file(filename, 'r')
    stocks = fi.read()
    fi.close()
    stocks = stocks[0:-1]
    return stocks

if __name__=="__main__":
	
    #start time
    starttime = time.clock()

    SHAurl = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=FD&sty=TSTC&st=1&sr=1&p=1&ps=2000&js=var%20GQWitEGZ=(x)&mkt=1'
    SZAurl = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=FD&sty=TSTC&st=1&sr=1&p=1&ps=2000&js=var%20mhKpHKDS=(x)&mkt=3'


    #allstocks = getStocks(SHAurl)
    writeStock(getStocks(SHAurl), '/Users/stefen/Desktop/stock/SHA.stk')
    writeStock(getStocks(SZAurl), '/Users/stefen/Desktop/stock/SZA.stk')

    #end time
    endtime = time.clock()
    print 'Total : %f s' % (endtime-starttime)