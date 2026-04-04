from assignment.zhuangyuan.庄园助手 import zhuhsou
from assignment.zhuangyuan.加工站 import jiagongzhan
from assignment.zhuangyuan.同游 import tongyou
from assignment.zhuangyuan.庄园任务领取 import lingqu
# from pathlib import Path
# from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
# from base_tool.read_json import json_reader
# from base_tool.projection_root import find_project_root
from base_tool.backtomain import BackToMain
# script_path = Path(__file__).resolve()
# print(script_path)
# # 获取脚本所在的目录
# script_dir = find_project_root()
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
class totalzhuangyuan():
    def __init__(self, AndroidDevice, json_reader,stop_event=None):
        self.device = AndroidDevice
        self.Zhuangyuan_json = json_reader
        self.zhushou_flag = False
        self.tongyou_flag = False
        self.lingqu_flag=False
        self.zhuhsou = zhuhsou(self.device, self.Zhuangyuan_json)
        self.jiagongzhan = jiagongzhan(self.device, self.Zhuangyuan_json)
        self.tongyou = tongyou(self.device, self.Zhuangyuan_json)
        self.lingqu=lingqu(self.device, self.Zhuangyuan_json)
        self.back = BackToMain(AndroidDevice)
        self.stop_event = stop_event

    def start(self):
        if self.zhushou_flag != True:
            self.zhuhsou.start_zhushou()
            self.zhushou_flag = self.zhuhsou.finish_flag
        if self.tongyou_flag != True:
            self.tongyou.start()
            self.tongyou_flag=self.tongyou.finish
        self.jiagongzhan.start()
        if self.lingqu_flag != True:
            self.lingqu.start()
            self.lingqu_flag=self.lingqu.lingqu1





# dd=totalzhuangyuan(device,Zhuangyuan_json)
# dd.start()



