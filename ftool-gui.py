import psutil
import hashlib
import frida
import time
import threading
import re
import os
import sys
import requests

import wx
import wx.xrc
import wx.stc

import gettext
_ = gettext.gettext

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"ftool-gui"), pos = wx.DefaultPosition, size = wx.Size( 955,705 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

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

        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_checkBox_autoswitch = wx.CheckBox( self, wx.ID_ANY, _(u"Auto Switch"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBox_autoswitch.SetValue(True)
        bSizer12.Add( self.m_checkBox_autoswitch, 0, wx.ALL, 5 )

        self.m_checkBox_showall = wx.CheckBox( self, wx.ID_ANY, _(u"Show All"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer12.Add( self.m_checkBox_showall, 0, wx.ALL, 5 )

        self.m_checkBox_force = wx.CheckBox( self, wx.ID_ANY, _(u"Force Attach"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer12.Add( self.m_checkBox_force, 0, wx.ALL, 5 )


        bSizer4.Add( bSizer12, 0, wx.EXPAND, 5 )

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

        self.m_button_open = wx.Button( self, wx.ID_ANY, _(u"Open"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.m_button_open, 0, wx.ALL, 5 )

        self.m_button_exec = wx.Button( self, wx.ID_ANY, _(u"Exec"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.m_button_exec, 0, wx.ALL, 5 )


        bSizer5.Add( bSizer8, 0, wx.EXPAND, 5 )

        self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0, u"Default" )
        self.m_panel1 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )

        self.m_scintilla_code = wx.stc.StyledTextCtrl( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_scintilla_code.SetUseTabs ( True )
        self.m_scintilla_code.SetTabWidth ( 4 )
        self.m_scintilla_code.SetIndent ( 4 )
        self.m_scintilla_code.SetTabIndents( True )
        self.m_scintilla_code.SetBackSpaceUnIndents( True )
        self.m_scintilla_code.SetViewEOL( False )
        self.m_scintilla_code.SetViewWhiteSpace( False )
        self.m_scintilla_code.SetMarginWidth( 2, 0 )
        self.m_scintilla_code.SetIndentationGuides( True )
        self.m_scintilla_code.SetReadOnly( False )
        self.m_scintilla_code.SetMarginType ( 1, wx.stc.STC_MARGIN_SYMBOL )
        self.m_scintilla_code.SetMarginMask ( 1, wx.stc.STC_MASK_FOLDERS )
        self.m_scintilla_code.SetMarginWidth ( 1, 16)
        self.m_scintilla_code.SetMarginSensitive( 1, True )
        self.m_scintilla_code.SetProperty ( "fold", "1" )
        self.m_scintilla_code.SetFoldFlags ( wx.stc.STC_FOLDFLAG_LINEBEFORE_CONTRACTED | wx.stc.STC_FOLDFLAG_LINEAFTER_CONTRACTED )
        self.m_scintilla_code.SetMarginType( 0, wx.stc.STC_MARGIN_NUMBER )
        self.m_scintilla_code.SetMarginWidth( 0, self.m_scintilla_code.TextWidth( wx.stc.STC_STYLE_LINENUMBER, "_99999" ) )
        self.m_scintilla_code.MarkerDefine( wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS )
        self.m_scintilla_code.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDER, wx.BLACK)
        self.m_scintilla_code.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDER, wx.WHITE)
        self.m_scintilla_code.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS )
        self.m_scintilla_code.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.BLACK )
        self.m_scintilla_code.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.WHITE )
        self.m_scintilla_code.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_EMPTY )
        self.m_scintilla_code.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUS )
        self.m_scintilla_code.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEREND, wx.BLACK )
        self.m_scintilla_code.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEREND, wx.WHITE )
        self.m_scintilla_code.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUS )
        self.m_scintilla_code.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.BLACK)
        self.m_scintilla_code.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.WHITE)
        self.m_scintilla_code.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_EMPTY )
        self.m_scintilla_code.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_EMPTY )
        self.m_scintilla_code.SetSelBackground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT ) )
        self.m_scintilla_code.SetSelForeground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
        bSizer9.Add( self.m_scintilla_code, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel1.SetSizer( bSizer9 )
        self.m_panel1.Layout()
        bSizer9.Fit( self.m_panel1 )
        self.m_notebook1.AddPage( self.m_panel1, _(u"Custom"), True )
        self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        self.m_scintilla_default = wx.stc.StyledTextCtrl( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_scintilla_default.SetUseTabs ( True )
        self.m_scintilla_default.SetTabWidth ( 4 )
        self.m_scintilla_default.SetIndent ( 4 )
        self.m_scintilla_default.SetTabIndents( True )
        self.m_scintilla_default.SetBackSpaceUnIndents( True )
        self.m_scintilla_default.SetViewEOL( False )
        self.m_scintilla_default.SetViewWhiteSpace( False )
        self.m_scintilla_default.SetMarginWidth( 2, 0 )
        self.m_scintilla_default.SetIndentationGuides( True )
        self.m_scintilla_default.SetReadOnly( False )
        self.m_scintilla_default.SetMarginType ( 1, wx.stc.STC_MARGIN_SYMBOL )
        self.m_scintilla_default.SetMarginMask ( 1, wx.stc.STC_MASK_FOLDERS )
        self.m_scintilla_default.SetMarginWidth ( 1, 16)
        self.m_scintilla_default.SetMarginSensitive( 1, True )
        self.m_scintilla_default.SetProperty ( "fold", "1" )
        self.m_scintilla_default.SetFoldFlags ( wx.stc.STC_FOLDFLAG_LINEBEFORE_CONTRACTED | wx.stc.STC_FOLDFLAG_LINEAFTER_CONTRACTED )
        self.m_scintilla_default.SetMarginType( 0, wx.stc.STC_MARGIN_NUMBER )
        self.m_scintilla_default.SetMarginWidth( 0, self.m_scintilla_default.TextWidth( wx.stc.STC_STYLE_LINENUMBER, "_99999" ) )
        self.m_scintilla_default.MarkerDefine( wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS )
        self.m_scintilla_default.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDER, wx.BLACK)
        self.m_scintilla_default.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDER, wx.WHITE)
        self.m_scintilla_default.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS )
        self.m_scintilla_default.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.BLACK )
        self.m_scintilla_default.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.WHITE )
        self.m_scintilla_default.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_EMPTY )
        self.m_scintilla_default.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUS )
        self.m_scintilla_default.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEREND, wx.BLACK )
        self.m_scintilla_default.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEREND, wx.WHITE )
        self.m_scintilla_default.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUS )
        self.m_scintilla_default.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.BLACK)
        self.m_scintilla_default.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.WHITE)
        self.m_scintilla_default.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_EMPTY )
        self.m_scintilla_default.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_EMPTY )
        self.m_scintilla_default.SetSelBackground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT ) )
        self.m_scintilla_default.SetSelForeground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
        bSizer10.Add( self.m_scintilla_default, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel2.SetSizer( bSizer10 )
        self.m_panel2.Layout()
        bSizer10.Fit( self.m_panel2 )
        self.m_notebook1.AddPage( self.m_panel2, _(u"Default"), False )

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
# UI界面初始化
    def Init(self):
        Util.LOG_WINDOW = self.m_textCtrl_log
        Util.CODE_WINDOW = self.m_scintilla_code
        Util.DEFAULT_WINDOW = self.m_scintilla_default
        Util.ATTACHED_CHOICES = self.m_choice_attached
        self.handle_code_style(Util.CODE_WINDOW)
        self.handle_code_style(Util.DEFAULT_WINDOW)
        # Connect Events
        self.Bind(wx.EVT_MENU, self.on_close, self.m_menuItem_close)
        self.m_button_search.Bind(wx.EVT_BUTTON, self.on_search)
        self.m_button_attach.Bind(wx.EVT_BUTTON, self.on_attach)
        self.m_button_detach.Bind(wx.EVT_BUTTON, self.on_detach)
        self.m_button_clear.Bind(wx.EVT_BUTTON, self.on_clear)
        self.m_button_load.Bind(wx.EVT_BUTTON, self.on_load)
        self.m_button_open.Bind(wx.EVT_BUTTON, self.on_open)
        self.m_button_exec.Bind(wx.EVT_BUTTON, self.on_exec)
        self.m_choice_attached.Bind(wx.EVT_CHOICE, self.on_choice)
        self.m_checkBox_autoswitch.Bind(wx.EVT_CHECKBOX, self.on_checkbox)
        self.m_checkBox_force.Bind(wx.EVT_CHECKBOX, self.on_checkbox)
        self.m_checkBox_showall.Bind(wx.EVT_CHECKBOX, self.on_checkbox)
        self.on_checkbox(None)
        Util.load_default_code()
# 对代码窗口进行格式处理
    def handle_code_style(self, component:wx.stc.StyledTextCtrl):
        # 设置默认字体和大小
        component.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "face:Courier New,size:12")
        component.StyleClearAll()

        # 设置 JavaScript 语法高亮
        component.SetLexer(wx.stc.STC_LEX_CPP)  # 使用 C++ 词法解析器处理 JavaScript
        component.SetKeyWords(0, "var let const function return if else for while switch case break continue try catch finally throw new in this typeof instanceof delete void")
        
        # 设置各种语法元素的颜色
        component.StyleSetSpec(wx.stc.STC_C_DEFAULT, "fore:#000000")   # 默认
        component.StyleSetSpec(wx.stc.STC_C_COMMENTLINE, "fore:#007F00,italic")  # 单行注释
        component.StyleSetSpec(wx.stc.STC_C_COMMENT, "fore:#007F00,italic")  # 多行注释
        component.StyleSetSpec(wx.stc.STC_C_NUMBER, "fore:#007F7F")    # 数字
        component.StyleSetSpec(wx.stc.STC_C_STRING, "fore:#7F007F")    # 字符串
        component.StyleSetSpec(wx.stc.STC_C_CHARACTER, "fore:#7F007F") # 字符
        component.StyleSetSpec(wx.stc.STC_C_WORD, "fore:#00007F,bold") # 关键字
        component.StyleSetSpec(wx.stc.STC_C_OPERATOR, "fore:#000000,bold") # 操作符
        component.StyleSetSpec(wx.stc.STC_C_IDENTIFIER, "fore:#000000")   # 标识符
        component.StyleSetSpec(wx.stc.STC_C_REGEX, "fore:#7F007F")    # 正则表达式
    
    # Event Handlers
    # 退出程序事件
    def on_close(self, event):
        dlg = wx.MessageDialog(self, "Are you sure you want to exit?", "Confirm Exit", wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        
        if result == wx.ID_YES:
            for thread in Util.THREADS:
                if thread is not None and thread.is_alive():
                    thread.join(timeout=2)  # 等待线程终止，如果超过5秒则强制关闭
            self.Destroy()
            os._exit(0)
    # 搜索按钮事件
    def on_search(self, event):
        search_text = self.m_textCtrl_search.GetValue()
        Util.log("search",f"Searching for: {search_text}\n")
        is_finded = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # 如果进程名称匹配，则返回 PID
                "".find
                if proc.info['name'].lower().find(search_text.lower()) != -1:
                    is_finded = True
                    Util.log("search",f"PID: {proc.info['pid']} Name: {proc.info['name']}\n")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                Util.log("search",f"Searching rrror for: {search_text}\n")
        if not is_finded:
            Util.log("search",f"Searching not found!\n")
    # 附加进程事件
    def on_attach(self, event):
        target = self.m_textCtrl_search.GetValue()
        # 支持多程序同时附加
        targets = target.split(",")
        Util.new_frida(targets)
    # 解除进程附加状态
    def on_detach(self, event):
        Util.exec_cmd("detach")
        # 刷新附加列表
        Util.refresh_choices()
    # 日志窗口清空
    def on_clear(self, event):
        self.m_textCtrl_log.Clear()
    # load按钮事件，支持url/打开文件窗口
    def on_load(self, event):
        file_path = self.m_textCtrl_jsfile.GetValue()
        if file_path.replace(" ","") == "":
            with wx.FileDialog(self, "选择一个文件", wildcard="所有文件 (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return
                # 获取所选文件的路径
                file_path = fileDialog.GetPath()
                self.m_textCtrl_jsfile.SetValue(file_path)
        if file_path.startswith("http://") or file_path.startswith("https://"):
            try:
                res = requests.get(file_path,headers={
                    "User-Agent": "ftool-gui"
                }, timeout=5)
                if res.status_code == 200:
                    Util.set_custom_code(res.text)
            except Exception as ex:
                Util.log("load code", "Error: " + str(ex))
        elif os.path.exists(file_path) and os.path.isfile(file_path):
            code = open(file_path,'r',encoding='utf8').read()
            Util.set_custom_code(code)
        else:
            Util.log("load code", "Path is a dir or not found!")
    #  open按钮事件，打开文件窗口选择文件
    def on_open(self, event):
        file_path = ""
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
    #  exec按钮事件，对附加进程执行命令
    def on_exec(self, event):
        Util.exec_cmd()
    # 附加列表变动事件 
    def on_choice(self, event):
        selected = self.m_choice_attached.GetString(self.m_choice_attached.GetSelection())
        Util.set_current(selected)
        print(f'You selected: {selected}')
    # flag变动事件
    def on_checkbox(self, event):
        Util.FLAGS["force_attach"] = self.m_checkBox_force.IsChecked()
        Util.FLAGS["auto_switch"] = self.m_checkBox_autoswitch.IsChecked()
        Util.FLAGS["show_all"] = self.m_checkBox_showall.IsChecked()
# 全局工具类   
class Util():
    LOG_WINDOW = None
    CODE_WINDOW = None
    DEFAULT_WINDOW = None
    DEFAULT_CODE_PATH = "code/all-in-one.js"
    FLAGS = {
        "force_attach": False,
        "auto_switch": True,
        "show_all": False
    }
    ATTACHED_CHOICES = None
    CLIENTS = {}
    CURRENT = ""
    LOCK = threading.Lock()
    THREADS = []
    # 日志窗口输出
    def log(source:str, message:str):
        if Util.LOG_WINDOW == None:
            return
        # 结尾换行处理
        if not message.endswith("\n"):
            message = message + "\n"
        # 附加进程返回消息判断是否为当前选择进程，如果不是不现实，如果是show_all为True全部显示
        # TODO 为每个附加的进程设置单独的消息存储
        if source.find("|") != -1 and Util.CURRENT != source and Util.CURRENT != "" and Util.FLAGS["show_all"] != True:
            return
        wx.CallAfter(Util.LOG_WINDOW.AppendText, f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n[{source}]: {message}")
    # 附加进程创建新的client
    def new_frida(targets:list):
        with Util.LOCK:
            for target in targets:
                Util.log("new_frida",str(target))
                client = FridaClient(target)
                thread = threading.Thread(target=client.attach).start()
                Util.THREADS.append(thread)
    # 设置cutom_code内容
    def set_custom_code(code):
        Util.CODE_WINDOW.SetValue(code)
    # 获取cutom_code内容
    def get_custom_code():
        return Util.CODE_WINDOW.GetValue()
    # 加载默认代码
    def load_default_code():
        # 路径针对打包做处理
        # TODO 自定义默认代码位置
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
    # 获取默认代码内容
    def get_default_code() -> str:
        return Util.DEFAULT_WINDOW.GetValue()
    # 增加client id，如果auto_switch为True，自动切换为最新的附加客户端
    def add_client(id):
        Util.CLIENTS[id] = ""
        if Util.CURRENT == "" or Util.FLAGS["auto_switch"]:
            Util.CURRENT = id
        Util.refresh_choices()
    # 客户端清除
    def exit_client(id):
        Util.CLIENTS.pop(id)
        Util.refresh_choices()
    # 命令执行
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
    # 根据客户端id获取当前执行命令
    def get_cmd(id=None):
        cmd = Util.CLIENTS[id]
        Util.CLIENTS[id] = ""
        return cmd
    # 设置当前客户端
    def set_current(id):
        Util.CURRENT = id
    # 附加客户端列表刷新
    def refresh_choices():
        client_ids = list(Util.CLIENTS.keys())
        if Util.CURRENT != "" and Util.CURRENT not in client_ids:
            Util.CURRENT = ""
        wx.CallAfter(Util.ATTACHED_CHOICES.Set,client_ids)
        if Util.CURRENT == "" and len(client_ids) > 0:
            Util.CURRENT = client_ids[0]
            print(Util.CURRENT,client_ids)
        if Util.CURRENT != "":
            # index = Util.ATTACHED_CHOICES.FindString(Util.CURRENT)
            index = client_ids.index(Util.CURRENT)
            print(index)
            if index != wx.NOT_FOUND:
                wx.CallAfter(Util.ATTACHED_CHOICES.SetSelection,index)
# Frida相关操作类
class FridaClient:
    # 初始化
    def __init__(self,target):
        self.target = target
        self.uuid = self.target + " | " + str(hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()[:8])
    # 客户端消息
    def log(self, message):
        Util.log(self.uuid, message)
    # 系统消息
    def sys_log(self, message):
        Util.log("system", message)
    # frida消息回调
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
    # 进程附加
    def attach(self):
        target = self.target
        # 对pid进行兼容
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
                # 应用多进程同时附加处理
                self.sys_log(f"{self.uuid} || Find {len(choices)} process: {str(choices)}")
                Util.new_frida(choices)
                return
            if error.startswith("unable to find process"):
                # 当force_attach为True时，循环等待进程启动
                if Util.FLAGS["force_attach"]:
                    time.sleep(0.2)
                    Util.new_frida([target])
            return

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

# 启动方法
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