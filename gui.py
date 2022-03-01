import wx
import tools
from wx.adv import TaskBarIcon
from main import AutoSaver
from os import path

class MyTaskBarIcon(TaskBarIcon):
    def __init__(self, frame):
        super().__init__()
        self._frame = frame
        self._paused = False

        path_to_png = path.abspath(path.join(path.dirname(__file__), 'auto.png'))
        self.SetIcon(wx.Icon(path_to_png, wx.BITMAP_TYPE_PNG), 'Screenshot Autosaver')
        self.Bind(wx.EVT_MENU, self.acitvate, id=1)
        self.Bind(wx.EVT_MENU, self.toggle_paused, id=2)
        self.Bind(wx.EVT_MENU, self.destroy, id=3)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu_list = ['Show', 'Continue' if self._paused else 'Pause', 'Quit']
        for idx, name in enumerate(menu_list):
            menu.Append(idx + 1, name)
        return menu

    def destroy(self, event):
        self._frame.destroy()

    def acitvate(self, event):
        if self._frame.IsShown():
            return
        self._frame.Raise()
        self._frame.ShowWithEffect(wx.SHOW_EFFECT_EXPAND, timeout=0)
    
    def toggle_paused(self, event):
        self._frame._autosaver.toggle_paused()
        self._paused = not self._paused

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        super().__init__(parent, id, title, (-1, -1), (290, 280))
        self._task_bar_icon = MyTaskBarIcon(self)
        self._autosaver = AutoSaver()
        self._autosaver.start()

        path_to_ico = path.abspath(path.join(path.dirname(__file__), 'icon_wxWidgets.ico'))
        self.SetIcon(wx.Icon(path_to_ico, wx.BITMAP_TYPE_ICO))
        self.SetSize((400, 250))
        self.Bind(wx.EVT_CLOSE, self.hide)
        self.Bind(wx.EVT_BUTTON, self.click)
        self.Centre()

        main_panel = self.generate_main_panel()
        self.initialize_directory_list(main_panel)
        box = self.generate_box(main_panel)
        button = self.generate_button(main_panel)
        sizer = self.generate_sizer(box, button)
        main_panel.SetSizer(sizer)

    def generate_button(self, main_panel):
        return wx.Button(main_panel, -1, label="Change")

    def generate_box(self, main_panel):
        box = wx.StaticBox(main_panel, wx.ID_ANY, "介紹")
        self.set_introduction(box)
        return box

    def set_introduction(self, box):
        intro_content = ("將使用 Windows鍵 + Shift + S 截取的圖案"
                         "自動儲存到所選取的資料夾位置。\n\n"
                         "關閉視窗時仍會自動執行，\n如需關閉請到工作列中選Quit將其關閉。")
        intro = wx.StaticText(box, wx.ID_ANY, intro_content, style=wx.LEFT)
        intro.Wrap(300)

    def generate_sizer(self, box, button):
        sizer = wx.GridBagSizer(5, 5)
        sizer.Add(box, pos=(0, 0), span=(3, 5),
                  flag=wx.TOP | wx.LEFT | wx.BOTTOM | wx.RIGHT | wx.EXPAND, border=5)
        sizer.Add(self._target_directory_text, pos=(4, 0), span=(1, 4),
                  flag=wx.LEFT | wx.BOTTOM | wx.EXPAND, border=15)
        sizer.Add(button, pos=(4, 4),
                  flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=15)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(2)
        return sizer

    def generate_main_panel(self):
        return wx.Panel(self, -1)

    def initialize_directory_list(self, main_panel):
        self._target_directory_text = wx.TextCtrl(main_panel, -1, value="",
                                                  style=wx.TE_READONLY)
        self.update_directory_list()

    def update_directory_list(self):
        self._target_directory_text.SetValue(tools.get_target_directory())

    def hide(self, event):
        self.Hide()

    def destroy(self):
        self._autosaver.stop()
        self._task_bar_icon.Destroy()
        self.Destroy()

    def click(self, event):
        dialog = wx.DirDialog(None, "Choose input directory", "",
                              wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            chosen_directory = dialog.GetPath()
            tools.update_target_directory(chosen_directory)
        dialog.Destroy()
        self.update_directory_list()


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'Screenshot autosaver')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp()
app.MainLoop()