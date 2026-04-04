# import json
import time
# from pathlib import Path
# from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
from base_tool.number_get import number_get,parse_chinese_number
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
class yijitansuo():
    def __init__(self, AndroidDevice, NIBO_json):
        self.device = AndroidDevice
        self.NIBO_json = NIBO_json
        self.back = BackToMain(AndroidDevice)
        self.tansuonum=0
        self.numberget=number_get(AndroidDevice,NIBO_json)
    def entre_yiji(self):
        # 先回到主页
        self.back.back_to_main()
        # 进入七宗罪
        self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('尼伯龙根'))[0])
        self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('尼伯龙根遗迹探险'))[0])
    def start(self):
        self.entre_yiji()
        tansuo_loc=self.device.wait_for_image(self.NIBO_json.img_path('遗迹探索可探索'),timeout=30,mask_name='遗迹探索探索')
        print('探索',tansuo_loc)
        self.tansuonum=len(tansuo_loc)
        if self.tansuonum==0:
            return True
        if tansuo_loc==[0]:
            return True
        else:
            for loc in tansuo_loc:
                print(loc)
                loc=list(loc)
                loc[1] = loc[1] + 100
                self.device.tap_on_screen(loc)
                self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('遗迹探索派遣伙伴'))[0])
                self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('派遣伙伴后的一件派遣'))[0])
                self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('一件派遣后的攻击小队'))[0])
                self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('遗迹探索小队出发'))[0])
                self.tansuonum=self.tansuonum-1

                time.sleep(2)
            return True
    def tiaozhan(self):
        self.entre_yiji()
        tiaozhan_loc = self.device.wait_for_image(self.NIBO_json.img_path('遗迹探索可挑战'), mask_name='尼伯龙根遗迹探索可探索',timeout=30)
        if tiaozhan_loc==[0]:
            return True
        for loc in tiaozhan_loc:
            loc=list(loc)
            loc[1]=loc[1]-100
            self.device.tap_on_screen(loc)
            self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('遗迹探索挑战'))[0])
            self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('跳过战斗'), mask_name='跳过战斗')[0])
            time.sleep(2)
            self.device.tap_on_screen(self.device.wait_for_image(self.NIBO_json.img_path('点击空白处关闭'))[0])
            time.sleep(2)
        return True
# yj=yijitansuo(device,NIBO_json)
#
# # yj.start()
# yj.start()







