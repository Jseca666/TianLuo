import os
import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt


def create_hsv_mask(image, hsv_values, invert=False):
    # 与之前相同
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

    for hsv_range in hsv_values:
        lower_bound = np.array([hsv_range['lower_h'], hsv_range['lower_s'], hsv_range['lower_v']])
        upper_bound = np.array([hsv_range['upper_h'], hsv_range['upper_s'], hsv_range['upper_v']])
        current_mask = cv2.inRange(hsv, lower_bound, upper_bound)
        mask = cv2.bitwise_or(mask, current_mask)

    if invert:
        mask = cv2.bitwise_not(mask)

    return mask


def verify_mask(mask):
    # 与之前相同
    unique_values = np.unique(mask)
    print(f"掩码中的唯一像素值: {unique_values}")
    print(f"掩码的数据类型: {mask.dtype}")
    if mask.dtype != np.uint8:
        print("警告: 掩码的类型不是 uint8。")
    if not np.array_equal(unique_values, [0, 255]):
        print("警告: 掩码中存在非二值像素值。")
    else:
        print("掩码验证通过。")


def show_image(title, image):
    """
    使用 Matplotlib 显示图像。

    :param title: 图像标题。
    :param image: 要显示的图像（BGR 格式）。
    """
    if len(image.shape) == 3 and image.shape[2] == 3:
        # 转换为 RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(8, 6))
    if len(image.shape) == 2:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(image)
    plt.title(title)
    plt.axis('off')
    plt.show()


def segment_digits(input_dir, output_dir, display=False):
    """
    处理输入目录中的图像，应用掩码，分割数字，并将结果保存到输出目录。

    :param input_dir: 输入图像目录路径。
    :param output_dir: 输出图像目录路径。
    :param display: 是否在处理过程中显示图像。
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 创建用于保存中间结果的子目录
    mask_dir = output_dir / "masks"
    contour_dir = output_dir / "contours"
    visualization_dir = output_dir / "visualizations"

    for directory in [mask_dir, contour_dir, visualization_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    # 定义HSV掩码参数
    mask_config = {
        'hsv_values': [
            {
                "lower_h": 0,
                "lower_s": 0,
                "lower_v": 150,  # 调整亮度下限
                "upper_h": 10,
                "upper_s": 100,  # 调整饱和度上限
                "upper_v": 255
            }
        ],
        'invert': False
    }

    # 检查 OpenCV 版本
    opencv_version = cv2.__version__
    print(f"OpenCV 版本: {opencv_version}")
    major_version = int(opencv_version.split('.')[0])

    # 遍历输入目录中的所有图片文件
    for filepath in input_dir.iterdir():
        if filepath.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp']:
            try:
                print(f"\n处理文件: {filepath.name}")

                # 使用 PIL 读取图像并转换为 BGR 格式
                pil_image = Image.open(filepath).convert('RGB')  # 确保为 RGB 格式
                img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)  # 转换为 BGR 格式

                if img is None:
                    print(f"无法读取 {filepath}")
                    continue

                # 创建掩码
                mask = create_hsv_mask(img, mask_config['hsv_values'], mask_config['invert'])

                # 强制二值化
                _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

                # 验证掩码
                verify_mask(mask)

                # 可选：膨胀以确保连通性
                kernel = np.ones((3, 3), np.uint8)
                mask = cv2.dilate(mask, kernel, iterations=1)

                # 保存原始掩码
                mask_output_path = mask_dir / filepath.name
                cv2.imwrite(str(mask_output_path), mask)

                # 输出掩码中非零像素的数量
                non_zero = cv2.countNonZero(mask)
                print(f"{filepath.name}: 掩码中非零像素数量 = {non_zero}")

                # 可视化掩码覆盖
                visualization = img.copy()

                # 创建一个红色遮罩
                red_overlay = np.zeros_like(img, dtype=np.uint8)
                red_overlay[:] = (0, 0, 255)  # BGR 中的红色

                # 将红色遮罩与原图加权叠加，仅在掩码区域
                alpha = 0.3  # 红色遮罩的透明度
                visualization[mask > 0] = cv2.addWeighted(red_overlay, alpha, visualization, 1 - alpha, 0)[mask > 0]

                # 保存可视化图像
                visualization_output_path = visualization_dir / filepath.name
                cv2.imwrite(str(visualization_output_path), visualization)

                # 使用 Matplotlib 显示图像（可选）
                if display:
                    show_image('Mask', mask)
                    show_image('Visualization', visualization)
                    print("查看图像。关闭 Matplotlib 窗口继续...")
                    # Matplotlib 会自动 wait for key presses when showing, no need for additional waitKey()

                # 查找掩码中的轮廓
                if major_version >= 4:
                    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                else:
                    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                print(f"找到 {len(contours)} 个轮廓。")

                if contours:
                    # 假设数字是最大的轮廓
                    largest_contour = max(contours, key=cv2.contourArea)
                    x, y, w, h = cv2.boundingRect(largest_contour)

                    # 裁剪原始图像到数字区域
                    cropped_img = img[y:y + h, x:x + w]

                    # 保存裁剪后的图像
                    cropped_output_path = output_dir / filepath.name
                    cv2.imwrite(str(cropped_output_path), cropped_img)

                    # 绘制轮廓并保存
                    contour_img = img.copy()
                    cv2.drawContours(contour_img, [largest_contour], -1, (0, 255, 0), 2)  # 绿色轮廓
                    contour_output_path = contour_dir / filepath.name
                    cv2.imwrite(str(contour_output_path), contour_img)

                    print(f"已保存裁剪图像和轮廓图像。")
                else:
                    print(f"在 {filepath.name} 中未找到轮廓")

            except Exception as e:
                print(f"处理文件 {filepath.name} 时出错：{e}")


if __name__ == "__main__":
    input_dir = r"D:\py_project\longzu\tool\location\numbers"  # 替换为实际的输入目录路径
    output_dir = r"D:\py_project\longzu\tool\location\processed_numbers"  # 替换为实际的输出目录路径
    segment_digits(input_dir, output_dir, display=False)  # 设置 display=True 使用 Matplotlib 显示图像
