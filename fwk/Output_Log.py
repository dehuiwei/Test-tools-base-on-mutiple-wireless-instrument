# coding = utf-8
"""
    Function: This class in to save log to file
"""

#Load all modules needed by us
import  logging
import time
import  os


class Log():
    def __init__(self,log_root,logger=None):
  
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)

#         self.log_time = time.strftime("%Y_%m_%d_%H_%M")
#         self.log_root = "%s\\01_logs_%s" % (os.getcwd(), time.strftime("%Y-%m-%d_%H%M%S"))
#         if not os.path.exists(self.log_root):
#             os.mkdir(self.log_root)
#         file_dir = os.getcwd()+'\\log'
#         if not os.path.exists(file_dir):
#             os.mkdir(file_dir)
#         self.log_path = file_dir
#         self.log_name = self.log_path + "\\" + "log_"+self.log_time + '.txt'
        self.log_name = log_root + "\\" + "detail.txt"
        fh = logging.FileHandler(self.log_name)
        fh.setLevel(logging.INFO)

        #Create format of output log
        formatter = logging.Formatter('[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        #self.logger.removeHandler(fh)
        fh.close()

    def getlog(self):
        return self.logger



