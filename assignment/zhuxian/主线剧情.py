import json
import time
import cv2
# from pathlib import Path
from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
from base_tool.number_get import number_get, parse_chinese_number
from base_tool.projection_root import find_project_root
from base_tool.get_matches import get_matches, get_wait_matches, ResultProcessor
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
device = AndroidDevice()
# device.img_path_abs = img_file
# device.connect_device()


class zhuxian():
    def __init__(self, AndroidDevice, json_reader,nandu_flag=0):
        self.device = AndroidDevice
        self.zhuxian_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.cur_chapter = 0
        self.tili=0
        self.cur_guanqia = 0
        self.numberget = number_get(AndroidDevice, json_reader)
        self.cur_xing=0
        self.nandu_flag=nandu_flag #0表示简单，1表示苦难
        self.cur_max_guanqia=10
        self.jiedian=None
    def enter_zhuxian(self):
        # 先回到主页
        self.back.back_to_main()
        # 进入七宗罪
        self.device.tap_on_screen(self.device.wait_for_image(self.zhuxian_json.img_path('主页主线剧情入口'))[0])
        time.sleep(2)
        if self.nandu_flag==0:
            self.device.tap_on_screen(self.device.get_centra(self.zhuxian_json.img_areas('主线简单点击区域')[0],
                                                             self.zhuxian_json.img_areas('主线简单点击区域')[1] ))
        else:
            self.device.tap_on_screen(self.device.get_centra(self.zhuxian_json.img_areas('主线苦难点击区域')[0],
                                                             self.zhuxian_json.img_areas('主线苦难点击区域')[1]))
    def get_zhuxian(self):

        time.sleep(4)
        self.cur_chapter = int(self.numberget.extract_numbers('探索进度区域', excluded_number=-1)[0])
        self.cur_guanqia = int(self.numberget.extract_numbers('探索进度区域', excluded_number=-1)[1])
        self.cur_xing = (self.cur_guanqia-1)*3

        self.device.tap_on_screen(self.device.wait_for_image(self.zhuxian_json.img_path('主线剧情入口后的探索'))[0])
        time.sleep(4)
        self.tili = int(self.numberget.extract_numbers('体力剩余区域', excluded_number=-1)[0])
        if self.device.wait_for_image(self.zhuxian_json.img_path('主线因为段位不足的提示'), timeout=2) != [
            0]:
            print('段位不足，主线探索结束')
            return True
        if self.nandu_flag==0:
            time.sleep(3)
            ddd = self.numberget.extract_numbers('当前章节的宝箱节点', excluded_number=-1)
            jiedian = []
            for i in ddd:
                if (ddd.index(i) + 1) % 2 == 0:
                    jiedian.append(int(i))

            self.cur_max_guanqia=jiedian[-1]
            self.jiedian=jiedian

        else:
            time.sleep(3)
            ddd = self.numberget.extract_numbers('主线苦难星级获取区域', excluded_number=-1)
            jiedian = []
            for i in ddd:
                if (ddd.index(i) + 1) % 2 == 0:
                    jiedian.append(int(i))
            self.cur_max_guanqia = jiedian[-1]/3
            self.jiedian = jiedian
        print(self.jiedian)

    def start(self):
        self.enter_zhuxian()
        if self.get_zhuxian()==True:
            return True
        dabuguo=None
        while True:
            if self.nandu_flag==1 and self.cur_guanqia!=1:
                self.device.tap_on_screen(
                    self.device.get_centra(self.zhuxian_json.img_areas('苦难上一关位置')[0],
                                           self.zhuxian_json.img_areas('苦难上一关位置')[1]))
                time.sleep(2)
                xing_loc = get_matches(self.zhuxian_json, self.zhuxian_json, self.device, '苦难识别星星位置',
                                       '苦难星星模板', use_color=True)
                if len(xing_loc) != 3:
                    print('上一关没满星')
                    self.cur_guanqia-=1
                    time.sleep(4)
                    pre_guan = int(self.numberget.extract_numbers('当前关卡和章节位置', excluded_number=-1)[1])
                    dabuguo=1
                else:
                    time.sleep(1)
                    self.device.tap_on_screen(
                        self.device.get_centra(self.zhuxian_json.img_areas('苦难下一关位置')[0],
                                               self.zhuxian_json.img_areas('苦难下一关位置')[1]))


            self.device.tap_on_screen(self.device.wait_for_image(self.zhuxian_json.img_path('关卡页面的挑战位置'))[0])
            if self.device.wait_for_image(self.zhuxian_json.img_path('体力不足的弹窗'),timeout=4) !=[0] :
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.zhuxian_json.img_path('使用体力的按钮'))[0])
                img1=cv2.imread(device.capture_screenshot())
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.zhuxian_json.img_path('使用确认的按钮'))[0])
                img2 = cv2.imread(device.capture_screenshot())
                if device.compare_images(img1,img2) ==True:
                    print('体力不足暂停挑战')
                    return True
                else:
                    self.device.tap_on_screen(
                        self.device.wait_for_image(self.zhuxian_json.img_path('关卡页面的挑战位置'))[0])


            time.sleep(2)
            target_names = [ '跳过战斗', '跳过']
            num_matchs, parm_list = get_wait_matches(beijingjson=self.zhuxian_json, targetjson=self.zhuxian_json,
                                                       device=self.device,
                                                       target_names=target_names,
                                                       maskname=['跳过战斗','同游跳过白色'],stop_on_first_match=True,thresholds=[0.7,0.7],time_out=15)
            print(num_matchs)
            path=parm_list[0]['template_path']
            # 使用反斜杠 '\\' 分割字符串，得到 ['location', 'zhuxian', '跳过.png']
            parts = path.split('\\')
            # 获取最后一部分 '跳过.png'
            file_name_with_extension = parts[-1]
            # 使用 '.' 分割，去掉扩展名，得到 '跳过'
            target_names = file_name_with_extension.split('.')[0]
            print(target_names)  # 输出: 跳过
            if target_names=='跳过':
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.zhuxian_json.img_path('跳过'), mask_name='同游跳过白色')[0])
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.zhuxian_json.img_path('打完剧情跳过确认'))[0])

            self.device.tap_on_screen(
                self.device.wait_for_image(self.zhuxian_json.img_path('跳过战斗'), mask_name='跳过战斗',threshold=0.5,timeout=25)[0])
            if self.device.wait_for_image(self.zhuxian_json.img_path('刷龙胜利'))[0] != 0:
                time.sleep(1)
                if self.device.wait_for_image(self.zhuxian_json.img_path('轮回走廊战斗失败标志'),timeout=2) != [
                    0] :
                    self.device.tap_on_screen(
                        self.device.get_centra(self.zhuxian_json.img_areas('点击空白处关闭')[0],
                                               self.zhuxian_json.img_areas('点击空白处关闭')[1]))
                    print('打不过了')
                    return True
                else:

                    self.device.tap_on_screen(
                        self.device.get_centra(self.zhuxian_json.img_areas('点击空白处关闭')[0],
                                               self.zhuxian_json.img_areas('点击空白处关闭')[1]))

                    tiaoguo_flag= self.device.wait_for_image(self.zhuxian_json.img_path('跳过'), mask_name='同游跳过白色',timeout=4)
                    if tiaoguo_flag != [0]:
                        self.device.tap_on_screen(tiaoguo_flag[0])
                        self.device.tap_on_screen(
                            self.device.wait_for_image(self.zhuxian_json.img_path('打完剧情跳过确认'))[0])
                    if self.nandu_flag==0:
                        self.cur_guanqia = self.cur_guanqia + 1
                        if self.cur_guanqia - 1 in self.jiedian:
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.zhuxian_json.img_path('点击空白处关闭'))[0])

                        time.sleep(2)

                    else:
                        if self.cur_xing  in self.jiedian:
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.zhuxian_json.img_path('点击空白处关闭'))[0])
                        time.sleep(3)
                        if dabuguo==1:

                            cur_guan=int(self.numberget.extract_numbers('当前关卡和章节位置', excluded_number=-1)[1])
                            if cur_guan==pre_guan:
                                print('确实是打不过了')
                                return True
                        self.device.tap_on_screen(
                            self.device.get_centra(self.zhuxian_json.img_areas('苦难上一关位置')[0],
                                                   self.zhuxian_json.img_areas('苦难上一关位置')[1]))
                        self.cur_guanqia = self.cur_guanqia + 1
                        self.cur_xing = self.cur_xing + 3
                        time.sleep(2)
                        xing_loc=get_matches(self.zhuxian_json,self.zhuxian_json,self.device,'苦难识别星星位置','苦难星星模板',use_color=True,threshold=0.5)
                        if len(xing_loc)!=3:
                            print('无法满星了停止挑战')
                            return True
                        time.sleep(2)
                        self.device.tap_on_screen(
                            self.device.get_centra(self.zhuxian_json.img_areas('苦难下一关位置')[0],
                                                   self.zhuxian_json.img_areas('苦难下一关位置')[1]))

            if self.cur_guanqia>self.cur_max_guanqia :
                time.sleep(3)
                if self.get_zhuxian() == True:
                    return True


# dd=zhuxian(device,zhuxian_json,0)
# dd.start()
