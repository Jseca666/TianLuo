from assignment.nibo.联合行动 import lianhe
from assignment.nibo.轮回石廊 import lunhuishilang
from assignment.nibo.遗迹探索 import yijitansuo
import json
import time
# from pathlib import Path
# from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
# from base_tool.number_get import number_get,parse_chinese_number
# from base_tool.projection_root import find_project_root
# from base_tool.get_matches import get_matches,get_wait_matches,ResultProcessor
import json
# 获取当前脚本文件的绝对路径
# script_dir = find_project_root()
# # 定义 seven.json 的绝对路径
# NIBO_file = script_dir /'base_tool' /'location' / 'NIBO' / 'seven_info.json'
# img_file=script_dir /'base_tool'#定义好图片的根目录
# print(img_file)
# # 检查文件是否存在
# if not NIBO_file.exists():
#     print(f"信息文件不存在: {NIBO_file}")
#     # 根据需要，可以选择创建文件或通过GUI应用程序生成
#     exit()
# NIBO_json=json_reader(NIBO_file)
# device=AndroidDevice()
# device.img_path_abs=img_file
# device.connect_device()
class total_nibo():
    def __init__(self, AndroidDevice, json_reader,lianhe_flag=1,yiji_flag=1,lunhui_flag=1,lianhegongji_flag=1,stop_event=None):
        self.device = AndroidDevice
        self.NIBO_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.lianhe_flag=lianhe_flag
        self.yiji_flag=yiji_flag
        self.lunhui_flag=lunhui_flag
        self.yijitansuo=yijitansuo(self.device,self.NIBO_json)
        self.lianhegongji_flag=lianhegongji_flag
        self.lianhe = lianhe(self.device, self.NIBO_json, lianhegongji_flag=self.lianhegongji_flag)
        self.lunhuishilang=lunhuishilang(self.device,self.NIBO_json)
        self.stop_event = stop_event
    def start(self):
        pretime=time.perf_counter()

        if self.yiji_flag!=0:
            self.yijitansuo.start()
        if self.lunhui_flag!=0:
            self.lunhuishilang.start()
        if self.lianhe_flag!=0:
            self.lianhe.start()




# dd=total_nibo(device,NIBO_json)
# dd.start()