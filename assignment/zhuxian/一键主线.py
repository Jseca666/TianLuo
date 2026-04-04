from assignment.zhuxian.主线剧情 import zhuxian
from assignment.zhuxian.学院试炼 import shilian
from assignment.zhuxian.战术演练 import yanlian
# import json
# import time
# from pathlib import Path
# from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
# from base_tool.backtomain import BackToMain
# from base_tool.number_get import number_get, parse_chinese_number
# from base_tool.projection_root import find_project_root
# from base_tool.get_matches import get_matches, get_wait_matches, ResultProcessor
# import json
# from collections import Counter

# # 获取当前脚本文件的绝对路径
# script_dir = find_project_root()
# # 定义 seven.json 的绝对路径
# zhuxian_file = script_dir / 'base_tool' / 'location' / 'zhuxian' / 'zhuxian.json'
# img_file = script_dir / 'base_tool'  # 定义好图片的根目录
# print(img_file)
# zhuxian_json = json_reader(zhuxian_file)
# device = AndroidDevice()
# device.img_path_abs = img_file
# device.connect_device()
class yijian_zhuxian():
    def __init__(self, AndroidDevice, json_reader,yanlian_flag=None,nandu_flag=0,stop_event=None):
        self.device = AndroidDevice
        self.zhuxian_json = json_reader
        self.nandu_flag = nandu_flag
        self.yanlian_flag = yanlian_flag
        self.zhuxian = zhuxian(self.device, self.zhuxian_json, self.nandu_flag)
        self.shilian = shilian(self.device, self.zhuxian_json)
        self.yanlian=yanlian(self.device,self.zhuxian_json,self.yanlian_flag)
        self.stop_event = stop_event
    def start(self):
        self.zhuxian.start()
        self.shilian.start()
        self.yanlian.start()
# dd=yijian_zhuxian(device,zhuxian_json,nandu_flag=1,yanlian_flag=[1,1,1])
# dd.start()

