# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 18:21:59 2019

@author: weidh2

"""

import time
import visa
import re
# import Output_Log
# from Output_Log import  *
from logging import Logger
from fwk.QCOM import *
import xlwt
import xlrd
import tkinter
from tkinter import filedialog
from tkinter import messagebox
import time
# from KeySightUXM import KeySightUXM
from devices import KeySightUXM
from devices import XAPPS
# from Output_Log import Log
import csv
import main
import os 
class Modem_CA_Verify_Keysight(object):
    
    def __init__(self,fwk):
#         super (Modem_CA_Verify_Keysight,self).__init__()

        self.log = fwk.log
        self.log.info("*** module Modem_CA_Verify_Keysight constructor")
        self.fwk = fwk
        self.cfg = self.fwk.cfg
#         print("self_config is %s"%self.cfg)
        self.ca_combs = []
        self.log.info(self.cfg["repeat_while_fail"])
        self.test_channel = "N/A"
        self.print = fwk.Print
        self.tx_power_lte = ""
        self.tx_power_nr = ""
#         fwk.attach(self)

#         self.setupPhone()
    
#         self.log = Logger("CA_TEST")
#         self.log = Log(__name__).getlog()
        
# 
#3gpp        '1C':(1,201,20),'1CC':(1,399,20),
#3gpp        '2A':(2,700,20),'2AA':(2,1100,20),
#3gpp        '2C':(2,700,20),'2CC':(2,898,20),
#3gpp        '3A':(3,1300,20),'3AA':(3,1850,20),
#3gpp        '3C':(3,1300,20),'3CC':(3,1498,20),
#3gpp        '4A':(4,2050,20),'4AA':(4,2300,20),
#3gpp        '5A':(5,2450,10),'5AA':(5,2600,10),'5B':(5,2450,10),'5BB':(5,2549,10),
#3gpp        '7A':(7,2850,20),'7AA':(7,3350,10),'7C':(7,2850,20),'7CC':(7,3028,20),'7B':(7,3327,15),'7BB':(7,3420,5),
#3gpp        '8A':(8,3625,10), '8B':(8,3651,10), '8BB':(8,3750,10),       
#3gpp        '12A':(12,5035,5),'12AA':(12,5155,5),'12B':(12,5038,5),'12BB':(12,5110,10),
#3gpp        '13A':(13,5230,10),
#3gpp        '17A':(17,5790,10),
#3gpp        '18A':(18,5925,10),
#3gpp        '19A':(19,6075,10),
#3gpp        '20A':(20,6300,10),
#3gpp        '25A':(25,8140,20),'25AA':(25,8590,20),
#3gpp        '26A':(26,8990,10),
#3gpp        '28A':(28,9435,10),
#3gpp        '66A':(66,66536,20),'66AA':(66,67236,10),'66B':(66,66486,10),'66BB':(66,66585,10),'66C':(66,66536,20),'66CC':(66,66734,20),
#3gpp        '66D':(66,66536,20),'66DD':(66,66734,20),'66DDD':(66,66932,20),
#3gpp        '71A':(71,68765,10),
#3gpp        '41A':(41,39750,20),'41AA':(41,41490,20),'41C':(41,39750,20),'41CC':(41,39948,20),'41D':(41,40422,20),'41DD':(41,40620,20),'41DDD':(41,40818,20),
#3gpp        '40A':(40,39150,10),'40AA':(40,39600,10),'40C':(40,39249,20),'40CC':(40,39051,20),
#3gpp        '38A':(38,38000,10),'n5':("n5",100),'n66':('n66',100),'n41':('n41',100),'n71':('n71',100)
        self.CA_dic={'1A':(1,300,10),'1AA':(1,500,20),
         '1C':(1,201,20),'1CC':(1,399,20),
         '2A':(2,900,10),'2AA':(2,1150,10),'2C':(2,801,20),'2CC':(2,999,20),
         '3A':(3,1300,20),'3AA':(3,1775,20),
         '3C':(3,1481,10),'3CC':(3,1625,20),
         '4A':(4,2175,10),'4AA':(4,2350,10),
         '5A':(5,2476,10),'5B':(5,2476,10),'5BB':(5,2575,10),'5AA':(5,2600,10),
         '7A':(7,3100,10),'7AA':(7,3400,10),'7C':(7,3006,10),'7CC':(7,3150,20),'7B':(7,3076,15),'7BB':(7,3169,5),
         '8A':(8,3625,10),       
         '12A':(12,5095,10),'12B':(12,5048,5),'12BB':(12,5120,10),
         '13A':(13,5230,10),
         '14A':(14,5330,10),
         '17A':(17,5790,10),
         '18A':(18,5925,10),
         '19A':(19,6075,10),
         '20A':(20,6300,10),
         '25A':(25,8140,20),'25AA':(25,8590,20),
         '26A':(26,8990,10),
         '26AA':(26,8990,5),
         '28A':(28,9435,10),
         '29A':(29,9715,10),
         '30A':(30,9820,10),
         '32A':(32,10140,10),
         '38A':(38,38000,10),'38C':(38,37850,20),'38CC':(38,38048,20),
         '40A':(40,39150,10),'40AA':(40,39600,10),'40C':(40,39249,20),'40CC':(40,39051,20),'40D':(40,"38952",20),'40DD':(40,39150,20),"40DDD":(40,39348,20),
         "46A":(46,46890),"46AA":(46,54340,20),"46C":(46,50692,20),"46CC":(46,50890,20),"46D":(46,53942,20),"46DD":(46,54140,20),"46DDD":(46,54338,20),
         '66B':(66,66837,10),'66BB':(66,66936,10),'66A':(66,66486,10),'66AA':(66,67086,10),'66C':(66,66787,20),'66CC':(66,66985,20),
        '66D':(66,66688,20),'66DD':(66,66886,20),'66DDD':(66,67084,20),
         '71A':(71,68765,10),
         '41C':(41,40521,20),'41CC':(41,40719,20),'41A':(41,40620,20),'41AA':(41,41540,10),'41D':(41,40422,20),'41DD':(41,40620,20),'41DDD':(41,40818,20),
         '41E':(41,39705,10),'41EE':(41,39849,20),'41EEE':(41,41292,20),'41EEEE':(41,41490,20),
         'n1A':('n1',430000,20),'n2A':('n2',390000,20),'n3A':('n3',370000,20),'n5A':("n5",176800,20),'n7A':('n7',530000,20),'n66A':('n66',430000,20),'n41A':('n41',510000,20),'n71A':('n71',127400,20),
         'n28A':("n28",158600,20),"n78A":("n78",625996,20),"n25A":("n25",388000,20),"n12A":("n12",147300,20)}
        
        self.duplex_mode_dic={1:'FDD',2:"FDD",3:'FDD',4:'FDD',5:'FDD',12:'FDD',7:'FDD',8:'FDD',13:'FDD',14:'FDD',17:'FDD',18:'FDD',19:'FDD',20:'FDD',25:'FDD',
          26:'FDD',28:'FDD',29:'FDD',30:'FDD',34:'TDD',32:'FDD',38:'TDD',39:'TDD',40:'TDD',41:'TDD',46:"TDD",66:'FDD',71:'FDD',"n1":"FDD","n2":"FDD","n3":"FDD","n5":"FDD","n7":"FDD","n8":"FDD","n20":"FDD","n71":"FDD","n28":"FDD","n38":"TDD","n66":"FDD","n79":"TDD","n77":"TDD","n78":"TDD","n41":"TDD","n25":"FDD","n12":"FDD","n257":"TDD","n258":"TDD","n260":"TDD","n261":"TDD"}
        
        self.ca_comb_special = {"41C-41C":["41E","41EE","41EEE","41EEEE"],"66A-66A-66A":["66A","66AA","66C"],"3C-7C":["3C","3CC","7C","7CC"],"5B-46C":["5B","5BB","46C","46CC"],"5B-66B":["5B","5BB","66B","66BB"],"5B-66C":["5B","5BB","66C","66CC"],"25A-25A-26A":["25A","25AA","26AA"]}
        
        self.read_nr_band_from_config()
    def read_nr_band_from_config(self):
        for nr_band in self.cfg["nr_band_list"]:
            nr_band_key= nr_band + "A"
            nr_band_list = []
            nr_band_list.append(nr_band)
            self.CA_dic[nr_band_key]=nr_band_list
        self.log.info(self.CA_dic)   
    def load_ca_conf(self):
        root=tkinter.Tk()
        root.withdraw()
#         if self.cfg["ca_parameter_load_type"] == "auto":
#         CA_Excel_file = os.path.join(self.cfg["document_path"],self.cfg["ca_combs_name"])
#         else:
#         CA_Excel_file=tkinter.filedialog.askopenfilename(title="please open your conf file",filetypes = (("xls files","*.xls"),("all files","*.*")))
         
        CA_Excel=xlrd.open_workbook(self.fwk.CA_Excel_file)
#         CA_Excel=xlrd.open_workbook(CA_Excel_file)
        CA_Sheet=CA_Excel.sheet_by_index(0)
#         CA_Sheet= CA_Excel.sheet_by_name(self.cfg["CA_tpye"])
        return CA_Sheet
   
    def read_conf(self,CA_Sheet): 
        ncols = CA_Sheet.ncols
        self.log.info("nocol:%d",ncols)    
        for i in range(ncols): 
            ca_combo=CA_Sheet.col_values(i)
#             ca_combos_rename = self.rename_combos(ca_comb)
#             print (ca_combs)
            self.ca_combs.extend(ca_combo)####modify by weidehui on 2019 -11-02
        
#             self.rename_ca_combs(ca_combs,"CA_","%sCA-"%str(i+2)) 
#         CA_Result_file=CA_Excel_file.replace('.xls','_Result.xls')
    def get_mimo_list(self,combos):
        str = ""
        a =  combos.replace(" ","").split("-")
        print(a)
        for band in a:
            if "["in band:
                b = band.replace("]","").split("[")
                if b !="": 
                    str = str+b[1]
            mimo_list  = str.replace(",","")
            self.log.info(mimo_list)
        return mimo_list
            
        
    def rename_ca_combs(self,ca_combs,source_w,trage_w):
        for ca_comb in ca_combs:
            new_combs= ca_comb.replace('%s',"%s"%(source_w,trage_w))
            self.ca_combs.append(new_combs)
            
    def get_position(self,tar_w,ca_comb):
        j = 0
        for i in ca_comb:
            if str(tar_w) in i:
                return j
            j = j+1
        return None  
    def create_test_report_csv_report(self):
        self.open_test_report_csv_file()
        self.writer.writerow(["project_name","ca_comb","iteration","ca_comb_new","cells_parameter","NR_channel","pcell","mimo","Verdict","DL_TPUT/(Mbps)[average-tput]","UL_TPUT/(Mbps)[average-tput]","DL_BLER(%)","UL_BLER(%)","DL_TPUT_NR/(Mbps)[average-tput]","UL_TPUT_NR/(Mbps)[average-tput]","DL_BLER_NR/(%)","UL_BLER_NR/(%)","LTE_TX_POWER","NR_TX_POWER","error_info"])
        self.close_csv_report()
    
    def open_test_report_csv_file(self):######modify by weidehui on 2019-11-02
#         root_path = os.getcwd()
        csv_file = self.fwk.log_root  + "\\" + "CA_TEST" + ".csv"
        self.log.info("open CSV File:" + csv_file)
        self.fileDesc = open(csv_file, 'a', newline = "")
        self.writer = csv.writer(self.fileDesc, delimiter=',') 
    def print_verdict(self,ca_comb,ca_comb_new,cells_parameter):
        ####add by weidehui on 2020-04-21
 
        result_list = []
        j =0
        for data in [self.tput_dl,self.tput_ul,self.bler_dl,self.bler_ul,self.tput_dl_nr,self.tput_ul_nr,self.bler_dl_nr,self.bler_ul_nr]:
            if len(data)==0:
                result_list.append(data)
                continue
            data_new = self.transfer_data_type(data,j)
            result_list.append(data_new)
            j = j+1
        results_list = [self.cfg["ProjectName"],ca_comb,self.iterations,ca_comb_new,cells_parameter,self.test_channel,self.inst.pcell,self.cfg["mimo_list"],self.verdict] + result_list
        results_list.append(self.tx_power_lte)
        results_list.append(self.tx_power_nr)
        results_list.append(self.error_info)
        
        try:
            self.open_test_report_csv_file()
#             self.writer.writerow([self.cfg["ProjectName"],ca_comb,ca_comb_new,cells_parameter,self.inst.pcell,self.verdict,self.tput_dl,self.tput_ul,self.bler_dl,self.bler_ul,self.tput_dl_nr,self.tput_ul_nr,self.bler_dl_nr,self.bler_ul_nr,self.error_info])
            self.writer.writerow(results_list)
            self.close_csv_report()
        except Exception as e:
            self.log.error(e)
#             self.fwk.notify_a("VERDICT_PRINT",results_list)
        results_list.remove(self.cfg["ProjectName"])
        results_list.remove(ca_comb_new)
        results_list.remove(cells_parameter)
        results_list_new = []
        for data in results_list:
            data_new = str(data)
            results_list_new.append(data_new)
        self.fwk.Print("result list is %s"%results_list_new)
        self.fwk.notify_a("VERDICT_PRINT",results_list_new)
        
        self.fwk.Print("################ca_comb = %s #############"%ca_comb)
        self.fwk.Print("################pcell = %s ###############"%self.inst.pcell)
        self.fwk.Print("################iteration %s###################"%self.iterations)
        if self.test_channel and "n" in ca_comb:
            self.fwk.Print("#############nr channel %s####################"%self.test_channel)
        self.fwk.Print("################verdict = %s###################"%self.verdict)
#         print("DL_TPUT/(Mbps)[average-tput]:",result_list[0]) 
#         print("UL_TPUT/(Mbps)[average-tput]:",result_list[1])
#         print("DL_BLER(%):",result_list[2])
#         print("UL_BLER(%):",result_list[3])
#         print("DL_TPUT_NR/(Mbps)[average-tput]:",result_list[4])
#         print("UL_TPUT_NR/(Mbps)[average-tput]:",result_list[5])
#         print("DL_BLER_NR(%):",result_list[6])
#         print("UL_BLER_NR(%):",result_list[7])
        
        self.log.info("################ca_comb = %s #############"%ca_comb)
        self.log.info("################pcell = %s ###############"%self.inst.pcell)
        if self.test_channel:
            self.log.info("#############nr channel %s####################"%self.test_channel)
        self.log.info("################iteration %s###################"%self.iterations)
        self.log.info("################verdict = %s ###################"%self.verdict)
#         self.log.info("DL_TPUT/(Mbps)[average-tput]:",results_list[0]) 
#         self.log.info("UL_TPUT/(Mbps)[average-tput]:",results_list[1])
#         self.log.info("DL_BLER(%):",results_list[2])
#         self.log.info("UL_BLER(%):",results_list[3])
#         self.log.info("DL_TPUT_NR/(Mbps)[average-tput]:",results_list[4])
#         self.log.info("UL_TPUT_NR/(Mbps)[average-tput]:",results_list[5])
#         self.log.info("DL_BLER_NR(%):",results_list[6])
#         self.log.info("UL_BLER_NR(%):",results_list[7])
    def close_csv_report(self):
        self.fileDesc.close() 
       
       
    def sleep(self,timeout):
        self.log.info("sleep %d second"%int(timeout))
        self.fwk.Print("sleep %d second"%int(timeout))
        time.sleep(int(timeout))  
    
    def preset_data(self):
        self.tput_dl = ""
        self.tput_ul = ""
        self.bler_dl = ""
        self.bler_ul = ""
        self.tput_dl_nr = ""
        self.tput_ul_nr = ""
        self.bler_dl_nr = ""
        self.bler_ul_nr = "" 
    
    
    def rename_combos(self,ca_combos):### add by weidehui on 20200710 for mimo new combos type is B3C[4,4]-B7A[2]-n28A[2]
        combos_temp = ca_combos.replace(" ","")### ca temp is 3C[4,4]-7A[2]-n28A[2]
        combos_new = re.sub('\\[.*?\\]','',combos_temp)
        return combos_new
             
    def main(self):
#         for  i  in range(100):
#             j = str(i)
#         results_list = ["7A-40A","1","LOW","band7","PASS","{'cell1': 4.3860672, 'cell2': 1.600730947}","{'cell1': 9.765338400000001}","{'cell1': 0.0, 'cell2': 0.0}","{'cell1': 0.8}"]
#         self.fwk.notify_a("VERDICT_PRINT",results_list)
#         self.sleep(30)
        
        self.create_test_report_csv_report()
        self.fwk.Print("creat result excel")
        self.log.info("########################################")
        self.log.info("#########main starts#########")
        self.log.info("########################################")
        self.fwk.Print("######################################################")
        self.fwk.Print("#######################test start######################")
        self.fwk.Print("######################################################")

        ca_comb = ""
        ca_comb_new = ""
        
        try:
            self.inst = KeySightUXM.KeySightUXM(self.fwk,self.cfg["device_ta"])
            self.sleep(5)
            if self.cfg["is_tx_power_test"]:
                self.xapp = XAPPS.XApps(self.fwk,self.cfg["device_xapp_ip"])
            ca_sheet = self.load_ca_conf()####read conf from excel
            self.read_conf(ca_sheet) ###conf ca parameter 
        except Exception as e:
            self.fwk.Print("instrument connect fail please check HW connection and make sure TA and xapps have been opened")
            raise(e)
        
        
#         self.sleep(5)

        for ca_combo in self.ca_combs:
            if ca_combo == '':
                    continue
            ca_comb = self.rename_combos(ca_combo)
            self.fwk.Print(ca_comb)
            self.log.info("ca combos new name is %s"%ca_comb)
            self.cfg["mimo_list"] = self.get_mimo_list(ca_combo)
            self.fwk.Print(self.cfg["mimo_list"])
            self.log.info("ca combo is %s "%ca_comb)
            self.log.info("mimo list is %s"%self.cfg["mimo_list"])
#             continue
            ###add while to for pause stop and resue control
            while True:
                self.fwk.Print("into event control")
                if self.cfg["test_pause"]:
                    self.fwk.Print("test have been pasued")
                    self.sleep(10)
                elif self.cfg["test_stop"]:
                    self.fwk.Print("test have been stopped")
                    raise("test stop")
                else:
                    break
            self.log.info("##############################################\n")
            self.log.info("############################【%s】#######################\n"%ca_comb)
            self.log.info("#############################################\n")
            self.fwk.Print("################################################################\n")
            self.fwk.Print("################################【%s】###########################\n"%ca_comb)
            self.fwk.Print("#################################################################\n")
            self.iterations = 0
            self.verdict = "FAIL"
            try :
                self.tput_dl = ""
                self.tput_ul = ""
                self.bler_dl = ""
                self.bler_ul = ""
                self.tput_dl_nr = ""
                self.tput_ul_nr = ""
                self.bler_dl_nr = ""
                self.bler_ul_nr = ""
                self.error_info =[]
                cells_parameter = []


                print(ca_comb)
                if ca_comb not in self.ca_comb_special.keys():
                    ca_comb_new = self.get_cell_parameter_from_CA_combs(ca_comb)
                else: 
                    ca_comb_new = self.ca_comb_special[ca_comb]
#                 self.print_verdict(ca_comb,ca_comb_new)
#                 continue


                self.log.info("ca_comb_new.:%s"%ca_comb_new)
                for i in range(len(ca_comb_new)):
                    cell = list(self.CA_dic[ca_comb_new[i]])
                    cell.insert(0,self.duplex_mode_dic[cell[0]])
                    cells_parameter.append(cell)    
                self.fwk.Print("cells_parameter: %s"%cells_parameter)
                if "n" in ca_comb or "N" in ca_comb:
                    self.fwk.Print("test1")
                    if len(self.cfg["channel_config_nr"])==0:
                        self.cfg["channel_config_nr"]= ["LOW"]
                    self.fwk.Print("%s"%self.cfg["channel_config_nr"])
                    for self.test_channel in self.cfg["channel_config_nr"]:
                        self.fwk.Print("test2")
                        self.verdict = "FAIL"
                        self.procedure_NSA(cells_parameter,ca_comb,ca_comb_new)

                            
                else:
                    self.procedure_LTE_CA(cells_parameter,ca_comb,ca_comb_new)
                    if self.cfg["is_tx_power_test"]:
                        self.tx_power_mea_lte()
            except Exception as e:
                self.log.error('there are errors in test please check the setup and rerun error is %s'%e) 
                self.verdict = "ERROR"
                self.error_info.append("test error is %s please check the setup and rerun"%e)
                self.print_verdict(ca_comb,ca_comb_new,cells_parameter)
              

        self.cleanup() 
        self.log.info("#################################################")
        self.log.info("##########test finished#########################") 
        self.log.info("################################################")
        print("##################################################################")
        print("########################test finished##########################################")
        print("##################################################################")
        self.Print("##################################################################")
        self.Print("########################test finished##########################################")
        self.Print("##################################################################")
#         os.system("pause")
          
    def trigger_attach(self):
        self.log.info("trigger attach on UE")
        self.fwk.Print("trigger attach on UE")
        self.fwk.Print("%s"%self.cfg["manual"])
        if not self.cfg["manual"]:
            self.restart_phone(50)
        else:
            self.fwk.Print("resrart phone")
            self.fwk.notify("EVEN_RESTART_PHONE",None)
#             self.restart_phone_dialog()
            self.sleep(10)
            
#         for i in range(3):
#             self.switch_off_phone()
# #             self.sleep(2)
#             self.switch_on_phone()
# #             self.sleep(2)
# #         self.setupPhone()
        resp = self.inst.check_cell_state(1, "CONN",60)
        if resp:
            self.log.info("ue attach successfully")
            print("ue attach successfully")
            return True
        self.log.error("UE attach failed")
        print("UE attach failed")
        return False 
    
    
    def read_throughput(self,duration_time=20,cell_numbers = 1):
        self.log.info("read throughput in LTE CA mode")
        print("read throughput in LTE CA mode")
        self.inst.open_MAC_PADDing_DL(6)
        self.inst.open_MAC_PADDing_UL(1)
        self.inst.stop_measure_tput()
        self.sleep(2)
        self.inst.start_measure_tput()
        self.sleep(duration_time)
        self.tput_dl = self.inst.read_DL_TPUT_Mulitcells(cell_numbers)
        self.tput_ul = self.inst.read_UL_Tput(1) 
        self.bler_dl = self.inst.read_DL_BLER_Mulitcells(cell_numbers) 
        self.bler_ul = self.inst.read_UL_Bler(1)

    def read_throughput_NSA(self,duration_time=20,lte_cell_num =1,nr_cell_num =1):
        self.log.info("read throughput on NSA mode")
        print("read throughput on NSA mode")
        self.inst.open_MAC_PADDing_DL(6)
        self.inst.open_MAC_PADDing_UL(1)
        self.inst.stop_measure_tput()
        self.inst.stop_measure_tput_NR()
        self.sleep(2)
        
        self.inst.start_measure_tput()
        self.inst.start_measure_tput_NR()
        
        self.sleep(duration_time)
        
        self.tput_dl = self.inst.read_DL_TPUT_Mulitcells(lte_cell_num)
        self.tput_ul = self.inst.read_UL_Tput(1)
        self.bler_dl = self.inst.read_DL_BLER_Mulitcells(lte_cell_num)
        self.bler_ul = self.inst.read_UL_Bler(1)
        self.sleep(5)
        
        self.tput_dl_nr =self.inst.read_DL_TPUT_Mulitcells_NR(nr_cell_num)
        self.tput_ul_nr = self.inst.read_UL_Tput_NR(nr_cell_num)
        self.bler_dl_nr = self.inst.read_DL_BLER_Mulitcells_NR(nr_cell_num)
        self.bler_ul_nr = self.inst.read_UL_Bler_NR(nr_cell_num)
        
    def trigger_CA(self,scc_number):
        self.log.info("trigger %dCA"%(scc_number+1))
        print("trigger %dCA"%(scc_number+1))
#         self.inst.open_MAC_PADDing_DL(6)
#         self.inst.open_MAC_PADDing_UL(1)
        resp = self.inst.add_scells(scc_number)
        resp1 = self.inst.active_scells(scc_number)
        if not resp or not resp1:
            self.log.error("trigger CA failed")
            print("trigger CA failed")
            return False
        self.sleep(1)
        return True   
    def trigger_CA_NSA(self):
        self.log.info("trigger CA in NSA mode ") 
           

    def cleanup(self):
        self.log.info("preset device")
#         self.inst.deactive_cells_mulit(6)
#         self.inst.preset() 
#         self.switch_off_phone()
        self.inst.stop_measure_tput()
          
    def restart_phone(self,timeout):
        if not self.cfg["restart_phone"]:
            return
        self.log.info("restart phone")
        print("restart phone")

        for i in range(3):
            resp = os.system("adb reboot")
            self.sleep(20)
            if resp == 0:
                end_time = time.time() + timeout
                while time.time() < end_time:

                    resp1 = os.system("adb root")
                    self.sleep(10)
#                     self.sleep(2)
                    if resp1 == 0:
                        self.log.info("restart phone successfully")
                        print("restart phone successfully")
                        return True
        self.log.error("restart phone unsuccessfully")
        print("restart phone unsuccessfully")
        return False
        self.sleep(10)
        
    def switch_on_phone(self):
        if self.cfg["phone_control_method"] == "qualcomm":
            self.phone.connect_phone(self.qualcomm_port)
            self.phone.set_online_mode()
        else:
            os.system("adb root")
            self.sleep(5)
            ###airplane mode on
            os.system("adb shell settings put global airplane_mode_on 1")
            self.sleep(2)
            ###airplane mode off
            os.system("adb shell am broadcast -a android.intent.action.AIRPLANE_MODE")
            self.sleep(2)
            os.system("adb shell settings put global airplane_mode_on 0")
            self.sleep(2)
            os.system("adb shell am broadcast -a android.intent.action.AIRPLANE_MODE")
            self.sleep(2)
        
    def switch_off_phone(self):
        if self.cfg["phone_control_method"] == "qualcomm":
            self.phone.connect_phone(self.qualcomm_port)
            self.phone.set_FTM_mode()
        else:
            self.log.info("switch off phone")
            os.system("adb root")
            os.system("adb shell settings put global airplane_mode_on 1")
            os.system("adb shell am broadcast -a android.intent.action.AIRPLANE_MODE")
            self.sleep(5)
#         for ca_comb in ca_combs:
#             if "2CA" in ca_comb:

    def get_cell_parameter_from_CA_combs(self,ca_comb): 
        ca = ca_comb.replace('CA_','').replace(' ','').split("-")
        self.log.info("ca is %s"%ca)
#        del ca[0]
        ca_new = []
        ca_new.extend(ca)
        length = len(ca)
#         print(length)
        for index in range(length):
            self.log.info("ca_new is %s"%ca_new)
            self.log.info("ca is %s"%ca)
            if (ca[index][-1] == 'A'):
#             if (ca[index][-1] == 'A'):
                if (index > 0):
                    if (ca[index]) == ca[index-1]:
                        ca_new[index] = ca[index] + "A"

#            if (index > 0):
#                if (ca[index] == ca[index - 1]):
#                    ca[index] = ca[index]+ca[index][-1]

            elif (ca[index][-1] == 'B'):
                ca_new.insert((index + 1), (ca[index]+'B'))
            
            elif (ca[index][-1] == 'C'):
                ca_new.insert((index + 1), (ca[index]+'C'))

            elif (ca[index][-1] == 'D'):
                ca_new.insert((index + 1), (ca[index]+'D'))
                ca_new.insert((index + 2), (ca[index]+'DD'))
        return ca_new
    
    def transfer_data_type(self,datas,j):
        self.log.info("the data need to be transfer is %s"%datas)
        i=1
        float_data_dic ={}
#     a = ['4.900000000E+04,3.285600000E+07,3.285600000E+07,3.285600000E+07,3.285600000E+07,3.285600000E+07']
        for data in datas:
            float_data_list = []
            new_data_list = data.split(",")
    #         print(b)
            for new_data in new_data_list:
                new_data_float = float(new_data)/1000000
                
                float_data_list.append(new_data_float)
#                 print("############## float data is %s"%float_data_list)
            if j <2 or j ==4 or j==5:
                float_data_dic["cell%d"%i] = float_data_list[-2]
            elif j == 2 or j==6:
                float_data_dic["cell%d"%i] = (float_data_list[3]*100000000)
            elif j ==3 or j==7:
                float_data_dic["cell%d"%i] = (float_data_list[-1]*100000000)

#             float_data_dic["cell%d"%i] = float_data_list
            i = i+1
        return float_data_dic
    
    def setupPhone(self):
        self.log.info("Enter setupPhone fun, Create connection PC and Phone")
        try:
            self.phone = QCOM_phone(self.fwk)
            self.phone.initial_QMSL(bUseQPST)
            #鏍规嵁娴嬭瘯鏂瑰紡锛岃幏鍙栨寚瀹氱殑Qualcomm Port
            if(self.cfg["auto_get_qualcomm_port"]):## qualcomm port set
                tempPort = self.phone.get_phone_port_list()
                Qualcomm_port = tempPort[0]
                self.log.info("Auto to get phone num:%d"%Qualcomm_port)
#                 print("auto to get phone num:",Qualcomm_port)
            else:
                Qualcomm_port = self.cfg["qualcomm_port"]### modify by weidehui on 20191127
            self.qualcomm_port =  Qualcomm_port
            self.log.info("The current qualcomm port:%d"%Qualcomm_port)
            #鍒濆鍖朡ualcomm Port绔彛
            self.phone.connect_phone(Qualcomm_port)
            self.phone.set_FTM_mode()
            self.sleep(10)
            self.phone.set_online_mode()
            
#             self.log.info("Set FTM Mode OK")
        except Exception as err:
#             self.log.error("Set FTM Mode error")
            self.log.warning("Create Phone Connection Fail!!!,Error code:%s"%err)
            return
        
    def procedure_LTE_CA(self,cells_parameter,ca_comb,ca_comb_new):
        self.test_channel = "N/A"
        for count in range(len(cells_parameter)):######loop for Pcell
            self.iterations  = 0
            while True:
                self.preset_data()
                self.error_info =[]
#                         self.sleep(10)
#                         self.inst.preset(20)
#                         self.inst.Release_RRC_LTE()
#                 self.inst.deactive_cells_mulit(4)### modify by weidehui on 2020-07-31
                self.inst.deactive_cell1_loop()
                resp0 = self.inst.init_cell_lte(cells_parameter,count)                 
                if "skip" in resp0:
                    break  
                self.inst.active_cells_mulit(len(ca_comb_new))
                         
                resp1 = self.trigger_attach()
#             .            resp1 = True
                if resp1:
                    resp2 = self.trigger_CA(int(len(ca_comb_new)-1))
#                             resp2  = True
                    if resp2:
                        self.read_throughput(10, len(ca_comb_new))
                        self.verdict  = 'PASS'
                        
                        if self.cfg["is_tx_power_test"]:
                            self.tx_power_mea_lte()
                            self.tx_power_mea_NR()
                    else:
                        self.verdict  = 'FAIL'
                        self.error_info.append("trigger CA failed")   
                         
                else:###to modify 
                    self.log.error("UE attach failed")
                    print("UE attach failed")
                    self.error_info.append("UE attach failed")
                    self.verdict  = 'FAIL'
#                         self.switch_off_phone()####switch off UE to advice the reject from live network 
#                         self.switch_off_phone() 
                
                self.print_verdict(ca_comb,ca_comb_new,cells_parameter)
                        
                        
                if (self.verdict != "PASS" and self.cfg["repeat_while_fail"] and self.iterations < int(self.cfg["repeat_fail_max"])):
#                 if (self.verdict != "PASS" and self.cfg["repeat_while_fail"]):
                    self.iterations = self.iterations + 1
                    continue
                else:
                    break
            self.log.info(self.cfg["is_loop_pcell"])
            if not self.cfg["is_loop_pcell"]:####add by widehui on 20191025
                self.log.info("end loop for Pcell")
                break 
#                         if not self.cfg["is_loop_pcell"]:
#                         if True:
#                             break  
    def procedure_NSA(self,cells_parameter,ca_comb,ca_comb_new):
            self.error_info =[]
            self.iterations  = 0
            while True:
                resp0 = True
                resp1 = True
                resp2 = True
                resp3 = True
                resp4 = True
                resp5 = True
#                     self.inst.preset(10)
#                 self.inst.deactive_cells_NSA(4, 1)
                self.inst.deactive_cell1_loop()
                    
#                     resp0 = self.inst.init_cell_NSA(cells_parameter)
                    
#                     self.inst.load_asn_message('E:\share\8CC_8D_4U_withX55-7250.xml',"Sub6_1CC_forX55_V7_7250_ES4")### add by weidehui on 2019-11-21
#                     self.sleep(25)
                resp0 = self.inst.init_cell_NSA(cells_parameter,self.test_channel)
                
                    
#                     a = len(cells_parameter)-1
#                     print(a)
#                     self.sleep(25)
                resp1 = self.inst.active_cells_NSA(len(cells_parameter)-1, 1)
                        
                if resp1 and resp0:
                    resp2 = self.trigger_attach()
#                         resp2 = True
                    if resp2:
#                             resp3 = self.inst.send_asn_message("Sub6_1CC_forX55_V7_7250_ES4")
                        if len(cells_parameter)>2:
                                resp3 = self.trigger_CA(len(cells_parameter)-2)
                        if resp3:
                            resp4 = self.inst.nr_scell_aggregation(1)
                            if resp4:
                                resp5 = self.inst.check_cell_state_NR(1, "CONN", 20)
                                self.preset_data()

                                if resp5:
                                    self.read_throughput_NSA(10, len(cells_parameter)-1, 1) 
                                    self.verdict = "PASS"
                                    if self.cfg["is_tx_power_test"]:
                                        self.tx_power_mea_lte()
                                        self.tx_power_mea_NR()
#                             else:
#                                 self.read_throughput_NSA(20, len(cells_parameter)-1, 1)
#                                     self.verdict = "PASS"
                if not resp0 or not resp1:
                    self.log.error("init and active nsa cell failed")
                    print("init and active nsa cell failed")
                    self.error_info.append("init and active nsa cell failed")
                
                if not resp2:
                    self.log.error("LTE attach failed")
                    print("LTE attach failed")  
                    self.error_info.append("lte attach failed")      
                if not resp3:
                    self.log.error("add lte scell failed")
                    print("add lte scell failed")  
                    self.error_info.append("add lte scell failed")
                        
                if not resp4 or not resp5:        
                        self.log.error("add NR failed")
                        print("add NR failed")
                        self.error_info.append("add NR failed")
                

                    
                self.print_verdict(ca_comb,ca_comb_new,cells_parameter)
                if (self.verdict != "PASS" and self.cfg["repeat_while_fail"] and self.iterations < int(self.cfg["repeat_fail_max"])):
#                 if (self.verdict != "PASS" and self.cfg["repeat_while_fail"]):
                    self.iterations = self.iterations + 1
                    continue
                else:
                    break

    
    def tx_power_mea_lte(self):
        self.tx_power_lte = ""
        self.log.info("init lte cell parameter for tx power test")
        print("init lte cell parameter for tx power test")
        self.inst.write("BSE:SELected:CELL LTE, CELL1")
      
        self.inst.write("BSE:FUNC:LTE:TXM:SYNC")
        self.xapp.write("INIT:CONT OFF")
        self.xapp.write(":CHPower:AVERage OFF")
        self.xapp.write("INIT:CHP")
        try:
            tx_power = self.xapp.query("FETCH:CHPower:CHPower?")
        except:
            for i in range(3):
                tx_power = self.xapp.query("FETCH:CHPower:CHPower?")
        print(tx_power)
        self.tx_power_lte  = str(float(tx_power))
        print("lte tx power is %s"%self.tx_power_lte )
        return self.tx_power_lte
        
    
    def tx_power_measure_NSA(self):
        self
        pass
#
    def tx_power_mea_NR(self):
        self.tx_power_nr = ""
        self.log.info("init nr cell parameter for tx power test")
        print("init nr cell parameter for tx power test")
        self.inst.write("BSE:SELected:CELL NR5G, CELL1")
        
        self.inst.write("BSE:FUNC:LTE:TXM:SYNC")
        self.xapp.write("INIT:CONT OFF")
        self.xapp.write(":CHPower:AVERage OFF")
        self.xapp.write("INIT:CHP")
        try:
            tx_power = self.xapp.query("FETCH:CHPower:CHPower?")
        except:
            for i in range(3):
                tx_power = self.xapp.query("FETCH:CHPower:CHPower?")

        print(tx_power)
        self.tx_power_nr = str(float(tx_power))
        print("NR tx power is %s"%self.tx_power_nr)
def restart_phone_dialog(self):

    root=tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo("retart phone", "please restrt  your phone")
    print("continue")    
if __name__ == "__main__":
        #     pass
    fwk = main.TestFramework()
    test = Modem_CA_Verify_Keysight(fwk)
#     test.main()
    test.setupPhone()
#     test.setupPhone()




























