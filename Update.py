#coding=utf-8;
#Author:张祖兴 iyueer@163.com

import wx;
# from time import strftime,localtime;
import shelve,dbhash,anydbm;
import SearchGoods;

class UpdatePage(wx.Dialog):
    """
    This is UpdatePage.  
    """
    Return_ID="";
    NameData="";
    ColorData="";
    SData="";
    MData="";
    LData="";
    XLData="";
    XXLData="";
    PriceData="";
    CommentData="";
    def __init__(self, Selected_ID):
        self.Return_ID=Selected_ID;
        wx.Dialog.__init__(self,None,-1, u"编辑修改商品信息",size=(450, 450))
        self.Centre();
        self.icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon);
        self.U_panel = wx.Panel(self);
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(11,2,9,18)

        U_GoodsID_Label = wx.StaticText(self.U_panel, -1, u"商品编号 : ");
        U_GoodsName_Label = wx.StaticText(self.U_panel, -1, u"商品名称 : ");
        U_GoodsColor_Label = wx.StaticText(self.U_panel, -1, u"商品颜色 : ");
        U_GoodsSize_S_Label = wx.StaticText(self.U_panel, -1, u"S码数量 : ");
        U_GoodsSize_U_Label = wx.StaticText(self.U_panel, -1, u"M码数量 : ");
        U_GoodsSize_L_Label = wx.StaticText(self.U_panel, -1, u"L码数量 : ");
        U_GoodsSize_XL_Label = wx.StaticText(self.U_panel, -1, u"XL码数量  : ");
        U_GoodsSize_XXL_Label = wx.StaticText(self.U_panel, -1, u"XXL码数量  : ");
        U_GoodsPrice_Label = wx.StaticText(self.U_panel, -1, u"标准吊牌价 : ");
        U_GoodsComments_Label = wx.StaticText(self.U_panel, -1, u"备注 : ");

        dbreader=shelve.open('database.dat','r');
        # print dbreader["%s"%Selected_ID];
        self.NameData=dbreader["%s"%Selected_ID]['GName'];
        self.ColorData=dbreader["%s"%Selected_ID]['GColor'];
        self.SData=str(int(dbreader["%s"%Selected_ID]["S"]));
        self.MData=str(int(dbreader["%s"%Selected_ID]["M"]));
        self.LData=str(int(dbreader["%s"%Selected_ID]["L"]));
        self.XLData=str(int(dbreader["%s"%Selected_ID]["XL"]));
        self.XXLData=str(int(dbreader["%s"%Selected_ID]["XXL"]));
        self.PriceData=dbreader["%s"%Selected_ID]['GPrice'];
        self.CommentData=dbreader["%s"%Selected_ID]['GComments'];
        self.TimeData=dbreader["%s"%Selected_ID]['GStoreTime'];

        self.U_GoodsSelectedID_Label = wx.StaticText(self.U_panel, -1, "%s"%Selected_ID);
        self.GoodsName = wx.TextCtrl(self.U_panel,-1,"%s"%self.NameData);
        self.Color = wx.TextCtrl(self.U_panel,-1,"%s"%self.ColorData);
        self.S = wx.TextCtrl(self.U_panel,-1,"%s"%self.SData,validator=SearchGoods.CharValidator("no-alpha"));
        self.M = wx.TextCtrl(self.U_panel,-1,"%s"%self.MData,validator=SearchGoods.CharValidator("no-alpha"));
        self.L = wx.TextCtrl(self.U_panel,-1,"%s"%self.LData,validator=SearchGoods.CharValidator("no-alpha"));
        self.XL = wx.TextCtrl(self.U_panel,-1,"%s"%self.XLData,validator=SearchGoods.CharValidator("no-alpha"));
        self.XXL = wx.TextCtrl(self.U_panel,-1,"%s"%self.XXLData,validator=SearchGoods.CharValidator("no-alpha"));                
        self.Price = wx.TextCtrl(self.U_panel,-1,"%s"%self.PriceData,validator=SearchGoods.CharValidator("no-alpha"));
        self.Comments = wx.TextCtrl(self.U_panel,-1,"%s"%self.CommentData);


        U_GoodsUpdate_Button = wx.Button(self.U_panel, 60, u"修  改");
        U_GoodsUpdateReset_Button = wx.Button(self.U_panel, 70, u"重  填");

        self.Bind(wx.EVT_BUTTON,self.Submit_Update,id=60);
        self.Bind(wx.EVT_BUTTON,self.Reset_Update,id=70);

        fgs.AddMany([(U_GoodsID_Label,1,wx.EXPAND),(self.U_GoodsSelectedID_Label,1,wx.EXPAND),(U_GoodsName_Label),
                     (self.GoodsName,1,wx.EXPAND),(U_GoodsColor_Label),(self.Color,1,wx.EXPAND),
                     (U_GoodsSize_S_Label),(self.S,1,wx.EXPAND),(U_GoodsSize_U_Label),(self.M,1,wx.EXPAND),
                     (U_GoodsSize_L_Label),(self.L,1,wx.EXPAND),(U_GoodsSize_XL_Label),(self.XL,1,wx.EXPAND),
                     (U_GoodsSize_XXL_Label),(self.XXL,1,wx.EXPAND),(U_GoodsPrice_Label),(self.Price,1,wx.EXPAND),
                     (U_GoodsComments_Label),(self.Comments,1,wx.EXPAND),(U_GoodsUpdateReset_Button),(U_GoodsUpdate_Button,1,wx.EXPAND)]);
        fgs.AddGrowableRow(9,1)
        fgs.AddGrowableCol(1,1)

        hbox.Add(fgs,proportion=1,flag=wx.ALL|wx.EXPAND,border=15);
        self.U_panel.SetSizer(hbox);
        self.U_panel.Layout();
        dbreader.close();

    fieldNames = ["GoodsName", "Color", "S", "M", "L", "XL", "XXL", "Price", "Comments"];

    def Submit_Update(self, evt):
        # # make a dictionary of values
        fieldData = {};
        IDs=[];
        GoodsID=self.Return_ID ;
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
            fieldData['GStoreTime'] = self.TimeData;
            dlg = wx.MessageDialog(None, u"确定要修改以上商品信息吗?", u'提示', wx.OK|wx.CANCEL);
            # print fieldData;
            if(int(fieldData['GStoreNum'])!=0):
	            if dlg.ShowModal() == wx.ID_OK:
	            	SearchGoods.StoreRecord(str(GoodsID),fieldData);
	            	SearchGoods.UpdateMessageBox();
	            	dlg.Destroy();
	            	self.Close();
	            else:
	            	pass;
            else:
                SearchGoods.ReminderMessageBox(u"所有尺码商品总数为0,不能进行入库, 请输入部分尺码的数量再提交入库!");
        else:
            SearchGoods.UpdateErrorMessageBox();

    def Reset_Update(self, evt):
        getattr(self, "GoodsName").SetValue("%s"%self.NameData)                                    
        getattr(self, "Color").SetValue("%s"%self.ColorData) 
        getattr(self, "S").SetValue("%s"%self.SData) 
        getattr(self, "M").SetValue("%s"%self.MData) 
        getattr(self, "L").SetValue("%s"%self.LData) 
        getattr(self, "XL").SetValue("%s"%self.XLData) 
        getattr(self, "XXL").SetValue("%s"%self.XXLData) 
        getattr(self, "Price").SetValue("%s"%self.PriceData) 
        getattr(self,"Comments").SetValue("%s"%self.CommentData) 

