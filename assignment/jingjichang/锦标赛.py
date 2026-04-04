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
import  datetime
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
class jingbiaosai():
    def __init__(self, AndroidDevice, json_reader):
        self.device = AndroidDevice
        self.jingji_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.numberget = number_get(AndroidDevice, json_reader)

    def enter_jingbiaosai(self):
        # 先回到主页
        self.back.back_to_main()
        # 进入七宗罪
        self.device.tap_on_screen(self.device.wait_for_image(self.jingji_json.img_path('竞技训练入口'))[0])
        time.sleep(1)
        img1=self.device.capture_screenshot()
        time.sleep(2)
        self.device.tap_on_screen(self.device.wait_for_image(self.jingji_json.img_path('锦标赛入口'))[0])
        time.sleep(2)
        img2 = self.device.capture_screenshot()
        if self.device.compare_images(img1,img2,threshold=0.8)==True:
            print('当前账号未开启锦标赛')
            return True

    def start(self):


        # 获取当前时间
        now = datetime.datetime.now()

        # 获取当前小时
        current_hour = now.hour
        if current_hour < 10 or current_hour > 20:
            print('锦标赛未到开放时间')
            return True
        print("当前小时:", current_hour)
        if self.enter_jingbiaosai():
            return True
        # while True:
        time.sleep(3)
        self.device.tap_on_screen(
            self.device.get_centra(self.jingji_json.img_areas('点击空白处关闭')[0],
                                   self.jingji_json.img_areas('点击空白处关闭')[1]))
        time.sleep(3)
        self.device.tap_on_screen(
            self.device.get_centra(self.jingji_json.img_areas('点击空白处关闭')[0],
                                   self.jingji_json.img_areas('点击空白处关闭')[1]))
        tiaozhan_loc=self.device.wait_for_image(self.jingji_json.img_path('锦标赛挑战标志'),threshold=0.7)
        if tiaozhan_loc!=[0]:
            for i in  tiaozhan_loc:
                time.sleep(3)
                self.device.tap_on_screen(i)
                self.device.tap_on_screen(self.device.wait_for_image(self.jingji_json.img_path('锦标赛发起挑战'))[0])
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.jingji_json.img_path('跳过战斗'), mask_name='跳过战斗',threshold=0.6,timeout=20)[0])

                time.sleep(1)
                self.device.tap_on_screen(
                        self.device.get_centra(self.jingji_json.img_areas('点击空白处关闭')[0],
                                               self.jingji_json.img_areas('点击空白处关闭')[1]))
                time.sleep(2)
                self.device.tap_on_screen(
                        self.device.get_centra(self.jingji_json.img_areas('点击空白处关闭')[0],
                                               self.jingji_json.img_areas('点击空白处关闭')[1]))
                time.sleep(2)
                self.device.tap_on_screen(
                    self.device.get_centra(self.jingji_json.img_areas('点击空白处关闭')[0],
                                           self.jingji_json.img_areas('点击空白处关闭')[1]))
                time.sleep(2)
                self.device.tap_on_screen(
                    self.device.get_centra(self.jingji_json.img_areas('点击空白处关闭')[0],
                                           self.jingji_json.img_areas('点击空白处关闭')[1]))

            return True


        else:
            print('挑战完成')
            return True
# dd=jingbiaosai(device,jingji_json)
# dd.start()
