import json
import time
from pathlib import Path
from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
from base_tool.number_get import number_get, parse_chinese_number
from base_tool.projection_root import find_project_root
from base_tool.get_matches import get_matches, get_wait_matches, ResultProcessor
import json
from collections import Counter

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
class jingjichang():
    def __init__(self, AndroidDevice, json_reader):
        self.device = AndroidDevice
        self.jingji_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.numberget = number_get(AndroidDevice, json_reader)

    def enter_weituo(self):
        # 先回到主页
        self.back.back_to_main()
        # 进入七宗罪
        self.device.tap_on_screen(self.device.wait_for_image(self.jingji_json.img_path('竞技训练入口'))[0])
        self.device.tap_on_screen(self.device.wait_for_image(self.jingji_json.img_path('竞技场入口'))[0])
    def start(self):
        self.enter_weituo()
        while True:
            self.device.tap_on_screen(self.device.wait_for_image(self.jingji_json.img_path('竞技场站五次',),timeout=3)[0])
            self.device.tap_on_screen(self.device.wait_for_image(self.jingji_json.img_path('站五次后的确定'),timeout=3)[0])

            if self.device.wait_for_image(self.jingji_json.img_path('竞技场挑战券不足的弹窗'),timeout=3) != [0]:
                self.back.back()
                time.sleep(4)
                self.device.tap_on_screen(self.device.wait_for_image(self.jingji_json.img_path('竞技场领取馈赠'))[0])
                time.sleep(4)
                return True






# dd=jingjichang(device,jingji_json)
# dd.start()
