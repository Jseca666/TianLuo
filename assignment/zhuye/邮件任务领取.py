# import json
import time
import random
from paddle.distributed.transpiler.distribute_transpiler import PRINT_LOG

# from pathlib import Path
# from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
from base_tool.number_get import number_get, parse_chinese_number
from base_tool.get_matches import get_matches, get_wait_matches, ResultProcessor
# from base_tool.projection_root import find_project_root
from base_tool.link_head import calculate_distance, merge_close_matches

# # 获取当前脚本文件的绝对路径
# script_dir = find_project_root()
# print(script_dir)
# # 定义 seven.json 的绝对路径
# zhuye_file = script_dir /'base_tool' /'location' / 'zhuye' / 'zhuye.json'
# img_file=script_dir /'base_tool'#定义好图片的根目录
# print(img_file)
# # 检查文件是否存在
# if not zhuye_file.exists():
#     print(f"信息文件不存在: {zhuye_file}")
#     # 根据需要，可以选择创建文件或通过GUI应用程序生成
#     exit()
# zhuye_json=json_reader(zhuye_file)
# device=AndroidDevice()
# device.img_path_abs=img_file
# device.connect_device()
class youxiang_renwu():
    def __init__(self, AndroidDevice, json_reader,stop_event=None):
        self.device = AndroidDevice
        self.zhuye_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.number_get = number_get(AndroidDevice=self.device, json_reader=self.zhuye_json)
        self.zuanshi=0
        self.stop_event = stop_event
    def enter(self):
        self.back.back_to_main()
    def youxiang(self):
        self.enter()
        self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('邮箱所在位置')[0],
                                       self.zhuye_json.img_areas('邮箱所在位置')[1]))
        if self.device.tap_on_screen(self.device.wait_for_image(self.zhuye_json.img_path('一键领取'), threshold=0.95)[0]):
            self.device.tap_on_screen(self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'))[0])
    def renwu(self):
        self.enter()
        self.device.tap_on_screen(
            self.device.wait_for_image(self.zhuye_json.img_path('主页任务'), threshold=0.97)[0])
        self.device.tap_on_screen(
            self.device.wait_for_image(self.zhuye_json.img_path('任务里面的领取'), threshold=0.97)[0])
        time.sleep(2)
        self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('点击空白处关闭')[0],
                                                         self.zhuye_json.img_areas('点击空白处关闭')[1]))
        target_names = ['小光点图片']
        zhou_huo, parm_list = get_wait_matches(beijingjson=self.zhuye_json, targetjson=self.zhuye_json,
                                                 device=self.device,
                                                 target_names=target_names,
                                                beijing_name='本周学分所在区域',
                                               maskname=['小光点'], stop_on_first_match=False,
                                                 thresholds=[0.65],time_out=10)

        if zhou_huo!=[0]:
            for i in zhou_huo:
                self.device.tap_on_screen(i)

                time.sleep(2)
                self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('点击空白处关闭')[0],
                                                                 self.zhuye_json.img_areas('点击空白处关闭')[1]))
        self.device.tap_on_screen(
            self.device.wait_for_image(self.zhuye_json.img_path('学分等级'), threshold=0.97)[0])
        time.sleep(2)
        zhou_huo, parm_list = get_wait_matches(beijingjson=self.zhuye_json, targetjson=self.zhuye_json,
                                               device=self.device,
                                               target_names=target_names,
                                               beijing_name='学分等级领取奖励区域',
                                               maskname=['小光点'], stop_on_first_match=False,
                                               thresholds=[0.6], time_out=10)
        if zhou_huo!=[0]:
            for i in zhou_huo:
                self.device.tap_on_screen(i)
                time.sleep(2)
                self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('点击空白处关闭')[0],
                                                                 self.zhuye_json.img_areas('点击空白处关闭')[1]))
    def shangdian(self):
        self.enter()
        self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('主页商店所在区域')[0],
                                                         self.zhuye_json.img_areas('主页商店所在区域')[1]))
        if self.device.tap_on_screen(self.device.wait_for_image(self.zhuye_json.img_path('买免费的体力'), threshold=0.97, timeout=6)[0]):
            self.device.tap_on_screen(
                self.device.wait_for_image(self.zhuye_json.img_path('购买'), timeout=6)[0])
            self.device.tap_on_screen(
                self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'), timeout=6)[0])
    def dianzan(self):
        self.enter()
        self.device.tap_on_screen(
            self.device.wait_for_image(self.zhuye_json.img_path('进入零钻石'), threshold=0.65, timeout=30)[0])
        while True:
            if self.device.tap_on_screen(
            self.device.wait_for_image(self.zhuye_json.img_path('领取悬赏任务奖励'), threshold=0.7, timeout=10)[0]):
                time.sleep(2)
                self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('点击空白处关闭')[0],
                                                                 self.zhuye_json.img_areas('点击空白处关闭')[1]))
                time.sleep(2)
                continue
            else:break
        time.sleep(2)
        self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('学员风采')[0],
                                                         self.zhuye_json.img_areas('学员风采')[1]))
        time.sleep(2)

        loc=self.device.wait_for_image(self.zhuye_json.img_path('点赞'), threshold=0.90, timeout=3)
        if loc!=[0]:
            for i in loc:
                self.device.tap_on_screen(i)
    def zhuhe(self):
        self.enter()
        self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('好友位置')[0],
                                                         self.zhuye_json.img_areas('好友位置')[1]))
        self.device.tap_on_screen(
            self.device.wait_for_image(self.zhuye_json.img_path('祝贺'), threshold=0.97, timeout=6)[0])
        self.device.tap_on_screen(
            self.device.wait_for_image(self.zhuye_json.img_path('一键祝贺'), threshold=0.97, timeout=6)[0])
    def zhaomu(self):
        self.enter()
        self.device.tap_on_screen(
            self.device.wait_for_image(self.zhuye_json.img_path('招募位置'), threshold=0.8,timeout=10)[0])
        if self.device.tap_on_screen(self.device.wait_for_image(self.zhuye_json.img_path('免费伙伴招募'), threshold=0.96, timeout=20)[0]):
            time.sleep(3)
            self.device.swipe_on_screen(self.zhuye_json.img_areas('伙伴招募的华东位置')[1],
                                        self.zhuye_json.img_areas('伙伴招募的华东位置')[0], duration=800)
            time.sleep(2)
            self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('点击空白处关闭')[0],
                                                             self.zhuye_json.img_areas('点击空白处关闭')[1]))
            self.device.tap_on_screen(
                self.device.wait_for_image(self.zhuye_json.img_path('跳过'), mask_name='同游跳过白色')[0])
            time.sleep(4)
            self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('点击空白处关闭')[0],
                                                             self.zhuye_json.img_areas('点击空白处关闭')[1]))
            time.sleep(4)
            self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('点击空白处关闭')[0],
                                                             self.zhuye_json.img_areas('点击空白处关闭')[1]))
            time.sleep(4)
            self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('点击空白处关闭')[0],
                                                             self.zhuye_json.img_areas('点击空白处关闭')[1]))
            time.sleep(4)
            self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('充值关闭位置')[0],
                                                             self.zhuye_json.img_areas('充值关闭位置')[1]))

        time.sleep(2)
        self.device.tap_on_screen(
            self.device.wait_for_image(self.zhuye_json.img_path('战术补给'), threshold=0.97, timeout=3)[0])
        if self.device.tap_on_screen(self.device.wait_for_image(self.zhuye_json.img_path('免费战术补给'), threshold=0.96, timeout=20)[0]):
            time.sleep(3)
            self.device.swipe_on_screen(self.zhuye_json.img_areas('战术补给华东位置')[1],
                                        self.zhuye_json.img_areas('战术补给华东位置')[0], duration=800)
            time.sleep(3)
            self.device.tap_on_screen(
                self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'),timeout=6)[0])
            time.sleep(3)
            self.device.tap_on_screen(
                self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'), timeout=6)[0])
            time.sleep(4)
            self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('充值关闭位置')[0],
                                                             self.zhuye_json.img_areas('充值关闭位置')[1]))
        time.sleep(2)
        self.device.tap_on_screen(
            self.device.wait_for_image(self.zhuye_json.img_path('命轮祈愿'), threshold=0.97, timeout=3)[0])
        if self.device.tap_on_screen(
                self.device.wait_for_image(self.zhuye_json.img_path('免费祈愿'), threshold=0.96, timeout=20)[0]):
            time.sleep(3)
            self.device.swipe_on_screen(self.zhuye_json.img_areas('战术补给华东位置')[1],
                                        self.zhuye_json.img_areas('战术补给华东位置')[0], duration=800)
            time.sleep(3)
            self.device.tap_on_screen(
                self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'), timeout=6)[0])
            time.sleep(3)
            self.device.tap_on_screen(
                self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'), timeout=6)[0])
            time.sleep(4)
            self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('充值关闭位置')[0],
                                                             self.zhuye_json.img_areas('充值关闭位置')[1]))

    def pingji(self):
        self.enter()
        self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('评级区域')[0],
                                                         self.zhuye_json.img_areas('评级区域')[1]))
        if self.device.tap_on_screen(self.device.wait_for_image(self.zhuye_json.img_path('评级提升'),threshold=0.98)[0]):
            while True:
                if self.device.wait_for_image(self.zhuye_json.img_path('红色感叹号'), mask_name='红色感叹号',
                                              threshold=0.8,timeout=3) != [0]:
                    self.device.tap_on_screen(self.device.wait_for_image(self.zhuye_json.img_path('评级晋升'))[0])
                    time.sleep(2)
                    self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('评级区域')[0],
                                                                     self.zhuye_json.img_areas('评级区域')[1]))
                else:
                    return True
        # self.device.tap_on_screen(self.device.wait_for_image(self.zhuye_json.img_path('评级晋升'))[0])
        # time.sleep(2)
        # num_list = self.number_get.extract_numbers('评级证书数量获取区域', excluded_number=-1,mask_name='评级橙色文字')
        # que_num=int(num_list[0])-int(num_list[1])
        # self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('评级之证书获取区域')[0],
        #                                                  self.zhuye_json.img_areas('评级之证书获取区域')[1]))
        # self.device.tap_on_screen(self.device.wait_for_image(self.zhuye_json.img_path('证书获取前往'))[0])
        # time.sleep(2)
    # def lianjinyanxishe(self):
    #     self.enter()
    #     self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('评级区域')[0],
    #                                                      self.zhuye_json.img_areas('评级区域')[1]))
    #     if self.device.tap_on_screen(
    #         self.device.wait_for_image(self.zhuye_json.img_path('炼金研习社'), threshold=0.98)[0]):
    #         self.device.tap_on_screen(
    #             self.device.wait_for_image(self.zhuye_json.img_path('炼金研习社'), threshold=0.98)[0])

    def mianfeichongzhi(self):
        self.enter()

        self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('主页充值入口')[0],
                                                         self.zhuye_json.img_areas('主页充值入口')[1]))
        time.sleep(2)


        while True:

            target_names = ['小光点图片','小光点2','小光点3','小光点4',
                            '小光点5','小光点6','小光点7','小光点8'
                            ,'小光点9','小光点10','小光点11'
                            , '小光点12', '小光点13','小光点14','小光点15']
            chongzuo, parm_list = get_wait_matches(beijingjson=self.zhuye_json, targetjson=self.zhuye_json,
                                                   device=self.device,
                                                   target_names=target_names,
                                                   beijing_name='充值左区域',
                                                   maskname=['小光点new'], stop_on_first_match=False,
                                                   thresholds=[0.9], time_out=5)

            print(chongzuo)
            if chongzuo!=[0]:
                chongzuo = merge_close_matches(chongzuo, distance_threshold=20)
                for i in chongzuo:

                    self.device.tap_on_screen(i)
                    target_names = ['小光点图片', '小光点2', '小光点3', '小光点4',
                                    '小光点5', '小光点6', '小光点7', '小光点8', '小光点9', '小光点10'
                        , '小光点11', '小光点12', '小光点13', '小光点14', '小光点15']
                    time.sleep(2)
                    chongyou2, parm_list = get_wait_matches(beijingjson=self.zhuye_json, targetjson=self.zhuye_json,
                                                            device=self.device,
                                                            target_names=target_names,
                                                            beijing_name='充值右区域',
                                                            maskname=['小光点new'], stop_on_first_match=False,
                                                            thresholds=[0.85], time_out=5)
                    if chongyou2 != [0]:
                        chongyou2 = merge_close_matches(chongyou2, distance_threshold=20)
                        random.shuffle(chongyou2)
                    else:
                        if self.device.tap_on_screen(
                                self.device.wait_for_image(self.zhuye_json.img_path('充值领取'), threshold=0.97,
                                                           timeout=4)[
                                    0]):
                            time.sleep(2)
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'),
                                                           timeout=6)[0])
                        continue

                    if self.device.tap_on_screen(
                            self.device.wait_for_image(self.zhuye_json.img_path('充值领取'), threshold=0.97, timeout=4)[
                                0]):
                        time.sleep(2)
                        self.device.tap_on_screen(
                            self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'),
                                                       timeout=6)[0])
                        time.sleep(2)

                    guoqu_you = []
                    pr_len = len(guoqu_you)
                    if chongyou2 != [0]:
                        chongyou2 = merge_close_matches(chongyou2, distance_threshold=20)
                    else:
                        if self.device.tap_on_screen(
                                self.device.wait_for_image(self.zhuye_json.img_path('充值领取'), threshold=0.92,
                                                           timeout=4)[
                                    0]):
                            time.sleep(2)
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'),
                                                           timeout=6)[0])
                            time.sleep(2)
                        continue

                    if self.device.tap_on_screen(
                            self.device.wait_for_image(self.zhuye_json.img_path('充值领取'), threshold=0.92,
                                                       timeout=4)[
                                0]):
                        time.sleep(2)
                        self.device.tap_on_screen(
                            self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'),
                                                       timeout=6)[0])
                        time.sleep(2)

                    guoqu_you = []
                    pr_len = len(guoqu_you)
                    for j in chongyou2:
                        if j not in guoqu_you:
                            guoqu_you.append(j)
                            self.device.tap_on_screen(j)
                            time.sleep(2)
                            if self.device.tap_on_screen(
                                    self.device.wait_for_image(self.zhuye_json.img_path('充值领取'),
                                                               threshold=0.97, timeout=4)[
                                        0]):
                                time.sleep(2)
                                self.device.tap_on_screen(
                                    self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'),
                                                               timeout=6)[0])
                                self.back.back()
                                time.sleep(2)

                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'),
                                                           timeout=6)[0])

                    cr_len = len(guoqu_you)
                    print('1')
                    if pr_len == cr_len:
                        continue



            else:
                print('不存在小光点')
                return True
            # cur_len = len(guoqu)
            # if cur_len==prelen:
            #     return True
    def zengli(self):
        self.enter()
        self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('主页赠礼位置')[0],
                                                         self.zhuye_json.img_areas('主页赠礼位置')[1]))
        time.sleep(2)
        guoqu = []

        while True:
            prelen = len(guoqu)
            target_names = ['小光点图片', '小光点2', '小光点3', '小光点4',
                            '小光点5', '小光点6', '小光点7', '小光点8'
                , '小光点9', '小光点10','小光点11'
                            , '小光点12', '小光点13','小光点14','小光点15','小光点16']
            print('查找左边区域')
            zuodian, parm_list = get_wait_matches(beijingjson=self.zhuye_json, targetjson=self.zhuye_json,
                                                   device=self.device,
                                                   target_names=target_names,
                                                   beijing_name='赠礼左区域',
                                                   maskname=['小光点new'], stop_on_first_match=False,
                                                   thresholds=[0.9], time_out=5)

            print(zuodian)
            if zuodian != [0]:
                zuodian = merge_close_matches(zuodian, distance_threshold=20)
                for i in zuodian:

                    guoqu.append(i)
                    self.device.tap_on_screen(i)
                    target_names = ['小光点图片', '小光点2', '小光点3', '小光点4',
                                    '小光点5', '小光点6', '小光点7', '小光点8',
                                    '小光点9', '小光点10', '小光点11', '小光点12', '小光点13', '小光点14', '小光点15','小光点16']
                    time.sleep(2)
                    print('查找右边区域')
                    youdian, parm_list = get_wait_matches(beijingjson=self.zhuye_json, targetjson=self.zhuye_json,
                                                          device=self.device,
                                                          target_names=target_names,
                                                          beijing_name='赠礼右区域',
                                                          maskname=['小光点new'], stop_on_first_match=False,
                                                          thresholds=[0.85], time_out=5)
                    if youdian != [0]:
                        youdian = merge_close_matches(youdian, distance_threshold=20)
                        random.shuffle(youdian)
                        lingqu_names = ['赠礼资源找回领取', '新手任务的领取', '新手任务领取2']
                        time.sleep(2)
                        lingqudian, parm_list = get_wait_matches(beijingjson=self.zhuye_json,
                                                                 targetjson=self.zhuye_json,
                                                                 device=self.device,
                                                                 target_names=lingqu_names,
                                                                 beijing_name='赠礼右区域',
                                                                 maskname=None, stop_on_first_match=True,
                                                                 thresholds=[0.95], time_out=5)
                        if lingqudian != [0]:
                            time.sleep(2)
                            self.device.tap_on_screen(lingqudian[0])
                            time.sleep(2)
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'),
                                                           timeout=6)[0])
                            time.sleep(2)
                    else:
                        lingqu_names = ['赠礼资源找回领取', '新手任务的领取', '新手任务领取2']
                        lingqudian, parm_list = get_wait_matches(beijingjson=self.zhuye_json,
                                                                 targetjson=self.zhuye_json,
                                                                 device=self.device,
                                                                 target_names=lingqu_names,
                                                                 beijing_name='赠礼右区域',
                                                                 maskname=None, stop_on_first_match=True,
                                                                 thresholds=[0.98,0.95,0.95], time_out=5)
                        if lingqudian != [0]:
                            time.sleep(2)
                            self.device.tap_on_screen(lingqudian[0])
                            time.sleep(2)
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'),
                                                           timeout=6)[0])
                            time.sleep(2)
                        continue

                    guoqu_you = []
                    pr_len = len(guoqu_you)
                    for j in youdian:
                        if j not in guoqu_you:
                            guoqu_you.append(j)
                            self.device.tap_on_screen(j)
                            time.sleep(2)
                            lingqu_names = ['赠礼资源找回领取', '新手任务的领取', '新手任务领取2']
                            lingqudian, parm_list = get_wait_matches(beijingjson=self.zhuye_json,
                                                                     targetjson=self.zhuye_json,
                                                                     device=self.device,
                                                                     target_names=lingqu_names,
                                                                     beijing_name='赠礼右区域',
                                                                     maskname=None, stop_on_first_match=True,
                                                                     thresholds=[0.98,0.95,0.95], time_out=5)
                            if lingqudian != [0]:
                                time.sleep(2)
                                self.device.tap_on_screen(lingqudian[0])
                                time.sleep(2)
                                self.device.tap_on_screen(
                                    self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'),
                                                               timeout=6)[0])
                                time.sleep(2)

                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'),
                                                           timeout=6)[0])

                    cr_len = len(guoqu_you)
                    print('1')


            else:
                print('不存在小光点')
                return True
            cur_len = len(guoqu)
            if cur_len == prelen:
                print('2')
                return True

        print('3')
    def chengjiu(self):
        self.enter()
        time.sleep(2)
        self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('主页成就位置')[0],
                                                         self.zhuye_json.img_areas('主页成就位置')[1]))
        time.sleep(2)
        self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('成就领取进入')[0],
                                                         self.zhuye_json.img_areas('成就领取进入')[1]))
        time.sleep(3)
        guoqu = []

        while True:
            prelen = len(guoqu)
            target_names = ['小光点图片', '小光点2', '小光点3', '小光点4',
                            '小光点5', '小光点6', '小光点7', '小光点8'
                , '小光点9', '小光点10', '小光点11'
                , '小光点12', '小光点13', '小光点14', '小光点15','小光点16']
            print('查找左边区域')
            zuodian, parm_list = get_wait_matches(beijingjson=self.zhuye_json, targetjson=self.zhuye_json,
                                                  device=self.device,
                                                  target_names=target_names,
                                                  beijing_name='成就领取左区域',
                                                  maskname=['小光点new'], stop_on_first_match=False,
                                                  thresholds=[0.9], time_out=5)

            print(zuodian)
            if zuodian != [0]:
                zuodian = merge_close_matches(zuodian, distance_threshold=20)
                for i in zuodian:
                    self.device.tap_on_screen(i)
                    lingqu_names = ['成就内的领取','成就外的领取']
                    time.sleep(2)
                    lingqudian, parm_list = get_wait_matches(beijingjson=self.zhuye_json,
                                                             targetjson=self.zhuye_json,
                                                             device=self.device,
                                                             target_names=lingqu_names,
                                                             beijing_name='赠礼右区域',
                                                             maskname=['小光点new'], stop_on_first_match=True,
                                                             thresholds=[0.85], time_out=5)
                    if lingqudian != [0]:
                        time.sleep(2)
                        self.device.tap_on_screen(lingqudian[0])

                        time.sleep(2)

            else:
                time.sleep(2)
                self.back.back()
                time.sleep(2)
                break
        while True:
            prelen = len(guoqu)
            target_names = ['小光点图片', '小光点2', '小光点3', '小光点4',
                            '小光点5', '小光点6', '小光点7', '小光点8'
                , '小光点9', '小光点10', '小光点11'
                , '小光点12', '小光点13', '小光点14', '小光点15','小光点16']
            print('查找左边区域')
            zuodian, parm_list = get_wait_matches(beijingjson=self.zhuye_json, targetjson=self.zhuye_json,
                                                  device=self.device,
                                                  target_names=target_names,
                                                  beijing_name='成就外的光点区域',
                                                  maskname=['小光点new'], stop_on_first_match=False,
                                                  thresholds=[0.9], time_out=5)

            print(zuodian)
            if zuodian != [0]:
                zuodian = merge_close_matches(zuodian, distance_threshold=20)
                for i in zuodian:
                    self.device.tap_on_screen(i)
                    lingqu_names = ['成就内的领取','成就外的领取']
                    time.sleep(2)
                    lingqudian, parm_list = get_wait_matches(beijingjson=self.zhuye_json,
                                                             targetjson=self.zhuye_json,
                                                             device=self.device,
                                                             target_names=lingqu_names,
                                                             beijing_name='赠礼右区域',
                                                             maskname=['小光点new'], stop_on_first_match=True,
                                                             thresholds=[0.85], time_out=5)
                    if lingqudian != [0]:
                        time.sleep(2)
                        self.device.tap_on_screen(lingqudian[0])
                        time.sleep(2)
                        self.device.tap_on_screen(
                            self.device.wait_for_image(self.zhuye_json.img_path('点击空白处关闭'),
                                                       timeout=6)[0])
                        time.sleep(2)

            else:
                time.sleep(2)
                self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('点击空白处关闭')[0],
                                                                 self.zhuye_json.img_areas('点击空白处关闭')[1]))
                time.sleep(2)
                self.back.back()

                time.sleep(2)
                break












    def start(self):
        self.mianfeichongzhi()
        self.zengli()
        self.youxiang()
        self.pingji()
        self.zhaomu()
        self.shangdian()
        self.renwu()
        self.dianzan()
        self.zhuhe()
        self.chengjiu()


# dd=youxiang_renwu(device,zhuye_json)
# dd.start()




