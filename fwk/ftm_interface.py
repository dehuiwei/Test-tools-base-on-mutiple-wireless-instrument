#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-

"""
File:               ftm_interface.py
User:               zengwen1
Create Date:        2019/06/27
Create Time:        11:03
function:  common definition for ftm command
 """

# LTE band enum for RF DEBUG
class RF_TEST_LTE_BandClasstype:
    RF_TEST_LTE_BAND_1 = 1
    RF_TEST_LTE_BAND_2 = 2
    RF_TEST_LTE_BAND_3 = 3
    RF_TEST_LTE_BAND_4 = 4
    RF_TEST_LTE_BAND_5 = 5
    RF_TEST_LTE_BAND_7 = 7
    RF_TEST_LTE_BAND_8 = 8
    RF_TEST_LTE_BAND_12 = 12
    RF_TEST_LTE_BAND_13 = 13
    RF_TEST_LTE_BAND_14 = 14
    RF_TEST_LTE_BAND_17 = 17
    RF_TEST_LTE_BAND_18 = 18
    RF_TEST_LTE_BAND_19 = 19
    RF_TEST_LTE_BAND_20 = 20
    RF_TEST_LTE_BAND_25 = 25
    RF_TEST_LTE_BAND_26 = 26
    RF_TEST_LTE_BAND_28 = 28
    RF_TEST_LTE_BAND_30 = 30
    RF_TEST_LTE_BAND_34 = 34
    RF_TEST_LTE_BAND_38 = 38
    RF_TEST_LTE_BAND_39 = 39
    RF_TEST_LTE_BAND_40 = 40
    RF_TEST_LTE_BAND_41 = 41
    RF_TEST_LTE_BAND_66 = 66
    RF_TEST_LTE_BAND_71 = 71

# WCDMA band enum for RF DEBUG
class RF_TEST_WCDMA_BandClasstype:
    RF_TEST_WCDMA_BAND_1 = 1
    RF_TEST_WCDMA_BAND_2 = 2
    RF_TEST_WCDMA_BAND_3 = 3
    RF_TEST_WCDMA_BAND_4 = 4
    RF_TEST_WCDMA_BAND_5 = 5
    RF_TEST_WCDMA_BAND_8 = 8
    RF_TEST_WCDMA_BAND_9 = 9
    RF_TEST_WCDMA_BAND_11 = 11
    RF_TEST_WCDMA_BAND_19 = 19

# GSM band enum for RF DEBUG
class RF_TEST_GSM_BandClasstype:
    RF_TEST_GSM_850 = 850
    RF_TEST_GSM_900 = 900
    RF_TEST_GSM_1800 = 1800
    RF_TEST_GSM_1900 = 1900

# TDSCDMA band enum for RF DEBUG
class RF_TEST_TDSCDMA_BandClasstype:
    RF_TEST_TDSCDMA_B34 = 34
    RF_TEST_TDSCDMA_B39 = 39
    RF_TEST_TDSCDMA_B40 = 40

# CDMA band enum for RF DEBUG
class RF_TEST_CDMA_BandClasstype:
    RF_TEST_CDMA_BC0 = 0
    RF_TEST_CDMA_BC1 = 1
    RF_TEST_CDMA_BC10 = 10

# Enumeration listing the technology family type(technology enum used on tools side)
# Technology Mode used by ftm_rf_path_information_request
class technology_family_type_for_path_information:
    TECHNOLOGY_FAMILY_CDMA = 0
    TECHNOLOGY_FAMILY_WCDMA = 1
    TECHNOLOGY_FAMILY_GSM = 2
    TECHNOLOGY_FAMILY_BLUETOOTH =3
    TECHNOLOGY_FAMILY_MEDIAFLO = 4
    TECHNOLOGY_FAMILY_DVBH = 5
    TECHNOLOGY_FAMILY_ANALOG = 6
    TECHNOLOGY_FAMILY_GPS = 7
    TECHNOLOGY_FAMILY_ISDBT = 8
    TECHNOLOGY_FAMILY_1xEVDO = 9
    TECHNOLOGY_FAMILY_LTE = 10
    TECHNOLOGY_FAMILY_TDSCDMA = 11
    TECHNOLOGY_FAMILY_WLAN = 12
    TECHNOLOGY_FAMILY_NFC = 13
    TECHNOLOGY_FAMILY_MULTIMEDIA = 14
    TECHNOLOGY_FAMILY_FM_RADIO = 15
    TECHNOLOGY_FAMILY_TYPE_MAX = 0xFFFF

# RF TECH enum for rf debug
class ftm_rf_technology_type:
        FTM_RF_TECH_CDMA = 0 # / *RF is in CDMA tech * /
        FTM_RF_TECH_WCDMA = 1 #/ *RF is in WCDMA tech * /
        FTM_RF_TECH_GSM = 2  #/* RF is in GSM tech      */
        FTM_RF_TECH_LTE = 3  #/* RF is in LTE tech      */
        FTM_RF_TECH_TDSCDMA = 4  #/* RF is in TDSCDMA tech  */
        FTM_RF_TECH_HDR = 5 # /* RF is in HDR tech      */

# all RF debug command enum
class ftm_rf_debug_command_enum_type:
    FTM_RF_DEBUG_CMD_UNASSIGNED = 0  #/ * ! < 0: Unassignedcommand * /
    FTM_RF_DEBUG_CMD_RADIO_CONFIGURE = 1 #/*!< 1 : Radio Configure command */
    FTM_RF_DEBUG_CMD_TX_OVERRIDE = 2 #/*!< 2 : Tx override command */
    FTM_RF_DEBUG_CMD_RX_OVERRIDE = 3 #/*!< 3 : Rx override command */
    FTM_RF_DEBUG_CMD_DISCOVERY = 4 #/*!< 4 : Command discovery command */
    FTM_RF_DEBUG_CMD_PROPERTY_DISCOVERY = 5 #/*!< 5 : Command property discovery command */
    FTM_RF_DEBUG_CMD_TX_MEASURE = 6 #/*!< 6 : Tx Measure command */
    FTM_RF_DEBUG_CMD_LOAD_UNITY_DPD = 7 #/*!< 7 : Load Unity DPD command */
    FTM_RF_DEBUG_CMD_VDPD_CAL = 8 #/*!< 8 : Performing XPT capture and loading DPD table command */
    FTM_RF_DEBUG_CMD_VDPD_CONVERSION = 9 #/*!< 9 : Converting the Volterra kernel weights to AMAM and AMPM values */
    FTM_RF_DEBUG_CMD_LOAD_DPD = 10 #/*!< 10 : Load DPD command */
    FTM_RF_DEBUG_CMD_RX_MEASURE = 11 #/*!< 11 : Rx Measure command */
    FTM_RF_DEBUG_CMD_CODEBOOK_OVERRIDE = 12 #/*!< 12 : Codebook Override command */
    FTM_RF_DEBUG_CMD_TX_MEASURE_ADV = 13 #/*!< 13 : Tx Measure via advanced 5G handler */
    FTM_RF_DEBUG_CMD_SET_DPD_DEBUG_MODE = 14 #/*!< 14 : Override debug mode to predpd or post dpd before DPD Cal */
    FTM_RF_DEBUG_CMD_IDC_CAL = 15 #/*!< 15 : Perform WTR IDC Cal on single path and bandwidth */

# all prop for radio config
class ftm_rf_debug_radio_config_property_type:
    #from ftm_rf_debug_interface.h
    # prop: 4bytes, value: 8 bytes
    FTM_RF_DEBUG_RADIO_CFG_PROP_UNASSIGNED = 0 #/*!< 0 : Unassigned property */
    FTM_RF_DEBUG_RADIO_CFG_PROP_IS_TEARDOWN = 1 #/*!< 1 : If teardown needs to be done */
    FTM_RF_DEBUG_RADIO_CFG_PROP_RADIO_SETUP_TYPE = 2 #/*!< 2 : Type of Radio setup needed */
    FTM_RF_DEBUG_RADIO_CFG_PROP_RFM_DEVICE = 3 #/*!< 3 : RFM Device*/
    FTM_RF_DEBUG_RADIO_CFG_PROP_SIG_PATH = 4 #/*!< 4 : Signal Path for AT forward */
    FTM_RF_DEBUG_RADIO_CFG_PROP_ANT_PATH = 5 #/*!< 5 : Antenna Path */
    FTM_RF_DEBUG_RADIO_CFG_PROP_RFM_PATH_TYPE = 6 #/*!< 6 : RFM Path type - Tx/PRx/DRx */
    FTM_RF_DEBUG_RADIO_CFG_PROP_BAND = 7 #/*!< 7 : Operating Tech Band */
    FTM_RF_DEBUG_RADIO_CFG_PROP_SUBBAND = 8 #/*!< 8: Radio Bandwidth */
    FTM_RF_DEBUG_RADIO_CFG_PROP_RESERVED = 9 #/*!< 9: Reserved for future use */
    FTM_RF_DEBUG_RADIO_CFG_PROP_CHANNEL = 10 #/*!< 10 : Operating Tech channel */
    FTM_RF_DEBUG_RADIO_CFG_PROP_WAVEFORM = 11 #/*!< 11 : Tx waveform type */
    FTM_RF_DEBUG_RADIO_CFG_PROP_BANDWIDTH = 12 #/*!< 12 : Radio Bandwidth */
    FTM_RF_DEBUG_RADIO_CFG_PROP_NUM_RB = 13 #/*!< 13 : Number of RBs */
    FTM_RF_DEBUG_RADIO_CFG_PROP_START_RB = 14 #/*!< 14 : Start RB Index */
    FTM_RF_DEBUG_RADIO_CFG_PROP_CW_OFFSET = 15 #/*!< 15 : Offset frequency wrt channel to be tuned to*/
    FTM_RF_DEBUG_RADIO_CFG_PROP_IS_DC = 16 #/*!< 16 : Flag for Dual Carrier */
    FTM_RF_DEBUG_RADIO_CFG_PROP_MOD_TYPE = 17 #/*!< 17 : Modulation type */
    FTM_RF_DEBUG_RADIO_CFG_PROP_LOOPBACK_TYPE = 18 #/*!< 18 : 5GNR Only: Loopback type, as defined by RFC */
    FTM_RF_DEBUG_RADIO_CFG_PROP_BEAM_ID = 19 #/*!< 19 : 5GNR Only: Beam ID, as defined by RFC */
    FTM_RF_DEBUG_RADIO_CFG_PROP_CC_INDEX = 20 #/*!< 20 : 5GNR Only: Component Carrier Index */
    FTM_RF_DEBUG_RADIO_CFG_PROP_CC_START_RB = 21 #/*!< 21 : 5GNR Only: Start RB Index for the Component Carrier*/
    FTM_RF_DEBUG_RADIO_CFG_PROP_CC_NUM_RB = 22 #/*!< 22 : 5GNR Only: Number of RBs for the Component Carrier*/
    FTM_RF_DEBUG_RADIO_CFG_PROP_CC_BANDWIDTH = 23 #/*!< 23 : 5GNR Only: CC Bandwidth*/
    FTM_RF_DEBUG_RADIO_CFG_PROP_LOOPBACK_RFM_DEVICE = 24 #/*!< 24 : 5GNR Only: Output param. Loopback RFM Device*/
    FTM_RF_DEBUG_RADIO_CFG_PROP_PLL_ID = 25 #/*!< 25 : PLL id is part of the RFM Path definition*/
    FTM_RF_DEBUG_RADIO_CFG_PROP_TUNE_TX_TO_RX_FREQ = 26 #/*!< 26 : Flag indicating tune to Rx frequence*/
    FTM_RF_DEBUG_RADIO_CFG_PROP_LOAD_CODEBOOK = 27 #/*!< 27 : 5GNR Only: Load Codebook Flag*/
    FTM_RF_DEBUG_RADIO_CFG_PROP_FREQUENCY = 28 #/*!< 28 : Operating Tech frequency*/
    FTM_RF_DEBUG_RADIO_CFG_PROP_VERSION = 29 # /*!< 29 : Radio setup  version type*/
    FTM_RF_DEBUG_RADIO_CFG_PROP_SWITCH_TDSCDMA_WAVEFORM = 30 #/*!< 30 : flag to indicate only switch TDSCDMA waveform during radio setup call- TDSCDMA specic*/

# reverse hex format string
# input: str, hex format string
# output: return hex format string
def reverse_hex_string(str):
    #00 00 00 00 00 00 01 2C ==> 2C 01 00 00 00 00 00 00
    length = len(str)
    response = ""
    while length > 0:
        response += str[length-2: length]
        length = length -2
    return response