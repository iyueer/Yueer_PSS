# coding: UTF-8
#Author:张祖兴 iyueer@163.com

import wx;

import shelve,dbhash,anydbm;
import SearchGoods;
from sys import maxint
import win32print


class PrintSellPage(wx.Dialog):
    """
    This is StatementPage.  
    """
    def __init__(self):
        wx.Dialog.__init__(self,None,-1, u"打印小票",size=(300, 400))
        self.ScreenSize=wx.DisplaySize(); ##Get the ScreenSize(Resloution)
        self.Centre();
        panel = wx.Panel(self);

        # self.CreateStatusBar()
        self.icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon);
        self.SellPrint_Label = wx.StaticText(panel, -1, u"      \n待打印商品:                                ",style=wx.ALIGN_BOTTOM);
        DeletePrint_Button = wx.Button(panel, 500, u"删除打印项")
        Print_Button = wx.Button(panel, 501, u"打 印 小 票")
        Close_Button = wx.Button(panel, 502, u"关   闭")
        TotalPrice_Label = wx.StaticText(panel, -1, u"  总 金 额(￥) : ")
        self.TotalPrice_Label2 = wx.StaticText(panel, -1, "%s"%self.ReturnPrices()[0])
        FinalPrice_Label = wx.StaticText(panel, -1, u"  最终金额(￥) : ")
        self.FinalPrice_Label2 = wx.StaticText(panel, -1, "%s"%self.ReturnPrices()[2])
        OffersPrice_Label = wx.StaticText(panel, -1, u"  优    惠(￥) : ")
        self.OffersPrice_Label2 = wx.StaticText(panel, -1, "-%s"%self.ReturnPrices()[1])
        Blank_Label = wx.StaticText(panel, -1, "")
        Blank_Label2 = wx.StaticText(panel, -1, "")
        self.SellPrint = wx.ListCtrl(panel, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_SINGLE_SEL|wx.LC_SORT_ASCENDING, size=(280,200))
        Print_columns = ['\xc9\xcc\xc6\xb7\xb1\xe0\xba\xc5','\xc0\xe0\xb1\xf0','\xca\xfd\xc1\xbf','\xb5\xa5\xbc\xdb']
        for col, text in enumerate(Print_columns):
            self.SellPrint.InsertColumn(col, text, wx.LIST_FORMAT_CENTRE);
        self.SellPrint.SetColumnWidth(0, 80);
        self.SellPrint.SetColumnWidth(1, 50)
        self.SellPrint.SetColumnWidth(2, 80)
        self.SellPrint.SetColumnWidth(3, 80)

        fgs = wx.FlexGridSizer(4,2,8,10)


        RowSizer1 = wx.BoxSizer(wx.HORIZONTAL);
        RowSizer1.Add(self.SellPrint_Label, flag=wx.LEFT, border=10)
        RowSizer1.Add(DeletePrint_Button, flag=wx.EXPAND|wx.LEFT, border=0)

        RowSizer2 = wx.BoxSizer(wx.HORIZONTAL);
        RowSizer2.Add(Close_Button, flag=wx.LEFT, border=10)
        RowSizer2.Add(Print_Button, flag=wx.EXPAND|wx.LEFT, border=105)

        fgs.AddMany([(TotalPrice_Label,1,wx.EXPAND),(self.TotalPrice_Label2,1,wx.EXPAND),
                     (OffersPrice_Label,1,wx.EXPAND),(self.OffersPrice_Label2,1,wx.EXPAND),
                     (FinalPrice_Label,1,wx.EXPAND),(self.FinalPrice_Label2,1,wx.EXPAND),
                     (Blank_Label,1,wx.EXPAND),(Blank_Label2,1,wx.EXPAND)])
        fgs.AddGrowableCol(1,1)

        ColSizer = wx.BoxSizer(wx.VERTICAL);
        # ColSizer.Add(RowSizer1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP|wx.ALL, border=7);
        ColSizer.Add(RowSizer1,flag=wx.RIGHT, border=7);
        ColSizer.Add(self.SellPrint,flag=wx.LEFT, border=10);
        ColSizer.Add(fgs,flag=wx.RIGHT, border=7);
        # ColSizer.Add(RowSizer3,flag=wx.RIGHT, border=7);
        # ColSizer.Add(RowSizer4,flag=wx.RIGHT, border=7);
        # ColSizer.Add(RowSizer5,flag=wx.RIGHT, border=7);
        ColSizer.Add(RowSizer2,flag=wx.RIGHT, border=7);

        self.Bind(wx.EVT_BUTTON, self.SellPrintDelete, id = 500)
        self.Bind(wx.EVT_BUTTON, self.ClosePrintlist, id=502)
        self.Bind(wx.EVT_BUTTON, self.Print_Querysell, id=501)

        self.SellPrintQueryAll_NoEvt();

        panel.SetSizer(ColSizer);
        panel.Layout();

    def Return_AllPrintList(self):
        ''''可打印列表'''
        AllRows=[];
        dbreader=shelve.open('PrintList.dat','r');
        rows=SearchGoods.GetPrintList_To_tuple(AllRows,dbreader)
        dbreader.close()
        # print rows;
        return rows

    def SellPrintListDisplay(self, rows):
        self.SellPrint.DeleteAllItems()
        self.itemDataMap = {}
        for item in rows:
            index = self.SellPrint.InsertStringItem(maxint, item[0])
            for col, text in enumerate(item[1:]):
                self.SellPrint.SetStringItem(index, col+1, text)
            self.SellPrint.SetItemData(index, index)
            self.itemDataMap[index] = item;

    def SellPrintQueryAll_NoEvt(self):
        self.SellPrintListDisplay(self.Return_AllPrintList())

    def SellPrintDelete(self, evt):
        index = long(self.SellPrint.GetFirstSelected());
        # print index
        if(index != -1):
            item = self.SellPrint.GetItem(index)
            GoodsID=str(item.GetText())
            dbwriter=shelve.open('PrintList.dat','w',writeback=True)
            dbwriter.pop(GoodsID)
            dbwriter.close()
            self.Print_Teardown();
            self.SellPrint.Select(index);###返回到刚才的选中项
        else:
            SearchGoods.ReminderMessageBox(u"请先选中某打印项后进行删除！")

    def ClosePrintlist(self, evt):
        self.Close();

    def ReturnPrices(self):
        TotalPrice=0;
        FinalPrice=0;
        OffersPrice=0;
        dbreader2=shelve.open("PrintList.dat",'r')
        for item in dbreader2.items():
            TotalPrice=str(int(item[1]["Price"])+int(TotalPrice));
            FinalPrice=str(int(item[1]["Finalprice"])+int(FinalPrice));
            OffersPrice=str(int(item[1]["PriceGap"])+int(OffersPrice));
        dbreader2.close();
        return TotalPrice, OffersPrice, FinalPrice;

    def Print_Teardown(self):
        self.TotalPrice_Label2.SetLabel("%s"%self.ReturnPrices()[0])
        self.OffersPrice_Label2.SetLabel("-%s"%self.ReturnPrices()[1])
        self.FinalPrice_Label2.SetLabel("%s"%self.ReturnPrices()[2])
        self.SellPrintListDisplay(self.Return_AllPrintList())
    # def Print_Querysell(self, evt):
    #     dbreader=shelve.open('config.dat','r')
    #     self.Name_Print=dbreader["config"]["Name"]
    #     self.Address_Print=dbreader["config"]["Address"]
    #     self.Tel_Print=dbreader["config"]["Tel"]
    #     self.Comments_Print=dbreader["config"]["Comments"]
    #     self.Welcome_Print=dbreader["config"]["Welcome"]
    #     self.Addr_Print=dbreader["config"]["Addr"]
    #     self.TelPhone_Print=dbreader["config"]["TelPhone"]
    #     dbreader.close()

    #     dbreader2=shelve.open("PrintList.dat",'r')


    #     if (SearchGoods.Printer_Ready() != None):
    #         self.FormatContent(u"\n欢迎光临\n")
    #         # self.FormatContent("         ")
    #         self.FormatContent(self.Name_Print)
    #         self.FormatContent("\n\n")
    #         self.FormatContent(u"时  间:")
    #         self.FormatContent("%s" % SearchGoods.GetDetailTime())
    #         self.FormatContent("\n")
    #         self.FormatContent("********************************")
    #         self.FormatContent("\n")
    #         self.FormatContent(u"商品编号  商品名称  数量 单价\n")
    #         for item in dbreader2.items():
    #             self.FormatContent(item[1]['ID'])
    #             self.FormatContent("      ")
    #             self.FormatContent(item[1]['Name'])
    #             self.FormatContent("      ")
    #             self.FormatContent(item[1]['amount'])
    #             self.FormatContent("    ")                
    #             self.FormatContent(item[1]["Price"])
    #             self.FormatContent("\n")    
    #         self.FormatContent("\n")    
    #         self.FormatContent("********************************")
    #         self.FormatContent("\n\n")
    #         self.FormatContent(u" 总 金 额(￥) : ")
    #         self.FormatContent(self.ReturnPrices()[0])
    #         self.FormatContent("\n")
    #         self.FormatContent(u" 优    惠(￥) : ")
    #         self.FormatContent("-")
    #         self.FormatContent(self.ReturnPrices()[1])
    #         self.FormatContent("\n")
    #         self.FormatContent(u" 最终金额(￥) : ")
    #         self.FormatContent(self.ReturnPrices()[2])
    #         self.FormatContent("\n")
    #         self.FormatContent(u"电  话:")
    #         self.FormatContent(self.Tel_Print)
    #         self.FormatContent("\n")
    #         self.FormatContent(u"地  址:")
    #         self.FormatContent(self.Address_Print)
    #         self.FormatContent("\n")
    #         self.FormatContent(self.Comments_Print)
    #         self.FormatContent("\n")
    #         self.FormatContent(u"\n谢谢惠顾 欢迎下次光临！\n")
    #         self.FormatContent("\n\n\n")
    #         SearchGoods.ReminderMessageBox(u"出库成功,打印成功!")
    #     else:
    #         SearchGoods.ErrorMessageBox(u"打印失败,请检查打印机配置!")

    def Print_Querysell(self,evt):
        dbreader=shelve.open('config.dat','r')
        self.Name_Print=dbreader["config"]["Name"]
        self.Address_Print=dbreader["config"]["Address"]
        self.Tel_Print=dbreader["config"]["Tel"]
        self.Comments_Print=dbreader["config"]["Comments"]
        # self.Welcome_Print=dbreader["config"]["Welcome"]
        self.Addr_Print=dbreader["config"]["Addr"]
        self.TelPhone_Print=dbreader["config"]["TelPhone"]
        dbreader.close()
        dbreader2=shelve.open("PrintList.dat",'r')
        printer_name = win32print.GetDefaultPrinter()
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Sell Receipt", None, "RAW"))
            if(dbreader2!={}):
                try:
                    win32print.StartPagePrinter(hPrinter)
                    win32print.WritePrinter(hPrinter, self.FormatContent(u"\n欢迎光临\n"))
                    win32print.WritePrinter(hPrinter, self.FormatContent(self.Name_Print))
                    win32print.WritePrinter(hPrinter, self.FormatContent("\n\n"))
                    win32print.WritePrinter(hPrinter, self.FormatContent(u"时  间:"))
                    win32print.WritePrinter(hPrinter, self.FormatContent("%s" % SearchGoods.GetDetailTime()))
                    win32print.WritePrinter(hPrinter, self.FormatContent("\n"))
                    win32print.WritePrinter(hPrinter, self.FormatContent("*******************************"))
                    win32print.WritePrinter(hPrinter, self.FormatContent("\n"))
                    win32print.WritePrinter(hPrinter, self.FormatContent(u"商品名称    数量    单价\n"))
                    for item in dbreader2.items():
                        win32print.WritePrinter(hPrinter, self.FormatContent(item[1]['Name']))
                        win32print.WritePrinter(hPrinter, self.FormatContent("         "))
                        win32print.WritePrinter(hPrinter, self.FormatContent(item[1]['amount']))
                        win32print.WritePrinter(hPrinter, self.FormatContent("       "))     
                        win32print.WritePrinter(hPrinter, self.FormatContent(item[1]["Perprice"]))
                        win32print.WritePrinter(hPrinter, self.FormatContent("\n"))
                    win32print.WritePrinter(hPrinter, self.FormatContent("\n"))
                    win32print.WritePrinter(hPrinter, self.FormatContent("*******************************"))
                    win32print.WritePrinter(hPrinter, self.FormatContent("\n"))
                    win32print.WritePrinter(hPrinter, self.FormatContent(u"总 金 额(￥): "))
                    win32print.WritePrinter(hPrinter, self.FormatContent(self.ReturnPrices()[0]))
                    win32print.WritePrinter(hPrinter, self.FormatContent("\n"))
                    win32print.WritePrinter(hPrinter, self.FormatContent(u"优    惠(￥): "))
                    win32print.WritePrinter(hPrinter, self.FormatContent("-"))
                    win32print.WritePrinter(hPrinter, self.FormatContent(self.ReturnPrices()[1]))
                    win32print.WritePrinter(hPrinter, self.FormatContent("\n"))
                    win32print.WritePrinter(hPrinter, self.FormatContent(u"最终金额(￥): "))
                    win32print.WritePrinter(hPrinter, self.FormatContent(self.ReturnPrices()[2]))
                    win32print.WritePrinter(hPrinter, self.FormatContent("\n\n"))                    
                    win32print.WritePrinter(hPrinter, self.FormatContent("*******************************"))
                    win32print.WritePrinter(hPrinter, self.FormatContent("\n"))
                    win32print.WritePrinter(hPrinter, self.FormatContent(u"电  话:"))
                    win32print.WritePrinter(hPrinter, self.FormatContent(self.Tel_Print))
                    win32print.WritePrinter(hPrinter, self.FormatContent("\n"))
                    win32print.WritePrinter(hPrinter, self.FormatContent(u"地  址:"))
                    win32print.WritePrinter(hPrinter, self.FormatContent(self.Address_Print))
                    win32print.WritePrinter(hPrinter, self.FormatContent("\n"))
                    win32print.WritePrinter(hPrinter, self.FormatContent(self.Comments_Print))
                    win32print.WritePrinter(hPrinter, self.FormatContent("\n"))
                    win32print.WritePrinter(hPrinter, self.FormatContent(u"\n谢谢惠顾 欢迎下次光临！\n"))
                    win32print.WritePrinter(hPrinter, self.FormatContent("\n\n"))
                    win32print.EndPagePrinter(hPrinter)
                    #删除整个数据字典
                    dbwriter=shelve.open('PrintList.dat','w', writeback=True)
                    dbwriter.clear();
                    dbwriter.close();
                    #重置界面元素项
                    self.Print_Teardown();
                    SearchGoods.ReminderMessageBox(u"打印成功!")
                except:
                    SearchGoods.ReminderMessageBox(u"打印失败!")
                finally:
                    win32print.EndDocPrinter(hPrinter)
            else:
                SearchGoods.ReminderMessageBox(u"打印失败!")
        except:
            SearchGoods.ReminderMessageBox(u"获取打印机信息失败，请确保打印机正常连接，正常工作\n可参考本软件菜单帮助->打印机设置")
        finally:
            dbreader2.close()
            win32print.ClosePrinter(hPrinter)

    def FormatContent(self,raw_data):
        try:
            raw_data = raw_data.encode('gb2312');
        except:
            raw_data = raw_data;
        return raw_data;

if __name__ == '__main__':
    app = wx.App();
    frame = PrintSellPage();
    frame.Show();
    app.MainLoop();