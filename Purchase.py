#coding=utf-8;
#Author:张祖兴 iyueer@163.com

import wx;
from time import strftime;
from time import localtime;
import shelve,dbhash,anydbm;
import SearchGoods;

class PurchasePage(wx.Dialog):
    """
    This is PurchasePage.  
    """
    def __init__(self):
        wx.Dialog.__init__(self,None,-1, u"入库登记",size=(450, 450))
        self.Centre();
        self.icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon);
        P_panel = wx.Panel(self);
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(11,2,9,18)

        P_GoodsID_Label = wx.StaticText(P_panel, -1, u"商品编号 *: ");
        P_GoodsName_Label = wx.StaticText(P_panel, -1, u"商品名称 : ");
        P_GoodsColor_Label = wx.StaticText(P_panel, -1, u"商品颜色 : ");
        P_GoodsSize_S_Label = wx.StaticText(P_panel, -1, u"S码数量 : ");
        P_GoodsSize_M_Label = wx.StaticText(P_panel, -1, u"M码数量 : ");
        P_GoodsSize_L_Label = wx.StaticText(P_panel, -1, u"L码数量 : ");
        P_GoodsSize_XL_Label = wx.StaticText(P_panel, -1, u"XL码数量 : ");
        P_GoodsSize_XXL_Label = wx.StaticText(P_panel, -1, u"XXL码数量 : ");
        P_GoodsPrice_Label = wx.StaticText(P_panel, -1, u"标准吊牌价 *: ");
        P_GoodsComments_Label = wx.StaticText(P_panel, -1, u"备   注 : ");

        self.ID = wx.TextCtrl(P_panel, -1, "",style=wx.TE_RICH2);
        self.GoodsName = wx.TextCtrl(P_panel,-1,"",style=wx.TE_RICH2);
        self.Color = wx.TextCtrl(P_panel,-1,"",style=wx.TE_RICH2);
        self.S = wx.TextCtrl(P_panel,-1,"",style=wx.TE_RICH2,validator=SearchGoods.CharValidator("no-alpha"));
        self.M = wx.TextCtrl(P_panel,-1,"",style=wx.TE_RICH2,validator=SearchGoods.CharValidator("no-alpha"));
        self.L = wx.TextCtrl(P_panel,-1,"",style=wx.TE_RICH2,validator=SearchGoods.CharValidator("no-alpha"));
        self.XL = wx.TextCtrl(P_panel,-1,"",style=wx.TE_RICH2,validator=SearchGoods.CharValidator("no-alpha"));
        self.XXL = wx.TextCtrl(P_panel,-1,"",style=wx.TE_RICH2,validator=SearchGoods.CharValidator("no-alpha"));                
        self.Price = wx.TextCtrl(P_panel,-1,"",style=wx.TE_RICH2,validator=SearchGoods.CharValidator("no-alpha"));
        self.Comments = wx.TextCtrl(P_panel,-1,"",style=wx.TE_MULTILINE|wx.TE_RICH2|wx.TE_WORDWRAP);

        P_GoodsPurchase_Button = wx.Button(P_panel, 20, u"入  库");
        P_GoodsPurchaseReset_Button = wx.Button(P_panel, 30, u"重  填");

        self.Bind(wx.EVT_BUTTON,self.Submit_Purchase,id=20);
        self.Bind(wx.EVT_BUTTON,self.Reset_Purchase,id=30);

        fgs.AddMany([(P_GoodsID_Label,1,wx.EXPAND),(self.ID,1,wx.EXPAND),(P_GoodsName_Label),
                     (self.GoodsName,1,wx.EXPAND),(P_GoodsColor_Label),(self.Color,1,wx.EXPAND),
                     (P_GoodsSize_S_Label),(self.S,1,wx.EXPAND),(P_GoodsSize_M_Label),(self.M,1,wx.EXPAND),
                     (P_GoodsSize_L_Label),(self.L,1,wx.EXPAND),(P_GoodsSize_XL_Label),(self.XL,1,wx.EXPAND),
                     (P_GoodsSize_XXL_Label),(self.XXL,1,wx.EXPAND),(P_GoodsPrice_Label),(self.Price,1,wx.EXPAND),
                     (P_GoodsComments_Label),(self.Comments,1,wx.EXPAND),(P_GoodsPurchaseReset_Button),(P_GoodsPurchase_Button,1,wx.EXPAND)]);
        fgs.AddGrowableRow(9,1)
        fgs.AddGrowableCol(1,1)

        hbox.Add(fgs,proportion=1,flag=wx.ALL|wx.EXPAND,border=15);


        P_panel.SetSizer(hbox);
        P_panel.Layout();

    fieldNames = ["ID", "GoodsName", "Color", "S", "M", "L", "XL", "XXL", "Price", "Comments"];

    def Submit_Purchase(self, evt):
        # # make a dictionary of values
        fieldData = {};
        IDs=[];
        GoodsID= (getattr(self, "ID").GetValue()).encode('gb2312');
        GoodsName = (getattr(self, "GoodsName").GetValue()).encode('gb2312');                                       
        GoodsColor = (getattr(self, "Color").GetValue()).encode('gb2312');
        SizeS = (getattr(self, "S").GetValue()).encode('gb2312');
        SizeM = (getattr(self, "M").GetValue()).encode('gb2312');
        SizeL = (getattr(self, "L").GetValue()).encode('gb2312');
        SizeXL = (getattr(self, "XL").GetValue()).encode('gb2312');
        SizeXXL = (getattr(self, "XXL").GetValue()).encode('gb2312');
        GoodsPrice = (getattr(self, "Price").GetValue()).encode('gb2312');
        GoodsComments = (getattr(self,"Comments").GetValue()).encode('gb2312');
        if(SearchGoods.PurchaseJugdement(GoodsID,SizeS,SizeM,SizeL,SizeXL,SizeXXL,GoodsPrice)):
            dbreader=shelve.open('database.dat','r')
            for i in dbreader.items():
                IDs.append(i[0]);
            if GoodsID not in IDs:
                fieldData['GID'] = GoodsID;
                fieldData['GName'] = GoodsName;
                fieldData['GColor'] = GoodsColor; 
                if(len(SizeS)==1):
                    SizeS="0"+SizeS;
                if(SizeS=="" or int(SizeS)==0):
                    SizeS="0";
                if(len(SizeM)==1):
                    SizeM="0"+SizeM;
                if(SizeM=="" or int(SizeM)==0):
                    SizeM="0";
                if(len(SizeL)==1):
                    SizeL="0"+SizeL;
                if(SizeL=="" or int(SizeL)==0):
                    SizeL="0";
                if(len(SizeXL)==1):
                    SizeXL="0"+SizeXL;
                if(SizeXL=="" or int(SizeXL)==0):
                    SizeXL="0";
                if(len(SizeXXL)==1):
                    SizeXXL="0"+SizeXXL;
                if(SizeXXL=="" or int(SizeXXL)==0):
                    SizeXXL="0";
                fieldData["S"] = SizeS;
                fieldData["M"] = SizeM;
                fieldData["L"] = SizeL;
                fieldData["XL"] = SizeXL;
                fieldData["XXL"] = SizeXXL;
                fieldData['GStoreNum']=str(int(SizeS)+int(SizeM)+int(SizeL)+int(SizeXL)+int(SizeXXL));
                if(len(fieldData['GStoreNum'])==1):
                    fieldData['GStoreNum']="0"+fieldData['GStoreNum'];
                if(fieldData['GStoreNum']=="00"):
                    fieldData['GStoreNum']="0";
                fieldData['GPrice'] = GoodsPrice;
                fieldData['GComments'] = GoodsComments;
                fieldData['GStoreTime'] = strftime("%Y-%m-%d", localtime());
                dlg = wx.MessageDialog(None, u"确定要入库吗?", u'提示', wx.OK|wx.CANCEL);
                # print fieldData;
                if(int(fieldData['GStoreNum'])!=0):
                    if dlg.ShowModal() == wx.ID_OK:
                        SearchGoods.StoreRecord(str(GoodsID),fieldData);
                        SearchGoods.PurchaseMessageBox();
                    else:
                        pass;
                else:
                    SearchGoods.ReminderMessageBox(u"所有尺码商品总数为0,不能进行入库, 请输入部分尺码的数量再提交入库!");
                dlg.Destroy();
            else:
                SearchGoods.GoodsIDExistMessageBox();
        else:
            SearchGoods.PurchaseErrorMessageBox();


    def Reset_Purchase(self, evt):
        # make a dictionary of values
        for name in self.fieldNames:
            tc = getattr(self, name);
            tc.SetValue("");
    




