import time
# from pathlib import Path
# from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
from base_tool.find_loc import get_mul_matches
from base_tool.number_get import number_get,parse_chinese_number
class yijitansuo():
    def __init__(self, AndroidDevice, NIBO_json):
        self.device = AndroidDevice
        self.NIBO_json = NIBO_json
        self.back = BackToMain(AndroidDevice)
        self.tansuonum=0
        self.numberget=number_get(AndroidDevice,NIBO_json)
        self.get_mul_matches = get_mul_matches(AndroidDevice, NIBO_json)
    def entre_yiji(self):
        # 先回到主页
        self.back.back_to_main()
        # 进入七宗罪
        self.get_mul_matches.get_and_clik(target_names=['尼伯龙根'], thresholds=[0.8],time_out=5)
        if self.get_mul_matches.get_and_clik(target_names=['尼伯龙根遗迹探险','尼伯龙根遗迹探险2'], thresholds=[0.8], time_out=5):
            print('开始执行遗迹探险')
        else:
            print('遗迹探险进入失败')
            return True

    def start(self):
        if self.entre_yiji()==True:
            return True
        if self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('遗迹小助手位置'))[0]):
            time.sleep(2)
            self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('遗迹小助手一键执行'))[0])
            time.sleep(2)
        else:
            tansuo_loc = self.device.wait_for_image(self.NIBO_json.img_path('遗迹探索可探索'), timeout=30,
                                                    mask_name='遗迹探索探索')
            print('探索', tansuo_loc)
            self.tansuonum = len(tansuo_loc)
            if self.tansuonum == 0:
                return True
            if tansuo_loc == [0]:
                print('无需探索')
            else:
                for loc in tansuo_loc:
                    print(loc)
                    loc = list(loc)
                    loc[1] = loc[1] + 100
                    self.device.tap_on_screen(loc)
                    self.device.tap_on_screen(
                        self.device.wait_for_image(self.NIBO_json.img_path('遗迹探索派遣伙伴'))[0])
                    self.device.tap_on_screen(
                        self.device.wait_for_image(self.NIBO_json.img_path('派遣伙伴后的一件派遣'))[0])
                    self.device.tap_on_screen(
                        self.device.wait_for_image(self.NIBO_json.img_path('一件派遣后的攻击小队'))[0])
                    self.device.tap_on_screen(
                        self.device.wait_for_image(self.NIBO_json.img_path('遗迹探索小队出发'))[0])
                    self.tansuonum = self.tansuonum - 1

                    time.sleep(2)
                print('等待20分钟探索完成后挑战')
                time.sleep(1200)
            tiaozhan_loc = self.device.wait_for_image(self.NIBO_json.img_path('遗迹探索可挑战'),
                                                      mask_name='尼伯龙根遗迹探索可探索', timeout=30)
            if tiaozhan_loc == [0]:
                return True
            for loc in tiaozhan_loc:
                loc = list(loc)
                loc[1] = loc[1] - 100
                self.device.tap_on_screen(loc)
                self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('遗迹探索挑战'))[0])
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.NIBO_json.img_path('跳过战斗'), mask_name='跳过战斗',threshold=0.7)[0])
                time.sleep(2)
                self.device.tap_on_screen(self.device.get_centra(self.NIBO_json.img_areas('点击空白处关闭')[0],
                                                   self.NIBO_json.img_areas('点击空白处关闭')[1]))
                time.sleep(2)
                self.device.tap_on_screen(self.device.get_centra(self.NIBO_json.img_areas('点击空白处关闭')[0],
                                                                 self.NIBO_json.img_areas('点击空白处关闭')[1]))
                time.sleep(2)
                self.device.tap_on_screen(self.device.get_centra(self.NIBO_json.img_areas('点击空白处关闭')[0],
                                                                 self.NIBO_json.img_areas('点击空白处关闭')[1]))
                time.sleep(2)
            return True


