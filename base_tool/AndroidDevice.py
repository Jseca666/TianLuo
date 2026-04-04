
from pathlib import Path
# script_path = Path(__file__).resolve().parent
import os
import subprocess
from base_tool.pengzhang import ImageDilationProcessor
from paddleocr import PaddleOCR
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import numpy as np
import cv2
from base_tool.ocr_unit import Uocr
from PIL import Image
from pathlib import Path
import glob
import time
from base_tool.link_head import calculate_distance, merge_close_matches
import json  # 导入 json 模块
from skimage.metrics import structural_similarity as ssim  # 用于计算图片相似度
from base_tool.projection_root import find_project_root
class AndroidDevice:
    def __init__(self, adb_path = r"E:\leidian\LDPlayer9\adb.exe", device_address = "127.0.0.1:5555"):
        self.adb_path = adb_path
        self.device_address = device_address
        self.Cocr = Uocr(1)  # 中文识别器
        self.img_path_abs = ''  # 模板图片的相对路径
        self.screen_capture_path = r"./tool/screen_pic/tmp"
        self.ImageDilationProcessor=None
        # 新增属性，用于存储掩码
        self.mask = None  # 默认的掩码是整个范围（即不遮挡）
        self.masks = {}  # 用于存储 masks.json 中的掩码
        self.lu = find_project_root()
        # 加载 masks.json 文件中的掩码
        if os.path.exists(self.lu /'tool'/'masks.json'):
            with open(self.lu /'tool'/'masks.json', 'r', encoding='utf-8') as f:
                try:
                    self.masks = json.load(f)
                except json.JSONDecodeError:
                    self.masks = {}
        else:
            self.masks = {}

    def create_hsv_mask(self, image, hsv_values, invert=False):
        """
            创建HSV掩模的函数，支持多个HSV范围。
            """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        masks = []
        for hsv_value in hsv_values:
            lower_bound = np.array([hsv_value['lower_h'], hsv_value['lower_s'], hsv_value['lower_v']])
            upper_bound = np.array([hsv_value['upper_h'], hsv_value['upper_s'], hsv_value['upper_v']])
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            masks.append(mask)
        if not masks:
            # 如果没有HSV范围，返回全黑的掩模
            combined_mask = np.zeros(image.shape[:2], dtype=np.uint8)

        else:
            # 将所有掩模通过按位“或”操作合并为一个掩模
            combined_mask = masks[0]
            for mask in masks[1:]:
                combined_mask = cv2.bitwise_or(combined_mask, mask)
            # cv2.imwrite('template_after_mask.png', combined_mask)
            # print(f"Combined Mask Unique Values: {np.unique(combined_mask)}")

        if invert:
            # 如果需要反转掩模，执行按位非操作
            combined_mask = cv2.bitwise_not(combined_mask)
            # 调试信息

        return combined_mask

    def set_mask(self, mask_name):
        """
        设置当前使用的掩码。

        :param mask_name: 掩码的名称
        """
        # print(self.masks)
        if mask_name in self.masks:
            self.mask = self.masks[mask_name]
        else:
            print(f"掩码 '{mask_name}' 未找到，将不使用掩码。")
            self.mask = None

    def connect_device(self):
        connect_command = f'"{self.adb_path}" connect {self.device_address}'
        subprocess.run(connect_command, shell=True)

    def is_device_connected(self):
        devices_command = f'"{self.adb_path}" devices'
        connected_devices = subprocess.check_output(devices_command, shell=True).decode()
        return self.device_address in connected_devices

    def clear_png_files(self, save_dir):
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
            return True
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
        # 打印图像的形状
        # print("图像形状 (Height, Width, Channels):", cropped_image.shape)

        # 打印图像的数据类型
        # print("图像数据类型:", cropped_image.dtype)

        return cropped_image

    def find_image_on_screen(self, template_path, threshold=0.7, mask_name=None, use_color=False):
        template_path = self.img_path_abs / template_path
        print(f"正在查找区域  {template_path}")

        # 截取屏幕并获取图像数据
        screenshot_path = self.capture_screenshot()
        if not screenshot_path:
            print("未能获取截图，请检查设备连接。")
            return [0]

        # 使用 OpenCV 读取截图
        screenshot = cv2.imread(str(screenshot_path))
        if screenshot is None:
            print(f"无法读取截图文件: {screenshot_path}")
            return [0]
        # print(self.masks)
        # print(mask_name)
        # 如果指定了掩码，应用掩码
        if mask_name and mask_name in self.masks:
            mask_data = self.masks[mask_name]
            hsv_values = mask_data['hsv_values']
            invert = mask_data.get('invert', False)
            mask = self.create_hsv_mask(screenshot, hsv_values, invert)
            # 应用掩码
            screenshot = cv2.bitwise_and(screenshot, screenshot, mask=mask)


        elif mask_name:
            print(f"掩码 '{mask_name}' 未找到，将不使用掩码。")
        # 使用 PIL 打开模板图像
        try:
            pil_image = Image.open(template_path).convert('RGB')  # 确保为 RGB 格式
            template = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)  # 转换为 BGR 格式
            # 对模板图也使用掩码
            if mask_name and mask_name in self.masks:
                template_mask = self.create_hsv_mask(template, hsv_values, invert)
                template = cv2.bitwise_and(template, template, mask=template_mask)
            if not use_color:
                template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
        except Exception as e:
            print(f"模板图片 {template_path} 无法读取。错误: {e}")
            return [0]
        # cv2.imwrite('screenshot_after_mask.png', screenshot)
        # cv2.imwrite('template_after_mask.png', template)
        if np.all(template == 0):
            print("模板图像在应用掩码后变为全黑，无法进行匹配。请检查掩码的 HSV 范围。")
            return [0]
        # 根据 use_color 参数处理截图
        if not use_color:
            # 将截图转换为灰度图
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # 检查模板和截图的通道数是否一致
        if template.ndim != screenshot.ndim:
            print("模板和截图的通道数不一致，无法匹配。")
            return [0]

        # 打印图像信息
        # print(f"模板图像尺寸: {template.shape}, 数据类型: {template.dtype}")
        # print(f"截图尺寸: {screenshot.shape}, 数据类型: {screenshot.dtype}")
        # 在应用掩码后，添加以下代码保存图像
        # cv2.imwrite('screenshot_after_mask.png', screenshot)
        # cv2.imwrite('template_after_mask.png', template)
        # 检查模板图像是否为全零（全黑）
        # if np.all(template == 0):
        #     print("模板图像在应用掩码后变为全黑，无法进行匹配。请检查掩码的 HSV 范围。")
        #     return [0]
        # # 检查图像是否为空
        # if template.size == 0 or screenshot.size == 0:
        #     print("模板图像或截图在应用掩码后为空，无法进行匹配。")
        #     return [0]
        #
        # # 检查模板图像是否大于截图
        # if template.shape[0] > screenshot.shape[0] or template.shape[1] > screenshot.shape[1]:
        #     print("模板图像尺寸大于截图尺寸，无法进行匹配。")
        #     return [0]
        # 执行模板匹配
        try:
            res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        except cv2.error as e:
            print(f"模板匹配时发生错误: {e}")
            return [0]

        loc = np.where(res >= threshold)
        if use_color:
            w, h, _ = template.shape
        else:
            w, h = template.shape[::-1]

        matches = []
        for pt in zip(*loc[::-1]):
            matches.append((pt[0] + w // 2, pt[1] + h // 2))
        if not matches:
            print('未找到匹配的坐标')
            matches = [0]
        elif matches and len(matches) != 1:
            matches = merge_close_matches(matches, distance_threshold=20)

        return matches
    def set_img_path_abs(self,img_path_abs):
        print('已将设备类默认读取图像目录更改，使用完记得改回去')
        self.img_path_abs=img_path_abs
    def find_image_in_screenshot(self, screenshot, template_path, threshold=0.7, mask_name=None, use_color=False):
        """
        在给定的截图中查找指定的图像模板。

        :param screenshot: 已读取的截图图像（numpy数组）。
        :param template_path: 模板图像的相对路径。
        :param threshold: 匹配阈值。
        :param mask_name: 要使用的掩码名称。
        :param use_color: 是否使用彩色图进行匹配，默认 False（使用灰度图）。
        :return: 匹配到的位置列表 [(x, y), ...]，如果未找到则返回 [0]。
        """
        template_path = self.img_path_abs / template_path
        print(f"正在查找区域  {template_path}")

        # 复制截图，避免修改原图
        screenshot_copy = screenshot.copy()
        # print('screenshot的形状是',screenshot_copy.shape)
        if screenshot_copy is None:
            print("截图无效。")
            return [0]

        # 如果指定了掩码，应用掩码
        if mask_name and mask_name in self.masks:
            mask_data = self.masks[mask_name]
            hsv_values = mask_data['hsv_values']
            invert = mask_data.get('invert', False)
            mask = self.create_hsv_mask(screenshot_copy, hsv_values, invert)
            # 应用掩码
            screenshot_copy = cv2.bitwise_and(screenshot_copy, screenshot_copy, mask=mask)
            # cv2.imwrite('screenshot_after_mask.png', screenshot_copy)
        elif mask_name:
            print(f"掩码 '{mask_name}' 未找到，将不使用掩码。")

        # 使用 PIL 打开模板图像
        try:
            pil_image = Image.open(template_path).convert('RGB')  # 确保为 RGB 格式
            template = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)  # 转换为 BGR 格式

            # 对模板图也使用掩码
            if mask_name and mask_name in self.masks:
                template_mask = self.create_hsv_mask(template, hsv_values, invert)
                template = cv2.bitwise_and(template, template, mask=template_mask)

            if not use_color:
                template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
        except Exception as e:
            print(f"模板图片 {template_path} 无法读取。错误: {e}")
            return [0]

        # cv2.imwrite('template_after_mask.png', template)
        # 根据 use_color 参数处理截图
        if not use_color:
            # 将截图转换为灰度图
            screenshot_copy = cv2.cvtColor(screenshot_copy, cv2.COLOR_BGR2GRAY)

        # 检查模板和截图的通道数是否一致
        if template.ndim != screenshot_copy.ndim:
            print("模板和截图的通道数不一致，无法匹配。")
            return [0]

        # 检查模板图像是否为全零（全黑）
        if np.all(template == 0):
            print("模板图像在应用掩码后变为全黑，无法进行匹配。请检查掩码的 HSV 范围。")
            return [0]

        # 检查图像是否为空
        if template.size == 0 or screenshot_copy.size == 0:
            print("模板图像或截图在应用掩码后为空，无法进行匹配。")
            return [0]

        # 检查模板图像是否大于截图
        if template.shape[0] > screenshot_copy.shape[0] or template.shape[1] > screenshot_copy.shape[1]:
            print("模板图像尺寸大于截图尺寸，无法进行匹配。")
            return [0]

        # 执行模板匹配
        try:
            res = cv2.matchTemplate(screenshot_copy, template, cv2.TM_CCOEFF_NORMED)
        except cv2.error as e:
            print(f"模板匹配时发生错误: {e}")
            return [0]

        loc = np.where(res >= threshold)
        if use_color:
            w, h, _ = template.shape
        else:
            w, h = template.shape[::-1]

        matches = []
        for pt in zip(*loc[::-1]):
            matches.append((pt[0] + w // 2, pt[1] + h // 2))
        if not matches:
            print('未找到匹配的坐标')
            matches = [0]
        elif matches!=[0] and len(matches) != 1:
            matches = merge_close_matches(matches, distance_threshold=15)
        return matches
    def get_text_from_screen(self, top_left=None, bottom_right=None, mask_name=None,kernel_size=None,flag=1):
        """
        从屏幕上提取文字。

        :param top_left: 可选，截取区域的左上角坐标 (x1, y1)。
        :param bottom_right: 可选，截取区域的右下角坐标 (x2, y2)。
        :param mask_name: 要使用的掩码名称。
        :return: 识别的文字列表。
        """
        if top_left and bottom_right:
            cropped_image = self.local_get(top_left, bottom_right)
        else:
            screenshot_path = self.capture_screenshot()
            cropped_image = cv2.imread(screenshot_path)

        if cropped_image is None:
            print("无法读取截图")
            return None

        # 如果指定了掩码，应用掩码
        # print(13215)
        # print(mask_name)
        if mask_name and mask_name in self.masks:
            # print('1231')
            mask_data = self.masks[mask_name]
            hsv_values = mask_data['hsv_values']
            invert = mask_data['invert']
            mask = self.create_hsv_mask(cropped_image, hsv_values, invert)
            # 应用掩码
            cropped_image = cv2.bitwise_and(cropped_image, cropped_image, mask=mask)
            # cv2.imwrite('cropped_image_after_mask.png', cropped_image)
        elif mask_name:
            print(f"掩码 '{mask_name}' 未找到，将不使用掩码。")
        # cv2.imwrite('template_after_mask.png', template)
        if kernel_size!=None:
            self.ImageDilationProcessor=ImageDilationProcessor(
                image_array=cropped_image,
                kernel_size=kernel_size
            )
            cropped_image=self.ImageDilationProcessor.process_image()
            cropped_image=cv2.bitwise_not(cropped_image)
            # cv2.imwrite('pengcropped_image_after_mask.png', cropped_image)
            if flag==1:
                text = self.Cocr.SHIBIE(cropped_image)
            if flag==0:
                text = self.Cocr.total_shibie(cropped_image)
        else:
            # cv2.imwrite('nopengcropped_image_after_mask.png', cropped_image)
            if flag == 1:
                text = self.Cocr.SHIBIE(cropped_image)
            if flag == 0:
                text = self.Cocr.total_shibie(cropped_image)
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

    def wait_for_image(self, template_path, timeout=15, interval=1, threshold=0.8, mask_name=None, use_color=False):
        """
        等待直到在屏幕上找到指定的图像模板。

        :param template_path: 模板图像的路径。
        :param timeout: 等待超时时间（秒）。
        :param interval: 检查间隔时间（秒）。
        :param threshold: 匹配阈值。
        :param mask_name: 要使用的掩码名称。
        :param use_color: 是否使用彩色图进行匹配，默认 False（使用灰度图）。
        :return: 如果找到则返回匹配位置，否则返回 None。
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            matches = self.find_image_on_screen(template_path, threshold=threshold, mask_name=mask_name, use_color=use_color)
            if matches != [0]:
                matches = merge_close_matches(matches, distance_threshold=20)
                return matches
            time.sleep(interval)

        self.clear_png_files(self.screen_capture_path)
        return [0]

    def wait_for_images(self, template_paths, timeout=10, interval=1, thresholds=0.8,
                        mask_names=None, use_color=False, stop_on_first_match=True,beijinares=None):
        """
        并行等待直到在屏幕上找到指定的图像模板列表中的任意一个。

        :param template_paths: 模板图像路径的列表。
        :param timeout: 等待超时时间（秒）。
        :param interval: 检查间隔时间（秒）。
        :param thresholds: 匹配阈值的列表，或单个值，默认0.8。
        :param mask_names: 掩码名称的列表，或单个值，默认None。
        :param use_color: 是否使用彩色图进行匹配，默认 False（使用灰度图）。
        :param stop_on_first_match: 是否在找到第一个匹配后立即停止，默认 True。
        :return: 如果找到则返回匹配位置和匹配的模板路径，否则返回 [0]。
        """
        # 确保 thresholds 和 mask_names 是列表
        if isinstance(thresholds, (int, float)):
            thresholds = [thresholds] * len(template_paths)
        if mask_names is None or isinstance(mask_names, str):
            mask_names = [mask_names] * len(template_paths)

        start_time = time.time()
        if stop_on_first_match:
            found_event = threading.Event()
        else:
            found_event = None  # 不使用事件
        result = []

        while time.time() - start_time < timeout:
            # 获取截图  # 读取截图
            screenshot_path = self.capture_screenshot()
            # if not screenshot_path:
            #     print("未能获取截图，请检查设备连接。")
            #     return [0]
            if beijinares is not None:

                screenshot=beijinares
            else:
                screenshot = cv2.imread(str(screenshot_path))
                # screenshot = self.local_get([0, 0], [1280, 720])
            if screenshot is None:
                print(f"无法读取截图文件: ")
                return [0]

            with ThreadPoolExecutor(max_workers=len(template_paths)) as executor:
                # futures = []
                futures = {}
                result_list = []
                for i, template_path in enumerate(template_paths):
                    threshold = thresholds[i]
                    mask_name = mask_names[i]
                    # 提交任务
                    if stop_on_first_match:
                        future = executor.submit(
                            self._match_template_thread,
                            screenshot,
                            template_path,
                            threshold,
                            mask_name,
                            use_color,
                            found_event=found_event
                        )
                        # futures.append(executor.submit(
                        #     self._match_template_thread,
                        #     screenshot,
                        #     template_path,
                        #     threshold,
                        #     mask_name,
                        #     use_color,
                        #     found_event=found_event
                        # ))

                    else:
                        future = executor.submit(
                            self._match_template_thread,
                            screenshot,
                            template_path,
                            threshold,
                            mask_name,
                            use_color
                        )
                        # futures.append(executor.submit(
                        #     self._match_template_thread,
                        #     screenshot,
                        #     template_path,
                        #     threshold,
                        #     mask_name,
                        #     use_color
                        # ))
                    futures[future] = {
                        "template_path": template_path,
                        "threshold": threshold,
                        "mask_name": mask_name,
                    }

                if stop_on_first_match:
                    # 等待任意一个任务完成
                    for future in as_completed(futures):
                        match_result = future.result()
                        if match_result != [0]:
                            # 如果找到匹配，设置事件，保存结果
                            params = futures[future]
                            params['results']=match_result
                            result_list.append(params)
                            # print(f"匹配成功的线程参数: {params}")
                            found_event.set()
                            result.extend(match_result)
                            # result.append(match_result)
                            break  # 退出循环
                    if result:
                        print(result)
                        break  # 退出外层循环
                    else:
                        time.sleep(interval)
                else:
                    # 等待所有任务完成，收集所有匹配结果
                    current_results = []
                    for future in as_completed(futures):
                        match_result = future.result()
                        if match_result != [0]:
                            params = futures[future]
                            params['results'] = match_result
                            result_list.append(params)
                            # print(params)
                            # print(f"匹配成功的线程参数: {params}")
                            current_results.extend(match_result)
                            # current_results.append(match_result)
                    if current_results:
                        for i in current_results:
                            if i not in result:

                                result.extend(current_results)

                          # 找到匹配，退出循环
                    else:
                        time.sleep(interval)

        self.clear_png_files(self.screen_capture_path)
        if result_list  == []:
            result_list.append(0)
        if result  == []:
            result.append(0)
        if result !=[0] and result_list!=[0]:
            print('result=',result)

            return result,result_list
        else:
            return [0],[0]
    def _match_template_thread(self, screenshot, template_path, threshold, mask_name, use_color, found_event=None):
        """
        线程函数，在截图中查找模板图像。

        :param screenshot: 已读取的截图图像（numpy数组）。
        :param template_path: 模板图像的相对路径。
        :param threshold: 匹配阈值。
        :param mask_name: 要使用的掩码名称。
        :param use_color: 是否使用彩色图进行匹配。
        :param found_event: 线程间通信的事件对象。
        :return: 匹配到的位置列表 [(x, y), ...]，如果未找到则返回 [0]。
        """
        if found_event is not None:
            if found_event.is_set():
                return [0]  # 已经找到匹配，直接返回


        matches = self.find_image_in_screenshot(screenshot, template_path, threshold=threshold, mask_name=mask_name,
                                                use_color=use_color)
        if matches != [0]:
            return matches
        else:
            return [0]
    def swipe_on_screen(self, start_pos, end_pos, duration=3000):
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


    def get_centra(self, top_left, bottom_right):
        centra = [int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2)]
        return tuple(centra)

    def compare_images(self, image1_path, image2_path, threshold=0.85, mask_name=None, use_color=False):
        """
        比较两张图片是否一致。

        :param image1_path: 第一张图片的路径。
        :param image2_path: 第二张图片的路径。
        :param threshold: 相似度阈值，默认0.85。
        :param mask_name: 要使用的掩码名称。
        :param use_color: 是否使用彩色图进行比较，默认 False（使用灰度图）。
        :return: 如果两张图片相似度 >= threshold，则返回 True，否则返回 False。
        """
        img1=image1_path
        img2=image2_path
        # 读取两张图片
        #
        # img2 = cv2.imread(image2_path)
        #
        if isinstance(image1_path, str):

            img1 = cv2.imread(image1_path)
        if isinstance(image2_path, str):
            img2 = cv2.imread(image2_path)

        if img1 is None:
            print(f"无法读取图片: {image2_path}")
            return False
        if img2 is None:
            print(f"无法读取图片: {image2_path}")
            return False

        # 如果指定了掩码，应用掩码
        if mask_name and mask_name in self.masks:
            mask_data = self.masks[mask_name]
            hsv_values = mask_data['hsv_values']
            invert = mask_data['invert']
            mask1 = self.create_hsv_mask(img1, hsv_values, invert)
            mask2 = self.create_hsv_mask(img2, hsv_values, invert)
            # 应用掩码
            img1 = cv2.bitwise_and(img1, img1, mask=mask1)
            img2 = cv2.bitwise_and(img2, img2, mask=mask2)
        elif mask_name:
            print(f"掩码 '{mask_name}' 未找到，将不使用掩码。")

        # 根据 use_color 参数处理图像
        if not use_color:
            # 将图片转换为灰度图
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # 确保两张图片大小一致
        if img1.shape != img2.shape:
            print("图片尺寸不一致")
            return False

        # 计算相似度
        if use_color:
            similarity = ssim(img1, img2, multichannel=True)
        else:
            similarity = ssim(img1, img2)

        print(f"图片相似度: {similarity}")

        return similarity >= threshold

    def monitor_screenshots(self, interval, duration, mask_name=None, use_color=False,threshold=0.90,test_loc=None):
        """
        在指定时间间隔内对比屏幕截图是否一致。

        :param interval: 截图间隔时间（秒）。
        :param duration: 总监控时间（秒）。
        :param save_dir: 保存截图的目录。
        :param mask_name: 要使用的掩码名称。
        :param use_color: 是否使用彩色图进行比较，默认 False（使用灰度图）。
        :return: 如果在整个监控期间截图一致，则返回 True，否则返回 False。
        """
        save_dir = self.screen_capture_path
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.clear_png_files(save_dir)

        num_checks = int(duration / interval)
        previous_screenshot = None
        for i in range(num_checks):
            screenshot_path = cv2.imread(self.capture_screenshot())
            if test_loc is not None:
                screenshot_path=self.local_get(test_loc[0],test_loc[1])

            if  screenshot_path is None:
                print("未能获取截图，请检查设备连接。")
                return False

            if previous_screenshot is not None:
                are_same = self.compare_images(previous_screenshot, screenshot_path, mask_name=mask_name, use_color=use_color,threshold=threshold)
                if not are_same:
                    print(f"截图在第 {i}与{i + 1} 次对比时不一致。")
                    return False
                else:
                    print(f"第 {i}与{i + 1}  次截图一致。")
            else:
                print("已获取第一张截图。")

            previous_screenshot = screenshot_path
            time.sleep(interval)

        print("所有截图在指定时间间隔内保持一致。")
        return True
# device = AndroidDevice()
# device.connect_device()
#
# # 设置要使用的掩码（假设掩码名为 'example_mask'）
# device.set_mask('绿色小怪的叹号')
# img_file=script_path /'base_tool'#定义好图片的根目录
# device.img_path_abs=img_file
# # 在屏幕上查找图像，使用指定的掩码
# matches = device.find_image_on_screen('location\Zhuangyuan\绿色小怪叹号.png', threshold=0.8, mask_name='绿色小怪的叹号')
#
# # 从屏幕中获取文字，使用指定的掩码
# device.tap_on_screen(matches[0])
# # text = device.get_text_from_screen(mask_name='example_mask')
#
# # 比较两张图片，使用指定的掩码
# # are_same = device.compare_images('image1.png', 'image2.png', threshold=0.9, mask_name='example_mask')
# dd=AndroidDevice(device_address='127.0.0.1:5558')
# dd.connect_device()