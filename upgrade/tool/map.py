import os
import subprocess
from datetime import datetime
import numpy as np
import cv2
import torch
from transformers import SegformerForSemanticSegmentation, SegformerImageProcessor
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib

class AndroidDevice:
    def __init__(self, adb_path=r"E:\leidian\LDPlayer9\adb.exe", device_address="127.0.0.1:5555"):
        self.adb_path = adb_path
        self.device_address = device_address
        self.img_path_abs = ''

    def connect_device(self):
        connect_command = f'"{self.adb_path}" connect {self.device_address}'
        subprocess.run(connect_command, shell=True)

    def is_device_connected(self):
        devices_command = f'"{self.adb_path}" devices'
        connected_devices = subprocess.check_output(devices_command, shell=True).decode()
        return self.device_address in connected_devices

    def capture_screenshot(self, save_dir=r"D:\py_project\crawl_novel-main\screen_pic\tmp"):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        screenshot_filename = f"{timestamp}.png"
        screenshot_path = os.path.join(save_dir, screenshot_filename)

        if self.is_device_connected():
            screenshot_command = f'"{self.adb_path}" -s {self.device_address} exec-out screencap -p'
            result = subprocess.run(screenshot_command, shell=True, stdout=subprocess.PIPE)
            with open(screenshot_path, 'wb') as f:
                f.write(result.stdout)
            return screenshot_path
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
            feature_extractor = SegformerImageProcessor.from_pretrained(model_name)
            model = SegformerForSemanticSegmentation.from_pretrained(model_name)
            model.eval()

            # 获取类别标签
            # Cityscapes 数据集的类别
            labels = [
                'road', 'sidewalk', 'building', 'wall', 'fence', 'pole', 'traffic light',
                'traffic sign', 'vegetation', 'terrain', 'sky', 'person', 'rider',
                'car', 'truck', 'bus', 'train', 'motorcycle', 'bicycle'
            ]
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

    def capture_and_identify_walkable_areas(self):
        """
        截取屏幕并识别可行走区域。
        """
        if not self.is_device_connected():
            print(f"设备 {self.device_address} 未连接。")
            return

        screenshot_path = self.capture_screenshot(save_dir=self.screenshot_dir)
        if screenshot_path:
            # 识别可行走区域
            walkable_area = self.identify_walkable_areas(
                image_path=screenshot_path,
                output_path=screenshot_path.replace(".png", "_walkable.png")
            )
            # 显示结果
            if walkable_area is not None:
                plt.figure(figsize=(15, 7))
                plt.subplot(1, 2, 1)
                plt.title("原始图像")
                img = Image.open(screenshot_path)
                plt.imshow(img)
                plt.axis('off')

                plt.subplot(1, 2, 2)
                plt.title("可行走区域")
                plt.imshow(walkable_area)
                plt.axis('off')

                plt.show()

    def identify_walkable_areas(self, image_path, output_path=None):
        """
        使用Segformer模型识别给定图像中的可行走区域。

        :param image_path: 输入图像的路径
        :param output_path: 可选，保存分割结果的路径
        :return: 分割后的图像
        """
        # 读取图像
        image = Image.open(image_path).convert("RGB")
        original_size = image.size  # (width, height)

        # 预处理
        inputs = self.feature_extractor(images=image, return_tensors="pt")

        # 使用GPU加速
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # 推断
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits  # [1, num_classes, H, W]
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

if __name__ == "__main__":
    # 创建 MapReconstructorDevice 实例
    device = MapReconstructorDevice()

    # 连接设备
    device.connect_device()

    # 截取屏幕并识别可行走区域
    device.capture_and_identify_walkable_areas()
