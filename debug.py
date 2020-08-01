# -*- coding:gbk -*-
'''

@author: weidh2


'''
import os
import csv

# a = os.getcwd()
# file_name = "ca_combs.xlsx"
# path = os.path.join(a,file_name)
# print(path)
# import modules
# from modules import MeasureCA
# a  = __import__("modules.MeasureCA",fromlist=["MeasureCA"])
# print(a)
# b = a.MeasureCA("fwk")

# import visa
# import csv
# import os
# from configobj import ConfigObj
# import time
# root_path = os.getcwd()
# test_config_path = root_path + "\\test_config.ini"
# test_config_obj = ConfigObj(test_config_path)
# # print(test_config_obj)
# sections = test_config_obj.sections
# print(sections)
# cfg = {}
# for section in test_config_obj.sections:
#     print (section)
#     print(test_config_obj[section].iteritems())
#     for key,value in test_config_obj[section].iteritems():
#         print("key is %s value is %s"%(key,value))
#         cfg[key]
# sections = test_config_parser.senctions()
# print(sections)
# from lib2to3.fixer_util import Newline
# root_path = os.getcwd()
# file = root_path + "//log" + ".csv"
# filedesc = open(file,"a",newline = '')
# writer = csv.writer(filedesc)
# # house_title = house_title.encode("utf8")
# # b = a.encode('utf-8')
# # print(type(b))
# writer.writerow(["hahhahh"])
# a = []
# b = {"a":[1,2,3]}
# def get_new_list(tar_dic):
#     a = tar_dic
#     print(a)
#     a.append(4)
#     return a
#     
# d = get_new_list(b["a"])
# print(d)
# print(b["a"])
# log_root = os.getcwd()
# print(log_root)
# conf_path = log_root + "\\test_config.ini"
# print(conf_path)

import re
# a = "1A-20A"
# import re
import logging
log = logging.Logger("test")
import re
a=1
def get_ca_comb(combos,csv_file):
    
#     if a ==1:
#         raise ("test stop")
    print(csv_file)
    fileDesc = open(csv_file, 'a', newline = "")
    writer = csv.writer(fileDesc, delimiter=',')
    combos_split = re.split("CA_|DC_",combos)
#     print("******",combos_split)
    combos_num  =len(combos_split)
    combos = combos.split(",")
#     print("tydefueh",combos)
    print("combos number is %d"%combos_num)
#     print("combos number is %d"%len(combos))
    for combo in combos:
        list = []
        
#         print(combo)
#         new_combos = re.split("CA_","[","DC_",combo)
#         print("hhhh",combo)
        if "DC_" not in combo and "CA_" not in combo:
            continue
        combolist_sp = re.split("DC_|CA_",combo)
        print(combolist_sp)
        for combo_list_n in combolist_sp:
            if combo_list_n == " ":
                continue
            new_combos = combo_list_n.split("[")
        print(new_combos[0])
        new_combos[0].replace("_","-")
#         for comb in new_combos:
#             list = []
#             if comb == " " or comb == ",":
#                 continue
#             comboss = comb.split("[")
#         
#             print(comboss[0])
        list.append(new_combos[0])
        writer.writerow(list)
            
    def creat_csv():
        csv_file = os.getcwd()+"\\" + "combos" + ".csv"
        if os.path.exists(csv_file):
            os.remove(csv_file)
        file_desvc = open(csv_file, 'a', newline = "")
#     if ca_type != 'DC':
#         c = a.replace(" ","").replace(",","").split("CA_")
#         for i in c:
#         #     print(i)
#             if "C" in i or "B" in i or "D" in i:
#                 print(i)
#         print(c)
#         d = len(c)
#         log.error("there are ca comb %s"%(d-1))
#         if ca_type == 2:
#             re1 = re.compile(r"(\d+[A-Za-z]-\d+[A_Za-z])\S")
#             list = re1.findall(a)
#             print(list)
#             for i in list:
#                 print (i)
#         elif ca_type == 3:
#             re1 = re.compile(r"(\d+[A-Za-z]-\d+[A_Za-z]-\d+[A_Za-z])\S")
#             list = re1.findall(a)
#             print(list)
#             for i in list:
#                 print (i)
#     else:
#         c = a.replace(" ","").replace(",","").split("DC_")
#         print("DC ca_combs is %d"%(len(c)-1))
#         for i in c:
#             print(i)
#     
# ca2 ="CA_1C, CA_1A-1A, CA_1A-3A, CA_1A-5A, CA_1A-7A, CA_1A-8A, CA_1A-20A, CA_1A-28A, CA_1A-32A, CA_1A-38A[All], CA_1A-40A[1A,40A], CA_2A-4A, CA_2A-5A, CA_3C[All], CA_3A-3A[All], CA_3A-5A, CA_3A-7A[All], CA_3A-8A[3A], CA_3A-20A[3A], CA_3A-28A, CA_3A-32A, CA_3A-38A[All], CA_3A-40A[3A,40A], CA_4A-4A, CA_4A-5A, CA_4A-7A, CA_5A-38A, CA_5A-41A, CA_7B[All], CA_7C[All], CA_7A-7A[All], CA_7A-8A[7A], CA_7A-20A[7A], CA_7A-28A, CA_7A-32A[7A], CA_7A-40A[7A,40A], CA_8A-28A, CA_8A-32A, CA_8A-38A[38A], CA_8A-40A, CA_20A-32A, CA_20A-38A[38A], CA_20A-40A, CA_28A-40A[40A], CA_38C[All], CA_40C" 
ca1 = "CA_2A-2A[All], CA_2A-4A[All], CA_2A-5A[2A], CA_2A-13A[2A], CA_2A-66A[All], CA_4A-4A[All], CA_4A-5A[4A], CA_4A-13A[4A], CA_5B, CA_5A-5A, CA_5A-66A[66A], CA_13A-66A[66A], CA_66B[All], CA_66C[All], CA_66A-66A[All]"
ca2 = "CA_2A-2A-4A, CA_2A-2A-5A, CA_2A-2A-13A, CA_2A-2A-66A, CA_2A-4A-4A, CA_2A-4A-5A, CA_2A-4A-13A, CA_2A-5B[2A], CA_2A-5A-66A, CA_2A-13A-66A, CA_2A-66B, CA_2A-66C, CA_2A-66A-66A, CA_4A-4A-5A, CA_4A-4A-13A, CA_4A-5B, CA_5B-66A, CA_5A-5A-66A, CA_5A-66B, CA_5A-66C, CA_5A-66A-66A, CA_13A-66B, CA_13A-66C, CA_13A-66A-66A, CA_66D, CA_66A-66B, CA_66A-66C[All], CA_66A-66A-66A"
ca3 = "DC_1A_n3A[1A], DC_1A_n7A[All], DC_1A_n8A[1A], DC_1A_n28A[1A], DC_1A_n38A[All], DC_1A_n77A[All], DC_1A_n78A[All], DC_3A_n1A[3A], DC_3A_n7A[All], DC_3A_n8A[3A], DC_3A_n28A[3A], DC_3A_n38A[All], DC_3A_n41A[n41A], DC_3A_n77A[n77A], DC_3A_n78A[All], DC_5A_n78A[n78A], DC_7A_n1A[7A], DC_7A_n3A[7A], DC_7A_n28A[7A], DC_7A_n78A[All], DC_8A_n1A, DC_8A_n3A, DC_8A_n41A[n41A], DC_8A_n78A[n78A], DC_20A_n1A, DC_20A_n3A, DC_20A_n38A, DC_20A_n78A[n78A], DC_28A_n78A[n78A], DC_38A_n78A[All], DC_1A-3A_n28A[1A,3A,1A-3A], DC_1A-3A_n78A[All], DC_1A-7A_n3A[1A,7A], DC_1A-7A_n28A[1A,7A,1A-7A], DC_1A-7A_n78A[All], DC_1A-8A_n3A[1A], DC_1A-8A_n78A[1A,n78A], DC_1A-20A_n3A[1A], DC_1A-20A_n78A[1A,n78A,1A-n78A], DC_1A-28A_n78A[1A,n78A,1A-n78A], DC_3C_n28A[3A,3C], DC_3C_n78A[All], DC_3A-7A_n28A[3A,7A,3A-7A], DC_3A-7A_n78A[3A,7A,n78A], DC_3A-8A_n78A[3A,n78A,3A-n78A], DC_3A-20A_n78A[3A,n78A,3A-n78A], DC_3A-28A_n78A[3A,n78A,3A-n78A], DC_3A-38A_n78A[3A,n78A,3A-n78A], DC_7C_n28A[7A,7C], DC_7C_n78A[All], DC_7A-20A_n3A[7A], DC_7A-20A_n78A[7A,n78A,7A-n78A], DC_7A-28A_n78A[7A,n78A,7A-n78A], DC_1A-3C_n28A[1A,3C], DC_1A-7C_n28A[1A,7C], DC_3A-3A-7A_n1A, DC_3C-7A_n28A[7A,3C], DC_3A-3A-7A_n78A, DC_3A-7A-7A_n1A[7A], DC_3A-7C_n28A[3A,7C], DC_3C-7C_n28A"

combos_path = os.getcwd() + "\\" + "03_document"+"\\" "combos_of_OD.txt"
combos_file = open(combos_path,"r")

csv_file = os.getcwd()+"\\" + "03_document" + "\\" +  "combos" + ".csv"
if os.path.exists(csv_file):
    os.remove(csv_file)
for ca in combos_file.readlines():
    print(ca)
# list = [ca1,ca2,ca3]
# for ca in list:
    get_ca_comb(ca,csv_file)
# import wx
# # import wx
# 
# 
# # class Example(wx.Frame):
# 
#     def __init__(self, parent, title):
#         super(Example, self).__init__(parent, title=title,
#             size=(350, 300))
# 
#         self.InitUI()
#         self.Centre()
# 
#     def InitUI(self):
# 
#         self.panel = wx.Panel(self)
# 
#         self.panel.SetBackgroundColour("gray")
# 
#         self.LoadImages()
# 
#         self.mincol.SetPosition((20, 20))
#         self.bardejov.SetPosition((40, 160))
#         self.rotunda.SetPosition((170, 50))
# 
# 
#     def LoadImages(self):
# 
#         self.mincol = wx.StaticBitmap(self.panel, wx.ID_ANY,
#             wx.Bitmap("mincol.jpg", wx.BITMAP_TYPE_ANY))
# 
#         self.bardejov = wx.StaticBitmap(self.panel, wx.ID_ANY,
#             wx.Bitmap("bardejov.jpg", wx.BITMAP_TYPE_ANY))
# 
#         self.rotunda = wx.StaticBitmap(self.panel, wx.ID_ANY,
#             wx.Bitmap("rotunda.jpg", wx.BITMAP_TYPE_ANY))
# 
# 
# def main():
# 
#     app = wx.App()
#     ex = Example(None, title='Absolute positioning')
#     ex.Show()
#     app.MainLoop()
# 
# 
# if __name__ == '__main__':
#     main()
