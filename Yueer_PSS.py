# coding: UTF-8
#Author:张祖兴 iyueer@163.com

import wx;
import Main;
import SearchGoods;
import shelve,dbhash,anydbm;

class loginFrame(wx.Dialog):
    """
    This is Login in Frame.
    """
    def __init__(self):
    	wx.Dialog.__init__(self, None, -1, u"Yueer服装类出入库系统登陆", size=(250, 180))
    	self.Centre();
    	self.icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
    	self.SetIcon(self.icon);
    	panel = wx.Panel(self);
        self.Last_Account=SearchGoods.Recent_Login_Account_Name();
        if(self.Last_Account!=None):
            self.defaultValue=str(self.Last_Account);
        else:
            self.defaultValue="";


    	UserName_Label = wx.StaticText(panel, -1, u"用户名: ",style=wx.ALIGN_BOTTOM);
    	self.UserName_Text = wx.TextCtrl(panel, 6, value=self.defaultValue,size=(28,28),style=wx.TE_RICH2|wx.TE_LEFT);
    	Password_Label = wx.StaticText(panel, -1, u"密  码:", style=wx.ALIGN_BOTTOM);
    	self.Password_Text =wx.TextCtrl(panel, 5, size=(28,28), style=wx.TE_PROCESS_ENTER|wx.TE_LEFT|wx.TE_PASSWORD);

    	hbox = wx.BoxSizer(wx.HORIZONTAL)
    	fgs = wx.FlexGridSizer(2,2,5,5)

        Login_Button = wx.Button(panel, 100, u"登  录", size=(20,20));
        fgs.AddMany([(UserName_Label,1,wx.RIGHT),(self.UserName_Text,1,wx.EXPAND),(Password_Label),(self.Password_Text,1,wx.EXPAND)])
        fgs.AddGrowableRow(1,1)
        fgs.AddGrowableCol(1,1)

        vbox=wx.BoxSizer(wx.VERTICAL)
        hbox.Add(fgs,proportion=1,flag=wx.ALL|wx.EXPAND,border=10);
        
        vbox.Add(hbox,proportion=1,flag=wx.ALL|wx.EXPAND,border=10)
        vbox.Add(Login_Button,proportion=1,flag=wx.ALL|wx.EXPAND,border=10);

        self.Bind(wx.EVT_BUTTON, self.Login, id=100);
        self.Bind(wx.EVT_TEXT_ENTER, self.Login, id=5)

        panel.SetSizer(vbox);
        panel.Layout();

    def Login(self, evt):
        Name= (getattr(self, "UserName_Text").GetValue()).encode("gb2312");
        Password = getattr(self, "Password_Text").GetValue();
        dbreader=shelve.open('Account.dat','r');
        dbwriter=shelve.open('Account.dat','w', writeback=True);
        if(Name!=""):
            if(Password!=""):
                if(Name in SearchGoods.ListBox_Display_withAdmin()):
                    if(Password==dbreader[Name]["Password1"]):
                        if(dbreader[Name]["Right"]=="111"):
                            if(self.Last_Account!=None):
                                if(Name!=self.Last_Account):
                                    dbwriter[self.Last_Account]["IsRecentAccount"]="No";
                                    dbwriter[Name]["IsRecentAccount"]="Yes";
                                else:
                                    pass;
                            else:
                                dbwriter[Name]["IsRecentAccount"]="Yes";
                            dbwriter[Name]["IsActive"]="Yes";
                            dbwriter.close();
                            dbreader.close();
                            self.Destroy()
                            app2 = wx.App();
                            Name=Name.decode("gb2312");
                            frame = Main.MyFrame(None, u"Yueer服装类出入库系统--店长: "+Name, "111");
                            frame.Show();
                            app2.MainLoop();

                        else:
                            if(self.Last_Account!=None):
                                if(Name!=self.Last_Account):
                                    dbwriter[self.Last_Account]["IsRecentAccount"]="No";
                                    dbwriter[Name]["IsRecentAccount"]="Yes";
                                else:
                                    pass;
                            else:
                                dbwriter[Name]["IsRecentAccount"]="Yes";
                            dbwriter[Name]["IsActive"]="Yes"; 
                            dbwriter.close();
                            dbreader.close();
                            self.Destroy()
                            app2 = wx.App();                       
                            Name=Name.decode("gb2312");
                            frame = Main.MyFrame(None, u"Yueer服装类出入库系统-导购员: "+Name, "222");
                            frame.Show();
                            app2.MainLoop();

                    else:
                        SearchGoods.WrongPasswordMessageBox();
                else:
                    SearchGoods.WrongUsernameMessageBox();
            else:
                SearchGoods.InputPasswordMessageBox();
        else:
            SearchGoods.InputUsernameMessageBox();
                       
if __name__ == '__main__':
    app = wx.App();
    frame = loginFrame();
    frame.Show();
    app.MainLoop();

        