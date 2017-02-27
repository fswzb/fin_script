# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
import tushare as ts
import internal.common
from internal.ts_common import *

#Ŀǰflag����Ĭ��0
#����Ϊ1���г��Ǵ�����ͣ����ͣ�͵�ͣ��������

# ��ͣ��һ����ͣ����ͣ���䡢һ�ִ���
zt=0
yzzt=0
zthl=0
yzcx=0

# ��ͣ��һ�ֵ�ͣ����ͣ����
dt=0
yzdt=0
dtft=0

# ���ǡ��µ���ƽ��
szstk=0
xdstk=0
ppstk=0

def analyze_df(df, flag):
	global zt
	global yzzt
	global zthl
	global yzcx
	global dt
	global yzdt
	global dtft
	global szstk
	global xdstk
	global ppstk

	if df is None:
		return

	oldst = []
	dt_list = []
	dtft_list = []
	# ������һ�ִ���
	zt_list = []
	for index,row in df.iterrows():
		#print row[0],row[1],row[2],row[3],row[4],row[5],row[6]
		chg_percent = float(row[2])
		high = float(row['high'])
		low = float(row['low'])
		trade = float(row['trade'])
		volume = int(row['volume'])
		if volume==0:
			continue
		if chg_percent>=9.9:
			all_yz = check_cx(row[0])
			if trade==high:
				zt += 1
				if all_yz==0 and high!=low:
					zt_list.append(row[0])
			if high==low:
				yzzt += 1
				if all_yz==1:
					yzcx += 1
				else:
					print row[0]
					oldst.append(row[0])
					#print row[0],row[1]
			szstk += 1
		elif chg_percent<=-9.9:
			if trade==low:
				dt += 1
				dt_list.append(row[0])
			if high==low:
				yzdt += 1
			xdstk += 1
		else:
			pre_close = float(row['settlement'])
			high_perct = (high-pre_close)*100/pre_close
			low_perct = (low-pre_close)*100/pre_close
			if high_perct>=9.9:
				zthl += 1
			if low_perct<=-9.9:
				dtft += 1
				dtft_list.append(row[0])
			if chg_percent>0:
				szstk += 1
			elif chg_percent<0:
				xdstk += 1
			else:
				ppstk += 1
	#һ��list׷����һ��list��Ҫextend������append()
	zt_list.extend(oldst)
	print zt_list
	
	print "ZT: %4d(%4d%4d)(%4d%4d)"%(zt, yzzt, zthl, yzcx, (yzzt-yzcx))
	print "DT: %4d(%4d%4d)"%(dt, yzdt, dtft)
	print "ST: %4d %4d%4d"%(szstk, xdstk, ppstk)

	if flag==1:
		#print dt_list
		#print dtft_list
		number = len(zt_list)
		if number>0:
			#ZTһ��ȡ�� base ��
			#��ȡlist��ͨ��������ʼλ��
			base = 20
			ed = 0
			tl = len(zt_list)
			ct = tl/base
			if tl%base!=0:
				ct += 1
			for i in range(0, ct):
				ed = min(base*(i+1), tl)
				cut_list = zt_list[i*base:ed]
				if len(cut_list)==0:
					break
				stdf = ts.get_realtime_quotes(cut_list)
				print stdf[['code','name','price','high','low','pre_close','open']]
			print "==================================================="
		
		number = len(dt_list)
		if number>0 and number<30:
			stdf = ts.get_realtime_quotes(dt_list)
			print stdf[['code','name','price','low','pre_close','open']]
		elif number>=30:
			print "DT number too much"
		if number>0 and number<30:
			stdf = ts.get_realtime_quotes(dtft_list)
			print stdf[['code','name','price','low','pre_close','open']]
		elif number>=30:
			print "DTFT number too much"

#main run from here��
show_idx = ['000001', '399001', '399005', '399006']
idx_df=ts.get_index()
show_index_info(idx_df, show_idx)

df = ts.get_today_all()
print ''
flag = 0
pindex = len(sys.argv)
if pindex==2:
	flag = int(sys.argv[1])
analyze_df(df, flag)