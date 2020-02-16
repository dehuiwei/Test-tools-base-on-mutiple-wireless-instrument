import wx
from wx.lib.splitter import MultiSplitterWindow

class MyFrame(wx.Frame):
    def __init__(self,parent,id,title=""):
        wx.Frame.__init__(self,parent,title = title,pos = (15,15),size = (1260,800))
        mainsplitter = MultiSplitterWindow(self, style=wx.SP_3D | wx.SP_LIVE_UPDATE)
        mainsplitter.SetOrientation(wx.VERTICAL)
        self.splitterpanel1 = MainPanel(mainsplitter)
        self.splitterpanel2 = BottomPanel(mainsplitter)
        mainsplitter.AppendWindow(self.splitterpanel1, -1)
        mainsplitter.AppendWindow(self.splitterpanel2, -1)
        mainsplitter.SetSashPosition(0, 410)
        
class MainPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,style=wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)
        self.toppanel = TopPanel(self)
        self.midpanel = MidPanel(self)
        
class TopPanel(wx.Panel):
    def __init__(self,parent):
#         wx.Panel.__init__(self, parent,size= (1000,100),style=wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)
        wx.Panel.__init__(self, parent,-1,size = (1225,50),pos= (5,25), style=wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)
        self.SetBackgroundColour('LIGHTGREY')
        self.mid_panel = MidPanel(self)
        self.grid0 = wx.GridBagSizer(5,5)
         
        self.font1 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.checkbox_auto = wx.CheckBox(self,label="AUTO",style = wx.CHK_3STATE)
        self.checkbox_auto.SetFont(self.font1)
        self.grid0.Add(self.checkbox_auto,pos = (0,0),flag = wx.ALL,border = 5)
         
        self.checkbox_manual = wx.CheckBox(self,label="MANUAL",style = wx.CHK_3STATE)
        self.checkbox_manual.SetFont(self.font1)
        self.grid0.Add(self.checkbox_manual,pos =(0,1),flag = wx.ALL, border = 5)
        
        self.statictext_inst = wx.StaticText(self,label = "Instrument IP")
        self.statictext_inst.SetFont(self.font1)
        self.grid0.Add(self.statictext_inst,pos = (0,2),flag = wx.ALL,border = 5)
         
#         self.text_loadfile = wx.MultiChoiceDialog(self,"test","yes",["auto","manual"])
#         self.grid0.Add(self.text_loadfile,pos= (0,18),flag = wx.ALL,border =5)
        textctrl_inst_ip = wx.TextCtrl(self,size = (151,20))
        self.grid0.Add(textctrl_inst_ip,pos = (0,3),flag = wx.ALL,border = 5 )
        
        self.button_connect = wx.Button(self,label = "Connect",size = (80,20))
        self.button_connect.SetFont(self.font)
        self.grid0.Add(self.button_connect,pos = (0,4),flag = wx.ALL,border = 5)
        
        self.button_browser = wx.Button(self,label = "Load CA",size = (100,20))
        self.button_browser.SetFont(self.font)
        self.grid0.Add(self.button_browser,pos = (0,5),flag = wx.ALL,border = 5)
         
 
         
        self.button_app = wx.Button(self,label = "Apply",size = (122,20))
        self.button_app.SetFont(self.font)
        self.grid0.Add(self.button_app,pos = (0,6),flag = wx.ALL,border = 5)
         
        self.button_clear = wx.Button(self,label = "Clear",size = (122,20))
        self.button_clear.SetFont(self.font)
        self.grid0.Add(self.button_clear,pos = (0,7),flag = wx.ALL,border = 5)
        self.SetSizerAndFit(self.grid0)
         
        self.button_start = wx.Button(self,label = "Start",size = (122,20))
        self.button_start.SetFont(self.font)
        self.grid0.Add(self.button_start,pos = (0,8),flag = wx.ALL,border = 5)
        self.SetSizerAndFit(self.grid0)
         
        self.button_stop = wx.Button(self,label = "Stop",size = (122,20))
        self.button_stop.SetFont(self.font)
        self.grid0.Add(self.button_stop,pos = (0,9),flag = wx.ALL,border = 5)
        
        


        
#         self.file_loder = wx.LoadFileSelector("please lode the ca comb excel file","*.*","ca_comb",self)
        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.grid0)
        self.Layout()
class MidPanel(wx.Panel):
    def __init__(self,parent):
        
#         wx.Panel.__init__(self, parent, pos = (5,105),size= (1000,300),style=wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)
        wx.Panel.__init__(self, parent, -1,size = (1250,300),pos = (5,70),style=wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
#         self.grid0 = self.grid = wx.GridBagSizer(18,0)
        
        self.grid = wx.GridBagSizer(18,0)
        
        text_duplex = wx.StaticText(self,label = "Duplex mode")
        self.grid.Add(text_duplex,pos = (2,0),flag = wx.ALL,border = 5)
        text_duplex.SetFont(self.font)
        
        text_band = wx.StaticText(self,label = "Band")
        self.grid.Add(text_band,pos = (3,0),flag = wx.ALL,border = 5)
        text_band.SetFont(self.font)
        
        text_dlbandwidth = wx.StaticText(self,label = "DL BandWidth")
        self.grid.Add(text_dlbandwidth,pos = (4,0),flag = wx.ALL,border = 5)
        text_dlbandwidth.SetFont(self.font)
        
        text_dlarfcn = wx.StaticText(self,label = "DL ARFCN")
        self.grid.Add(text_dlarfcn,pos = (5,0),flag  = wx.ALL,border = 5)
        text_dlarfcn.SetFont(self.font)
        
        
        text_scs = wx.StaticText(self,label = "SCS")
        self.grid.Add(text_scs,pos = (6,0),flag  = wx.ALL,border = 5)
        text_scs.SetFont(self.font)
        
            
        self.grid1 = wx.GridBagSizer(10,0)
        
        for i in range(9):
            i = i+1
            if i > 7: 
                cell_name = wx.StaticText(self,label = "   5G Cell%d"%(i-7))
            else:
                cell_name = wx.StaticText(self,label = "   LTE Cell%d"%i)
            cell_name.SetFont(self.font)
            self.grid1.Add(cell_name,pos = (1,i),flag =wx.ALL,border =5)
        
            textctrl_duplex_pcell = wx.TextCtrl(self)
            self.grid1.Add(textctrl_duplex_pcell,pos = (2,i),flag = wx.ALL,border = 5 )
         
            textctrl_band_pcell = wx.TextCtrl(self)
            self.grid1.Add(textctrl_band_pcell,pos = (3,i),flag = wx.ALL,border = 5 )
               
            textctrl_dlbandwidth_pcell = wx.TextCtrl(self)
            self.grid1.Add(textctrl_dlbandwidth_pcell,pos = (4,i),flag = wx.ALL,border = 5 )   
    
    
            textctrl_arfcn_pcell = wx.TextCtrl(self)
            self.grid1.Add(textctrl_arfcn_pcell,pos = (5,i),flag = wx.ALL,border = 5 )
            
            textctrl_scs_pcell = wx.TextCtrl(self)
            self.grid1.Add(textctrl_scs_pcell,pos = (6,i),flag = wx.ALL,border = 5 )
   
   
        self.mainSizer.Add(self.grid, 0,wx.ALL,5)
        self.mainSizer.Add(self.grid1,0,wx.ALL,5)
        
#         self.SetSizerAndFit(self.grid1,0,wx.ALL,5)
        self.SetSizerAndFit(self.mainSizer)
#         self.SetBackgroundColour('LIGHTGREY')
#         self.check_list = wx.CheckListBox(self,-1,pos = (20,20),size = (100,50),choices = ["auto"])
#         self.check_list = wx.CheckListBox(self,-1,pos = (20,20),size = (100,50),choices = ["auto","manual"])
#         self.check_box_auto.SetBackgroundStyle(style)
#         self.check_box_auto.
    def button(self,parent,pos,size):
        self.button = wx.Button(self,pos = pos,size = size)

class BottomPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent, pos = (5,409),size = (1000,350),style=wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)
        mainsplitter = MultiSplitterWindow(self)
        mainsplitter.SetOrientation(wx.VERTICAL)
        self.splitterpanel_result = ResultPanel(mainsplitter)
        self.splitterpanel_log = LogPanel(mainsplitter)
        mainsplitter.AppendWindow(self.splitterpanel_result,0)
        mainsplitter.AppendWindow(self.splitterpanel_log,0)
        mainsplitter.SetSashPosition(0,200)
class LogPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent,pos =(5,5),size = (100,100),style=wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)
        
class ResultPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent, pos = (5,5),size = (15,15),style=wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)
        
        
        
        
if __name__ == "__main__":
    app =  wx.App()
#     frame = wx.Frame(None,-1,title = "CA_TEST_Tools",pos = (15,15),size = (1000,800))
    frame = MyFrame(None,-1,title = "CA_TEST_GUI")
#     panel = wx.Panel(frame,-1,pos = (15,15),size = (100,100),style=wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)
    frame.Show()
    app.MainLoop()