# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 14:01:04 2019

@author: lidz1
"""

import logging
import visa
import pyvisa as visa
import time
import tkinter
from tkinter import messagebox
import fwk
class CMW500(object):
    def __init__(self,fwk,GPIB):
###modify by weidehui
        rm=visa.ResourceManager()
        ##RTB = rm.open_resource('TCPIP0::169.254.4.61::inst0::INSTR')
#         GPIB = self.cfg["GPIB"]
#         RTB = rm.open_resource('GPIB0::20::INSTR')
        self.fwk = fwk
        self.log = self.fwk.log
        self.inst = rm.open_resource(GPIB)
        self.inst.timeout=20000
        self.inst.read_termination = "\n"
        self.cfg = self.fwk.cfg
###modify by weidehui

    def ber(self,rtb,pwr):
        rtb.write('CONF:GSM:SIGN1:RFS:LEV:TCH '+str(pwr))
    #    rtb.write('CONFigure:GSM:SIGN:BER:CSWitched:MMODe BER')
    #    rtb.write('CONFigure:GSM:SIGN:BER:CSWitched:SCOunt 100') 
        res = rtb.query('READ:GSM:SIGN:BER:CSWitched?')
        return float(res.split(',')[2])
    def band_handover(self,rtb,band,chan,pcl):
        band_str=''
        if (band==850):
            band_str='G085'
        if (band==900):
            band_str='G09'
        if (band==1800):
            band_str='G18'
        if (band==1900):
            band_str='G19'
        rtb.write('PREPare:GSM:SIGN1:HANDover:TARGet '+ band_str)
        rtb.write('PREPare:GSM:SIGN1:HANDover:CHANnel:TCH '+str(chan))
        rtb.write('PREPare:GSM:SIGN1:HANDover:LEVel:TCH  -100')
        rtb.write('PREPare:GSM:SIGN1:HANDover:PCL '+str(pcl))
    #    rtb.write('PREPare:GSM:SIGN1:HANDover:TSLot 3')
        rtb.write('CALL:GSM:SIGN1:HANDover:STARt')
    def band_conf(self,rtb,chan,pcl):
        rtb.write('CONF:GSM:SIGN1:RFS:CHAN:TCH '+str(chan))
        rtb.write('CONF:GSM:SIGN1:RFS:LEV:TCH  -80')
        rtb.write('CONF:GSM:SIGN1:RFS:PCL:TCH:CSW '+str(pcl))
    def ber_search(self,rtb):
        bler=0
        pwr=-100
        step=5
        last_pass_pwr=0
        last_fail_pwr=-120
    
        while True:
            bler=self.ber(rtb, pwr)
            if(bler<2.4):
                last_pass_pwr=pwr
                print('PASS:','{:.1f}'.format(pwr),'{:.1f}'.format(step),'{:.1f}'.format(bler),'{:.1f}'.format(last_pass_pwr))
    
                if(last_fail_pwr-last_pass_pwr>-0.15):
                    return pwr
                pwr=int(pwr*10)/10
                pwr=pwr-step
                
            else:
                last_fail_pwr=pwr
                step=int(step*10/2)/10
                if(step<0.1):step=0.1
                if(last_fail_pwr-last_pass_pwr<-0.15):last_pass_pwr=last_pass_pwr-0.1
                print('FAIL:','{:.1f}'.format(pwr),'{:.1f}'.format(step),'{:.1f}'.format(bler),'{:.1f}'.format(last_fail_pwr))
                pwr=pwr+step
                pwr=int(pwr*10)/10
    
    
    
    
    def swtich_freq(self,rtb):
        a=rtb.query('FETCh:GSM:MEAS:MEValuation:SSWitching:FREQuency?').split(',')
        res=[0,0,0,0,0,0,0,0,0]
        try:
            res=a[17:26]
            for i in range(9):
                res[i]=float(res[i])
            return res
        except:
            return res
    def CA_Init(self,rtb,PCC_MODE,SCC_MODE):
        rtb.write('SYST:RES:ALL\n')
        time.sleep(0.5)
        rtb.write('CONF:BASE:FDC:CTAB:CRE \'SuperCA\', 300000000.0, 10.0, 3000000000.0, 10.0\n')
        time.sleep(1)
        
    
    
        rtb.write('ROUT:LTE:SIGN1:SCEN:CATR RF1C,RX1,RF1C,TX1,RF1C,TX3\n')
        rtb.write('CONF:LTE:SIGN1:DMOD:UCSP ON\n')    
        rtb.write('CONF:LTE:SIGN1:PCC:DMOD:UCSP ON\n')
        rtb.write('CONF:LTE:SIGN1:SCC:DMOD:UCSP ON\n')
        rtb.write('CONF:LTE:SIGN1:PCC:DMOD '+PCC_MODE+'\n')
        rtb.write('CONF:LTE:SIGN1:SCC:DMOD '+SCC_MODE+'\n')
        rtb.write('SOUR:LTE:SIGN1:CELL:STAT ON\n')    
        while(True):
            resstr=rtb.query('FETC:LTE:SIGN1:PSW:STAT?')
            time.sleep(1)
            if ('ON' in resstr):break
    def CA3_Init(self,rtb,PCC_MODE,SCC_MODE,SCC2_MODE):
    
        rtb.write('SYST:RES:ALL\n')
        rtb.write('CONF:BASE:FDC:CTAB:CRE \'SuperCA\', 300000000.0, 7.0, 3000000000.0, 7.0\n')
        rtb.write('MMEM:RCL \'@SAVE\\3ca.dfl\'\n')
        rtb.write('ROUT:LTE:SIGN1:SCEN:CC RF1C,RX1,RF1C,TX1,RF1C,TX3,RF3C,TX2\n')
    #    rtb.write('ROUT:LTE:SIGN1:SCEN:CF SUW1,RF1C,RX1,RF1C,TX1,RF3C,TX2,SUW2,RF1C,TX1,RF3C,TX4,SUW3,RF1C,TX3,RF3C,TX4\n')
        rtb.write('CONF:LTE:SIGN1:DMOD:UCSP ON\n')    
        rtb.write('CONF:LTE:SIGN1:PCC:DMOD:UCSP ON\n')
        rtb.write('CONF:LTE:SIGN1:SCC1:DMOD:UCSP ON\n')
        rtb.write('CONF:LTE:SIGN1:SCC2:DMOD:UCSP ON\n')
        rtb.write('CONF:LTE:SIGN1:PCC:DMOD '+PCC_MODE+'\n')
        rtb.write('CONF:LTE:SIGN1:SCC1:DMOD '+SCC_MODE+'\n') 
        rtb.write('CONF:LTE:SIGN1:SCC2:DMOD '+SCC2_MODE+'\n')
        rtb.write('SOUR:LTE:SIGN1:CELL:STAT ON\n')   
        rtb.write('CONF:LTE:SIGN1:EBL:SFR 1000\n')
    
        while(True):
            resstr=rtb.query('FETC:LTE:SIGN1:PSW:STAT?')
            time.sleep(1)
            if ('ON' in resstr):break
        
    def CA_PCC(self,rtb,band,chan,bw):    
        rtb.write('CONF:LTE:SIGN1:CELL:BAND:PCC:DL B'+str(10*bw))
        rtb.write('CONF:LTE:SIGN1:PCC:BAND OB'+str(band))
        rtb.write('CONF:LTE:SIGN1:RFS:PCC:CHAN:DL '+str(chan))
    def CA_SCC1(self,rtb,band,chan,bw):    
        rtb.write('CONF:LTE:SIGN1:CELL:BAND:SCC1:DL B'+str(10*bw))
        rtb.write('CONF:LTE:SIGN1:SCC1:BAND OB'+str(band))
        rtb.write('CONF:LTE:SIGN1:RFS:SCC1:CHAN:DL '+str(chan))
    def CA_SCC2(self,rtb,band,chan,bw):    
        rtb.write('CONF:LTE:SIGN1:CELL:BAND:SCC2:DL B'+str(10*bw))
        rtb.write('CONF:LTE:SIGN1:SCC2:BAND OB'+str(band))
        rtb.write('CONF:LTE:SIGN1:RFS:SCC2:CHAN:DL '+str(chan))
    def CA_Set(self,rtb,band1,chan1,bw1,band2,chan2,bw2):
        rtb.write('CONF:LTE:SIGN1:RFS:ALL:BWCH OB'+str(band1)+','+str(chan1)+', B'+str(10*bw1)+',OB'+str(band2)+','+str(chan2)+', B'+str(10*bw2)+'\n')
        time.sleep(0.5)
    #    rtb.write('CONF:LTE:SIGN1:EBL:REP SING')
    #    time.sleep(0.5)
    
    #    time.sleep(0.5)
    #    rtb.write('INIT:LTE:SIGN1:EBL')
    #    time.sleep(0.5)
        print('PCC:B'+str(band1)+'\t'+'SCC:B'+str(band2))
    def CA3_Set(self,rtb,band1,chan1,bw1,band2,chan2,bw2,band3,chan3,bw3):
        rtb.write('CONF:LTE:SIGN1:RFS:ALL:BWCH OB'+str(band1)+','+str(chan1)+', B'+str(10*bw1)+',OB'+str(band2)+','+str(chan2)+', B'+str(10*bw2)+',OB'+str(band3)+','+str(chan3)+', B'+str(10*bw3)+' \n')
    #    rtb.write('CONF:LTE:SIGN1:EBL:SFR 1000\n')
        print('PCC:B'+str(band1)+'\t'+'SCC1:B'+str(band2)+'\t'+'SCC2:B'+str(band3)+'\n')
    def Read_Throutput(self,rtb):
    #    try:
    
            rtb.write('CONF:LTE:SIGN1:EBL:REP SING\n')
            rtb.write('INIT:LTE:SIGN1:EBL\n')
            time.sleep(0.5)
            resstr=rtb.query('FETC:LTE:SIGN1:EBL:STAT?')
            time.sleep(0.5)
            rtb.write('CALL:LTE:SIGN1:PSW:ACT CONN\n')
            count=0
            res=[0,0]
            while(True):
                if('RDY' in resstr):
                    resstr=rtb.query('FETC:LTE:SIGN1:EBL:ALL:ABS?')
                    resstr=resstr.split(',')
                    if('INV'in resstr[4]):
                        print('测试数据为空！%d'%count)
                        rtb.write('CALL:LTE:SIGN1:PSW:ACT CONN\n')
                        time.sleep(0.3)
                        rtb.write('CONF:LTE:SIGN1:EBL:REP SING\n')
                        time.sleep(0.3)
                        rtb.write('INIT:LTE:SIGN1:EBL\n')
                        time.sleep(0.3)
                        count=count+1
                        if(count>100):
                            return(res)
                    else:
                        time.sleep(0.5)
                        res[0]=float(resstr[4])
                        res[1]=(float(resstr[2])+float(resstr[7]))/float(resstr[8])*100
                        print(res)
                        return(res)
                else:
                    time.sleep(0.5)
                    resstr=rtb.query('FETC:LTE:SIGN1:EBL:STAT?')
                    time.sleep(0.5)
                    print('测试数据为空！%d'%count)
                    count=count+1
                    if(count>100):
                        print('无法驻网! 返回0')
                        return(res)
                    
    #    except:
    #        print('仪器控制错误！')
        
    def Read3_BLER(self,rtb):
        try:
    
            rtb.write('CONF:LTE:SIGN1:EBL:REP SING\n')
            time.sleep(0.5)
            rtb.write('INIT:LTE:SIGN1:EBL\n')
            time.sleep(0.5)
            resstr=rtb.query('FETC:LTE:SIGN1:EBL:STAT?')
            time.sleep(0.5)
            rtb.write('CALL:LTE:SIGN1:PSW:ACT CONN\n')
    
            BER=[0,0,0]
            while(True):
                if('RDY' in resstr):
                    resstr1=rtb.query('FETC:LTE:SIGN1:EBL:PCC:ABS?').split(',')
                    resstr2=rtb.query('FETC:LTE:SIGN1:EBL:SCC1:ABS?').split(',')
                    resstr3=rtb.query('FETC:LTE:SIGN1:EBL:SCC2:ABS?').split(',')
                    if('INV'in resstr1[4] or 'INV'in resstr2[4] or 'INV'in resstr3[4] ):
                        print('吞吐率值错误，貌似掉网 请手动辅助')
                        rtb.write('CALL:LTE:SIGN1:PSW:ACT CONN\n')
                        time.sleep(0.5)
                        resstr=rtb.query('FETC:LTE:SIGN1:EBL:STAT?')
    
                    else:
                        BER[0]=(float(resstr1[2])+float(resstr1[7]))/float(resstr1[8])
                        BER[1]=(float(resstr2[2])+float(resstr2[7]))/float(resstr2[8])
                        BER[2]=(float(resstr3[2])+float(resstr3[7]))/float(resstr3[8])
                        time.sleep(0.5)
                        print(BER)
                        return(BER)
                else:
                    time.sleep(0.5)
                    resstr=rtb.query('FETC:LTE:SIGN1:EBL:STAT?')
                    time.sleep(0.5)
                    print(resstr)
                   
        except:
            print('仪器控制错误！')
    
    
    
