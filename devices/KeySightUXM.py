# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 14:01:04 2019

@author: weidh
"""

import logging
import visa
import pyvisa as visa
import time
import tkinter
from tkinter import messagebox
import os
# from __builtin__ import True
# import main
# from Output_Log import Log
# import test_config 

class KeySightUXM(object):
    def __init__(self,fwk,tcpip):
        self.log = fwk.log 
        self.fwk = fwk
        self.cfg = self.fwk.cfg

#         super(KeySightUXM,self).__init__()
        rm=visa.ResourceManager()
#         self.tcpip = "TCPIP0::%s::%s::SOCKET"%(ip_addr,port)
        self.fwk.Print("connect to keysight UXM: %s"%tcpip)
        self.log.info("connect to keysight UXM: %s"%tcpip)
#         self.log = Log(__name__).getlog() 
        try:
            self.inst = rm.open_resource(tcpip)
            self.fwk.Print("TA connect successfully")
        except Exception as e :
            self.log.info("can't connect to UXM error code is %s"%e)
            self.fwk.Print("can't connect to UXM")
        self.inst.timeout = 20000
        
        
        self.inst.read_termination = "\n"
        
        self.pcell = ""
    ######SYS procedures#####    
    def write(self,cmd):
        try:
            self.log.info("SCPI COMMAND : %s"%cmd)
            self.fwk.Print("SCPI COMMAND : %s"%cmd)
            self.inst.write(str(cmd))

            return True
        except:
            return False
        self.sleep(2)
#     def write_ongoing(self,cmd):###modify by weidehui ongoing
#         try:
#             self.inst.write(str(cmd))
#             self.log.info("SCPI COMMAND : %s"%cmd)
#             return True
#         except:
#             return False
    def query(self,cmd):
        self.log.info("SCPI COMMAND :%s"%cmd)
        self.fwk.Print("SCPI COMMAND : %s"%cmd)
        return self.inst.query(str(cmd))  
         
    def read(self,cmd):
        try:
            self.log.info("SCPI COMMAND :%s"%cmd)
            self.fwk.Print("SCPI COMMAND : %s"%cmd)
            res = self.inst.read(str(cmd))

            return res
        except:
            return False
        
    def instrument_initialize(self):
        self.Write("")
    
    def sleep(self,timeout):
        self.log.info("sleep %d second"%int(timeout))
        time.sleep(int(timeout)) 
    def preset(self,timeout=10):
        self.set_timeout(30000)
        self.log.info("preset device config")
        self.write("SYSTem:PRESet:FULL")
        self.sleep(timeout)
        self.sleep(20)
#     def init_cell_lte(self,cells_parameter):
#         i = 1
#         for cell_parameter_list in cells_parameter: 
#             self.log.info("initialize LTE cell%d"%i)
#             self.log.info("#######cell_Parameter list is  %s",cell_parameter_list)
#             self.fwk.Print("#####debug")
#             self.write("BSE:CONFig:LTE:CELL%d:DUPLex:MODE %s"%(i,(cell_parameter_list[0])))### set cell1 duplex mode
#             self.fwk.Print("a") 
#             self.write("BSE:CONFig:LTE:CELL%d:BAND %d"%(i,cell_parameter_list[1]))
#             self.fwk.Print("b") 
#             self.fwk.Print(type(cell_parameter_list[2]))
#             self.write("BSE:CONFig:LTE:CELL%d:DL:EARFcn %d"%(i,cell_parameter_list[2]))
#             self.fwk.Print("c") 
#             self.write("BSE:CONFig:LTE:CELL%d:DL:BW BW%d"%(i,cell_parameter_list[3]))
#             self.fwk.Print("d") 
#         #         self.send("BSE:CONFig:LTE:CELL1:EARFcn %d"%cell1[2])
#             self.write("BSE:CONFig:LTE:CELL1:DL:POWer:RSTP -75")
#             i = i+1 


    def init_cell_lte(self,cells_parameter,count):####add by weidehui on 2019/11/01
            self.pcell = "bandx"
            for i in range(len(cells_parameter)): 
                try:
                    cell_parameter_list = cells_parameter[(count+i)%len(cells_parameter)]
                    if (46 in cell_parameter_list or 32 in cell_parameter_list or 29 in cell_parameter_list) and i == 0:
                        self.log.info("Pcell is band%s skip this comb"%cell_parameter_list[1])
                        return "skip"
                    if i == 0:
                        self.pcell = ("band%d"%cell_parameter_list[1])
                    self.log.info("initialize LTE cell%d"%(i+1))
                    self.config_lte_cell(i+1,cell_parameter_list)
                except Exception as e:
                    self.log.error(e)
                    return self.pcell
#                 self.log.info("#######cell_Parameter list is  %s",cell_parameter_list)
#                 self.fwk.Print("#####debug")
#                 self.write("BSE:CONFig:LTE:CELL%d:DUPLex:MODE %s"%(i,(cell_parameter_list[0])))### set cell1 duplex mode
#                 self.fwk.Print("a") 
#                 self.write("BSE:CONFig:LTE:CELL%d:BAND %d"%(i,cell_parameter_list[1]))
#                 self.fwk.Print("b") 
#                 self.fwk.Print(type(cell_parameter_list[2]))
#                 self.write("BSE:CONFig:LTE:CELL%d:DL:EARFcn %d"%(i,cell_parameter_list[2]))
#                 self.fwk.Print("c") 
#                 self.write("BSE:CONFig:LTE:CELL%d:DL:BW BW%d"%(i,cell_parameter_list[3]))
#                 self.fwk.Print("d") 
#                 self.write("BSE:CONFig:LTE:CELL1:DL:POWer:RSTP -75")
            return self.pcell
    def config_lte_cell(self,cell_num,cell_parameter_list):
                self.log.info("#######cell_Parameter list is  %s",cell_parameter_list)
#                 self.fwk.Print("#####debug")
                self.write("BSE:CONFig:LTE:CELL%d:DUPLex:MODE %s"%(cell_num,(cell_parameter_list[0])))### set cell1 duplex mode
#                 self.fwk.Print("a") 
                self.write("BSE:CONFig:LTE:CELL%d:BAND %d"%(cell_num,cell_parameter_list[1]))
#                 self.fwk.Print("b") 
#                 self.fwk.Print(type(cell_parameter_list[2]))
                self.write("BSE:CONFig:LTE:CELL%d:DL:EARFcn %d"%(cell_num,cell_parameter_list[2]))
#                 self.write("BSE:CONFig:LTE:CELL%d:PHY:TDD:ULDL:CONFig 1"%cell_num)
#                 self.fwk.Print("c") 
                self.write("BSE:CONFig:LTE:CELL%d:DL:BW BW%d"%(cell_num,cell_parameter_list[3]))
#                 self.fwk.Print("d") 
                self.write("BSE:CONFig:LTE:CELL%d:DL:POWer:RSTP -65"%cell_num)
                self.write("RFANalyzer:LTE:CELL%d:MANual:POWer 0"%cell_num)
                if self.cfg["mimo_list"]!="":
                    if self.cfg["mimo_list"][cell_num-1] == "2":
                        self.write("BSE:CONFig:LTE:CELL%d:PHY:DL:ANTenna D2U2"%(cell_num))
                    elif self.cfg["mimo_list"][cell_num-1] == "4":
                            self.write("BSE:CONFig:LTE:CELL%d:PHY:DL:ANTenna D4U4"%(cell_num))
                else:
                    self.write("BSE:CONFig:LTE:CELL%d:PHY:DL:ANTenna D2U2"%(cell_num))
                self.fwk.Print(str(cell_parameter_list[1]))
#                 if str(cell_parameter_list[1]) in self.cfg["lte_4X4_mimo_band"]:
#                     self.write("BSE:CONFig:LTE:CELL%d:PHY:DL:ANTenna D4U4"%cell_num)
                if self.cfg["sim_card_type"] == "KEYS":
                    self.write("BSE:CONFig:LTE:SECURITY:AUTH:KEY KEYS")
                elif self.cfg["sim_card_type"] == "TEST3GPP":
                    self.write("BSE:CONFig:LTE:SECURITY:AUTH:KEY TEST3GPP")
                self.cells_reconfigure("LTE")
                
    def active_cells(self, tar_cell = 1):
#         self.log.info("active lte cells")
#         self.fwk.Print("active lte cells")
        self.set_timeout(40000)
        for i in range(3):
            self.log.info("active cell%d"%int(tar_cell))
            self.fwk.Print("active cell%d"%int(tar_cell))
            self.query("BSE:CONFig:LTE:CELL%d:ACTive 1;*OPC?"%int(tar_cell))
            resp = self.check_cell_state(tar_cell, "ON",20)
            if resp:
                return resp

        return resp
    def active_cells_mulit(self,cell_num):
        for cell in range(cell_num):
            res = self.active_cells(cell + 1)
            if res:
                self.log.info("LTE Cell%s active successfully"%str(cell+1))
                
            else:
                self.log.error("LTE Cell%s active unsuccessfully"%str(cell+1))
#                 self.error("sleep 5s")
                return False
            self.sleep(5)
        return True
    def deactive_cells(self,tar_cell = 1):
        for i in range(3):
            self.log.info("deactive cell%d"%int(tar_cell))
            self.query("BSE:CONFig:LTE:CELL%d:ACTive 0;*OPC?"%int(tar_cell))
            resp = self.check_cell_state(tar_cell, "OFF")
            if resp:
                return resp
            self.sleep(20) 
        return resp
    def Release_RRC_LTE(self):
        self.log.info("release lte cells RRC ")
        resp = self.check_cell_state(1,"CONN",2)
        if resp:
            self.write("BSE:FUNCtion:LTE:CELL1:RELease:SEND")
        self.sleep(20)
        
    def deactive_cells_mulit(self,cells_num):
        self.log.info("deactive all the lte actived cells")
        self.fwk.Print("deactive all the lte actived cells")
        for i in range(int(cells_num)):
            res1 = self.check_cell_state(int(4-i),'OFF',5)
            if not res1: 
                res2 = self.deactive_cells(int(4-i))
                if not res2:
                    self.log.error("cell%d deactive unsuccessfully"%(3-i))
#                     i = i+1
#             self.sleep(5)  
    def deactive_cell1(self):
        self.log.info("deactive cell1")
        self.fwk.Print("deactive cell1")
        self.deactive_cells(1)
        self.sleep(20)
        for j in range(6):
            res = self.check_cell_state(6-j,'OFF',5)
            if not res:
                return False

        return True
    def deactive_cell1_loop(self):
        for i in range(3):
            resp = self.deactive_cell1()
            if resp:
                return True
        return False        
                
                                    
    def set_timeout(self, timeout):
        self.inst.timeout = timeout   
        
    def send(self, cmd="", delay=0.02, timeout=None):
        try:
            if timeout is not None:
                    self.set_timeout(timeout)
            if (delay + 0.1) < self.inst.timeout:
                    self.inst.write(cmd + ";*OPC?")
                    if delay > 0.0:
                        time.sleep(delay)
            else:
                    self.inst.write(cmd)
                    if delay > 0.0:
                        time.sleep(delay)
                    self.inst.write("*OPC?")
            opc_res = self.device.read()
            if not "1" in opc_res:
#                     self.log.debug("OPC bit was not set by equipment! Better increase command delay!")
                if timeout is not None:
                    self.reset_timeout()
        except:  # visa.VisaIOError:
#                 self.log.info("VISA addr: %s, TIMEOUT waiting for *OPC? query response!" % self.visa_addr)
                if timeout is not None:
                    self.reset_timeout()
                self.clear()
    def clear(self):
        try:
            self.inst.clear()
        except:
            return
#             self.log.info("VISA addr: %s, attempt to clear the GPIB bus resulted in ERROR!" % self.visa_addr)
     
    def check_cell_state(self,tar_cell = 1,tar_state = 'ON',timeout = 20):##ON OFF IDLE ACT CONN  AGG
        end_time =  timeout + time.time()
        while  time.time() < end_time:
            resp = self.query("BSE:STATus:LTE:CELL%d?"%int(tar_cell))
            if tar_state in resp:
                return True
            self.sleep(2)
        return False 
     
     
    def read_DL_Tput(self,tar_cell):
        self.log.info('get dl Tput on cell%s'%tar_cell)
        resp = self.query("BSE:MEASure:LTE:BTHRoughput:DL:THRoughput:OTA:CELL%s?"%tar_cell)
        return resp
    
    def read_UL_Tput(self,tar_cell = 1):
        UL_Tput = []
        self.log.info('get ul Tput on cell%s'%tar_cell)
        resp = self.query("BSE:MEASure:LTE:BTHRoughput:UL:THRoughput:OTA:CELL%s?"%tar_cell)
        UL_Tput.append(resp)
        return UL_Tput
        
    def read_UL_Bler(self,tar_cell = 1):
        UL_Bler = []
        self.log.info('get ul bler on cell%s'%tar_cell)
        resp = self.query("BSE:MEASure:LTE:BTHRoughput:UL:BLER:CELL%s?"%tar_cell)
        UL_Bler.append(resp)
        self.log.info("Ul bler is %s"%UL_Bler)
        return UL_Bler
    
    def read_DL_Bler(self,tar_cell = 1):
        self.log.info('get dl bler on cell%s'%tar_cell)
        resp = self.query("BSE:MEASure:LTE:BTHRoughput:DL:BLER:CELL%s?"%tar_cell)
        
        return resp
    
    def add_scell(self,scell_number = 2):##TBD
        self.log.info('add scc%d'%scell_number)
        self.inst.write("BSE:CONFig:LTE:CELL1:CAGGregation:AGGRegate:SCC:LIST CELL%d"%scell_number)
        resp = self.check_cell_state(scell_number, "AGGR", 5)
        if resp:
            self.log.info("add scc%d successfully"%scell_number)
            return True
        else:
            self.log.error("add scc%d unsuccessfully"%scell_number)
            return False
    def add_scells(self,scell_numbers):
        if scell_numbers == 1:
            self.write("BSE:CONFig:LTE:CELL1:CAGGregation:AGGRegate:SCC:LIST CELL2")
        elif scell_numbers ==2:
            self.write("BSE:CONFig:LTE:CELL1:CAGGregation:AGGRegate:SCC:LIST CELL2,CELL3")
        elif scell_numbers ==3:   
            self.write("BSE:CONFig:LTE:CELL1:CAGGregation:AGGRegate:SCC:LIST CELL2,CELL3,CELL4")
        for i in range(scell_numbers):
            resp = self.check_cell_state(i+2, "AGGR", 5)
            if not resp:
                self.log.error("add %scc unsuccessfully"%scell_numbers)
                self.fwk.Print("add %scc unsuccessfully"%scell_numbers)
                return False
        self.log.info("add %dscc successfully"%scell_numbers)
        self.fwk.Print("add %dscc successfully"%scell_numbers)
        return True
      
    def active_scells(self,scell_numbers):
        if scell_numbers == 1:
            self.write("BSE:CONFig:LTE:CELL1:CAGGregation:ACTivate:SCC:LIST CELL2")
        elif scell_numbers ==2:
            self.write("BSE:CONFig:LTE:CELL1:CAGGregation:ACTivate:SCC:LIST CELL2,CELL3")
        elif scell_numbers ==3:   
            self.write("BSE:CONFig:LTE:CELL1:CAGGregation:ACTivate:SCC:LIST CELL2,CELL3,CELL4")
        for i in range(scell_numbers):
            resp = self.check_cell_state(i+2, "ACT", 5)
            if not resp:
                self.log.error("ACTivate d%scc unsuccessfully"%scell_numbers)
                return False
        self.log.info("ACTivate %dscc successfully"%scell_numbers)
        return True  
                  
    def active_scell(self,scell_number):
        self.log.info('add scell%d'%scell_number)
        self.inst.write("BSE:CONFig:LTE:CELL1:CAGGregation:ACTivate:SCC:LIST CELL%d"%scell_number) 
        resp = self.check_cell_state(scell_number, "ACT", 5)
        if resp:
            self.log.info("active scc%d successfully"%scell_number)
            return True
        else:
            self.log.error("active scc%d unsuccessfully"%scell_number)
            return False    
    
    def deactive_scell(self,scell_number):##TBD
        pass
    
    def delete_scell(self):## TBD
        pass
    
    def start_measure_tput(self):
        self.write("BSE:MEASure:LTE:CELL1:BTHRoughput:STATe 1")
        res = self.query("BSE:MEASure:LTE:CELL1:BTHRoughput:STATe?")
        if res == "1":
            self.log.info("tput measure stop successfully")
            return True
        return False
        
    def stop_measure_tput(self):
        self.write("BSE:MEASure:LTE:CELL1:BTHRoughput:STATe 0")
        res = self.query("BSE:MEASure:LTE:CELL1:BTHRoughput:STATe?")
        if res == "0":
            self.log.info("tput measure stop successfully")
            return True
        return False
    def read_DL_TPUT_Mulitcells(self,tar_cell_nums):
        DL_tput = []
        for i in range(tar_cell_nums):
            tput = self.read_DL_Tput(i+1)
#             self.fwk.Print("dl tput is",tput)
            DL_tput.append(tput)
        return DL_tput
    
    def read_DL_BLER_Mulitcells(self,tar_cell_nums):
        DL_bler = []
        for i in range(tar_cell_nums):
            self.log.info("get dl bler")
#             self.fwk.Print("#########%^(*&(*(",tar_cell_nums)
            bler = self.read_DL_Bler(i+1)
            DL_bler.append(bler)
            self.log.info("DL bler is %s"%DL_bler)
        return DL_bler

    
#     def query(self, cmd):## TBD
#         res = self.ask(cmd + "?", delay)
#         return res
    def open_MAC_PADDing_DL(self,tar_cell_num):
        for i in range(tar_cell_num):
            self.inst.write("BSE:CONFig:LTE:CELL%d:MAC:DL:PADDing:STAte 1"%(i+1))
            resp = self.query("BSE:CONFig:LTE:CELL%d:MAC:DL:PADDing:STAte?"%(i+1))
            if resp != "1":
                self.log.info("close MAC PADDing  successfully")
                return False
        return True

    def close_MAC_PADDing_DL(self,tar_cell_num):
        for i in range(tar_cell_num):
            self.inst.write("BSE:CONFig:LTE:CELL%d:MAC:DL:PADDing:STAte 0"%(i+1))
            resp = self.query("BSE:CONFig:LTE:CELL%d:MAC:DL:PADDing:STAte?"%(i+1))
            if resp !="0":
                self.log.info("close MAC PADDing  successfully")
                return False
        return True
    def open_MAC_PADDing_UL(self,tar_cell_num):
        for i in range(tar_cell_num):
            self.inst.write("BSE:CONFig:LTE:CELL%d:MAC:UL:PADDing:STAte 1"%(i+1))
            resp = self.query("BSE:CONFig:LTE:CELL%d:MAC:DL:PADDing:STAte?"%(i+1))
            if resp !="1":
                self.log.info("close MAC PADDing  successfully")
                return False
        return True

    def close_MAC_PADDing_UL(self,tar_cell_num):
        for i in range(tar_cell_num):
            self.inst.write("BSE:CONFig:LTE:CELL%d:MAC:UL:PADDing:STAte 0"%(i+1))
            resp = self.query("BSE:CONFig:LTE:CELL%d:MAC:DL:PADDing:STAte?"%(i+1))
            if resp !="0":
                self.log.info("close MAC PADDing  successfully")
                return False
        return True
#### function for NSA command not verify##############
    def init_cell_NSA(self,cells_parameter,test_channel): ### TBD
        self.log.info("initialize NSA cells")
        LTEcell_num = 1
        NRcell_num = 1
        self.pcell = "band%s"%cells_parameter[0][1]
        try:
            for cell_parameter_list in cells_parameter:
                if "n" in str(cell_parameter_list[1]):
                    self.config_NR_cell(NRcell_num, cell_parameter_list,test_channel)
                    NRcell_num = NRcell_num +1
                else:
                    self.config_lte_cell(LTEcell_num, cell_parameter_list)
                    LTEcell_num = LTEcell_num +1
        except Exception as e:
            self.log.info("initialize nsa cell fail as %s"%e)
            return False                                      
        return True
    def active_cells_NSA(self,lte_cell_num,NR_cell_num):
        
        for i in range(lte_cell_num):
            resp1 = self.active_cells(i+1)
        for j in range(NR_cell_num):
            resp2 = self.active_cells_NR(j+1)
        if resp1 and resp2:
            return True
        return False
    
    def config_NR_cell(self,cell_num,cell_parameter_list,test_channel):
            self.log.info("#######cell_Parameter list is  %s",cell_parameter_list)
#             self.fwk.Print("#####debug")
            if cell_parameter_list[1] in ["n257","n258","n261","n260"]:
                self.write("BSE:CONFig:NR5G:FREQuency:RANGE FR2")
            else:
                self.write("BSE:CONFig:NR5G:FREQuency:RANGE FR1")
            self.sleep(5)
            self.write("BSE:CONFig:NR5G:CELL%d:DUPLex:MODE %s"%(cell_num,(cell_parameter_list[0])))### set cell1 duplex mode
#             self.log.info("set DUPLex mode")
            self.sleep(5) 
            self.write("BSE:CONFig:NR5G:CELL%d:BAND %s"%(cell_num,cell_parameter_list[1]))
#             self.write("BSE:CONFig:NR5G:CELL1:BAND n78")
            self.sleep(3)
            if "FDD" in cell_parameter_list[0]:
                self.write("BSE:CONFig:NR5G:CELL1:SUBCarrier:SPACing:COMMon MU0")
            else:
                self.write("BSE:CONFig:NR5G:CELL1:SUBCarrier:SPACing:COMMon MU1")
            self.sleep(5)
#             self.fwk.Print(type(cell_parameter_list[2]))
#             self.write("BSE:CONFig:NR5G:CELL%d:DL:ARFCN %s"%(cell_num,cell_parameter_list[2]))
#             self.sleep(2)
            if  cell_parameter_list[0] == "TDD":
                self.write("BSE:CONFig:NR5G:CELL%d:DL:BW BW%s"%(cell_num,int(self.cfg["NR_TDD_BW"])))
            elif cell_parameter_list[0] == "FDD":
                self.write("BSE:CONFig:NR5G:CELL%d:DL:BW BW%s"%(cell_num,int(self.cfg["NR_FDD_BW"])))
                
            self.sleep(2) 
            self.write("BSE:CONFig:NR5G:CELL1:TESTChanLoc %s"%test_channel)
            self.sleep(2)
            if self.cfg["mimo_list"] != "":
                if self.cfg["mimo_list"][-1]== "4":
                    self.write("BSE:CONfig:NR5G:CELL1:DL:MIMO:CONfig N4X4")
                elif self.cfg["mimo_list"][-1] == "2":
                    self.write("BSE:CONfig:NR5G:CELL1:DL:MIMO:CONfig N2X2")
            else:
                self.write("BSE:CONfig:NR5G:CELL1:DL:MIMO:CONfig N2X2")
            self.cells_reconfigure("NR5G")

    def read_DL_Tput_NR(self,tar_cell):
        self.log.info('get dl Tput on cell%s'%tar_cell)
        resp = self.query("BSE:NR5G:MEASure:BTHRoughput:DL:THRoughput:OTA:CELL%s?"%tar_cell)
        return resp
    
    def read_UL_Tput_NR(self,tar_cell = 1):
        UL_tput = []
        self.log.info('get ul Tput on cell%s'%tar_cell)
        resp = self.query("BSE:NR5G:MEASure:BTHRoughput:UL:THRoughput:OTA:CELL%s?"%tar_cell)
        UL_tput.append(resp)
        return UL_tput
    
    def read_UL_Bler_NR(self,tar_cell = 1):
        UL_bler = []
        self.log.info('get ul bler on cell%s'%tar_cell)
        resp = self.query("BSE:NR5G:MEASure:BTHRoughput:UL:BLER:CELL%s?"%tar_cell)
        UL_bler.append(resp)
        self.log.info("nr UL bler is %s"%UL_bler)
        return UL_bler
    
    def read_DL_Bler_NR(self,tar_cell = 1):
        self.log.info('get dl bler on cell%s'%tar_cell)
        resp = self.query("BSE:NR5G:MEASure:BTHRoughput:DL:BLER:CELL%s?"%tar_cell)
        return resp
    
    def add_scell_NR(self,scell_number = 2):##TBD
        self.log.info('add scc%d'%scell_number)
        resp = self.query("BSE:CONFig:LTE:CELL1:CAGGregation:AGGRegate:SCC:LIST CELL%d"%scell_number)
        if resp:
            self.log.info("add scc%d successfully"%scell_number)
            return True
        else:
            self.log.info("add scc%d unsuccessfully"%scell_number)
            return False
    def active_scell_NR(self,scell_number):### TBD
        self.log.info('add scell%d'%scell_number)
        resp = self.query("BSE:CONFig:LTE:CELL1:CAGGregation:ACTivate:SCC:LIST CELL%d"%scell_number) 
        if resp:
            self.log.info("active scc%d successfully"%scell_number)
            return True
        else:
            self.log.info("active scc%d unsuccessfully"%scell_number)
            return False    
    
    def deactive_scell_NR(self,scell_number):##TBD
        pass
    
    def delete_scell_NR(self):## TBD
        pass
    
    def start_measure_tput_NR(self):
        self.write("BSE:NR5G:MEASure:BTHRoughput:STATe 1")
        res = self.query("BSE:NR5G:MEASure:BTHRoughput:STATe?")
        if res == "1":
            self.log.info("tput measure stop successfully")
            return True
        return False
        
    def stop_measure_tput_NR(self):
        self.write("BSE:NR5G:MEASure:BTHRoughput:STATe 0")
        res = self.query("BSE:NR5G:MEASure:BTHRoughput:STATe?")
        if res == "0":
            self.log.info("tput measure stop successfully")
            return True
        return False
    
    def read_DL_TPUT_Mulitcells_NR(self,tar_cell_nums):
        DL_tput = []
        for i in range(tar_cell_nums):

            tput = self.read_DL_Tput_NR(i+1)
#             self.fwk.Print("dl tput is",tput)
            DL_tput.append(tput)
        return DL_tput
    
    def read_DL_BLER_Mulitcells_NR(self,tar_cell_nums):
        DL_bler = []
        for i in range(tar_cell_nums):
            self.log.info("get dl bler")
#             self.fwk.Print("#########%^(*&(*(",tar_cell_nums)
 
            bler = self.read_DL_Bler_NR(i+1)
            DL_bler.append(bler)
        return DL_bler


    def active_cells_NR(self, tar_cell = 1):
        self.set_timeout(30000)
        self.log.info("active nr cells")
        self.fwk.Print("active nr cells")
        for i in range(3):###try three times 
            self.log.info("active cell%d"%int(tar_cell))
            self.query("BSE:CONFig:NR5G:CELL%d:ACTive 1;*OPC?"%int(tar_cell))
            resp = self.check_cell_state_NR(tar_cell, "ON",20)
            if not resp:
                continue 
               
            return resp
     
    def deactive_cells_NR(self,tar_cell = 1):
        for i in range(3):
            self.log.info("deactive cell%d"%int(tar_cell))
            self.query("BSE:CONFig:NR5G:CELL%d:ACTive 0;*OPC?"%int(tar_cell))
            resp = self.check_cell_state_NR(tar_cell, "OFF")
            if resp:
                return resp
            self.sleep(5) 
        return resp
     
    def deactive_cells_mulit_NR(self,cells_num):
        self.log.info("deactive all the actived cells")
        self.fwk.Print("deactive all the NR actived cells")
        for i in range(int(cells_num)):
            res1 = self.check_cell_state_NR(int(i+1), 'ON',5)
            if res1: 
                res2 = self.deactive_cells_NR(int(i+1))
                if not res2:
                    self.log.error("cell%d deactive unsuccessfully"%i)
                    i = i+1
            self.sleep(5)     
    
    def check_cell_state_NR(self,tar_cell = 1,tar_state = 'ON',timeout = 20):##ON OFF IDLE ACT CONN  AGG
        end_time =  timeout + time.time()
        while  time.time() < end_time:
            resp = self.query("BSE:STATus:NR5G:CELL%d?"%int(tar_cell))
            if tar_state in resp:
                return True
            self.sleep(2)
        return False 
    
    def nr_scell_aggregation(self,tar_cell = 1):
        self.log.info("add nr cell to lte")
        self.fwk.Print("add nr cell to lte")
        self.inst.write("BSE:CONFig:LTE:CELL1:CAGGregation:NRCC:DL CELL%d"%int(tar_cell))
        self.inst.write("BSE:CONFig:LTE:CELL1:CAGGregation:NRCC:APPly")
        self.sleep(5)
        resp = self.check_cell_state_NR(tar_cell, "CONN", 10)
        if resp:
            self.log.info("add NR cell successfully")
            return True
        self.log.error("add NR cell unsuccessfully")
        return False

    def deactive_cells_NSA(self,lte_cell_num,nr_cell_num):
        self.log.info("deactive NSA cell")
        self.fwk.Print("deactive NSA cell")
        self.deactive_cells_mulit_NR(nr_cell_num)
#         self.sleep(5)
        self.deactive_cells_mulit(lte_cell_num)
        
        
    def load_asn_message(self,asn_list_file,asn_name):

        self.write("BSE:CONFig:LTE:RRC:REConfig:ASN:LOAD:LIST '%s'"%asn_list_file)
        time.sleep(2)
        self.write("BSE:CONFig:LTE:CELL1:RRC:REConfig:ASN:LOAD:MSG '%s'"%asn_name)

# load_asn_message('D:\lenovo\ASN Favourite Lists\8CC_8D_4U.xml',"Sub6_1CC_V9")
    def send_asn_message(self,asn_name):
        self.write("BSE:CONFig:LTE:CELL1:RRC:REConfig:ASN:SEND:MSG '%s'"%asn_name) 
        
        
        
        
    def set_mimo(self,mimo_type):####  to be done modify by weidehui
        self.write("")
    
    def cells_reconfigure(self,rat_type):
        self.log.info("reconfigure %s cells"%rat_type)
        self.fwk.Print("reconfigure %s cells"%rat_type)
        scpi_command_path = os.path.join(self.cfg["scpi_command"],self.cfg["scpi_command_extra_name"])
        f = open(scpi_command_path,"r")
        for line in f.readlines():
            if line[0]== "#":
                continue
            if rat_type in line:
                self.write(line)
        f.close()
        
class XApps(object):###ADD by weidehui on 2020-04-29
    def __init__(self,fwk,tcpip):
#         super(KeySightUXM,self).__init__()
        rm=visa.ResourceManager()
#         self.tcpip = "TCPIP0::%s::%s::SOCKET"%(ip_addr,port)
        self.log.info("connect to keysight X-Apps :%s"%tcpip)
        self.fwk.Print("connect to keysight X-Apps :%s"%tcpip)
        try:
            self.inst = rm.open_resource(tcpip)
        except Exception as e:
            self.log.info("can't connect to xapp")
            self.fwk.Print("can't connect to xapp")
              
#         self.log = Log(__name__).getlog() 
        self.fwk = fwk
        self.log = fwk.log 
        self.inst.timeout = 20000
        self.inst.read_termination = "\n"
        self.cfg = self.fwk.cfg
    def write(self,cmd):
        try:
            self.log.info("SCPI COMMAND : %s"%cmd)
            self.fwk.Print("SCPI COMMAND : %s"%cmd)
            self.inst.write(str(cmd))

            return True
        except:
            return False
        self.sleep(5)

    def query(self,cmd):
        self.log.info("SCPI COMMAND :%s"%cmd)
        self.fwk.Print("SCPI COMMAND : %s"%cmd)
        return self.inst.query(str(cmd))  
         
    def read(self,cmd):
        try:
            self.log.info("SCPI COMMAND :%s"%cmd)
            self.fwk.Print("SCPI COMMAND : %s"%cmd)
            res = self.inst.read(str(cmd))

            return res
        except:
            return False
        
    
    def sleep(self,timeout):
        self.log.info("sleep %d second"%int(timeout))
        self.fwk.Print("sleep %d second"%int(timeout))
        time.sleep(int(timeout)) 
        