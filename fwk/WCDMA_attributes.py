#!/usr/bin/env python
# for instrument/phone setting
# William Chang

#Test for git

#Instrument setting
Instrument_GPIB = 20		#GPIB
Average_times = 20		# average times for Txp and ACLR measurement
IMSI = '001010123456789'
path_loss = {700: -0.3, 1200: -0.3, 1500: -0.6, 2300: -0.6, 2500: -0.7, 2700: -0.7}		#initiate path loss table (using dict)
#CMW500 List
cmw500List = ["151212","122126","155612","150996","146855","152502","152501","146147"]
#Anritsu 8820C setting
Integrity = 1			# Integrity ON|OFF
#Phone settings
bUseQPST = 1			# bUseQPST = true to use QPST, FALSE to use QPHONEMS 
Phone_Com_Port = 15		# Phone COM port
bSet_WCDMA_Waveform = 0	# For GLU(MSM8974),  not to set WCDMA waveform
bSet_CDMA_Waveform = 1	# Reserve this parameter
PDM_init = 88			# Start PDM (High gain mode default PDM) (RTR6285:210, WTR1605:90)
PDM_low = 50			# PDM for -20dBm (Low gain mode PDM) (RTR6285:140, WTR1605:60)
PDM_max = 255			# PDM Max (RTR6285:255, WTR1605:127)
PDM_min = 0
iPArange_high = 0			# for high gain mode (RTR6285:3, WTR1605:0)
iPArange_low = 3			# for low gain mode (RTR6285:0, WTR1605:3)
PA_range_map = dict(B7=(0,1), # for different Band-PA setting => Band=(HPM,LPM)
					B20=(0,3), 
					)
"""
	0 - R0 = 0, R1 = 0,
	1 - R0 = 1, R1 = 0,
	2 - R0 = 0, R1 = 1,
	3 - R0 = 1, R1 = 1
"""

SMPS_ON_init = 1	#SMPS ON(1)/OFF(0)
SMPS_init = 3400	#SMPS value (for High gain mode) (MSM8x25/RTR6285:380/511, MSM8x30/WTR1605:780, MSM8974/WTR1605:1000)
SMPS_low = 1000		#SMPS value for -20dBm (for Low gain mode) (MSM8x25/RTR6285:95, MSM8x30/WTR1605:230, MSM8974/WTR1605:1000)
# Tuning sweep
TARGET_PWR = 23.5
PDM_start = 80
PDM_end = 90

# Tested Power Supply list
Power_Suppply_list = ["GOOD WILL;PPT-1830;", "HEWLETT-PACKARD,E3631A,", "Agilent Technologies,66319D"]

# WCDMA attributes
#channel list
WCDMA_B1_TX_ch_freq = [1, 9612,10562,1922.4,2112.4]
WCDMA_B2_TX_ch_freq = [2, 9262,9662,1852.4,1932.4]
WCDMA_B4_TX_ch_freq = [4, 1312,1537,1712.4,2112.4]
WCDMA_B5_TX_ch_freq = [5, 4132,4357,826.4,871.4]
WCDMA_B8_TX_ch_freq = [8, 2712,2937,882.4,927.4]
WCDMA_B19_TX_ch_freq = [19, 312,712,832.4,877.4]

WCDMA_B1_RX_ch_freq = [1, 9888,10838,1977.6,2167.6]
WCDMA_B2_RX_ch_freq = [2, 9538,9938,1907.6,1987.6]
WCDMA_B4_RX_ch_freq = [4, 1513,1738,1752.6,2152.6]
WCDMA_B5_RX_ch_freq = [5, 4233,4458,846.6,891.6]
WCDMA_B8_RX_ch_freq = [8, 2863,3088,912.6,957.6]
WCDMA_B19_RX_ch_freq = [19, 363,763,842.6,887.6]

#band-channel mapping
WCDMA_Band_TX_ch_map = dict(B1=WCDMA_B1_TX_ch_freq,
				B2=WCDMA_B2_TX_ch_freq,
				B4=WCDMA_B4_TX_ch_freq, B5=WCDMA_B5_TX_ch_freq,
				B8=WCDMA_B8_TX_ch_freq, B19=WCDMA_B19_TX_ch_freq)
WCDMA_Band_RX_ch_map = dict(B1=WCDMA_B1_RX_ch_freq,
				B2=WCDMA_B2_RX_ch_freq,
				B4=WCDMA_B4_RX_ch_freq, B5=WCDMA_B5_RX_ch_freq,
				B8=WCDMA_B8_RX_ch_freq, B19=WCDMA_B19_RX_ch_freq)

# LTE attributes  Band,UL Channel,DL Channel, UL Freq, DL Freq
# channel list
LTE_B1_TX_ch_freq = [1, 18050,50,1925,2115]
LTE_B2_TX_ch_freq = [2, 18650,650,1855,1935]
LTE_B3_TX_ch_freq = [3, 19250,1250,1715,1810]
LTE_B4_TX_ch_freq = [4, 20000,2000,1715,2115]
LTE_B5_TX_ch_freq = [5, 20450,2450,829,874]
LTE_B6_TX_ch_freq = [6, 20700,2700,835,880]
LTE_B7_TX_ch_freq = [7, 20800,2800,2505,2625]
LTE_B8_TX_ch_freq = [8, 21500,3500,885,930]
LTE_B9_TX_ch_freq = [9, 21975,3975,1767.4,1862.4]
LTE_B10_TX_ch_freq = [10, 22450,4450,1740,2140]
LTE_B11_TX_ch_freq = [11,22850,4850,1437.9,1485.9]
LTE_B12_TX_ch_freq = [12, 23060,5060,704,734]
LTE_B13_TX_ch_freq = [13, 23230,5230,782,751]
LTE_B14_TX_ch_freq = [14, 23330,5330,793,763]
LTE_B17_TX_ch_freq = [17, 23780,5780,709,739]
LTE_B18_TX_ch_freq = [18, 23900,5900,820,865]
LTE_B19_TX_ch_freq = [19, 24050,6050,835,880]
LTE_B20_TX_ch_freq = [20, 24200,6200,837,796]
LTE_B21_TX_ch_freq = [21,24525,6525,1455.4,1503.4]
LTE_B23_TX_ch_freq = [23,25600,7600,2010,2190]
LTE_B24_TX_ch_freq = [24,25870,7870,1643.5,1542]
LTE_B25_TX_ch_freq = [25, 26090,8090,1855,1935]
LTE_B26_TX_ch_freq = [26, 26740,8740,819,864]
LTE_B27_TX_ch_freq = [27,27125,9125,815.5,860.5]
LTE_B28_TX_ch_freq = [28,27435,9435,725.5,780.5]
LTE_B28A_TX_ch_freq = [28, 27260,9260,708,763]
LTE_B28B_TX_ch_freq = [28, 27260,9260,708,763]
LTE_B30_TX_ch_freq = [30, 27710,9820,2310,2355]
LTE_B31_TX_ch_freq = [31,27785,9895,455,465]
LTE_B34_TX_ch_freq = [34, 36250,36250,2015,2015]
LTE_B38_TX_ch_freq = [38, 37800,37800,2575,2575]
LTE_B39_TX_ch_freq = [39, 38300,38300,1885,1885]
LTE_B40_TX_ch_freq = [40, 38700,38700,2305,2305]
LTE_B41_TX_ch_freq = [41, 39700,39700,2501,2501]
LTE_B66_TX_ch_freq = [66, 132022,66486,1715,2115]
LTE_B71_TX_ch_freq = [71, 133172,68636,668,622]

LTE_B1_RX_ch_freq = [1, 18599,599,1979.9,2169.9]
LTE_B2_RX_ch_freq = [2, 19199,1199,1909.9,1989.9]
LTE_B3_RX_ch_freq = [3, 19949,1949,1784.9,1879.9]
LTE_B4_RX_ch_freq = [4, 20399,2399,1754.9,2154.9]
LTE_B5_RX_ch_freq = [5, 20649,2649,848.9,893.9]
LTE_B7_RX_ch_freq = [7, 21449,3449,2659.9,2689.9]
LTE_B8_RX_ch_freq = [8, 21799,3799,914.9,959.9]
LTE_B11_RX_ch_freq = [11,0,0,0,0]
LTE_B12_RX_ch_freq = [12, 23179,5179,715.9,745.9]
LTE_B13_RX_ch_freq = [13, 23279,5279,786.9,755.9]
LTE_B14_RX_ch_freq = [14, 23379,5379,797.9,767.9]
LTE_B17_RX_ch_freq = [17, 23849,5849,715.9,745.9]
LTE_B18_RX_ch_freq = [18, 23999,5999,829.9,874.9]
LTE_B19_RX_ch_freq = [19, 24149,6149,844.9,889.9]
LTE_B20_RX_ch_freq = [20, 24449,6449,861.9,820.9]
LTE_B21_RX_ch_freq = [21,0,0,0,0]
LTE_B25_RX_ch_freq = [25, 26689,8689,1914.9,1994.9]
LTE_B26_RX_ch_freq = [26, 27309,9039,848.9,893.9]
LTE_B28A_RX_ch_freq = [28, 27659,9659,747.9,802.9]
LTE_B28B_RX_ch_freq = [28, 27659,9659,747.9,802.9]
LTE_B30_RX_ch_freq = [30, 27759,9869,2314.9,2359.9]
LTE_B34_RX_ch_freq = [34, 36349,36349,2024.9,2024.9]
LTE_B38_RX_ch_freq = [38, 38249,38249,2619.9,2619.9]
LTE_B39_RX_ch_freq = [39, 38649,38649,1919.9,1919.9]
LTE_B40_RX_ch_freq = [40, 39649,39649,2399.9,2399.9]
LTE_B41_RX_ch_freq = [41, 41589,41589,2689.9,2689.9]
LTE_B66_RX_ch_freq = [66, 132671,67135,1779.9,2179.9]
LTE_B71_RX_ch_freq = [71, 133471,68935,697.9,651.9]

# band-channel mapping
LTE_Band_TX_ch_map = dict(B1=LTE_B1_TX_ch_freq, B2=LTE_B2_TX_ch_freq, B3=LTE_B3_TX_ch_freq, B4=LTE_B4_TX_ch_freq, B5=LTE_B5_TX_ch_freq,B6=LTE_B6_TX_ch_freq, B7=LTE_B7_TX_ch_freq,
						B8=LTE_B8_TX_ch_freq, B9=LTE_B9_TX_ch_freq,B10=LTE_B10_TX_ch_freq,B11=LTE_B11_TX_ch_freq,B12=LTE_B12_TX_ch_freq,B13=LTE_B13_TX_ch_freq, B14=LTE_B14_TX_ch_freq,
						B17=LTE_B17_TX_ch_freq,B18=LTE_B18_TX_ch_freq,B19=LTE_B19_TX_ch_freq, B20=LTE_B20_TX_ch_freq, B21=LTE_B21_TX_ch_freq,B23=LTE_B23_TX_ch_freq,
						B24=LTE_B24_TX_ch_freq,B25=LTE_B25_TX_ch_freq,B26=LTE_B26_TX_ch_freq,B27=LTE_B27_TX_ch_freq,B28=LTE_B28_TX_ch_freq,B281=LTE_B28A_TX_ch_freq, B282=LTE_B28B_TX_ch_freq,
						B30=LTE_B30_TX_ch_freq,B31=LTE_B31_TX_ch_freq,B66=LTE_B66_TX_ch_freq,B71=LTE_B71_TX_ch_freq,B34=LTE_B34_TX_ch_freq,B38=LTE_B38_TX_ch_freq,B39=LTE_B39_TX_ch_freq,
						B40=LTE_B40_TX_ch_freq,B41=LTE_B41_TX_ch_freq)
LTE_Band_RX_ch_map = dict(B1=LTE_B1_RX_ch_freq, B2=LTE_B2_RX_ch_freq, B3=LTE_B3_RX_ch_freq, B4=LTE_B4_RX_ch_freq, B5=LTE_B5_RX_ch_freq,B7=LTE_B7_RX_ch_freq,
						B8=LTE_B8_RX_ch_freq,B11=LTE_B11_RX_ch_freq,B12=LTE_B12_RX_ch_freq,B13=LTE_B13_RX_ch_freq, B14=LTE_B14_RX_ch_freq,
						B17=LTE_B17_RX_ch_freq,B18=LTE_B18_RX_ch_freq,B19=LTE_B19_RX_ch_freq, B20=LTE_B20_RX_ch_freq, B21=LTE_B21_RX_ch_freq,B25=LTE_B25_RX_ch_freq,
						B26=LTE_B26_RX_ch_freq,B281=LTE_B28A_RX_ch_freq, B282=LTE_B28B_RX_ch_freq,B30=LTE_B30_RX_ch_freq,B66=LTE_B66_RX_ch_freq,B71=LTE_B71_RX_ch_freq,
						B34=LTE_B34_RX_ch_freq,B38=LTE_B38_RX_ch_freq,B39=LTE_B39_RX_ch_freq,B40=LTE_B40_RX_ch_freq,B41=LTE_B41_RX_ch_freq)
# LTE attributes  Band,UL Channel,DL Channel, UL Freq, DL Freq
# channel list
TDSCDMA_B34_TX_ch_freq = [34,10087,10087,2017.4,2017.4]
TDSCDMA_B39_TX_ch_freq = [39,9500,9500,1900,1900]
#tdscdma band-channel mapping
TDSCDMA_Band_TX_ch_map = dict(B34=TDSCDMA_B34_TX_ch_freq,B39=TDSCDMA_B39_TX_ch_freq)
# GSM attributes
# channel list
GSM850_TX_ch_freq = [850, 128,128,824.2,869.2,0]
GSM900_TX_ch_freq = [900, 975,975,880.2,925.2,1]
GSM1800_TX_ch_freq = [1800, 512,512,1710.2,1805.2,2]
GSM1900_TX_ch_freq = [1900, 512,512,1850.2,1930.2,3]

GSM850_RX_ch_freq = [850, 251,251,848.8,893.8,0]
GSM900_RX_ch_freq = [900, 124,124,914.8,959.8,1]
GSM1800_RX_ch_freq = [1800, 885,885,1784.8,1879.8,2]
GSM1900_RX_ch_freq = [1900, 810,810,1909.8,1989.8,3]

# band-channel mapping
GSM_Band_TX_ch_map = dict(GSM850=GSM850_TX_ch_freq, GSM900=GSM900_TX_ch_freq, GSM1800=GSM1800_TX_ch_freq, GSM1900=GSM1900_TX_ch_freq)
GSM_Band_RX_ch_map = dict(GSM850=GSM850_RX_ch_freq, GSM900=GSM900_RX_ch_freq, GSM1800=GSM1800_RX_ch_freq, GSM1900=GSM1900_RX_ch_freq)



# C2k attributes
# channel list
CDMA_BC0_TX_ch_freq = [0, 356,356,835.68,880.68]
CDMA_BC1_TX_ch_freq = [1, 600,600,1880,1960]
CDMA_BC10_TX_ch_freq = [10, 500,500,818.5,863.5]

CDMA_BC0_RX_ch_freq = [0, 356,356,835.68,880.68]
CDMA_BC1_RX_ch_freq = [1, 600,600,1880,1960]
CDMA_BC10_RX_ch_freq = [10, 500,500,818.5,863.5]

# band-channel mapping
CDMA_Band_TX_ch_map = dict(BC0=CDMA_BC0_TX_ch_freq, BC1=CDMA_BC1_TX_ch_freq, BC10=CDMA_BC10_TX_ch_freq)
CDMA_Band_RX_ch_map = dict(BC0=CDMA_BC0_RX_ch_freq, BC1=CDMA_BC1_RX_ch_freq, BC10=CDMA_BC10_RX_ch_freq)
					
					
# Below is QMSL defined variable
# Just copy from QLib_Defines.h. It should be better way to include or reference, but I don't know at this moment.

# Definition of the COM port value that will be used to "auto detect" the COM port
QLIB_COM_AUTO_DETECT  = 0xFFFF

# Phone modes
MODE_OFFLINE_A_F = 0  #Go to offline analog
MODE_OFFLINE_D_F = 1  #Go to offline digital 
MODE_RESET_F = 2      #Reset. Only exit from offline 
MODE_FTM_F = 3        #FTM mode
MODE_ONLINE_F = 4     #Go to Online 
MODE_LPM_F = 5        #Low Power Mode (if supported)
MODE_POWER_OFF_F = 6  #Power off (if supported)
MODE_MAX_F = 7        #Last (and invalid) mode enum value

# Phone logging settings
LOG_NOTHING = 0x0000	# log nothing
LOG_C_HIGH_LEVEL_START = 0x0200	# High level C function start, indicates the begining of a high level C function, which
								# calls other low level C functions internal to the library
LOG_C_HIGH_LEVEL_STOP = 0x4000	# High level C function stop
LOG_IO = 0x0001		# data IO (data bytes)
LOG_FN = 0x0002		# function calls with parameters
LOG_RET = 0x0004	# function return data
LOG_INF = 0x0008	# general information (nice to know)--do not use this one, as
					# this space needs to be reserved for async messages
LOG_ASYNC = 0x0008	# asynchronous messages
LOG_ERR = 0x0010	# critical error information
LOG_IO_AHDLC = 0x0020	# HDLC IO tracing (data bytes)
LOG_FN_AHDLC = 0x0040	# HDLC layer function calls
LOG_RET_AHDLC = 0x0080	# HDLC function return data
LOG_INF_AHDLC = 0x0100	# HDLC general information
LOG_ERR_AHDLC = LOG_INF_AHDLC	# HDLC Error info merged with LOG_INF_AHDLC, to free up the log bit
LOG_IO_DEV = 0x0400	# device IO tracing (data bytes)
LOG_FN_DEV = 0x0800	# device layer function calls
LOG_RET_DEV = 0x1000	# device function return data
LOG_INF_DEV = 0x2000	# device general information
LOG_ERR_DEV = LOG_INF_DEV		# device error information, merged with LOG_INF_DEV to free up the log bit
LOG_DEFAULT	= (LOG_C_HIGH_LEVEL_START|LOG_C_HIGH_LEVEL_STOP|LOG_FN|LOG_IO|LOG_RET|LOG_ERR|LOG_ASYNC) #  default settings
LOG_ALL = 0xFFFF	# everything

# Set FTM Mode
FTM_MODE_ID_CDMA_1X     = 0
FTM_MODE_ID_WCDMA       = 1
FTM_MODE_ID_GSM         = 2
FTM_MODE_ID_CDMA_1X_RX1 = 3
FTM_MODE_ID_BLUETOOTH   = 4
FTM_MODE_ID_CDMA_1X_CALL= 7
FTM_MODE_ID_LOGGING     = 9
FTM_MODE_ID_AGPS        = 10
FTM_MODE_ID_PMIC        = 11
FTM_MODE_GSM_BER        = 13
FTM_MODE_ID_AUDIO       = 14
FTM_MODE_ID_CAMERA      = 15
FTM_MODE_WCDMA_BER      = 16
FTM_MODE_ID_GSM_EXTENDED_C = 17
FTM_MODE_CDMA_API_V2    = 18
FTM_MODE_ID_MF_C        = 19
FTM_MODE_RF_COMMON      = 20
FTM_MODE_WCDMA_RX1      = 21
FTM_MODE_ID_LTE        = 29	# LTE FTM Calibration
FTM_MODE_LTE_NS        = 30	# LTE FTM Non-Signaling
FTM_MODE_CDMA_C2        = 32
FTM_MODE_CDMA_C3        = 40
FTM_MODE_CDMA_C4        = 45
FTM_MODE_ID_PRODUCTION  = 0x8000
FTM_MODE_ID_LTM         = 0x8001	# LTM


# For FTM Mode/Band setting
PHONE_MODE_FM        = 1      #(FM)
PHONE_MODE_SLEEP 	 = 2	  #(Sleep Mode)
PHONE_MODE_GPS       = 3      #(GPS)
PHONE_MODE_GPS_SINAD = 4      #(GPS SINAD)
PHONE_MODE_CDMA_800  = 5      #(CDMA 800)
PHONE_MODE_CDMA_1900 = 6      #(CDMA 1900)
PHONE_MODE_CDMA_1800 = 8      #(CDMA 1800)
PHONE_MODE_J_CDMA    = 14     #(JCDMA)
PHONE_MODE_CDMA_450  = 17     #(CDMA 450)
PHONE_MODE_CDMA_IMT  = 19     #(CDMA IMT)
PHONE_MODE_CDMA_1900_EXT = 26 # Secndary CDMA 1900MHz Band, Band Class 14
PHONE_MODE_CDMA_450_EXT = 27  # CDMA BC 11 (450 Extension)
PHONE_MODE_CDMA_800_SEC = 33  # Secondary CDMA 800MHz Band, Band Class 10

PHONE_MODE_WCDMA_IMT   =9      #(WCDMA IMT, Band I)
PHONE_MODE_GSM_900     =10     #(GSM 900)
PHONE_MODE_GSM_1800    =11     #(GSM 1800)
PHONE_MODE_GSM_1900    =12     #(GSM 1900)
PHONE_MODE_WCDMA_1900A =15     #(WCDMA 1900 A, Band II Add)
PHONE_MODE_WCDMA_1900B =16     #(WCDMA 1900 B, Band II Gen)
PHONE_MODE_GSM_850     =18     #(GSM 850)
PHONE_MODE_WCDMA_800   =22     #(WCDMA 800, Band V Gen)
PHONE_MODE_WCDMA_800A  =23     #(WCDMA 800, Band V Add)
PHONE_MODE_WCDMA_1800  =25     #(WCDMA 1800, Band III)
PHONE_MODE_WCDMA_BC4   =28     #(WCDMA BC4-used for both Band IV Gen and Band IV Add)
PHONE_MODE_WCDMA_BC8   =29     #(WCDMA BC8, Band VIII)
PHONE_MODE_MF_700      =30     #(MediaFLO)
PHONE_MODE_WCDMA_BC9   =31     #(WCDMA BC9 (1750MHz & 1845MHz), Band IX)
PHONE_MODE_CDMA_BC15   =32     #(CDMA Band Class 15)

PHONE_MODE_LTE_B1     =34    #(LTE Band Class 1)
PHONE_MODE_LTE_B7     =35    #(LTE Band Class 7)
PHONE_MODE_LTE_B4	  =42	 #(LTE Band Class 4)
PHONE_MODE_LTE_B11	  =41    #(LTE Band Class 11)
PHONE_MODE_LTE_B13    =36    #(LTE Band Class 13)
PHONE_MODE_LTE_B17    =37    #(LTE Band Class 17)
PHONE_MODE_LTE_B38    =38    #(LTE Band Class 38)
PHONE_MODE_LTE_B40    =39    #(LTE Band Class 40)
PHONE_MODE_WCDMA_1500 =40
PHONE_MODE_LTE_B11 = 41
PHONE_MODE_LTE_B2=43 
PHONE_MODE_LTE_B3=44 
PHONE_MODE_LTE_B5=45 
PHONE_MODE_LTE_B6=46 
PHONE_MODE_LTE_B8=47 
PHONE_MODE_LTE_B9=48 
PHONE_MODE_LTE_B10=49 
PHONE_MODE_LTE_B12=50 
PHONE_MODE_LTE_B14=51 
PHONE_MODE_LTE_B15=52 
PHONE_MODE_LTE_B16=53 
PHONE_MODE_LTE_B18=54 
PHONE_MODE_LTE_B19=55 
PHONE_MODE_LTE_B20=56 
PHONE_MODE_LTE_B21=57 
PHONE_MODE_LTE_B22=58 
PHONE_MODE_LTE_B23=59 
PHONE_MODE_LTE_B24=60 
PHONE_MODE_LTE_B25=61 
PHONE_MODE_LTE_B26=62 
PHONE_MODE_LTE_B27=63 
PHONE_MODE_LTE_B28=64 
PHONE_MODE_LTE_B29=65 
PHONE_MODE_LTE_B30=66 
PHONE_MODE_LTE_B31=67 
PHONE_MODE_LTE_B32=68 
PHONE_MODE_LTE_B33=69 
PHONE_MODE_LTE_B34=70 
PHONE_MODE_LTE_B35=71 
PHONE_MODE_LTE_B36=72 
PHONE_MODE_LTE_B38=73
PHONE_MODE_LTE_B39=74
PHONE_MODE_LTE_B40=75
PHONE_MODE_WCDMA_BC19=76
PHONE_MODE_LTE_B41=77
PHONE_MODE_LTE_B66 = 78
PHONE_MODE_LTE_B71 = 79

#TDSCDMA reserves 90 - 99
PHONE_MODE_TDSCDMA_B34=90 
PHONE_MODE_TDSCDMA_B39=91 
PHONE_MODE_TDSCDMA_B40=92 
PHONE_MODE_MAX         =255    #(Last possible value, not a valid mode)

# LTE Bandwidth 
RFCOM_BW_LTE_1P4MHz = 0
RFCOM_BW_LTE_3MHz = 1
RFCOM_BW_LTE_5MHz = 2 
RFCOM_BW_LTE_10MHz = 3
RFCOM_BW_LTE_15MHz = 4
RFCOM_BW_LTE_20MHz = 5


#GSM TX DataSources Enum
FTM_GSM_TX_DATA_SOURCE_PSDRND = 0	#Pseudorandom
FTM_GSM_TX_DATA_SOURCE_TONE = 1		#Single tone
FTM_GSM_TX_DATA_SOURCE_BUFFER = 2	#Buffer
FTM_GSM_TX_DATA_SOURCE_TWOTONE = 3	#2 tone


#Band-QMSL variable mapping
LTE_Band_QMSL_map = dict(B1=PHONE_MODE_LTE_B1, B2=PHONE_MODE_LTE_B2, B3=PHONE_MODE_LTE_B3, B4=PHONE_MODE_LTE_B4, B5=PHONE_MODE_LTE_B5, B6=PHONE_MODE_LTE_B6,B7=PHONE_MODE_LTE_B7,
					B8=PHONE_MODE_LTE_B8,B9=PHONE_MODE_LTE_B9, B10=PHONE_MODE_LTE_B10,B11=PHONE_MODE_LTE_B11, B12=PHONE_MODE_LTE_B12,B13=PHONE_MODE_LTE_B13,B14=PHONE_MODE_LTE_B14,
					B15=PHONE_MODE_LTE_B15,B16=PHONE_MODE_LTE_B16,B17=PHONE_MODE_LTE_B17,B18=PHONE_MODE_LTE_B18,B19=PHONE_MODE_LTE_B19, B20=PHONE_MODE_LTE_B20, B21=PHONE_MODE_LTE_B21,
					B23=PHONE_MODE_LTE_B23,B24=PHONE_MODE_LTE_B24,B25=PHONE_MODE_LTE_B25,B26=PHONE_MODE_LTE_B26, B27=PHONE_MODE_LTE_B27,B28=PHONE_MODE_LTE_B28,
					B281=PHONE_MODE_LTE_B28, B282=PHONE_MODE_LTE_B28, B30=PHONE_MODE_LTE_B30,B31=PHONE_MODE_LTE_B31,B66=PHONE_MODE_LTE_B66,B71=PHONE_MODE_LTE_B71,
					B34=PHONE_MODE_LTE_B34,B38=PHONE_MODE_LTE_B38,B39=PHONE_MODE_LTE_B39,B40=PHONE_MODE_LTE_B40,B41=PHONE_MODE_LTE_B41)
WCDMA_Band_QMSL_map = dict(B1=PHONE_MODE_WCDMA_IMT, B2=PHONE_MODE_WCDMA_1900B,
				B4=PHONE_MODE_WCDMA_BC4, B5=PHONE_MODE_WCDMA_800, B8=PHONE_MODE_WCDMA_BC8, 
				B9=PHONE_MODE_WCDMA_BC9,B19=PHONE_MODE_WCDMA_BC19)
TDSCDMA_Band_QMSL_map = dict(B34=PHONE_MODE_TDSCDMA_B34,B39=PHONE_MODE_TDSCDMA_B39)

GSM_Band_QMSL_map = dict(GSM900=PHONE_MODE_GSM_900, GSM850=PHONE_MODE_GSM_850, GSM1800=PHONE_MODE_GSM_1800, GSM1900=PHONE_MODE_GSM_1900)
CDMA_Band_QMSL_map = dict(BC0=PHONE_MODE_CDMA_800, BC1=PHONE_MODE_CDMA_1900, BC10=PHONE_MODE_CDMA_800_SEC)				
				
#Anritsu 8820C CALL Status
ANRITSU_OFF = 0		#Call processing function set to Off
ANRITSU_IDLE = 1	#Idle state
ANRITSU_IDLE_REGIST = 2		#Idle( Regist ) Idle state (location registered)
ANRITSU_REGIST = 3			# Under location registration
ANRITSU_ORIGIN = 4			# Origination from a terminal
ANRITSU_TERMIN = 5			# Origination from the MT8815B/MT8820B (network)
ANRITSU_COMMUN = 6			# Under communication
ANRITSU_LOOP_1 = 7			# Loopback mode 1
ANRITSU_LOOP_1_OPEN = 8		# Loopback mode 1 open
ANRITSU_LOOP_1_CLOSE = 9	# Loopback mode 1 close
ANRITSU_LOOP_2 = 10			# Loopback mode 2
ANRITSU_LOOP_2_OPEN = 11	# Loopback mode 2 open
ANRITSU_LOOP_2_CLOSE = 12	# Loopback mode 2 close
ANRITSU_HAND = 13			# Under handover
ANRITSU_NW_RELEASE = 14		# Release by the MT8815B/MT8820B (network)
ANRITSU_UE_RELEASE = 15		# Release by a terminal
ANRITSU_OTHER = 16			# Other
