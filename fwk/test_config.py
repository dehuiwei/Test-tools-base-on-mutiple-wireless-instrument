'''

@author: weidh2
'''
import os
import logging
import time
from configobj import ConfigObj
import re
# from Output_Log import *
class TestConfig(object):
    def __init__(self,fwk):
        self.fwk = fwk
        self.log = fwk.log
        self.config = {}
#         self.log = logging.Logger("CA_TEST")
        self.create_default_params()
        self.read_config_file(self.config["test_config_name"])  
 
    def create_default_params(self):
        self.log.error("Creating default configuration")
        self.config["project"] = "Defender"
        self.config["device_name"] = "keysightUXM"
        self.config["tc_module"] = "Modem_CA_Verify_Keysight"
        self.config["test_config_name"] = "test_config.ini"
        self.config["ProjectName"] = "Defender"
        self.config["is_restart_phone"] = False
        self.config["root_path"] = os.getcwd()
        self.config["config_path"] = self.config["root_path"] + "\\02_config"
        self.config["CA_tpye"] = "LTE"
        self.config["ca_combs_name"] = "ca_combs.xlsx"
        self.config["ca_parameter_load_type"] = "auto"
        self.config["document_path"] = os.getcwd() + "\\" +"03_document"
        self.config["auto_get_qualcomm_port"] = True
        self.config["qualcomm_port"] = "21"
        self.config["phone_control_method"] = "qualcomm"
        self.config["is_loop_pcell"] = True
        
    def read_config_file(self,test_config_file_name):
        
        test_config_file_path = os.path.join(self.config["config_path"], test_config_file_name)
        self.log.error("read test config from file %s"%test_config_file_path)
        if not os.path.exists(test_config_file_path):
            self.log.error("** %s missing, only default values will be used **" % test_config_file_name)
            return False
        
        test_config_obj = ConfigObj(test_config_file_path)
        # print(test_config_obj)
        for section in test_config_obj.sections:
#             print (section)
#             print(test_config_obj[section].iteritems())
            for key,value in test_config_obj[section].iteritems():
#                 print("key is %s value is %s"%(key,value))
                self.config[key] = value
#                 print(self.config)
        self.log.info(self.config)      
    def get_ca_comb(self,ca_type,a):
        if ca_type != 'DC':
            c = a.replace(" ","").replace(",","").split("CA_")
            for i in c:
            #     print(i)
                if "C" in i or "B" in i or "D" in i:
                    print(i)
            print(c)
            d = len(c)
            print ("there are ca comb",d-1)
            if ca_type == 2:
                re1 = re.compile(r"(\d+[A-Za-z]-\d+[A_Za-z])\S")
                list = re1.findall(a)
                print(list)
                for i in list:
                    print (i)
            elif ca_type ==3:
                re1 = re.compile(r"(\d+[A-Za-z]-\d+[A_Za-z]-\d+[A_Za-z])\S")
                list = re1.findall(a)
                print(list)
                for i in list:
                    print (i)
        else:
            c = a.replace(" ","").replace(",","").split("DC_")
            for i in c:
                print(i)
            

                
if __name__ == "__main__":
#     test = TestConfig() 
#     ca2 ="CA_1C, CA_1A-1A, CA_1A-3A, CA_1A-5A, CA_1A-7A, CA_1A-8A, CA_1A-20A, CA_1A-28A, CA_1A-32A, CA_1A-38A[All], CA_1A-40A[1A,40A], CA_2A-4A, CA_2A-5A, CA_3C[All], CA_3A-3A[All], CA_3A-5A, CA_3A-7A[All], CA_3A-8A[3A], CA_3A-20A[3A], CA_3A-28A, CA_3A-32A, CA_3A-38A[All], CA_3A-40A[3A,40A], CA_4A-4A, CA_4A-5A, CA_4A-7A, CA_5A-38A, CA_5A-41A, CA_7B[All], CA_7C[All], CA_7A-7A[All], CA_7A-8A[7A], CA_7A-20A[7A], CA_7A-28A, CA_7A-32A[7A], CA_7A-40A[7A,40A], CA_8A-28A, CA_8A-32A, CA_8A-38A[38A], CA_8A-40A, CA_20A-32A, CA_20A-38A[38A], CA_20A-40A, CA_28A-40A[40A], CA_38C[All], CA_40C" 
#     ca3 = "CA_1A-1A-3A, CA_1A-1A-5A, CA_1A-1A-7A, CA_1A-1A-28A, CA_1A-3C, CA_1A-3A-3A, CA_1A-3A-7A, CA_1A-3A-8A[1A,3A,1A-3A], CA_1A-3A-20A[1A,3A,1A-3A], CA_1A-3A-28A[1A,3A], CA_1A-3A-32A, CA_1A-3A-40A[1A,3A,40A], CA_1A-7C, CA_1A-7A-8A, CA_1A-7A-20A[1A,7A,1A-7A], CA_1A-7A-28A[1A,7A], CA_1A-7A-32A, CA_1A-7A-40A[1A,7A,40A], CA_1A-8A-38A[1A,38A,1A-38A], CA_1A-20A-32A, CA_1A-40C[1A,40A,40C], CA_2A-4A-5A, CA_3C-5A, CA_3C-7A, CA_3A-3A-7A, CA_3C-8A[3A,3B,3C], CA_3C-20A[3A,3B,3C], CA_3A-3A-20A[3A,3A-3A], CA_3C-28A, CA_3A-3A-28A, CA_3C-32A[3A,3B,3C], CA_3A-7B, CA_3A-7C, CA_3A-7A-8A[3A,7A,3A-7A], CA_3A-7A-20A[3A,7A,3A-7A], CA_3A-7A-28A, CA_3A-7A-32A[3A,7A,3A-7A], CA_3A-7A-40A[3A,7A,40A], CA_3A-8A-38A[3A,38A,3A-38A], CA_3A-28A-40A[3A,40A], CA_3A-40C[3A,40A,40C], CA_7C-20A[7A,7B,7C], CA_7B-28A[7A,7B], CA_7C-28A[7A,7B,7C], CA_7A-8A-38A[7A,38A,7A-38A], CA_7A-20A-32A[7A], CA_7A-20A-38A, CA_7A-40C[7A,40A,40C], CA_20A-38C[38A,38C], CA_28A-40C[40A,40C]"
#     ca4 = "CA_1A-3C-7A, CA_1A-3C-20A, CA_1A-3C-28A, CA_1A-3A-7C, CA_1A-3A-40C, CA_1A-7C-20A, CA_1A-7C-28A[1A,7A], CA_1A-7A-40C, CA_3C-7C, CA_3C-7A-20A, CA_3C-7A-28A, CA_3C-7A-32A, CA_3A-7C-20A, CA_3A-7C-28A, CA_3A-7A-40C, CA_3A-28A-40C, CA_3A-40D"
#     test.get_ca_comb(4,ca4)
    tc_conf = TestConfig()
    print(tc_conf.config["weidehui"])
        