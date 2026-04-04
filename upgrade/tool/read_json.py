import json
import time
from pathlib import Path
import json
# from base_tool.linkstart import AndroidDevice
class json_reader:
    def __init__(self, json_path = r"base_tool/location/NIBO/seven_info.json"):
        self.json_path = json_path
        self.arename=''
        self.img_path1="image_path"
        self.ares="coordinates"
        self.top_left="top_left"
        self.bottom_right ="bottom_right"
    def load_json(self,arename):
        self.arename =arename

        with open(self.json_path, 'r', encoding='utf-8') as f:
            json_info = json.load(f)
        return json_info.get(self.arename)
    def img_path(self,arename):
        json_info=self.load_json(arename)
        img_path=json_info.get(self.img_path1)
        return img_path
    def img_areas(self,arename):
        json_info=self.load_json(arename)
        area_info=json_info.get(self.ares)
        top_left=area_info.get(self.top_left)
        bottom_right = area_info.get(self.bottom_right)
        return top_left,bottom_right
# script_path = Path(__file__).resolve()
#
# # 获取脚本所在的目录
# dec=AndroidDevice()
# script_dir = script_path.parent
# # 定义 seven.json 的相对路径
# info_file = script_dir / 'location' / 'NIBO' / 'seven_info.json'
# ddd=json_reader(info_file)
# print(ddd.img_path('退出主页提醒'))
# print(ddd.img_areas('退出主页提醒'))
# print(dec.get_centra(ddd.img_areas('退出主页提醒')[0],ddd.img_areas('退出主页提醒')[1]))