#coding=utf-8
#Author:张祖兴 iyueer@163.com

import wx
import SearchGoods,PrintSell
import shelve,dbhash,anydbm
# import win32print


class QuerySellPage(wx.Dialog):
    """
    This is SellPage.  
    """
    Return_ID=0

    def __init__(self, Selected_ID, Selected_Prices, Vendor):
        self.Org_price=Selected_Prices
        self.Return_ID = Selected_ID
        wx.Dialog.__init__(self, None, -1, u"商品出库登记", size=(450, 450))
        self.Centre()
        self.icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        S_panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        fgs = wx.FlexGridSizer(6,2,30,15)
        self.S_Vendor=SearchGoods.ListBox_Display()
        self.S_SizeList=SearchGoods.SizeList_Display(Selected_ID)
        # S_CountList=[u"无折扣",u"95折"]

        def GotDefaultVendor(): 
            if(str(SearchGoods.Active_Account_Name())!="None"):
                self.S_Vendor_Default=str(SearchGoods.Active_Account_Name())
            else:
                if(len(self.S_Vendor)!=0):
                    self.S_Vendor_Default=self.S_Vendor[0]
                else:
                    self.S_Vendor_Default=""
            return self.S_Vendor_Default


        S_GoodsID_Label = wx.StaticText(S_panel, -1, u"商品编号 : ")
        S_GoodsSize_Label = wx.StaticText(S_panel, -1, u"尺   码 : ")
        S_GoodsPrice_Label = wx.StaticText(S_panel, -1, u"标准吊牌价格 : ")
        S_GoodsVendor_Label = wx.StaticText(S_panel, -1, u"导 购 员: ")
        S_GoodsCount_Label = wx.StaticText(S_panel, -1, u"折扣(限两数字)")
        S_GoodsFinalPrice_Label = wx.StaticText(S_panel, -1, u"最终交易价 : ")

        self.S_GoodsIDNum_Label = wx.StaticText(S_panel, 71, u"%s"%Selected_ID)
        self.S_GoodsSize_ComboBox = wx.ComboBox(S_panel,72,"",(15,30),wx.DefaultSize,self.S_SizeList,wx.CB_DROPDOWN|wx.CB_READONLY)
        self.S_GoodsPrice2_Label = wx.StaticText(S_panel, 73, u"%s"%Selected_Prices)
        self.S_GoodsVendor_ComboBox = wx.ComboBox(S_panel,130,GotDefaultVendor(),(15,30),wx.DefaultSize,self.S_Vendor,wx.CB_DROPDOWN|wx.CB_READONLY)
        self.GoodsCount = wx.TextCtrl(S_panel,77,validator=SearchGoods.CharValidator("no-alpha"))
        #self.GoodsCount = wx.TextCtrl(S_panel,77);
        self.GoodsCount.SetMaxLength(2)
        self.S_GoodsFinalPrice_Label2 = wx.StaticText(S_panel, 76, u"%s"%Selected_Prices)

        dbreader=shelve.open('config.dat','r')
        self.PrinterEnable=int(dbreader["config"]["Enable"])
        dbreader.close()

        S_GoodsSell_Button = wx.Button(S_panel, 74, u"出  库")
        if(self.PrinterEnable==0):
            self.S_GoodsPrinter_Button = wx.Button(S_panel, 78, u"打  印")
        else:
            pass;
        S_GoodsSellReset_Button = wx.Button(S_panel, 75, u"重  填")

        self.Bind(wx.EVT_TEXT,self.WhileInputCount,id=77)
        self.Bind(wx.EVT_BUTTON,self.Submit_QuerySell,id=74)
        self.Bind(wx.EVT_BUTTON,self.Reset_QuerySell,id=75)
        self.Bind(wx.EVT_BUTTON,self.OpenPrintSell,id=78)


        fgs.AddMany([(S_GoodsID_Label,1,wx.EXPAND),(self.S_GoodsIDNum_Label,1,wx.EXPAND),
                     (S_GoodsSize_Label,1,wx.EXPAND),(self.S_GoodsSize_ComboBox,1,wx.EXPAND),
                     (S_GoodsVendor_Label,1,wx.EXPAND),(self.S_GoodsVendor_ComboBox,1,wx.EXPAND),
                     (S_GoodsPrice_Label,1,wx.EXPAND),(self.S_GoodsPrice2_Label,1,wx.EXPAND),
                     (S_GoodsCount_Label,1,wx.EXPAND),(self.GoodsCount,1,wx.EXPAND),
                     (S_GoodsFinalPrice_Label,1,wx.EXPAND),(self.S_GoodsFinalPrice_Label2,1,wx.EXPAND)])
        fgs.AddGrowableCol(1,1)

        hbox.Add(fgs,proportion=1,flag=wx.ALL|wx.EXPAND,border=15)
        hbox2.Add(S_GoodsSellReset_Button, proportion=1, border=5, flag=wx.CENTRE)
        hbox2.Add(S_GoodsSell_Button, proportion=1, border=5, flag=wx.CENTRE)
        if(self.PrinterEnable==0):
            hbox2.Add(self.S_GoodsPrinter_Button, proportion=1, border=5, flag=wx.CENTRE)
        else:
            pass;
        vbox.Add(hbox, proportion=1, border=20, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP|wx.ALL);
        vbox.Add(hbox2, proportion=1, border=20, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP|wx.ALL);

        S_panel.SetSizer(vbox)
        S_panel.Layout()
    
    def WhileInputCount(self, evt):
        try:
            GoodsCount = int((getattr(self, "GoodsCount").GetValue()).encode('gb2312'))
        except:
            GoodsCount = 0
        # GoodsID=str(int(self.Org_price*(float(GoodsID)/100)))
        if(GoodsCount!=0):
            try:
                GoodsCount=str(int(float((int(self.Org_price)*GoodsCount)/100)))
            except:
                pass
            self.S_GoodsFinalPrice_Label2.SetLabel("%s" %GoodsCount)
        else:
            self.S_GoodsFinalPrice_Label2.SetLabel("%s"%self.Org_price)

    def Submit_QuerySell(self, evt):
        GoodsID = self.Return_ID;
        GoodsName = SearchGoods.GetGoodsName(GoodsID);
        GoodsColor = SearchGoods.GetGoodsColor(GoodsID);
        GoodsSize = (getattr(self,"S_GoodsSize_ComboBox").GetStringSelection()).encode('gb2312');
        GoodsVendor = (getattr(self,"S_GoodsVendor_ComboBox").GetStringSelection()).encode('gb2312');
        GoodsPrice = str((getattr(self, "S_GoodsPrice2_Label").GetLabel()).encode('gb2312'));
        GoodsCount = (getattr(self, "GoodsCount").GetValue()).encode('gb2312');
        GoodsFinalprice = str((getattr(self, "S_GoodsFinalPrice_Label2").GetLabel()).encode('gb2312'));
        GoodsPriceGap = str(int(GoodsPrice)-int(GoodsFinalprice))
        if(GoodsVendor==""):
            GoodsVendor=str(SearchGoods.Active_Account_Name());
        if(GoodsSize==""):
            GoodsSize=self.S_SizeList[1];
        try:
            GoodsCount=int(GoodsCount);
            if(GoodsCount==0):
                GoodsCount = '''\xce\xde\xd5\xdb\xbf\xdb'''
            else:
                GoodsCount = str(GoodsCount)+"%";
        except:
            GoodsCount=100;
            GoodsCount = '''\xce\xde\xd5\xdb\xbf\xdb''';
        if(self.S_Vendor_Default!=""):
            if(SearchGoods.SellPageJudge(GoodsID, GoodsSize, GoodsVendor, GoodsPrice, GoodsFinalprice)):
                dlg = wx.MessageDialog(None, u"确定要出库吗?", u'提示', wx.OK|wx.CANCEL);
                if dlg.ShowModal() == wx.ID_OK:
                    SearchGoods.UpdatedDB(GoodsID,GoodsSize);
                    SearchGoods.SellStatement(GoodsID, GoodsName, GoodsColor, GoodsSize ,GoodsVendor,GoodsPrice,GoodsCount,GoodsFinalprice);
                    if(self.PrinterEnable==0):
                        if(self.PrintListExist(GoodsID)):
                            self.PrintListPlus(GoodsID,1,GoodsPrice,GoodsFinalprice,GoodsPriceGap);
                        else:
                            SearchGoods.SellPrintData(GoodsID, GoodsName, GoodsColor, GoodsSize ,GoodsVendor,GoodsPrice,GoodsPrice, GoodsCount,GoodsFinalprice,GoodsPriceGap,1,1);
                    else:
                        pass;                      
                    SearchGoods.SellMessageBox();
                    if(SearchGoods.DeleteEmptyDB(GoodsID)!=None):
                        self.Destroy();
                else:
                    pass;
                    dlg.Destroy();
            else:
                pass;
        else:
            SearchGoods.ReminderMessageBox(u"Admin权限只用来做软件授权管理,不做出入库操作,\n请在菜单: 管理->账户管理添加新账户后,用新账户进行出库操作!");

    def PrintListExist(self, ID):
        IDs=[]
        dbreader=shelve.open('PrintList.dat','r')
        ID=str(ID);
        for i in dbreader.items():
            IDs.append(i[0]);
        dbreader.close()
        if ID in IDs:
            return True;
        else:
            return False;

    def PrintListPlus(self, ID, amount, price, finalprice, pricegap):
        dbreader=shelve.open('PrintList.dat','r')
        ID=str(ID);
        Org_Amount=dbreader[ID]["amount"];
        Org_Price=dbreader[ID]["Price"];
        Org_PriceGap=dbreader[ID]["PriceGap"]
        Org_FinalPrice=dbreader[ID]["Finalprice"];
        New_amount=str(int(Org_Amount)+1);
        New_finalprice=str(int(Org_FinalPrice)+int(finalprice))
        New_pricegap=str(int(Org_PriceGap)+int(pricegap))
        New_price = str(int(Org_Price)+int(price))
        dbreader.close();
        dbwriter=shelve.open("PrintList.dat","w",writeback=True)
        dbwriter[ID]["amount"]=New_amount;
        dbwriter[ID]["Price"]=New_price;
        dbwriter[ID]["Finalprice"]=New_finalprice;
        dbwriter[ID]["PriceGap"]=New_pricegap;
        dbwriter.close();


    def OpenPrintSell(self, evt):
        dlg = PrintSell.PrintSellPage()
        dlg.ShowModal() 
        dlg.Destroy()
        
    def Reset_QuerySell(self, evt):
        getattr(self,"S_GoodsSize_ComboBox").SetStringSelection(self.S_SizeList[1])
        getattr(self, "S_GoodsVendor_ComboBox").SetStringSelection(self.S_Vendor_Default)
        getattr(self,"GoodsCount").SetValue("")


# if __name__ == '__main__':
#     app = wx.App();
#     frame = QuerySellPage();
#     frame.Show();
#     app.MainLoop();