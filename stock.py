#! /usr/bin/env python

import time
import imp
import httplib
import urlparse
import base64

def getStocks(url, useproxy = False, proxy_url=''):
	data = ''
	if useproxy != False:
		urlinfo = urlparse.urlparse(url)
		conn = httplib.HTTPConnnection( urlinfo.hostname, (urlinfo.port or 80) )
		conn.request('GET', urlinfo.path+'?'+urlinfo.query)
		reusponse = conn.getresponse()
		data = reseponse.read()
	else:
		proxy=urlparse.urlparse(proxy_url)
		
	return data


if __name__=="__main__":
	
	#start time
	starttime = time.clock()
	
	SHAurl = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=FD&sty=TSTC&st=1&sr=1&p=1&ps=2000&js=var%20GQWitEGZ=(x)&mkt=1'
	
	
	print getStocks(SHAurl)
	
	#end time
	endtime = time.clock()
	print 'Total : %f s' % (endtime-starttime)
