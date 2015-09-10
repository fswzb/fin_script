# -*- coding:gbk -*-
#from openpyxl import Workbook
#from openpyxl.reader.excel  import  load_workbook
import sys
import re
import urllib
import urllib2

#url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=sz300001&date=2015-09-10&page=48"
#�ɽ�ʱ��	�ɽ���	�ǵ���	�۸�䶯	�ɽ���(��)		�ɽ���(Ԫ)	����
#	<tr ><th>11:29:48</th><td>14.57</td><td>-3.06%</td><td>+0.01</td><td>16</td><td>23,312</td><th><h1>������</h1></th></tr>
#<tr ><th>11:29:36</th><td>14.56</td><td>-3.13%</td><td>--</td><td>9</td><td>13,104</td><th><h6>����</h6></th></tr>
#<tr ><th>11:29:21</th><td>14.56</td><td>-3.13%</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>����</h6></th></tr>

pindex = len(sys.argv)
if (pindex != 3):
	sys.stderr.write("Usage: command ���� ʱ��<YYYY-MM-DD>\n")
	exit(1);

code = sys.argv[1]
qdate = sys.argv[2]
if (len(code) != 6):
	sys.stderr.write("Len should be 6\n")
	exit(1);

head3 = code[0:3]
result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0)
if result is True:
	code = "sz" + code
	print code
else:
	result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0)
	if result is True:
		code = "sh" + code
		print code
	else:
		print "�Ƿ�����:" +code+ "\n"
		exit(1);
	
dateObj = re.search(r'^\d{4}-\d{2}-\d{2}', qdate)
if (dateObj is None):
	print "�Ƿ����ڸ�ʽ��" +qdate+ ",������ʽ:YYYY-MM-DD"
	exit(1);

qdate = dateObj.group(0)
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=" + code

lasttime = ''
fl = open('a.csv', 'w')
for i in range(1,1000):
	urlall = url + "&date=2015-09-10&page=" +str(i)
#	print "%d, %s" %(i,urlall)
	
	req = urllib2.Request(urlall)
	res_data = urllib2.urlopen(req)

	flag = 0
	count = 0
	line = res_data.readline()
	checkStr = '�ɽ�ʱ��'
	while line:
		index = line.find(checkStr)
		if (index<0):
			line = res_data.readline()
			continue

		if flag==0:
			checkStr = '<th>'
			flag = 1
		else:
			key = re.match(r'\D+(\d{2}:\d{2}:\d{2})\D+(\d+.\d{1,2})</td><td>\+?-?(\d+.\d+)\D+(--|\+\d+.\d+|-\d+.\d+)\D+(\d+)</td><td>([\d,]+)</td><th><h\d+>(����|����|������)\D', line)
			if (key):
#				print key.groups()
				curtime = key.group(1)
				if re.search(curtime, lasttime):
					pass
				else:
					lasttime = curtime
					strline = key.group(1) +","+ key.group(2) +","+ key.group(3) +","+ key.group(4) +","+ key.group(5) +","+ key.group(6) +","+ key.group(7) + "\n"
					fl.write(strline)
				count += 1
				pass
			else:
				endObj = re.search(r'</td><td>', qdate)
				if (endObj):
					print "Error line:" + line
				else:
					break;
		line = res_data.readline()

	if (count==0):
		print "page:" +str(i)+ " No DATA"
		break;
fl.close()
