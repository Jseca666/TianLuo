import time
from pathlib import Path
from base_tool.AndroidDevice import AndroidDevice  # 确保linkstart模块在你的环境中可用
from base_tool.read_json import json_reader


class BackToMain:
    def __init__(self, device: AndroidDevice):
        """
        初始化 BackToMain 类。

        :param device: 已存在的 AndroidDevice 实例。
        """
        # 验证传入的 device 是否为 AndroidDevice 的实例
        if not isinstance(device, AndroidDevice):
            raise TypeError("device 必须是 AndroidDevice 的实例")

        self.device = device

        # 获取当前脚本文件的绝对路径
        self.script_path = Path(__file__).resolve()
        # 动态查找项目根目录，假设根目录包含 main.py 文件
        self.project_root = self.find_project_root()

        # 定义 seven_info.json 的绝对路径
        self.info_file = self.project_root / 'base_tool' / 'location' / 'NIBO' / 'seven_info.json'
        self.img_file = self.project_root / 'base_tool'

        # 检查信息文件是否存在
        if not self.info_file.exists():
            print(f"信息文件不存在: {self.info_file}")
            exit()

        # 读取 JSON 文件
        self.json_reader = json_reader(self.info_file)

        # 设置设备的图片路径
        self.device.img_path_abs = self.img_file

    def find_project_root(self):
        """
        查找项目的根目录，假设项目根目录包含 'main.py' 文件。

        :return: 项目的根目录路径。
        """
        current_path = self.script_path

        # 向上递归查找，直到找到包含 'main.py' 的目录
        while current_path != current_path.parent:
            if (current_path / 'main.py').exists():
                return current_path
            current_path = current_path.parent

        raise FileNotFoundError("未能找到项目的根目录，请确保项目包含 'main.py' 文件")

    def connect_and_check_device(self):
        """
        连接 Android 设备并检查是否成功连接。
        """
        # 连接设备
        self.device.connect_device()

        # 检查设备是否连接成功
        if not self.device.is_device_connected():
            print(f"无法连接到设备 {self.device.device_address}。请检查设备是否已启动并连接。")
            exit()

    def back_to_main(self):
        """
        持续按返回按钮，直到回到主页，找到指定的图像并点击取消按钮。
        """
        back = True
        # 获取图像路径
        TUICHU_img = self.json_reader.img_path('退出主页提醒')
        quxiao_img = self.json_reader.img_path('取消退出')

        # 持续按返回键，直到检测到图像
        while back:
            self.device.press_back_button()

            matches = self.device.find_image_on_screen(str(TUICHU_img))[0]
            if  matches != 0:
                print(f"找到区域 '退出主页提醒' 在位置: {matches}")

                # 等待并点击取消按钮
                quxiaoloc = self.device.wait_for_image(quxiao_img)[0]
                if quxiaoloc and quxiaoloc != 0:
                    print(f"找到取消按钮的位置: {quxiaoloc}")
                    time.sleep(2)
                    self.device.tap_on_screen(quxiaoloc)
                    print('已回到主页')
                    back = False
                else:
                    print("未能找到取消按钮的位置，继续尝试返回。")
            else:
                print("未检测到 '退出主页提醒'，继续按返回键。")
            time.sleep(1)  # 防止过于频繁的按键操作
    def back(self):
        self.device.press_back_button()
        return None

# # 示例使用
# if __name__ == "__main__":
#     # 初始化 AndroidDevice 实例
#     device = AndroidDevice()
#     device.img_path_abs = Path("/path/to/your/base_tool")  # 替换为实际的图片路径
#
#     # 连接设备
#     device.connect_device()
#     if not device.is_device_connected():
#         print(f"无法连接到设备 {device.device_address}。请检查设备是否已启动并连接。")
#         exit()
#
#     # 实例化 BackToMain 类，并传入已有的 device 实例
#     back_to_main = BackToMain(device)
#
#     # 按返回键直到回到主页
#     back_to_main.back_to_main()
