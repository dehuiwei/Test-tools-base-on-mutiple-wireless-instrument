'''

@author: weidh2
'''
import os
import logging
# import Modem_CA_Verify_Keysight
# import imp
import time
from fwk.Output_Log import  *
import fwk.test_config
class TestFramework(object):
    def __init__(self):
        self.log_time = time.strftime("%Y_%m_%d_%H_%M")
        self.log_root = "%s\\01_logs_%s" % (os.getcwd(), time.strftime("%Y-%m-%d_%H%M%S"))
        if not os.path.exists(self.log_root):
            os.mkdir(self.log_root)
        Logs = Log(self.log_root)
        self.log = Logs.getlog()
        
        self.config = fwk.test_config.TestConfig(self)
        self.cfg = self.config.config
        print("this is farther class TestFramework")
           
            
    def get_tc_module(self):
        
        tc_module = self.cfg["tc_module"]
        print("tc_module is ",tc_module)
        try: 
            tc_module_name = "modules.%s"%tc_module
            tc_modules = __import__(tc_module_name,fromlist=[tc_module]) 
            self.log.info(tc_modules)
#             imp.reload(tc_module)
            tc_object = getattr(tc_modules,tc_module)(self)#### add self
            return  tc_object
        except:
#             self.log.error("Dynamic loading failed for TC module: %s!" % tc_module_name)
            return None  
class Main(object):
    def __init__(self):
#         pass
#         self.log = logging.Logger("MODE_LOG")
        self.log_root_result = "%s\\log\\result_%s\\" % (os.getcwd(), time.strftime("%Y-%m-%d_%H%M%S"))
#         if not os.path.exists(self.log_root):
#             os.mkdir(self.log_root)
#         self.log_root = os.getcwd()+'\log'+"\\result\\"
#         print(self.log_root)
        self.result_path = self.log_root_result
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)
        print("this is farther class Main")
        

        
if __name__ == "__main__":           
    test = TestFramework()
    tc_object = test.get_tc_module()
    tc_object.main()

