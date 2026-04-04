# import json
import time

from assignment.zhuxian.主线剧情 import device
# from pathlib import Path
from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
from base_tool.number_get import number_get, parse_chinese_number
from base_tool.projection_root import find_project_root
from base_tool.get_matches import get_matches, get_wait_matches, ResultProcessor
# import json
import datetime
# 获取当前脚本文件的绝对路径
# script_dir = find_project_root()
# # 定义 seven.json 的绝对路径
# tmp_AC_file = script_dir / 'base_tool' / 'location' / 'tmp_AC' / 'tmp_AC.json'
# img_file = script_dir / 'base_tool'  # 定义好图片的根目录
# print(img_file)
# # 检查文件是否存在
# if not tmp_AC_file.exists():
#     print(f"信息文件不存在: {tmp_AC_file}")
#     # 根据需要，可以选择创建文件或通过GUI应用程序生成
#     exit()
# tmp_AC_json = json_reader(tmp_AC_file)
# device = AndroidDevice()
# device.img_path_abs = img_file
# device.connect_device()


class world_hunt():
    def __init__(self, AndroidDevice, json_reader,flag=1,stop_event=None,world_hunt_option=3):
        self.device = AndroidDevice
        self.tmp_AC_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.num_shoulie = 0
        self.num_fuhuoing = 0
        self.flag=flag
        self.numberget = number_get(AndroidDevice, json_reader)
        self.stop_event = stop_event
        self.strategy=world_hunt_option

    def enter_world_hunt(self):
        # 先回到主页

        self.back.back_to_main()
        # 进入七宗罪
        self.device.tap_on_screen(self.device.get_centra(self.tmp_AC_json.img_areas('限时玩法进入位置')[0],self.tmp_AC_json.img_areas('限时玩法进入位置')[1]))
        self.device.tap_on_screen(self.device.wait_for_image(self.tmp_AC_json.img_path('世界狩猎位置（周日）'))[0])
        time.sleep(2)
        if self.flag==0:
            self.device.tap_on_screen(self.device.wait_for_image(self.tmp_AC_json.img_path('普通狩猎场'))[0])
        time.sleep(4)
        self.num_shoulie = int(self.numberget.extract_numbers('世界狩猎狩猎次数剩余区域', excluded_number=-1)[0])
    def taofa(self):
        long_name = ['世界狩猎地图中的罪渊龙蜥', '世界狩猎地图中的龙侍三代种', '世界狩猎地图中的深厄蝮龙']
        pre_img=device.capture_screenshot()
        self.device.tap_on_screen(
            self.device.wait_for_image(self.tmp_AC_json.img_path('世界狩猎前往狩猎'))[0])
        time.sleep(3)
        cur_img = device.capture_screenshot()
        if device.compare_images(pre_img,cur_img,threshold=0.8)==True:
            self.device.tap_on_screen(
                self.device.wait_for_image(self.tmp_AC_json.img_path('普通狩猎场'),threshold=0.6)[0])
            time.sleep(2)
            self.device.tap_on_screen(self.device.get_centra(self.tmp_AC_json.img_areas('世界狩猎前往狩猎')[0],
                                                             self.tmp_AC_json.img_areas('世界狩猎前往狩猎')[1]))
            time.sleep(2)
            self.back.back()
            time.sleep(2)
            self.device.tap_on_screen(self.device.get_centra(self.tmp_AC_json.img_areas('高级狩猎场')[0],
                                                             self.tmp_AC_json.img_areas('高级狩猎场')[1]))
            time.sleep(2)
            self.device.tap_on_screen(
                self.device.wait_for_image(self.tmp_AC_json.img_path('世界狩猎前往狩猎'))[0])
        self.device.tap_on_screen(
            self.device.wait_for_image(self.tmp_AC_json.img_path(long_name[self.strategy-1]))[0])
        img1=device.capture_screenshot()
        self.device.tap_on_screen(
            self.device.wait_for_image(self.tmp_AC_json.img_path('世界狩猎点开首领后的挑战'), timeout=20)[
                0])
        time.sleep(2)
        img2=device.capture_screenshot()
        if device.compare_images(img1,img2,threshold=0.8)==True:
            self.enter_world_hunt()
            self.taofa()


        while True:
            finished_flag = self.device.wait_for_image(self.tmp_AC_json.img_path('世界狩猎狩猎完成宝箱点击区域'))[0]
            if finished_flag != 0:
                time.sleep(2)
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.tmp_AC_json.img_path('世界狩猎狩猎完成宝箱点击区域'))[
                        0])
                time.sleep(2)
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.tmp_AC_json.img_path('点击空白处关闭'))[0])
                time.sleep(2)
                self.device.tap_on_screen(self.device.get_centra(self.tmp_AC_json.img_areas('点击空白处关闭')[0],
                                                                 self.tmp_AC_json.img_areas('点击空白处关闭')[1]))
                time.sleep(2)
                self.device.tap_on_screen(
                    self.device.get_centra(self.tmp_AC_json.img_areas('点击空白处关闭')[0],
                                           self.tmp_AC_json.img_areas('点击空白处关闭')[1]))
                time.sleep(2.5)
                self.back.back()
                time.sleep(4)
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.tmp_AC_json.img_path('普通狩猎场'), threshold=0.6)[0])
                time.sleep(2)
                self.device.tap_on_screen(self.device.get_centra(self.tmp_AC_json.img_areas('世界狩猎前往狩猎')[0],
                                                                 self.tmp_AC_json.img_areas('世界狩猎前往狩猎')[1]))
                time.sleep(2)
                self.back.back()
                time.sleep(2)
                self.device.tap_on_screen(self.device.get_centra(self.tmp_AC_json.img_areas('高级狩猎场')[0],
                                                                 self.tmp_AC_json.img_areas('高级狩猎场')[1]))
                self.num_shoulie -= 1
                return True
    def start(self):
        # 获取当前时间
        now = datetime.datetime.now()

        # 获取当前小时
        current_hour = now.hour
        if current_hour < 10 :
            print('狩猎未到开放时间')
            return True
        start_time = time.perf_counter()
        self.enter_world_hunt()
        print(self.num_shoulie)

        if self.num_shoulie == 0:
            return True

        while True:
            if self.num_shoulie == 0:
                time.sleep(4)
                self.back.back()
                time.sleep(4)
                return True
            if self.strategy==1:
                zui_flag = get_matches(self.tmp_AC_json, self.tmp_AC_json, self.device, '世界狩猎罪渊龙蜥复活检测区域',
                                       '世界狩猎高级狩猎场复活中标志', mask_name='世界狩猎复活检测',timeout=5)
                if zui_flag ==[0]:
                    time.sleep(2)
                    self.device.tap_on_screen(device.get_centra(self.tmp_AC_json.img_areas('世界狩猎罪渊龙蜥复活检测区域')[0],
                                                                self.tmp_AC_json.img_areas('世界狩猎罪渊龙蜥复活检测区域')[1]))
                    time.sleep(2)
                    self.taofa()

            elif self.strategy==2:
                long_flag = get_matches(self.tmp_AC_json, self.tmp_AC_json, self.device,
                                        '世界狩猎龙侍三代种复活检测区域',
                                        '世界狩猎高级狩猎场复活中标志', mask_name='世界狩猎复活检测',timeout=5)
                if long_flag == [0]:
                    time.sleep(1)
                    self.device.tap_on_screen(
                        device.get_centra(self.tmp_AC_json.img_areas('世界狩猎龙侍三代种复活检测区域')[0],
                                          self.tmp_AC_json.img_areas('世界狩猎龙侍三代种复活检测区域')[1]))
                    time.sleep(2)
                    self.taofa()
            elif self.strategy==3:
                shen_flag = get_matches(self.tmp_AC_json, self.tmp_AC_json, self.device, '世界狩猎深厄蝮龙复活检测区域',
                                        '世界狩猎高级狩猎场复活中标志', mask_name='世界狩猎复活检测',timeout=5)
                if shen_flag == [0]:
                    time.sleep(1)
                    self.device.tap_on_screen(
                        device.get_centra(self.tmp_AC_json.img_areas('世界狩猎深厄蝮龙复活检测区域')[0],
                                          self.tmp_AC_json.img_areas('世界狩猎深厄蝮龙复活检测区域')[1]))
                    time.sleep(2)
                    self.taofa()
            else:
                print('无效数字')
                return True













# dd=world_hunt(device,tmp_AC_json)
# dd.start()