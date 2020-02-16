# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 18:21:59 2019

@author: lidz1
"""

import time
import visa
import pyvisa as visa
from devices.CMW500 import CMW500
# from CMW500.CMW500 import band_handover
# from CMW500.CMW500 import band_conf
# from CMW500.CMW500 import ber_search
# from CMW500.CMW500 import swtich_freq
# from CMW500.CMW500 import CA_PCC
# from CMW500.CMW500 import CA_SCC1
# from CMW500.CMW500 import CA_SCC2
# from CMW500.CMW500 import CA_Set
# from CMW500.CMW500 import CA3_Set
# from CMW500.CMW500 import CA_Init
# from CMW500.CMW500 import CA3_Init
# from CMW500.CMW500 import Read3_BLER
# from CMW500.CMW500 import Read_Throutput
import xlwt
import xlrd
import tkinter
from tkinter import filedialog
from tkinter import messagebox
   
    

class MeasureCA(object):
    def __init__(self,fwk):
        self.fwk = fwk
        self.log = fwk.log
        self.log.error("*** module MeasureCA constructor")
        self.cfg = fwk.cfg
        self.inst= CMW500()
        print("this CMW500 test setup")
        
    def main(self):
        root=tkinter.Tk()
        root.withdraw()
        
        CA_Excel_file=tkinter.filedialog.askopenfilename(title="请打开CA配置文件",filetypes = (("xls files","*.xls"),("all files","*.*")))
        CA_Excel=xlrd.open_workbook(CA_Excel_file)
        ##add by weidehui
        CA_Sheet=CA_Excel.sheet_by_index(0)
        ca_combo=CA_Sheet.col_values(0)
        CA_Result_file=CA_Excel_file.replace('.xls','_Result.xls')
        
        
        xlsout=xlwt.Workbook()
        sheet={}
        sheet[0]=xlsout.add_sheet(u'2CA测试结果',cell_overwrite_ok=True)
        sheet[1]=xlsout.add_sheet(u'3CA测试结果',cell_overwrite_ok=True)
        
        
        rm=visa.ResourceManager()
        ##RTB = rm.open_resource('TCPIP0::169.254.4.61::inst0::INSTR')
        GPIB = self.cfg["GPIB"]
#         RTB = rm.open_resource('GPIB0::20::INSTR')
        RTB = rm.open_resource(GPIB)
        RTB.timeout=20000
        
        
        
        
        
        CA_dic={'1A':(1,50,10),'1AA':(1,300,10),
                '1C':(1,201,20),'1CC':(1,399,20),
                '2A':(2,900,10),'2AA':(2,1150,10),'2C':(2,801,20),'2CC':(2,999,20),
                '3A':(3,1250,10),'3AA':(3,1575,10),
                '3C':(3,1703,20),'3CC':(3,1307,20),
                '2A':(2,900,10),'2AA':(2,1150,10),
                '4A':(4,2175,10),'4AA':(4,2350,10),
                '5A':(5,2476,10),'5B':(5,2476,10),'5BB':(5,2575,10),'5AA':(5,2600,10),
                '7A':(7,3100,10),'7AA':(7,3400,10),'7C':(7,3001,20),'7CC':(7,3199,20),'7B':(7,3076,15),'7BB':(7,3169,5),
                '8A':(8,3625,10),       
                '12A':(12,5095,10),'12B':(12,5048,5),'12BB':(12,5120,10),
                '13A':(13,5230,10),
                '17A':(17,5790,10),
                '18A':(18,5925,10),
                '19A':(19,6075,10),
                '20A':(20,6300,10),
                '25A':(25,8365,10),'25AA':(25,8640,10),
                '26A':(26,8990,10),
                '28A':(28,9435,10),
                '66B':(66,66837,10),'66BB':(66,66936,10),'66A':(66,66486,10),'66AA':(66,67086,10),'66C':(66,66787,20),'66CC':(66,66985,20),
               '66D':(66,66688,20),'66DD':(66,66886,20),'66DDD':(66,67084,20),
                '71A':(71,68765,10),
                '41C':(41,40521,20),'41CC':(41,40719,20),'41A':(41,40620,10),'41AA':(41,41540,10),'41D':(41,40422,20),'41DD':(41,40620,20),'41DDD':(41,40818,20),
                '40A':(40,39150,10),'40AA':(40,39600,10),'40C':(40,39249,20),'40CC':(40,39051,20),
                '38A':(38,38000,10)
                }
        FDTD_dic={1:'FDD',2:'FDD',3:'FDD',4:'FDD',5:'FDD',12:'FDD',7:'FDD',8:'FDD',13:'FDD',17:'FDD',18:'FDD',19:'FDD',20:'FDD',25:'FDD',
                  26:'FDD',28:'FDD',34:'TDD',38:'TDD',39:'TDD',40:'TDD',41:'TDD',66:'FDD',71:'FDD',}
        row_3ca=0
        row_2ca=0
        
        sheet[0].write(row_2ca,0,'CA')
        sheet[0].write(row_2ca,1,'PCC_BAND')
        sheet[0].write(row_2ca,2,'PCC_CHAN')
        sheet[0].write(row_2ca,3,'PCC_BW')
        sheet[0].write(row_2ca,4,'SCC_BAND')
        sheet[0].write(row_2ca,5,'SCC_CHAN')
        sheet[0].write(row_2ca,6,'SCC_BW')
        sheet[0].write(row_2ca,7,'Throughput')
        sheet[1].write(row_3ca,0,'CA')
        sheet[1].write(row_3ca,1,'PCC_BAND')
        sheet[1].write(row_3ca,2,'PCC_CHAN')
        sheet[1].write(row_3ca,3,'PCC_BW')
        sheet[1].write(row_3ca,4,'SCC1_BAND')
        sheet[1].write(row_3ca,5,'SCC1_CHAN')
        sheet[1].write(row_3ca,6,'SCC1_BW')
        sheet[1].write(row_3ca,7,'SCC2_BAND')
        sheet[1].write(row_3ca,8,'SCC2_CHAN')
        sheet[1].write(row_3ca,9,'SCC2_BW')
        sheet[1].write(row_3ca,10,'Throughput')
        sheet[1].write(row_3ca,11,'BLER')
        
        
        
        row_2ca=1
        row_3ca=1
        PCC_BAND=''
        SCC_BAND=''
        SCC2_BAND=''
        for CAcombo in ca_combo:
            ca=CAcombo.replace('CA_','').replace(' ','').split('-')
            if(len(ca)==3) :
                if(ca[0]==ca[1]):
                    ca[1]=ca[1]+'A'
                if(ca[2]==ca[1]):
                    ca[1]=ca[1]+'A'
                if(ca[2]==ca[0]):
                    ca[2]=ca[2]+'A'
                if(FDTD_dic[CA_dic[ca[0]][0]]==FDTD_dic[CA_dic[ca[1]][0]] and FDTD_dic[CA_dic[ca[1]][0]]==FDTD_dic[CA_dic[ca[2]][0]]):
         
                    if(FDTD_dic[CA_dic[ca[0]][0]]!=PCC_BAND or FDTD_dic[CA_dic[ca[1]][0]]!=SCC_BAND or FDTD_dic[CA_dic[ca[2]][0]]!=SCC2_BAND ):
                        PCC_BAND=FDTD_dic[CA_dic[ca[0]][0]]
                        SCC_BAND=FDTD_dic[CA_dic[ca[1]][0]]
                        SCC2_BAND=FDTD_dic[CA_dic[ca[2]][0]]
                        self.inst.CA3_Init(RTB,PCC_BAND,SCC_BAND,SCC2_BAND)
                        cnt=0
                    for cnt in range(3):
                            
                            self.CA3_Set(RTB,CA_dic[ca[cnt%3]][0],CA_dic[ca[cnt%3]][1],CA_dic[ca[cnt%3]][2],CA_dic[ca[(cnt+1)%3]][0],CA_dic[ca[(cnt+1)%3]][1],CA_dic[ca[(cnt+1)%3]][2],CA_dic[ca[(cnt+2)%3]][0],CA_dic[ca[(cnt+2)%3]][1],CA_dic[ca[(cnt+2)%3]][2])
                            res=self.inst.Read_Throutput(RTB)
                            sheet[1].write(row_3ca,0,CAcombo)
                            sheet[1].write(row_3ca,1,CA_dic[ca[(cnt)%3]][0])
                            sheet[1].write(row_3ca,2,CA_dic[ca[(cnt)%3]][1])
                            sheet[1].write(row_3ca,3,CA_dic[ca[(cnt)%3]][2])
                            sheet[1].write(row_3ca,4,CA_dic[ca[(cnt+1)%3]][0])
                            sheet[1].wcrite(row_3ca,5,CA_dic[ca[(cnt+1)%3]][1])
                            sheet[1].write(row_3ca,6,CA_dic[ca[(cnt+1)%3]][2])
                            sheet[1].write(row_3ca,7,CA_dic[ca[(cnt+2)%3]][0])
                            sheet[1].write(row_3ca,8,CA_dic[ca[(cnt+2)%3]][1])
                            sheet[1].write(row_3ca,9,CA_dic[ca[(cnt+2)%3]][2])
                            sheet[1].write(row_3ca,10,res[0])
                            sheet[1].write(row_3ca,11,res[1])
            
                        
                            row_3ca=row_3ca+1
                else:
                    if(FDTD_dic[CA_dic[ca[0]][0]]!=PCC_BAND or FDTD_dic[CA_dic[ca[1]][0]]!=SCC_BAND or FDTD_dic[CA_dic[ca[2]][0]]!=SCC2_BAND ):
                        PCC_BAND=FDTD_dic[CA_dic[ca[0]][0]]
                        SCC_BAND=FDTD_dic[CA_dic[ca[1]][0]]
                        SCC2_BAND=FDTD_dic[CA_dic[ca[2]][0]]
                        self.CA3_Init(RTB,PCC_BAND,SCC_BAND,SCC2_BAND)
                        cnt=0                   
                        self.CA3_Set(RTB,CA_dic[ca[cnt%3]][0],CA_dic[ca[cnt%3]][1],CA_dic[ca[cnt%3]][2],CA_dic[ca[(cnt+1)%3]][0],CA_dic[ca[(cnt+1)%3]][1],CA_dic[ca[(cnt+1)%3]][2],CA_dic[ca[(cnt+2)%3]][0],CA_dic[ca[(cnt+2)%3]][1],CA_dic[ca[(cnt+2)%3]][2])
                        res=self.inst.Read_Throutput(RTB)
                        sheet[1].write(row_3ca,0,CAcombo)
                        sheet[1].write(row_3ca,1,CA_dic[ca[(cnt)%3]][0])
                        sheet[1].write(row_3ca,2,CA_dic[ca[(cnt)%3]][1])
                        sheet[1].write(row_3ca,3,CA_dic[ca[(cnt)%3]][2])
                        sheet[1].write(row_3ca,4,CA_dic[ca[(cnt+1)%3]][0])
                        sheet[1].write(row_3ca,5,CA_dic[ca[(cnt+1)%3]][1])
                        sheet[1].write(row_3ca,6,CA_dic[ca[(cnt+1)%3]][2])
                        sheet[1].write(row_3ca,7,CA_dic[ca[(cnt+2)%3]][0])
                        sheet[1].write(row_3ca,8,CA_dic[ca[(cnt+2)%3]][1])
                        sheet[1].write(row_3ca,9,CA_dic[ca[(cnt+2)%3]][2])
                        sheet[1].write(row_3ca,10,res[0])
                        sheet[1].write(row_3ca,11,res[1])
                        row_3ca=row_3ca+1
            if(len(ca)==2) :
                if('B' in ca[0]):
                    ca.append(ca[0]+'B')
                if('B' in ca[1]):
                    ca.append(ca[1]+'B')
                if('C' in ca[0]):
                    ca.append(ca[0]+'C')
                if('C' in ca[1]):
                    ca.append(ca[1]+'C')
                #3CA
                if('B' in ca[0] or 'B' in ca[1] or 'C' in ca[0] or 'C' in ca[1]):
                    #3Ca  all fdd or all tdd
                    if(FDTD_dic[CA_dic[ca[0]][0]]==FDTD_dic[CA_dic[ca[1]][0]] and FDTD_dic[CA_dic[ca[1]][0]]==FDTD_dic[CA_dic[ca[2]][0]]):
                        if(FDTD_dic[CA_dic[ca[0]][0]]!=PCC_BAND or FDTD_dic[CA_dic[ca[1]][0]]!=SCC_BAND or FDTD_dic[CA_dic[ca[2]][0]]!=SCC2_BAND ):
                           PCC_BAND=FDTD_dic[CA_dic[ca[0]][0]]
                           SCC_BAND=FDTD_dic[CA_dic[ca[1]][0]]
                           SCC2_BAND=FDTD_dic[CA_dic[ca[2]][0]]
                           CA3_Init(RTB,PCC_BAND,SCC_BAND,SCC2_BAND)
                           cnt=0
                        for cnt in range(3):
                            
                            self.inst.CA3_Set(RTB,CA_dic[ca[cnt%3]][0],CA_dic[ca[cnt%3]][1],CA_dic[ca[cnt%3]][2],CA_dic[ca[(cnt+1)%3]][0],CA_dic[ca[(cnt+1)%3]][1],CA_dic[ca[(cnt+1)%3]][2],CA_dic[ca[(cnt+2)%3]][0],CA_dic[ca[(cnt+2)%3]][1],CA_dic[ca[(cnt+2)%3]][2])
                            res=self.inst.Read_Throutput(RTB)
                            sheet[1].write(row_3ca,0,CAcombo)
                            sheet[1].write(row_3ca,1,CA_dic[ca[(cnt)%3]][0])
                            sheet[1].write(row_3ca,2,CA_dic[ca[(cnt)%3]][1])
                            sheet[1].write(row_3ca,3,CA_dic[ca[(cnt)%3]][2])
                            sheet[1].write(row_3ca,4,CA_dic[ca[(cnt+1)%3]][0])
                            sheet[1].write(row_3ca,5,CA_dic[ca[(cnt+1)%3]][1])
                            sheet[1].write(row_3ca,6,CA_dic[ca[(cnt+1)%3]][2])
                            sheet[1].write(row_3ca,7,CA_dic[ca[(cnt+2)%3]][0])
                            sheet[1].write(row_3ca,8,CA_dic[ca[(cnt+2)%3]][1])
                            sheet[1].write(row_3ca,9,CA_dic[ca[(cnt+2)%3]][2])
                            sheet[1].write(row_3ca,10,res[0])
                            sheet[1].write(row_3ca,11,res[1])
                            row_3ca=row_3ca+1
                    else:
                           if(FDTD_dic[CA_dic[ca[0]][0]]!=PCC_BAND or FDTD_dic[CA_dic[ca[1]][0]]!=SCC_BAND or FDTD_dic[CA_dic[ca[2]][0]]!=SCC2_BAND ):
                               PCC_BAND=FDTD_dic[CA_dic[ca[0]][0]]
                               SCC_BAND=FDTD_dic[CA_dic[ca[1]][0]]
                               SCC2_BAND=FDTD_dic[CA_dic[ca[2]][0]]
                               CA3_Init(RTB,PCC_BAND,SCC_BAND,SCC2_BAND)
                           cnt=0                   
                           CA3_Set(RTB,CA_dic[ca[cnt%3]][0],CA_dic[ca[cnt%3]][1],CA_dic[ca[cnt%3]][2],CA_dic[ca[(cnt+1)%3]][0],CA_dic[ca[(cnt+1)%3]][1],CA_dic[ca[(cnt+1)%3]][2],CA_dic[ca[(cnt+2)%3]][0],CA_dic[ca[(cnt+2)%3]][1],CA_dic[ca[(cnt+2)%3]][2])
                           res=self.inst.Read_Throutput(RTB)
                           sheet[1].write(row_3ca,0,CAcombo)
                           sheet[1].write(row_3ca,1,CA_dic[ca[(cnt)%3]][0])
                           sheet[1].write(row_3ca,2,CA_dic[ca[(cnt)%3]][1])
                           sheet[1].write(row_3ca,3,CA_dic[ca[(cnt)%3]][2])
                           sheet[1].write(row_3ca,4,CA_dic[ca[(cnt+1)%3]][0])
                           sheet[1].write(row_3ca,5,CA_dic[ca[(cnt+1)%3]][1])
                           sheet[1].write(row_3ca,6,CA_dic[ca[(cnt+1)%3]][2])
                           sheet[1].write(row_3ca,7,CA_dic[ca[(cnt+2)%3]][0])
                           sheet[1].write(row_3ca,8,CA_dic[ca[(cnt+2)%3]][1])
                           sheet[1].write(row_3ca,9,CA_dic[ca[(cnt+2)%3]][2])
                           sheet[1].write(row_3ca,10,res[0])
                           sheet[1].write(row_3ca,11,res[1])
                           row_3ca=row_3ca+1
                else:
                    if(ca[0]==ca[1]): ca[1]=ca[1]+'A'
                    if(FDTD_dic[CA_dic[ca[0]][0]]!=PCC_BAND or FDTD_dic[CA_dic[ca[1]][0]]!=SCC_BAND ):
                       PCC_BAND=FDTD_dic[CA_dic[ca[0]][0]]
                       SCC_BAND=FDTD_dic[CA_dic[ca[1]][0]]
        #               SCC2_BAND=FDTD_dic[CA_dic[ca[2]][0]]
                       self.inst.CA_Init(RTB,PCC_BAND,SCC_BAND)
                       cnt=0
                       self.inst.CA_Set(RTB,CA_dic[ca[cnt%2]][0],CA_dic[ca[cnt%2]][1],CA_dic[ca[cnt%2]][2],CA_dic[ca[(cnt+1)%2]][0],CA_dic[ca[(cnt+1)%2]][1],CA_dic[ca[(cnt+1)%2]][2])
        
                    else:
                        self.inst.CA_Set(RTB,CA_dic[ca[cnt%2]][0],CA_dic[ca[cnt%2]][1],CA_dic[ca[cnt%2]][2],CA_dic[ca[(cnt+1)%2]][0],CA_dic[ca[(cnt+1)%2]][1],CA_dic[ca[(cnt+1)%2]][2])
        
                    if(PCC_BAND!=SCC_BAND):RANGE_cnt=1
                    else:RANGE_cnt=2
                    for cnt in range(RANGE_cnt):
                         res=self.inst.Read_Throutput(RTB)
                         sheet[0].write(row_2ca,0,CAcombo)
                         sheet[0].write(row_2ca,1,CA_dic[ca[(cnt)%2]][0])
                         sheet[0].write(row_2ca,2,CA_dic[ca[(cnt)%2]][1])
                         sheet[0].write(row_2ca,3,CA_dic[ca[(cnt)%2]][2])
                         sheet[0].write(row_2ca,4,CA_dic[ca[(cnt+1)%2]][0])
                         sheet[0].write(row_2ca,5,CA_dic[ca[(cnt+1)%2]][1])
                         sheet[0].write(row_2ca,6,CA_dic[ca[(cnt+1)%2]][2])
                         sheet[0].write(row_2ca,7,res[0])
                         sheet[0].write(row_2ca,8,res[1])
                         row_2ca=row_2ca+1
            if(len(ca)==1):
                if('D'in ca[0]):
                     ca.append(ca[0]+'D')
                     ca.append(ca[0]+'DD')
                if('B' in ca[0]):
                    ca.append(ca[0]+'B')
                if('C' in ca[0]):
                    ca.append(ca[0]+'C')
                #2CA
                if('B' in ca[0] or 'C' in ca[1]):
                         cnt=0
                         if(FDTD_dic[CA_dic[ca[0]][0]]!=PCC_BAND or FDTD_dic[CA_dic[ca[1]][0]]!=SCC_BAND):
                             PCC_BAND=FDTD_dic[CA_dic[ca[0]][0]]
                             SCC_BAND=FDTD_dic[CA_dic[ca[1]][0]]
                             self.inst.CA_Init(RTB,PCC_BAND,SCC_BAND)
                             self.inst.CA_Set(RTB,CA_dic[ca[cnt%2]][0],CA_dic[ca[cnt%2]][1],CA_dic[ca[cnt%2]][2],CA_dic[ca[(cnt+1)%2]][0],CA_dic[ca[(cnt+1)%2]][1],CA_dic[ca[(cnt+1)%2]][2])
        
                         else:
                             self.inst.CA_Set(RTB,CA_dic[ca[cnt%2]][0],CA_dic[ca[cnt%2]][1],CA_dic[ca[cnt%2]][2],CA_dic[ca[(cnt+1)%2]][0],CA_dic[ca[(cnt+1)%2]][1],CA_dic[ca[(cnt+1)%2]][2])                     
                         res=self.inst.Read_Throutput(RTB)
                         sheet[0].write(row_2ca,0,CAcombo)
                         sheet[0].write(row_2ca,1,CA_dic[ca[(cnt)%2]][0])
                         sheet[0].write(row_2ca,2,CA_dic[ca[(cnt)%2]][1])
                         sheet[0].write(row_2ca,3,CA_dic[ca[(cnt)%2]][2])
                         sheet[0].write(row_2ca,4,CA_dic[ca[(cnt+1)%2]][0])
                         sheet[0].write(row_2ca,5,CA_dic[ca[(cnt+1)%2]][1])
                         sheet[0].write(row_2ca,6,CA_dic[ca[(cnt+1)%2]][2])
                         sheet[0].write(row_2ca,7,res[0])
                         sheet[0].write(row_2ca,8,res[1])
                         row_2ca=row_2ca+1  
                if('D' in ca[0]):
                           if(FDTD_dic[CA_dic[ca[0]][0]]!=PCC_BAND or FDTD_dic[CA_dic[ca[1]][0]]!=SCC_BAND or FDTD_dic[CA_dic[ca[2]][0]]!=SCC2_BAND ):
                               PCC_BAND=FDTD_dic[CA_dic[ca[0]][0]]
                               SCC_BAND=FDTD_dic[CA_dic[ca[1]][0]]
                               SCC2_BAND=FDTD_dic[CA_dic[ca[2]][0]]
                               self.inst.CA3_Init(RTB,PCC_BAND,SCC_BAND,SCC2_BAND)
                           cnt=0                   
                           self.inst.CA3_Set(RTB,CA_dic[ca[cnt%3]][0],CA_dic[ca[cnt%3]][1],CA_dic[ca[cnt%3]][2],CA_dic[ca[(cnt+1)%3]][0],CA_dic[ca[(cnt+1)%3]][1],CA_dic[ca[(cnt+1)%3]][2],CA_dic[ca[(cnt+2)%3]][0],CA_dic[ca[(cnt+2)%3]][1],CA_dic[ca[(cnt+2)%3]][2])
                           res=self.inst.Read_Throutput(RTB)
                           sheet[1].write(row_3ca,0,CAcombo)
                           sheet[1].write(row_3ca,1,CA_dic[ca[(cnt)%3]][0])
                           sheet[1].write(row_3ca,2,CA_dic[ca[(cnt)%3]][1])
                           sheet[1].write(row_3ca,3,CA_dic[ca[(cnt)%3]][2])
                           sheet[1].write(row_3ca,4,CA_dic[ca[(cnt+1)%3]][0])
                           sheet[1].write(row_3ca,5,CA_dic[ca[(cnt+1)%3]][1])
                           sheet[1].write(row_3ca,6,CA_dic[ca[(cnt+1)%3]][2])
                           sheet[1].write(row_3ca,7,CA_dic[ca[(cnt+2)%3]][0])
                           sheet[1].write(row_3ca,8,CA_dic[ca[(cnt+2)%3]][1])
                           sheet[1].write(row_3ca,9,CA_dic[ca[(cnt+2)%3]][2])
                           sheet[1].write(row_3ca,10,res[0])
                           sheet[1].write(row_3ca,11,res[1])
                           row_3ca=row_3ca+1
        xlsout.save(CA_Result_file)
        
        print('Done！')
































