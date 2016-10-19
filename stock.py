#! /usr/bin/env python

import time
import imp
import httplib
import urlparse
import base64
import json
import pymongo

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
	#TODO: 
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

def writeStock2mongo(stocks, client, dbname='test', collectionname='stockstest'):
    db=client[dbname]
    collection = db[collectionname]
    for everystock in stocks:
        collection.insert_one(everystock)
    return True
	
	
def readStock(filename):
    """@stocks: return as json"""
    """struct of stocks:
    [{stock_number1,stock_name1}, {stock_number2,stock_name2},...]"""
    fi = file(filename, 'r')
    stocks = fi.read()
    fi.close()
    stocks = json.loads(stocks)
    return stocks

if __name__=="__main__":
	
    """here for test code"""
    #start time
    starttime = time.clock()

    #SHAurl = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=FD&sty=TSTC&st=1&sr=1&p=1&ps=2000&js=var%20GQWitEGZ=(x)&mkt=1'
    #SZAurl = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=FD&sty=TSTC&st=1&sr=1&p=1&ps=2000&js=var%20mhKpHKDS=(x)&mkt=3'
    
    stocks = readStock('d:/__P/test-master/SZA.stk')
    client=pymongo.MongoClient()
    writeStock2mongo(stocks, client)

    #allstocks = getStocks(SHAurl)
    #writeStock(getStocks(SHAurl), '/Users/stefen/Desktop/stock/SHA.stk')
    #writeStock(getStocks(SZAurl), '/Users/stefen/Desktop/stock/SZA.stk')

    #end time
    endtime = time.clock()
    print 'Total : %f s' % (endtime-starttime)
