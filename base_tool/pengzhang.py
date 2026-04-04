import cv2
from PIL import Image
import numpy as np
import os
import time

class ImageDilationProcessor:
    def __init__(self, image_array, kernel_size=3):
        """
        初始化图像膨胀处理器。

        :param image_array: 输入图像的NumPy数组。
        :param kernel_size: 膨胀核的大小（必须为正整数，通常为奇数）。
        """
        self.image_array = image_array
        self.kernel_size = kernel_size
        self.processed_image = None

        self._validate_inputs()

    def _validate_inputs(self):
        """
        验证输入参数的有效性。
        """
        if not isinstance(self.image_array, np.ndarray):
            raise TypeError("输入图像必须为NumPy数组。")

        if not isinstance(self.kernel_size, int) or self.kernel_size < 1:
            raise ValueError("膨胀核大小必须为正整数。")

        if self.kernel_size % 2 == 0:
            print(f"膨胀核大小 {self.kernel_size} 不是奇数，将自动加1。")
            self.kernel_size += 1

    def process_image(self, output_path=None):
        """
        应用膨胀操作到图像，并根据需要保存处理后的图像。

        :param output_path: 可选，处理后图像的保存路径。如果指定，将保存图像并返回保存路径。
                            如果未指定，将返回处理后的图像数组。
        :return: 如果指定了output_path，返回保存路径；否则，返回处理后的图像数组。
        """
        if self.image_array is None:
            raise ValueError("输入图像未提供。")

        # 创建膨胀核
        kernel = np.ones((self.kernel_size, self.kernel_size), np.uint8)

        # 应用膨胀操作
        self.processed_image = cv2.dilate(self.image_array, kernel, iterations=1)
        print(f"应用膨胀操作，核大小: {self.kernel_size}")

        if output_path:
            # 确保保存目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.isdir(output_dir):
                try:
                    os.makedirs(output_dir)
                    print(f"已创建输出目录: {output_dir}")
                except Exception as e:
                    raise IOError(f"无法创建输出目录: {output_dir}\n{e}")

            # 转换颜色从 BGR 到 RGB
            img_rgb = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(img_rgb)

            try:
                # 保存图像
                pil_image.save(output_path)
                print(f"处理后的图像已保存到: {output_path}")
                return output_path
            except Exception as e:
                raise IOError(f"无法保存图像到: {output_path}\n{e}")
        else:
            # 返回处理后的图像数组
            return self.processed_image

    def get_processed_image(self):
        """
        获取处理后的图像的NumPy数组。

        :return: 处理后的图像的NumPy数组。
        """
        if self.processed_image is not None:
            return self.processed_image
        else:
            raise ValueError("图像尚未处理。调用 process_image() 方法。")
