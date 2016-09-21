# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
import urllib
import urllib2
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
import internal.common
import time

def currentIndexData(url, code):
	urllink = url + code
	try:
		req = urllib2.Request(urllink)
		stockData = urllib2.urlopen(req, timeout=2).read()
	except:
		loginfo(1)
		print "URL timeout"
	else:
		stockObj = stockData.split(',')
		if len(stockObj)<3:
			return
		idxVal = "%.02f"%(float(stockObj[1]))
		print "%10s	%s%%(%s)" % (idxVal, stockObj[3], stockObj[2])

def currentSinaData(url, code):
	urllink = url + code
	buy = []
	buyVol = []
	sell = []
	sellVol = []
	try:
		req = urllib2.Request(urllink)
		stockData = urllib2.urlopen(req, timeout=2).read()
	except:
		loginfo(1)
		print "URL timeout"
	else:
		stockObj = stockData.split(',')
		stockLen = len(stockObj)
		#for i in range(0, stockLen):
		#	print "%02d:	%s" % (i, stockObj[i])

		curPrice = stockObj[3]
		highPrice = stockObj[4]
		lowPrice = stockObj[5]
		lastPrice = stockObj[2]
		#variation = stockObj[43]
		#zhangdiejia = stockObj[31]
		#zhangdiefu = stockObj[32]
		volume = stockObj[8]
		amount = stockObj[9]
		
		index = 11
		for i in range(0, 5):
			buy.append(stockObj[index+i*2])
		index = 10
		for i in range(0, 5):
			buyVol.append(int(stockObj[index+i*2])/100)
		index = 21
		for i in range(0, 5):
			sell.append(stockObj[index+i*2])
		index = 20
		for i in range(0, 5):
			sellVol.append(int(stockObj[index+i*2])/100)
		print "---------------------"
		print "[%s]	[%s	%s]" % (curPrice, highPrice, lowPrice)
		index = 4
		for i in range(0, 5):
			print "%s	%8s" %(sell[index], sellVol[index])
			index -= 1
		print "===%s" %(curPrice)
		index = 0
		for i in range(0, 5):
			print "%s	%8s" %(buy[index], buyVol[index])
			index += 1
		print "~~~~~~~~~~~~~~~~~~~~~"
		print "	"
		
pindex = len(sys.argv)
if pindex<2:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " ���� \n")
	exit(1);

code = sys.argv[1]
if (len(code) != 6):
	sys.stderr.write("Len should be 6\n")
	exit(1);

head3 = code[0:3]
result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0)
if result is True:
	code = "sz" + code
else:
	result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0)
	if result is True:
		code = "sh" + code
	else:
		print "�Ƿ�����:" +code+ "\n"
		exit(1);

#os.system('msg "*" "aaa"')
url = "http://hq.sinajs.cn/list="
while True:
	print "---------------------"
	currentIndexData(url, "s_sh000001")
	currentIndexData(url, "s_sz399006")
	currentSinaData(url, code)
	now = datetime.datetime.now()
	hour = now.hour
	minute = now.minute
	if (hour<9 or hour>=15):
		break;
	elif (hour==9 and minute<15):
		break;
	time.sleep(3)
	#os.system('msg "*" "aaa"')