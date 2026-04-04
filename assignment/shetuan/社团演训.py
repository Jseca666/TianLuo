# import json
import time
# from pathlib import Path
import re
# from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
from base_tool.number_get import number_get, parse_chinese_number
# from base_tool.ocr_unit import Uocr
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


class yanxun():
    def __init__(self, AndroidDevice, json_reader):
        self.device = AndroidDevice
        self.shetuan_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.res_num=5
        self.zen_num=0
        self.numberget = number_get(AndroidDevice, json_reader)
    def enter_weituo(self):
        # 先回到主页
        self.back.back_to_main()
        # 进入七宗罪
        self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团入口'))[0])
        if self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团演训入口'))[0]):
            print('进入社团演训')
        else:
            print('进入演训失败')
            return True
        try:
            time.sleep(4)
            self.res_num = int(
                self.numberget.extract_numbers('挑战剩余次数剩余区域', excluded_number=-1, mask_name='社团烟熏次数')[0])
            self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团烟熏赠送入口'))[0])
            time.sleep(4)
            self.zen_num = int(self.numberget.extract_numbers('社团烟熏赠送次数区域查询', excluded_number=-1)[0])
            self.back.back()
        except:
            return True
    def baoxiang(self):
        if self.enter_weituo()==True:
            return True
        self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('宝箱'))[0])
        guangloc=self.device.wait_for_image(self.shetuan_json.img_path('小光点'),mask_name='小光点',threshold=0.8)
        if guangloc!=[0]:
            for i in  guangloc:
                self.device.tap_on_screen(i)
                while True:
                    if self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('章节里面的宝箱'))[0]):
                        break
                    else:
                        self.device.swipe_on_screen(self.shetuan_json.img_areas('宝箱滑动区域')[1],self.shetuan_json.img_areas('宝箱滑动区域')[0],duration=500)
                        time.sleep(2)
            return True

    def start(self):
        # self.baoxiang()
        if self.enter_weituo() == True:
            return True
        shibie=self.device.get_text_from_screen([0,0],[1280,720],mask_name='社团烟熏文字',flag=0)
        target=[]
        aims=[]
        for s in shibie[0]:
            if '压制值' in s[1][0]:
                aims.append([s[0][0],s[0][2],s[1][0]])
        print(aims)
        for i in aims:
            numbers = re.findall(r'\d+', i[2])
            numbers_list = [int(num) for num in numbers]
            if numbers_list[0] !=0:
                i[0][0]=i[0][0]-50
                target.append([i[0],i[1]])
        print('ta=',target)
        target=[self.device.get_centra(target[0][0],target[0][1])]
        if self.zen_num!=0:
            self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团烟熏赠送入口'))[0])
            while self.zen_num:
                if self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('赠送按钮'))[0]):
                    self.zen_num=self.zen_num-1
                if self.zen_num==0:
                    break

            self.back.back()

        if target!=[0] and self.res_num !=0:

            time.sleep(2)
            self.device.tap_on_screen(target[0])
            emeng = self.device.wait_for_image(self.shetuan_json.img_path('噩梦难度'),timeout=5)
            kunnan = self.device.wait_for_image(self.shetuan_json.img_path('困难难度'),timeout=5)
            jiandan=self.device.wait_for_image(self.shetuan_json.img_path('普通难度'),timeout=5)
            nandu_lis=emeng+kunnan+jiandan

            for i in nandu_lis:
                while True:
                    if self.res_num == 0:

                        return True
                    time.sleep(1)
                    self.device.tap_on_screen(i)

                    self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('挑战按钮'))[0])
                    if self.device.wait_for_image(self.shetuan_json.img_path('点击空白处关闭'),timeout=5) != [0]:
                        self.device.tap_on_screen(
                            self.device.get_centra(self.shetuan_json.img_areas('点击空白处关闭')[0],
                                                   self.shetuan_json.img_areas('点击空白处关闭')[1]))
                    else:
                        if self.device.wait_for_image(self.shetuan_json.img_path('社团烟熏难度通过后的弹窗'),timeout=5) != [0]:
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.shetuan_json.img_path('猛鬼入侵挑战确认'))[0])
                            while True:
                                self.device.tap_on_screen(
                                    self.device.wait_for_image(self.shetuan_json.img_path('挑战按钮'))[0])
                                time.sleep(1.5)
                                self.device.tap_on_screen(
                                    self.device.get_centra(self.shetuan_json.img_areas('点击空白处关闭')[0],
                                                           self.shetuan_json.img_areas('点击空白处关闭')[1]))
                                self.res_num = self.res_num - 1
                                if self.res_num == 0:

                                    return True
                        while True:
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.shetuan_json.img_path('跳过战斗'), mask_name='跳过战斗',
                                                           threshold=0.65, timeout=20)[0])
                            if self.device.wait_for_image(self.shetuan_json.img_path('刷龙胜利'))[0] != 0:
                                break
                        if self.device.wait_for_image(self.shetuan_json.img_path('社团烟熏失败标志'),
                                                      timeout=2) != [0]:
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.shetuan_json.img_path('社团烟熏失败标志'),
                                                           timeout=2)[0])
                            time.sleep(1)

                            break

                        else:
                            time.sleep(1)
                            self.device.tap_on_screen(
                                self.device.get_centra(self.shetuan_json.img_areas('点击空白处关闭')[0],
                                                       self.shetuan_json.img_areas('点击空白处关闭')[1]))
                            time.sleep(1)
                            self.device.tap_on_screen(
                                self.device.get_centra(self.shetuan_json.img_areas('点击空白处关闭')[0],
                                                       self.shetuan_json.img_areas('点击空白处关闭')[1]))
                            self.res_num = self.res_num - 1







        else:
            print('执行失败')
            return False
# dd=yanxun(device,shetuan_json)
# dd.start()