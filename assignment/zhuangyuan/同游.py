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

class tongyou:
    def __init__(self,AndroidDevice,json_reader):
        self.device=AndroidDevice
        self.Zhuangyuan_json=json_reader
        self.back = BackToMain(AndroidDevice)
        self.finish=False
        self.res_numn=1
        self.number_get = number_get(AndroidDevice=self.device, json_reader=self.Zhuangyuan_json)
    def enter_tongyou(self):
        self.back.back_to_main()
        self.device.tap_on_screen(
            self.device.wait_for_image(self.Zhuangyuan_json.img_path('主页庄园图标'), threshold=0.95)[0])
        self.device.tap_on_screen(
            self.device.wait_for_image(self.Zhuangyuan_json.img_path('同游按钮'), threshold=0.8,timeout=15)[0])
        time.sleep(2)
        self.res_numn = int(self.number_get.extract_numbers(loc_name='剩余要求次数',
                                                           excluded_number=-1)[0])

    def start(self):
        while True:
            self.enter_tongyou()
            if self.res_numn == 0:
                self.finish = True
                return True
            else:
                # self.device.get_centra(self.Zhuangyuan_json.img_areas('第一个同游人物位置')[0],self.Zhuangyuan_json.img_areas('第一个同游人物位置')[1])
                # time.sleep(1)
                yaoqingty = self.device.wait_for_image(self.Zhuangyuan_json.img_path('邀请同游按钮'), threshold=0.99)[0]
                if yaoqingty != 0:
                    img1=self.device.capture_screenshot()
                    print('进入同游选择界面')
                    self.device.tap_on_screen(
                        self.device.get_centra(self.Zhuangyuan_json.img_areas('第一个同游人物位置')[0],
                                               self.Zhuangyuan_json.img_areas('第一个同游人物位置')[1]))
                    time.sleep(2)
                    self.device.tap_on_screen(yaoqingty)
                    time.sleep(2)
                    img2 = self.device.capture_screenshot()
                    if self.device.compare_images(img1, img2, threshold=0.8) == True:
                        print('同游次数不足')
                        return True

                time.sleep(1)
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.Zhuangyuan_json.img_path('闲聊'), use_color=True, timeout=8,
                                               threshold=0.9)[0])
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.Zhuangyuan_json.img_path('跳过'), mask_name='同游跳过白色')[0])
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.Zhuangyuan_json.img_path('闲聊跳过后的确认'))[0])
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.Zhuangyuan_json.img_path('闲聊跳过确认后的摄影'))[0])
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.Zhuangyuan_json.img_path('摄影后的点击屏幕继续'))[0])
                if self.device.wait_for_image(self.Zhuangyuan_json.img_path('闲聊完成点击空白处关闭'))[0] != 0:
                    self.device.tap_on_screen(
                        self.device.wait_for_image(self.Zhuangyuan_json.img_path('闲聊完成点击空白处关闭'))[0])




# tongyou=tongyou(device,Zhuangyuan_json)
# if tongyou.start() == False:
#     back2main.back_to_main()





