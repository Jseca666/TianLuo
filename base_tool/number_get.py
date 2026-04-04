import re
from base_tool.AndroidDevice import AndroidDevice
from base_tool.read_json import json_reader
import re


def parse_chinese_number(s):
    """
    将包含中文单位的数字字符串转换为整数。

    支持的单位包括：千, 万, 亿, 兆
    例如：
    '159万' -> 1590000
    '1.59万' -> 15900
    '2亿' -> 200000000
    '3.5兆' -> 3500000000000
    '123' -> 123
    """
    # 定义单位对应的乘数
    unit_multipliers = {
        '千': 10 ** 3,
        '万': 10 ** 4,
        '亿': 10 ** 8,
        '兆': 10 ** 12
    }

    # 使用正则表达式分离数字部分和单位部分
    pattern = r'^([0-9]+(?:\.[0-9]+)?)([千万亿兆]?)$'
    match = re.match(pattern, s)

    if not match:
        raise ValueError(f"无法解析的数字格式: '{s}'")

    number_str, unit = match.groups()
    number = float(number_str)

    if unit:
        multiplier = unit_multipliers.get(unit)
        if not multiplier:
            raise ValueError(f"未知的单位: '{unit}'")
        number *= multiplier

    return int(number)
class number_get():
    def __init__(self,AndroidDevice,json_reader):
        self.input_str=''
        self.excluded_number=[]
        self.device=AndroidDevice
        self.json=json_reader
        self.loc_name = None
        self.mask_name=None
        self.kernel_size=None
    def extract_numbers(self,loc_name,excluded_number,mask_name=None,kernel_size=None):
        self.loc_name = loc_name
        self.mask_name=mask_name
        self.kernel_size=kernel_size
        self.excluded_number=excluded_number
        self.input_str = self.device.get_text_from_screen(self.json.img_areas(self.loc_name)[0],
                                          self.json.img_areas(self.loc_name)[1],
                                          mask_name=self.mask_name,kernel_size=self.kernel_size)
        print(self.input_str)
        all_numbers=[]
        self.excluded_number=excluded_number
        for i in self.input_str:
            numbers = re.findall(r'\d+', i)
            all_numbers.extend(numbers)

        # 排除指定的数字
        result = [num for num in all_numbers if num != str(self.excluded_number)]
        print('result=',result)
        return result

