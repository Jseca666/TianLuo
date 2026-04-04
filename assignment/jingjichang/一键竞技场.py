from assignment.jingjichang.学院风云 import xueyuanfengyun
from assignment.jingjichang.竞技场 import jingjichang
from assignment.jingjichang.锦标赛 import jingbiaosai
import json
import time
from pathlib import Path
from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
from base_tool.read_json import json_reader
from base_tool.projection_root import find_project_root
# 获取当前脚本文件的绝对路径
# script_dir = find_project_root()
# # 定义 seven.json 的绝对路径
# jingji_file = script_dir / 'base_tool' / 'location' / 'jingjichang' / 'jingjichang.json'
# img_file = script_dir / 'base_tool'  # 定义好图片的根目录
# print(img_file)
# # 检查文件是否存在
# if not jingji_file.exists():
#     print(f"信息文件不存在: {jingji_file}")
#     # 根据需要，可以选择创建文件或通过GUI应用程序生成
#     exit()
# jingji_json = json_reader(jingji_file)
# device = AndroidDevice()
# device.img_path_abs = img_file
# device.connect_device()
class total_jingji():
    def __init__(self, AndroidDevice, json_reader, stop_event=None):
        self.device = AndroidDevice
        self.jingji_json = json_reader
        self.xueyuanfengyun=xueyuanfengyun(self.device,self.jingji_json)
        self.jingjichang=jingjichang(self.device,self.jingji_json)
        self.jingbiaosai=jingbiaosai(self.device,self.jingji_json)
        self.stop_event = stop_event
    def start(self):

        self.xueyuanfengyun.start()
        self.jingjichang.start()
        self.jingbiaosai.start()
# dd=total_jingji(device,jingji_json)
# dd.start()
