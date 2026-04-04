import os
import subprocess
from datetime import datetime
import numpy as np
import cv2
import json
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets


def create_hsv_mask(image, hsv_values,invert=False):
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

    if invert:
        # 如果需要反转掩模，执行按位非操作
        combined_mask = cv2.bitwise_not(combined_mask)
    return combined_mask


def save_hsv_config(config_path, mask_name, hsv_values, invert):
    """
    将多个HSV值保存到JSON配置文件。
    """
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                configs = json.load(f)
            except json.JSONDecodeError:
                configs = {}
    else:
        configs = {}

    configs[mask_name] = {
        "hsv_values": hsv_values,
        "invert": invert
    }

    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(configs, f, indent=4, ensure_ascii=False)
        print(f"HSV配置已保存到 {config_path}，掩模名称: {mask_name}")
    except TypeError as e:
        print(f"保存配置时发生错误: {e}")
        QtWidgets.QMessageBox.warning(None, "保存错误", f"保存配置时发生错误: {e}")


class ImageLabel(QtWidgets.QLabel):
    point_selected = QtCore.pyqtSignal(int, int)  # 用于传递点击的图像坐标

    def __init__(self):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.pixmap = None
        self.scale_factor = 1.0
        self.offset = QtCore.QPoint(0, 0)
        self.last_mouse_pos = None
        self.panning = False
        self.setMouseTracking(True)

    def setImage(self, image):
        self.pixmap = QtGui.QPixmap.fromImage(image)
        self.scale_factor = 1.0
        self.offset = QtCore.QPoint(0, 0)
        self.update()

    def paintEvent(self, event):
        if self.pixmap:
            painter = QtGui.QPainter(self)
            # 计算缩放后的图像大小
            scaled_pixmap_size = self.pixmap.size() * self.scale_factor
            scaled_pixmap = self.pixmap.scaled(
                scaled_pixmap_size,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            # 计算绘制的位置
            center = self.rect().center() + self.offset
            top_left = center - QtCore.QPointF(scaled_pixmap.width() / 2, scaled_pixmap.height() / 2)
            painter.drawPixmap(top_left.toPoint(), scaled_pixmap)
        else:
            super().paintEvent(event)

    def wheelEvent(self, event):
        if self.pixmap:
            # 获取鼠标位置相对于窗口的坐标
            cursor_pos = event.pos()
            # 获取缩放前鼠标对应的图像坐标
            img_pos_before = self.mapToImage(cursor_pos)

            # 缩放
            zoom_factor = 1.25 if event.angleDelta().y() > 0 else 0.8
            self.scale_factor *= zoom_factor
            self.scale_factor = max(0.1, min(self.scale_factor, 10))

            # 获取缩放后鼠标对应的图像坐标
            img_pos_after = self.mapToImage(cursor_pos)

            # 调整偏移，使得缩放以鼠标为中心
            delta_img_pos = img_pos_after - img_pos_before
            self.offset += QtCore.QPointF(delta_img_pos.x() * self.scale_factor, delta_img_pos.y() * self.scale_factor).toPoint()

            self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # 左键点击用于选择点
            img_point = self.mapToImage(event.pos())
            img_x = int(img_point.x())
            img_y = int(img_point.y())
            if 0 <= img_x < self.pixmap.width() and 0 <= img_y < self.pixmap.height():
                self.point_selected.emit(img_x, img_y)
        elif event.button() == QtCore.Qt.MiddleButton or event.button() == QtCore.Qt.RightButton:
            # 中键或右键按下开始拖动
            self.last_mouse_pos = event.pos()
            self.panning = True
            self.setCursor(QtCore.Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self.panning and self.last_mouse_pos:
            # 计算鼠标移动的距离，更新偏移量
            delta = event.pos() - self.last_mouse_pos
            self.offset += delta
            self.last_mouse_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton or event.button() == QtCore.Qt.RightButton:
            # 松开中键或右键，结束拖动
            self.panning = False
            self.setCursor(QtCore.Qt.ArrowCursor)

    def mapToImage(self, point):
        """
        将窗口坐标映射到图像坐标
        """
        center = self.rect().center() + self.offset
        scaled_size = self.pixmap.size() * self.scale_factor
        image_top_left = center - QtCore.QPointF(scaled_size.width() / 2, scaled_size.height() / 2)
        x = (point.x() - image_top_left.x()) / self.scale_factor
        y = (point.y() - image_top_left.y()) / self.scale_factor
        return QtCore.QPointF(x, y)


class ImageWindow(QtWidgets.QMainWindow):
    def __init__(self, title="Image"):
        super().__init__()
        self.setWindowTitle(title)
        self.image_label = ImageLabel()
        self.setCentralWidget(self.image_label)
        self.resize(600, 400)


class MaskAdjuster(QtWidgets.QWidget):
    def __init__(self, adb_path=r"E:\leidian\LDPlayer9\adb.exe", device_address="127.0.0.1:5555",
                 config_path='masks.json'):
        super().__init__()
        self.adb_path = adb_path
        self.device_address = device_address
        self.config_path = config_path
        self.screenshot_dir = r"D:\py_project\crawl_novel-main\screen_pic\tmp"
        self.original_image_np = None  # 用于存储原始图像
        self.masks = {}  # 存储掩模数据

        self.selected_points = []  # 存储选中的点，用于撤销
        self.hsv_values = []  # 存储多个HSV值

        # 创建图像窗口
        self.original_window = ImageWindow("原始图像")
        self.mask_window = ImageWindow("掩码图像")
        self.result_window = ImageWindow("结果图像")

        self.init_ui()
        self.capture_screenshot()

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle('HSV Mask Adjuster')
        self.setGeometry(100, 100, 400, 300)

        # 创建主布局
        main_layout = QtWidgets.QVBoxLayout()

        # 创建控制布局
        controls_layout = QtWidgets.QVBoxLayout()

        # 创建滑动条布局
        sliders_layout = QtWidgets.QGridLayout()

        # 创建滑动条和标签
        self.sliders = {}
        slider_names = ['Lower H', 'Lower S', 'Lower V', 'Upper H', 'Upper S', 'Upper V']
        for i, name in enumerate(slider_names):
            label = QtWidgets.QLabel(name)
            slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            slider.setMinimum(0)
            if 'H' in name:
                slider.setMaximum(179)
            else:
                slider.setMaximum(255)
            slider.setValue(0 if 'Lower' in name else (179 if 'H' in name else 255))
            slider.valueChanged.connect(self.update_from_sliders)
            self.sliders[name] = slider
            sliders_layout.addWidget(label, i, 0)
            sliders_layout.addWidget(slider, i, 1)

        controls_layout.addLayout(sliders_layout)

        # 添加反转掩模的复选框
        self.invert_checkbox = QtWidgets.QCheckBox('Invert Mask')
        self.invert_checkbox.stateChanged.connect(self.update_image)
        controls_layout.addWidget(self.invert_checkbox)

        # 创建按钮布局
        buttons_layout = QtWidgets.QHBoxLayout()

        # 保存按钮
        save_button = QtWidgets.QPushButton('Save Mask')
        save_button.clicked.connect(self.save_mask)
        buttons_layout.addWidget(save_button)

        # 撤销按钮
        undo_button = QtWidgets.QPushButton('Undo')
        undo_button.clicked.connect(self.undo_selection)
        buttons_layout.addWidget(undo_button)

        # 刷新截图按钮
        refresh_button = QtWidgets.QPushButton('Refresh Screenshot')
        refresh_button.clicked.connect(self.capture_screenshot)
        buttons_layout.addWidget(refresh_button)

        # 选择图片按钮
        select_image_button = QtWidgets.QPushButton('Select Image')
        select_image_button.clicked.connect(self.select_image)
        buttons_layout.addWidget(select_image_button)

        controls_layout.addLayout(buttons_layout)

        # 添加掩码列表
        self.mask_list_widget = QtWidgets.QListWidget()
        self.mask_list_widget.itemClicked.connect(self.apply_mask_from_list)
        controls_layout.addWidget(QtWidgets.QLabel("Mask List:"))
        controls_layout.addWidget(self.mask_list_widget)

        # 删除掩码按钮
        delete_mask_button = QtWidgets.QPushButton('Delete Selected Mask')
        delete_mask_button.clicked.connect(self.delete_selected_mask)
        controls_layout.addWidget(delete_mask_button)

        # 添加掩码计算器按钮
        mask_calculator_button = QtWidgets.QPushButton('Mask Calculator')
        mask_calculator_button.clicked.connect(self.open_mask_calculator)
        controls_layout.addWidget(mask_calculator_button)

        # 将控制布局添加到主布局
        main_layout.addLayout(controls_layout)

        self.setLayout(main_layout)

        # 连接鼠标点击信号
        self.original_window.image_label.point_selected.connect(self.on_point_selected)

        # 加载掩码
        self.load_masks()

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

    def capture_screenshot(self):
        self.connect_device()
        if not self.is_device_connected():
            QtWidgets.QMessageBox.warning(self, "连接错误", f"设备 {self.device_address} 未连接。")
            return

        screenshot_path = self.get_screenshot_path()
        if screenshot_path:
            image = Image.open(screenshot_path).convert("RGB")
            self.original_image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            self.update_image()  # 自动更新掩模和结果
            print(f"屏幕截图已保存到 {screenshot_path}")
        else:
            QtWidgets.QMessageBox.warning(self, "截图错误", "无法截取屏幕截图。")

    def select_image(self):
        """
        让用户从本地选择一张图片进行掩码操作。
        """
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.jpg *.bmp)", options=options)
        if filename:
            image = Image.open(filename).convert("RGB")
            self.original_image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            self.update_image()
            print(f"已加载图片 {filename}")

    def get_screenshot_path(self):
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        screenshot_filename = f"screenshot_{timestamp}.png"
        screenshot_path = os.path.join(self.screenshot_dir, screenshot_filename)

        try:
            screenshot_command = f'"{self.adb_path}" -s {self.device_address} exec-out screencap -p'
            result = subprocess.run(screenshot_command, shell=True, stdout=subprocess.PIPE)
            with open(screenshot_path, 'wb') as f:
                f.write(result.stdout)
            return screenshot_path
        except Exception as e:
            print(f"截取屏幕截图时出错: {e}")
            return None

    def update_from_sliders(self):
        """
        当滑动条改变时，更新HSV值，并刷新图像。
        """
        lower_h = int(self.sliders['Lower H'].value())
        lower_s = int(self.sliders['Lower S'].value())
        lower_v = int(self.sliders['Lower V'].value())
        upper_h = int(self.sliders['Upper H'].value())
        upper_s = int(self.sliders['Upper S'].value())
        upper_v = int(self.sliders['Upper V'].value())

        # 更新当前的HSV值列表，只包含一个范围
        self.hsv_values = [{
            'lower_h': lower_h,
            'lower_s': lower_s,
            'lower_v': lower_v,
            'upper_h': upper_h,
            'upper_s': upper_s,
            'upper_v': upper_v
        }]

        self.update_image()

    def update_image(self):
        """
        更新掩模和显示结果图像。
        """
        if self.original_image_np is None:
            return

        invert = self.invert_checkbox.isChecked()

        if not self.hsv_values:
            # 如果没有HSV值，创建全黑的掩模
            mask = np.zeros(self.original_image_np.shape[:2], dtype=np.uint8)
        else:
            # 创建掩模
            mask = create_hsv_mask(self.original_image_np, self.hsv_values)
            if invert:
                mask = cv2.bitwise_not(mask)

        # 应用掩模
        result = cv2.bitwise_and(self.original_image_np, self.original_image_np, mask=mask)

        # 转换为RGB用于显示
        original_rgb = cv2.cvtColor(self.original_image_np, cv2.COLOR_BGR2RGB)
        mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

        # 将NumPy数组转换为QImage
        original_image = QtGui.QImage(original_rgb.data, original_rgb.shape[1], original_rgb.shape[0],
                                      original_rgb.strides[0], QtGui.QImage.Format_RGB888)
        mask_image = QtGui.QImage(mask_rgb.data, mask_rgb.shape[1], mask_rgb.shape[0],
                                  mask_rgb.strides[0], QtGui.QImage.Format_RGB888)
        result_image = QtGui.QImage(result_rgb.data, result_rgb.shape[1], result_rgb.shape[0],
                                    result_rgb.strides[0], QtGui.QImage.Format_RGB888)

        # 显示图像
        self.original_window.image_label.setImage(original_image)
        self.mask_window.image_label.setImage(mask_image)
        self.result_window.image_label.setImage(result_image)

        # 显示窗口
        self.original_window.show()
        self.mask_window.show()
        self.result_window.show()

    def on_point_selected(self, x, y):
        """
        当在原始图像上点击时，更新HSV滑动条，并添加新的HSV范围。
        """
        if self.original_image_np is None:
            return

        hsv_image = cv2.cvtColor(self.original_image_np, cv2.COLOR_BGR2HSV)
        hsv_value = hsv_image[y, x]

        # 根据选中点的HSV值，设置滑动条范围为 ±10（或其他值，可调整）
        delta = 10
        lower_h = max(hsv_value[0] - delta, 0)
        lower_s = max(hsv_value[1] - delta, 0)
        lower_v = max(hsv_value[2] - delta, 0)
        upper_h = min(hsv_value[0] + delta, 179)
        upper_s = min(hsv_value[1] + delta, 255)
        upper_v = min(hsv_value[2] + delta, 255)

        # 添加新的HSV范围到列表中
        self.hsv_values.append({
            'lower_h': int(lower_h),
            'lower_s': int(lower_s),
            'lower_v': int(lower_v),
            'upper_h': int(upper_h),
            'upper_s': int(upper_s),
            'upper_v': int(upper_v)
        })

        # 更新滑动条，显示所有选中区域的最小下限和最大上限
        self.update_sliders()

        # 保存选中的点，用于撤销
        self.selected_points.append((x, y))

        # 更新图像
        self.update_image()

    def update_sliders(self):
        """
        更新滑动条，显示所有选中区域的最小下限和最大上限。
        """
        if not self.hsv_values:
            self.reset_sliders()
            return

        lower_h = min(hsv['lower_h'] for hsv in self.hsv_values)
        lower_s = min(hsv['lower_s'] for hsv in self.hsv_values)
        lower_v = min(hsv['lower_v'] for hsv in self.hsv_values)
        upper_h = max(hsv['upper_h'] for hsv in self.hsv_values)
        upper_s = max(hsv['upper_s'] for hsv in self.hsv_values)
        upper_v = max(hsv['upper_v'] for hsv in self.hsv_values)

        self.sliders['Lower H'].blockSignals(True)
        self.sliders['Lower S'].blockSignals(True)
        self.sliders['Lower V'].blockSignals(True)
        self.sliders['Upper H'].blockSignals(True)
        self.sliders['Upper S'].blockSignals(True)
        self.sliders['Upper V'].blockSignals(True)

        self.sliders['Lower H'].setValue(lower_h)
        self.sliders['Lower S'].setValue(lower_s)
        self.sliders['Lower V'].setValue(lower_v)
        self.sliders['Upper H'].setValue(upper_h)
        self.sliders['Upper S'].setValue(upper_s)
        self.sliders['Upper V'].setValue(upper_v)

        self.sliders['Lower H'].blockSignals(False)
        self.sliders['Lower S'].blockSignals(False)
        self.sliders['Lower V'].blockSignals(False)
        self.sliders['Upper H'].blockSignals(False)
        self.sliders['Upper S'].blockSignals(False)
        self.sliders['Upper V'].blockSignals(False)

    def undo_selection(self):
        """
        撤销上一个感兴趣的区域，并更新掩模。
        """
        if not self.selected_points or not self.hsv_values:
            QtWidgets.QMessageBox.warning(self, "撤销错误", "没有可撤销的操作。")
            return

        # 移除最后一个选中的点和对应的HSV范围
        self.selected_points.pop()
        self.hsv_values.pop()

        # 更新滑动条
        self.update_sliders()

        # 更新图像
        self.update_image()

    def reset_sliders(self):
        self.sliders['Lower H'].blockSignals(True)
        self.sliders['Lower S'].blockSignals(True)
        self.sliders['Lower V'].blockSignals(True)
        self.sliders['Upper H'].blockSignals(True)
        self.sliders['Upper S'].blockSignals(True)
        self.sliders['Upper V'].blockSignals(True)

        self.sliders['Lower H'].setValue(0)
        self.sliders['Lower S'].setValue(0)
        self.sliders['Lower V'].setValue(0)
        self.sliders['Upper H'].setValue(179)
        self.sliders['Upper S'].setValue(255)
        self.sliders['Upper V'].setValue(255)

        self.sliders['Lower H'].blockSignals(False)
        self.sliders['Lower S'].blockSignals(False)
        self.sliders['Lower V'].blockSignals(False)
        self.sliders['Upper H'].blockSignals(False)
        self.sliders['Upper S'].blockSignals(False)
        self.sliders['Upper V'].blockSignals(False)

    def save_mask(self):
        """
        保存当前HSV参数，并命名。
        """
        if self.original_image_np is None:
            QtWidgets.QMessageBox.warning(self, "保存错误", "尚未截取屏幕截图或加载图片。")
            return

        if not self.hsv_values:
            QtWidgets.QMessageBox.warning(self, "保存错误", "没有设置HSV值。")
            return

        invert = self.invert_checkbox.isChecked()

        # 获取掩模名称
        mask_name, ok = QtWidgets.QInputDialog.getText(self, '保存掩模', '请输入掩模的名称 (e.g., water):')
        if ok and mask_name:
            # 检查掩模名称是否已存在
            if mask_name in self.masks:
                reply = QtWidgets.QMessageBox.question(
                    self, '确认覆盖', f"掩模名称 '{mask_name}' 已存在。是否覆盖？",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No
                )
                if reply == QtWidgets.QMessageBox.No:
                    return

            # 保存HSV参数和反转选项
            save_hsv_config(self.config_path, mask_name, self.hsv_values.copy(), invert)
            self.masks[mask_name] = {
                "hsv_values": self.hsv_values.copy(),
                "invert": invert
            }
            # 更新掩码列表
            self.load_masks()
            QtWidgets.QMessageBox.information(self, "保存成功", f"掩模 '{mask_name}' 已保存。")
        else:
            QtWidgets.QMessageBox.warning(self, "保存取消", "掩模名称不能为空。")

    def load_masks(self):
        """
        从JSON配置文件加载掩模并更新列表。
        """
        self.mask_list_widget.clear()
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                try:
                    self.masks = json.load(f)
                except json.JSONDecodeError:
                    self.masks = {}
            for mask_name in self.masks.keys():
                self.mask_list_widget.addItem(mask_name)
        else:
            self.masks = {}

    def apply_mask_from_list(self, item):
        """
        从列表中选择掩模并应用到当前图像。
        """
        mask_name = item.text()
        mask_data = self.masks.get(mask_name)
        if mask_data:
            hsv_values = mask_data.get('hsv_values', [])
            # 兼容旧格式，如果是字典，转换为列表
            if isinstance(hsv_values, dict):
                hsv_values = [hsv_values]
            self.hsv_values = hsv_values
            invert = mask_data.get('invert', False)
            self.invert_checkbox.setChecked(invert)

            # 更新滑动条
            self.update_sliders()

            # 更新图像
            self.update_image()
        else:
            QtWidgets.QMessageBox.warning(self, "错误", f"未找到掩模 '{mask_name}'。")

    def delete_selected_mask(self):
        """
        删除选定的掩模并更新配置文件。
        """
        selected_items = self.mask_list_widget.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "删除错误", "请先在列表中选择要删除的掩模。")
            return

        item = selected_items[0]
        mask_name = item.text()

        reply = QtWidgets.QMessageBox.question(
            self, '确认删除', f"确定要删除掩模 '{mask_name}' 吗？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            # 从self.masks中删除
            if mask_name in self.masks:
                del self.masks[mask_name]
                # 保存到JSON文件
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.masks, f, indent=4, ensure_ascii=False)
                # 从列表中删除
                self.mask_list_widget.takeItem(self.mask_list_widget.row(item))
                QtWidgets.QMessageBox.information(self, "删除成功", f"掩模 '{mask_name}' 已删除。")
            else:
                QtWidgets.QMessageBox.warning(self, "删除错误", f"掩模 '{mask_name}' 不存在。")

    def open_mask_calculator(self):
        """
        打开掩码计算器对话框。
        """
        self.mask_calculator = MaskCalculatorDialog(self.masks)
        self.mask_calculator.new_mask_saved.connect(self.on_new_mask_saved)
        self.mask_calculator.exec_()

    def on_new_mask_saved(self, mask_name, hsv_values, invert):
        """
        保存从掩码计算器得到的新掩模。
        """
        # 保存到self.masks
        self.masks[mask_name] = {
            'hsv_values': hsv_values,
            'invert': invert
        }
        # 保存到JSON文件
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.masks, f, indent=4, ensure_ascii=False)
        # 更新掩码列表
        self.load_masks()


class MaskCalculatorDialog(QtWidgets.QDialog):
    new_mask_saved = QtCore.pyqtSignal(str, list, bool)  # mask_name, hsv_values, invert

    def __init__(self, masks):
        super().__init__()
        self.masks = masks
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Mask Calculator')
        self.setGeometry(200, 200, 400, 300)

        layout = QtWidgets.QVBoxLayout()

        # 说明标签
        instruction_label = QtWidgets.QLabel('选择掩模和操作以创建新掩模:')
        layout.addWidget(instruction_label)

        # 掩模选择列表
        self.mask_list_widget = QtWidgets.QListWidget()
        self.mask_list_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        for mask_name in self.masks.keys():
            self.mask_list_widget.addItem(mask_name)
        layout.addWidget(self.mask_list_widget)

        # 操作选择
        operation_layout = QtWidgets.QHBoxLayout()
        operation_layout.addWidget(QtWidgets.QLabel('Operation:'))

        self.operation_combo = QtWidgets.QComboBox()
        self.operation_combo.addItems(['Intersection', 'Union', 'Invert'])
        operation_layout.addWidget(self.operation_combo)

        layout.addLayout(operation_layout)

        # 保存按钮
        save_button = QtWidgets.QPushButton('Save New Mask')
        save_button.clicked.connect(self.save_new_mask)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_new_mask(self):
        selected_items = self.mask_list_widget.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "错误", "请先选择一个或多个掩模。")
            return

        selected_masks = [item.text() for item in selected_items]
        operation = self.operation_combo.currentText()

        # 执行操作
        if operation == 'Invert':
            if len(selected_masks) != 1:
                QtWidgets.QMessageBox.warning(self, "错误", "反转操作只能选择一个掩模。")
                return
            mask_name = selected_masks[0]
            mask_data = self.masks[mask_name]
            hsv_values = mask_data['hsv_values']
            invert = not mask_data['invert']
        else:
            # 对于交集和并集，需要组合多个HSV范围
            hsv_values_list = []
            for name in selected_masks:
                hsv_values = self.masks[name]['hsv_values']
                if isinstance(hsv_values, dict):
                    hsv_values = [hsv_values]
                hsv_values_list.append(hsv_values)

            if operation == 'Intersection':
                # 取每个HSV范围的交集
                combined_hsv_values = []
                for hsvs in zip(*hsv_values_list):
                    lower_h = max(hsv['lower_h'] for hsv in hsvs)
                    lower_s = max(hsv['lower_s'] for hsv in hsvs)
                    lower_v = max(hsv['lower_v'] for hsv in hsvs)
                    upper_h = min(hsv['upper_h'] for hsv in hsvs)
                    upper_s = min(hsv['upper_s'] for hsv in hsvs)
                    upper_v = min(hsv['upper_v'] for hsv in hsvs)
                    combined_hsv_values.append({
                        'lower_h': lower_h,
                        'lower_s': lower_s,
                        'lower_v': lower_v,
                        'upper_h': upper_h,
                        'upper_s': upper_s,
                        'upper_v': upper_v
                    })
            elif operation == 'Union':
                # 将所有HSV范围合并
                combined_hsv_values = []
                for hsv_values in hsv_values_list:
                    combined_hsv_values.extend(hsv_values)
            invert = False

            hsv_values = combined_hsv_values

        # 获取新掩模名称
        mask_name, ok = QtWidgets.QInputDialog.getText(self, '保存掩模', '请输入新掩模的名称:')
        if ok and mask_name:
            # 发射信号保存新掩模
            self.new_mask_saved.emit(mask_name, hsv_values, invert)
            QtWidgets.QMessageBox.information(self, "保存成功", f"新掩模 '{mask_name}' 已保存。")
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "保存取消", "掩模名称不能为空。")


def main():
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    adb_path = r"E:\leidian\LDPlayer9\adb.exe"  # 请根据实际情况修改
    device_address = "127.0.0.1:5555"  # 请根据实际情况修改
    window = MaskAdjuster(adb_path=adb_path, device_address=device_address, config_path='masks.json')
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
