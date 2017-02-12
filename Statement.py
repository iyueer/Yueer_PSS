# coding: UTF-8
#Author:张祖兴 iyueer@163.com

import wx;
import shelve,dbhash,anydbm;
import SearchGoods;
from os.path import splitext,exists
from sys import maxint
from time import strftime,localtime;
from datetime import date,timedelta;
from re import sub;
from os import getcwd;
import wx.lib.calendar;
from xlwt import Workbook;


class StatementPage(wx.Dialog):
    """
    This is StatementPage.  
    """
    def __init__(self):
        wx.Dialog.__init__(self,None,-1, u"销售报表",size=(800, 660))
        self.ScreenSize=wx.DisplaySize(); ##Get the ScreenSize(Resloution)
        self.Centre();
        panel = wx.Panel(self);

        # self.CreateStatusBar()
        self.icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon);
        DefaultDateTime=wx.DateTime.Today();
        DateFilter_Type=[u"日报",u"周报", u"月报", u"半年报", u"一年报", u"三年报", u"自定义"];
        self.DateFilter_Label = wx.StaticText(panel, -1, u"  时段过滤",style=wx.ALIGN_BOTTOM);
        self.DateFilter_Combox = wx.ComboBox(panel, 204, u"日报",(15,30),wx.DefaultSize,DateFilter_Type,wx.CB_DROPDOWN|wx.CB_READONLY);
        # A text widget to display the doc and let it be edited
        self.DateFrom_Label = wx.StaticText(panel, -1, u"自定义日期从",style=wx.ALIGN_BOTTOM);
        self.DateFrom_Text = wx.TextCtrl(panel,201, "%s"%strftime("%Y-%m-%d", localtime()),style=wx.TE_RICH2|wx.TE_PROCESS_ENTER|wx.TE_LEFT);
        self.DateEnd_Label = wx.StaticText(panel, -1, u"至",style=wx.ALIGN_BOTTOM);
        self.DateEnd_Text=wx.TextCtrl(panel,202,"%s"%strftime("%Y-%m-%d", localtime()),style=wx.TE_RICH2|wx.TE_PROCESS_ENTER|wx.TE_LEFT);
        self.QueryButton = wx.Button(panel, 211, u"开始汇总");
        self.ExportButton = wx.Button(panel, 203, u"销售统计\日志导出Excel");
        self.SellLog_Label = wx.StaticText(panel, -1, u"销售日志",style=wx.ALIGN_BOTTOM);
        self.SellReport_Label = wx.StaticText(panel, -1, u"销量统计(前30)",style=wx.ALIGN_BOTTOM);
        self.SellLog = wx.ListCtrl(panel, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_SINGLE_SEL|wx.LC_SORT_DESCENDING, size=(700,700))
        self.SellReport = wx.ListCtrl(panel, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_SINGLE_SEL|wx.LC_SORT_ASCENDING, size=(210,400))
        Report_columns = ['\xc9\xcc\xc6\xb7\xc0\xe0\xb1\xf0','\xcf\xfa\xc1\xbf','\xcf\xfa\xca\xdb\xb6\xee']
        Log_columns = ['\xcf\xfa\xca\xdb\xca\xb1\xbc\xe4','\xc9\xcc\xc6\xb7\xb1\xe0\xba\xc5','\xc9\xcc\xc6\xb7\xc0\xe0\xb1\xf0',\
        '\xd1\xd5\xc9\xab','\xb3\xdf\xc2\xeb','\xbc\xdb\xb8\xf1','\xd5\xdb\xbf\xdb','\xca\xdb\xbc\xdb','\xb5\xbc\xb9\xba\xd4\xb1']
        Star_columns = ['\xb5\xbc\xb9\xba\xd4\xb1','\xcf\xfa\xc1\xbf','\xcf\xfa\xca\xdb\xb6\xee'];
        self.SellStar_Label = wx.StaticText(panel, -1, u"销售之星(前10)",style=wx.ALIGN_BOTTOM)
        self.SellStar = wx.ListCtrl(panel, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_SINGLE_SEL, size=(210,220))
        for col, text in enumerate(Report_columns):
            self.SellReport.InsertColumn(col, text, wx.LIST_FORMAT_CENTRE);
        self.SellReport.SetColumnWidth(0, 80);
        self.SellReport.SetColumnWidth(1, 50)
        self.SellReport.SetColumnWidth(2, 80)
        for col2, text2 in enumerate(Log_columns):
            self.SellLog.InsertColumn(col2, text2, wx.LIST_FORMAT_CENTRE);
        self.SellLog.SetColumnWidth(0,70);
        self.SellLog.SetColumnWidth(1,70);
        self.SellLog.SetColumnWidth(2,70);
        self.SellLog.SetColumnWidth(3,75);
        self.SellLog.SetColumnWidth(4,45);
        self.SellLog.SetColumnWidth(5,45);
        self.SellLog.SetColumnWidth(6,50);
        self.SellLog.SetColumnWidth(7,50);
        self.SellLog.SetColumnWidth(8,65);
        for col, text in enumerate(Star_columns):
            self.SellStar.InsertColumn(col, text, wx.LIST_FORMAT_CENTRE);
        self.SellStar.SetColumnWidth(0, 80);
        self.SellStar.SetColumnWidth(1, 50)
        self.SellStar.SetColumnWidth(2, 80)

        now = date.today();
        EndTimer = now+timedelta(days=1);
        StartTimer=now;
        EndTimer=int(DateTimeFormat(EndTimer));
        StartTimer=int(DateTimeFormat(StartTimer));
        self.SellGoodsQueryAll_NoEvt(EndTimer,StartTimer);
        self.SellStarQueryAll_NoEvt(EndTimer,StartTimer);
        self.SellLogQueryAll_NoEvt(EndTimer,StartTimer);
        # self.GotDateComboxSelected();

        RowSizer1 = wx.BoxSizer(wx.HORIZONTAL);
        fgs = wx.FlexGridSizer(1,8,10,10)

        fgs.AddMany([(self.DateFilter_Label,1,wx.LEFT),(self.DateFilter_Combox,1,wx.EXPAND),(self.DateFrom_Label,1,wx.EXPAND),\
            (self.DateFrom_Text,1,wx.EXPAND),(self.DateEnd_Label,1,wx.EXPAND),(self.DateEnd_Text,1,wx.EXPAND),\
            (self.QueryButton,1,wx.EXPAND),(self.ExportButton,1,wx.RIGHT)]);
        RowSizer1.Add(fgs, flag=wx.EXPAND, border=5);

        ColSizer1 = wx.BoxSizer(wx.VERTICAL);
        ColSizer1.Add(self.SellReport_Label, flag=wx.LEFT, border=10)
        ColSizer1.Add(self.SellReport, flag=wx.LEFT, border=10)
        ColSizer1.Add(self.SellStar_Label, flag=wx.LEFT, border=10)
        ColSizer1.Add(self.SellStar, flag=wx.LEFT, border=10)
        
        ColSizer2 = wx.BoxSizer(wx.VERTICAL);
        ColSizer2.Add(self.SellLog_Label, flag=wx.LEFT, border=10)
        ColSizer2.Add(self.SellLog, flag=wx.RIGHT, border=10)


        RowSizer2 = wx.BoxSizer(wx.HORIZONTAL);
        RowSizer2.Add(ColSizer1, flag=wx.LEFT, border=0);
        RowSizer2.Add(ColSizer2, flag=wx.RIGHT, border=0);

        ColSizer = wx.BoxSizer(wx.VERTICAL);
        ColSizer.Add(RowSizer1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP|wx.ALL, border=7);
        ColSizer.Add(RowSizer2,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP|wx.ALL, border=7);
        
        self.DateFrom_Text.Bind(wx.EVT_LEFT_DOWN,self.GotDateFrom);
        self.Bind(wx.EVT_COMBOBOX, self.GotDateComboxSelected, id=204);
        self.Bind(wx.EVT_BUTTON, self.GotDateTextCtrlSelected, id=211);
        self.Bind(wx.EVT_BUTTON, self.ExportSellLogToExcelFile,id=203);
        self.DateEnd_Text.Bind(wx.EVT_LEFT_DOWN, self.GotDateEnd);

        panel.SetSizer(ColSizer);
        panel.Layout();

    def ExportSellLogToExcelFile(self,evt):
        wildcard2 = "Excel 2003 File (*.xls)|*.xls"
        dlg = wx.FileDialog(self, u"另存为Excel文件...", getcwd(), 
            "", wildcard2, wx.SAVE|wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            filename=u"%s"%dlg.GetPath()
            if not splitext(filename)[1]:
                filename = filename + '.xls'
            self.filename = filename
            findname='''%s'''%filename

            # try:
            self.SellLogExportToExcel(filename)
            dlg.Destroy()
            SearchGoods.ExportMessageBox()
            # except:
            #     dlg.Destroy()
            #     SearchGoods.ExportErrorMessageBox(filename)                
        else:
            pass

    def SellLogExportToExcel(self, Excelfile):
        getattr(self,"DateFilter_Combox").SetStringSelection(u"自定义");
        StartTimer = getattr(self, "DateFrom_Text").GetValue();
        StartTimer_Short=StartTimer;
        StartTimer=int(DateTimeFormat(StartTimer)); 
        EndTimer = getattr(self, "DateEnd_Text").GetValue();
        EndTimer_Short=EndTimer;
        EndTimer=int(DateTimeFormat(EndTimer));
        EndTimer=str(EndTimer); ###实现当天延长.
        EndTimer=sub(r"000000", "235900",EndTimer);
        EndTimer=int(EndTimer);

        dbreader=shelve.open('statement.dat','r');
        book=Workbook(encoding="utf-8", style_compression=0)
        ######写第一个sheet.
        sheet=book.add_sheet(u'销售日志', cell_overwrite_ok=True)
        #写第一行：
        FirstRow=['\xcf\xfa\xca\xdb\xca\xb1\xbc\xe4','\xc9\xcc\xc6\xb7\xb1\xe0\xba\xc5','\xc9\xcc\xc6\xb7\xc0\xe0\xb1\xf0',\
            '\xd1\xd5\xc9\xab','\xb3\xdf\xc2\xeb','\xbc\xdb\xb8\xf1','\xd5\xdb\xbf\xdb','\xca\xdb\xbc\xdb','\xb5\xbc\xb9\xba\xd4\xb1'];
        for m in range(0,len(FirstRow)):
            sheet.write(0, m, "%s"%FirstRow[m].decode('gb2312'));
        
        if(EndTimer<StartTimer):
            sheet.write(1,0,u"开始日期应该小于结束日期,所以此销售日志报表未获取任何数据, 请在销售报表窗口重新设置开始日期与结束日期!")
        else:
            bigdata=[];
            bigdata=self.SellLogReturn_AllData(EndTimer,StartTimer)
            bigdata.sort(reverse=True);
            # print len(bigdata);
            for n in range(0, len(bigdata)):
                for h in range(0, 9):
                    try:
                        sheet.write((n+1), h, int(bigdata[n][h]));
                    except:
                        sheet.write((n+1), h, bigdata[n][h].decode('gb2312'));
    
        #写第二个sheet.
        sheet2=book.add_sheet(u'销量统计', cell_overwrite_ok=True)
        # print StartTimer;
        # print EndTimer;
        if(EndTimer<StartTimer):
            sheet2.write(0,0,u"开始日期应该小于结束日期,所以此销售统计报表未获取任何数据, 请在销售报表窗口重新设置开始日期与结束日期!")
        else:
            #写第一行:
            sheet2.write(0,0,u"统计开始时间:")
            sheet2.write(0,1,StartTimer_Short)
            sheet2.write(1,0,u"统计结束时间:")
            sheet2.write(1,1,EndTimer_Short)
            #写第三行：
            FirstRow2=['\xd0\xf2\xba\xc5','\xc9\xcc\xc6\xb7\xc0\xe0\xb1\xf0','\xcf\xfa\xc1\xbf', '\xcf\xfa\xca\xdb\xb6\xee'];
            for m in range(0,len(FirstRow2)):
                sheet2.write(2, m, "%s"%FirstRow2[m].decode('gb2312'));
            bigdata2=self.GetGoodsStatementRows_List(EndTimer, StartTimer);
            for x in range(0, len(bigdata2)):
                sheet2.write((x+3), 0, x);
            for t in range(0, len(bigdata2)):
                for p in range(0, 3):
                    try:
                        sheet2.write((t+3), p+1, int(bigdata2[t][p]));
                    except:
                        sheet2.write((t+3), p+1, bigdata2[t][p].decode('gb2312'));
        book.save("%s"%Excelfile);
        dbreader.close();

    def GotDateComboxSelected(self, event):
        now = date.today();
        FilterSelected = (getattr(self,"DateFilter_Combox").GetStringSelection()).encode('gb2312');
        if(FilterSelected=="\xc8\xfd\xc4\xea\xb1\xa8"):  #几年报
            StartTimer=now-timedelta(days = 1096);
        elif(FilterSelected=="\xd2\xbb\xc4\xea\xb1\xa8"):#一年报
            StartTimer=now-timedelta(days = 365);
        elif(FilterSelected=="\xb0\xeb\xc4\xea\xb1\xa8"):#半年报
            StartTimer=now-timedelta(days = 183);
        elif(FilterSelected=="\xd4\xc2\xb1\xa8"):#月报
            StartTimer=now-timedelta(days = 30);
        elif(FilterSelected=="\xd6\xdc\xb1\xa8"):#周报
            StartTimer=now-timedelta(days = 7);
        elif(FilterSelected=="\xbd\xf1\xc8\xd5"):#日报
            StartTimer=now;
        else:
            StartTimer=now;
        getattr(self,"DateFrom_Text").SetValue("%s"%StartTimer);
        getattr(self,"DateEnd_Text").SetValue("%s"%now);
        StartTimer=int(DateTimeFormat(StartTimer));
        EndTimer=str(DateTimeFormat(StartTimer));
        EndTimer=sub(r"000000", "235900",EndTimer);###实现当天延长.
        EndTimer=int(EndTimer);
        self.SellReport.DeleteAllItems();
        self.SellLog.DeleteAllItems();
        self.SellStar.DeleteAllItems();
        self.SellStarQueryAll_NoEvt(EndTimer,StartTimer);
        self.SellGoodsQueryAll_NoEvt(EndTimer,StartTimer);
        self.SellLogQueryAll_NoEvt(EndTimer,StartTimer);

    def GotDateTextCtrlSelected(self, event):
        getattr(self,"DateFilter_Combox").SetStringSelection(u"自定义");
        StartTimer = getattr(self, "DateFrom_Text").GetValue();
        StartTimer=int(DateTimeFormat(StartTimer)); 
        EndTimer = getattr(self, "DateEnd_Text").GetValue();
        EndTimer=int(DateTimeFormat(EndTimer));
        EndTimer=str(EndTimer); ###实现当天延长.
        EndTimer=sub(r"000000", "235900",EndTimer);
        EndTimer=int(EndTimer);
        if(EndTimer<StartTimer):
            SearchGoods.ReminderMessageBox(u"查询出错,开始日期应该小于结束日期,\n请重新设定查询的开始日期和结束日期!");
        else:
            self.SellReport.DeleteAllItems();
            self.SellLog.DeleteAllItems();
            self.SellStar.DeleteAllItems();
            self.SellStarQueryAll_NoEvt(EndTimer,StartTimer);
            self.SellGoodsQueryAll_NoEvt(EndTimer,StartTimer);
            self.SellLogQueryAll_NoEvt(EndTimer,StartTimer);

    def GotDateFrom(self, event):       # test the date dialog
        PosWidth=self.ScreenSize[0]*0.366;
        PosHigh=self.ScreenSize[1]*0.124;
        dlg = CalendarFrame(None,PosWidth,PosHigh);
        dlg.ShowModal();
        getattr(self,"DateFrom_Text").SetValue("%s"%dlg. GotDateSelected())
        dlg.Destroy;

    def GotDateEnd(self, event):       # test the date dialog
        PosWidth=self.ScreenSize[0]*0.465;
        PosHigh=self.ScreenSize[1]*0.124;
        dlg = CalendarFrame(None,PosWidth,PosHigh);
        dlg.ShowModal();
        getattr(self,"DateEnd_Text").SetValue("%s"%dlg. GotDateSelected());
        dlg.Destroy;   

    def GetStatementValues_To_tuple(self,values,db,EndTimer,StartTimer):
        #"ID":ID, "Size":size, "Name": name,"Vendor":vendor, "Price":price, "Count":count,"Finalprice"
        for item in db.items():
            if(int(item[0])>=StartTimer and int(item[0])<=EndTimer):
                tupledata=(item[1]["ShortTime"], item[1]["ID"],item[1]["Name"],\
                    item[1]["Color"],item[1]["Size"],item[1]["Price"],item[1]["Count"],item[1]["Finalprice"],item[1]["Vendor"]);
                values.append(tupledata);
        return values;

    def GetStarStatementRows_Tuple(self,EndTimer,StartTimer):
        AllRows=[];
        SaleAmounts_List=[];
        NewSaleAmounts_List=[];
        for j in SearchGoods.ListBox_Display():
            SaleAmounts_List.append([int(self.StarSaleAmount(j,EndTimer,StartTimer)),self.StarSaleVolumn(j,EndTimer,StartTimer),j]);
        SaleAmounts_List.sort(reverse=True);##按销量排序.
        if(len(SearchGoods.ListBox_Display())>=10):
            for i in range(0,10):
                AllRows.append(self.List_PositionAdjust(SaleAmounts_List[i]));
            return AllRows;
        else:
            for i in range(0,len(SearchGoods.ListBox_Display())):
                AllRows.append(self.List_PositionAdjust(SaleAmounts_List[i]));
            return AllRows;


    def StarSaleAmount(self, vendor,EndTimer,StartTimer):
        ''''销量'''
        OneVendorSaleAmount=0;
        dbreader=shelve.open('statement.dat','r');
        for i in dbreader.items():
            if(int(i[0])>=StartTimer and int(i[0])<=EndTimer):
                if(i[1]["Vendor"]==vendor):
                    OneVendorSaleAmount=OneVendorSaleAmount+1;
        dbreader.close();
        return OneVendorSaleAmount;
    
    def StarSaleVolumn(self, vendor,EndTimer,StartTimer):
        '''销售总额'''
        OneVendorSaleVolumn=0;
        dbreader=shelve.open('statement.dat','r');
        for i in dbreader.items():
            if(int(i[0])>=StartTimer and int(i[0])<=EndTimer):
                if(i[1]["Vendor"]==vendor):
                    OneVendorSaleVolumn=int(i[1]["Finalprice"])+OneVendorSaleVolumn;
        dbreader.close();
        return OneVendorSaleVolumn;
    
    def GoodsNameType(self, EndTimer,StartTimer):
        GoodsNameType_List=[];
        dbreader=shelve.open('statement.dat','r');
        for i in dbreader.items():
            if(int(i[0])>=StartTimer and int(i[0])<=EndTimer):
                if(i[1]["Name"]!=""):
                    GoodsNameType_List.append(i[1]["Name"]);
    
        GoodsNameType_List=sorted(set(GoodsNameType_List));
        dbreader.close();
        return GoodsNameType_List;
    
    def GetGoodsStatementRows_Tuple(self, EndTimer,StartTimer):
        AllRows=[];
        k=0
        SaleAmounts_List=[];
        NewSaleAmounts_List=[];
        Total_Tuple=tuple(["\xd7\xdc\xbc\xc6",str(self.AllGoodsSaleAmount(EndTimer,StartTimer)),str(self.AllGoodsSaleVolumn(EndTimer,StartTimer))]);
        for j in self.GoodsNameType(EndTimer,StartTimer):
            SaleAmounts_List.append([int(self.GoodsSaleAmount(j, EndTimer,StartTimer)),self.GoodsSaleVolumn(j, EndTimer,StartTimer),j]);
        SaleAmounts_List.sort(reverse=True);##按销量排序.

        #加[序号]空格
        for m in SaleAmounts_List:
            k=k+1
            if(k<10):
                m[2]="[0%s] "%k+str(m[2]);
            else:
                m[2]="[%s] "%k+str(m[2]);
    
        if(len(self.GoodsNameType(EndTimer,StartTimer))>=20):
            for i in range(0,20):
                AllRows.append(self.List_PositionAdjust(SaleAmounts_List[i]));
            # AllRows.append(("","",""));
            AllRows.append(Total_Tuple);
            return AllRows;
        else:
            for i in range(0,len(self.GoodsNameType(EndTimer,StartTimer))):
                AllRows.append(self.List_PositionAdjust(SaleAmounts_List[i]));
            AllRows.append(Total_Tuple);
            return AllRows;

    def GetGoodsStatementRows_List(self, EndTimer,StartTimer):
        AllRows=[];
        k=0
        SaleAmounts_List=[];
        NewSaleAmounts_List=[];
        Total_List=list(["\xd7\xdc\xbc\xc6",str(self.AllGoodsSaleAmount(EndTimer,StartTimer)),str(self.AllGoodsSaleVolumn(EndTimer,StartTimer))]);
        for j in self.GoodsNameType(EndTimer,StartTimer):
            SaleAmounts_List.append([int(self.GoodsSaleAmount(j, EndTimer,StartTimer)),self.GoodsSaleVolumn(j, EndTimer,StartTimer),j]);
        SaleAmounts_List.sort(reverse=True);##按销量排序.

        for i in range(0,len(self.GoodsNameType(EndTimer,StartTimer))):
            AllRows.append(self.List_PositionAdjust(SaleAmounts_List[i]));
        AllRows.append(Total_List);
        # print AllRows;
        return AllRows;

    def List_PositionAdjust(self, ListName):
        temp1="";
        temp2="";
        temp1=str(ListName[0]);
        temp2=str(ListName[1]);
        ListName[0]=str(ListName[2]);
        ListName[1]=temp1;
        ListName[2]=temp2;
        return tuple(ListName);
    
    
    def GoodsSaleAmount(self, Nametype,EndTimer,StartTimer):
        ''''某个产品销量'''
        OneGoodsSaleAmount=0;
        dbreader=shelve.open('statement.dat','r');
        for i in dbreader.items():
            if(int(i[0])>=StartTimer and int(i[0])<=EndTimer):
                if(i[1]["Name"]==Nametype):
                    OneGoodsSaleAmount=OneGoodsSaleAmount+1;
        dbreader.close();
        return OneGoodsSaleAmount;

    def AllGoodsSaleAmount(self,EndTimer,StartTimer):
        ''''总计销量'''
        AllGoodsSaleAmount=0;
        dbreader=shelve.open('statement.dat','r');
        for i in dbreader.items():
            if(int(i[0])>=StartTimer and int(i[0])<=EndTimer):
                AllGoodsSaleAmount=AllGoodsSaleAmount+1;
        dbreader.close();
        return AllGoodsSaleAmount;


    def GoodsSaleVolumn(self, Nametype, EndTimer,StartTimer):    
        '''某件产品销售总额'''
        OneGoodsSaleVolumn=0;
        dbreader=shelve.open('statement.dat','r');
        for i in dbreader.items():
            if(int(i[0])>=StartTimer and int(i[0])<=EndTimer):
                if(i[1]["Name"]==Nametype):
                    OneGoodsSaleVolumn=int(i[1]["Finalprice"])+OneGoodsSaleVolumn;
        dbreader.close();
        return OneGoodsSaleVolumn;

    def AllGoodsSaleVolumn(self,EndTimer,StartTimer):    
        '''总计销售总额'''
        AllGoodsSaleVolumn=0;
        dbreader=shelve.open('statement.dat','r');
        for i in dbreader.items():
            if(int(i[0])>=StartTimer and int(i[0])<=EndTimer):
                    AllGoodsSaleVolumn=int(i[1]["Finalprice"])+AllGoodsSaleVolumn;
        dbreader.close();
        return AllGoodsSaleVolumn;
    
    
    def GotDateFromDlg(self, event):       # test the date dialog
        dlg = wx.calendar.CalenDlg(self)
        dlg.Centre()

        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.result
            day = result[1]
            month = result[2]
            year = result[3]
            new_date = str(month) + '/'+ str(day) + '/'+ str(year)
            self.log.WriteText('Date Selected: %s\n' % new_date)
        else:
            pass;

    def SellLogListDisplay(self, rows):
        self.SellLog.DeleteAllItems()
        self.itemDataMap = {}
        for item in rows:
            index = self.SellLog.InsertStringItem(maxint, item[0])
            for col, text in enumerate(item[1:]):
                self.SellLog.SetStringItem(index, col+1, text)
            self.SellLog.SetItemData(index, index)
            self.itemDataMap[index] = item;

    def SellLogQueryAll_NoEvt(self, EndTimer,StartTimer):
        self.SellLogListDisplay(self.SellLogReturn_AllData(EndTimer,StartTimer))

    def SellLogReturn_AllData(self,EndTimer,StartTimer):
        Allvalues=[]
        dbreader=shelve.open('Statement.dat','r')
        rows=self.GetStatementValues_To_tuple(Allvalues,dbreader,EndTimer,StartTimer)
        dbreader.close();
        return rows;


    def SellStarListDisplay(self, rows):
        self.SellStar.DeleteAllItems()
        self.itemDataMap = {}
        for item in rows:
            index = self.SellStar.InsertStringItem(maxint, item[0])
            for col, text in enumerate(item[1:]):
                self.SellStar.SetStringItem(index, col+1, text)
            self.SellStar.SetItemData(index, index)
            self.itemDataMap[index] = item

    def SellGoodsListDisplay(self, rows):
        self.SellReport.DeleteAllItems()
        self.itemDataMap = {}
        for item in rows:
            index = self.SellReport.InsertStringItem(maxint, item[0]);
            # print index;
            for col, text in enumerate(item[1:]):
                self.SellReport.SetStringItem(index, col+1, text)
            self.SellReport.SetItemData(index, index)
            self.itemDataMap[index] = item;

    def SellStarQueryAll_NoEvt(self,EndTimer,StartTimer):
        self.SellStarListDisplay(self.GetStarStatementRows_Tuple(EndTimer,StartTimer));

    def SellGoodsQueryAll_NoEvt(self,EndTimer,StartTimer):
        self.SellGoodsListDisplay(self.GetGoodsStatementRows_Tuple(EndTimer,StartTimer));

class CalendarFrame(wx.Dialog):#排序用
    """
    #零边框的Calendar
    """
    def __init__(self, parent, x, y):
        # self.text="";
        self.holidays = {1: [1],2: [13],3: [22],4: [3],5: [29],6: [15],7: [4, 11],8: [],9: [3],10: [],11: [27, 26],12: [24, 25]}
        wx.Dialog.__init__(self, parent, -1, pos=(x, y),size=(191, 205),style=wx.FRAME_TOOL_WINDOW)
        self.cal = wx.lib.calendar.Calendar(self, -1, pos=(0, 30), size=(190, 172))
        start_month = self.cal.GetMonth()
        start_year = self.cal.GetYear()
        self.SetBackgroundColour("white")
        self.cal.SetWeekColor('white', 'pink')
        self.cal.SetColor(wx.lib.calendar.COLOR_WEEKEND_BACKGROUND, 'white')
        self.cal.ShowWeekEnd()
        self.set_days = self.holidays[start_month]
        self.cal.AddSelect(self.set_days, 'black', 'white')
        self.cal.Refresh()
        self.cal.HideTitle();
        self.Bind(wx.lib.calendar.EVT_CALENDAR, self.OnCalSelected)
        self.texty = wx.TextCtrl(self, -1, str(start_year), pos=(2, 3), size=(40, -1))
        h = self.texty.GetSize().height
        self.spiny = wx.SpinButton(self, -1, pos=(42, 3), size=(h*2, h))
        self.spiny.SetRange(1970, 3000)
        self.spiny.SetValue(start_year)
        self.Bind(wx.EVT_SPIN, self.OnSpiny, self.spiny)
        self.textm = wx.TextCtrl(self, -1, str(start_month), pos=(109, 3), size=(30, -1))
        h = self.textm.GetSize().height
        self.spinm = wx.SpinButton(self, -1, pos=(139, 3), size=(h*2, h))
        self.spinm.SetRange(1, 12)
        self.spinm.SetValue(start_month)
        self.Bind(wx.EVT_SPIN, self.OnSpinm, self.spinm)

    def OnCalSelected(self, evt):
        self.Destroy();
        if(len(str(evt.month))==1):
            evt.month=str("0"+str(evt.month));
        if(len(str(evt.day))==1):
            evt.day=str("0"+str(evt.day));
        self.text = "%s-%s-%s" % (evt.year,evt.month,evt.day);

    def GotDateSelected(self):
        return self.text;

    def OnSpiny(self, event):
        year = event.GetPosition()
        self.texty.SetValue(str(year))
        self.cal.SetYear(year)
        self.ResetDisplay()
    
    def OnSpinm(self, event):
        month = event.GetPosition()
        self.textm.SetValue(str(month))
        self.cal.SetMonth(month)
        self.ResetDisplay()
    
    def ResetDisplay(self):
        # reset holiday colour
        self.cal.AddSelect(self.set_days, 'black', 'white')
        # get number of the month
        month = self.cal.GetMonth()
        set_days = self.holidays[month]
        # set new holiday colour
        self.cal.AddSelect(set_days, 'black', 'white')
        self.cal.Refresh()
        # keep present list to reset colour
        self.set_days = set_days



def CurrentYear():
    now = str(date.today());
    return now[:4];

def CurrentMonth():
    now = str(date.today());
    return now[5:7];

def DateTimeFormat(datetimer):
    datetimer=str(datetimer);
    datetimer=sub(r'-','',datetimer);
    if(len(datetimer)):
        datetimer=datetimer+"0000000"
    return datetimer;

if __name__ == '__main__':
    app = wx.App();
    frame = StatementPage();
    frame.Show();
    app.MainLoop();