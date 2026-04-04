# import json
import time
# from pathlib import Path
# from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
from base_tool.number_get import number_get,parse_chinese_number
from base_tool.get_matches import get_matches, get_wait_matches, ResultProcessor
from base_tool.find_loc import get_mul_matches
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
class lunhuishilang():
    def __init__(self, AndroidDevice, NIBO_json):
        self.device = AndroidDevice
        self.NIBO_json = NIBO_json
        self.back = BackToMain(AndroidDevice)
        self.cur_floor=0
        self.fresh_cost=0
        self.numberget=number_get(AndroidDevice,NIBO_json)
        self.get_mul_matches=get_mul_matches(AndroidDevice,NIBO_json)
    def entra_lunhui(self):
        # 先回到主页
        self.back.back_to_main()
        # 进入七宗罪
        self.get_mul_matches.get_and_clik(target_names=['尼伯龙根'], thresholds=[0.8],
                                          time_out=5)

        if self.get_mul_matches.get_and_clik(target_names=['轮回石廊','轮回石廊2'], thresholds=[0.8],time_out=5):
            print('开始执行轮回任务')
        else:
            print('轮回任务进入失败')
            return True
        time.sleep(4)
        # # text=device.get_text_from_screen(NIBO_json.img_areas('轮回石廊当前层数文字区域')[0],NIBO_json.img_areas('轮回石廊当前层数文字区域')[1])
        try:self.cur_floor = int(self.numberget.extract_numbers('轮回石廊当前层数文字区域', excluded_number=1)[0])
        except:self.cur_floor = int(self.numberget.extract_numbers('轮回走廊文字区域2', excluded_number=1)[0])
        # # print(self.cur_floor)轮回走廊文字区域2
        self.get_mul_matches.get_and_clik(target_names=['轮回石廊快速探索', '轮回石廊快速探索2'],thresholds=[0.7],time_out=5)



        if self.device.wait_for_image(self.NIBO_json.img_path('轮回石廊快速探索出现区域'))!=[0]:
            self.fresh_cost = int(self.numberget.extract_numbers('轮回石廊快速探索钻石消耗区域', excluded_number=-9,
                                                                 mask_name='轮回石廊快速探索mask', kernel_size=1)[0])
        self.back.back()
        # print(self.fresh_cost)


        # print(self.cur_floor)
    def start(self):
        if self.entra_lunhui()==True:
            return True


        self.get_mul_matches.get_and_clik(target_names=['轮回石廊领取', '轮回石廊领取2'], thresholds=[0.7],
                                          time_out=5)

        time.sleep(2)
        self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('点击空白处关闭'))[0])
        if self.fresh_cost==0:
            self.get_mul_matches.get_and_clik(target_names=['轮回石廊快速探索', '轮回石廊快速探索2'],thresholds=[0.7],time_out=5)
            self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('轮回石廊快速探索确定'))[0])
            self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('点击空白处关闭'))[0])


        self.get_mul_matches.get_and_clik(target_names=['轮回石廊挑战', '轮回石廊挑战2', '轮回石廊挑战3','轮回石廊挑战4'],
                                          thresholds=[0.7],
                                          time_out=5)

        time.sleep(2)

        while True:


            self.get_mul_matches.get_and_clik(target_names=['轮回石廊挑战', '轮回石廊挑战2','轮回石廊挑战3','轮回石廊挑战4'], thresholds=[0.7],
                                              time_out=5)

            if self.cur_floor % 5 != 0:
                time.sleep(3)
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.NIBO_json.img_path('跳过战斗'), mask_name='跳过战斗',threshold=0.6,timeout=20)[0])
                if self.device.wait_for_image(self.NIBO_json.img_path('刷龙胜利'))[0] != 0:
                    time.sleep(1)

                    if  self.device.find_image_on_screen(self.NIBO_json.img_path('轮回走廊战斗失败标志（重试）'))!=[0]:
                        self.device.tap_on_screen(
                            self.device.wait_for_image(self.NIBO_json.img_path('轮回石廊返回'))[0])
                        print('打不过了')
                        time.sleep(4)
                        return True
                    else:
                        self.cur_floor = self.cur_floor + 1
                        self.device.tap_on_screen(
                            self.device.wait_for_image(self.NIBO_json.img_path('轮回石廊下一关'))[0])


            else:
                time.sleep(3)
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.NIBO_json.img_path('跳过战斗'), mask_name='跳过战斗',threshold=0.6,timeout=20)[0])
                if self.device.wait_for_image(self.NIBO_json.img_path('刷龙胜利'))[0] != 0:
                    time.sleep(1)
                    if  self.device.find_image_on_screen(self.NIBO_json.img_path('轮回走廊战斗失败标志（重试）'))!=[0]:
                        self.device.tap_on_screen(
                            self.device.wait_for_image(self.NIBO_json.img_path('轮回石廊返回'))[0])
                        print('打不过了')
                        time.sleep(5)
                        return True
                    else:
                        self.cur_floor = self.cur_floor + 1
                        self.device.tap_on_screen(
                            self.device.wait_for_image(self.NIBO_json.img_path('轮回石廊返回'))[0])
                        self.device.tap_on_screen(
                            self.device.wait_for_image(self.NIBO_json.img_path('点击空白处关闭'))[0])


                        self.get_mul_matches.get_and_clik(
                            target_names=['轮回石廊挑战', '轮回石廊挑战2', '轮回石廊挑战3','轮回石廊挑战4'], thresholds=[0.7],
                            time_out=5)
                        time.sleep(2)



# dd=lunhuishilang(device,NIBO_json)
# dd.entra_lunhui()
# dd.start()