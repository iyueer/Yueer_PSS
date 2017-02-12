#coding=utf-8;
import wx;
from wx.html import HtmlWindow;

class AboutPage(wx.Dialog):
    text = u'''
    <html>
    <body bgcolor="#ECFFFF">
    <p><b>Yueer服装类出入库系统高级版</b></p>
    <p>版本号: V1.2</p>
    <p>All Copyright Reserved @张祖兴</p>
    <p>本软件只可供指定服装店使用.</p>
    <p>任何非经授权的使用,窃取,复制,
    都是违反知识产权法的行为, 
    如需使用,请购买正版版权,
    联系方式:iyueer@163.com</p>
    </body>
    </html>
    '''

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, u'关于软件',
                          size=(300, 300) )

        html = HtmlWindow(self)
        html.SetPage(self.text);
        self.Centre();
        self.icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO);
        self.SetIcon(self.icon);
        button = wx.Button(self, wx.ID_OK, u"已知晓")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()


class HelpPage(wx.Dialog):
    text2 = u'''
    <html>
    <body bgcolor="#ECFFFF">
    <p><b>1.导入模板</b></p>
    <p>本软件已经准备好了导入模板,下图就是三个导入模板的模板文件示范, 
    这三个模板文件一般可以在C:\Program Files\Yueer_PSS\Backup目录下找到:</p></br>
    <img src="Template.png">
    <p><b>2.导入帮助</b></p>
    <p>本软件支持office excel 2003~2013版本,即.xls, xlsx的导入.
    也支持csv导入, csv文件内容格式较Excel比较简单, 更不会出错,所以更推荐csv导入.</p>
    <p>下图介绍了一些导入技巧:</p>
    <img src="import.png">
    <br>
    <p><b>3.自动备份功能介绍</b></p>
    <p>本软件版本支持自动备份功能.
    每次软件关闭后都会在Backup文件夹内生成一个最新的以当天日期命名的.xls文件.
    如果程序出问题了,还可以到C:\Program Files\Yueer_PSS\Backup(取决于你的安装目录)
    找回最新的数据备份, 然后还可以通过Excel导入导入到软件中去.</p>
    <img src="Backup.png">
    </p>
    </body>
    </html>
    '''

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, u'软件帮助',
                          size=(550, 495))

        html = HtmlWindow(self)
        html.SetPage(self.text2);
        self.Centre();
        self.icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO);
        self.SetIcon(self.icon);
        button = wx.Button(self, wx.ID_OK, u"已知晓")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()