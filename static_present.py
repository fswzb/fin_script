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
st_bas.to_excel("atemp.xlsx")