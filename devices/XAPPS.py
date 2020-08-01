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


class XApps(object):###ADD by weidehui on 2020-04-29
    def __init__(self,fwk,tcpip):
        self.log = fwk.log
        self.fwk= fwk
#         super(KeySightUXM,self).__init__()
        rm=visa.ResourceManager()
#         self.tcpip = "TCPIP0::%s::%s::SOCKET"%(ip_addr,port)
        self.log.info("connect to keysight X-Apps :%s"%tcpip)
        self.fwk.Print("connect to keysight X-Apps :%s"%tcpip)
        print("connect to keysight X-Apps :%s"%tcpip)
        try:
            self.inst = rm.open_resource(tcpip)
            self.fwk.Print("connect to Xapps successfully")
        except Exception as e:
            self.log.info("can't connect to xapp")
            self.fwk.Print("can't connect tp xapp")
            print("can't connect to xapp")
             
#         self.log = Log(__name__).getlog() 
        self.fwk = fwk
         
        self.inst.timeout = 20000
        self.inst.read_termination = "\n"
        self.cfg = self.fwk.cfg
    def write(self,cmd):
        try:
            self.log.info("SCPI COMMAND : %s"%cmd)
            print("SCPI COMMAND : %s"%cmd)
            self.inst.write(str(cmd))

            return True
        except:
            return False
        self.sleep(5)

    def query(self,cmd):
        self.log.info("SCPI COMMAND :%s"%cmd)
        print("SCPI COMMAND : %s"%cmd)
        return self.inst.query(str(cmd))  
         
    def read(self,cmd):
        try:
            self.log.info("SCPI COMMAND :%s"%cmd)
            print("SCPI COMMAND : %s"%cmd)
            res = self.inst.read(str(cmd))

            return res
        except:
            return False
        
    
    def sleep(self,timeout):
        self.log.info("sleep %d second"%int(timeout))
        time.sleep(int(timeout))
        
        