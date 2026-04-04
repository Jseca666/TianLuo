# import json
import time
# from pathlib import Path
# from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
from base_tool.backtomain import BackToMain
from base_tool.number_get import number_get,parse_chinese_number
# from base_tool.projection_root import find_project_root
# from tubu_ares import is_point_in_union
# import json
# # 获取当前脚本文件的绝对路径
# script_path = Path(__file__).resolve()
# print(script_path)
# # 获取脚本所在的目录
# script_dir = script_path.parent.parent.parent
# print(script_path)
# # 定义 seven.json 的绝对路径
# ZJ_file = script_dir /'base_tool' /'location' / 'Zhuangyuan' / 'Zhuangyuan.json'
# bj=script_dir /'base_tool' /'location' / 'Zhuangyuan' /'baifangtouxiang'/'baifangtouxiang.json'
# img_file=script_dir /'base_tool'#定义好图片的根目录
# print(img_file)
# # 检查文件是否存在
# if not ZJ_file.exists():
#     print(f"信息文件不存在: {ZJ_file}")
#     # 根据需要，可以选择创建文件或通过GUI应用程序生成
#     exit()
# Zhuangyuan_json=json_reader(ZJ_file)
# baifang_json=json_reader(bj)
# device=AndroidDevice()
# device.img_path_abs=img_file
# device.connect_device()
class zhuhsou():

    def __init__(self, AndroidDevice, json_reader):
        self.device = AndroidDevice
        self.Zhuangyuan_json = json_reader
        self.back = BackToMain(self.device)
        self.number_get = number_get(AndroidDevice=self.device, json_reader=self.Zhuangyuan_json)
        self.ruqin_num=0
        self.baifang_num = 0
        self.finish_flag=False
    def get_num(self):
        time.sleep(2)
        self.baifang_num=int(self.number_get.extract_numbers(loc_name='庄园助手拜访数量区域',excluded_number=-1)[0])
        self.ruqin_num=int(self.number_get.extract_numbers(loc_name='庄园助手入侵者数量区域',excluded_number=-1)[0])

    def start_zhushou(self):
        self.back.back_to_main()
        self.device.tap_on_screen(
            self.device.wait_for_image(self.Zhuangyuan_json.img_path('主页庄园图标'), threshold=0.95)[0])
        self.device.tap_on_screen(
            self.device.wait_for_image(self.Zhuangyuan_json.img_path('庄园助手'),timeout=20, threshold=0.95)[0])
        self.get_num()
        if True:
            self.device.tap_on_screen(
                self.device.wait_for_image(self.Zhuangyuan_json.img_path('庄园助手一键执行区域'), threshold=0.95)[0])
            time.sleep(2)
            self.device.tap_on_screen(
                self.device.wait_for_image(self.Zhuangyuan_json.img_path('一键执行后的确认区域'), threshold=0.95)[0])
        if self.baifang_num==0 and self.ruqin_num==0:
            self.finish_flag=True
        return True

# dd=zhuhsou(device,Zhuangyuan_json)
# dd.get_zuanshi()