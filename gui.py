import wx
from wx.adv import TaskBarIcon as TaskBarIcon
from main import AutoSaver
import configparser

config_file = "config.ini"

class MyTaskBarIcon(TaskBarIcon):
    def __init__(self, frame):
        TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(wx.Icon('./images/bitmaps/aegeanki.png', wx.BITMAP_TYPE_PNG), 'Screenshot Autosaver')
        self.Bind(wx.EVT_MENU, self.taskBarActivate, id=1)
        self.Bind(wx.EVT_MENU, self.taskBarClose, id=2)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(1, 'Show')
        menu.Append(2, 'Quit')
        return menu

    def taskBarClose(self, event):
        self.frame.destroy()

    def taskBarActivate(self, event):
        if self.frame.IsShown():
            return
        self.frame.Raise()
        self.frame.ShowWithEffect(wx.SHOW_EFFECT_EXPAND,timeout=0)

    def taskBarDeactivate(self, event):
        if not self.frame.IsShown():
            return
        
        self.frame.Hide()

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, (-1, -1), (290, 280))
        self.SetIcon(wx.Icon('./images/icons/icon_wxWidgets.ico', wx.BITMAP_TYPE_ICO))
        self.SetSize((350, 250))
        self.tskic = MyTaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.hide)
        self.Centre()

        self.config_parser = configparser.ConfigParser()
        self.autosaver = AutoSaver()
        self.autosaver.run()


        # initializing the UI
        self.main_panel = wx.Panel(self,-1)
        # add sizer
        sizer = wx.GridBagSizer(5,5)

        # Text box showing what the app is doing
        box = wx.StaticBox(self.main_panel,wx.ID_ANY,"介紹")
        intro = wx.StaticText(box,wx.ID_ANY,"將使用 Windows鍵 + Shift + S 截取的圖案\
自動儲存到所選取的資料夾位置。\n\n\
關閉視窗時仍會自動執行，\n如需關閉請到工作列中選Quit將其關閉。",
                                style=wx.LEFT)
        intro.Wrap(300)
        sizer.Add(box, pos=(0, 0), 
                        span =(3,5),
                        flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.EXPAND, 
                        border=5)


        # showing target directory text and button
        self.target_dir_text = wx.TextCtrl(self.main_panel,-1,
                                            value="",
                                            style=wx.TE_READONLY)
        self.update_directory_list()
        sizer.Add(self.target_dir_text,pos=(4,0),
                                        span=(1,4),
                                        flag=wx.LEFT|wx.BOTTOM|wx.EXPAND, 
                                        border=15)

        self.update_btn = wx.Button(self.main_panel,-1,
                                    label="Change")
        sizer.Add(self.update_btn,pos=(4,4),
                                flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,
                                border=15)
        self.Bind(wx.EVT_BUTTON, self.click)

        # set sizers
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(2)
        self.main_panel.SetSizer(sizer)

        self.Show()

    def get_target_directory(self):
        self.config_parser.read(config_file, encoding="utf-8")
        config = dict(self.config_parser.items("DEFAULT"))
        return config["target_directory"]

    def update_directory_list(self):
        target_directory = self.get_target_directory()
        self.target_dir_text.SetValue(target_directory)

    def hide(self, event):
        self.Hide()

    def destroy(self):
        self.autosaver.stop()
        self.tskic.Destroy()
        self.Destroy()

    def click(self, event):
        dlg = wx.DirDialog (None, "Choose input directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.config_parser.set("DEFAULT", "target_directory", dlg.GetPath())
            with open(config_file, 'w+') as f:
                self.config_parser.write(f)
        dlg.Destroy()
        self.update_directory_list()


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'Screenshot autosaver')
        frame.Show(True)
        self.SetTopWindow(frame)
        
        return True

app = MyApp()
app.MainLoop()