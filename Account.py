# coding: UTF-8
#Author:张祖兴 iyueer@163.com

import wx;

import shelve,dbhash,anydbm;
import SearchGoods;

class AccountPage(wx.Dialog):
    """
    This is AccountManagementPage.  
    """
    def __init__(self):
        wx.Dialog.__init__(self,None,-1, u"账户管理",size=(380, 470))
        self.Centre();
        panel = wx.Panel(self);
        self.icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon);
        Account_list=SearchGoods.ListBox_Display();

        Account_Type=[u"管理员(店长)", u"导购员", ""];
        self.Account_listBox=wx.ListBox(panel,113,size=(200,200),choices=Account_list,style=wx.LB_SINGLE|wx.LB_HSCROLL|wx.LB_NEEDED_SB|wx.LB_SORT)
        AccountList_Label = wx.StaticText(panel, 114, u"      账户列表: ",style=wx.ALIGN_TOP);
        Admin_Button = wx.Button(panel, 110, u"设为管理员");
        Guide_Button = wx.Button(panel, 111, u"设为导购员");
        Remove_Button = wx.Button(panel, 115, u"删除账户");
        Creat_Button = wx.Button(panel, 117, u"清   空");
        Save_Button = wx.Button(panel, 125, u"保存新账户");
        Account_Label = wx.StaticText(panel, 118 , u"账户名(支持汉字) :",style=wx.ALIGN_BOTTOM);
        Password_Label = wx.StaticText(panel, 119, u"密码 :",style=wx.ALIGN_BOTTOM);
        PasswordAgain_Label = wx.StaticText(panel, -1, u"再次输入密码 :",style=wx.ALIGN_BOTTOM);
        AccountType_Label = wx.StaticText(panel, -1, u"权限类型 :",style=wx.ALIGN_BOTTOM);

    	self.UserName_Text = wx.TextCtrl(panel, 120, style=wx.TE_RICH2|wx.TE_PROCESS_ENTER|wx.TE_LEFT);
    	self.Password_Text =wx.TextCtrl(panel, 121, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_PASSWORD);
    	self.PasswordAgain_Text =wx.TextCtrl(panel, 122, style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_PASSWORD);
    	self.Accout_ComboBox = wx.ComboBox(panel,123,"",(15,30),wx.DefaultSize,Account_Type,wx.CB_DROPDOWN|wx.CB_READONLY);

        self.Bind(wx.EVT_BUTTON, self.SetAdmin, id = 110);
        self.Bind(wx.EVT_BUTTON, self.SetGuide, id = 111);
        self.Bind(wx.EVT_BUTTON, self.DeleteAccount, id = 115);
        self.Bind(wx.EVT_BUTTON, self.Create_Reset, id = 117);
        self.Bind(wx.EVT_BUTTON, self.SaveAccount,id=125);
        self.Bind(wx.EVT_LISTBOX, self.ModifyAccount) ###账户列表选中

        RowSizer= wx.BoxSizer(wx.HORIZONTAL);
        fgs1 = wx.FlexGridSizer(4,2,5,5)
        # fgs2 = wx.FlexGridSizer(1,3,5,5)

        RowSizer1 = wx.BoxSizer(wx.HORIZONTAL);
        RowSizer1.Add(AccountList_Label, proportion=1, border=10, flag=wx.TOP);

        RowSizer2 = wx.BoxSizer(wx.HORIZONTAL);

        ColSizer1 = wx.BoxSizer(wx.VERTICAL);
        ColSizer1.Add(self.Account_listBox, proportion=1, border=10, flag=wx.LEFT );
        ColSizer2 = wx.BoxSizer(wx.VERTICAL);
        ColSizer2.Add(Admin_Button, proportion=1, border=10, flag=wx.RIGHT)
        ColSizer2.Add(Guide_Button, proportion=1, border=10, flag=wx.RIGHT)
        ColSizer2.Add(Remove_Button, proportion=1, border=10, flag=wx.RIGHT)

        RowSizer2.Add(ColSizer1,flag=wx.LEFT, border=10);
        RowSizer2.Add(ColSizer2,flag=wx.RIGHT, border=10);

        RowSizer3 = wx.BoxSizer(wx.HORIZONTAL);
        RowSizer3.Add(Creat_Button, proportion=1, border=10, flag=wx.RIGHT);
        RowSizer3.Add(Save_Button,proportion=1, border=10, flag=wx.RIGHT);

        fgs1.AddMany([(Account_Label,1,wx.RIGHT),(self.UserName_Text,1,wx.EXPAND),(Password_Label,1,wx.RIGHT),(self.Password_Text,1,wx.EXPAND),(PasswordAgain_Label,1,wx.RIGHT),(self.PasswordAgain_Text,1,wx.EXPAND)\
        	,(AccountType_Label,1,wx.RIGHT),(self.Accout_ComboBox,1,wx.EXPAND)]);

        fgs1.AddGrowableRow(3,1)
        fgs1.AddGrowableCol(1,1)

        ColSizer = wx.BoxSizer(wx.VERTICAL);

        ColSizer.Add(RowSizer1,proportion=1,flag=wx.TOP, border=10);
        ColSizer.Add(RowSizer2,proportion=1,flag=wx.LEFT, border=10);
        ColSizer.Add(fgs1,proportion=1,flag=wx.ALL|wx.EXPAND,border=20)
        ColSizer.Add(RowSizer3,proportion=1,flag=wx.ALL|wx.EXPAND,border=5)
        panel.SetSizer(ColSizer);
        panel.Layout();
        
    def ModifyAccount(self, evt):
        try:
            Name_org=(self.Account_listBox.GetStringSelection()).encode("gb2312");
        except:
            Name_org=(self.Account_listBox.GetStringSelection()).encode("iso8859-1");
        if(self.Account_listBox.FindString(Name_org)!=-1):
            dbreader=shelve.open('Account.dat','r');
            getattr(self, "UserName_Text").SetValue("%s"%dbreader[Name_org]["Name"]);
            getattr(self, "Password_Text").SetValue("%s"%dbreader[Name_org]["Password1"]);                                       
            getattr(self, "PasswordAgain_Text").SetValue("%s"%dbreader[Name_org]["Password2"]);
            if(dbreader[Name_org]["Right"]=="222"):
                getattr(self,"Accout_ComboBox").SetStringSelection(u"导购员");
            else:
                getattr(self,"Accout_ComboBox").SetStringSelection(u'管理员(店长)');
            dbreader.close();
        else:
            pass;

    def SaveAccount(self,evt):
        try:
            Name_org=(self.Account_listBox.GetStringSelection()).encode("gb2312");
        except:
            Name_org=(self.Account_listBox.GetStringSelection()).encode("iso8859-1");
        Account_Dict={};
        try:
            Name= (getattr(self, "UserName_Text").GetValue()).encode("gb2312");
        except:
            Name= (getattr(self, "UserName_Text").GetValue()).encode("iso8859-1");
        Password1 = getattr(self, "Password_Text").GetValue();                                       
        Password2 = getattr(self, "PasswordAgain_Text").GetValue();
        Right = (getattr(self,"Accout_ComboBox").GetStringSelection()).encode("gb2312");
        if((Name!="") and (Right!="") and (Password1!="") and (Password2!="") and (Name!="admin") and (Name!="Admin")):
            if(len(Password1)>=4 or len(Password1)<=16):
                if(Password1==Password2):
                    if(Right=='''\xb5\xbc\xb9\xba\xd4\xb1''' or \
                    Right=='''\xb9\xdc\xc0\xed\xd4\xb1(\xb5\xea\xb3\xa4)'''):
                        dlg1 = wx.MessageDialog(None, u"确定要保存以上相关信息吗?", u'提示', wx.OK|wx.CANCEL);
                        if dlg1.ShowModal() == wx.ID_OK:
                            try:
                                dbwriter=shelve.open('Account.dat','w');
                            except:
                                dbwriter1=shelve.open("Account.dat","c");
                                dbwriter1.close();
                                dbwriter=shelve.open("Account.dat","w");
                            Account_Dict["Name"]=Name;
                            Account_Dict["Password1"]=Password1;
                            Account_Dict["Password2"]=Password2;
                            Account_Dict["IsActive"]="No";
                            Account_Dict["IsRecentAccount"]="No";
                            if(Right=='''\xb5\xbc\xb9\xba\xd4\xb1'''):
                                Account_Dict["Right"]="222";
                            elif(Right=='''\xb9\xdc\xc0\xed\xd4\xb1(\xb5\xea\xb3\xa4)'''):
                                Account_Dict["Right"]="111";
                            else:
                                pass;
                            dbwriter["%s"%Name]=Account_Dict;
                            SearchGoods.SaveAccountMessageBox();
                            dbwriter.close();
                            self.Reset_NoEvt();
                            self.Account_listBox.Clear();
                            for i in SearchGoods.ListBox_Display():
                                self.Account_listBox.Append("%s"%i);
                            if(self.Account_listBox.FindString(Name_org)!=-1):
                                if(Name_org!=Name):
                                    SearchGoods.DeleteAccountDB(Name_org);
                                    self.Account_listBox.Clear();
                                    for i in SearchGoods.ListBox_Display():
                                        self.Account_listBox.Append("%s"%i);
                            else:
                                pass;     
                        else:
                            pass;
                        dlg1.Destroy();
                    else:
                        SearchGoods.AccountDataErrorMessageBox();
                else:
                    SearchGoods.PasswordDidNotEqualMessageBox();
            else:
                SearchGoods.PasswordTooShortMessageBox();
        else:
            SearchGoods.EmptyValuesFoundMessageBox();
   


    def DeleteAccount(self,evt):
        try:
            Name=(self.Account_listBox.GetStringSelection()).encode("gb2312");
        except:
            Name=(self.Account_listBox.GetStringSelection()).encode("iso8859-1");
        # print Name;
        if(self.Account_listBox.FindString(Name)!=-1):
            dlg1 = wx.MessageDialog(None, u"确定要删除该账户吗?", u'提示', wx.OK|wx.CANCEL);
            if dlg1.ShowModal() == wx.ID_OK:
                SearchGoods.DeleteAccountDB(Name);
                SearchGoods.DeleteAccountMessageBox();
                self.Reset_NoEvt();
                self.Account_listBox.Clear();
                for i in SearchGoods.ListBox_Display():
                    self.Account_listBox.Append("%s"%i);
            else:
                pass;
        else:
            pass;

    def SetAdmin(self, evt):
        try:
            Name=(self.Account_listBox.GetStringSelection()).encode("gb2312");
        except:
            Name=(self.Account_listBox.GetStringSelection()).encode("iso8859-1");
        if(self.Account_listBox.FindString(Name)!=-1):
            dbwriter=shelve.open('Account.dat','w',writeback=True);
            dbreader=shelve.open('Account.dat','r');
            if(dbreader[Name]["Right"]=="111"):
                SearchGoods.AccountIsAdminAlreadyMessageBox();
            elif(dbreader[Name]["Right"]=="222"):
                dlg1 = wx.MessageDialog(None, u"确定要设置为管理员吗?", u'提示', wx.OK|wx.CANCEL);
                if dlg1.ShowModal() == wx.ID_OK:
                    dbwriter[Name]["Right"]="111";
                    SearchGoods.AccountSetAdminMessageBox();
                else:
                    pass;
            else:
                pass;
            dbreader.close();
            dbwriter.close();
            self.Account_listBox.Clear();
            for i in SearchGoods.ListBox_Display():
                self.Account_listBox.Append("%s"%i);
        else:
            pass;

    def SetGuide(self, evt):
        try:
            Name=(self.Account_listBox.GetStringSelection()).encode("gb2312");
        except:
            Name=(self.Account_listBox.GetStringSelection()).encode("iso8859-1");
        if(self.Account_listBox.FindString(Name)!=-1):
            dbwriter=shelve.open('Account.dat','w',writeback=True);
            dbreader=shelve.open('Account.dat','r');
            if(dbreader[Name]["Right"]=="222"):
                SearchGoods.AccountIsGuideAlreadyMessageBox();
            elif(dbreader[Name]["Right"]=="111"):
                dlg1 = wx.MessageDialog(None, u"确定要设置为导购员吗?", u'提示', wx.OK|wx.CANCEL);
                if dlg1.ShowModal() == wx.ID_OK:
                    dbwriter[Name]["Right"]="222";
                    SearchGoods.AccountSetGuideMessageBox();
                else:
                    pass;
            else:
                pass;
            dbreader.close();
            dbwriter.close();
            self.Account_listBox.Clear();
            for i in SearchGoods.ListBox_Display():
                self.Account_listBox.Append("%s"%i);
        else:
            pass;

    def Create_Reset(self,evt):
        getattr(self, "UserName_Text").SetValue("");
        getattr(self, "Password_Text").SetValue("");                                       
        getattr(self, "PasswordAgain_Text").SetValue("");
        getattr(self,"Accout_ComboBox").SetStringSelection("");
        for i in range(0, len(SearchGoods.ListBox_Display())):
            self.Account_listBox.Deselect(i);


    def Reset_NoEvt(self):
        getattr(self, "UserName_Text").SetValue("");
        getattr(self, "Password_Text").SetValue("");                                       
        getattr(self, "PasswordAgain_Text").SetValue("");
        getattr(self,"Accout_ComboBox").SetStringSelection("");


# if __name__ == '__main__':
#     app = wx.App();
#     frame = AccountPage();
#     frame.Show();
#     app.MainLoop();