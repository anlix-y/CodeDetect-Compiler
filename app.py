import wx
import os
import wx.adv
import configparser
from CDC import Code

Code.once_system_definer()

TRAY_TOOLTIP = 'CodeDetectCompiler' 
TRAY_ICON = 'style/ico.png'

config = configparser.ConfigParser()
config.read("settings.ini")

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Open menu', self.on_hello)
        create_menu_item(menu, 'Screenshot', self.on_screen)
        menu.AppendSeparator()
        create_menu_item(menu, 'Setings', self.on_setting)
        create_menu_item(menu, 'Open log.txt', self.on_log)
        create_menu_item(menu, 'Check update', self.on_update)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):      
        print ('Tray icon was left-clicked.')

    def on_screen(self, event):
        from screenshot import StartAppS
        StartAppS()

    def on_hello(self, event):
        from front import StartAppF
        StartAppF()

    def on_setting(self, event):
        try:
            file_path = r'settings.ini'
            if config['CDC']['your_system'].lower() == 'macos':
                os.system(f'open {file_path}')
            elif config['CDC']['your_system'].lower() == 'linux':
                os.system(f'xdg-open {file_path}')
            elif config['CDC']['your_system'].lower() == 'windows':
                os.system(f'start {file_path}')
        except Exception as e:
            Code.err_out(e)

    def on_log(self, event):
        file_path = r'log.txt'
        try:
            if config['CDC']['your_system'].lower() == 'macos':
                os.system(f'open {file_path}')
            elif config['CDC']['your_system'].lower() == 'linux':
                os.system(f'xdg-open {file_path}')
            elif config['CDC']['your_system'].lower() == 'windows':
                os.system(f'start {file_path}')
        except Exception as e:
            Code.err_out(e)

    def on_update(self, event):
        import update

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

if __name__ == '__main__':
    app = App(False)
    app.MainLoop()