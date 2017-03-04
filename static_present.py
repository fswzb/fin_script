# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import tushare as ts
from internal.ts_common import *

curdate = ''
data_path = "..\\Data\\_self_define.txt"
stockCode = []

today = datetime.date.today()
curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
#print curdate

#˵��show_flag
#0�������ÿһֻ����ͨ�̣�������㻻����
#1�����ÿһֻ����ͨ�̣����Ҽ��㻻����
#2����ʾÿһֻ���µ����ţ����������ȫ����ʾ������û��ֻ��ʾһ��news
pindex = len(sys.argv)

st_bas=ts.get_stock_basics()
st_bas.to_excel("a_stock_base.xlsx")
st_pb_base = st_bas[st_bas.pb!=0]
st_pb_base = st_pb_base.sort_values(['timeToMarket'], 0, False)
st_pb_base.to_excel("a_stock_pb_base.xlsx")
st_index = st_pb_base.index
st_list=list(st_index)

number = len(st_list)
if number>0:
	#ZTһ��ȡ�� base ��
	#��ȡlist��ͨ��������ʼλ��
	base = 23
	ed = 0
	tl = number
	ct = tl/base
	if tl%base!=0:
		ct += 1
	for i in range(0, ct):
		ed = min(base*(i+1), tl)
		cut_list = st_list[i*base:ed]
		if len(cut_list)==0:
			break
		print cut_list
		stdf = ts.get_realtime_quotes(cut_list)

