# -*- coding:gbk -*-
import urllib
import urllib2
import re

url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?date=2015-09-18&symbol=sz300001"
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?date=2015-05-06&symbol=sz300001"
#url = "http://market.finance.sina.com.cn/transHis.php?symbol=sz300001&date=2015-9-11&page=1"

req = urllib2.Request(url)
#print req

res_data = urllib2.urlopen(req)

flag = 0
line = res_data.readline()
checkStr = '���̼�'
while line:
	index = line.find(checkStr)
	if (index<0):
		line = res_data.readline()
		continue
	else:
		flag = 1
		break;

#�ҵ��ؼ��ֺ󣬲����µĹؼ���
i = 0
keyw='���̼�|�ǵ���|ǰ�ռ�|���̼�|��߼�|��ͼ�|�ɽ���|�ɽ���'
dtlRe = re.compile(r'\D+('+keyw+').*>(\d+\.\d+)')
while line:
	#print "s='"+ line + "'"
	#dtlRe = re.compile(r'\D+ǰ�ռ�\D+(\d+\.\d+)')
	print line
	obj = dtlRe.match(line)
	if obj:
		print "FD---", obj.group(2)
	else:
		print "NNNNNNNNNNNN"
	i += 1
	if (i>10):
		break
	line = res_data.readline()


