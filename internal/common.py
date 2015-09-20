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

#url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=sz300001&date=2015-09-10&page=48"
#�ɽ�ʱ��	�ɽ���	�ǵ���	�۸�䶯	�ɽ���(��)		�ɽ���(Ԫ)	����
#	<tr ><th>11:29:48</th><td>14.57</td><td>-3.06%</td><td>+0.01</td><td>16</td><td>23,312</td><th><h1>������</h1></th></tr>
#<tr ><th>11:29:36</th><td>14.56</td><td>-3.13%</td><td>--</td><td>9</td><td>13,104</td><th><h6>����</h6></th></tr>
#<tr ><th>11:29:21</th><td>14.56</td><td>-3.13%</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>����</h6></th></tr>

class fitItem:
	volumn = 0
	buyvol = 0
	buyct = 0
	buyavg = 0
	sellvol = 0
	sellct = 0
	sellavg = 0
	def __init__(self, vol):
		self.volumn = vol
		self.buyvol = 0
		self.buyct = 0
		self.buyavg = 0
		self.sellvol = 0
		self.sellct = 0
		self.sellavg = 0

dftsarr = "0,200,300,600,900"

def loginfo(flag=0):
	if (flag==1):
		frame = None
		try:
			raise  ZeroDivisionError
		except  ZeroDivisionError:
			frame = sys.exc_info()[2].tb_frame.f_back
		print "%s in line %d" %(str(datetime.datetime.now()), frame.f_lineno)

def parseCode(code):
	if (len(code) != 6):
		sys.stderr.write("Len should be 6\n")
		return (-1, '')

	head3 = code[0:3]
	result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0)
	if result is True:
		ncode = "sz" + code
	else:
		result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0)
		if result is True:
			ncode = "sh" + code
		else:
			print "�Ƿ�����:" +code+ "\n"
			return (-1, '')
	return (0, ncode)

def parseDate(qdate, today):
	dateObj = re.match(r'^(\d{4})-(\d+)-(\d+)', qdate)
	if (dateObj is None):
		dateObj = re.match(r'^(\d+)-(\d+)', qdate)
		if (dateObj is None):
			print "�Ƿ����ڸ�ʽ��" +qdate+ ",������ʽ:YYYY-MM-DD or MM-DD"
			return (-1, '')
		else:
			year = today.year
			month = int(dateObj.group(1))
			day = int(dateObj.group(2))
	else:
		year = int(dateObj.group(1))
		month = int(dateObj.group(2))
		day = int(dateObj.group(3))
	strdate = '%04d-%02d-%02d' %(year, month, day)
	return (0, strdate)


def write_statics(ws, fctime, dataObj, qdate):
	ws.title = 'statistics'

	ascid = 65
	row = 1
	if cmp(fctime, '')==0:
		title = [qdate, 'B', 'S', 'B_vol', 'S_vol', 'B_avg', 'S_avg', ]
	else:
		title = [qdate, 'B', 'S', 'B_vol', 'S_vol', 'B_avg', 'S_avg', fctime]
	number = len(title)
	for i in range(0,number):
		cell = chr(ascid+i) + str(row)
		ws[cell] = title[i]

	dataObjLen = len(dataObj)
	for j in range(0, dataObjLen):
		list = []
		list.append(dataObj[j].volumn)
		
		buyvol = dataObj[j].buyvol
		buyct = dataObj[j].buyct
		
		sellvol = dataObj[j].sellvol
		sellct = dataObj[j].sellct
		
		list.append(buyvol)
		list.append(sellvol)
		list.append(buyct)
		list.append(sellct)
		if buyct==0:
			list.append(0)
		else:
			list.append(buyvol/buyct)
		if sellct==0:
			list.append(0)
		else:
			list.append(sellvol/sellct)
		list.append('')
		list.append(buyvol + sellvol)
		list.append(buyct + sellct)
		bsct = buyct + sellct
		if bsct==0:
			list.append(0)
		else:
			list.append((buyvol + sellvol)/bsct)
		
		row = row+1
		number = len(list)
		for i in range(0,number):
			cell = chr(ascid+i) + str(row)
			ws[cell] = list[i]

def handle_data(addcsv, prepath, dflag, url, code, qdate, sarr):
	if dflag==0:
		url = url +"?symbol="+ code
	elif dflag==1:
		url = url +"?date="+ qdate +"&symbol="+ code
	else:
		print "Unknown flag:"+ str(dflag)
		return
	#print url

	if not os.path.isdir(prepath):
		os.makedirs(prepath)

	dataObj = []
	if cmp(sarr, '')==0:
		sarr = dftsarr
	volObj = sarr.split(',')
	arrlen = len(volObj)
	for i in range(0,arrlen):
		obj = fitItem(int(volObj[i]))
		dataObj.append(obj)
	dataObjLen = len(dataObj)

	wb = Workbook()
	# grab the active worksheet
	ws = wb.active

	totalline = 0
	#���������ڲ�ͬ��ҳ�棬ͬʱ���ڣ������ظ�������Ҫ�����ظ����
	#��������ͬʱ�䣬��������ɽ�������Ҫ������
	lasttime = ''
	lastvol = 0
	pageFtime = ''
	bFtime = 0
	bFindHist = 0
	hisUrl = ''
	filename = code+ '_' + qdate
	fctime = ''
	if dflag==0:
		cur=datetime.datetime.now()
		fctime = '%02d:%02d' %(cur.hour, cur.minute)
		filename = '%s_%02d-%02d' %(filename, cur.hour, cur.minute)
	if addcsv==1:
		filecsv = prepath + filename + '.csv'
		fcsv = open(filecsv, 'w')
		strline = '�ɽ�ʱ��,�ɽ���,�ǵ���,�۸�䶯,�ɽ���,�ɽ���,����'
		fcsv.write(strline)
		fcsv.write("\n")

	strline = u'�ɽ�ʱ��,�ɽ���,�ǵ���,�۸�䶯,�ɽ���,�ɽ���,����'
	strObj = strline.split(u',')
	ws.append(strObj)
	dtlRe = re.compile(r'\D+(\d{2}:\d{2}:\d{2})\D+(\d+.\d{1,2})</td><td>(\+?-?\d+.\d+%)\D+(--|\+\d+.\d+|-\d+.\d+)\D+(\d+)</td><td>([\d,]+)</td><th><h\d+>(����|����|������)\D')
	frameRe = re.compile(r'.*name=\"list_frame\" src=\"(.*)\" frameborder')
	excecount = 0
	for i in range(1,500):
		urlall = url + "&page=" +str(i)
		#print "%d, %s" %(i,urlall)
		loginfo()

		if excecount>10:
			break

		req = urllib2.Request(urlall)
		try:
			res_data = urllib2.urlopen(req)
		except:
			print "Get URL except"
			i -= 1
			excecount += 1
			continue
		else:
			pass
		#print "Parse data"
		loginfo()

		flag = 0
		count = 0
		line = res_data.readline()
		if dflag==0:
			checkStr = '�ɽ�ʱ��'
		else:
			checkStr = 'ǰ�ռ�'
		while line:
			index = line.find(checkStr)
			if (index<0):
				line = res_data.readline()
				continue
			else:
				checkStr = '<script type='
				break;
		loginfo()

		#�ҵ��ؼ��ֺ󣬲����µĹؼ���
		while line:
			#print "s='"+ line + "'"
			index = line.find(checkStr)
			if (index>=0):
				#�ҵ�֮���˳�
				break;

			#key = re.match(r'\D+(\d{2}:\d{2}:\d{2})\D+(\d+.\d{1,2})</td><td>(\+?-?\d+.\d+%)\D+(--|\+\d+.\d+|-\d+.\d+)\D+(\d+)</td><td>([\d,]+)</td><th><h\d+>(����|����|������)\D', line)
			key = dtlRe.match(line)
			if key:
				#print key.groups()
				curtime = key.group(1)
				curvol = int(key.group(5))
				#��ס��ǰҳ��һ����ʱ��
				if (bFtime==0):
					timeobj = re.search(curtime, pageFtime)
					if timeobj:
						break
					pageFtime = curtime
					bFtime = 1

				timeobj = re.search(curtime, lasttime)
				if (timeobj and curvol==lastvol):
					pass
				else:
					lasttime = curtime
					lastvol = curvol
					amount = key.group(6)
					obj = amount.split(',')
					amount = ''.join(obj)

					intamount = int(key.group(5))
					state = key.group(7)
					for j in range(0, dataObjLen):
						filtvol = int(dataObj[j].volumn)
						if intamount<filtvol:
							continue;
						if cmp(state, '����')==0:
							dataObj[j].sellvol += intamount
							dataObj[j].sellct += 1
							#print "S:%d %d" %(dataObj[j].sellvol, dataObj[j].sellct)
						elif cmp(state, '����')==0:
							dataObj[j].buyvol += intamount
							dataObj[j].buyct += 1
							#print "B:%d %d" %(dataObj[j].buyvol, dataObj[j].buyct)

					if addcsv==1:
						strline = curtime +","+ key.group(2) +","+ key.group(3) +","+ key.group(4) +","+ key.group(5) +","+ amount +","+ key.group(7) + "\n"
						fcsv.write(strline)

					totalline += 1
					row = totalline+1
					cell = 'A' + str(row)
					ws[cell] = curtime
					cell = 'B' + str(row)
					ws[cell] = key.group(2)
					cell = 'C' + str(row)
					ws[cell] = key.group(3)
					cell = 'D' + str(row)
					ws[cell] = key.group(4)
					cell = 'E' + str(row)
					ws[cell] = int(key.group(5))
					cell = 'F' + str(row)
					ws[cell] = int(amount)
					cell = 'G' + str(row)
					s1 = key.group(7).decode('gbk')
					ws[cell] = s1
				count += 1
				line = res_data.readline()
				continue

			if dflag==1:
				key = frameRe.match(line)
				if key:
					bFindHist = 1
					hisUrl = key.group(1)
					#print key.groups()
					break
			
			line = res_data.readline()

		loginfo()
		bFtime = 0
		if (count==0):
			break;

	if addcsv==1:
		fcsv.close()
		if (totalline==0):
			os.remove(filecsv)

	if totalline>0:
		loginfo()
		ws = wb.create_sheet()
		write_statics(ws, fctime, dataObj, qdate)

	loginfo()
	filexlsx = prepath +filename+ '.xlsx'
	wb.save(filexlsx)
	if (totalline==0):
		os.remove(filexlsx)
		if bFindHist==1:
			handle_his_data(addcsv, prepath, hisUrl, code, qdate, sarr)
		else:
			print qdate+ " No Matched Record"
	else:
		print qdate+ " Saved OK"

def handle_his_data(addcsv, prepath, url, code, qdate, sarr):
	#print url
	if not os.path.isdir(prepath):
		os.makedirs(prepath)

	dataObj = []
	if cmp(sarr, '')==0:
		sarr = dftsarr
	volObj = sarr.split(',')
	arrlen = len(volObj)
	for i in range(0,arrlen):
		obj = fitItem(int(volObj[i]))
		dataObj.append(obj)
	dataObjLen = len(dataObj)

	wb = Workbook()
	# grab the active worksheet
	ws = wb.active

	totalline = 0
	#���������ڲ�ͬ��ҳ�棬ͬʱ���ڣ������ظ�������Ҫ�����ظ����
	#��������ͬʱ�䣬��������ɽ�������Ҫ������
	lasttime = ''
	lastvol = 0
	pageFtime = ''
	bFtime = 0
	filename = code+ '_' + qdate
	if addcsv==1:
		filecsv = prepath + filename + '.csv'
		fcsv = open(filecsv, 'w')
		strline = '�ɽ�ʱ��,�ɽ���,�ǵ���,�۸�䶯,�ɽ���,�ɽ���,����'
		fcsv.write(strline)
		fcsv.write("\n")

	strline = u'�ɽ�ʱ��,�ɽ���,�ǵ���,�۸�䶯,�ɽ���,�ɽ���,����'
	strObj = strline.split(u',')
	ws.append(strObj)
	dtlRe = re.compile(r'\D+(\d{2}:\d{2}:\d{2})\D+(\d+.\d{1,2})</td><td>(--|\+?\d+.\d+|-\d+.\d+)\D+(\d+)</td><td>([\d,]+)</td><th><h\d+>(����|����|������)\D')
	for i in range(1,500):
		urlall = url + "&page=" +str(i)
		#print "%d, %s" %(i,urlall)

		req = urllib2.Request(urlall)
		res_data = urllib2.urlopen(req)

		flag = 0
		count = 0
		line = res_data.readline()
		checkStr = '�ɽ�ʱ��'
		while line:
			#print line
			index = line.find(checkStr)
			if (index<0):
				line = res_data.readline()
				continue

			if flag==0:
				checkStr = '<th>'
				flag = 1
			else:
				key = dtlRe.match(line)
				if (key):
					curtime = key.group(1)
					price = key.group(2)
					p_change = key.group(3)
					curvol = int(key.group(4))
					intcurvol = int(key.group(4))
					amount = key.group(5)
					state = key.group(6)
					srange = ''
					
					#��ס��ǰҳ��һ����ʱ��
					if (bFtime==0):
						timeobj = re.search(curtime, pageFtime)
						if timeobj:
							break
						pageFtime = curtime
						bFtime = 1

					timeobj = re.search(curtime, lasttime)
					if (timeobj and intcurvol==lastvol):
						pass
					else:
						lasttime = curtime
						lastvol = intcurvol
						obj = amount.split(',')
						amount_n = ''.join(obj)
						intamount = int(amount_n)

						for j in range(0, dataObjLen):
							filvol = int(dataObj[j].volumn)
							if intcurvol<filvol:
								continue;
							if cmp(state, '����')==0:
								dataObj[j].sellvol += intcurvol
								dataObj[j].sellct += 1
								#print "S:%d %d" %(dataObj[j].sellvol, dataObj[j].sellct)
							elif cmp(state, '����')==0:
								dataObj[j].buyvol += intcurvol
								dataObj[j].buyct += 1
								#print "B:%d %d" %(dataObj[j].buyvol, dataObj[j].buyct)

						if addcsv==1:
							strline = curtime +","+ price +","+ srange +","+ p_change +","+ curvol +","+ amount_n +","+ state +"\n"
							fcsv.write(strline)

						totalline += 1
						row = totalline+1
						cell = 'A' + str(row)
						ws[cell] = curtime
						cell = 'B' + str(row)
						ws[cell] = price
						cell = 'C' + str(row)
						ws[cell] = srange
						cell = 'D' + str(row)
						ws[cell] = p_change
						cell = 'E' + str(row)
						ws[cell] = curvol
						cell = 'F' + str(row)
						ws[cell] = intamount
						cell = 'G' + str(row)
						s1 = state.decode('gbk')
						ws[cell] = s1
					count += 1
				else:
					endObj = re.search(r'</td><td>', qdate)
					if (endObj):
						print "Error line:" + line
					else:
						break;
			line = res_data.readline()

		bFtime = 0
		if (count==0):
			break;

	if addcsv==1:
		fcsv.close()
		if (totalline==0):
			os.remove(filecsv)

	if (totalline>0):
		ws = wb.create_sheet()
		write_statics(ws, '', dataObj, qdate)

	filexlsx = prepath +filename+ '.xlsx'
	wb.save(filexlsx)
	if (totalline==0):
		print qdate +" No Matched Record!"
		os.remove(filexlsx)
	else:
		print qdate+ " Saved OK!"
