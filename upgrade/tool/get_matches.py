
import time
from base_tool.AndroidDevice import AndroidDevice
from base_tool.read_json import json_reader
def get_matches(beijingjson,targetjson,device,beijing_name,target_name,mask_name=None,use_color=False,timeout=5):
    top_left=beijingjson.img_areas(beijing_name)[0]
    bottom_right=beijingjson.img_areas(beijing_name)[1]
    beijinares=device.local_get(top_left,
                                bottom_right)
    start_time = time.time()
    interval=1
    while time.time() - start_time < timeout:
        maches = device.find_image_in_screenshot(screenshot=beijinares,
                                                 template_path=targetjson.img_path(target_name),
                                                 mask_name=mask_name, threshold=0.6, use_color=use_color)
        if maches != [0]:
            break
        else:
            time.sleep(interval)
    rescult=[]
    print(maches)
    if maches!=[0]:
        print('背景中存在匹配点')
        for mache in maches:
            mache=list(mache)
            mache[0]=mache[0]+top_left[0]
            mache[1] = mache[1]+top_left[1]
            rescult.append(tuple(mache))
    else:
        rescult.append(0)
    return rescult
def get_wait_matches(targetjson,device,beijingjson,target_names,beijing_name=None,maskname=None,stop_on_first_match=False,thresholds=None,time_out=10):
    if beijing_name is not None:
        top_left = beijingjson.img_areas(beijing_name)[0]
        bottom_right = beijingjson.img_areas(beijing_name)[1]
        beijinares = device.local_get(top_left, bottom_right)
    else:
        top_left=[0,0]
        bottom_right=[1280,720]
        beijinares=device.local_get(top_left,bottom_right )
    template_paths=[targetjson.img_path(target_name) for target_name in target_names]
    if maskname is not None and maskname is not [] and len(maskname)==1:
        masknames = maskname * len(template_paths)
        print(masknames)
    else:
        masknames=maskname
    if thresholds is not  None and len(thresholds) !=1:
        thresholds=thresholds

    else:thresholds=thresholds*len(template_paths)
    print(thresholds)
    maches,parm_list = device.wait_for_images(beijinares=beijinares,
                                             template_paths=template_paths,
                                             mask_names=masknames, thresholds=thresholds,stop_on_first_match=stop_on_first_match,timeout=time_out)
    rescult = []
    print('maches=',maches)
    print(parm_list)
    if maches != [0]:
        print('背景中存在匹配点')
        for mache in maches:
            mache = list(mache)
            mache[0] = mache[0] + top_left[0]
            mache[1] = mache[1] + top_left[1]
            rescult.append(tuple(mache))
    if rescult  == []:
        rescult.append(0)
    print('rescult=',rescult)
    return rescult,parm_list


import re
from typing import List, Dict, Tuple

class ResultProcessor:
    def __init__(self, result_list: List[Dict]):
        self.result_list = result_list
        self.numbers_with_coords = self._extract_numbers_with_coordinates()

    def _extract_number_from_path(self, template_path: str) -> int:
        match = re.search(r'标准数字(\d+)\.png', template_path)
        if match:
            return int(match.group(1))
        else:
            raise ValueError(f"无法从路径中提取数字: {template_path}")

    def _extract_numbers_with_coordinates(self) -> List[Tuple[int, List[Tuple[int, int]]]]:
        numbers_coords = []
        for item in self.result_list:
            number = self._extract_number_from_path(item['template_path'])
            coords = item.get('results', [])
            numbers_coords.append((number, coords))
        return numbers_coords

    def count_coordinates_per_number(self) -> Dict[int, int]:
        count_dict = {}
        for number, coords in self.numbers_with_coords:
            count = len(coords)
            count_dict[number] = count
            print(f"数字 {number} 对应的坐标个数: {count}")
        return count_dict

    def concatenate_numbers_left_to_right(self) -> str:
        x_number_list = []
        for number, coords in self.numbers_with_coords:
            for coord in coords:
                x = coord[0]
                x_number_list.append((x, number))

        sorted_x_number = sorted(x_number_list, key=lambda x: x[0])
        concatenated = ''.join(str(num) for _, num in sorted_x_number)
        print(f"拼接后的数字字符串: {concatenated}")
        return concatenated

    def sum_of_numbers(self) -> int:
        print("定义 sum_of_numbers 方法")
        total = 0
        for number, coords in self.numbers_with_coords:
            total += number * len(coords)
        print(f"所有坐标对应数字的总和: {total}")
        return total

# # 测试代码
# if __name__ == "__main__":
#     result_list = [
#         {
#             'template_path': 'location\\numbers\\标准数字0.png',
#             'threshold': 0.6,
#             'mask_name': '宠物之家猫粮数量',
#             'results': [(24, 20), (230, 20)]
#         },
#         {
#             'template_path': 'location\\numbers\\标准数字1.png',
#             'threshold': 0.6,
#             'mask_name': '宠物之家猫粮数量',
#             'results': [(127, 20)]
#         }
#     ]
#
#     processor = ResultProcessor(result_list)
#
#     # 功能一：输出每个数字对应的坐标个数
#     processor.count_coordinates_per_number()
#
#     # 功能二：输出拼接后的数字字符串
#     concatenated_string = processor.concatenate_numbers_left_to_right()
#     print(f"最终输出: {concatenated_string}")  # 预期输出: "010"
#
#     # 功能三：输出所有坐标对应数字的总和
#     total_sum = processor.sum_of_numbers()
#     print(f"数字总和: {total_sum}")  # 预期输出: 1
