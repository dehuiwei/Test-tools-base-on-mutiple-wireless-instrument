#!/usr/bin/env python
"""
	Control Qualcomm based phone via QMSL lib
	
	 This file is part of RF_Tuning_Tool.

	:copyright: (c) 2013 by the A-mao Chang (maomaoto@gmail.com)
	:license: MIT, see COPYING for more details.

"""
import time
# from fwk.rf_debug_cmd import *
from ctypes import *
from fwk.WCDMA_attributes import *
from fwk.ftm_interface import *
# from Output_Log import  *
# import mid_pid_dict
import fwk

truth_dict = {True:"Yes",False:"No"}
pass_dict = {True:"Pass",False:"Fail"}
#
# mid_dict = {0x217: "Qualcomm Incorporated",
# 			0x126: "Toshiba Electronic Devices & Storage Corporation",
# 			0x20C:"Murata Manufacturing Co., Ltd.",
# 			0x1A5:"Skyworks Solutions Inc.",
# 			0x11A:"Infineon Technologies AG",
# 			0x134:"RF Micro Devices",
# 			0x338:"VanChip Technologies Limited",
# 			}


class QCOM_phone:
	def __init__(self,fwk):
		self.fwk = fwk
		self.log = self.fwk.log
		self.g_hResourceContext = c_void_p()
		self.qdll = None
# 		self.qBW = RFCOM_BW_LTE_5MHz	# BW corresponds to QMSL defined const
# 		self.log = Log(__name__).getlog()
	
	def initial_QMSL(self, bUseQPST):
		self.log.info("Enter Initial QMSL Fun.")
		# Import dll
		try:
# 			self.qdll = CDLL("QMSL_MSVC10R.dll")
			self.qdll = CDLL(r"D:\PAT\LEN_AUTO_19.00_DEV01_MODEM_V1.0\fwk\QMSL_MSVC10R.dll")
			
		except Exception as err:
			self.log.warning("Can't Find QMSL_MSVC10R DLL file,Error code=%s"%err)

		#QPST Library Mode, True:QPST	False:QPHONEMS
		#QPST and QPHONEMS have been definied in WCDMA_attributes.py
		self.qdll.QLIB_SetLibraryMode(bUseQPST)

		#Get the library version	Return: QLIB VXX.xx, <MODE>
		#return "b'QLIB V6.0.1,QPHONEMS'" @home(py 3.3.2 + win7)
		sLibraryVersion = create_string_buffer(50)
		self.qdll.QLIB_GetLibraryVersion(sLibraryVersion)
		self.log.info("Get Lib Version of QPST:%s"%sLibraryVersion.value)
		print("QCOM Fun, Get Lib Version of QPST:%s"%sLibraryVersion.value)

		#These will get filled in by the library interface
		_bSupportsDiag = c_bool(0)
		_bSupportsEFS = c_bool(0)
		_bSupportsSwDownload = c_bool(0)
		_bUsingQPST = c_bool(0)
		# Get the capabilities
		self.qdll.QLIB_GetLibraryCapabilities(byref(_bSupportsDiag), byref(_bSupportsEFS), byref(_bSupportsSwDownload), byref(_bUsingQPST))

		# Print the results
		self.log.info("Support Diag:{0}".format(truth_dict[bool(_bSupportsDiag)]))
		self.log.info("Support EFS:{0}".format(truth_dict[bool(_bSupportsEFS)]))
		self.log.info("Support SW Download:{0}".format(truth_dict[bool(_bSupportsSwDownload)]))
		self.log.info("Support QPST:{0}".format(truth_dict[bool(_bUsingQPST)]))

		print("Supports DIAG: {0}".format(truth_dict[bool(_bSupportsDiag)]))
		print("Using QPST: {0}".format(truth_dict[bool(_bUsingQPST)]))
		
	def get_phone_port_list(self):
		"""
			Return a list containing available phone ports
			If no port found, return a empty list
		"""
		self.log.info("Enter Get Phone Port List Fun")
		#Define all paras
		iNumPorts = c_ushort(16)	# as an input: max length of aPortList
		UShortList = c_ushort * 16
		aPortList = UShortList()	# output: array of ports available
		iNumIgnorePorts = c_ushort(0)	# number of ports to ignore
		aIgnorePortList = pointer(c_ushort())	# list of ports to ignore
		#Call QLIB to Get availabe phone Port list
		bOK = self.qdll.QLIB_GetAvailablePhonesPortList(byref(iNumPorts), byref(aPortList), iNumIgnorePorts, aIgnorePortList)
		PhoneList = []
		if (bOK):
			print("NumPorts: {0}".format(iNumPorts))
			print("Port:")
			for i in range(iNumPorts.value):
				print(aPortList[i])
				PhoneList.append(aPortList[i])
		else:
			print("no port found")
		
		return PhoneList

	def connect_phone(self, ComPort):
		self.log.info("Enter Connect Phone Fun")
		#iComPort = c_uint(40)	# move to WCDMA_attributes
		if (type(ComPort)== int):
			iComPort = c_uint(ComPort)
		else:
			iComPort = ComPort
			
		self.qdll.QLIB_ConnectServerWithWait.restype = c_void_p
		self.qdll.QLIB_ConnectServer.restype = c_void_p
		self.g_hResourceContext = self.qdll.QLIB_ConnectServerWithWait(iComPort)
		#iComPort = QLIB_COM_AUTO_DETECT
		#self.g_hResourceContext = self.qdll.QLIB_ConnectServerWithWait(iComPort, c_int(3000))
		#print("QCOM Handle: {0}".format(self.g_hResourceContext))
		self.log.info("Phone Connected: {0}".format(truth_dict[bool(self.qdll.QLIB_IsPhoneConnected(self.g_hResourceContext))]))
		print("Phone Connected: {0}".format(truth_dict[bool(self.qdll.QLIB_IsPhoneConnected(self.g_hResourceContext))]))

		#Get COM port number
		self.qdll.QLIB_GetComPortNumber( self.g_hResourceContext, byref(iComPort) )
		print("Port Number: {0}".format(iComPort))

		#Get SW version info
		comp_date = create_string_buffer(11)	#compile date
		comp_time = create_string_buffer(8)		#compile time
		rel_date = create_string_buffer(11)		#release date
		rel_time = create_string_buffer(8)		#release time
		ver_dir = create_string_buffer(8)		#version directory
		scm = c_ubyte()				#Station class mark
		mob_cai_rev = c_ubyte()		#CAI rev
		mob_model = c_ubyte()		#Mobile model
		mob_firm_rev = c_ushort()	#Firmware rev.
		slot_cycle_index = c_ubyte()#slot cycle index
		voc_maj = c_ubyte()			#Vocoder major version
		voc_min = c_ubyte()			#Vocoder minor version
		bOK = self.qdll.QLIB_DIAG_VERNO_F(self.g_hResourceContext, comp_date, comp_time, rel_date, rel_time, ver_dir,
			byref(scm), byref(mob_cai_rev), byref(mob_model), byref(mob_firm_rev), byref(slot_cycle_index),
			byref(voc_maj), byref(voc_min))  

		if (bool(bOK) == True):
			print("Mobile version report:")
			#print("Compile Date: {0}".format(comp_date.value))
			#print("Compile Time: {0}".format(comp_time.value))
			#print("Release Date: {0}".format(rel_date.value))
			#print("Release Time: {0}".format(rel_time.value))
			#print("Version Dir: {0}".format(ver_dir.value))
			#print("Station Class Mark: {0}".format(scm.value))
			#print("CAI Rev: {0}".format(mob_cai_rev.value))
			#print("Mobile Model: {0}".format(mob_model.value))
			#print("Firmware Rev.: {0}".format(mob_firm_rev.value))
			#print("Slot Cycle Index: {0}".format(slot_cycle_index.value))
			#print("Vocoder major version: {0}".format(voc_maj.value))
			#print("Vocoder minor version: {0}".format(voc_min.value))
		else:
			print("Mobile version fail")

		#Get extended version info
		_iMSM_HW_Version = c_ulong(0)
		_iMobModel = c_ulong(0)
		_sMobSwRev = create_string_buffer(512)
		_sModelStr = create_string_buffer(512)
		bOK = self.qdll.QLIB_DIAG_EXT_BUILD_ID_F( self.g_hResourceContext, byref(_iMSM_HW_Version),byref(_iMobModel), _sMobSwRev, _sModelStr )

		detailedinfo = []
		if (bool(bOK) == True):
			print("Ext MSM HW Version: {0}".format(hex(_iMSM_HW_Version.value)))
			detailedinfo.append(hex(_iMSM_HW_Version.value))
			print("Ext Mobile Model: {0}".format(hex(_iMobModel.value)))
			detailedinfo.append(hex(_iMobModel.value))
			print("Ext Mobile Mobile SW Rev: {0}".format(_sMobSwRev.value))
			detailedinfo.append(_sMobSwRev.value)
			print("Ext Model ID: {0}".format(_sModelStr.value))
			detailedinfo.append(_sModelStr.value)
		else:
			print("Extended Mobile version fail")
		return detailedinfo
	
	def set_online_mode(self):
		# Set online mode
		self.log.info("set phone to online mode")
		bOK = self.qdll.QLIB_DIAG_CONTROL_F(self.g_hResourceContext, MODE_ONLINE_F)
		print("change to Online mode: {0}".format(pass_dict[bool(bOK)]))
	
	def set_FTM_mode(self):
		# Set FTM mode
		self.log.info("set phone to FTM mode")
		bOK = self.qdll.QLIB_DIAG_CONTROL_F(self.g_hResourceContext, MODE_FTM_F)
		print("change to FTM mode: {0}".format(pass_dict[bool(bOK)]))
		bFTMMode = c_ubyte()
		bOK = self.qdll.QLIB_IsFTM_Mode(self.g_hResourceContext, byref(bFTMMode))
		if (bool(bOK) == True):
			print("Is FTM Mode: {0}".format(truth_dict[bool(bFTMMode)]))
		else:
			print("Is FTM Mode function fail")
		# Set Calibration State for latest device
		self.set_calibration_state()
	
	def set_calibration_state(self):
		# Set Calibration state for latest device
		bOK = self.qdll.QLIB_FTM_SET_CALIBRATION_STATE(self.g_hResourceContext,1)   
# 
# 	
# 	def set_band(self, eModeId, eNewMode):	
# 		"""
# 			Set technology/band
# 			eModeId: technology  
# 			eNewMode: band
# 		"""
# 		bOK = self.qdll.QLIB_FTM_SET_MODE_ID(self.g_hResourceContext, eModeId)  
# 		if (bool(bOK) == False): 
# 			print("Set FTM tech {0}: {1}".format(eModeId, pass_dict[bool(bOK)]))
# 		bOK = self.qdll.QLIB_FTM_SET_MODE(self.g_hResourceContext, eNewMode)
# 		if (bool(bOK) == False): 
# 			print("Set Band mode {0}: {1}".format(eNewMode, pass_dict[bool(bOK)]))
# 	
# 	def set_channel(self, iChannel):
# 		bOK = self.qdll.QLIB_FTM_SET_CHAN(self.g_hResourceContext,iChannel)
# 		if (bool(bOK) == False): 
# 			print("Set UL channel {0}: {1}".format(iChannel, pass_dict[bool(bOK)]))
# 		
# 	def set_Tx_ON(self):
# 		#Set Tx ON
# 		bOK = self.qdll.QLIB_FTM_SET_TX_ON( self.g_hResourceContext)
# 		if (bool(bOK) == False): 
# 			print("Set Tx ON: {0}".format(pass_dict[bool(bOK)]))
# 		
# 	def set_waveform(self):
# 		# Set WCDMA/C2k waveform
# 		if (bSet_WCDMA_Waveform == 1):
# 			bSelectCW = 0 	# Set 0 for de-select CW 
# 			bOK = self.qdll.QLIB_FTM_CDMA_CW_WAVEFORM(self.g_hResourceContext,bSelectCW)
# 			if (bool(bOK) == False): 
# 				print("Set WCDMA waveform: {0}".format(pass_dict[bool(bOK)]))
# 		
# 	def set_PA_range(self, iPArange):
# 		# Set PA range
# 		bOK = self.qdll.QLIB_FTM_SET_PA_RANGE(self.g_hResourceContext, iPArange)  
# 		if (bool(bOK) == False): 
# 			print("Set PA range {0}: {1}".format(iPArange, pass_dict[bool(bOK)]))
# 	
# 	def set_PDM(self, iPDMvalue):
# 		"""
# 		WCDMA mode values
# 		2 - Tx AGC Adjust PDM
# 		4 - Trk Lo Adjust PDM
# 
# 		GSM mode values
# 		0 - Trk Lo Adjust PDM
# 
# 		CDMA mode values
# 		2 - Tx AGC Adjust PDM
# 		4 - Trk Lo Adjust PDM
# 		"""
# 		iPDMtype = 2	#Tx AGC Adj PDM
# 		#iPDMvalue = 210	# 6285 Max:255
# 		bOK = self.qdll.QLIB_FTM_SET_PDM(self.g_hResourceContext, iPDMtype, iPDMvalue)  
# 		if (bool(bOK) == False): 
# 			print("Set Tx PDM value {0}: {1}".format(iPDMvalue, pass_dict[bool(bOK)]))
# 
# 	def set_PA_BIAS_override(self, iOnOff):
# 		"""
# 			need to test
# 			seems iOnOff = 1/0
# 		"""
# 		bOK = self.qdll.QLIB_FTM_SET_SMPS_PA_BIAS_OVERRIDE(self.g_hResourceContext, iOnOff)  
# 		if (bool(bOK) == False): 
# 			print("Set PA BIAS override: {0}".format(pass_dict[bool(bOK)]))
# 		
# 	def set_PA_BIAS_value(self, iPA_Bias_Value):
# 		"""
# 			need to test
# 		"""
# 		bOK = self.qdll.QLIB_FTM_SET_SMPS_PA_BIAS_VAL(self.g_hResourceContext, iPA_Bias_Value)
# 		if (bool(bOK) == False): 
# 			print("Set PA BIAs value {0}: {1}".format(iPA_Bias_Value, pass_dict[bool(bOK)]))
# 
# 	def set_Tx_off(self):
# 		bOK = self.qdll.QLIB_FTM_SET_TX_OFF( self.g_hResourceContext)
# 		if (bool(bOK) == False): 
# 			print("Set Tx OFF: {0}".format(pass_dict[bool(bOK)]))
# 	
# 	def set_LTE_Tx_BW(self, BW=5):
# 		"""
# 			Set LTE Tx BW
# 		"""
# 		if BW == 1:
# 			self.qBW = RFCOM_BW_LTE_1P4MHz
# 		elif BW == 3:
# 			self.qBW = RFCOM_BW_LTE_3MHz
# 		elif BW == 5:
# 			self.qBW = RFCOM_BW_LTE_5MHz
# 		elif BW == 10:
# 			self.qBW = RFCOM_BW_LTE_10MHz
# 		elif BW == 15:
# 			self.qBW = RFCOM_BW_LTE_15MHz
# 		elif BW == 20:
# 			self.qBW = RFCOM_BW_LTE_20MHz
# 		else:
# 			self.qBW = RFCOM_BW_LTE_5MHz	# Set 5MHz as default
# 			print("Wrong Tx BW input: {0}MHz, set BW as 5MHz".format(BW))
# 		bOK = self.qdll.QLIB_FTM_LTE_SET_TX_BANDWIDTH( self.g_hResourceContext, self.qBW)
# 		if (bool(bOK) == False): 
# 			print("Set Tx BW {0}MHz: {1}".format(BW, pass_dict[bool(bOK)]))
# 	
# 	def set_LTE_Tx_QPSK(self):
# 		# Set Tx Modulation to QPSK
# 		# Need to find QMSL doc
# 		bOK = self.qdll.QLIB_FTM_LTE_SET_TX_MODULATION_TYPE(self.g_hResourceContext,0) #0-QPSK, 1-16QAM, 2-64QAM
# 		#bOK = True
# 		if (bool(bOK) == False): 
# 			print("Set Tx Modulation: {0}".format(pass_dict[bool(bOK)]))
# 			
# 	def set_LTE_Rx_BW(self, BW=5):
# 		"""
# 			Set LTE Rx BW
# 		"""
# 		if BW == 1:
# 			self.qBW = RFCOM_BW_LTE_1P4MHz
# 		elif BW == 3:
# 			self.qBW = RFCOM_BW_LTE_3MHz
# 		elif BW == 5:
# 			self.qBW = RFCOM_BW_LTE_5MHz
# 		elif BW == 10:
# 			self.qBW = RFCOM_BW_LTE_10MHz
# 		elif BW == 15:
# 			self.qBW = RFCOM_BW_LTE_15MHz
# 		elif BW == 20:
# 			self.qBW = RFCOM_BW_LTE_20MHz
# 		else:
# 			self.qBW = RFCOM_BW_LTE_5MHz	# Set 5MHz as default
# 			print("Wrong Rx BW input: {0}MHz, set BW as 5MHz".format(BW))
# 		bOK = self.qdll.QLIB_FTM_LTE_SET_RX_BANDWIDTH( self.g_hResourceContext, self.qBW)
# 		if (bool(bOK) == False): 
# 			print("Set Rx BW {0}MHz: {1}".format(BW, pass_dict[bool(bOK)]))
# 	
# 	def set_LTE_Tx_waveform(self):
# 		"""
# 			Set LTE Tx waveform to Full RB PUSCH
# 		"""
# 		fRB = None
# 		if self.qBW == RFCOM_BW_LTE_1P4MHz:
# 			fRB = 6
# 		elif self.qBW == RFCOM_BW_LTE_3MHz:
# 			fRB = 15
# 		elif self.qBW == RFCOM_BW_LTE_5MHz:
# 			fRB = 25
# 		elif self.qBW == RFCOM_BW_LTE_10MHz:
# 			fRB = 50
# 		elif self.qBW == RFCOM_BW_LTE_15MHz:
# 			fRB = 75
# 		elif self.qBW == RFCOM_BW_LTE_20MHz:
# 			fRB = 100
# 		iTxWaveform = 1	# 0-CW, 1- PUSCH, 2- PUCCH, 3 - PRACH, 4 - SRS, 5 - UpPTS 
# 		inumRBsPUSCH = fRB
# 		inumRBsPUCCH = 0
# 		iPUSCHStartRBIndex = 0
# 		bOK = self.qdll.QLIB_FTM_LTE_SET_TX_WAVEFORM( self.g_hResourceContext, iTxWaveform, inumRBsPUSCH, inumRBsPUCCH, iPUSCHStartRBIndex)
# 		if (bool(bOK) == False): 
# 			print("Set Tx waveform: {0}".format(pass_dict[bool(bOK)]))
# 	
# 	def set_LTE_PDM(self, iTxGainIndex):
# 		"""
# 			LTE Tx PDM function is different with WCDMA
# 		"""
# 		bOK = self.qdll.QLIB_FTM_SET_TX_GAIN_INDEX(self.g_hResourceContext, iTxGainIndex)
# 		if (bool(bOK) == False): 
# 			print("Set Tx PDM value {0}: {1}".format(iTxGainIndex, pass_dict[bool(bOK)]))
# 	
# 	def disconnect(self):
# 		if self.g_hResourceContext is not None:
# 			#print("g_hResourceContext")
# 			self.qdll.QLIB_DisconnectServer(self.g_hResourceContext)
# 		self.qdll.QLIB_DisconnectAllServers()
# 
# 	def set_GSM_Tx_burst(self):
# 		"""
# 			Set GSM Tx burst parameters (fixed)
# 			According to QCOM reference, it is "Set Tx Burst".
# 			But it may change to "Set Tx Continue" depends on tuning experience
# 		"""
# 		iSlotNum = 0
# 		iDataSource = FTM_GSM_TX_DATA_SOURCE_PSDRND
# 		iTSCindex = 5
# 		iNumBursts = 0
# 		bIsInfiniteDuration = 1
# 		bOK = self.qdll.QLIB_FTM_SET_TRANSMIT_BURST(self.g_hResourceContext, iSlotNum, iDataSource, iTSCindex, iNumBursts, bIsInfiniteDuration)  
# 		if (bool(bOK) == False): 
# 			print("Set GSM Tx Burst: {0}".format(pass_dict[bool(bOK)]))
# 	
# 	def set_TCXO_Adj_PDM(self, iPDMvalue = 0):
# 		"""
# 			For GSM tuning
# 			Set TCXO Adj PDM to 0
# 		"""
# 		iPDMtype = 0	#GSM mode 0: Trk Lo Adjust PDM
# 		iPDMvalue = 0	#Set TXCO Adj PDM to 0
# 		bOK = self.qdll.QLIB_FTM_SET_PDM_signed( self.g_hResourceContext, iPDMtype, iPDMvalue)
# 		if (bool(bOK) == False): 
# 			print("Set GSM TCXO Adj PDM {0}: {1}".format(iPDMvalue, pass_dict[bool(bOK)]))
# 			
# 	def set_GSM_Linear_PA_range(self, iPaRange = 0):
# 		"""
# 			Set GSM Linear PA range
# 			Slot: 0
# 			Range: 0
# 		"""
# 		iSlotNum = 0
# 		bOK = self.qdll.QLIB_FTM_SET_GSM_LINEAR_PA_RANGE( self.g_hResourceContext, iSlotNum, iPaRange)
# 		if (bool(bOK) == False): 
# 			print("Set GSM Linear PA range: {0}".format(pass_dict[bool(bOK)]))
# 	
# 	def set_GSM_Linear_RGI(self, iRgiIndex = 31):
# 		"""
# 			Set GSM Linear RGI
# 			For tuning, it sets to 31 by default
# 		"""
# 		iSlotNum = 0
# 		iModType = 1	#GSM
# 		bOK = self.qdll.QLIB_FTM_GSM_SET_LINEAR_RGI(self.g_hResourceContext, iSlotNum, iRgiIndex, iModType)
# 		if (bool(bOK) == False): 
# 			print("Set GSM Linear RGI {0}: {1}".format(iRgiIndex, pass_dict[bool(bOK)]))
# 
# 	def set_CDMA_TRK_LO(self, iPDMvalue = 0):
# 		"""
# 		WCDMA mode values
# 		2 - Tx AGC Adjust PDM
# 		4 - Trk Lo Adjust PDM
# 
# 		GSM mode values
# 		0 - Trk Lo Adjust PDM
# 
# 		CDMA mode values
# 		2 - Tx AGC Adjust PDM
# 		4 - Trk Lo Adjust PDM
# 		"""
# 		iPDMtype = 4	# Trk Lo Adjust PDM
# 		bOK = self.qdll.QLIB_FTM_SET_PDM(self.g_hResourceContext, iPDMtype, iPDMvalue)  
# 		if (bool(bOK) == False): 
# 			print("Set CDMA Trk Lo Adjust PDM value {0}: {1}".format(iPDMvalue, pass_dict[bool(bOK)]))
# 
# 	def set_CDMA_TX_waveform(self):
# 		# Set CDMA waveform (it's the same function as WCDMA)
# 		if (bSet_CDMA_Waveform == 1):
# 			bSelectCW = 0 	# Set 0 for de-select CW 
# 			bOK = self.qdll.QLIB_FTM_CDMA_CW_WAVEFORM(self.g_hResourceContext,bSelectCW)
# 			if (bool(bOK) == False): 
# 				print("Set CDMA waveform: {0}".format(pass_dict[bool(bOK)]))	
	
	def RFFE_readwrite(self, Read, SlaveID, Address, Data=None, ExtMode=False, iChannel=0, HalfSpeed=False):
		"""
			Wrap QLIB_FTM_RFFE_READWRITE_CMD function
			Parameters:
				Read(bool): True->Read, False->Write
				SlaveID(str): HEX(1~F)
				Address(str): HEX
				Data(str): in/out HEX
				ExtMode(bool): True->Extended, False->Non-extended
				iChannel(int): 0/1
				HalfSpeed(bool): True-> Half-speed, False-> Full-speed
			Return:
				Data in HEX string
				None if failed
		"""
		iExtMode = int(ExtMode)
		iReadWrite = int(Read)
		iSlave = c_int(SlaveID)
		# Convert address from hex to int to c_int
		iAddress = c_int(Address)
		# Check Data
		if Data is None:
			iData = c_int()
		else:
			iData = c_int(int(Data,16))
		iHalfSpeed = int(HalfSpeed)
		
		#print("before")
		#print(iData)

		# QLIB_FTM_RFFE_READWRITE_CMD( hResourceContext, iExtMode, iReadWrite, iChannel, iSlave, iAddress, byref(iData), iHalfSpeed)
		
		self.qdll.QLIB_FTM_RFFE_READWRITE_CMD( self.g_hResourceContext, iExtMode, iReadWrite, iChannel, iSlave, iAddress, byref(iData), iHalfSpeed)
		
		#print("after")
		#print(iData)
		#print(iData.value)
		bOk = True
		if bool(bOk):
			return iData.value
		else:
			return None

# 	def Read_MID_PID(self, SlaveID, Data=None, ExtMode=False, iChannel=0, HalfSpeed=False):
# 
# 		# Get the Mid
# 		iAddress = 0x1E
# 		iMid = 0
# 		iLowMid = 0
# 		iHighMid = 0
# 
# 		iLowMid = self.RFFE_readwrite(1, SlaveID, iAddress, Data, ExtMode, iChannel, HalfSpeed)
# 		if iLowMid != 0x0:
# 			# 8~9 bit
# 			iAddress = 0x1F
# 			iHighMid = self.RFFE_readwrite(1, SlaveID, iAddress, Data, ExtMode, iChannel, HalfSpeed)
# 
# 			iMid = iLowMid | ((iHighMid & 0x30) << 4)
# 		else:
# 			return None
# 		#print("iMid: ", hex(iMid))
# 
# 
# 		# Get PID
# 		iAddress = 0x1D
# 		iIsMIPI2 = 0
# 		iLowPId = 0
# 		iHighPId = 0
# 		iPId = 0
# 
# 		# RFFE_readwrite(self, Read, SlaveID, Address, Data=None, ExtMode=False, iChannel=0, HalfSpeed=False):
# 		iLowPId = self.RFFE_readwrite(1, SlaveID,iAddress, Data, ExtMode, iChannel, HalfSpeed)
# 		#print("result: ",iLowPId)
# 		iAddress = 0x20
# 		iHighPId = self.RFFE_readwrite(1, SlaveID,iAddress, Data, ExtMode, iChannel, HalfSpeed)
# 		if iHighPId != 0x0:
# 			iIsMIPI2 = 1
# 
# 		iPId = iLowPId | (iHighPId << 8 & 0xFF00)
# 			#print("iPId: ", hex(iPId))
# 
# 		result = []
# 		result.append(hex(iMid))
# 		try:
# 			result.append(mid_pid_dict.MID_DICT[hex(iMid)])
# 		except Exception as err:
# 			result.append("No name, please add in xlsx")
# 		result.append(hex(iPId))
# 		#result.append(mid_pid_dict.PID_DICT[iMid][hex(iPId)])
# 		try:
# 			result.append(mid_pid_dict.PID_DICT[hex(iMid)][hex(iPId)])
# 		except Exception as err:
# 			result.append("No name, please add in xlsx")
# 
# 		result.append(str(iIsMIPI2))
# 		print(result)
# 		return result

	#bool Call_bands_ns_testDlg::SendDIAGCmd(CString cmd, uint8 *response, uint16* sizeRespose  )
	def SendSync(self, cmd):
		"""
            QLIB_API unsigned char QLIB_SendSync
            (
               HANDLE hResourceContext,
               short iRequestSize,
               unsigned char* piRequestBytes,
               short* piResponseSize,
               unsigned char* piResponseBytes,
               unsigned long iTimeout
            );
		"""
		time.sleep(1)
		RequestSize = len(cmd) / 2
		print("RequestSize: ", RequestSize)
		tmp_str = ""
		i = 0
		j = 0
		PiRequestBytes = create_string_buffer(int(RequestSize)+1)
		PiResponseSize = c_ulong(512)
		PiResponseBytes = create_string_buffer(PiResponseSize.value)
		
		for c in cmd:
			tmp_str += c
			i = i+1
			if i%2 == 0:
				#print(tmp_str)
				PiRequestBytes[j] = c_char(int(tmp_str, 16))
				#print(PiRequestBytes[j])
				i = 0
				j = j + 1
				tmp_str = ""

		#print(PiRequestBytes)
		#print("bytes raw: ", PiRequestBytes.raw)

		bOk = self.qdll.QLIB_SendSync( self.g_hResourceContext, int(RequestSize), PiRequestBytes, byref(PiResponseSize), PiResponseBytes, 4000)

		if bOk:
			print("PiResponseSize: ", PiResponseSize.value)

			# response2 = bytearray()
			# i = 13
			# while i < PiResponseSize.value:
			# 	response2.append(PiResponseBytes.raw[i])
			# 	i = i + 1
			#
			# ss = zlib.decompress(response2)
			# print("ss: ", ss)

			i = 0
			response = ""
			response2 = ""
			while i < PiResponseSize.value:
				tmp = "{:02x}".format(PiResponseBytes.raw[i])
				#print(tmp)
				response2 += " "
				response += tmp
				response2 += tmp
				i = i + 1
			print(response2)
			return response
		else:
			return ""

# if __name__ == "__main__":
# 	phone = QCOM_phone()
# 	phone.initial_QMSL(bUseQPST)
# 	pl = phone.get_phone_port_list()
# 	for i in pl: print(i)
# 	try:
# 		phone.connect_phone(pl[0])
# 	except Exception as err:
# 		print("error occur: ", err)
# 		print("确保bp-tools模式已经打开，DIAG口已经存在，手机已经连接")
# 		exit(-1)

	#def Read_MID_PID(self, SlaveID, Data=None, ExtMode=False, iChannel=0, HalfSpeed=False):

# 	mid_pid_dict.generate_mid_pid_dict()
# 	iChannel = 0
# 	while iChannel < 8:
# 		iSlave = 0
# 		while iSlave < 16:
# 			time.sleep(0.01)
# 			phone.Read_MID_PID(iSlave, None, 0, iChannel, 1)
# 			iSlave = iSlave + 1
# 
# 		iChannel = iChannel + 1



	#cmd = "4B0B14008F02000000000A01000001"
	# rf_path_information_request = ftm_rf_path_information_request(technology_family_type_for_path_information.TECHNOLOGY_FAMILY_LTE, RF_TEST_LTE_BandClasstype.RF_TEST_LTE_BAND_1)
	# print("rf_path_information_request: ", rf_path_information_request.get_cmd_for_diag())
	#
	# responsebytes = phone.SendSync(rf_path_information_request.get_cmd_for_diag())
	# print("PiResponseSize: ", len(responsebytes)/2)
	# print("responsebytes after send cmd:", responsebytes)
	#
	# if len(responsebytes):
	# 	rf_path_information_response = ftm_rf_path_information_response()
	# 	rf_path_information_response.parse_response(responsebytes)
	# 	print("compress: ", rf_path_information_response.compressionStatus)
	# 	print("len arrayOfResponsePacket: ", len(rf_path_information_response.arrayOfResponsePacket))
	# 	print("is_get_rf_path_info_cmd_success: ", rf_path_information_response.is_get_rf_path_info_cmd_success())
	#
	#
	# 	if rf_path_information_response.is_get_rf_path_info_cmd_success():
	#
	# 		ftm_rf_debug_radio_config_cmd = ftm_rf_debug_radio_cmd_type()
	# 		cmd = ftm_rf_debug_radio_config_cmd.get_radio_config_cmd_for_diag(ftm_rf_technology_type.FTM_RF_TECH_LTE,RF_TEST_LTE_BandClasstype.RF_TEST_LTE_BAND_1,300, 18300)
	# 		print("ftm_rf_debug_radio_config_cmd:",cmd)
	# 		responsebytes = phone.SendSync(cmd)
	# 		print("PiResponseSize: ", len(responsebytes) / 2)
	# 		print("responsebytes after send cmd:", responsebytes)
	#
	# 		ftm_rf_debug_radio_config_cmd_response = ftm_rf_debug_cmd_response_type()
	# 		ftm_rf_debug_radio_config_cmd_response.parse_response(responsebytes)
	# 		response = ftm_rf_debug_radio_config_cmd_response.get_string()
	# 		print("ftm_rf_debug_cmd_response after parse:", response)
	# 		print("is_rf_debug_cmd_success:", ftm_rf_debug_radio_config_cmd_response.is_rf_debug_cmd_success())
	#
	# 		# 睡眠1s
	# 		time.sleep(1)
	#
	# 		####Tx process
	# 		ftm_rf_debug_tx_override_cmd = ftm_rf_debug_radio_cmd_type()
	# 		cmd = ftm_rf_debug_tx_override_cmd.get_tx_override_cmd_for_diag(ftm_rf_technology_type.FTM_RF_TECH_LTE)
	# 		print("ftm_rf_debug_tx_override_cmd:", cmd)
	# 		responsebytes = phone.SendSync(cmd)
	# 		print("PiResponseSize: ", len(responsebytes) / 2)
	# 		print("responsebytes after send cmd:", responsebytes)
	#
	#
	# 		####Rx process
	# 		# rx over ride
	# 		# ftm_rf_debug_rx_override_cmd = ftm_rf_debug_radio_cmd_type()
	# 		# cmd = ftm_rf_debug_rx_override_cmd.get_rx_override_cmd_for_diag(ftm_rf_technology_type.FTM_RF_TECH_LTE)
	# 		# print("ftm_rf_debug_rx_override_cmd:", cmd)
	# 		# responsebytes = phone.SendSync(cmd)
	# 		# print("PiResponseSize: ", len(responsebytes) / 2)
	# 		# print("responsebytes after send cmd:", responsebytes)
	# 		#
	# 		# ftm_rf_debug_rx_override_cmd_response = ftm_rf_debug_cmd_response_type()
	# 		# ftm_rf_debug_rx_override_cmd_response.parse_response(responsebytes)
	# 		# response = ftm_rf_debug_rx_override_cmd_response.get_string()
	# 		# print("ftm_rf_debug_cmd_response after parse:", response)
	# 		# print("rx agc offset value:", ftm_rf_debug_rx_override_cmd_response.get_agc_offset_value())
	# 		# print("is_rf_debug_cmd_success:", ftm_rf_debug_rx_override_cmd_response.is_rf_debug_cmd_success())
	#
	# 		# tear down cmd
	# 		time.sleep(5)
	# 		ftm_rf_debug_tear_down_cmd = ftm_rf_debug_radio_cmd_type()
	# 		cmd = ftm_rf_debug_tear_down_cmd.get_tear_down_cmd_for_diag(ftm_rf_technology_type.FTM_RF_TECH_LTE)
	# 		print("ftm_rf_debug_tear_down_cmd:", cmd)
	# 		responsebytes = phone.SendSync(cmd)
	# 		print("PiResponseSize: ", len(responsebytes) / 2)
	# 		print("responsebytes after send cmd:", responsebytes)

	#disconnect phone after all test
# 	phone.disconnect()
