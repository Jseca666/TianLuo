# import json
import time
# from pathlib import Path
# from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
from base_tool.number_get import number_get,parse_chinese_number
# import json
# 获取当前脚本文件的绝对路径
# script_path = Path(__file__).resolve()
# print(script_path)
# # 获取脚本所在的目录
# script_dir = script_path.parent.parent.parent
# print(script_path)
# # 定义 seven.json 的绝对路径
# info_file = script_dir /'base_tool' /'location' / 'Zhuangyuan' / 'Zhuangyuan.json'
#
# img_file=script_dir /'base_tool'#定义好图片的根目录
# print(img_file)
# # 检查文件是否存在
# if not info_file.exists():
#     print(f"信息文件不存在: {info_file}")
#     # 根据需要，可以选择创建文件或通过GUI应用程序生成
#     exit()
# Zhuangyuan_json=json_reader(info_file)
# device=AndroidDevice()
# device.img_path_abs=img_file
# device.connect_device()
# back2main=BackToMain(device)

class lingqu:
    def __init__(self,AndroidDevice,json_reader):
        self.device=AndroidDevice
        self.Zhuangyuan_json=json_reader
        self.back = BackToMain(AndroidDevice)
        self.lingqu1=False
        self.res_numn=1
        self.number_get = number_get(AndroidDevice=self.device, json_reader=self.Zhuangyuan_json)
    def enter_lingqu(self):
        self.back.back_to_main()
        self.device.tap_on_screen(
            self.device.wait_for_image(self.Zhuangyuan_json.img_path('主页庄园图标'), threshold=0.95)[0])
    def rizhilingqu(self):
        self.enter_lingqu()
        self.device.tap_on_screen(
            self.device.wait_for_image(self.Zhuangyuan_json.img_path('日志领取'), threshold=0.90,timeout=15)[0])
        self.device.tap_on_screen(
            self.device.wait_for_image(self.Zhuangyuan_json.img_path('庄园领奖'), threshold=0.90,timeout=10)[0])
        self.device.tap_on_screen(
            self.device.wait_for_image(self.Zhuangyuan_json.img_path('全部领取'), threshold=0.90,timeout=10)[0])

    def start(self):
        self.rizhilingqu()
        self.enter_lingqu()
        if self.lingqu1==False:
            self.device.tap_on_screen(
                self.device.wait_for_image(self.Zhuangyuan_json.img_path('庄园指引（任务列表）'), threshold=0.95)[0])
            while True:
                if self.device.tap_on_screen(
                        self.device.wait_for_image(self.Zhuangyuan_json.img_path('庄园指引领取'), threshold=0.95,
                                                   timeout=3)[0]) == False:
                    break
                else:
                    self.device.tap_on_screen(
                        self.device.wait_for_image(self.Zhuangyuan_json.img_path('闲聊完成点击空白处关闭'),timeout=3)[0])
            self.lingqu1=True


