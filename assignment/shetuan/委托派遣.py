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


class weituo():
    def __init__(self, AndroidDevice, json_reader):
        self.device = AndroidDevice
        self.shetuan_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.numberget = number_get(AndroidDevice, json_reader)
    def enter_weituo(self):
        # 先回到主页
        self.back.back_to_main()
        # 进入七宗罪
        self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团入口'))[0])
        self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('委托派遣入口'))[0])
    def start(self):
        self.enter_weituo()
        while True:
            paiqian_loc = self.device.wait_for_image(self.shetuan_json.img_path('委托派遣按钮'))

            if paiqian_loc != [0]:
                for i in paiqian_loc:
                    self.device.tap_on_screen(i)
                    time.sleep(1)
                    self.device.tap_on_screen(
                        self.device.get_centra(self.shetuan_json.img_areas('点击空白处关闭')[0],
                                               self.shetuan_json.img_areas('点击空白处关闭')[1]))
                    time.sleep(2)
                    self.device.tap_on_screen(
                        self.device.wait_for_image(self.shetuan_json.img_path('委托派遣一键选人按钮'))[0])
                    self.device.tap_on_screen(
                        self.device.wait_for_image(self.shetuan_json.img_path('委托派遣选人完成出发'))[0])
                    self.device.tap_on_screen(
                        self.device.wait_for_image(self.shetuan_json.img_path('委托派遣出发后的求援按钮'))[0])
            time.sleep(2)
            if self.fanye():
                continue
            else:
                print("已完成")
                return True


    def fanye(self):
        test_loc1 = self.device.local_get(self.shetuan_json.img_areas('社团派遣滑动区域')[0],
                                     self.shetuan_json.img_areas('社团派遣滑动区域')[1])
        time.sleep(2)
        self.device.swipe_on_screen(self.shetuan_json.img_areas('社团派遣滑动区域')[1],
                                    self.shetuan_json.img_areas('社团派遣滑动区域')[0], duration=500)
        time.sleep(2)
        test_loc2 = self.device.local_get(self.shetuan_json.img_areas('社团派遣滑动区域')[0],
                                     self.shetuan_json.img_areas('社团派遣滑动区域')[1])
        if self.device.compare_images(image1_path=test_loc1, image2_path=test_loc2, threshold=0.80) != True:
            print('换页成功')
            return True
        else:
            print('换页存在问题')
            return False
# dd=weituo(device,shetuan_json)
# dd.start()