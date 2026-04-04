import sys
import os
import json
import subprocess
import cv2
import numpy as np
from projection_root import find_project_root
from datetime import datetime
from pathlib import Path
from PIL import Image  # 使用Pillow保存图像
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QFileDialog,
    QVBoxLayout, QHBoxLayout, QInputDialog, QMessageBox, QScrollArea, QLineEdit
)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QRect, pyqtSignal, QPoint
from AndroidDevice import AndroidDevice  # 确保这个模块在你的环境中可用
X_file = Path('zhuxian')
X_json = 'zhuxian.json'
adb_path=r"E:\leidian\LDPlayer9\adb.exe"
device_address="127.0.0.1:5555"
# adb_path=r"E:\Program Files\Netease\MuMuPlayer-12.0\shell\adb.exe"
# device_address="127.0.0.1:16384"
class ImageLabel(QLabel):
    # 定义一个信号，用于在区域被选中时通知主窗口
    region_selected = pyqtSignal(QRect)
    zoom_requested = pyqtSignal(float, QPoint)  # 新增信号，用于缩放

    def __init__(self, parent=None):
        super(ImageLabel, self).__init__(parent)
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.start_point = None
        self.end_point = None
        self.rectangles = []
        self.current_rect = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.end_point = self.start_point
            self.current_rect = QRect(self.start_point, self.end_point)
            self.update()

    def mouseMoveEvent(self, event):
        if self.start_point:
            self.end_point = event.pos()
            self.current_rect = QRect(self.start_point, self.end_point)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.start_point:
            self.end_point = event.pos()
            self.current_rect = QRect(self.start_point, self.end_point)

            # 只添加有效的矩形
            if self.current_rect.width() > 10 and self.current_rect.height() > 10:
                self.rectangles.append(self.current_rect)
                # 触发信号，通知主窗口区域被选中
                self.region_selected.emit(self.current_rect)
            else:
                QMessageBox.warning(self, "警告", "选定的区域过小，请重新选择。")

            self.current_rect = None
            self.start_point = None
            self.end_point = None
            self.update()

    def paintEvent(self, event):
        super(ImageLabel, self).paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.green, 2, Qt.SolidLine)
        painter.setPen(pen)

        # 绘制当前正在绘制的矩形
        if self.current_rect:
            painter.drawRect(self.current_rect)

        # 绘制已绘制的所有矩形
        for rect in self.rectangles:
            painter.drawRect(rect)

    def wheelEvent(self, event):
        # 捕获鼠标滚轮事件，用于放大缩小
        if event.angleDelta().y() > 0:
            zoom_in_factor = 1.25
            self.zoom_requested.emit(zoom_in_factor, event.pos())
        else:
            zoom_out_factor = 0.8
            self.zoom_requested.emit(zoom_out_factor, event.pos())

        event.accept()

    def clear_rectangles(self):
        self.rectangles = []
        self.current_rect = None
        self.update()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("游戏脚本自动化工具")
        self.device = AndroidDevice(adb_path=adb_path,device_address=device_address)
        self.init_ui()

        # 缩放相关
        self.scale_factor = 1.0  # 初始缩放比例

    def init_ui(self):
        # 创建按钮
        self.connect_btn = QPushButton("连接设备")
        self.connect_btn.clicked.connect(self.connect_device)

        self.capture_btn = QPushButton("捕获截图")
        self.capture_btn.clicked.connect(self.capture_screenshot)
        self.capture_btn.setEnabled(False)

        self.select_dir_btn = QPushButton("选择图片目录")
        self.select_dir_btn.clicked.connect(self.select_image_directory)

        self.browse_btn = QPushButton("选择图片")
        self.browse_btn.clicked.connect(self.select_image)
        self.browse_btn.setEnabled(False)

        self.save_screenshot_btn = QPushButton("保存截图")
        self.save_screenshot_btn.clicked.connect(self.save_full_screenshot)
        self.save_screenshot_btn.setEnabled(False)

        self.set_save_dir_btn = QPushButton("选择保存目录")
        self.set_save_dir_btn.clicked.connect(self.set_save_directory)

        self.save_dir_label = QLabel("保存目录: 未指定")
        self.save_dir_path = ""

        self.save_info_btn = QPushButton("保存区域信息")
        self.save_info_btn.clicked.connect(self.save_areas_info)
        self.save_info_btn.setEnabled(False)

        # 创建一个 QLabel 显示当前缩放比例
        self.zoom_label = QLabel("缩放比例: 100%")

        # 图像显示区域放在 QScrollArea 中
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.image_label = ImageLabel(self)
        self.scroll_area.setWidget(self.image_label)

        # 连接信号
        self.image_label.region_selected.connect(self.process_selected_area)
        self.image_label.zoom_requested.connect(self.zoom_image)  # 连接缩放信号

        # 布局
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.connect_btn)
        top_layout.addWidget(self.capture_btn)
        top_layout.addWidget(self.save_screenshot_btn)
        top_layout.addWidget(self.set_save_dir_btn)
        top_layout.addWidget(self.save_dir_label)

        middle_layout = QHBoxLayout()
        middle_layout.addWidget(self.select_dir_btn)
        middle_layout.addWidget(self.browse_btn)
        middle_layout.addWidget(self.save_info_btn)
        middle_layout.addWidget(self.zoom_label)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)

        # 数据
        self.image = None
        self.clone = None
        self.areas_info = {}
        self.script_dir = find_project_root()
        print(self.script_dir)
        self.areas_dir = self.script_dir / 'tool' / 'location'/X_file
        self.areas_dir.mkdir(parents=True, exist_ok=True)
        self.info_file = self.areas_dir / X_json
        self.load_areas_info()

    def connect_device(self):
        try:
            if self.device.is_device_connected():
                QMessageBox.information(self, "信息", f"设备 {self.device.device_address} 已连接。")
                self.capture_btn.setEnabled(True)
                self.connect_btn.setEnabled(False)  # 连接成功后禁用连接按钮
                return

            self.device.connect_device()
            if self.device.is_device_connected():
                QMessageBox.information(self, "成功", f"已连接到设备 {self.device.device_address}")
                self.capture_btn.setEnabled(True)
                self.connect_btn.setEnabled(False)  # 连接成功后禁用连接按钮
            else:
                QMessageBox.critical(self, "失败", f"无法连接到设备 {self.device.device_address}。请检查设备是否已启动并连接。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"连接设备时发生错误: {e}")

    def capture_screenshot(self):
        try:
            # 捕获最新的截图
            image_path = self.device.capture_screenshot()
            if not image_path:
                QMessageBox.warning(self, "失败", "未能获取截图，请检查设备连接。")
                return

            self.image = cv2.imread(image_path)
            if self.image is None:
                QMessageBox.critical(self, "错误", f"无法读取截图文件: {image_path}")
                return

            self.clone = self.image.copy()
            self.scale_factor = 1.0  # 重置缩放比例
            self.display_image(self.image)

            # 清除之前的矩形框
            self.image_label.clear_rectangles()

            self.save_info_btn.setEnabled(True)
            self.save_screenshot_btn.setEnabled(True)
            QMessageBox.information(self, "成功", "截图已捕获并显示。请在图像上选择区域。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"捕获截图时发生错误: {e}")

    def set_save_directory(self):
        options = QFileDialog.Options()
        dir_name = QFileDialog.getExistingDirectory(self, "选择保存截图的目录", "", options=options)
        if dir_name:
            self.save_dir_path = dir_name
            self.save_dir_label.setText(f"保存目录: {dir_name}")
            QMessageBox.information(self, "成功", f"保存目录已设置为: {dir_name}")
        else:
            QMessageBox.warning(self, "警告", "未选择保存目录。")

    def save_full_screenshot(self):
        if self.image is None:
            QMessageBox.warning(self, "警告", "请先捕获截图或选择图片。")
            return

        if not self.save_dir_path:
            QMessageBox.warning(self, "警告", "请先指定保存目录。")
            return

        # 询问用户为截图命名
        screenshot_name, ok = QInputDialog.getText(self, "保存截图", "请输入截图名称:")
        if not ok:
            # 用户取消了输入
            return

        screenshot_name = screenshot_name.strip()
        if not screenshot_name:
            QMessageBox.warning(self, "警告", "名称不能为空，无法保存截图。")
            return

        # 构建保存路径
        image_filename = f"{screenshot_name}.png"
        image_path = Path(self.save_dir_path) / image_filename

        try:
            # 将BGR转为RGB
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            pil_image.save(image_path)
            QMessageBox.information(self, "成功", f"截图已保存为: {image_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存截图时发生错误: {e}")

    def select_image_directory(self):
        options = QFileDialog.Options()
        dir_name = QFileDialog.getExistingDirectory(self, "选择图片目录", "", options=options)
        if dir_name:
            self.image_dir = dir_name
            self.browse_btn.setEnabled(True)
            QMessageBox.information(self, "成功", f"图片目录已设置为: {dir_name}")
        else:
            QMessageBox.warning(self, "警告", "未选择图片目录。")

    def select_image(self):
        if not hasattr(self, 'image_dir') or not self.image_dir:
            QMessageBox.warning(self, "警告", "请先选择图片目录。")
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择图片", self.image_dir,
            "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)",
            options=options
        )
        if file_name:
            self.image = cv2.imread(file_name)
            if self.image is None:
                QMessageBox.critical(self, "错误", f"无法读取图片文件: {file_name}")
                return
            self.clone = self.image.copy()
            self.scale_factor = 1.0  # 重置缩放比例
            self.display_image(self.image)
            # 清除之前的矩形框
            self.image_label.clear_rectangles()
            self.save_info_btn.setEnabled(True)
            self.save_screenshot_btn.setEnabled(False)  # 选择图片后，禁用保存截图按钮
            QMessageBox.information(self, "成功", "图片已加载并显示。请在图像上选择区域。")

    def display_image(self, img):
        try:
            # 应用缩放
            scaled_img = cv2.resize(img, None, fx=self.scale_factor, fy=self.scale_factor, interpolation=cv2.INTER_LINEAR)

            height, width, channel = scaled_img.shape
            bytes_per_line = 3 * width
            q_img = QImage(scaled_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(q_img)
            self.image_label.setPixmap(pixmap)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"显示图像时发生错误: {e}")

    def zoom_image(self, factor, mouse_pos):
        if self.image is None:
            return

        # 记录当前缩放比例
        old_scale = self.scale_factor
        self.scale_factor *= factor

        # 限制缩放比例在10%到500%
        self.scale_factor = max(0.1, min(self.scale_factor, 5.0))

        # 重新显示图像
        self.display_image(self.image)

        # 更新缩放比例标签
        self.zoom_label.setText(f"缩放比例: {int(self.scale_factor * 100)}%")

        # 计算鼠标在视图中的位置
        scroll_bar_x = self.scroll_area.horizontalScrollBar()
        scroll_bar_y = self.scroll_area.verticalScrollBar()

        # 获取鼠标在ImageLabel中的坐标
        mouse_x = mouse_pos.x()
        mouse_y = mouse_pos.y()

        # 计算图像中鼠标对应的坐标
        img_x = mouse_x / old_scale
        img_y = mouse_y / old_scale

        # 计算新的缩放后鼠标对应的坐标
        new_mouse_x = img_x * self.scale_factor
        new_mouse_y = img_y * self.scale_factor

        # 获取视口的大小
        viewport = self.scroll_area.viewport()
        viewport_width = viewport.width()
        viewport_height = viewport.height()

        # 计算新的滚动条位置，以保持鼠标指针下的图像部分在视口中心
        new_scroll_x = new_mouse_x - mouse_x
        new_scroll_y = new_mouse_y - mouse_y

        # 限制滚动条的范围
        new_scroll_x = max(0, min(new_scroll_x, scroll_bar_x.maximum()))
        new_scroll_y = max(0, min(new_scroll_y, scroll_bar_y.maximum()))

        # 设置滚动条的位置
        scroll_bar_x.setValue(int(new_scroll_x))
        scroll_bar_y.setValue(int(new_scroll_y))

    def process_selected_area(self, rect):
        if self.image is None:
            QMessageBox.warning(self, "警告", "请先捕获截图或选择图片。")
            return

        try:
            # 获取显示的图像尺寸
            pixmap = self.image_label.pixmap()
            if pixmap is None:
                QMessageBox.warning(self, "警告", "未能获取显示的图像。")
                return

            # 计算缩放比例
            img_height, img_width, _ = self.image.shape
            pixmap_width = pixmap.width()
            pixmap_height = pixmap.height()

            # 反向计算缩放比例
            scale_x = img_width / pixmap_width
            scale_y = img_height / pixmap_height

            # 根据当前缩放比例调整选择区域
            x1 = int(rect.left() * scale_x)
            y1 = int(rect.top() * scale_y)
            x2 = int(rect.right() * scale_x)
            y2 = int(rect.bottom() * scale_y)

            # 确保坐标在图像范围内
            x1, x2 = sorted([max(0, x1), min(img_width, x2)])
            y1, y2 = sorted([max(0, y1), min(img_height, y2)])

            # 检查区域有效性
            if x2 <= x1 or y2 <= y1:
                QMessageBox.warning(self, "警告", "选定的区域无效，跳过保存该区域。")
                return

            roi = self.clone[y1:y2, x1:x2]

            # 询问用户为该区域命名
            area_name, ok = QInputDialog.getText(self, "区域命名", "请输入该区域的名称（用于保存和识别）:")
            if not ok:
                # 用户取消了输入
                return

            area_name = area_name.strip()
            if not area_name:
                QMessageBox.warning(self, "警告", "名称不能为空，跳过保存该区域。")
                return

            # 检查名称是否重复
            if area_name in self.areas_info:
                QMessageBox.warning(self, "警告", f"区域名称 '{area_name}' 已存在。请使用其他名称。")
                return

            # 使用Pathlib处理路径，确保支持中文
            image_filename = f"{area_name}.png"
            image_path = self.areas_dir / image_filename

            try:
                # 将BGR转为RGB
                roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(roi_rgb)
                pil_image.save(image_path)
                QMessageBox.information(self, "成功", f"局部截图已保存为: {image_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存局部截图时发生错误: {e}")
                return

            # 添加区域信息，使用相对路径
            relative_image_path = image_path.relative_to(self.script_dir/'tool')
            self.areas_info[area_name] = {
                "image_path": str(relative_image_path),
                "coordinates": {
                    "top_left": [x1, y1],
                    "bottom_right": [x2, y2]
                }
            }

            # 保存更新后的信息
            self.save_areas_info()

        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理选定区域时发生错误: {e}")
            return

    def save_areas_info(self):
        try:
            with open(self.info_file, 'w', encoding='utf-8') as f:
                json.dump(self.areas_info, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "成功", f"区域信息已保存至: {self.info_file}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存区域信息时发生错误: {e}")

    def load_areas_info(self):
        if self.info_file.exists():
            try:
                with open(self.info_file, 'r', encoding='utf-8') as f:
                    self.areas_info = json.load(f)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载区域信息时发生错误: {e}")
                self.areas_info = {}

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, '退出', "确定要退出吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
