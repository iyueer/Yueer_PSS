#coding=utf-8;
#Author:张祖兴 iyueer@163.com

import wx;
from time import strftime,localtime;
import shelve,dbhash,anydbm;
import SearchGoods;



class ModifyPage(wx.Dialog):
    """
    This is ModifyPage.  
    """
    def __init__(self):
        wx.Dialog.__init__(self,None,-1, u"二次入库修改登记",size=(450, 450))
        self.Centre();
        self.icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon);
        M_panel = wx.Panel(self);
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(11,2,9,18)

        M_GoodsID_Label = wx.StaticText(M_panel, -1, u"商品编号 [保持一致] *: ");
        M_GoodsName_Label = wx.StaticText(M_panel, -1, u"商品名称 [可修改] : ");
        M_GoodsColor_Label = wx.StaticText(M_panel, -1, u"商品颜色 [可修改] : ");
        M_GoodsSize_S_Label = wx.StaticText(M_panel, -1, u"S码数量 [可增加] : ");
        M_GoodsSize_M_Label = wx.StaticText(M_panel, -1, u"M码数量 [可增加] : ");
        M_GoodsSize_L_Label = wx.StaticText(M_panel, -1, u"L码数量 [可增加] : ");
        M_GoodsSize_XL_Label = wx.StaticText(M_panel, -1, u"XL码数量 [可增加]  : ");
        M_GoodsSize_XXL_Label = wx.StaticText(M_panel, -1, u"XXL码数量 [可增加]  : ");
        M_GoodsPrice_Label = wx.StaticText(M_panel, -1, u"标准吊牌价 [可修改]  : ");
        M_GoodsComments_Label = wx.StaticText(M_panel, -1, u"备注 [可修改] : ");

        self.ID = wx.TextCtrl(M_panel, -1, "",style=wx.TE_RICH2);
        self.GoodsName = wx.TextCtrl(M_panel,-1,"",style=wx.TE_RICH2);
        self.Color = wx.TextCtrl(M_panel,-1,"",style=wx.TE_RICH2);
        self.S = wx.TextCtrl(M_panel,-1,"",style=wx.TE_RICH2,validator=SearchGoods.CharValidator("no-alpha"));
        self.M = wx.TextCtrl(M_panel,-1,"",style=wx.TE_RICH2,validator=SearchGoods.CharValidator("no-alpha"));
        self.L = wx.TextCtrl(M_panel,-1,"",style=wx.TE_RICH2,validator=SearchGoods.CharValidator("no-alpha"));
        self.XL = wx.TextCtrl(M_panel,-1,"",style=wx.TE_RICH2,validator=SearchGoods.CharValidator("no-alpha"));
        self.XXL = wx.TextCtrl(M_panel,-1,"",style=wx.TE_RICH2,validator=SearchGoods.CharValidator("no-alpha"));                
        self.Price = wx.TextCtrl(M_panel,-1,"",style=wx.TE_RICH2,validator=SearchGoods.CharValidator("no-alpha"));
        self.Comments = wx.TextCtrl(M_panel,-1,"",style=wx.TE_RICH2);

        M_GoodsModify_Button = wx.Button(M_panel, 20, u"更  新");
        M_GoodsModifyReset_Button = wx.Button(M_panel, 30, u"重  填");

        self.Bind(wx.EVT_BUTTON,self.Submit_Modify,id=20);
        self.Bind(wx.EVT_BUTTON,self.Reset_Modify,id=30);

        fgs.AddMany([(M_GoodsID_Label,1,wx.EXPAND),(self.ID,1,wx.EXPAND),(M_GoodsName_Label),
                     (self.GoodsName,1,wx.EXPAND),(M_GoodsColor_Label),(self.Color,1,wx.EXPAND),
                     (M_GoodsSize_S_Label),(self.S,1,wx.EXPAND),(M_GoodsSize_M_Label),(self.M,1,wx.EXPAND),
                     (M_GoodsSize_L_Label),(self.L,1,wx.EXPAND),(M_GoodsSize_XL_Label),(self.XL,1,wx.EXPAND),
                     (M_GoodsSize_XXL_Label),(self.XXL,1,wx.EXPAND),(M_GoodsPrice_Label),(self.Price,1,wx.EXPAND),
                     (M_GoodsComments_Label),(self.Comments,1,wx.EXPAND),(M_GoodsModifyReset_Button),(M_GoodsModify_Button,1,wx.EXPAND)]);
        fgs.AddGrowableRow(9,1)
        fgs.AddGrowableCol(1,1)

        hbox.Add(fgs,proportion=1,flag=wx.ALL|wx.EXPAND,border=15);
        M_panel.SetSizer(hbox);
        M_panel.Layout();

    fieldNames = ["ID", "GoodsName", "Color", "S", "M", "L", "XL", "XXL", "Price", "Comments"];

    def Submit_Modify(self, evt):
        fieldData = {};
        IDs=[];
        GoodsID= (getattr(self, "ID").GetValue()).encode('gb2312');
        # print GoodsID;
        GoodsName = (getattr(self, "GoodsName").GetValue()).encode('gb2312');   
        # print GoodsName;                                    
        GoodsColor = (getattr(self, "Color").GetValue()).encode('gb2312');
        SizeS = (getattr(self, "S").GetValue()).encode('gb2312');
        SizeM = (getattr(self, "M").GetValue()).encode('gb2312');
        SizeL = (getattr(self, "L").GetValue()).encode('gb2312');
        SizeXL = (getattr(self, "XL").GetValue()).encode('gb2312');
        SizeXXL = (getattr(self, "XXL").GetValue()).encode('gb2312');
        GoodsPrice = (getattr(self, "Price").GetValue()).encode('gb2312');
        GoodsComments = (getattr(self,"Comments").GetValue()).encode('gb2312');
        # print GoodsComments;
        if(SearchGoods.ModifyJugdement(GoodsID,SizeS,SizeM,SizeL,SizeXL,SizeXXL,GoodsPrice)):
            dbreader=shelve.open('database.dat','r')
            for i in dbreader.items():
                IDs.append(i[0]);
            if GoodsID in IDs:
                # print dbreader[GoodsID];
                fieldData['GID'] = GoodsID;
                # print fieldData['''\xc9\xcc\xc6\xb7\xb1\xe0\xba\xc5''']; 
                if(GoodsName!=""):
                    fieldData['GName'] = GoodsName;
                else:
                    fieldData['GName'] = dbreader[GoodsID]['GName'];
                # print fieldData['''\xc9\xcc\xc6\xb7\xc3\xfb\xb3\xc6'''];
                if(GoodsColor!=""):
                    fieldData['GColor'] = GoodsColor;
                else:
                    fieldData['GColor'] = dbreader[GoodsID]['GColor'];
                # print fieldData['''\xd1\xd5\xc9\xab'''];
                if(SizeS==""):
                    fieldData["S"]=dbreader[GoodsID]["S"];
                else:
                    fieldData["S"]=str(int(SizeS)+int(dbreader[GoodsID]["S"]));

                # print fieldData["S"];
                if(SizeM==""):
                    fieldData["M"]=dbreader[GoodsID]["M"];
                else:
                    fieldData["M"]=str(int(SizeM)+int(dbreader[GoodsID]["M"]));
                # print fieldData["M"];
                if(SizeL==""):
                    fieldData["L"]=dbreader[GoodsID]["L"];
                else:
                    fieldData["L"]=str(int(SizeL)+int(dbreader[GoodsID]["L"]));
                # print fieldData["L"];
                if(SizeXL==""):
                    fieldData["XL"]=dbreader[GoodsID]["XL"];
                else:
                    fieldData["XL"]=str(int(SizeXL)+int(dbreader[GoodsID]["XL"]));
                # print fieldData["XL"];
                if(SizeXXL==""):
                    fieldData["XXL"]=dbreader[GoodsID]["XXL"];
                else:
                    fieldData["XXL"]=str(int(SizeXXL)+int(dbreader[GoodsID]["XXL"]));
                if(len(fieldData["S"])==1):
                    fieldData["S"]="0"+fieldData["S"];
                if(int(fieldData["S"])==0):
                    fieldData["S"]="0"
                if(len(fieldData["M"])==1):
                    fieldData["M"]="0"+fieldData["M"];
                if(int(fieldData["M"])==0):
                    fieldData["M"]="0"
                if(len(fieldData["L"])==1):
                    fieldData["L"]="0"+fieldData["L"];
                if(int(fieldData["L"])==0):
                    fieldData["L"]="0"
                if(len(fieldData["XL"])==1):
                    fieldData["XL"]="0"+fieldData["XL"];
                if(int(fieldData["XL"])==0):
                    fieldData["XL"]="0"
                if(len(fieldData["XXL"])==1):
                    fieldData["XXL"]="0"+fieldData["XXL"];
                if(int(fieldData["XXL"])==0):
                    fieldData["XXL"]="0"
                # print fieldData["XXL"];
                fieldData['GStoreNum']=str(int(fieldData["S"])+int(fieldData["M"])+int(fieldData["L"])+int(fieldData["XL"])+int(fieldData["XXL"]));
                if(len(fieldData['GStoreNum'])==1):
                    fieldData['GStoreNum']="0"+fieldData['GStoreNum'];
                if(int(fieldData['GStoreNum'])==0):
                    fieldData['GStoreNum']="0";
                if(GoodsPrice!=""):
                    fieldData['GPrice'] = GoodsPrice;
                else:
                    fieldData['GPrice'] = dbreader[GoodsID]['GPrice'];
                if(GoodsComments!=""):
                    fieldData['GComments'] = GoodsComments;
                else:
                    fieldData['GComments'] = dbreader[GoodsID]['GComments'];
                fieldData['GStoreTime'] = strftime("%Y-%m-%d", localtime());
                # print fieldData;
                dlg = wx.MessageDialog(None, u"确定要更新以上商品信息吗?", u'提示', wx.OK|wx.CANCEL);
                if dlg.ShowModal() == wx.ID_OK:
                    SearchGoods.StoreRecord(str(GoodsID),fieldData);
                    SearchGoods.ModifyMessageBox();
                else:
                    pass;
                dlg.Destroy();
            else:
                SearchGoods.NoThisDataMessageBox();
            dbreader.close();
        else:
            SearchGoods.ModifyErrorMessageBox();


    def Reset_Modify(self, evt):
        for name in self.fieldNames:
            tc = getattr(self, name);
            tc.SetValue("");
    




