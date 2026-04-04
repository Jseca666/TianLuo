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
# zhuxian_file = script_dir / 'base_tool' / 'location' / 'zhuxian' / 'zhuxian.json'
# img_file = script_dir / 'base_tool'  # 定义好图片的根目录
# print(img_file)
# # 检查文件是否存在
# if not zhuxian_file.exists():
#     print(f"信息文件不存在: {zhuxian_file}")
#     # 根据需要，可以选择创建文件或通过GUI应用程序生成
#     exit()
# zhuxian_json = json_reader(zhuxian_file)
# device = AndroidDevice()
# device.img_path_abs = img_file
# device.connect_device()


class yanlian():
    def __init__(self, AndroidDevice, json_reader,yanlian_flag=None):
        self.device = AndroidDevice
        self.zhuxian_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.res_num = 0
        self.yanlian_flag=yanlian_flag
        self.numberget=number_get(self.device,self.zhuxian_json)

    def enter_yanlian(self):
        # 先回到主页
        self.back.back_to_main()
        # 进入七宗罪
        self.device.tap_on_screen(self.device.wait_for_image(self.zhuxian_json.img_path('主页主线剧情入口'))[0])
        if self.device.tap_on_screen(self.device.wait_for_image(self.zhuxian_json.img_path('战术演练入口'))[0]):
            print('战术演练开始')
        else:
            print('战术演练进入失败')
            return True
        time.sleep(3.5)
        self.res_num = int(self.numberget.extract_numbers('演练额外奖励剩余次数', excluded_number=-1)[0])
    def start(self):
        if self.enter_yanlian()==True:
            return True
        yan_loc_name = ['金币关','经验关','元件关']
        if self.yanlian_flag==None:
            return True

        else:
            if self.res_num == 0:
                print('演练完成')
                return True
            for i in range(len(self.yanlian_flag)):
                while True:
                    if self.yanlian_flag[i] != 0:
                        self.device.tap_on_screen(self.device.wait_for_image(self.zhuxian_json.img_path(yan_loc_name[i]))[0])
                        self.device.tap_on_screen(
                            self.device.wait_for_image(self.zhuxian_json.img_path('尝试挑战'))[0])
                        if self.device.wait_for_image(self.zhuxian_json.img_path('体力不足的弹窗'), timeout=2) != [0]:
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.zhuxian_json.img_path('使用体力的按钮'))[0])
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.zhuxian_json.img_path('使用确认的按钮'))[0])

                        self.device.tap_on_screen(
                            self.device.wait_for_image(self.zhuxian_json.img_path('跳过战斗'), mask_name='跳过战斗',timeout=20,threshold=0.6)[0])
                        if self.device.wait_for_image(self.zhuxian_json.img_path('刷龙胜利'))[0] != 0:
                            time.sleep(1)
                            if self.device.wait_for_image(self.zhuxian_json.img_path('轮回走廊战斗失败标志'),
                                                          timeout=2) != [
                                0]:
                                self.device.tap_on_screen(
                                    self.device.get_centra(self.zhuxian_json.img_areas('点击空白处关闭')[0],
                                                           self.zhuxian_json.img_areas('点击空白处关闭')[1]))
                                print('打不过了,扫荡')
                                time.sleep(1)
                                self.device.tap_on_screen(
                                    self.device.wait_for_image(self.zhuxian_json.img_path('挑战不过扫荡'))[-1])
                                time.sleep(1)
                                if self.device.tap_on_screen(
                                    self.device.wait_for_image(self.zhuxian_json.img_path('扫荡完成确认'))[0]) :
                                    self.res_num-=1
                                    self.yanlian_flag[i] = self.yanlian_flag[i] - 1

                            else:
                                self.device.tap_on_screen(
                                    self.device.get_centra(self.zhuxian_json.img_areas('点击空白处关闭')[0],
                                                           self.zhuxian_json.img_areas('点击空白处关闭')[1]))

                    if self.res_num == 0:
                        return True
                    if  self.yanlian_flag[i]==0:
                        self.back.back()
                        break
  



# dd=yanlian(device,zhuxian_json,[0,0,6])
#
#
# dd.start()