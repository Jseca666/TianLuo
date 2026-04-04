from assignment.shetuan.社团演训 import yanxun
from assignment.shetuan.委托派遣 import weituo
from assignment.shetuan.浇水 import jiaoshui
from assignment.shetuan.社团大厅与核心工坊 import datingtongfang
from assignment.shetuan.猛鬼来袭 import menggui
from  assignment.shetuan.社团红包 import hongbao
# import json
# import time
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
class total_shetuan():
    def __init__(self, AndroidDevice, json_reader,stop_event=None):
        self.device = AndroidDevice
        self.shetuan_json = json_reader
        self.back = BackToMain(AndroidDevice)
        self.shetuanflag=False
        self.numberget = number_get(AndroidDevice, json_reader)
        self.hongbao=hongbao(self.device,self.shetuan_json)
        self.yanxun=yanxun(self.device,self.shetuan_json)
        self.weituo=weituo(self.device,self.shetuan_json)
        self.jiaoshui=jiaoshui(self.device,self.shetuan_json)
        self.datingtongfang=datingtongfang(self.device,self.shetuan_json)
        self.menggui=menggui(self.device,self.shetuan_json)
        self.stop_event = stop_event
    def start(self):
        self.back.back_to_main()
        self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团入口'))[0])
        if self.device.tap_on_screen(self.device.wait_for_image(self.shetuan_json.img_path('社团红包入口'),timeout=15)[0]):
            print('该账号已加入了社团可以执行社团任务')
        else:
            print('该账户未加入社团')
            return True
        self.hongbao.start()
        self.yanxun.start()
        self.weituo.start()
        self.jiaoshui.start()
        self.datingtongfang.start()
        self.menggui.start()
        self.shetuanflag=True
# dd=total_shetuan(device,shetuan_json)
# dd.start()


