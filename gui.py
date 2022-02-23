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
        menu.Append(2, 'Close')
        return menu

    def taskBarClose(self, event):
        self.frame.destroy()

    def taskBarActivate(self, event):
        if self.frame.IsShown():
            return
        
        self.frame.Show()

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

        self.choices = wx.Choice(wx.Panel(self,-1), -1, pos=(20,20))
        self.update_directory_list()
        self.Bind(wx.EVT_CHOICE, self.select)
        self.Show()

    def get_target_directory(self):
        self.config_parser.read(config_file, encoding="utf-8")
        config = dict(self.config_parser.items("DEFAULT"))
        return config["target_directory"]

    def update_directory_list(self):
        target_directory = self.get_target_directory()
        self.choices.Clear()
        self.choices.Append(target_directory)
        self.choices.Append("other")
        self.choices.SetSelection(0)

    def hide(self, event):
        self.Hide()

    def destroy(self):
        self.autosaver.stop()
        self.tskic.Destroy()
        self.Destroy()

    def select(self, event):
        if event.GetSelection() == 0:
            return
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