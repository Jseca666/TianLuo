import cv2
import numpy as np

def create_rich_color_test_image():
    """
    创建一张包含丰富颜色的测试图像，包括不同色调的红色、黄色、蓝色、绿色以及渐变区域。
    """
    # 定义图像尺寸
    height, width = 400, 800
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # 每个色块的宽度
    block_width = width // 8

    # 创建不同色调的色块
    # 黄色色块
    image[0:height//2, 0:block_width] = (0, 255, 255)        # 标准黄色
    image[0:height//2, block_width:2*block_width] = (0, 200, 200)  # 浅黄色
    image[0:height//2, 2*block_width:3*block_width] = (0, 150, 150)  # 更浅黄色

    # 红色色块
    image[height//2:height, 0:block_width] = (0, 0, 255)        # 标准红色
    image[height//2:height, block_width:2*block_width] = (0, 0, 200)  # 深红色
    image[height//2:height, 2*block_width:3*block_width] = (0, 0, 150)  # 更深红色

    # 绿色色块
    image[0:height//2, 3*block_width:4*block_width] = (0, 255, 0)        # 标准绿色
    image[0:height//2, 4*block_width:5*block_width] = (0, 200, 0)        # 浅绿色
    image[0:height//2, 5*block_width:6*block_width] = (0, 150, 0)        # 更浅绿色

    # 蓝色色块
    image[height//2:height, 3*block_width:4*block_width] = (255, 0, 0)        # 标准蓝色
    image[height//2:height, 4*block_width:5*block_width] = (200, 0, 0)        # 深蓝色
    image[height//2:height, 5*block_width:6*block_width] = (150, 0, 0)        # 更深蓝色

    # 添加一些杂色部分
    cv2.rectangle(image, (6*block_width, 0), (7*block_width, height//2), (150, 100, 50), -1)  # 棕色
    cv2.rectangle(image, (7*block_width, 0), (8*block_width, height//2), (100, 150, 200), -1)  # 淡蓝色
    cv2.rectangle(image, (6*block_width, height//2), (7*block_width, height), (50, 100, 150), -1)  # 淡灰蓝色
    cv2.rectangle(image, (7*block_width, height//2), (8*block_width, height), (50, 150, 50), -1)  # 灰绿色

    return image

def main():
    # 创建丰富的测试图像
    image = create_rich_color_test_image()

    # 显示生成的测试图像
    cv2.imshow("Rich Color Test Image", image)

    # 将图像从 BGR 转换为 HSV 颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义黄色的 HSV 范围
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # 定义红色的 HSV 范围 (红色在HSV中有两段)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # 创建黄色的掩码
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

    # 创建红色的掩码（两段红色）
    red_mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    # 对黄色和红色掩码取并集
    combined_mask = cv2.bitwise_or(yellow_mask, red_mask)

    # 对黄色和红色掩码取交集
    intersection_mask = cv2.bitwise_and(yellow_mask, red_mask)

    # 使用并集掩码提取黄色和红色区域
    result_combined = cv2.bitwise_and(image, image, mask=combined_mask)

    # 使用交集掩码提取交集区域（交集可能为空）
    result_intersection = cv2.bitwise_and(image, image, mask=intersection_mask)

    # 显示掩码和结果
    cv2.imshow("Yellow Mask", yellow_mask)
    cv2.imshow("Red Mask", red_mask)
    cv2.imshow("Combined Mask (Yellow + Red)", combined_mask)
    cv2.imshow("Intersection Mask (Yellow AND Red)", intersection_mask)
    cv2.imshow("Result (Yellow + Red)", result_combined)
    cv2.imshow("Result (Intersection of Yellow and Red)", result_intersection)

    # 等待按键然后关闭所有窗口
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
