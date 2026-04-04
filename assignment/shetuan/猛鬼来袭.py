# import json
import time
# from pathlib import Path
# from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
from base_tool.number_get import number_get, parse_chinese_number
# from base_tool.projection_root import find_project_root
# from base_tool.get_matches import get_matches, get_wait_matches, ResultProcessor
# import json
# from collections import Counter

# 获取当前脚本文件的绝对路径
# script_dir = find_project_root()
# # 定义 seven.json 的绝对路径
# shetuan_file = script_dir / 'base_tool' / 'location' / 'shetuan' / 'shetuan.json'
# img_file = script_dir / 'base_tool'  # 定义好图片的根目录
# print(img_file)
# # 检查文件是否存在
# if not shetuan_file.exists():
#     print(f"信息文件不存在: {shetuan_file}")
#     # 根据需要，可以选择创建文件或通过GUI应用程序生成
#     exit()
# shetuan_json = json_reader(shetuan_file)
# device = AndroidDevice()
# device.img_path_abs = img_file
# device.connect_device()


class menggui():
    def __init__(self, AndroidDevice, json_reader):
        self.device = AndroidDevice
        self.shetuan_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.numberget = number_get(AndroidDevice, json_reader)

    def enter_menggui(self):
        # 先回到主页
        self.back.back_to_main()
        # 进入七宗罪
        self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团入口'))[0])
        self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团活动入口'))[0])
        self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('猛鬼来袭'))[0])
    def start(self):
        self.enter_menggui()
        self.device.tap_on_screen(self.device.get_centra(self.shetuan_json.img_areas('猛鬼入侵备战区域')[0],self.shetuan_json.img_areas('猛鬼入侵备战区域')[1]))
        self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('猛鬼入侵挑战'))[0])
        if self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('猛鬼入侵挑战确认'),timeout=5)[0]):
            while True:
                self.device.tap_on_screen(self.device.get_centra(self.shetuan_json.img_areas('跳过战斗')[0],
                                                            self.shetuan_json.img_areas('跳过战斗')[1]))
                if self.device.wait_for_image(self.shetuan_json.img_path('刷龙胜利'))[0] != 0:
                    print('挑战完成')
                    time.sleep(2)
                    self.device.tap_on_screen(
                        self.device.get_centra(self.shetuan_json.img_areas('点击空白处关闭')[0],
                                               self.shetuan_json.img_areas('点击空白处关闭')[1]))
                    time.sleep(2)
                    self.device.tap_on_screen(
                        self.device.get_centra(self.shetuan_json.img_areas('点击空白处关闭')[0],
                                               self.shetuan_json.img_areas('点击空白处关闭')[1]))
                    break
            time.sleep(2)
            self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('猛鬼入侵奖励入口'),timeout=6)[0])
            self.device.tap_on_screen(
            self.device.wait_for_image(self.shetuan_json.img_path('猛鬼入侵奖励入口后领取'))[0])
            time.sleep(2)
            self.device.tap_on_screen(self.device.get_centra(self.shetuan_json.img_areas('跳过战斗')[0],
                                                             self.shetuan_json.img_areas('跳过战斗')[1]))
            self.back.back()


        else:
            self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('猛鬼入侵奖励入口'),timeout=6)[0])
            time.sleep(2)
            self.device.tap_on_screen(
                self.device.wait_for_image(self.shetuan_json.img_path('猛鬼入侵奖励入口后领取'),timeout=3)[0])
            self.back.back()
            print('挑战任务已完成')
            return True
# dd=menggui(device,shetuan_json)
# dd.start()

