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

# 获取当前脚本文件的绝对路径
# script_dir = find_project_root()
# # 定义 seven.json 的绝对路径
# jingji_file = script_dir / 'base_tool' / 'location' / 'jingjichang' / 'jingjichang.json'
# img_file = script_dir / 'base_tool'  # 定义好图片的根目录
# print(img_file)
# # 检查文件是否存在
# if not jingji_file.exists():
#     print(f"信息文件不存在: {jingji_file}")
#     # 根据需要，可以选择创建文件或通过GUI应用程序生成
#     exit()
# jingji_json = json_reader(jingji_file)
# device = AndroidDevice()
# device.img_path_abs = img_file
# device.connect_device()
class xueyuanfengyun():
    def __init__(self, AndroidDevice, json_reader):
        self.device = AndroidDevice
        self.jingji_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.numberget = number_get(AndroidDevice, json_reader)
        self.res_num=10

    def enter_paiwei(self):
        # 先回到主页

        self.back.back_to_main()
        # 进入七宗罪
        self.device.tap_on_screen(self.device.wait_for_image(self.jingji_json.img_path('竞技训练入口'))[0])
        time.sleep(1)
        self.device.tap_on_screen(self.device.wait_for_image(self.jingji_json.img_path('学院风云入口'))[0])
        if self.device.wait_for_image(self.jingji_json.img_path('锦标赛内新任管理弹窗')) !=[0]:
            self.back.back()


    def start(self):
        self.enter_paiwei()
        if self.device.tap_on_screen(self.device.wait_for_image(self.jingji_json.img_path('会长竞选'))[0]):
            zan_loc=self.device.wait_for_image(self.jingji_json.img_path('会长竞选点赞图标'))

            for i in zan_loc:
                self.device.tap_on_screen(i)
            self.back.back()
        if self.device.tap_on_screen(self.device.wait_for_image(self.jingji_json.img_path('会长竞猜'))[0]):
            time.sleep(2)
            self.device.tap_on_screen(
                self.device.get_centra(self.jingji_json.img_areas('竞猜第一名按钮所在位置')[0],
                                       self.jingji_json.img_areas('竞猜第一名按钮所在位置')[1]))
            time.sleep(2)
            self.back.back()
        time.sleep(2)
        self.device.tap_on_screen(
            self.device.get_centra(self.jingji_json.img_areas('学院风云排位赛入口')[0],
                                   self.jingji_json.img_areas('学院风云排位赛入口')[1]))

        while True:
            if self.res_num==0:
                self.device.tap_on_screen(
                    self.device.get_centra(self.jingji_json.img_areas('点击空白处关闭')[0],
                                           self.jingji_json.img_areas('点击空白处关闭')[1]))
                time.sleep(2)
                break
            else:
                time.sleep(3)
                if self.device.tap_on_screen(self.device.wait_for_image(self.jingji_json.img_path('开始匹配'),threshold=0.85,timeout=10)[0]):

                    self.device.tap_on_screen(self.device.wait_for_image(self.jingji_json.img_path('跳过战斗'), mask_name='跳过战斗',threshold=0.65, timeout=20)[0])
                    if self.device.wait_for_image(self.jingji_json.img_path('刷龙胜利'))[0] != 0:
                        self.device.tap_on_screen(
                            self.device.get_centra(self.jingji_json.img_areas('点击空白处关闭')[0],
                                                   self.jingji_json.img_areas('点击空白处关闭')[1]))
                        time.sleep(2)
                        self.device.tap_on_screen(
                            self.device.get_centra(self.jingji_json.img_areas('点击空白处关闭')[0],
                                                   self.jingji_json.img_areas('点击空白处关闭')[1]))
                        time.sleep(4)
                        self.res_num-=1
                else:
                    print('赛季结束')
                    return True


        self.device.tap_on_screen(
            self.device.wait_for_image(self.jingji_json.img_path('学院风云排位赛奖励'))[0])
        self.device.tap_on_screen(
            self.device.wait_for_image(self.jingji_json.img_path('排位赛总积分奖励'))[0])
        self.device.tap_on_screen(
            self.device.wait_for_image(self.jingji_json.img_path('排位赛每日奖励'))[0])
        if self.device.tap_on_screen(
            self.device.wait_for_image(self.jingji_json.img_path('排位赛奖励领取按钮'))[0]):
            self.device.tap_on_screen(
                self.device.get_centra(self.jingji_json.img_areas('点击空白处关闭')[0],
                                       self.jingji_json.img_areas('点击空白处关闭')[1]))
            time.sleep(2)
            self.device.tap_on_screen(
                self.device.get_centra(self.jingji_json.img_areas('点击空白处关闭')[0],
                                       self.jingji_json.img_areas('点击空白处关闭')[1]))

        time.sleep(3)
        self.device.tap_on_screen(
            self.device.wait_for_image(self.jingji_json.img_path('排位赛段位奖励'),timeout=5,threshold=0.98)[0])
        time.sleep(1)
        self.device.tap_on_screen(
            self.device.wait_for_image(self.jingji_json.img_path('排位赛奖励领取按钮'))[0])
        return True
# dd=xueyuanfengyun(device,jingji_json)
# dd.start()