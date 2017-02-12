#coding=utf-8;

class AboutPage(wx.Dialog):
    text = u'''
    <html>
    <body bgcolor="#ECFFFF">
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
