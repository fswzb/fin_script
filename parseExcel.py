# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook

prepath = '../Data/'
allFileNum = 0
def printPath(level, path,fileList):
	global allFileNum
	# �����ļ��У���һ���ֶ��Ǵ�Ŀ¼�ļ���
	dirList = []
	# �����ļ�
	#fileList = []
	# ����һ���б����а�����Ŀ¼��Ŀ������(google����)
	files = os.listdir(path)
	# �����Ŀ¼����
	dirList.append(str(level))
	for f in files:
		if(os.path.isdir(path + '/' + f)):
			# �ų������ļ��С���Ϊ�����ļ��й���
			if(f[0] == '.'):
				pass
			else:
				# ��ӷ������ļ���
				dirList.append(f)
		if(os.path.isfile(path + '/' + f)):
			# ����ļ�
			fileList.append(f)
	# ��һ����־ʹ�ã��ļ����б��һ�����𲻴�ӡ
	''' Ŀǰ����Ҫ���ļ���
	i_dl = 0
	for dl in dirList:
		if(i_dl == 0):
			i_dl = i_dl + 1
		else:
			# ��ӡ������̨�����ǵ�һ����Ŀ¼
			print '-' * (int(dirList[0])), dl
			# ��ӡĿ¼�µ������ļ��к��ļ���Ŀ¼����+1
			printPath((int(dirList[0]) + 1), path + '/' + dl)
	for fl in fileList:
		# ��ӡ�ļ�
		#print '-' * (int(dirList[0])), fl
		# ������һ���ж��ٸ��ļ�
		allFileNum = allFileNum + 1
		file = os.open(fl, "r")
	'''
	
	'''
	printPath(1, path, fileList)
	for fl in fileList:
		wkfile = path +"//"+ fl
		wb = load_workbook(wkfile)
		print "Worksheet range(s):", wb.get_named_ranges()
		print "Worksheet name(s):", wb.get_sheet_names()
		if "statistics" not in wb.get_sheet_names():
			print "NONNN"
			continue

		sheet_ranges_r = wb.get_sheet_by_name(name='statistics')
		print "YYYY:"
		print sheet_ranges_r
	'''	

def parseFile(path, filename):
	wkfile = path +"/"+ filename
	print wkfile

	wb = load_workbook(wkfile)
	print "Worksheet range(s):", wb.get_named_ranges()
	print "Worksheet name(s):", wb.get_sheet_names()
	if "statistics" not in wb.get_sheet_names():
		return

	ws = wb.get_sheet_by_name(name='statistics')
	print   "Work Sheet Titile:" , ws.title
	print   "Work Sheet Rows:" , ws.max_row

	max_column = ws.max_column
	if max_column<7:
		print "column(%d) too short, please check" % max_column
		return

	# �����洢���ݵ��ֵ� 
	data_dic = {} 

	#�����ݴ浽�ֵ���
	for rx in range(1,ws.max_row):
		print "rx=", rx
		temp_list = []
		pid = ws.cell(row = rx, column = 0).value
		w1 = ws.cell(row = rx, column = 1).value
		w2 = ws.cell(row = rx, column = 2).value
		w3 = ws.cell(row = rx, column = 3).value
		w4 = ws.cell(row = rx, column = 4).value
		w5 = ws.cell(row = rx, column = 5).value
		w6 = ws.cell(row = rx, column = 6).value
		w7 = ws.cell(row = rx, column = 7).value
		temp_list = [w1,w2,w3,w4,w5,w6,w7]
		print temp_list

		data_dic[pid] = temp_list

	#��ӡ�ֵ����ݸ���
	print 'Total:%d' %len(data_dic)
	
	
	
	

if __name__ == '__main__':
	pindex = len(sys.argv)
	if pindex<2:
		sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " ����\n")
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
	#print code

	fileList = []
	path = prepath + code
	if not os.path.isdir(path):
		print "'"+ path +"' not a dir"
		exit(1)

	for (dirpath, dirnames, filenames) in os.walk(path):  
		print('dirpath = ' + dirpath)
		for filename in filenames:
			extname = filename.split('.')[-1]
			if cmp(extname,"xlsx")!=0:
				continue

			parseFile(path, filename)
			
		#�����õ����ļ��е��ļ����������ļ������ļ�
		break;

		
