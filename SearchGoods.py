#python;
#coding=utf-8;
#Author:张祖兴 iyueer@163.com

from csv import DictReader, writer;
import shelve, dbhash, anydbm;
from re import match, sub, split;
import wx;
from time import strftime, localtime;
from types import FloatType, IntType;
from xlwt import Workbook;
from xlrd import open_workbook;
from datetime import datetime, date, timedelta;
from os.path import join, getmtime;
from os import remove;
import win32print;
from string import letters;
# import logging;

# logging.basicConfig(format='%(levelname)s %(filename)s(%(lineno)d): %(message)s',\
#                     level = logging.DEBUG)

def StoreDataFromCSV(filename,db):
	a={};#add
	GoodsID="";#add
	csvfile = file(filename, 'rb');
	reader = DictReader(csvfile);
	try:
		for i in reader:
			ID=i["\xc9\xcc\xc6\xb7\xb1\xe0\xba\xc5"];
			price=i["\xb1\xea\xd7\xbc\xb5\xf5\xc5\xc6\xbc\xdb"];
			if(ID!=""):
				if(match(r'^[a-zA-Z0-9]*\_*[a-zA-Z0-9]*\-*[a-zA-Z0-9]*$', ID)):
					if(price!=""):
						if(match(r"\d+\.*\d*", price)):
							if('\xc9\xcc\xc6\xb7\xc0\xe0\xb1\xf0' in i.keys()):
								if('\xd1\xd5\xc9\xab' in i.keys()):
									if("S" in i.keys()):
										if("M" in i.keys()):
											if("L" in i.keys()):
												if("XL" in i.keys()):
													if("XXL" in i.keys()):
														if("\xbf\xe2\xb4\xe6\xca\xfd" in i.keys()):
															if("\xb1\xb8\xd7\xa2" in i.keys()):
																if("\xc8\xeb\xbf\xe2\xca\xb1\xbc\xe4" in i.keys()):
																	if(match(r"\d+",i["S"]) or i["S"]=="" or i["S"]==None):
																		if(match(r"\d+",i["M"]) or i["M"]=="" or i["M"]==None):
																			if(match(r"\d+",i["L"]) or i["L"]=="" or i["L"]==None):
																				if(match(r"\d+",i["XL"]) or i["XL"]=="" or i["XL"]==None):
																					if(match(r"\d+",i["XXL"]) or i["XXL"]=="" or i["XXL"]==None):
																						GoodsID=a["GID"]=ID;
																						a["GName"]=i["\xc9\xcc\xc6\xb7\xc0\xe0\xb1\xf0"];
																						a['GColor']=i['\xd1\xd5\xc9\xab'];
																						a['S']=i['S'];
																						a['M']=i['M'];
																						a['L']=i['L'];
																						a['XL']=i['XL'];
																						a['XXL']=i['XXL'];
																						a['GComments']=i['\xb1\xb8\xd7\xa2'];
																						a['GPrice']=price;
																						a['GStoreTime']=i['\xc8\xeb\xbf\xe2\xca\xb1\xbc\xe4'];
																						if(a["GName"]==None):
																							a["GName"]="";
																						if(a['GColor']==None):
																							a['GColor']="";
																						if(len(a["S"])==1):
																							a["S"]="0"+a["S"];
																						if(a["S"]=="" or int(a["S"])==0 or a["S"]==None):
																							a["S"]="0";
																						if(len(a["M"])==1):
																							a["M"]="0"+a["M"];
																						if(a["M"]=="" or int(a["M"])==0 or a["M"]==None):
																							a["M"]="0";
																						if(len(a["L"])==1):
																							a["L"]="0"+a["L"];
																						if(a["L"]=="" or int(a["L"])==0  or a["L"]==None):
																							a["L"]="0";
																						if(len(a["XL"])==1):
																							a["XL"]="0"+a["XL"];
																						if(a["XL"]=="" or int(a["XL"])==0 or a["XL"]==None):
																							a["XL"]="0";
																						if(len(a["XXL"])==1):
																							a["XXL"]="0"+a["XXL"];
																						if(a["XXL"]=="" or int(a["XXL"])==0 or a["XXL"]==None):
																							a["XXL"]="0";
																						if(a['GComments']==None):
																							a['GComments']="";
																						if(match(r".*:.*", a['GStoreTime'])):
																							a['GStoreTime']=sub(r"\:","-",a['GStoreTime']);
																						if(match(r".*\/.*", a['GStoreTime'])):
																							a['GStoreTime']=sub(r"\/","-",a['GStoreTime']);
																						if(a['GStoreTime']=="" or a['GStoreTime']==None):
																							a['GStoreTime']=DateFormat(strftime("%Y-%m-%d", localtime()));
																						else:
																							try:
																								a['GStoreTime']=DateFormat(a['GStoreTime']);
																							except:
																								pass;
																						a["GStoreNum"]=str(int(a['S'])+int(a['M'])+int(a['L'])+int(a['XL'])+int(a['XXL']));
																						# a["GStoreNum"]="0";
																						if(len(a["GStoreNum"])==1):
																							a["GStoreNum"]="0"+a["GStoreNum"];
																						if(int(a["GStoreNum"])!=0):
																							db[GoodsID]=a;
																					else:
																						SizeColumnFormatMessageBox("XXL");
																						csvfile.close();
																						return False;
																				else:
																					SizeColumnFormatMessageBox("XL");
																					csvfile.close();
																					return False;
																			else:
																				SizeColumnFormatMessageBox("L");
																				csvfile.close();
																				return False;
																		else:
																			SizeColumnFormatMessageBox("M");
																			csvfile.close();
																			return False;
																	else:
																		SizeColumnFormatMessageBox("S");
																		csvfile.close();
																		return False;
																else:
																	GStoreTimeMessageBox();
																	csvfile.close();
																	return False;
															else:
																GCommentsMessageBox();
																csvfile.close();
																return False;
														else:
															GStoreNumMessageBox();
															csvfile.close();
															return False;
													else:
														SizeItemNotFoundMessageBox("XXL");
														csvfile.close();
														return False;
												else:
													SizeItemNotFoundMessageBox("XL");
													csvfile.close();
													return False;
											else:
												SizeItemNotFoundMessageBox("L");
												csvfile.close();
												return False;
										else:
											SizeItemNotFoundMessageBox("M");
											csvfile.close();
											return False;
									else:
										SizeItemNotFoundMessageBox("S");
										csvfile.close();
										return False;
								else:
									GColorMessageBox();
									csvfile.close();
									return False;
							else:
								GNameMessageBox();
								csvfile.close();
								return False;
						else:
							GPriceFormatMessageBox();
							csvfile.close();
							return False;
					else:
						GPriceMessageBox();
						csvfile.close();
						return False;
				else:
					GIDFormatMessageBox();
					csvfile.close();
					return False;
			else:
				GIDMessageBox();
				csvfile.close();
				return False;
	except:
		csvfile.close();
		return False;
	csvfile.close();
	return True;


def StoreDataFromExcel(Excelname, db):
	a={};#add
	GoodsID="";#add
	try:
		book=open_workbook(Excelname);
		table = book.sheets()[0];
		ncols = table.ncols #列数
		nrows = table.nrows #行数
		TotalList=[];
		for m in range(1,nrows):
			TempDict={}
			for n in range(0, len(table.row_values(0))):
				try:
					DictKey=(table.row_values(0)[n]).encode('gb2312'); ##先对DictKey做编码。
				except:
					DictKey=(table.row_values(0)[n]).encode('iso8859-1');
				# print DictKey;
				try:
					# print repr(table.row_values(m)[n]);
					if(type(float(table.row_values(m)[n])) is FloatType):###由于float不能做编码， 所以转换成int形.
						TempDict["%s"%DictKey]= str(int(table.row_values(m)[n]));
				except:
					try:
						TempDict["%s"%DictKey]= table.row_values(m)[n].encode('gb2312');#先对DictValue做编码。
					except:
						TempDict["%s"%DictKey]= (table.row_values(m)[n]).encode('iso8859-1');#先对DictValue做编码。
					# print TempDict;
			TotalList.append(TempDict);

		for i in TotalList:
			# print i;
			try:
				ID=i["\xc9\xcc\xc6\xb7\xb1\xe0\xba\xc5"];
				price=i["\xb1\xea\xd7\xbc\xb5\xf5\xc5\xc6\xbc\xdb"];
				if(ID!=""):
					if(match(r'^[a-zA-Z0-9]*\_*[a-zA-Z0-9]*\-*[a-zA-Z0-9]*$', ID)):
						if(price!=""):
							if(match(r"\d+\.*\d*", price)):
								if('\xc9\xcc\xc6\xb7\xc0\xe0\xb1\xf0' in i.keys()):
									if('\xd1\xd5\xc9\xab' in i.keys()):
										if("S" in i.keys()):
											if("M" in i.keys()):
												if("L" in i.keys()):
													if("XL" in i.keys()):
														if("XXL" in i.keys()):
															if("\xbf\xe2\xb4\xe6\xca\xfd" in i.keys()):
																if("\xb1\xb8\xd7\xa2" in i.keys()):
																	if("\xc8\xeb\xbf\xe2\xca\xb1\xbc\xe4" in i.keys()):
																		if(match(r"\d+",i["S"]) or i["S"]=="" or i["S"]==None):
																			if(match(r"\d+",i["M"]) or i["M"]=="" or i["M"]==None):
																				if(match(r"\d+",i["L"]) or i["L"]=="" or i["L"]==None):
																					if(match(r"\d+",i["XL"]) or i["XL"]=="" or i["XL"]==None):
																						if(match(r"\d+",i["XXL"]) or i["XXL"]=="" or i["XXL"]==None):
																							GoodsID=a["GID"]=ID;
																							a["GName"]=i["\xc9\xcc\xc6\xb7\xc0\xe0\xb1\xf0"];
																							a['GColor']=i['\xd1\xd5\xc9\xab'];
																							a['S']=i['S'];
																							a['M']=i['M'];
																							a['L']=i['L'];
																							a['XL']=i['XL'];
																							a['XXL']=i['XXL'];
																							a['GComments']=i['\xb1\xb8\xd7\xa2'];
																							a['GPrice']=price;
																							a['GStoreTime']=i['\xc8\xeb\xbf\xe2\xca\xb1\xbc\xe4'];
																							if(a["GName"]==None):
																								a["GName"]="";
																							if(a['GColor']==None):
																								a['GColor']="";
																							if(len(a["S"])==1):
																								a["S"]="0"+a["S"];
																							if(a["S"]=="" or int(a["S"])==0 or a["S"]==None):
																								a["S"]="0";
																							if(len(a["M"])==1):
																								a["M"]="0"+a["M"];
																							if(a["M"]=="" or int(a["M"])==0 or a["M"]==None):
																								a["M"]="0";
																							if(len(a["L"])==1):
																								a["L"]="0"+a["L"];
																							if(a["L"]=="" or int(a["L"])==0  or a["L"]==None):
																								a["L"]="0";
																							if(len(a["XL"])==1):
																								a["XL"]="0"+a["XL"];
																							if(a["XL"]=="" or int(a["XL"])==0 or a["XL"]==None):
																								a["XL"]="0";
																							if(len(a["XXL"])==1):
																								a["XXL"]="0"+a["XXL"];
																							if(a["XXL"]=="" or int(a["XXL"])==0 or a["XXL"]==None):
																								a["XXL"]="0";
																							# if(len(a["GPrice"])==1 and ):
																							# 	a["GPrice"]="00"+a["GPrice"];
																							# if(len(a["GPrice"])==2):
																							if(a['GComments']==None):
																								a['GComments']="";
																							if(match(r".*:.*", a['GStoreTime'])):
																								a['GStoreTime']=sub(r"\:","-",a['GStoreTime']);
																							if(match(r".*\/.*", a['GStoreTime'])):
																								a['GStoreTime']=sub(r"\/","-",a['GStoreTime']);
																							if(a['GStoreTime']=="" or a['GStoreTime']==None):
																								a['GStoreTime']=DateFormat(strftime("%Y-%m-%d", localtime()));
																							else:
																								try:
																									a['GStoreTime']=DateFormat(a['GStoreTime']);
																								except:
																									pass;
																							a["GStoreNum"]=str(int(a['S'])+int(a['M'])+int(a['L'])+int(a['XL'])+int(a['XXL']));
																							# a["GStoreNum"]="0";
																							if(len(a["GStoreNum"])==1):
																								a["GStoreNum"]="0"+a["GStoreNum"];
																							if(int(a["GStoreNum"])!=0):
																								db[GoodsID]=a;
																						else:
																							SizeColumnFormatMessageBox("XXL");
																							return False;
																					else:
																						SizeColumnFormatMessageBox("XL");
																						return False;
																				else:
																					SizeColumnFormatMessageBox("L");
																					return False;
																			else:
																				SizeColumnFormatMessageBox("M");
																				return False;
																		else:
																			SizeColumnFormatMessageBox("S");
																			return False;
																	else:
																		GStoreTimeMessageBox();
																		return False;
																else:
																	GCommentsMessageBox();
																	return False;
															else:
																GStoreNumMessageBox();
																return False;
														else:
															SizeItemNotFoundMessageBox("XXL");
															return False;
													else:
														SizeItemNotFoundMessageBox("XL");
														return False;
												else:
													SizeItemNotFoundMessageBox("L");
													return False;
											else:
												SizeItemNotFoundMessageBox("M");
												return False;
										else:
											SizeItemNotFoundMessageBox("S");
											return False;
									else:
										GColorMessageBox();
										return False;
								else:
									GNameMessageBox();
									return False;
							else:
								GPriceFormatMessageBox();
								return False;
						else:
							GPriceMessageBox();
							return False;
					else:
						GIDFormatMessageBox();
						return False;
				else:
					GIDMessageBox();
					return False;
			except:
				return False;
	except:
		return False;
	return True;


def WriteToCSV(csvname):
    dbreader=shelve.open('database.dat','r');
    csvfile = file(csvname, 'wb');
    csvwriter = writer(csvfile);
    csvwriter.writerow(['''\xc9\xcc\xc6\xb7\xb1\xe0\xba\xc5''','''\xc9\xcc\xc6\xb7\xc0\xe0\xb1\xf0''',\
        '''\xd1\xd5\xc9\xab''',"S","M","L","XL","XXL",'''\xbf\xe2\xb4\xe6\xca\xfd''','''\xb1\xea\xd7\xbc\xb5\xf5\xc5\xc6\xbc\xdb''',\
        '''\xb1\xb8\xd7\xa2''','''\xc8\xeb\xbf\xe2\xca\xb1\xbc\xe4''']);
    for i in GetDBValues(dbreader):
        data=[i['GID'],i['GName']\
        ,i['GColor'],i["S"],i["M"],i["L"],i["XL"],i["XXL"],i['GStoreNum'],\
        i['GPrice'],i['GComments'],i['GStoreTime']];
        csvwriter.writerow(data);
    csvfile.close();
    dbreader.close();

def WriteToExcel(Excelfile):
	dbreader=shelve.open('database.dat','r');
	book=Workbook(encoding="utf-8", style_compression=0)
	sheet=book.add_sheet(u'商品库存信息表', cell_overwrite_ok=True)
	#写第一行：
	FirstRow=['''\xc9\xcc\xc6\xb7\xb1\xe0\xba\xc5''','''\xc9\xcc\xc6\xb7\xc0\xe0\xb1\xf0''',\
        '''\xd1\xd5\xc9\xab''',"S","M","L","XL","XXL",'''\xbf\xe2\xb4\xe6\xca\xfd''','''\xb1\xea\xd7\xbc\xb5\xf5\xc5\xc6\xbc\xdb''',\
        '''\xb1\xb8\xd7\xa2''','''\xc8\xeb\xbf\xe2\xca\xb1\xbc\xe4'''];
	for m in range(0,len(FirstRow)):
		sheet.write(0, m, "%s"%FirstRow[m].decode('gb2312'));

	bigdata=[];
	for i in GetDBValues(dbreader):
		FormatTime=i['GStoreTime'];
		FormatTime=sub(r"-",":",FormatTime);
		# print FormatTime;
		data=[i['GID'],i['GName']\
		,i['GColor'],i["S"],i["M"],i["L"],i["XL"],i["XXL"],i['GStoreNum'],\
		i['GPrice'],i['GComments'],FormatTime];
		bigdata.append(data);
	
	bigdata.sort(reverse=True);

	# print len(bigdata);
	for n in range(0, len(bigdata)):
		for h in range(0, 12):
			try:
				if(type(int(bigdata[n][h])) is IntType):
					sheet.write((n+1), h, bigdata[n][h]);
			except:
				sheet.write((n+1), h, bigdata[n][h].decode('gb2312'));
	book.save("%s"%Excelfile);
	dbreader.close();

def DateFormat(Timer):
	Timer=str(Timer);
	lists=split("-", Timer);
	if(len(str(lists[1]))==1):
		lists[1]="0"+str(lists[1]);
	if(len(str(lists[2]))==1):
		lists[2]="0"+str(lists[2]);
	Timer=lists[0]+"-"+lists[1]+"-"+lists[2];
	return Timer;

def DetailSellTimeFormat(Timer):
	Timer=str(Timer);
	Timer=Timer[:4]+"-"+Timer[4:6]+"-"+Timer[6:8]+" "+Timer[8:10]+":"+Timer[10:12]+":"+Timer[12:14];
	return Timer;

def GetGoodsName(ID):
	GoodsName="";
	dbreader=shelve.open('database.dat','r');
	GoodsName=dbreader[ID]['GName'];
	dbreader.close();
	return GoodsName;


def GetGoodsColor(ID):
	GoodsColor="";
	dbreader=shelve.open('database.dat','r');
	GoodsColor=dbreader[ID]['GColor'];
	dbreader.close();
	return GoodsColor;

def GetDBValues(db):
	values=[];
	for item in db.items():
		values.append(db[item[0]]);
		# print db[item[0]];
		# print "*"*20;
	# print values;
	values.sort(reverse=True);
	return values;

def GetQuery_To_tuple(ID):
	dbreader=shelve.open('database.dat','r');
	ID=str(ID);
	tuples=(dbreader[ID]['GID'],dbreader[ID]['GName'],\
			dbreader[ID]['GColor'],dbreader[ID]["S"],dbreader[ID]["M"],dbreader[ID]["L"],\
			dbreader[ID]["XL"],dbreader[ID]["XXL"],dbreader[ID]['GStoreNum'],dbreader[ID]['GPrice'],\
			dbreader[ID]['GComments'],dbreader[ID]['GStoreTime']);
	# print tuples;
	dbreader.close();
	return tuples;

def GetDBValues_To_tuple(values,db):
	for item in db.items():
		tupledata=(item[1]['GID'],item[1]['GName'],\
			item[1]['GColor'],item[1]["S"],item[1]["M"],item[1]["L"],\
			item[1]["XL"],item[1]["XXL"],item[1]['GStoreNum'],item[1]['GPrice'],\
			item[1]['GComments'],item[1]['GStoreTime']);
		values.append(tupledata);
		# print tupledata;
	# print values;
	return values;


def GetPrintList_To_tuple(values,db):
	for item in db.items():
		if(item[1]["Printed"]==1):
			tupledata=(item[1]["ID"],item[1]["Name"],item[1]["amount"],item[1]['Perprice']);
			values.append(tupledata);
	# 	print tupledata;
	# print values;
	return values;


def StoreRecord(id,dictdata):
	dbwriter=shelve.open('database.dat','w',writeback=True);
	dbwriter[id]=dictdata;
	dbwriter.close();


def ListBox_Display():
    Accounts=[];
    dbreader=shelve.open('Account.dat','r');
    for i in dbreader.items():
    	if(i[0]!="admin"):
        	Accounts.append(i[0]);
    dbreader.close();
    return Accounts;

def ListBox_Display_withAdmin():
    Accounts=[];
    dbreader=shelve.open('Account.dat','r');
    for i in dbreader.items():
        Accounts.append(i[0]);
    dbreader.close();
    return Accounts;

def Active_Account_Name():
    dbreader=shelve.open('Account.dat','r');
    for i in dbreader.items():
    	if(i[0]!="admin"):
    		if(i[1]["IsActive"]=="Yes"):
    			dbreader.close()
    			return i[0];


def Recent_Login_Account_Name():
    dbreader=shelve.open('Account.dat','r');
    for i in dbreader.items():
    	if(i[0]!="admin"):
    		if(i[1]["IsRecentAccount"]=="Yes"):
				dbreader.close();
				return i[0];


def Disable_Active_Account():
	Name=Active_Account_Name();
	if(Name!=None):
		dbwriter=shelve.open('Account.dat','w', writeback=True);
		dbwriter[Name]["IsActive"]="No";
		dbwriter.close();
	else:
		pass;

def SizeList_Display(ID):
	'''
	Return the avaliable Size list before QuerySell.
	'''
	SizeList=[];
	ID=str(ID)
	dbreader=shelve.open('database.dat','r');
	if(dbreader[ID]["S"]!="0"):
		SizeList.append("S");
	if(dbreader[ID]["M"]!="0"):
		SizeList.append("M");
	if(dbreader[ID]["L"]!="0"):
		SizeList.append("L");
	if(dbreader[ID]["XL"]!="0"):
		SizeList.append("XL");
	if(dbreader[ID]["XXL"]!="0"):
		SizeList.append("XXL");
	# SizeList.append("");
	dbreader.close();
	return SizeList;

def SellPageJudge(ID, size, vendor, price, count):
	'''1. Judge id's format
	   2. Judge id is the database ID
	   3. Judge Size is <=0
	'''
	# print size;
	dbreader=shelve.open('database.dat','r')
	if(size in ["S","M","L","XL","XXL"]):
		if(int(dbreader[ID][size])>=1):
			if(vendor in ListBox_Display()):
				if(price!=0 and price!=""):
					if(match(r'\d+',count)):
						dbreader.close();
						return True;
					else:
						CountFormatErrorMessageBox();
						dbreader.close();
						return False;
				else:
					PriceNotGetMessagebox();
					dbreader.close();
					return False;
			else:
				VendorErrorMessageBox();
				dbreader.close();
				return False;
		else:
			NoStoreMessageBox();
			dbreader.close();
			return False;
	else:
		SizeInputErrorMessageBox();
		return False;

def IDJudge(ID):
	'''1. Judge id's format
	   2. Judge id is the database ID
	'''
	dbreader=shelve.open('database.dat','r')
	# print dbreader.keys();
	ID=str(ID);
	if ID in dbreader.keys():
		dbreader.close();
		return True;
	else:
		dbreader.close();
		return False;

def SellStatement(ID, name, color, size, vendor, price, count, finalprice):
	'''Store the sell info into a database file'''
	Time=FormatTime(datetime.now());
	ShortTime = FormatShortTime(datetime.now());
	dbwriter=shelve.open("Statement.dat", "c");
	dbwriter[Time]={"ID":ID, "ShortTime":ShortTime, "Name": name,"Color":color,"Size":size,"Vendor":vendor, "Price":price, "Count":count,"Finalprice":finalprice};
	dbwriter.close();

def SellPrintData(ID, name, color, size, vendor, price, perprice,count, finalprice, pricegap, printed, amount):
	'''Store the sell Printer into a database file'''
	dbwriter=shelve.open("PrintList.dat", "c");
	dbwriter[ID]={"ID":ID, "Name": name,"Color":color,"Size":size,"Vendor":vendor, "Price":price, "Perprice":perprice, "Count":count,"Finalprice":finalprice,"PriceGap":pricegap, "Printed":printed, "amount":"1"};
	dbwriter.close();


def UpdatedDB(ID, size):
	'''
	Minus the Size number.
	Minus the TotalStoreNumber.
	'''
	ID=str(ID);
	dbreader=shelve.open('database.dat','r');
	tempsize=str(int(dbreader[ID][size])-1);
	if(len(tempsize)==1):
		tempsize="0"+tempsize;
	if(int(tempsize)==0):
		tempsize="0";
	temptotalsize=str(int(dbreader[ID]['GStoreNum'])-1);
	if(len(temptotalsize)==1):
		temptotalsize="0"+temptotalsize;
	if(int(temptotalsize)==0):
		temptotalsize="0";
	dbreader.close();

	dbwriter=shelve.open('database.dat','w',writeback=True);
	dbwriter[ID][size]=tempsize;
	dbwriter[ID]['GStoreNum']=temptotalsize;
	dbwriter.close();

def DeleteEmptyDB(ID):
	ID=str(ID);
	dbwriter=shelve.open('database.dat','w',writeback=True);
	if(int(dbwriter[ID]['GStoreNum'])<=0):
		dbwriter.pop(ID);
		DeleteEmptyMessageBox();
		dbwriter.close();
		return True;
	else:
		dbwriter.close();
		return None;

def DeleteAccountDB(ID):
	# ID=str(ID);
	dbwriter=shelve.open('Account.dat','w',writeback=True);
	dbwriter.pop(ID);
	dbwriter.close();

def PurchaseJugdement(ID,S,M,L,XL,XXL,Price):
	if(match(r'^[a-zA-Z0-9]*\_*[a-zA-Z0-9]*\-*[a-zA-Z0-9]*$',ID) and ID!="" and (match(r'\d+',S) or S=="")\
	 and (match(r'\d+',M) or M=="") and (match(r'\d+',L) or L=="")\
	 and (match(r'\d+',XL) or XL=="") and (match(r'\d+',XXL) or XXL=="")\
	 and (match(r'\d+\.*\d*',Price) and (int(Price)!=0))):
		return True;
	else:
		return False;

def ModifyJugdement(ID,S,M,L,XL,XXL,Price):
	if(match(r'^[a-zA-Z0-9]*\_*[a-zA-Z0-9]*\-*[a-zA-Z0-9]*$',ID) and (match(r'\d+',S) or S=="")\
	 and (match(r'\d+',M) or M=="") and (match(r'\d+',L) or L=="")\
	 and (match(r'\d+',XL) or XL=="") and (match(r'\d+',XXL) or XXL=="")\
	 and (match(r'\d+\.*\d*',Price) or Price=="")):
		return True;
	else:
		return False;


def FormatTime(datetimer):
	datetimer=str(datetimer);
	# print datetime;
	datetimer=sub(r'-','',datetimer);
	datetimer=sub(r':','',datetimer);
	datetimer=sub(r'\.','',datetimer);
	datetimer=sub(r'\s','',datetimer);
	return datetimer[:15];


def FormatShortTime(datetime):
	datetime=str(datetime);
	return datetime[2:16];

def GetStarStatementRows_Tuple():
	AllRows=[];
	SaleAmounts_List=[];
	NewSaleAmounts_List=[];
	for j in ListBox_Display():
		SaleAmounts_List.append([int(StarSaleAmount(j)),StarSaleVolumn(j),j]);
	SaleAmounts_List.sort(reverse=True);##按销量排序.

	if(len(ListBox_Display())>=10):
		for i in range(0,10):
			AllRows.append(List_PositionAdjust(SaleAmounts_List[i]));
		return AllRows;
	else:
		for i in range(0,len(ListBox_Display())):
			AllRows.append(List_PositionAdjust(SaleAmounts_List[i]));
		return AllRows;


def StarSaleAmount(vendor):
	''''销量'''
	OneVendorSaleAmount=0;
	dbreader=shelve.open('statement.dat','r');
	for i in dbreader.items():
		if(i[1]["Vendor"]==vendor):
			OneVendorSaleAmount=OneVendorSaleAmount+1;
	dbreader.close();
	return OneVendorSaleAmount;

def StarSaleVolumn(vendor):
	'''销售总额'''
	OneVendorSaleVolumn=0;
	dbreader=shelve.open('statement.dat','r');
	for i in dbreader.items():
		if(i[1]["Vendor"]==vendor):
			OneVendorSaleVolumn=int(i[1]["Finalprice"])+OneVendorSaleVolumn;
	dbreader.close();
	return OneVendorSaleVolumn;

def GoodsNameType():
	GoodsNameType_List=[];
	dbreader=shelve.open('statement.dat','r');
	for i in dbreader.items():
		if(i[1]["Name"]!=""):
			GoodsNameType_List.append(i[1]["Name"]);

	GoodsNameType_List=sorted(set(GoodsNameType_List));
	dbreader.close();
	return GoodsNameType_List;
# print GoodsNameType();

def GetGoodsStatementRows_Tuple():
	AllRows=[];
	# AllRowPart=();
	SaleAmounts_List=[];
	NewSaleAmounts_List=[];
	for j in GoodsNameType():
		SaleAmounts_List.append([int(GoodsSaleAmount(j)),GoodsSaleVolumn(j),j]);
	SaleAmounts_List.sort(reverse=True);##按销量排序.
	# print SaleAmounts_List;
	# print len(GoodsNameType());

	if(len(GoodsNameType())>=10):
		for i in range(0,10):
			AllRows.append(List_PositionAdjust(SaleAmounts_List[i]));
		return AllRows;
	else:
		for i in range(0,len(GoodsNameType())):
			# print SaleAmounts_List[i];
			AllRows.append(List_PositionAdjust(SaleAmounts_List[i]));
		return AllRows;

def List_PositionAdjust(ListName):
	temp1="";
	temp2="";
	temp1=str(ListName[0]);
	temp2=str(ListName[1]);
	ListName[0]=str(ListName[2]);
	ListName[1]=temp1;
	ListName[2]=temp2;
	return tuple(ListName);


def GoodsSaleAmount(Nametype):
	''''销量'''
	OneGoodsSaleAmount=0;
	dbreader=shelve.open('statement.dat','r');
	for i in dbreader.items():
		if(i[1]["Name"]==Nametype):
			OneGoodsSaleAmount=OneGoodsSaleAmount+1;
	dbreader.close();
	return OneGoodsSaleAmount;

def GoodsSaleVolumn(Nametype):
	'''销售总额'''
	OneGoodsSaleVolumn=0;
	dbreader=shelve.open('statement.dat','r');
	for i in dbreader.items():
		if(i[1]["Name"]==Nametype):
			OneGoodsSaleVolumn=int(i[1]["Finalprice"])+OneGoodsSaleVolumn;
	dbreader.close();
	return OneGoodsSaleVolumn;

def FormatDate(Datetime):
	datetime=str(Datetime);
	datetime=sub(r'-','',datetime);
	return datetime[:8];

def FormatDetailTime(datetime):
    datetime = str(datetime);
    return datetime[:19];


def GetDetailTime():
    return str(FormatDetailTime(datetime.now()));


def DeleteBackup(path, filename):
    now = date.today();
    EndTimer=now-timedelta(days = 90);
    EndTimer=int(FormatDate(EndTimer));
    FileModifyTime = getmtime(join(path, filename));
    FileModifyTime = date.fromtimestamp(FileModifyTime);
    FileModifyTime = int(FormatDate(FileModifyTime));
    if(FileModifyTime <= EndTimer):
    	remove(join(path,filename));

def Printer_Ready():
    try:
        printer_name = win32print.GetDefaultPrinter()
    except:
        printer_name = None;
    return printer_name;

def Printer_Process(raw_data):
    printer_name = win32print.GetDefaultPrinter()
    try:
        raw_data = raw_data.encode('gb2312');
    except:
        raw_data = raw_data;
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Sell Receipt", None, "RAW"))
        try:
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, raw_data)
            win32print.EndPagePrinter(hPrinter)
        finally:
            win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)

def Printer_Sell(raw_data):
    try:
        raw_data = raw_data.encode('gb2312');
    except:
        raw_data = raw_data;
    return raw_data;


# def Printer_Sell(raw_data):
#     printer_name = win32print.GetDefaultPrinter()
#     try:
#         raw_data = raw_data.encode('gb2312');
#     except:
#         raw_data = raw_data;
#     hPrinter = win32print.OpenPrinter(printer_name)
#     try:
#         hJob = win32print.StartDocPrinter(hPrinter, 1, ("Sell Receipt", None, "RAW"))
#         try:
#             win32print.StartPagePrinter(hPrinter)
#             win32print.WritePrinter(hPrinter, raw_data)
#             win32print.EndPagePrinter(hPrinter)
#         finally:
#             win32print.EndDocPrinter(hPrinter)
#     finally:
#         win32print.ClosePrinter(hPrinter)

class CharValidator(wx.PyValidator):
    def __init__(self, flag):
         wx.PyValidator.__init__(self)
         self.flag = flag
         self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
         """
         Note that every validator must implement the Clone() method.
         """
         return CharValidator(self.flag)

    def Validate(self, win):
         return True

    def TransferToWindow(self):
         return True 

    def TransferFromWindow(self):
         return True

    def OnChar(self, evt):
         key = chr(evt.GetKeyCode())
         if self.flag == "no-alpha" and key in letters:
              return
         evt.Skip()

class ErrorMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"输入数据有误,请再次检查", u'错误', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class GoodsIDExistMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"对不起, 商品编号已经存在, 如需更新请到出入库菜单->二次入库登记进行修改更新", u'错误', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class PurchaseErrorMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"对不起, 输入数据有误, 请再次检查,\n1.商品编号与吊牌价为必填项\n2.商品编号格式应为数字字母下划线_或者-,类似为65000或65000B或65000_B, \n3.尺码与吊牌价必须为纯数字, 谢谢!", u'错误', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class UpdateErrorMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"对不起, 输入数据有误, 请再次检查,\n1.吊牌价为必填项,不可为空, 不可为零.\n2.尺码与吊牌价必须为纯数字, 谢谢!", u'错误', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class ModifyErrorMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"对不起, 输入数据有误, 请再次检查,\n1.商品编号为必填项, 且应和需要修改的商品商品编号相同.\n2.商品编号格式应为数字字母下划线_或者-,类似为65000或65000B或65000_B, \n3.尺码与吊牌价必须为纯数字, 谢谢!", u'错误', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class ImportPassedMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self, Num1, Num2):
   		dlg = wx.MessageDialog(None, u"成功导入 %d 款商品, 新增库存 %d 件"%(Num1,Num2), u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class ExportMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导出成功!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class ExportErrorMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self,filename):
   		dlg = wx.MessageDialog(None, u"导出失败,请检查欲导出文件:%s\n是否已经打开,请先关闭该文件,再导出,谢谢!"%filename, u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class PurchaseMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"入库成功!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class UpdateMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"数据修改成功!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class ModifyMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"更新数据成功!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class SellMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"出库成功!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class PurchaseConfirmBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		wx.MessageDialog(None, u"确定要入库吗?", u'提示', wx.OK|wx.CANCEL);

class SellConfirmBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		wx.MessageDialog(None, u"确定要出库吗?", u'提示', wx.OK|wx.CANCEL);


class ModifyConfirmBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		wx.MessageDialog(None, u"确定要更新并修改数据吗?", u'提示', wx.YES_NO);

class InputDataMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"请输入需要查询的信息项! 比如输入\"白色\",\"万达\",\"_B\"等", u'错误', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class AccountDataErrorMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"输入有误,权限必须为“管理员（店长）”或“导购员”。", u'错误', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class AccountIsAdminAlreadyMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"该账户已经是管理员（店长）权限", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class AccountIsGuideAlreadyMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"该账户已经是导购员权限", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class AccountSetAdminMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"设置管理员（店长）权限成功", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();


class AccountSetGuideMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"设置导购员权限成功", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class NoThisDataMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"输入有误, 数据库中无此商品编号!", u'错误', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class InputEmptyValueMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"请输入商品编号!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class NoStoreMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"该尺码已无库存了, 请重新输入尺码!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class DeleteEmptyMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"该商品编号商品已经全部卖完, 已从库存信息中删除, 请知晓!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class DeleteAccountMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"该账户已经删除", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class DeleteGoodsMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self, SelectedID):
   		dlg = wx.MessageDialog(None, u"商品%s已被删除, 请知晓!"%SelectedID, u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class PasswordTooShortMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"密码小于4位数, 或者密码大于16位数, 请重新设置一个大于4位数小于16位数的密码.", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class EmptyValuesFoundMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"账户名,密码,权限等均不能为空,且用户名不能为admin", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class PasswordDidNotEqualMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"两处密码不相同, 请检查输入!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();


class SaveAccountMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"账户保存成功!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class WrongPasswordMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"输入密码有误!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class WrongUsernameMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"数据库中找不到该用户名!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();


class InputUsernameMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"请输入用户名!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class InputPasswordMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"请输入密码!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class CountFormatErrorMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"折扣项输入有误,请输入两位数字!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class PriceNotGetMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"获取的价格为空,请检查价格!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class VendorErrorMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"售出人输入有误,请选择一位用户下拉列表中的售出人!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class SizeInputErrorMessageBox(wx.MessageDialog):
	'''
	This is a MessageBox;
	'''
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"输入的尺码有误,请选择一个尺码下拉列表中的尺码!", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();
# DeleteEmptyMessageBox();
class XXLColMessageBox(wx.MessageDialog):
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导入失败,检测到导入文档中的\"XXL\"列有错误,请确保该列数据全是纯数字", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class XLColMessageBox(wx.MessageDialog):
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导入失败,检测到导入文档中的\"XL\"列有错误,请确保该列数据全是纯数字", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class LColMessageBox(wx.MessageDialog):
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导入失败,检测到导入文档中的\"L\"列有错误,请确保该列数据全是纯数字", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class MColMessageBox(wx.MessageDialog):
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导入失败,检测到导入文档中的\"M\"列有错误,请确保该列数据全是纯数字", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();
   		
class SColMessageBox(wx.MessageDialog):
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导入失败,检测到导入文档中的\"S\"列有错误,请确保该列数据全是纯数字", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class GIDMessageBox(wx.MessageDialog):
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导入失败,检测到导入文档中的\"商品编号\"列有空值,请确保商品编号不为空", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class GIDFormatMessageBox(wx.MessageDialog):
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导入失败,检测到导入文档中的\"商品编号\"列有异常字符,请确保商品编号只包含数字,字母,及下划线_", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class GPriceMessageBox(wx.MessageDialog):
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导入失败,检测到导入文档中的\"标准吊牌价\"列有空值,请确保标准吊牌价不为空", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class GPriceFormatMessageBox(wx.MessageDialog):
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导入失败,检测到导入文档中的\"标准吊牌价\"列有异常字符,请确保标准吊牌价只包含纯数字", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class GNameMessageBox(wx.MessageDialog):
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导入失败,导入文档中未检测到以\"商品类别\"开头的列名", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class GColorMessageBox(wx.MessageDialog):
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导入失败,导入文档中未检测到以\"颜色\"开头的列名", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class SizeItemNotFoundMessageBox(wx.MessageDialog):
	def __init__(self, size):
   		dlg = wx.MessageDialog(None, u"导入失败,导入文档中未检测到以\"%s\"开头的列名"%size, u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();


class GStoreNumMessageBox(wx.MessageDialog):
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导入失败,导入文档中未检测到以\"库存数\"开头的列名", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class GCommentsMessageBox(wx.MessageDialog):
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导入失败,导入文档中未检测到以\"备注\"开头的列名", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class GStoreTimeMessageBox(wx.MessageDialog):
	def __init__(self):
   		dlg = wx.MessageDialog(None, u"导入失败,导入文档中未检测到以\"入库时间\"开头的列名", u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class SizeColumnFormatMessageBox(wx.MessageDialog):
	def __init__(self, size):
   		dlg = wx.MessageDialog(None, u"导入失败,导入文档中检测到\"%s\"列有异常字符,请确保该列数据全是纯数字"%size, u'提示', wx.OK);
   		dlg.ShowModal();
   		dlg.Destroy();

class ReminderMessageBox(wx.MessageDialog):
	def __init__(self, messages):
		messages=messages.encode('gb2312');
   		dlg = wx.MessageDialog(None, messages, u'提示', wx.OK); 
   		dlg.ShowModal();
   		dlg.Destroy();

class ErrorMessageBox(wx.MessageDialog):
	def __init__(self, messages):
		messages=messages.encode('gb2312');
   		dlg = wx.MessageDialog(None, messages, u'错误', wx.OK); 
   		dlg.ShowModal();
   		dlg.Destroy();