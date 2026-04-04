import os
import json
import subprocess
from datetime import datetime
import numpy as np
import cv2
import torch
from transformers import SegformerForSemanticSegmentation, AutoImageProcessor
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib


def create_hsv_mask(image, lower_h, lower_s, lower_v, upper_h, upper_s, upper_v, invert=False):
    """
    创建HSV掩模的函数。

    参数：
    - image: 输入的BGR图像（numpy数组）
    - lower_h, lower_s, lower_v: HSV的下限值
    - upper_h, upper_s, upper_v: HSV的上限值
    - invert: 是否反转掩模（默认为False）

    返回：
    - mask: 生成的掩模图像
    """
    # 转换图像为HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义HSV的上下限
    lower_bound = np.array([lower_h, lower_s, lower_v])
    upper_bound = np.array([upper_h, upper_s, upper_v])

    # 创建掩模
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # 如果invert标志为True，则反转掩模
    if invert:
        mask = cv2.bitwise_not(mask)

    return mask


def load_hsv_config(config_path='masks.json'):
    """
    从配置文件加载所有命名的HSV范围值。

    参数：
    - config_path: 配置文件路径

    返回：
    - configs: 包含多个命名HSV范围的字典
    """
    if not os.path.exists(config_path):
        print(f"配置文件不存在: {config_path}")
        return {}

    with open(config_path, 'r', encoding='utf-8') as f:
        configs = json.load(f)
    print(f"从 {config_path} 加载HSV配置: {list(configs.keys())}")
    return configs


def apply_hsv_masks(image, configs):
    """
    应用多个HSV掩模到图像上。

    参数：
    - image: 输入的PIL图像
    - configs: 包含多个命名HSV范围的字典

    返回：
    - masked_image: 应用掩模后的PIL图像
    - combined_mask: 合并后的掩模图像（用于可视化）
    """
    # 将PIL图像转换为OpenCV BGR格式
    image_np = np.array(image)
    image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    combined_mask = np.zeros(image_np.shape[:2], dtype=np.uint8)

    for mask_name, config in configs.items():
        hsv_values = config.get('hsv_values', {})
        invert = config.get('invert', False)

        if not hsv_values:
            print(f"掩模 '{mask_name}' 缺少 'hsv_values' 配置，跳过。")
            continue

        mask = create_hsv_mask(
            image_np,
            hsv_values.get('lower_h', 0),
            hsv_values.get('lower_s', 0),
            hsv_values.get('lower_v', 0),
            hsv_values.get('upper_h', 179),
            hsv_values.get('upper_s', 255),
            hsv_values.get('upper_v', 255),
            invert
        )
        combined_mask = cv2.bitwise_or(combined_mask, mask)
        print(f"应用掩模: {mask_name}")

    # 应用合并后的掩模
    masked_img = image_np.copy()
    masked_img[combined_mask == 255] = 0  # 将掩模区域设为黑色

    # 转换回PIL图像
    masked_image = Image.fromarray(cv2.cvtColor(masked_img, cv2.COLOR_BGR2RGB))
    combined_mask_color = cv2.cvtColor(combined_mask, cv2.COLOR_GRAY2BGR)

    return masked_image, combined_mask


class AndroidDevice:
    def __init__(self, adb_path=r"E:\leidian\LDPlayer9\adb.exe", device_address="127.0.0.1:5555"):
        self.adb_path = adb_path
        self.device_address = device_address
        self.img_path_abs = ''

    def connect_device(self):
        connect_command = f'"{self.adb_path}" connect {self.device_address}'
        subprocess.run(connect_command, shell=True)
        print(f"尝试连接到设备 {self.device_address} ...")

    def is_device_connected(self):
        devices_command = f'"{self.adb_path}" devices'
        connected_devices = subprocess.check_output(devices_command, shell=True).decode()
        is_connected = self.device_address in connected_devices
        print(f"设备 {self.device_address} 连接状态: {is_connected}")
        return is_connected

    def capture_screenshot(self, save_dir=r"D:\py_project\crawl_novel-main\screen_pic\tmp"):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        screenshot_filename = f"screenshot_{timestamp}.png"
        screenshot_path = os.path.join(save_dir, screenshot_filename)

        if self.is_device_connected():
            try:
                screenshot_command = f'"{self.adb_path}" -s {self.device_address} exec-out screencap -p'
                result = subprocess.run(screenshot_command, shell=True, stdout=subprocess.PIPE)
                with open(screenshot_path, 'wb') as f:
                    f.write(result.stdout)
                print(f"屏幕截图已保存到 {screenshot_path}")
                return screenshot_path
            except Exception as e:
                print(f"截取屏幕截图时出错: {e}")
                return None
        else:
            print(f"设备 {self.device_address} 未连接。")
            return None


class MapReconstructorDevice(AndroidDevice):
    def __init__(self, adb_path=r"E:\leidian\LDPlayer9\adb.exe", device_address="127.0.0.1:5555"):
        super().__init__(adb_path, device_address)
        self.screenshot_dir = r"D:\py_project\crawl_novel-main\screen_pic\tmp"
        self.model, self.feature_extractor, self.labels = self.load_segformer_model()
        self.setup_matplotlib_font()

    def load_segformer_model(self):
        """
        加载预训练的Segformer模型，适用于Cityscapes数据集。
        """
        try:
            # 使用Hugging Face的Segformer模型
            model_name = "nvidia/segformer-b5-finetuned-cityscapes-1024-1024"
            feature_extractor = AutoImageProcessor.from_pretrained(model_name)  # 使用 AutoImageProcessor
            model = SegformerForSemanticSegmentation.from_pretrained(model_name)
            model.eval()

            # 获取类别标签
            # Cityscapes 数据集的类别
            labels = [
                'road', 'sidewalk', 'building', 'wall', 'fence', 'pole', 'traffic light',
                'traffic sign', 'vegetation', 'terrain', 'sky', 'person', 'rider',
                'car', 'truck', 'bus', 'train', 'motorcycle', 'bicycle'
            ]

            # 移动模型到设备
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)

            print("Segformer模型加载成功。")
            return model, feature_extractor, labels
        except Exception as e:
            print("加载Segformer模型失败。")
            raise e

    def setup_matplotlib_font(self):
        """
        设置Matplotlib字体以支持CJK字符。
        """
        try:
            # 尝试使用SimHei字体
            matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
            matplotlib.rcParams['axes.unicode_minus'] = False
        except Exception as e:
            print("设置Matplotlib字体失败。")
            raise e

    def capture_and_identify_walkable_areas(self, config_path='masks.json'):
        """
        截取屏幕并识别可行走区域。

        参数：
        - config_path: HSV配置文件路径
        """
        self.connect_device()
        screenshot_path = self.capture_screenshot(save_dir=self.screenshot_dir)
        if screenshot_path:
            # 读取图像
            image = Image.open(screenshot_path).convert("RGB")

            # 加载HSV配置
            configs = load_hsv_config(config_path)
            if not configs:
                print("未加载到任何HSV配置，跳过掩模应用。")
                masked_image = image
            else:
                # 应用HSV掩模
                masked_image, combined_mask = apply_hsv_masks(image, configs)

                # 保存掩模后的图像（可选）
                masked_screenshot_path = screenshot_path.replace(".png", "_masked.png")
                masked_image.save(masked_screenshot_path)
                print(f"应用 HSV mask 后的图像已保存到 {masked_screenshot_path}")

            # 使用掩模后的图像进行语义分割
            walkable_area = self.identify_walkable_areas(
                image_path=masked_screenshot_path if configs else screenshot_path,
                output_path=screenshot_path.replace(".png", "_walkable.png")
            )

            # 显示结果
            if walkable_area is not None:
                plt.figure(figsize=(15, 7))
                plt.subplot(1, 2, 1)
                plt.title("原始图像")
                plt.imshow(image)
                plt.axis('off')

                plt.subplot(1, 2, 2)
                plt.title("可行走区域")
                plt.imshow(walkable_area)
                plt.axis('off')

                plt.show()

    def identify_walkable_areas(self, image_path, output_path=None):
        """
        使用Segformer模型识别给定图像中的可行走区域。

        参数：
        - image_path: 输入图像的路径
        - output_path: 可选，保存分割结果的路径

        返回：
        - 分割后的图像
        """
        try:
            # 读取图像
            image = Image.open(image_path).convert("RGB")
            original_size = image.size  # (width, height)

            # 预处理
            inputs = self.feature_extractor(images=image, return_tensors="pt")
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(device)
            inputs = {k: v.to(device) for k, v in inputs.items()}

            # 推断
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits  # [batch_size, num_classes, H, W]
                predicted_segmentation = logits.argmax(dim=1)[0].cpu().numpy()  # [H, W]

            # 定义可行走区域的类别
            # 根据Cityscapes数据集，常见的可行走区域类别包括：road, sidewalk, terrain
            walkable_classes = ['road', 'sidewalk', 'terrain']

            # 获取对应的类别索引
            walkable_indices = [self.labels.index(cls) for cls in walkable_classes if cls in self.labels]
            print(f"可行走区域类别索引: {walkable_indices}")

            # 创建掩模
            walkable_mask = np.isin(predicted_segmentation, walkable_indices)

            if not np.any(walkable_mask):
                print("未检测到可行走区域。")
                return None

            # 将掩模调整回原始图像尺寸
            walkable_mask_resized = cv2.resize(walkable_mask.astype(np.uint8), original_size, interpolation=cv2.INTER_NEAREST)
            walkable_mask_resized = walkable_mask_resized.astype(bool)

            # 可选：进行形态学操作以去除噪点
            kernel = np.ones((5, 5), np.uint8)
            walkable_mask_resized = cv2.morphologyEx(walkable_mask_resized.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
            walkable_mask_resized = cv2.morphologyEx(walkable_mask_resized, cv2.MORPH_OPEN, kernel)
            walkable_mask_resized = walkable_mask_resized.astype(bool)

            # 将掩模应用到原始图像
            img_np = np.array(image)
            walkable_area = np.zeros_like(img_np)
            walkable_area[walkable_mask_resized] = img_np[walkable_mask_resized]

            # 如果指定了输出路径，保存结果
            if output_path:
                walkable_image = Image.fromarray(walkable_area)
                walkable_image.save(output_path)
                print(f"分割结果已保存到 {output_path}")

            return walkable_area

        except Exception as e:
            print("SegFormer语义分割过程中出错。")
            print(e)
            return None


def main():
    # 创建 MapReconstructorDevice 实例
    device = MapReconstructorDevice()

    # 捕获截图并进行语义分割
    device.capture_and_identify_walkable_areas(config_path='../tool/masks.json')


if __name__ == "__main__":
    main()
