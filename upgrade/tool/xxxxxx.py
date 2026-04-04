import os
import subprocess
from datetime import datetime
import numpy as np
import cv2
from base_tool.ocr_unit import Uocr
from PIL import Image
from pathlib import Path
import glob
import time
from base_tool.link_head import calculate_distance,merge_close_matches
class AndroidDevice:
    def __init__(self, adb_path = r"E:\leidian\LDPlayer9\adb.exe", device_address = "127.0.0.1:5555"):
        self.adb_path = adb_path
        self.device_address = device_address
        self.Cocr=Uocr(1)#中文识别器
        self.img_path_abs=''#模板图片的相对路径
        self.screen_capture_path=r"D:\py_project\crawl_novel-main\screen_pic\tmp"
    def connect_device(self):
        connect_command = f'"{self.adb_path}" connect {self.device_address}'
        subprocess.run(connect_command, shell=True)
    def is_device_connected(self):
        devices_command = f'"{self.adb_path}" devices'
        connected_devices = subprocess.check_output(devices_command, shell=True).decode()
        return self.device_address in connected_devices
    def clear_png_files(self,save_dir):
        """
        清除指定目录下所有 .png 图片文件

        :param save_dir: 需要清除 .png 文件的目录
        """
        # 构建 .png 文件的路径模式
        png_files = glob.glob(os.path.join(save_dir, "*.png"))

        # 遍历并删除所有的 .png 文件
        for file_path in png_files:
            try:
                os.remove(file_path)
                # print(f"已删除文件: {file_path}")
            except Exception as e:
                print(f"删除文件 {file_path} 时出错: {e}")
    def capture_screenshot(self):
        # 确保保存目录存在
        if not os.path.exists(self.screen_capture_path):
            os.makedirs(self.screen_capture_path)
        # self.clear_png_files(save_dir)
        # 生成以当前时间命名的文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_filename = f"{timestamp}.png"
        screenshot_path = os.path.join(self.screen_capture_path, screenshot_filename)

        if self.is_device_connected():
            # 直接获取截图数据并保存
            screenshot_command = f'"{self.adb_path}" -s {self.device_address} exec-out screencap -p'
            result = subprocess.run(screenshot_command, shell=True, stdout=subprocess.PIPE)

            # 将数据保存为文件
            with open(screenshot_path, 'wb') as f:
                f.write(result.stdout)

            #print(f"Screenshot saved as {screenshot_path}")
            return screenshot_path
        else:
            #print(f"Device {self.device_address} not connected.")
            return None
    def press_back_button(self):
        if self.is_device_connected():
            back_command = f'"{self.adb_path}" -s {self.device_address} shell input keyevent 4'
            subprocess.run(back_command, shell=True)
            #print("Back button pressed.")
        else:
            #print(f"Device {self.device_address} not connected.")
            return None
    def tap_on_screen(self, aimd):
        if self.is_device_connected() and aimd != 0:
            # 点击屏幕上的指定坐标
            tap_command = f'"{self.adb_path}" -s {self.device_address} shell input tap {aimd[0]} {aimd[1]}'
            subprocess.run(tap_command, shell=True)
            #print(f"Tapped on screen at ({aimd[0]}, {aimd[1]})")
        else:
            print(f"Device {self.device_address} 无法链接或者点击位置坐标缺失.")
            return False
    def local_get(self, top_left, bottom_right):
        """
        截取屏幕并提取指定区域。

        :param top_left: 区域的左上角坐标 (x1, y1)。
        :param bottom_right: 区域的右下角坐标 (x2, y2)。
        :return: 裁剪出的图像区域。
        """
        # 截取屏幕
        screenshot_path = self.capture_screenshot()

        # 读取截图
        screenshot = cv2.imread(screenshot_path)

        # 确保截图成功
        if screenshot is None:
            raise ValueError("Failed to capture screenshot")

        # 提取指定区域
        x1, y1 = top_left
        x2, y2 = bottom_right
        cropped_image = screenshot[y1:y2, x1:x2]
        return cropped_image
    def find_image_on_screen(self, template_path, threshold=0.7):
        """
        在最新的屏幕截图中查找指定的图像模板。

        :param template_path: 模板图像的相对路径。
        :param threshold: 匹配阈值。
        :return: 匹配到的位置列表 [(x, y), ...]，如果未找到则为空列表。
        """
        template_path=self.img_path_abs/template_path
        print(f"正在查找区域  {template_path}")
        # 构建截图保存目录
        # save_dir = Path(__file__).resolve().parent / 'screen_pic' / 'tmp'
        screenshot_path = self.capture_screenshot()
        if not screenshot_path:
            print("未能获取截图，请检查设备连接。")
            return [0]

        # 使用 OpenCV 读取截图
        screenshot = cv2.imread(str(screenshot_path))
        if screenshot is None:
            print(f"无法读取截图文件: {screenshot_path}")
            return [0]

        # 使用 PIL 打开模板图像
        try:
            pil_image = Image.open(template_path).convert('RGB')  # 确保为 RGB 格式
            template = np.array(pil_image)
            template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)  # 转换为灰度图
        except Exception as e:
            print(f"模板图片 {template_path} 无法读取。错误: {e}")
            return [0]

        # 将截图转换为灰度图
        gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # 执行模板匹配
        res = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        w, h = template.shape[::-1]

        matches = []
        for pt in zip(*loc[::-1]):
            matches.append((pt[0] + w // 2, pt[1] + h // 2))
        if matches == []:
            print('未找到匹配的坐标')
            matches=[0]
        elif matches !=[0] and len(matches)!=1:
            matches = merge_close_matches(matches, distance_threshold=10)

        return matches
    def get_text_from_screen(self, top_left=None, bottom_right=None):
        """
        从屏幕上提取文字。

        :param top_left: 可选，截取区域的左上角坐标 (x1, y1)。
        :param bottom_right: 可选，截取区域的右下角坐标 (x2, y2)。
        :return: 识别的文字列表。
        """
        if top_left and bottom_right:
            print(1)
            cropped_image = self.local_get(top_left, bottom_right)
            text = self.Cocr.SHIBIE(cropped_image)
        else:
            screenshot_path = self.capture_screenshot()
            text = self.Cocr.SHIBIE(screenshot_path)
        return text
    def launch_app(self, package_name, activity=None):
        """
        启动设备上的应用。

        :param package_name: 应用的包名（如 'com.example.game'）。
        :param activity: 启动的 Activity（可选）。
        """
        if self.is_device_connected():
            if activity:
                launch_command = f'"{self.adb_path}" -s {self.device_address} shell am start -n {package_name}/{activity}'
            else:
                launch_command = f'"{self.adb_path}" -s {self.device_address} shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1'
            subprocess.run(launch_command, shell=True)
            #print(f"App {package_name} launched.")
        else:
            print(f"Device {self.device_address} not connected.")
    def stop_app(self, package_name):
        """
        停止设备上的应用。

        :param package_name: 应用的包名（如 'com.example.game'）。
        """
        if self.is_device_connected():
            stop_command = f'"{self.adb_path}" -s {self.device_address} shell am force-stop {package_name}'
            subprocess.run(stop_command, shell=True)
            #print(f"App {package_name} stopped.")
        else:
            print(f"Device {self.device_address} not connected.")
    def get_current_activity(self):
        """
        获取设备上当前活跃的 Activity。

        :return: 活跃的 Activity 名称。
        """
        if self.is_device_connected():
            activity_command = f'"{self.adb_path}" -s {self.device_address} shell dumpsys window windows | grep -E "mCurrentFocus"'
            activity_output = subprocess.check_output(activity_command, shell=True).decode().strip()
            return activity_output
        else:
            print(f"Device {self.device_address} not connected.")
            return None
    def wait_for_image(self, template_path, timeout=30, interval=1, threshold=0.8):
        """
        等待直到在屏幕上找到指定的图像模板。

        :param template_path: 模板图像的路径。
        :param timeout: 等待超时时间（秒）。
        :param interval: 检查间隔时间（秒）。
        :param threshold: 匹配阈值。
        :return: 如果找到则返回匹配位置，否则返回 None。
        """
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            matches = self.find_image_on_screen(template_path)
            if matches!=[0]:
                return matches
            time.sleep(interval)

        return [0]
    def swipe_on_screen(self, start_pos, end_pos, duration=500):
        """
        在屏幕上执行滑动操作。

        :param start_pos: 滑动起始坐标 (x1, y1)。
        :param end_pos: 滑动结束坐标 (x2, y2)。
        :param duration: 滑动持续时间，单位毫秒。
        """
        if self.is_device_connected():
            swipe_command = f'"{self.adb_path}" -s {self.device_address} shell input swipe {start_pos[0]} {start_pos[1]} {end_pos[0]} {end_pos[1]} {duration}'
            subprocess.run(swipe_command, shell=True)
            #print(f"Swiped from {start_pos} to {end_pos} over {duration}ms")
        else:
            print(f"Device {self.device_address} not connected.")
    def get_centra(self,top_left,bottom_right):
        centra=[int((top_left[0]+bottom_right[0])/2),int((top_left[1]+bottom_right[1])/2)]
        return tuple(centra)
    def compare_images(self, image1_path, image2_path, threshold=0.85):
        """
        比较两张图片是否一致。

        :param image1_path: 第一张图片的路径。
        :param image2_path: 第二张图片的路径。
        :param threshold: 相似度阈值，默认0.99。
        :return: 如果两张图片相似度 >= threshold，则返回 True，否则返回 False。
        """
        # 读取两张图片
        img1 = cv2.imread(image1_path)
        img2 = cv2.imread(image2_path)

        if img1 is None:
            print(f"无法读取图片: {image1_path}")
            return False
        if img2 is None:
            print(f"无法读取图片: {image2_path}")
            return False

        # 将图片转换为灰度图
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # 确保两张图片大小一致
        if gray1.shape != gray2.shape:
            print("图片尺寸不一致")
            return False

        # 计算结构相似性指数（SSIM）
        from skimage.metrics import structural_similarity as ssim
        similarity, _ = ssim(gray1, gray2, full=True)

        print(f"图片相似度: {similarity}")

        return similarity >= threshold
    def monitor_screenshots(self, interval, duration, save_dir=r"D:\py_project\crawl_novel-main\tool\screen_pic\tmp"):
        """
        在指定时间间隔内对比屏幕截图是否一致。

        :param interval: 截图间隔时间（秒）。
        :param duration: 总监控时间（秒）。
        :param save_dir: 保存截图的目录。
        :return: 如果在整个监控期间截图一致，则返回 True，否则返回 False。
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.clear_png_files(save_dir)

        num_checks = int(duration / interval)
        previous_screenshot = None

        for i in range(num_checks):
            screenshot_path = self.capture_screenshot()
            if not screenshot_path:
                print("未能获取截图，请检查设备连接。")
                return False

            if previous_screenshot:
                are_same = self.compare_images(previous_screenshot, screenshot_path)
                if not are_same:
                    print(f"截图在第 {i + 1} 次对比时不一致。")
                    return False
                else:
                    print(f"第 {i + 1} 次截图一致。")
            else:
                print("已获取第一张截图。")

            previous_screenshot = screenshot_path
            time.sleep(interval)

        print("所有截图在指定时间间隔内保持一致。")
        return True
# 使用示例


# save_dir = r"screen_pic/tmp"
#
# # 创建 AndroidDevice 实例
# device = AndroidDevice()
#
# # 连接设备
# device.connect_device()
#
# # 截取屏幕并保存
# screenshot_path = device.capture_screenshot()
# device.press_back_button()
#time_down=(452, 293)
# 在屏幕指定坐标点击 (例如: x=500, y=800)
#device.tap_on_screen(time_down[0], time_down[1])
#roi=device.local_get((451, 186),(498, 257))
# 使用PaddleOCR进行OCR识别
#result =Nocr.SHIBIE(roi)
