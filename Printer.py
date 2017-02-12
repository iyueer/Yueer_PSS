#coding=utf-8;
#python

import wx;
import SearchGoods;
import shelve,dbhash,anydbm;
import win32print

class Printer_Page(wx.Dialog):
    """
    This is PrinterSettingsPage.  
    """
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, u"小票打印设置", size=(450, 450))
        self.Centre();
        self.icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon);
        S_panel = wx.Panel(self);
        Enable_list=[u"开启", u"不开启"];
        hbox = wx.BoxSizer(wx.HORIZONTAL);
        fgs = wx.FlexGridSizer(7,2,30,15);
        PrinterAble_Label = wx.StaticText(S_panel, -1, u"出库时小票\n打印功能\n是否开启? : ");
        Default_Printer_Label=wx.StaticText(S_panel,-1, u"当前默认打印机 : ");
        ShopName_Label = wx.StaticText(S_panel, -1, u"打印商家名称 : ");
        ShopAddress_Label = wx.StaticText(S_panel, -1, u"打印商家地址 : ");
        ShopTel_Label = wx.StaticText(S_panel, -1, u"打印商家电话 : ");
        ShopComments_Label = wx.StaticText(S_panel, -1, u"打印备注信息 : ");

        dbreader=shelve.open('config.dat','r');
        self.Enable=int(dbreader["config"]["Enable"]);
        self.Name=str(dbreader["config"]["Name"]);
        self.Address=str(dbreader["config"]["Address"]);
        self.Tel=str(dbreader["config"]["Tel"]);
        self.Comments=str(dbreader["config"]["Comments"]);
        dbreader.close();

        if(self.Enable==0):
            self.Enable_RadioBox = wx.RadioBox(S_panel,77,'', (150, 10), wx.DefaultSize, Enable_list,2,wx.RA_SPECIFY_COLS|wx.NO_BORDER);
            self.ShopName_Text=wx.TextCtrl(S_panel,310,"%s"%self.Name);
            self.ShopAddress_Text=wx.TextCtrl(S_panel,311,"%s"%self.Address);
            self.ShopTel_Text=wx.TextCtrl(S_panel,312,"%s"%self.Tel);
            self.ShopComments_Text=wx.TextCtrl(S_panel,313,"%s"%self.Comments);
        else:
            self.Enable_RadioBox = wx.RadioBox(S_panel,77,'', (150, 10), wx.DefaultSize, Enable_list,2,wx.RA_SPECIFY_COLS|wx.NO_BORDER);
            self.Enable_RadioBox.SetSelection(1);
            self.ShopName_Text=wx.TextCtrl(S_panel,310);
            self.ShopAddress_Text=wx.TextCtrl(S_panel,311);
            self.ShopTel_Text=wx.TextCtrl(S_panel,312);
            self.ShopComments_Text=wx.TextCtrl(S_panel,313);
        try:
            printer_name = win32print.GetDefaultPrinter();
        except:
            printer_name = u"未检测到可用打印机!"
        Default_Printer_Label2=wx.StaticText(S_panel,-1, "%s"%printer_name)
        PrinterSave_Button = wx.Button(S_panel, 314, u"保存");
        PrinterCancel_Button = wx.Button(S_panel, 315, u"取消更改");
        self.Bind(wx.EVT_BUTTON,self.CancelPrinter,id=315);
        self.Bind(wx.EVT_BUTTON,self.SavePrinter,id=314);
        self.Bind(wx.EVT_RADIOBOX, self.ModifyPrinter) ###开启/不开启选中

        fgs.AddMany([(PrinterAble_Label,1,wx.EXPAND),(self.Enable_RadioBox,1,wx.EXPAND),
                     (Default_Printer_Label,1,wx.EXPAND),(Default_Printer_Label2,1,wx.EXPAND),
                     (ShopName_Label,1,wx.EXPAND),(self.ShopName_Text,1,wx.EXPAND),
                     (ShopAddress_Label,1,wx.EXPAND),(self.ShopAddress_Text,1,wx.EXPAND),
                     (ShopTel_Label,1,wx.EXPAND),(self.ShopTel_Text,1,wx.EXPAND),
                     (ShopComments_Label,1,wx.EXPAND),(self.ShopComments_Text,1,wx.EXPAND),
                     (PrinterCancel_Button,1,wx.EXPAND),(PrinterSave_Button,1,wx.EXPAND)]);
        fgs.AddGrowableCol(1,1)
        hbox.Add(fgs,proportion=1,flag=wx.ALL|wx.EXPAND,border=15);
        S_panel.SetSizer(hbox);
        S_panel.Layout();

    def ModifyPrinter(self, evt):
        Printer_Enable=self.Enable_RadioBox.GetSelection();
        if(int(Printer_Enable)==1):
            self.ShopName_Text.Clear();
            self.ShopAddress_Text.Clear();
            self.ShopTel_Text.Clear();
            self.ShopComments_Text.Clear();
        else:
            getattr(self, "ShopName_Text").SetValue("%s"%self.Name)                                    
            getattr(self, "ShopAddress_Text").SetValue("%s"%self.Address) 
            getattr(self, "ShopTel_Text").SetValue("%s"%self.Tel) 
            getattr(self, "ShopComments_Text").SetValue("%s"%self.Comments) 

    def SavePrinter(self, evt):
        Printer_Dict={};
        Printer_Enable=self.Enable_RadioBox.GetSelection();
        # print Printer_Enable;
        try:
            ShopName= (getattr(self, "ShopName_Text").GetValue()).encode("gb2312");
        except:
            ShopName= (getattr(self, "ShopName_Text").GetValue()).encode("iso8859-1");
        try:
            ShopAddress= (getattr(self, "ShopAddress_Text").GetValue()).encode("gb2312");
        except:
            ShopAddress= (getattr(self, "ShopAddress_Text").GetValue()).encode("iso8859-1");
        try:
            ShopTel= (getattr(self, "ShopTel_Text").GetValue()).encode("gb2312");
        except:
            ShopTel= (getattr(self, "ShopTel_Text").GetValue()).encode("iso8859-1");
        try:
            ShopComments= (getattr(self, "ShopComments_Text").GetValue()).encode("gb2312");
        except:
            ShopComments= (getattr(self, "ShopComments_Text").GetValue()).encode("iso8859-1");
        if(int(Printer_Enable)==0):
            if((ShopName!="") and (ShopAddress!="")):
                try:
                    dbwriter=shelve.open('config.dat','w',writeback=True);
                except:
                    dbwriter1=shelve.open("config.dat","c");
                    dbwriter1.close();
                    dbwriter=shelve.open("config.dat","w",writeback=True);
                Printer_Dict["Enable"]=0;
                print Printer_Dict["Enable"];
                Printer_Dict["Name"]=ShopName;
                Printer_Dict["Address"]=ShopAddress;
                Printer_Dict["Tel"]=ShopTel;
                Printer_Dict["Comments"]=ShopComments;
                Printer_Dict["Welcome"]=u"欢迎光临";
                Printer_Dict["Addr"]=u"地址";
                Printer_Dict["TelPhone"]=u"电话"               
                dbwriter["config"]=Printer_Dict;
                dbwriter.close();
                SearchGoods.ReminderMessageBox(u"已保存!");
                self.Close();
            else:
                SearchGoods.ErrorMessageBox(u"商家名称,商家地址不可为空, 请再次填写!");   
        else:
            dbwriter2=shelve.open('config.dat','w',writeback=True);
            dbwriter2["config"]["Enable"]=1;
            dbwriter2.close();
            self.Close();

    def CancelPrinter(self, evt):
        self.Close();

if __name__ == '__main__':
    app = wx.App();
    frame = Printer_Page();
    frame.Show();
    app.MainLoop();