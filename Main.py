# coding: UTF-8
#Author:张祖兴 iyueer@163.com

import wx
from sys import maxint
from re import match, sub
from os import getcwd,mkdir,remove,listdir,_exit
from os.path import splitext,exists
from time import strftime,localtime
import shelve,dbhash,anydbm
import Purchase, Account, Statement, Printer;
import Sell
import Modify
import Update
import QuerySell
import SearchGoods
import About
import wx.lib.mixins.listctrl
import Yueer_PSS


class MyFrame(wx.Frame, wx.lib.mixins.listctrl.ColumnSorterMixin):#排序用
    """
    This is Main MyFrame.
    """
    def __init__(self, parent, title, Righttype):
        wx.Frame.__init__(self, parent, -1, title, size=(900, 735))
        self.Centre()
        self.icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.statusbar = self.CreateStatusBar()
        #将状态栏分割为3个区域,比例为1:2
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-2,-2,-4])

        self.statusbar.SetStatusText(u"商品总数: %d 款"%self.Return_TotalGoods(), 0)
        self.statusbar.SetStatusText(u"库存总数: %d 件"%self.Return_TotalStore(), 1)
        self.statusbar.SetStatusText("", 2)


        self.panel = wx.Panel(self)
        self.GoodsInfo_Text = wx.TextCtrl(self.panel,7, size=(37,37),style=wx.TE_RICH2|wx.TE_PROCESS_ENTER|wx.TE_LEFT)
        self.GoodsInfo_Label = wx.StaticText(self.panel, -1, u"     \n信息查询:\n",style=wx.ALIGN_BOTTOM)
        self.GoodsInfo_Label.SetFont(wx.Font(12,wx.DEFAULT,wx.NORMAL,wx.NORMAL))

        columns = ['\xc9\xcc\xc6\xb7\xb1\xe0\xba\xc5','\xc9\xcc\xc6\xb7\xc0\xe0\xb1\xf0', \
        '\xd1\xd5\xc9\xab', "S", "M","L","XL","XXL", "\xbf\xe2\xb4\xe6\xca\xfd",\
        "\xb1\xea\xd7\xbc\xb5\xf5\xc5\xc6\xbc\xdb","\xb1\xb8\xd7\xa2","\xc8\xeb\xbf\xe2\xca\xb1\xbc\xe4"]
        self.SearchList_Report = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_SINGLE_SEL, size=(510,750))

        for col, text in enumerate(columns):
            self.SearchList_Report.InsertColumn(col, text, wx.LIST_FORMAT_CENTRE)

        self.SearchList_Report.SetColumnWidth(0, 90)
        self.SearchList_Report.SetColumnWidth(1, 95)
        self.SearchList_Report.SetColumnWidth(2, 85)
        self.SearchList_Report.SetColumnWidth(3, 55)
        self.SearchList_Report.SetColumnWidth(4, 55)
        self.SearchList_Report.SetColumnWidth(5, 55)
        self.SearchList_Report.SetColumnWidth(6, 55)
        self.SearchList_Report.SetColumnWidth(7, 55)
        self.SearchList_Report.SetColumnWidth(8, 55)
        self.SearchList_Report.SetColumnWidth(9, 90)
        self.SearchList_Report.SetColumnWidth(10, 90)
 
        wx.lib.mixins.listctrl.ColumnSorterMixin.__init__(self,len(columns))##排序用
        self.QueryAll_NoEvt()
        
        self.SearchBMP = wx.Image("search.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.SearchAllBMP = wx.Image("searchall.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.SellBMP = wx.Image("out.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.GoodsSearch_Button=wx.BitmapButton(self.panel, 17, self.SearchBMP)
        self.GoodsSearchAll_Button=wx.BitmapButton(self.panel,18,self.SearchAllBMP)
        self.GoodsQuerySell_Button=wx.BitmapButton(self.panel,8,self.SellBMP)

        if(Righttype=="111"):
            self.__init__111()
        elif(Righttype=="222"):
            self.__init__222()
        else:
            pass

        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.menu1, u"文件")
        self.menuBar.Append(self.menu2, u"出入库")
        self.menuBar.Append(self.menu3, u"管理")
        self.menuBar.Append(self.menu4, u"关于")
        self.SetMenuBar(self.menuBar)

        self.Bind(wx.EVT_MENU, self.OnSelectExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.ImportExcelFile, id=2)
        self.Bind(wx.EVT_MENU, self.ImportCSVFile, id=3)
        self.Bind(wx.EVT_MENU, self.ExportExcelFile, id=4)
        self.Bind(wx.EVT_MENU, self.ExportCSVFile, id=5)
        self.Bind(wx.EVT_MENU, self.OpenPurchasePage, id=12)
        self.Bind(wx.EVT_MENU, self.OpenSellPage, id=13)
        self.Bind(wx.wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, id=13)
        self.Bind(wx.EVT_MENU, self.OpenAboutPage, id=14)
        self.Bind(wx.EVT_MENU, self.OpenHelpPage, id=299)
        self.Bind(wx.EVT_MENU, self.OpenModifyPage, id=19)
        self.Bind(wx.EVT_MENU, self.OpenAccountPage, id=90)
        self.Bind(wx.EVT_MENU, self.OpenStatementPage, id=91)
        self.Bind(wx.EVT_MENU, self.OpenPrinterPage, id=320)
        self.Bind(wx.EVT_CLOSE, self.OnCloseBackup)
        self.Bind(wx.EVT_PAINT, self.MaximizeFrame)

        self.Bind(wx.EVT_BUTTON, self.GoodsQuery, id = 17)
        self.Bind(wx.EVT_BUTTON, self.QueryAll, id = 18)
        self.Bind(wx.EVT_BUTTON, self.OpenQuerySellAndQuery, id=8)
        self.Bind(wx.EVT_BUTTON, self.OpenUpdatePageAndQuery, id = 9)
        self.Bind(wx.EVT_BUTTON, self.GoodsDeleteAndQuery, id = 16)
        self.Bind(wx.EVT_TEXT_ENTER, self.GoodsQuery,id=7)

        self.panel.SetSizer(self.ColSizer)
        self.panel.Layout()


    def __init__111(self):
        # SetTitle(u"Yueer PSS服装类出入库系统")
        self.menu1 = wx.Menu()
        self.submenu_Import = wx.Menu()
        self.submenu_Import.Append(2, u"Excel导入", u"从.xls文件导入库存数据")
        self.submenu_Import.Append(3, u"CSV导入", u"从.csv文件导入库存数据")
        self.menu1.AppendMenu(-1, u"导入", self.submenu_Import)
        self.submenu_Export = wx.Menu()
        self.submenu_Export.Append(4, u"导出Excel", u"将库存数据导出为.xls文件")
        self.submenu_Export.Append(5, u"导出CSV", u"将库存数据导出为.csv文件")
        self.menu1.AppendMenu(-1, u"导出", self.submenu_Export)
        self.menu1.Append(wx.ID_EXIT, u"退出登录", u"退出程序并返回到登录界面.")


        self.menu2 = wx.Menu()
        self.menu2.Append(12, u"入库登记",u"入库登记.")
        self.menu2.Append(13, u"出库登记", u"出库登记.")
        self.menu2.Append(19, u"二次入库登记", u"新增并修改入库登记,适合于第二次进货")
        self.menu3 = wx.Menu()
        self.menu3.Append(90, u"账户管理", u"管理员管理登陆账户")
        self.menu3.Append(91, u"绩效报表", u"导购员\店长销售绩效报表")
        self.menu3.Append(320, u"小票打印", u"出库小票打印设置")

        self.menu4 = wx.Menu()
        self.menu4.Append(14, u"关于", u"关于软件程序");
        self.menu4.Append(299, u"帮助", u"导入帮助和自动备份功能介绍!")

        self.DeleteBMP = wx.Image("delete.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.EditBMP = wx.Image("edit.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.GoodsDelete_Button=wx.BitmapButton(self.panel, 16, self.DeleteBMP)
        self.GoodsUpdate_Button=wx.BitmapButton(self.panel,9, self.EditBMP)

        RowSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        RowSizer1.Add(self.GoodsInfo_Label, flag=wx.LEFT,border=5)
        RowSizer1.Add(self.GoodsInfo_Text, proportion=1, border=10, flag=wx.LEFT)
        RowSizer1.Add(self.GoodsSearch_Button, proportion=1, border=20, flag=wx.LEFT)
        RowSizer1.Add(self.GoodsSearchAll_Button, proportion=1, border=20, flag=wx.LEFT)
        RowSizer1.Add(self.GoodsQuerySell_Button, proportion=1, border=20, flag=wx.LEFT)
        RowSizer1.Add(self.GoodsUpdate_Button, proportion=1, border=20, flag=wx.LEFT)
        RowSizer1.Add(self.GoodsDelete_Button, proportion=1, border=20, flag=wx.LEFT)

        RowSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        RowSizer2.Add(self.SearchList_Report, proportion=1, border=5, flag=wx.CENTRE)

        self.ColSizer = wx.BoxSizer(wx.VERTICAL)
        self.ColSizer.Add(RowSizer1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,border=10)
        self.ColSizer.Add(RowSizer2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP|wx.ALL,border=10)
        self.panel.SetSizer(self.ColSizer)
        self.panel.Layout()


    def __init__222(self):
        self.menu1 = wx.Menu()
        self.submenu_Export = wx.Menu()
        self.submenu_Export.Append(4, u"导出Excel", u"将库存数据导出为.xls文件")
        self.submenu_Export.Append(5, u"导出CSV", u"将库存数据导出为.csv文件")
        self.menu1.AppendMenu(-1, u"导出", self.submenu_Export)
        self.menu1.Append(wx.ID_EXIT, u"退出登录", u"退出程序并返回到登录界面.")

        self.menu2 = wx.Menu()
        self.menu2.Append(13, u"出库登记", u"出库登记.")

        self.menu3 = wx.Menu()

        self.menu4 = wx.Menu()
        self.menu4.Append(14, u"关于", u"关于软件程序")
        self.menu4.Append(299, u"帮助", u"导入帮助和自动备份功能介绍!")

        self.RowSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.RowSizer1.Add(self.GoodsInfo_Label, flag=wx.LEFT,border=5)
        self.RowSizer1.Add(self.GoodsInfo_Text, proportion=1, border=10, flag=wx.LEFT)
        self.RowSizer1.Add(self.GoodsSearch_Button, proportion=1, border=20, flag=wx.LEFT)
        self.RowSizer1.Add(self.GoodsSearchAll_Button, proportion=1, border=20, flag=wx.LEFT)
        self.RowSizer1.Add(self.GoodsQuerySell_Button, proportion=1, border=20, flag=wx.LEFT)


        self.RowSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.RowSizer2.Add(self.SearchList_Report, proportion=1, border=5, flag=wx.CENTRE)

        self.ColSizer = wx.BoxSizer(wx.VERTICAL)
        self.ColSizer.Add(self.RowSizer1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,border=10)
        self.ColSizer.Add(self.RowSizer2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP|wx.ALL,border=10)


    def GetListCtrl(self):
        return self.SearchList_Report

    def MaximizeFrame(self,evt):
        if(self.IsMaximized()==True):
            self.SearchList_Report.SetColumnWidth(0, 120)
            self.SearchList_Report.SetColumnWidth(1, 120)
            self.SearchList_Report.SetColumnWidth(2, 160)
            self.SearchList_Report.SetColumnWidth(3, 80)
            self.SearchList_Report.SetColumnWidth(4, 80)
            self.SearchList_Report.SetColumnWidth(5, 80)
            self.SearchList_Report.SetColumnWidth(6, 80)
            self.SearchList_Report.SetColumnWidth(7, 80)
            self.SearchList_Report.SetColumnWidth(8, 100)
            self.SearchList_Report.SetColumnWidth(9, 120)
            self.SearchList_Report.SetColumnWidth(10, 160)
        else:
            self.SearchList_Report.SetColumnWidth(0, 90)
            self.SearchList_Report.SetColumnWidth(1, 95)
            self.SearchList_Report.SetColumnWidth(2, 85)
            self.SearchList_Report.SetColumnWidth(3, 55)
            self.SearchList_Report.SetColumnWidth(4, 55)
            self.SearchList_Report.SetColumnWidth(5, 55)
            self.SearchList_Report.SetColumnWidth(6, 55)
            self.SearchList_Report.SetColumnWidth(7, 55)
            self.SearchList_Report.SetColumnWidth(8, 55)
            self.SearchList_Report.SetColumnWidth(9, 90)
            self.SearchList_Report.SetColumnWidth(10, 90)

    def OnCloseBackup(self, evt):
        dial = wx.MessageDialog(None,u"确定要关闭程序并退出登录吗?", u"提示",  
                                wx.YES_NO|wx.NO_DEFAULT|wx.ICON_QUESTION)  
        ret = dial.ShowModal()  
        if ret == wx.ID_YES:
            SearchGoods.Disable_Active_Account();
            if(exists(getcwd()+"\\Backup")==False):
                mkdir(getcwd()+"\\Backup")
            else:
                pass
            self.RemoveBackup();                        
            ExcelFileName=strftime("%Y-%m-%d", localtime())
            filename=getcwd()+"\\Backup\\%s"%ExcelFileName+".xls"
            if(exists(filename)==True):
                try:
                    remove(filename)
                except:
                    pass
            else:
                pass
            try:
                SearchGoods.WriteToExcel(filename);  
            except:
                pass;
            self.Destroy()
            _exit(0)  
        else:  
            evt.Veto()  


    def OnSelectExit(self, evt):
        SearchGoods.Disable_Active_Account();
        if(exists(getcwd()+"\\Backup")==False):
            mkdir(getcwd()+"\\Backup")
        else:
            pass
        self.RemoveBackup();
        ExcelFileName=strftime("%Y-%m-%d", localtime())
        filename=getcwd()+"\\Backup\\%s"%ExcelFileName+".xls"
        if(exists(filename)==True):
            try:
                remove(filename)
            except:
                pass
        else:
            pass
        try:
            SearchGoods.WriteToExcel(filename);
        except:
            pass;
        self.Destroy()
        app2 = wx.App()
        frame2 = Yueer_PSS.loginFrame()
        frame2.Show()
        app2.MainLoop()

    def RemoveBackup(self): 
        Dirpath=getcwd()+"\\Backup";
        filelist=listdir(Dirpath);
        for i in filelist:
            if(match(r".*\.xls",i)):
                try:
                    SearchGoods.DeleteBackup(Dirpath,i);
                except:
                    pass;

    def OnItemActivated(self, evt): 
        print "Item activated:****"*30;


    def OpenSellPage(self, evt):
        initNum1=self.Return_TotalGoods()
        initNum2=self.Return_TotalStore()
        if(self.GoodsIDSelected()!=None):
            dlg = QuerySell.QuerySellPage(self.GoodsIDSelected(),self.GoodsPricesSelected(),"")
            dlg.ShowModal()
            rows=[]
            index = long(self.SearchList_Report.GetFirstSelected());
            try:
                GoodsInfo= str(getattr(self,"GoodsInfo_Text").GetValue()) ##获取非中文时, 用这句
            except:
                GoodsInfo = repr((getattr(self,"GoodsInfo_Text").GetValue()).encode('gb2312'))#获取中文时,用这句
                GoodsInfo = sub(r"\'","",GoodsInfo) #由于用了repr,所以需要把字符串的两个单引号去掉, 所以去''
                GoodsInfo = sub(r"\\", "", GoodsInfo)#由于带\的所有gb2312编码的字符串都无法进行查询,替换等工作, 所以去\
            if(GoodsInfo==""):
                rows=self.Return_AllData()
            else:
                rows=self.Return_QueryData()
            self.ListDisplay(rows)
            self.SearchList_Report.Select(index);###返回到刚才的选中项
            initNum1=abs(self.Return_TotalGoods()-initNum1)
            initNum2=abs(self.Return_TotalStore()-initNum2)
            self.statusbar.SetStatusText(u"商品总数: %d 款"%self.Return_TotalGoods(), 0)
            self.statusbar.SetStatusText(u"库存总数: %d 件"%self.Return_TotalStore(), 1)
            self.statusbar.SetStatusText(u"刚出库商品数: %d 款, 刚出库库存数： %d 件"%(initNum1,initNum2), 2)
            dlg.Destroy() 
        else:
            dlg = Sell.SellPage("")
            dlg.ShowModal()
            dlg.Destroy()
            initNum1=abs(self.Return_TotalGoods()-initNum1)
            initNum2=abs(self.Return_TotalStore()-initNum2)
            self.statusbar.SetStatusText(u"商品总数: %d 款"%self.Return_TotalGoods(), 0)
            self.statusbar.SetStatusText(u"库存总数: %d 件"%self.Return_TotalStore(), 1)
            self.statusbar.SetStatusText(u"刚出库商品数: %d 款, 刚出库库存数： %d 件"%(initNum1,initNum2), 2)  

    def OpenPurchasePage(self, evt):
        initNum1=self.Return_TotalGoods()
        initNum2=self.Return_TotalStore()
        dlg = Purchase.PurchasePage()
        dlg.ShowModal()      
        dlg.Destroy()
        rows=[]
        try:
            GoodsInfo= str(getattr(self,"GoodsInfo_Text").GetValue()) ##获取非中文时, 用这句
        except:
            GoodsInfo = repr((getattr(self,"GoodsInfo_Text").GetValue()).encode('gb2312'))#获取中文时,用这句
            GoodsInfo = sub(r"\'","",GoodsInfo) #由于用了repr,所以需要把字符串的两个单引号去掉, 所以去''
            GoodsInfo = sub(r"\\", "", GoodsInfo)#由于带\的所有gb2312编码的字符串都无法进行查询,替换等工作, 所以去\
        if(GoodsInfo==""):
            rows=self.Return_AllData()
        else:
            rows=self.Return_QueryData()
        self.ListDisplay(rows)
        initNum1=abs(self.Return_TotalGoods()-initNum1)
        initNum2=abs(self.Return_TotalStore()-initNum2)
        self.statusbar.SetStatusText(u"商品总数: %d 款"%self.Return_TotalGoods(), 0)
        self.statusbar.SetStatusText(u"库存总数: %d 件"%self.Return_TotalStore(), 1)
        self.statusbar.SetStatusText(u"新增商品数: %d 款, 新增库存数： %d 件"%(initNum1,initNum2), 2)  

    def OpenModifyPage(self, evt):
        initNum1=self.Return_TotalGoods()
        initNum2=self.Return_TotalStore()
        dlg = Modify.ModifyPage()
        dlg.ShowModal() 
        dlg.Destroy()
        rows=[]
        try:
            GoodsInfo= str(getattr(self,"GoodsInfo_Text").GetValue()) ##获取非中文时, 用这句
        except:
            GoodsInfo = repr((getattr(self,"GoodsInfo_Text").GetValue()).encode('gb2312'))#获取中文时,用这句
            GoodsInfo = sub(r"\'","",GoodsInfo) #由于用了repr,所以需要把字符串的两个单引号去掉, 所以去''
            GoodsInfo = sub(r"\\", "", GoodsInfo)#由于带\的所有gb2312编码的字符串都无法进行查询,替换等工作, 所以去\
        if(GoodsInfo==""):
            rows=self.Return_AllData()
        else:
            rows=self.Return_QueryData()
        self.ListDisplay(rows)
        initNum1=abs(self.Return_TotalGoods()-initNum1)
        initNum2=abs(self.Return_TotalStore()-initNum2)        
        self.statusbar.SetStatusText(u"商品总数: %d 款"%self.Return_TotalGoods(), 0)
        self.statusbar.SetStatusText(u"库存总数: %d 件"%self.Return_TotalStore(), 1)
        self.statusbar.SetStatusText(u"新增商品数: %d 款, 新增库存数： %d 件"%(initNum1,initNum2), 2)   

    def OpenAccountPage(self, evt):
        dlg = Account.AccountPage()
        dlg.ShowModal() 
        dlg.Destroy()

    def OpenStatementPage(self, evt):
        dlg = Statement.StatementPage()
        dlg.ShowModal() 
        dlg.Destroy()

    def OpenPrinterPage(self, evt):
        dlg = Printer.Printer_Page()
        dlg.ShowModal() 
        dlg.Destroy()

    def OpenAboutPage(self, evt):
        dlg = About.AboutPage(self)
        dlg.ShowModal()
        dlg.Destroy()

    def OpenHelpPage(self, evt):
        dlg = About.HelpPage(self)
        dlg.ShowModal()
        dlg.Destroy()

    def Return_TotalGoods(self):
        IDs=[]
        dbreader=shelve.open('database.dat','r')
        for i in dbreader.items():
            IDs.append(i[0])
        dbreader.close()
        # print len(IDs)
        return len(IDs)        

    def Return_TotalStore(self):
        TotalStore=0
        dbreader=shelve.open('database.dat','r')
        for i in dbreader.items():
            TotalStore=TotalStore+int(i[1]['GStoreNum'])
        # print TotalStore
        dbreader.close()
        return TotalStore

    def ImportCSVFile(self, evt):
        initNum1=self.Return_TotalGoods()
        initNum2=self.Return_TotalStore()
        wildcard = "CSV File (*.csv)|*.csv"
        dialog = wx.FileDialog(None, u"请选择一个*.CSV数据文件", getcwd(), 
            "", wildcard, wx.OPEN)
        # print str(dialog.GetPath())[-1:4];
        if dialog.ShowModal() == wx.ID_OK:
            try:
                dbwriter=shelve.open('database.dat','w')
            except:
                dbwriter=shelve.open('database.dat','c')
            try:
                if(SearchGoods.StoreDataFromCSV(u"%s"%dialog.GetPath(),dbwriter)):
                    dbwriter.close() 
                    initNum1=abs(self.Return_TotalGoods()-initNum1)
                    initNum2=abs(self.Return_TotalStore()-initNum2)
                    SearchGoods.ImportPassedMessageBox(initNum1, initNum2)
                else:
                    dbwriter.close();
                    SearchGoods.ErrorMessageBox(u"导入失败, 请确保你导入的是有效的.csv文件!并确保内容的正确性,谢谢!");
                    initNum1=abs(self.Return_TotalGoods()-initNum1)
                    initNum2=abs(self.Return_TotalStore()-initNum2)
            except IOError:
                SearchGoods.ErrorMessageBox(u"你导入的文件有错误,请确保你导入的是有效的.csv文件!");
        else:
            pass
        self.QueryAll_NoEvt()
        self.statusbar.SetStatusText(u"商品总数: %d 款"%self.Return_TotalGoods(), 0)
        self.statusbar.SetStatusText(u"库存总数: %d 件"%self.Return_TotalStore(), 1)
        self.statusbar.SetStatusText(u"入库新增商品数: %d 款,  入库新增库存数： %d 件"%(initNum1,initNum2), 2) 
        dialog.Destroy()

    def ImportExcelFile(self, evt):
        initNum1=self.Return_TotalGoods()
        initNum2=self.Return_TotalStore()
        wildcard = "Excel 2007~2013 File(*.xlsx)|*.xlsx|"\
                    "Excel 2003 File (*.xls)|*.xls|"\
                    "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, u"请选择一个*.xls数据文件", getcwd(), 
            "", wildcard, wx.OPEN)
        # print str(dialog.GetPath())[-1:5];
        if dialog.ShowModal() == wx.ID_OK:
            try:
                dbwriter=shelve.open('database.dat','w')
            except:
                dbwriter=shelve.open('database.dat','c');
            # try:
            # # if(repr((dialog.GetPath()).encode('gb2312'))[-4:-1]=="csv"):
            if(SearchGoods.StoreDataFromExcel(u"%s"%dialog.GetPath(),dbwriter)):
                dbwriter.close() 
                initNum1=abs(self.Return_TotalGoods()-initNum1)
                initNum2=abs(self.Return_TotalStore()-initNum2)
                SearchGoods.ImportPassedMessageBox(initNum1, initNum2)
            else:
                dbwriter.close() 
                SearchGoods.ErrorMessageBox(u"导入失败,请确保你导入的是有效的.xls文件或者.xlsx文件!并确保内容的正确性,谢谢!");
                initNum1=abs(self.Return_TotalGoods()-initNum1)
                initNum2=abs(self.Return_TotalStore()-initNum2)
            # except:
            #     SearchGoods.ErrorMessageBox(u"请确保你导入的是有效的.xls文件或者.xlsx文件!");
        else:
            pass
        self.QueryAll_NoEvt()
        self.statusbar.SetStatusText(u"商品总数: %d 款"%self.Return_TotalGoods(), 0)
        self.statusbar.SetStatusText(u"库存总数: %d 件"%self.Return_TotalStore(), 1)
        self.statusbar.SetStatusText(u"入库新增商品数: %d 款,  入库新增库存数： %d 件"%(initNum1,initNum2), 2) 
        dialog.Destroy()

    def ExportCSVFile(self,evt):
        wildcard2 = "CSV File (*.csv)|*.csv"
        dlg = wx.FileDialog(self, u"另存为CSV文件...", getcwd(), 
            "", wildcard2, wx.SAVE|wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            filename=u"%s"%dlg.GetPath()
            # print filename
            if not splitext(filename)[1]:
                filename = filename + '.csv'
            self.filename = filename
            # print filename
            findname='''%s'''%filename
            try:
                SearchGoods.WriteToCSV(filename)
                dlg.Destroy()
                SearchGoods.ExportMessageBox()
            except:
                dlg.Destroy()
                SearchGoods.ExportErrorMessageBox(filename)
        else:
            pass

    def ExportExcelFile(self,evt):
        wildcard2 = "Excel 2003 File (*.xls)|*.xls"
        dlg = wx.FileDialog(self, u"另存为Excel文件...", getcwd(), 
            "", wildcard2, wx.SAVE|wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            filename=u"%s"%dlg.GetPath()
            # print filename
            if not splitext(filename)[1]:
                filename = filename + '.xls'
            self.filename = filename
            # print filename
            findname='''%s'''%filename
            # print findname
            try:
                SearchGoods.WriteToExcel(filename)
                dlg.Destroy()
                SearchGoods.ExportMessageBox()
            except:
                dlg.Destroy()
                SearchGoods.ExportErrorMessageBox(filename)                
        else:
            pass

    def ListDisplay(self, rows):
        self.SearchList_Report.DeleteAllItems()
        self.itemDataMap = {}
        for item in rows:
            index = self.SearchList_Report.InsertStringItem(maxint, item[0])
            for col, text in enumerate(item[1:]):
                self.SearchList_Report.SetStringItem(index, col+1, text)
            self.SearchList_Report.SetItemData(index, index)
            self.itemDataMap[index] = item

    def QueryAll(self,evt):
        getattr(self,"GoodsInfo_Text").SetValue("")
        self.ListDisplay(self.Return_AllData())
        self.statusbar.SetStatusText(u"商品总数: %d 款"%self.Return_TotalGoods(), 0)
        self.statusbar.SetStatusText(u"库存总数: %d 件"%self.Return_TotalStore(), 1)
        self.statusbar.SetStatusText(u"共查询到 %d 款商品"%len(self.Return_AllData()), 2)


    def QueryAll_NoEvt(self):
        getattr(self,"GoodsInfo_Text").SetValue("")
        self.ListDisplay(self.Return_AllData())

    def Return_AllData(self):
        Allvalues=[]
        dbreader=shelve.open('database.dat','r')
        rows=SearchGoods.GetDBValues_To_tuple(Allvalues,dbreader)
        dbreader.close()
        return rows

    def GoodsQuery(self, evt):
        if(self.Return_QueryData()!=None):
            self.ListDisplay(self.Return_QueryData())
            self.statusbar.SetStatusText(u"商品总数: %d 款"%self.Return_TotalGoods(), 0)
            self.statusbar.SetStatusText(u"库存总数: %d 件"%self.Return_TotalStore(), 1)
            self.statusbar.SetStatusText(u"共查询到 %d 款商品"%len(self.Return_QueryData()), 2)
        else:
            pass


    def Return_QueryData(self):
        try:
            GoodsInfo= str(getattr(self,"GoodsInfo_Text").GetValue()) ##获取非中文时, 用这句
        except:
            GoodsInfo = repr((getattr(self,"GoodsInfo_Text").GetValue()).encode('gb2312'))#获取中文时,用这句
            GoodsInfo = sub(r"\'","",GoodsInfo) #由于用了repr,所以需要把字符串的两个单引号去掉, 所以去''
            GoodsInfo = sub(r"\\", "", GoodsInfo)#由于带\的所有gb2312编码的字符串都无法进行查询,替换等工作, 所以去\

        #"+"号查询:
        if(match(r'.*(\+).*',GoodsInfo)):
            GoodsInfo=sub(r'\s',"",GoodsInfo);##去空格, 即支持查询条件输入后自动去空格.
            m=match(r'(.*)(\+)(.*)',GoodsInfo);
            GoodsInfo=m.group(1);
            GoodsInfo2=m.group(3)
        IDs=[]
        FindIDs=[]
        if(GoodsInfo!=""):
            dbreader=shelve.open('database.dat','r')
            for i in dbreader.items():
                str_i=str(i[1].values())###i[1]是字典, 获取字典的所有值,本来是返回一个列表,但是由于列表不能进行查询,替换等工作, 所以转换成字符串.
                TempList=[]  ##TempList做初始化工作, 一定要放这里, 不然会出问题.
                for num in str_i: ##对字符串内的所有字符进行去\ 去' 处理.
                    num = sub(r"\\","",num)
                    num = sub(r'\'',"",num)
                    TempList.append(num) #处理完后,再以列表的形式组合起来.
                TempString="".join(TempList)#因为列表无法用来做匹配工作, 所以转换成字符串.
                #"+"号查询, 因为可能GoodsInfo2可能会出现没定义的情况,正好抛出异常.正好执行异常语句
                try:
                    if(match(r".*(%s).*(%s).*"%(GoodsInfo,GoodsInfo2), TempString)):
                        IDs.append(i[0])
                    elif(match(r".*(%s).*(%s).*"%(GoodsInfo2,GoodsInfo), TempString)):
                        IDs.append(i[0])
                except:
                    if((match(r".*(%s).*"%GoodsInfo, TempString))):###这才是重点,获取i[0], 即商品编号.
                        IDs.append(i[0])
            for item in IDs:
                FindIDs.append(SearchGoods.GetQuery_To_tuple(item))
            dbreader.close()
            return FindIDs
        else:
            return None   
    
    def GoodsDeleteAndQuery(self, evt):
        initNum1=self.Return_TotalGoods()
        initNum2=self.Return_TotalStore()
        rows=[]
        index = long(self.SearchList_Report.GetFirstSelected());
        try:
            GoodsInfo= str(getattr(self,"GoodsInfo_Text").GetValue()) ##获取非中文时, 用这句
        except:
            GoodsInfo = repr((getattr(self,"GoodsInfo_Text").GetValue()).encode('gb2312'))#获取中文时,用这句
            GoodsInfo = sub(r"\'","",GoodsInfo) #由于用了repr,所以需要把字符串的两个单引号去掉, 所以去''
            GoodsInfo = sub(r"\\", "", GoodsInfo)#由于带\的所有gb2312编码的字符串都无法进行查询,替换等工作, 所以去\
        # print index
        if(index != -1):
            item = self.SearchList_Report.GetItem(index)
            GoodsID=str(item.GetText())
            dbwriter=shelve.open('database.dat','w',writeback=True)
            dlg1 = wx.MessageDialog(None, u"确定要删除商品%s的所有库存记录吗?"%GoodsID, u'提示', wx.OK|wx.CANCEL)
            if dlg1.ShowModal() == wx.ID_OK:
                dbwriter.pop(GoodsID)
                SearchGoods.DeleteGoodsMessageBox(GoodsID)
                dbwriter.close() 
                Allvalues=[]
                dbreader=shelve.open('database.dat','r')
                if(GoodsInfo==""):
                    rows=self.Return_AllData()
                else:
                    rows=self.Return_QueryData()
                self.ListDisplay(rows)
                self.SearchList_Report.Select(index);###返回到刚才的选中项
                initNum1=abs(self.Return_TotalGoods()-initNum1)
                initNum2=abs(self.Return_TotalStore()-initNum2)
                self.statusbar.SetStatusText(u"商品总数: %d 款"%self.Return_TotalGoods(), 0)
                self.statusbar.SetStatusText(u"库存总数: %d 件"%self.Return_TotalStore(), 1)
                self.statusbar.SetStatusText(u"删除商品数: %d 款, 此次删除共减少库存数： %d 件"%(initNum1,initNum2), 2)  
                dbreader.close()
            else:
                pass
                dbwriter.close() 
            dlg1.Destroy()
        else:
            pass
            
    def OpenUpdatePageAndQuery(self, evt):
        initNum2=self.Return_TotalStore()
        if(self.GoodsIDSelected()!=None):
            dlg = Update.UpdatePage(self.GoodsIDSelected())
            dlg.ShowModal()
            rows=[]
            index = long(self.SearchList_Report.GetFirstSelected());
            try:
                GoodsInfo= str(getattr(self,"GoodsInfo_Text").GetValue()) ##获取非中文时, 用这句
            except:
                GoodsInfo = repr((getattr(self,"GoodsInfo_Text").GetValue()).encode('gb2312'))#获取中文时,用这句
                GoodsInfo = sub(r"\'","",GoodsInfo) #由于用了repr,所以需要把字符串的两个单引号去掉, 所以去''
                GoodsInfo = sub(r"\\", "", GoodsInfo)#由于带\的所有gb2312编码的字符串都无法进行查询,替换等工作, 所以去\
            if(GoodsInfo==""):
                rows=self.Return_AllData()
            else:
                rows=self.Return_QueryData()
            self.ListDisplay(rows)
            self.SearchList_Report.Select(index);###返回到刚才的选中项            
            initNum2=self.Return_TotalStore()-initNum2
            self.statusbar.SetStatusText(u"商品总数: %d 款"%self.Return_TotalGoods(), 0)
            self.statusbar.SetStatusText(u"库存总数: %d 件"%self.Return_TotalStore(), 1)
            if(initNum2>0):
                self.statusbar.SetStatusText(u"修改了1款商品,  增加库存数： %d 件"%abs(initNum2), 2) 
            else:
                self.statusbar.SetStatusText(u"修改了1款商品,  减少库存数： %d 件"%abs(initNum2), 2)
            dlg.Destroy()
        else:
            pass

    def OpenQuerySellAndQuery(self, evt):
        initNum1=self.Return_TotalGoods()
        initNum2=self.Return_TotalStore()
        if(self.GoodsIDSelected()!=None):
            dlg = QuerySell.QuerySellPage(self.GoodsIDSelected(),self.GoodsPricesSelected(),"")
            dlg.ShowModal()
            rows=[]
            index = long(self.SearchList_Report.GetFirstSelected());

            try:
                GoodsInfo= str(getattr(self,"GoodsInfo_Text").GetValue()) ##获取非中文时, 用这句
            except:
                GoodsInfo = repr((getattr(self,"GoodsInfo_Text").GetValue()).encode('gb2312'))#获取中文时,用这句
                GoodsInfo = sub(r"\'","",GoodsInfo) #由于用了repr,所以需要把字符串的两个单引号去掉, 所以去''
                GoodsInfo = sub(r"\\", "", GoodsInfo)#由于带\的所有gb2312编码的字符串都无法进行查询,替换等工作, 所以去\
            if(GoodsInfo==""):
                rows=self.Return_AllData()
            else:
                rows=self.Return_QueryData()
            self.ListDisplay(rows)
            self.SearchList_Report.Select(index);###返回到刚才的选中项
            initNum1=abs(self.Return_TotalGoods()-initNum1)
            initNum2=abs(self.Return_TotalStore()-initNum2)
            self.statusbar.SetStatusText(u"商品总数: %d 款"%self.Return_TotalGoods(), 0)
            self.statusbar.SetStatusText(u"库存总数: %d 件"%self.Return_TotalStore(), 1)
            self.statusbar.SetStatusText(u"刚出库商品数: %d 款, 刚出库库存数： %d 件"%(initNum1,initNum2), 2)
            dlg.Destroy() 
        else:
            pass

    def GoodsIDSelected(self):
        index = self.SearchList_Report.GetFirstSelected()
        if(index != -1):
            item = self.SearchList_Report.GetItem(index)
            GoodsID=str(item.GetText());
            return GoodsID
        else:
            return None

    def GoodsPricesSelected(self):
        dbreader=shelve.open('database.dat','r')
        if(self.GoodsIDSelected!=None):
            ID=self.GoodsIDSelected()
            return dbreader[ID]['GPrice']
        else:
            dbreader.close();
            return None;
