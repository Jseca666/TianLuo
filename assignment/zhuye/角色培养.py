import json
import time
from pathlib import Path
import cv2
# from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
from base_tool.number_get import number_get, parse_chinese_number
# from base_tool.get_matches import get_matches, get_wait_matches, ResultProcessor
# from base_tool.projection_root import find_project_root

#
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
class peiyang():
    def __init__(self, AndroidDevice, json_reader,huoban_flag=0,zhuangbei_flag=0,stop_event=None):
        self.device = AndroidDevice
        self.zhuye_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.number_get = number_get(AndroidDevice=self.device, json_reader=self.zhuye_json)
        self.huoban_flag=huoban_flag
        self.zhuangbei_flag=zhuangbei_flag
        self.curjue=5
        self.curzhuang=5
        self.stop_event = stop_event
    def enter(self):
        self.back.back_to_main()
        self.device.tap_on_screen(
            self.device.wait_for_image(self.zhuye_json.img_path('小队入口'), threshold=0.97)[0])
    def huoban(self):
        self.enter()
        time.sleep(2)
        self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('第一个角色位置')[0],
                                                         self.zhuye_json.img_areas('第一个角色位置')[1]))
        time.sleep(2)
        self.device.tap_on_screen(
            self.device.wait_for_image(self.zhuye_json.img_path('主角培养'), threshold=0.95)[0])
        while True:
            while True:
                time.sleep(2)
                self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('充值关闭的位置')[0],
                                                                 self.zhuye_json.img_areas('充值关闭的位置')[
                                                                     1]))
                time.sleep(2)
                self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('升级位置')[0],
                                                                 self.zhuye_json.img_areas('升级位置')[
                                                                     1]))
                time.sleep(2)
                self.device.tap_on_screen(
                    self.device.wait_for_image(self.zhuye_json.img_path('提升5级所在区域'), threshold=0.97)[0])
                if self.device.wait_for_image(self.zhuye_json.img_path('进阶弹窗'), threshold=0.97,
                                              timeout=2) != [0]:


                    time.sleep(1)
                    self.back.back()
                    break
                if self.device.wait_for_image(self.zhuye_json.img_path('升级失败的系统提示'), timeout=3) != [0]:
                    self.device.tap_on_screen(self.device.wait_for_image(
                        self.zhuye_json.img_path('系统提示后的取消'), threshold=0.97)[0])
                    break
            time.sleep(3)
            self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('伙伴培养升阶所在位置')[0],
                                                             self.zhuye_json.img_areas('伙伴培养升阶所在位置')[
                                                                 1]))
            time.sleep(3)
            while True:
                if self.device.tap_on_screen(
                        self.device.wait_for_image(self.zhuye_json.img_path('进阶按钮'), threshold=0.97)[0]):
                    if self.device.wait_for_image(self.zhuye_json.img_path('进阶弹窗'), threshold=0.97,
                                                  timeout=2) != [0]:
                        if self.device.tap_on_screen(
                            self.device.wait_for_image(self.zhuye_json.img_path('进阶点击后的前往'),
                                                       threshold=0.97)[0]):
                            if self.device.wait_for_image(self.zhuye_json.img_path('未开启关卡的标志'),threshold=0.97,timeout=3) !=[0]:
                                time.sleep(2)
                                self.back.back()
                                time.sleep(2)
                                break
                            if self.device.wait_for_image(self.zhuye_json.img_path('关卡未挑战标志'),threshold=0.97,timeout=3) !=[0]:
                                time.sleep(2)
                                self.back.back()
                                time.sleep(2)
                                break
                            time.sleep(2)

                            self.device.tap_on_screen(
                                self.device.get_centra(self.zhuye_json.img_areas('进阶前往后的扫荡10')[0],
                                                       self.zhuye_json.img_areas('进阶前往后的扫荡10')[1]))
                            time.sleep(2)
                            if self.device.wait_for_image(self.zhuye_json.img_path('体力不足的弹窗'), timeout=2) != [0]:
                                self.device.tap_on_screen(
                                    self.device.wait_for_image(self.zhuye_json.img_path('使用体力的按钮'))[0])
                                time.sleep(2)
                                img1 = cv2.imread(self.device.capture_screenshot())
                                self.device.tap_on_screen(
                                    self.device.wait_for_image(self.zhuye_json.img_path('使用确认的按钮'))[0])
                                time.sleep(2)
                                self.device.tap_on_screen(
                                    self.device.get_centra(self.zhuye_json.img_areas('进阶前往后的扫荡10')[0],
                                                           self.zhuye_json.img_areas('进阶前往后的扫荡10')[1]))
                                img2 = cv2.imread(self.device.capture_screenshot())
                                if self.device.compare_images(img1, img2) == True:
                                    print('体力不足暂停挑战')
                                    return True
                            time.sleep(1)
                            self.device.tap_on_screen(
                                self.device.wait_for_image(self.zhuye_json.img_path('扫荡完成的确认'), threshold=0.97)[
                                    0])
                        else:
                            print('资源关卡未开启')
                            time.sleep(2)
                            self.back.back()
                            time.sleep(2)
                            break



                else:
                    break


            time.sleep(2)
            self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('伙伴培养下一个角色箭头')[0],
                                                                 self.zhuye_json.img_areas('伙伴培养下一个角色箭头')[
                                                                     1]))
            self.curjue -= 1
            time.sleep(1)
            if self.curjue==0:
                break
    def zhuangbei(self):
        self.enter()
        time.sleep(2)
        self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('第一个角色位置')[0],
                                                         self.zhuye_json.img_areas('第一个角色位置')[1]))
        time.sleep(2)
        self.device.tap_on_screen(
            self.device.wait_for_image(self.zhuye_json.img_path('伙伴培养装备位置'), threshold=0.97)[0])
        self.device.tap_on_screen(
            self.device.wait_for_image(self.zhuye_json.img_path('装备养成'), threshold=0.97)[0])
        lo2=self.device.get_centra(self.zhuye_json.img_areas('第二个装备位置')[0],self.zhuye_json.img_areas('第二个装备位置')[1])
        lo3 = self.device.get_centra(self.zhuye_json.img_areas('第三个装备位置')[0], self.zhuye_json.img_areas('第三个装备位置')[1])
        lo4 = self.device.get_centra(self.zhuye_json.img_areas('第四个装备位置')[0], self.zhuye_json.img_areas('第四个装备位置')[1])
        loc=[0,lo2,lo3,lo4]
        print(loc)
        time.sleep(1)
        while True:
            if self.curzhuang == 0:
                self.back.back()
                break
            for i in range(4):
                if i != 0:
                    self.device.tap_on_screen(loc[i])
                if self.curzhuang != 0:
                    time.sleep(1)

                    self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('充值关闭的位置')[0],
                                                                     self.zhuye_json.img_areas('充值关闭的位置')[
                                                                         1]))
                    time.sleep(3)
                    self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('装备打造区域')[0],
                                                                     self.zhuye_json.img_areas('装备打造区域')[1]))
                    while True:
                        self.device.tap_on_screen(
                            self.device.wait_for_image(self.zhuye_json.img_path('装备养成后的打造'),
                                                       threshold=0.97)[0])
                        if self.device.wait_for_image(self.zhuye_json.img_path('升级失败的系统提示'),
                                                      timeout=2,threshold=0.98) != [0]:
                            self.device.tap_on_screen(self.device.wait_for_image(
                                self.zhuye_json.img_path('系统提示后的取消'), threshold=0.97)[0])
                            break
                        if self.device.wait_for_image(self.zhuye_json.img_path('进阶弹窗'), threshold=0.97,
                                                      timeout=2) != [
                            0]:
                            self.back.back()
                            break
                        self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('充值关闭的位置')[0],
                                                                         self.zhuye_json.img_areas('充值关闭的位置')[
                                                                             1]))
                        time.sleep(2)
                        self.device.tap_on_screen(
                            self.device.get_centra(self.zhuye_json.img_areas('装备打造区域')[0],
                                                   self.zhuye_json.img_areas('装备打造区域')[1]))
                        time.sleep(2)
                        self.device.tap_on_screen(
                            self.device.get_centra(self.zhuye_json.img_areas('装备打造区域')[0],
                                                   self.zhuye_json.img_areas('装备打造区域')[1]))
                    time.sleep(1)
                    self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('精炼所在位置')[0],
                                                                     self.zhuye_json.img_areas('精炼所在位置')[1]))
                    while True:
                        if self.device.tap_on_screen(
                                self.device.wait_for_image(self.zhuye_json.img_path('快速精炼'), threshold=0.98,timeout=3)[
                                    0]):
                            time.sleep(1.5)

                            if self.device.wait_for_image(self.zhuye_json.img_path('升级失败的系统提示'), timeout=2,threshold=0.99) != [0]:
                                self.device.tap_on_screen(self.device.wait_for_image(
                                    self.zhuye_json.img_path('系统提示后的取消'), threshold=0.97)[0])
                                break
                            if self.device.wait_for_image(self.zhuye_json.img_path('进阶弹窗'), threshold=0.97,
                                                          timeout=2) != [0]:
                                time.sleep(1)
                                self.back.back()
                                break
                            if self.device.wait_for_image(self.zhuye_json.img_path('精炼结束标志去打造'),
                                                          threshold=0.97,timeout=2) != [0]:
                                break
                            self.device.tap_on_screen(
                                self.device.get_centra(self.zhuye_json.img_areas('充值关闭的位置')[0],
                                                       self.zhuye_json.img_areas('充值关闭的位置')[
                                                           1]))
                            time.sleep(2)
                            self.device.tap_on_screen(
                                self.device.get_centra(self.zhuye_json.img_areas('精炼所在位置')[0],
                                                       self.zhuye_json.img_areas('精炼所在位置')[1]))
                            time.sleep(2)
                            self.device.tap_on_screen(
                                self.device.get_centra(self.zhuye_json.img_areas('精炼所在位置')[0],
                                                       self.zhuye_json.img_areas('精炼所在位置')[1]))
                        else:
                            break
                    self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('充值关闭的位置')[0],
                                                                     self.zhuye_json.img_areas('充值关闭的位置')[
                                                                         1]))
                    time.sleep(2)
                    self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('升维所在区域')[0],
                                                                     self.zhuye_json.img_areas('升维所在区域')[1]))
                    while True:
                        if self.device.tap_on_screen(self.device.wait_for_image(
                                self.zhuye_json.img_path('升维按钮'), threshold=0.99,timeout=2)[0]):
                            if self.device.wait_for_image(self.zhuye_json.img_path('升级失败的系统提示'),
                                                          timeout=2,threshold=0.98) != [0]:
                                self.device.tap_on_screen(self.device.wait_for_image(
                                    self.zhuye_json.img_path('系统提示后的取消'), threshold=0.97)[0])
                                break
                            if self.device.wait_for_image(self.zhuye_json.img_path('进阶弹窗'), threshold=0.95,
                                                          timeout=2) != [
                                0]:
                                self.back.back()
                                break
                            if self.device.wait_for_image(self.zhuye_json.img_path('精炼结束标志去打造'),
                                                          threshold=0.97,
                                                          timeout=2) != [
                                0]:
                                break
                            self.device.tap_on_screen(
                                self.device.get_centra(self.zhuye_json.img_areas('充值关闭的位置')[0],
                                                       self.zhuye_json.img_areas('充值关闭的位置')[
                                                           1]))
                            time.sleep(2)
                            self.device.tap_on_screen(
                                self.device.get_centra(self.zhuye_json.img_areas('升维所在区域')[0],
                                                       self.zhuye_json.img_areas('升维所在区域')[1]))
                            time.sleep(2)
                            self.device.tap_on_screen(
                                self.device.get_centra(self.zhuye_json.img_areas('升维所在区域')[0],
                                                       self.zhuye_json.img_areas('升维所在区域')[1]))
                        else:
                            break
            self.device.tap_on_screen(
                self.device.get_centra(self.zhuye_json.img_areas('伙伴培养下一个角色箭头')[0],
                                       self.zhuye_json.img_areas('伙伴培养下一个角色箭头')[1]))
            self.curzhuang -= 1
            time.sleep(1)
        cout=0
        while True:
            if cout<=5:
                self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('充值关闭的位置')[0],
                                                                 self.zhuye_json.img_areas('充值关闭的位置')[
                                                                     1]))
                time.sleep(2)
                self.device.tap_on_screen(self.device.get_centra(self.zhuye_json.img_areas('一件强化所在位置')[0],
                                                                 self.zhuye_json.img_areas('一件强化所在位置')[1]))
                time.sleep(2)
                if self.device.tap_on_screen(self.device.wait_for_image(
                    self.zhuye_json.img_path('一件强化确定'), threshold=0.97,timeout=6)[0]):
                    if self.device.wait_for_image(self.zhuye_json.img_path('进阶弹窗'), threshold=0.95,
                                                  timeout=2) != [
                        0]:
                        self.back.back()
                    self.device.tap_on_screen(
                        self.device.get_centra(self.zhuye_json.img_areas('一件强化确定')[0],
                                               self.zhuye_json.img_areas('一件强化确定')[1]))

                    time.sleep(2)
                    self.device.tap_on_screen(
                        self.device.get_centra(self.zhuye_json.img_areas('充值关闭的位置')[0],
                                               self.zhuye_json.img_areas('充值关闭的位置')[1]))

                time.sleep(2)
                self.device.tap_on_screen(
                    self.device.get_centra(self.zhuye_json.img_areas('点击空白处关闭')[0],
                                           self.zhuye_json.img_areas('点击空白处关闭')[1]))
                time.sleep(2)
                self.device.tap_on_screen(
                    self.device.get_centra(self.zhuye_json.img_areas('伙伴培养下一个角色箭头')[0],
                                           self.zhuye_json.img_areas('伙伴培养下一个角色箭头')[1]))

                cout += 1
                time.sleep(2)
            else:
                return True







    def start(self):
        if self.huoban_flag==1:
            self.huoban()
        if self.zhuangbei_flag==1:
            self.zhuangbei()








# dd=peiyang(device,zhuye_json)
# dd.start()

