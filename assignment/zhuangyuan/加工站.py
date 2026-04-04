# import json
import time
# from pathlib import Path
# from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
from base_tool.number_get import number_get,parse_chinese_number
# from base_tool.projection_root import find_project_root
# from tubu_ares import is_point_in_union
import json
# 获取当前脚本文件的绝对路径
# script_path = Path(__file__).resolve()
# print(script_path)
# # 获取脚本所在的目录
# script_dir = script_path.parent.parent.parent
# print(script_path)
# # 定义 seven.json 的绝对路径
# ZJ_file = script_dir /'base_tool' /'location' / 'Zhuangyuan' / 'Zhuangyuan.json'
# bj=script_dir /'base_tool' /'location' / 'Zhuangyuan' /'baifangtouxiang'/'baifangtouxiang.json'
# img_file=script_dir /'base_tool'#定义好图片的根目录
# print(img_file)
# # 检查文件是否存在
# if not ZJ_file.exists():
#     print(f"信息文件不存在: {ZJ_file}")
#     # 根据需要，可以选择创建文件或通过GUI应用程序生成
#     exit()
# Zhuangyuan_json=json_reader(ZJ_file)
# baifang_json=json_reader(bj)
# device=AndroidDevice()
# device.img_path_abs=img_file
# device.connect_device()
class jiagongzhan():

    def __init__(self, AndroidDevice, json_reader):
        self.device = AndroidDevice
        self.Zhuangyuan_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.number_get = number_get(AndroidDevice=self.device, json_reader=self.Zhuangyuan_json)
        self.zuanshi=0
    def get_zuanshi(self):
        time.sleep(2)
        self.zuanshi=int(self.number_get.extract_numbers(loc_name='加工站内的钻石位置',
                                                     excluded_number=-1, mask_name='点击空白处关闭',kernel_size=1)[0])
    def start(self):
        start_time = time.time()
        self.back.back_to_main()
        self.device.tap_on_screen(
            self.device.wait_for_image(self.Zhuangyuan_json.img_path('主页庄园图标'), threshold=0.95)[0])
        self.device.tap_on_screen(
            self.device.wait_for_image(self.Zhuangyuan_json.img_path('庄园管家'), threshold=0.95,timeout=15)[0])
        self.device.tap_on_screen(
            self.device.wait_for_image(self.Zhuangyuan_json.img_path('庄园管家上的加工站'), threshold=0.95)[0])
        time.sleep(3)
        self.get_zuanshi()
        if self.device.tap_on_screen(
            self.device.wait_for_image(self.Zhuangyuan_json.img_path('加工站的全部领取按钮'), threshold=0.95,timeout=5)[0]):
            print('领取完毕')
        else:
            kong = self.device.wait_for_image(self.Zhuangyuan_json.img_path('剩余可加工区域'), threshold=0.90,timeout=6)
            # if
            # for i in kong:
            #     kong.remove(0)
            if kong !=[0]:
                count = len(kong)
                print(kong)
                print('count',count)
                max_refrash = 10
                if self.zuanshi >= 500:
                    while True:

                        chen = self.device.wait_for_image(self.Zhuangyuan_json.img_path('加工站列表中橙色的订单'),
                                                          threshold=0.8, mask_name='加工站橙色订单')
                        print(chen)
                        if chen !=[0]:
                            for i in range(len(chen)):
                                time.sleep(2)
                                if self.device.tap_on_screen(chen[i]) == True:
                                    self.device.tap_on_screen(
                                        self.device.wait_for_image(
                                            self.Zhuangyuan_json.img_path('加工站点击订单后的开始加工'),
                                            threshold=0.95)[0])
                                    count = count - 1
                                    if count == 0:
                                        print('今日加工任务以安排完成')
                                        return True


                        end_time = time.time()
                        if end_time - start_time >= 600:
                            print('已超时')
                            return False
                        time.sleep(2)
                        if count !=0:
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.Zhuangyuan_json.img_path('加工站用钻石刷新'),
                                                           threshold=0.95)[0])
                            max_refrash = max_refrash - 1

                        if max_refrash == 0:
                            if self.device.tap_on_screen(
                                    self.device.wait_for_image(self.Zhuangyuan_json.img_path('加工站列表中的紫色订单'),
                                                               threshold=0.95, mask_name='加工站紫色订单')[0]) == True:
                                self.device.tap_on_screen(self.device.wait_for_image(
                                    self.Zhuangyuan_json.img_path('加工站点击订单后的开始加工'), threshold=0.95)[0])
                                count = count - 1
                            if self.device.tap_on_screen(
                                    self.device.wait_for_image(self.Zhuangyuan_json.img_path('加工站列表中蓝色订单'),
                                                               threshold=0.95, mask_name='加工站蓝色订单')[0]) == True:
                                self.device.tap_on_screen(self.device.wait_for_image(
                                    self.Zhuangyuan_json.img_path('加工站点击订单后的开始加工'), threshold=0.95)[0])
                                count = count - 1
                else:
                    while True:

                        if self.device.tap_on_screen(
                                self.device.wait_for_image(self.Zhuangyuan_json.img_path('加工站列表中橙色的订单'),
                                                           threshold=0.8, mask_name='加工站橙色订单')[0]) == True:
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.Zhuangyuan_json.img_path('加工站点击订单后的开始加工'),
                                                           threshold=0.8)[0])

                            count = count - 1
                        if self.device.tap_on_screen(
                                self.device.wait_for_image(self.Zhuangyuan_json.img_path('加工站列表中的紫色订单'),
                                                           threshold=0.95, mask_name='加工站紫色订单')[0]) == True:
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.Zhuangyuan_json.img_path('加工站点击订单后的开始加工'),
                                                           threshold=0.95)[0])
                            count = count - 1
                        if self.device.tap_on_screen(
                                self.device.wait_for_image(self.Zhuangyuan_json.img_path('加工站列表中蓝色订单'),
                                                           threshold=0.95, mask_name='加工站蓝色订单')[0]) == True:
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.Zhuangyuan_json.img_path('加工站点击订单后的开始加工'),
                                                           threshold=0.95)[0])

                            count = count - 1
                        end_time = time.time()
                        if end_time - start_time >= 240:
                            print('已超时')
                            return False
            else:
                print('加工任务已完成')
                return True





# jiagongzhan=jiagongzhan(device,Zhuangyuan_json)
# jiagongzhan.start()

