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
#
# # 获取当前脚本文件的绝对路径
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


class hongbao():
    def __init__(self, AndroidDevice, json_reader):
        self.device = AndroidDevice
        self.shetuan_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.numberget = number_get(AndroidDevice, json_reader)
        self.res_num=10
    def enter_hongbao(self):
        # 先回到主页
        self.back.back_to_main()
        # 进入七宗罪
        self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团入口'))[0])
        self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团红包入口'))[0])
        time.sleep(4)
        self.res_num = int(
            self.numberget.extract_numbers('社团红包剩余可以抢的次数', excluded_number=-1)[0])
        print(self.res_num)

    def start(self):
        self.enter_hongbao()
        while True:
            if self.res_num==0:
                break
            if self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团红包领取'))[0]):
                self.res_num-=1
                time.sleep(1.5)
                self.device.tap_on_screen(
                    self.device.get_centra(self.shetuan_json.img_areas('点击空白处关闭')[0],
                                           self.shetuan_json.img_areas('点击空白处关闭')[1]))
                time.sleep(1.5)

            else:

                print('没可领取红包')
                break
        while True:
            if self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团红包发的模板'),threshold=0.85,timeout=6)[0]):



                time.sleep(2.5)
                self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团红包发放的确认'),threshold=0.98)[0])
                time.sleep(2)
                self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团红包发放完的领取'))[0])
                time.sleep(2)
                self.device.tap_on_screen(
                    self.device.get_centra(self.shetuan_json.img_areas('点击空白处关闭')[0],
                                           self.shetuan_json.img_areas('点击空白处关闭')[1]))
            else:
                return True



# dd=hongbao(device,shetuan_json)
# dd.start()
