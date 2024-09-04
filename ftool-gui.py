import psutil
import hashlib
import frida
import time
import threading
import re
import os
import sys

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"ftool-gui"), pos = wx.DefaultPosition, size = wx.Size( 575,438 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_textCtrl_search = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_textCtrl_search, 1, wx.ALL, 5 )

        self.m_button_search = wx.Button( self, wx.ID_ANY, _(u"Search"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button_search, 0, wx.ALL, 5 )

        self.m_button_attach = wx.Button( self, wx.ID_ANY, _(u"Attach"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button_attach, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        m_choice_attachedChoices = []
        self.m_choice_attached = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_attachedChoices, 0 )
        self.m_choice_attached.SetSelection( 0 )
        bSizer6.Add( self.m_choice_attached, 1, wx.ALL, 5 )

        self.m_button_detach = wx.Button( self, wx.ID_ANY, _(u"Detach"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_button_detach, 0, wx.ALL, 5 )
        self.m_button_clear = wx.Button( self, wx.ID_ANY, _(u"Clear"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_button_clear, 0, wx.ALL, 5 )


        bSizer4.Add( bSizer6, 0, wx.EXPAND, 5 )

        bSizer7 = wx.BoxSizer( wx.VERTICAL )

        self.m_textCtrl_log = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
        bSizer7.Add( self.m_textCtrl_log, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer4.Add( bSizer7, 1, wx.EXPAND, 5 )


        bSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )

        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_textCtrl_jsfile = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.m_textCtrl_jsfile, 1, wx.ALL, 5 )

        self.m_button_load = wx.Button( self, wx.ID_ANY, _(u"Load"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.m_button_load, 0, wx.ALL, 5 )

        self.m_button_exec = wx.Button( self, wx.ID_ANY, _(u"Exec"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.m_button_exec, 0, wx.ALL, 5 )


        bSizer5.Add( bSizer8, 0, wx.EXPAND, 5 )

        self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_panel1 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )

        self.m_textCtrl_code = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
        bSizer9.Add( self.m_textCtrl_code, 1, wx.ALL|wx.EXPAND, 5 )


        self.m_panel1.SetSizer( bSizer9 )
        self.m_panel1.Layout()
        bSizer9.Fit( self.m_panel1 )
        self.m_notebook1.AddPage( self.m_panel1, _(u"Custom"), False )
        self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        self.m_textCtrl_default = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
        bSizer10.Add( self.m_textCtrl_default, 1, wx.ALL|wx.EXPAND, 5 )


        self.m_panel2.SetSizer( bSizer10 )
        self.m_panel2.Layout()
        bSizer10.Fit( self.m_panel2 )
        self.m_notebook1.AddPage( self.m_panel2, _(u"Default"), True )

        bSizer5.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer3.Add( bSizer5, 1, wx.EXPAND, 5 )


        bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()
        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menubar1.Hide()

        self.m_menu_application = wx.Menu()
        self.m_menuItem_close = wx.MenuItem( self.m_menu_application, wx.ID_ANY, _(u"CLOSE")+ u"\t" + u"CTRL+Q", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_application.Append( self.m_menuItem_close )

        self.m_menubar1.Append( self.m_menu_application, _(u"App") )

        self.SetMenuBar( self.m_menubar1 )


        self.Centre( wx.BOTH )
        self.Init()

    def __del__( self ):
        pass
    
    def Init(self):
        Util.LOG_WINDOW = self.m_textCtrl_log
        Util.CODE_WINDOW = self.m_textCtrl_code
        Util.DEFAULT_WINDOW = self.m_textCtrl_default
        Util.ATTACHED_CHOICES = self.m_choice_attached
        # Connect Events
        self.Bind(wx.EVT_MENU, self.on_close, self.m_menuItem_close)
        self.m_button_search.Bind(wx.EVT_BUTTON, self.on_search)
        self.m_button_attach.Bind(wx.EVT_BUTTON, self.on_attach)
        self.m_button_detach.Bind(wx.EVT_BUTTON, self.on_detach)
        self.m_button_clear.Bind(wx.EVT_BUTTON, self.on_clear)
        self.m_button_load.Bind(wx.EVT_BUTTON, self.on_load)
        self.m_button_exec.Bind(wx.EVT_BUTTON, self.on_exec)
        self.m_choice_attached.Bind(wx.EVT_CHOICE, self.on_choice)
        Util.load_default_code()
    
    # Event Handlers
    def on_close(self, event):
        dlg = wx.MessageDialog(self, "Are you sure you want to exit?", "Confirm Exit", wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        
        if result == wx.ID_YES:
            for thread in Util.THREADS:
                if thread is not None and thread.is_alive():
                    thread.join(timeout=2)  # 等待线程终止，如果超过5秒则强制关闭
            self.Destroy()
            os._exit(0)
    
    def on_search(self, event):
        search_text = self.m_textCtrl_search.GetValue()
        Util.log("search",f"Searching for: {search_text}\n")
        is_finded = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # 如果进程名称匹配，则返回 PID
                if proc.info['name'].find(search_text) != -1:
                    is_finded = True
                    Util.log("search",f"PID: {proc.info['pid']} Name: {proc.info['name']}\n")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                Util.log("search",f"Searching rrror for: {search_text}\n")
        if not is_finded:
            Util.log("search",f"Searching not found!\n")

    def on_attach(self, event):
        target = self.m_textCtrl_search.GetValue()
        targets = target.split(",")
        Util.new_frida(targets)

    def on_detach(self, event):
        Util.exec_cmd("detach")
        
    def on_clear(self, event):
        self.m_textCtrl_log.Clear()

    def on_load(self, event):
        file_path = self.m_textCtrl_jsfile.GetValue()
        if file_path.replace(" ","") == "":
            with wx.FileDialog(self, "选择一个文件", wildcard="所有文件 (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return
                # 获取所选文件的路径
                file_path = fileDialog.GetPath()
                self.m_textCtrl_jsfile.SetValue(file_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            code = open(file_path,'r',encoding='utf8').read()
            Util.set_custom_code(code)
        else:
            Util.log("load code", "Path is a dir or not found!")

    def on_exec(self, event):
        Util.exec_cmd()
        
    def on_choice(self, event):
        selected = self.m_choice_attached.GetString(self.m_choice_attached.GetSelection())
        Util.set_current(selected)
        print(f'You selected: {selected}')
        
class Util():
    LOG_WINDOW = None
    CODE_WINDOW = None
    DEFAULT_WINDOW = None
    DEFAULT_CODE_PATH = "code/all-in-one.js"
    FLAGS = {
        "force_attach": False
    }
    ATTACHED_CHOICES = None
    CLIENTS = {}
    CURRENT = ""
    LOCK = threading.Lock()
    THREADS = []
    
    def log(source:str, message:str):
        if Util.LOG_WINDOW == None:
            return
        if not message.endswith("\n"):
            message = message + "\n"
        if source.find("|") != -1 and Util.CURRENT != source and Util.CURRENT != "":
            return
        wx.CallAfter(Util.LOG_WINDOW.AppendText, f"[{source}]: {message}")
    
    def new_frida(targets:list):
        with Util.LOCK:
            for target in targets:
                Util.log("new_frida",str(target))
                client = FridaClient(target)
                thread = threading.Thread(target=client.attach).start()
                Util.THREADS.append(thread)
    
    def set_custom_code(code):
        Util.CODE_WINDOW.SetValue(code)

    def get_custom_code():
        return Util.CODE_WINDOW.GetValue()
    
    def load_default_code():
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            # 未打包的情况下
            base_path = os.path.abspath(".")
        file_path = os.path.join(base_path, Util.DEFAULT_CODE_PATH)
        print(file_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            file_data = open(file_path,'r',encoding='utf-8').read()
            Util.DEFAULT_WINDOW.SetValue(file_data)
    
    def get_default_code() -> str:
        return Util.DEFAULT_WINDOW.GetValue()

    def add_client(id):
        Util.CLIENTS[id] = ""
        if Util.CURRENT == "":
            Util.CURRENT = id
        Util.refresh_choices()
    
    def exit_client(id):
        Util.CLIENTS.pop(id)
        Util.refresh_choices()
    
    def exec_cmd(cmd=None):
        id = Util.CURRENT
        if not cmd:
            cmd = Util.get_custom_code()
        if id in Util.CLIENTS:
            ocmd = Util.CLIENTS[id]
            if ocmd != "":
                time.sleep(0.3)
                Util.exec_cmd()
            else:
                Util.CLIENTS[id] = cmd
                Util.log("exec cmd",f"{id} || {cmd}")
        else:
            Util.log("exec cmd","No Client")
            
    def get_cmd(id=None):
        cmd = Util.CLIENTS[id]
        Util.CLIENTS[id] = ""
        return cmd
    
    def set_current(id):
        Util.CURRENT = id
    
    def refresh_choices():
        client_ids = list(Util.CLIENTS.keys())
        if Util.CURRENT != "" and Util.CURRENT not in client_ids:
            Util.CURRENT = ""
        wx.CallAfter(Util.ATTACHED_CHOICES.Set,client_ids)
        if len(client_ids) > 0:
            Util.CURRENT = client_ids[0]
            print(Util.CURRENT,client_ids)
        if Util.CURRENT != "":
            # index = Util.ATTACHED_CHOICES.FindString(Util.CURRENT)
            index = client_ids.index(Util.CURRENT)
            print(index)
            if index != wx.NOT_FOUND:
                wx.CallAfter(Util.ATTACHED_CHOICES.SetSelection,index)
            
class FridaClient:
    
    def __init__(self,target):
        self.target = target
        self.uuid = self.target + " | " + str(hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()[:8])
    
    def log(self, message):
        Util.log(self.uuid, message)
    
    def sys_log(self, message):
        Util.log("system", message)
        
    def on_message(self,message,data):
        out_data = ""
        try:
            if message['type'] == 'send':
                out_data = message.get('payload',None)
                if out_data == None:
                    return
            elif message['type'] == 'error':
                out_data = message['stack']
            else:
                out_data = message
        except:
            out_data = message
        out_data = str(out_data)
        self.log(out_data)
    
    def attach(self):
        target = self.target
        try:
            target = int(self.target)
        except:
            target = self.target
        try:
            session = frida.attach(target)
        except Exception as ex:
            error = str(ex)
            print(error)
            self.sys_log(self.uuid + " || " + error)
            if error.startswith('ambiguous name; it matches:'):
                pattern = re.compile(r'\b\d+\b')
                choices = pattern.findall(error)
                self.sys_log(f"{self.uuid} || Find {len(choices)} process: {str(choices)}")
                Util.new_frida(choices)
                return
            if error.startswith("unable to find process"):
                if Util.FLAGS["force_attach"]:
                    time.sleep(0.2)
                    Util.new_frida(target)

        default_code = Util.get_default_code()
        try:
            script = session.create_script(default_code)
            script.on('message', self.on_message)
            script.load()
        except Exception as ex:
            self.sys_log(f"Script load failed: {str(ex)}")
            session.detach()
            return
        self.sys_log(f'{self.uuid} || Hook进程成功({str(target)})')
        Util.add_client(self.uuid)
        while True and session.is_detached == False:
            cmd = Util.get_cmd(self.uuid)
            if cmd != "":
                if cmd == "detach":
                    session.detach()
                    break
                else:
                    script.post(cmd)
            time.sleep(0.2)
        self.log(f"client done.")
        Util.exit_client(self.uuid)


def main():
    try:
        app = wx.App(False)
        ex = MainFrame(None)
        ex.Show()
        app.MainLoop()
    except Exception as ex:
        print(ex.with_traceback())

if __name__ == '__main__':
    main()