# import json
import time
# from pathlib import Path
# from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
from base_tool.number_get import number_get,parse_chinese_number
from base_tool.find_loc import get_mul_matches
# from base_tool.projection_root import find_project_root
# from base_tool.get_matches import get_matches,get_wait_matches,ResultProcessor
# import json
# # 获取当前脚本文件的绝对路径
# script_dir = find_project_root()
# # 定义 seven.json 的绝对路径
# NIBO_file = script_dir /'base_tool' /'location' / 'NIBO' / 'seven_info.json'
# img_file=script_dir /'base_tool'#定义好图片的根目录
# print(img_file)
# # 检查文件是否存在
# if not NIBO_file.exists():
#     print(f"信息文件不存在: {NIBO_file}")
#     # 根据需要，可以选择创建文件或通过GUI应用程序生成
#     exit()
# NIBO_json=json_reader(NIBO_file)
# device=AndroidDevice()
# device.img_path_abs=img_file
# device.connect_device()
class lianhe():
    def __init__(self, AndroidDevice, NIBO_json,lianhegongji_flag=1):
        self.device = AndroidDevice
        self.NIBO_json = NIBO_json
        self.back = BackToMain(AndroidDevice)
        self.LIANHE=18
        self.gongji_flag=lianhegongji_flag
        self.numberget=number_get(AndroidDevice,NIBO_json)
        self.get_mul_matches = get_mul_matches(AndroidDevice, NIBO_json)
    def enter_lianhe(self):
        # 先回到主页
        self.back.back_to_main()
        # 进入七宗罪
        self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('尼伯龙根'))[0])

        if self.get_mul_matches.get_and_clik(target_names=['联合行动（获取七宗罪材料）', '联合行动2'], thresholds=[0.7],
                                          time_out=5):
            print('开始进行联合行动')
        else:
            print('联合行动进入失败')
            return True
        # text=device.get_text_from_screen(NIBO_json.img_areas('联合行动剩余次数区域')[0],NIBO_json.img_areas('联合行动剩余次数区域')[1])
        # print(text)
        time.sleep(3)




    def start(self):
        if self.enter_lianhe()==True:
            return True
        print(self.LIANHE)
        while True:

            if self.get_mul_matches.get_and_clik(target_names=['联合行动熔炼', '第二赛季熔炼2次'], thresholds=[0.7],
                                      time_out=5):
                self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('联合行动炼成截图'))[0])
                time.sleep(2)
            self.LIANHE = int(self.numberget.extract_numbers('联合行动剩余次数区域', excluded_number=-1)[0])
            if self.LIANHE == 0:
                return True
            if self.get_mul_matches.get_and_clik(target_names=['寻找队伍-七宗罪', '第二赛季寻找队伍'], thresholds=[0.7],
                                      time_out=5):
                self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('等级选择'))[0])
                self.device.swipe_on_screen(self.NIBO_json.img_areas('金银铜滚轮区域')[1],
                                            self.NIBO_json.img_areas('金银铜滚轮区域')[0])
                time.sleep(2)

                self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('金所在区域'), 0.99)[0])
                if self.gongji_flag == 1:
                    self.get_mul_matches.get_and_clik(target_names=['深渊之龙', '第二赛季镰鼬女王'], thresholds=[0.7],
                                                      time_out=5)
                    self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('侍龙之镣'))[0])
                if self.gongji_flag == 2:
                    self.get_mul_matches.get_and_clik(target_names=['深渊之龙', '第二赛季镰鼬女王'], thresholds=[0.7],
                                                      time_out=5)
                    self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('蝰龙之爪'))[0])
                if self.gongji_flag == 3:
                    self.get_mul_matches.get_and_clik(target_names=['深渊之龙', '第二赛季镰鼬女王'], thresholds=[0.7],
                                                      time_out=5)
                    self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('蛇蝮之心'))[0])
                if self.gongji_flag == 4:
                    self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('蛇蝮之心'))[0])
                    self.get_mul_matches.get_and_clik(target_names=['深渊之龙', '第二赛季镰鼬女王'], thresholds=[0.7],
                                                      time_out=5)

                suc = 1
                refrash_loc = self.device.wait_for_image(self.NIBO_json.img_path('刷新列表-七宗罪'))[0]
                entra_loc = self.device.get_centra(self.NIBO_json.img_areas('加入队伍-七宗罪')[0],
                                                   self.NIBO_json.img_areas('加入队伍-七宗罪')[1])
                while suc:
                    self.device.tap_on_screen(refrash_loc)
                    self.device.tap_on_screen(entra_loc)
                    time.sleep(2)
                    zun_loc = self.device.find_image_on_screen(self.NIBO_json.img_path('准备'))[0]
                    if zun_loc != 0:
                        self.device.tap_on_screen(zun_loc)
                        print('已找到队伍')
                        suc = 0
                        break

                # device.tap_on_screen(device.wait_for_image(json_reader.img_path('战斗开始')))
                while True:
                    if self.device.wait_for_image(self.NIBO_json.img_path('刷龙胜利'))[0] != 0:
                        time.sleep(2)
                        self.device.tap_on_screen(self.device.get_centra(self.NIBO_json.img_areas('取消退出')[0],
                                                                         self.NIBO_json.img_areas('取消退出')[1]))
                        time.sleep(2)
                        self.device.tap_on_screen(
                            self.device.wait_for_image(self.NIBO_json.img_path('点击空白处关闭'))[0])
                        self.LIANHE = self.LIANHE - 1

                        break
                    print('已超时重新寻找')
                    if self.get_mul_matches.get_wait(target_names=['寻找队伍-七宗罪', '第二赛季寻找队伍'], thresholds=[0.7],
                                      time_out=5):
                        print('已被踢出队伍重新加入')
                        break













                
# dd=lianhe(device,NIBO_json)
# dd.start()