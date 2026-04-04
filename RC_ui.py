import sys
import threading
import time
import uuid
import datetime
from pathlib import Path
import json
import multiprocessing
import sys
import os
import distutils.core


import requests
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSettings, QPoint,QDateTime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox,
    QLabel, QLineEdit, QCheckBox, QDialog, QComboBox, QSpinBox, QTextEdit,QFormLayout,QFileDialog
    ,QAbstractItemView,QMenu,QGroupBox,QDateTimeEdit
)
from networkx.classes import add_path

# 导入任务模块和工具模块
from assignment.jingjichang.一键竞技场 import total_jingji
from assignment.zhuxian.一键主线 import yijian_zhuxian
from assignment.shetuan.一键社团 import total_shetuan
from assignment.nibo.一键nibo import total_nibo
from assignment.zhuye.角色培养 import peiyang
from assignment.zhuye.邮件任务领取 import youxiang_renwu
from assignment.tmp_ac.世界狩猎 import world_hunt
from assignment.zhuangyuan.一键庄园 import totalzhuangyuan
from base_tool.AndroidDevice import AndroidDevice
from base_tool.read_json import json_reader
from base_tool.projection_root import find_project_root

# 服务器配置
SERVER_URL = 'http://8.138.167.2:5000'  # 请替换为您的服务器实际地址
HEARTBEAT_INTERVAL = 20  # 心跳发送间隔（秒）

def get_host_id():
    # 获取硬件的 MAC 地址作为主机标识码
    mac = uuid.getnode()
    host_id = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
    return host_id

def verify_key(key):
    try:
        response = requests.post(f'{SERVER_URL}/verify_key', json={'key': key}, timeout=10)
        if response.status_code == 200:
            return response.json().get('result')
        else:
            print('服务器返回错误状态码：', response.status_code)
            return False
    except requests.exceptions.RequestException as e:
        print('无法连接到服务器：', e)
        return False

def send_heartbeat(key, host_id):
    try:
        response = requests.post(f'{SERVER_URL}/heartbeat', json={'key': key, 'host_id': host_id}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('terminate', False), data.get('message', '')
        else:
            print('服务器返回错误状态码：', response.status_code)
            return True, '服务器错误，程序将终止'
    except requests.exceptions.RequestException as e:
        print('无法连接到服务器：', e)
        return True, '无法连接到服务器，程序将终止'

class HeartbeatThread(QThread):
    terminate_signal = pyqtSignal(str)

    def __init__(self, key, host_id):
        super().__init__()
        self.key = key
        self.host_id = host_id
        self._running = True

    def run(self):
        while self._running:
            terminate, message = send_heartbeat(self.key, self.host_id)
            if terminate:
                self.terminate_signal.emit(message)
                break
            time.sleep(HEARTBEAT_INTERVAL)

    def stop(self):
        self._running = False

# 将 run_task 函数移动到模块顶层
def run_task(task_name, task_queue, task_config,adb_path, device_address):
    try:
        # 初始化设备和配置文件
        script_dir = find_project_root()
        img_file = script_dir / 'tool'  # 定义好图片的根目录
        device = AndroidDevice(adb_path=adb_path,device_address=device_address)
        device.img_path_abs = img_file
        device.connect_device()


        # 读取JSON配置文件
        jingji_file = script_dir / 'tool' / 'location' / 'jingjichang' / 'jingjichang.json'
        jingji_json = json_reader(jingji_file)

        zhuxian_file = script_dir / 'tool' / 'location' / 'zhuxian' / 'zhuxian.json'
        zhuxian_json = json_reader(zhuxian_file)

        shetuan_file = script_dir / 'tool' / 'location' / 'shetuan' / 'shetuan.json'
        shetuan_json = json_reader(shetuan_file)

        NIBO_file = script_dir / 'tool' / 'location' / 'NIBO' / 'seven_info.json'
        NIBO_json = json_reader(NIBO_file)

        zhuye_file = script_dir / 'tool' / 'location' / 'zhuye' / 'zhuye.json'
        zhuye_json = json_reader(zhuye_file)

        tmp_AC_file = script_dir / 'tool' / 'location' / 'tmp_AC' / 'tmp_AC.json'
        tmp_AC_json = json_reader(tmp_AC_file)

        zhuangyuan_file = script_dir / 'tool' / 'location' / 'zhuangyuan' / 'zhuangyuan.json'
        zhuangyuan_json = json_reader(zhuangyuan_file)

        cur_week = datetime.datetime.now().weekday()

        # 任务映射
        def world_hunt_task(task_config):
            if cur_week in [0, 2, 4, 6]:
                world_hunt(device, tmp_AC_json, **task_config).start()
            else:
                print("世界狩猎任务当前不在可执行日期。")

        tasks = {
            "一键竞技场": lambda: total_jingji(device, jingji_json).start(),
            "一键主线": lambda: yijian_zhuxian(device, zhuxian_json, **task_config).start(),
            "一键社团": lambda: total_shetuan(device, shetuan_json).start(),
            "一键尼伯龙根": lambda: total_nibo(device, NIBO_json, **task_config).start(),
            "角色培养": lambda: peiyang(device, zhuye_json, **task_config).start(),
            "邮件等各种免费领取": lambda: youxiang_renwu(device, zhuye_json).start(),
            "世界狩猎": lambda: world_hunt_task(task_config),
            "一键庄园": lambda: totalzhuangyuan(device, zhuangyuan_json).start()
        }

        task_func = tasks.get(task_name)
        if task_func:
            task_func()
            task_queue.put("completed")
        else:
            print(f"任务 '{task_name}' 无效或条件不满足。")
            task_queue.put("invalid")
    except Exception as e:
        print(f"任务 '{task_name}' 执行过程中发生错误: {e}")
        task_queue.put("error")

class ExecutionThread(QThread):
    update_status = pyqtSignal(str)
    execution_finished = pyqtSignal()

    # def __init__(self, selected_tasks, task_configs,adb_path,device_address):
    #     super().__init__()
    #     self.selected_tasks = selected_tasks
    #     self.task_configs = task_configs
    #     self.stop_event = threading.Event()
    #     self.adb_path=adb_path
    #     self.device_address=device_address
    #     self.current_process = None
    def __init__(self, selected_tasks, task_configs, adb_path, device_address, start_time, interval, repeat_count):
        super().__init__()
        self.selected_tasks = selected_tasks
        self.task_configs = task_configs
        self.adb_path = adb_path
        self.device_address = device_address
        self.start_time = start_time
        self.interval = interval
        self.repeat_count = repeat_count
        self.stop_event = threading.Event()
        self.current_process = None

    # def run(self):
    #     try:
    #         self.update_status.emit("开始执行任务...")
    #
    #         for task_name in self.selected_tasks:
    #             if self.stop_event.is_set():
    #                 self.update_status.emit("执行被停止。")
    #                 break
    #
    #             self.update_status.emit(f"正在执行任务: {task_name}")
    #
    #             # 创建队列，用于子进程与主进程通信
    #             task_queue = multiprocessing.Queue()
    #
    #             # 获取任务配置
    #             task_config = self.task_configs.get(task_name, {})
    #
    #             # 创建并启动子进程
    #             self.current_process = multiprocessing.Process(target=run_task, args=(task_name, task_queue, task_config,self.adb_path,self.device_address))
    #             self.current_process.start()
    #
    #             # 等待任务完成或停止信号
    #             while self.current_process.is_alive():
    #                 if self.stop_event.is_set():
    #                     self.current_process.terminate()
    #                     self.current_process.join()
    #                     self.current_process = None
    #                     self.update_status.emit("执行被停止。")
    #                     break
    #                 time.sleep(0.5)  # 避免占用过多CPU
    #
    #             # 检查任务结果
    #             if not self.stop_event.is_set():
    #                 if not task_queue.empty():
    #                     result = task_queue.get()
    #                     if result == "completed":
    #                         self.update_status.emit(f"任务 '{task_name}' 执行完成。")
    #                     elif result == "invalid":
    #                         self.update_status.emit(f"任务 '{task_name}' 无效或条件不满足。")
    #                     elif result == "error":
    #                         self.update_status.emit(f"任务 '{task_name}' 执行过程中发生错误。")
    #                 else:
    #                     self.update_status.emit(f"任务 '{task_name}' 执行结束，未返回结果。")
    #             else:
    #                 break
    #
    #             # 关闭子进程
    #             if self.current_process:
    #                 self.current_process.join()
    #                 self.current_process = None
    #
    #         self.update_status.emit("所有选定的任务已执行完毕或被停止。")
    #     except Exception as e:
    #         self.update_status.emit(f"执行过程中发生错误: {str(e)}")
    #     finally:
    #         self.execution_finished.emit()
    def run(self):
        try:
            self.update_status.emit("开始执行任务...")

            # 等待开始时间
            now = datetime.datetime.now()
            if self.start_time > now:
                self.update_status.emit(f"等待开始时间 {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                while now < self.start_time:
                    if self.stop_event.is_set():
                        self.update_status.emit("执行被停止。")
                        return
                    time.sleep(1)
                    now = datetime.datetime.now()

            # 循环执行任务
            for i in range(self.repeat_count):
                if self.stop_event.is_set():
                    self.update_status.emit("执行被停止。")
                    break

                self.update_status.emit(f"第 {i + 1} 次执行任务...")

                # 执行选定的任务
                for task_name in self.selected_tasks:
                    if self.stop_event.is_set():
                        self.update_status.emit("执行被停止。")
                        break

                    self.update_status.emit(f"正在执行任务: {task_name}")

                    # 创建队列，用于子进程与主进程通信
                    task_queue = multiprocessing.Queue()

                    # 获取任务配置
                    task_config = self.task_configs.get(task_name, {})

                    # 创建并启动子进程
                    self.current_process = multiprocessing.Process(target=run_task, args=(
                    task_name, task_queue, task_config, self.adb_path, self.device_address))
                    self.current_process.start()

                    # 等待任务完成或停止信号
                    while self.current_process.is_alive():
                        if self.stop_event.is_set():
                            self.current_process.terminate()
                            self.current_process.join()
                            self.current_process = None
                            self.update_status.emit("执行被停止。")
                            break
                        time.sleep(0.5)  # 避免占用过多CPU

                    # 检查任务结果
                    if not self.stop_event.is_set():
                        if not task_queue.empty():
                            result = task_queue.get()
                            if result == "completed":
                                self.update_status.emit(f"任务 '{task_name}' 执行完成。")
                            elif result == "invalid":
                                self.update_status.emit(f"任务 '{task_name}' 无效或条件不满足。")
                            elif result == "error":
                                self.update_status.emit(f"任务 '{task_name}' 执行过程中发生错误。")
                        else:
                            self.update_status.emit(f"任务 '{task_name}' 执行结束，未返回结果。")
                    else:
                        break

                    # 关闭子进程
                    if self.current_process:
                        self.current_process.join()
                        self.current_process = None

                # 如果不是最后一次循环，且间隔时间大于0，则等待
                if i < self.repeat_count - 1 and self.interval > 0:
                    self.update_status.emit(f"等待 {self.interval} 秒后执行下一次任务...")
                    sleep_time = 0
                    while sleep_time < self.interval:
                        if self.stop_event.is_set():
                            self.update_status.emit("执行被停止。")
                            return
                        time.sleep(1)
                        sleep_time += 1

            self.update_status.emit("所有选定的任务已执行完毕或被停止。")
        except Exception as e:
            self.update_status.emit(f"执行过程中发生错误: {str(e)}")
        finally:
            self.execution_finished.emit()

    # def stop(self):
    #     self.stop_event.set()
    #     if self.current_process and self.current_process.is_alive():
    #         self.current_process.terminate()
    #         self.current_process.join()
    #         self.current_process = None
    def stop(self):
        self.stop_event.set()
        if self.current_process and self.current_process.is_alive():
            self.current_process.terminate()
            self.current_process.join()
            self.current_process = None


# 新增的任务配置对话框
class TaskConfigDialog(QDialog):
    def __init__(self, task_name, config=None, parent=None):
        super(TaskConfigDialog, self).__init__(parent)
        self.task_name = task_name
        self.config = config if config else {}
        self.setWindowTitle(f"{task_name} 参数配置")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 添加描述和介绍的文本区域
        description = QTextEdit()
        description.setReadOnly(True)
        description.setFixedHeight(100)

        # 根据任务名称，添加对应的参数配置
        if self.task_name == "一键尼伯龙根":
            description.setText("参数说明：\n"
                                "勾选框代表执行对应的任务\n"
                                "联合行动选择刷取的龙种（1-4）：\n"
                                "1：侍龙之镣 2：蝰龙之爪 \n"
                                "3：蛇蝮之心 4：深渊之龙 \n")

            # 添加参数描述和输入控件
            self.lianhe_flag = QCheckBox("执行联合任务")
            self.lianhe_flag.setChecked(bool(self.config.get('lianhe_flag', 1)))
            layout.addWidget(self.lianhe_flag)

            self.yiji_flag = QCheckBox("执行遗迹任务")
            self.yiji_flag.setChecked(bool(self.config.get('yiji_flag', 1)))
            layout.addWidget(self.yiji_flag)

            self.lunhui_flag = QCheckBox("执行轮回任务")
            self.lunhui_flag.setChecked(bool(self.config.get('lunhui_flag', 1)))
            layout.addWidget(self.lunhui_flag)

            self.lianhegongji_flag = QSpinBox()
            self.lianhegongji_flag.setRange(1, 4)
            self.lianhegongji_flag.setValue(self.config.get('lianhegongji_flag', 1))
            layout.addWidget(QLabel("联合行动选择刷取的龙种（1-4）："))
            layout.addWidget(self.lianhegongji_flag)


        elif self.task_name == "一键主线":

            description.setText("参数说明：\n"

                                "战术演练:最上面的三个选项是设置战术演练刷取不同关卡的次数\n"
                                "但是脚本默认是只会将3次有额外奖励的次数刷完就停止，按从上到下依次执行\n"
                                "难度选择部分指的是主线关卡困难或是简单")

            # yanlian_flag，需要输入列表，可以使用多个 QSpinBox 表示

            self.yanlian_values = []

            default_values = self.config.get('yanlian_flag', [0, 0, 0])

            yanlian_labels = ["金币关 次数", "经验关 次数", "元件关 次数"]

            layout.addWidget(QLabel("战术演练设置："))

            for i in range(3):
                spinbox = QSpinBox()

                spinbox.setMinimum(0)

                spinbox.setMaximum(9999)  # 根据需要设置最大值

                spinbox.setValue(default_values[i] if i < len(default_values) else 0)

                self.yanlian_values.append(spinbox)

                h_layout = QHBoxLayout()

                h_layout.addWidget(QLabel(yanlian_labels[i]))

                h_layout.addWidget(spinbox)

                layout.addLayout(h_layout)

            # nandu_flag，难度选择

            self.nandu_flag = QComboBox()

            self.nandu_flag.addItems(["简单", "困难"])

            nandu_value = self.config.get('nandu_flag', 0)

            self.nandu_flag.setCurrentIndex(nandu_value)

            layout.addWidget(QLabel("主线难度选择："))

            layout.addWidget(self.nandu_flag)

            layout.addWidget(description)


        elif self.task_name == "角色培养":
            description.setText("参数说明：\n"
                                "可以选择培养伙伴或者是强化装备，执行逻辑如下\n"
                                "优先从主角开始依次强化升阶直到材料耗尽或者段位不足")

            self.huoban_flag = QCheckBox("培养伙伴")
            self.huoban_flag.setChecked(bool(self.config.get('huoban_flag', 0)))
            layout.addWidget(self.huoban_flag)

            self.zhuangbei_flag = QCheckBox("培养装备")
            self.zhuangbei_flag.setChecked(bool(self.config.get('zhuangbei_flag', 0)))
            layout.addWidget(self.zhuangbei_flag)
        elif self.task_name == "世界狩猎":
            description.setText("参数说明：\n请选择世界狩猎任务攻击的目标boos\n"
                                "选项参数（1-3）对应boos从左到右的第一个到第三个")
            layout.addWidget(description)

            self.world_hunt_option = QSpinBox()
            self.world_hunt_option.setRange(1, 3)
            self.world_hunt_option.setValue(self.config.get('world_hunt_option', 1))
            layout.addWidget(QLabel("世界狩猎任务选项（1-3）："))
            layout.addWidget(self.world_hunt_option)

        else:
            description.setText("该任务无需配置参数。")
            layout.addWidget(description)
            # 确定和取消按钮
            buttons = QHBoxLayout()
            self.ok_button = QPushButton("确定")
            self.cancel_button = QPushButton("取消")
            buttons.addStretch()
            buttons.addWidget(self.ok_button)
            buttons.addWidget(self.cancel_button)

            # 连接按钮事件
            self.ok_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)

            layout.addLayout(buttons)
            self.setLayout(layout)
            return  # 直接返回

        layout.addWidget(description)

        # 确定和取消按钮
        buttons = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        buttons.addStretch()
        buttons.addWidget(self.ok_button)
        buttons.addWidget(self.cancel_button)

        # 连接按钮事件
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout.addLayout(buttons)
        self.setLayout(layout)

    def get_config(self):
        if self.task_name == "一键尼伯龙根":
            return {
                'lianhe_flag': int(self.lianhe_flag.isChecked()),
                'yiji_flag': int(self.yiji_flag.isChecked()),
                'lunhui_flag': int(self.lunhui_flag.isChecked()),
                'lianhegongji_flag': self.lianhegongji_flag.value()
            }
        elif self.task_name == "一键主线":
            yanlian_flag = [spinbox.value() for spinbox in self.yanlian_values]
            return {
                'yanlian_flag': yanlian_flag,
                'nandu_flag': self.nandu_flag.currentIndex()
            }
        elif self.task_name == "角色培养":
            return {
                'huoban_flag': int(self.huoban_flag.isChecked()),
                'zhuangbei_flag': int(self.zhuangbei_flag.isChecked())
            }
        elif self.task_name == "世界狩猎":
            return {
                'world_hunt_option': self.world_hunt_option.value()
            }
        else:
            return {}

class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super(PasswordDialog, self).__init__(parent)
        self.setWindowTitle("输入卡密")
        self.resize(300, 150)
        self.init_ui()
        self.load_password()

    def init_ui(self):
        layout = QVBoxLayout()

        # 卡密输入框
        self.password_label = QLabel("请输入卡密：")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        # 显示卡密复选框
        self.show_password_checkbox = QCheckBox("显示卡密")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # 记住卡密复选框
        self.remember_password_checkbox = QCheckBox("记住卡密")

        # 确定和取消按钮
        buttons = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        buttons.addStretch()
        buttons.addWidget(self.ok_button)
        buttons.addWidget(self.cancel_button)

        # 连接按钮事件
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # 添加控件到布局
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.show_password_checkbox)
        layout.addWidget(self.remember_password_checkbox)
        layout.addLayout(buttons)

        self.setLayout(layout)


    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def load_password(self):
        # 从配置文件加载保存的卡密
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                saved_password = config.get('saved_password', '')
                if saved_password:
                    self.password_input.setText(saved_password)
                    self.remember_password_checkbox.setChecked(True)
        except FileNotFoundError:
            pass

    def save_password(self):
        if self.remember_password_checkbox.isChecked():
            # 保存卡密
            saved_password = self.password_input.text()
        else:
            saved_password = ''

        # 保存到配置文件
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}

        config['saved_password'] = saved_password
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("任务执行客户端")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()
        self.heartbeat_thread = None
        self.execution_thread = None
        self.task_configs = {}  # 用于存储每个任务的配置参数
        # 初始化 QSettings
        self.settings = QSettings("YourCompany", "TaskExecutor")

        # 加载历史记录
        self.adb_history = self.settings.value("adb_paths", type=list) or []
        self.device_history = self.settings.value("device_addresses", type=list) or []
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # ADB 配置部分
        adb_group_layout = QFormLayout()

        # ADB Path 输入和历史记录按钮
        adb_path_layout = QHBoxLayout()
        self.adb_path_edit = QLineEdit()
        self.adb_path_edit.setPlaceholderText("例如: E:\\leidian\\LDPlayer9\\adb.exe")
        adb_browse_button = QPushButton("浏览")
        adb_browse_button.clicked.connect(self.browse_adb_path)
        adb_history_button = QPushButton("历史记录")
        adb_history_button.clicked.connect(self.show_adb_history)
        adb_path_layout.addWidget(self.adb_path_edit)
        adb_path_layout.addWidget(adb_browse_button)
        adb_path_layout.addWidget(adb_history_button)
        adb_group_layout.addRow(QLabel("ADB 路径:"), adb_path_layout)

        # Device Address 输入和历史记录按钮
        device_address_layout = QHBoxLayout()
        self.device_address_edit = QLineEdit()
        self.device_address_edit.setPlaceholderText("例如: 127.0.0.1:5555")
        device_history_button = QPushButton("历史记录")
        device_history_button.clicked.connect(self.show_device_history)
        device_address_layout.addWidget(self.device_address_edit)
        device_address_layout.addWidget(device_history_button)
        adb_group_layout.addRow(QLabel("设备地址:"), device_address_layout)

        main_layout.addLayout(adb_group_layout)

        # 任务列表标签
        task_label = QLabel("选择要执行的任务，并调整执行顺序：")
        main_layout.addWidget(task_label)

        # 任务列表
        self.task_list = QListWidget()
        self.task_list.setSelectionMode(QListWidget.MultiSelection)
        self.tasks = [
            "一键社团",
            "一键庄园",
            "一键竞技场",
            "世界狩猎",
            "一键主线",
           "一键尼伯龙根",
            "角色培养",
            "邮件等各种免费领取"]
        for task in self.tasks:
            item = QListWidgetItem(task)
            item.setCheckState(Qt.Unchecked)
            self.task_list.addItem(item)
        main_layout.addWidget(self.task_list)

        # 排序和配置按钮
        control_layout = QHBoxLayout()
        up_button = QPushButton("上移")
        down_button = QPushButton("下移")
        config_button = QPushButton("配置参数")
        control_layout.addWidget(up_button)
        control_layout.addWidget(down_button)
        control_layout.addWidget(config_button)
        main_layout.addLayout(control_layout)

        up_button.clicked.connect(self.move_up)
        down_button.clicked.connect(self.move_down)
        config_button.clicked.connect(self.configure_task)

        # 按钮布局
        button_layout = QHBoxLayout()
        # 开始按钮
        self.start_button = QPushButton("开始执行")
        self.start_button.clicked.connect(self.start_execution)
        button_layout.addWidget(self.start_button)

        # 停止按钮
        self.stop_button = QPushButton("停止执行")
        self.stop_button.clicked.connect(self.stop_execution)
        self.stop_button.setEnabled(False)  # 初始时禁用
        button_layout.addWidget(self.stop_button)

        main_layout.addLayout(button_layout)

        # # 状态显示
        # self.status_label = QLabel("状态: 等待执行")
        # main_layout.addWidget(self.status_label)

        # central_widget.setLayout(main_layout)
        #定时执行板块
        # # 按钮布局
        # button_layout = QHBoxLayout()
        # # 开始按钮
        # self.start_button = QPushButton("开始执行")
        # self.start_button.clicked.connect(self.start_execution)
        # button_layout.addWidget(self.start_button)
        #
        # # 停止按钮
        # self.stop_button = QPushButton("停止执行")
        # self.stop_button.clicked.connect(self.stop_execution)
        # self.stop_button.setEnabled(False)  # 初始时禁用
        # button_layout.addWidget(self.stop_button)

        # main_layout.addLayout(button_layout)

        # 状态显示
        self.status_label = QLabel("状态: 等待执行")
        main_layout.addWidget(self.status_label)

        # 定时执行选项
        schedule_group = QGroupBox("定时执行设置")
        schedule_layout = QFormLayout()

        # 启用定时执行复选框
        self.enable_schedule_checkbox = QCheckBox("启用定时执行")
        schedule_layout.addRow(self.enable_schedule_checkbox)

        # 开始时间
        self.start_time_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.start_time_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.start_time_edit.setCalendarPopup(True)
        self.start_time_edit.setEnabled(False)
        schedule_layout.addRow("开始时间：", self.start_time_edit)

        # 任务间隔（秒）
        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setRange(1, 86400)  # 范围从1秒到24小时
        self.interval_spinbox.setValue(60)  # 默认60秒
        self.interval_spinbox.setEnabled(False)
        schedule_layout.addRow("任务间隔（秒）：", self.interval_spinbox)

        # 循环次数
        self.repeat_count_spinbox = QSpinBox()
        self.repeat_count_spinbox.setRange(1, 1000)
        self.repeat_count_spinbox.setValue(1)
        self.repeat_count_spinbox.setEnabled(False)
        schedule_layout.addRow("循环次数：", self.repeat_count_spinbox)

        schedule_group.setLayout(schedule_layout)
        main_layout.addWidget(schedule_group)

        central_widget.setLayout(main_layout)

        # 连接启用复选框的状态变化信号
        self.enable_schedule_checkbox.stateChanged.connect(self.toggle_schedule_options)

    def toggle_schedule_options(self, state):
        enabled = state == Qt.Checked
        self.start_time_edit.setEnabled(enabled)
        self.interval_spinbox.setEnabled(enabled)
        self.repeat_count_spinbox.setEnabled(enabled)

    def move_up(self):
        current_row = self.task_list.currentRow()
        if current_row > 0:
            current_item = self.task_list.takeItem(current_row)
            self.task_list.insertItem(current_row - 1, current_item)
            self.task_list.setCurrentRow(current_row - 1)

    def move_down(self):
        current_row = self.task_list.currentRow()
        if current_row < self.task_list.count() - 1:
            current_item = self.task_list.takeItem(current_row)
            self.task_list.insertItem(current_row + 1, current_item)
            self.task_list.setCurrentRow(current_row + 1)
    def browse_adb_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择 adb.exe",
            "",
            "Executable Files (*.exe);;All Files (*)",
            options=options
        )
        if file_path:
            self.adb_path_edit.setText(file_path)

    def add_to_history(self, adb_path, device_address):
        # 添加 adb_path 到历史记录
        if adb_path and adb_path not in self.adb_history:
            self.adb_history.insert(0, adb_path)
            # 可选：限制历史记录的数量
            if len(self.adb_history) > 10:
                self.adb_history = self.adb_history[:10]
            self.settings.setValue("adb_paths", self.adb_history)

        # 添加 device_address 到历史记录
        if device_address and device_address not in self.device_history:
            self.device_history.insert(0, device_address)
            # 可选：限制历史记录的数量
            if len(self.device_history) > 10:
                self.device_history = self.device_history[:10]
            self.settings.setValue("device_addresses", self.device_history)
    def show_adb_history(self):
        dialog = HistoryDialog(self.adb_history, "ADB 路径历史记录", self)
        if dialog.exec_() == QDialog.Accepted:
            selected = dialog.get_selected_item()
            if selected:
                self.adb_path_edit.setText(selected)
            # 更新历史记录
            updated_history = dialog.get_updated_history()
            self.adb_history = updated_history
            self.settings.setValue("adb_paths", self.adb_history)

    def show_device_history(self):
        dialog = HistoryDialog(self.device_history, "设备地址历史记录", self)
        if dialog.exec_() == QDialog.Accepted:
            selected = dialog.get_selected_item()
            if selected:
                self.device_address_edit.setText(selected)
            # 更新历史记录
            updated_history = dialog.get_updated_history()
            self.device_history = updated_history
            self.settings.setValue("device_addresses", self.device_history)
    # 其余方法保持不变...
    def configure_task(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请先选择一个任务进行配置。")
            return
        if len(selected_items) > 1:
            QMessageBox.warning(self, "警告", "一次只能配置一个任务。")
            return

        task_name = selected_items[0].text()
        config_dialog = TaskConfigDialog(task_name, self.task_configs.get(task_name, {}), self)
        if config_dialog.exec_() == QDialog.Accepted:
            self.task_configs[task_name] = config_dialog.get_config()

    def start_execution(self):
        # 获取 adb_path 和 device_address
        adb_path = self.adb_path_edit.text().strip()
        device_address = self.device_address_edit.text().strip()

        # 验证 adb_path 和 device_address
        if not adb_path:
            QMessageBox.warning(self, "警告", "请填写 ADB 路径。")
            return
        if not device_address:
            QMessageBox.warning(self, "警告", "请填写设备地址。")
            return

        # 验证 adb_path 是否存在
        if not os.path.isfile(adb_path):
            QMessageBox.warning(self, "警告", "ADB 路径无效，请检查路径是否正确。")
            return

        # 验证 device_address 格式
        if ":" not in device_address:
            QMessageBox.warning(self, "警告", "设备地址格式无效，应为 IP:端口 形式。")
            return

        # 获取选中的任务，并保持顺序
        selected_tasks = []
        for index in range(self.task_list.count()):
            item = self.task_list.item(index)
            if item.checkState() == Qt.Checked:
                selected_tasks.append(item.text())

        if not selected_tasks:
            QMessageBox.warning(self, "警告", "请至少选择一个任务。")
            return
            # 获取定时执行设置
        schedule_enabled = self.enable_schedule_checkbox.isChecked()
        if schedule_enabled:
            start_time = self.start_time_edit.dateTime().toPyDateTime()
            interval = self.interval_spinbox.value()
            repeat_count = self.repeat_count_spinbox.value()
        else:
            start_time = datetime.datetime.now()
            interval = 0
            repeat_count = 1
        # 弹出密码输入对话框
        password_dialog = PasswordDialog(self)
        if password_dialog.exec_() == QDialog.Accepted:
            key = password_dialog.password_input.text()
            if not key:
                QMessageBox.warning(self, "警告", "必须输入卡密才能继续。")
                return
            # 保存卡密（如果用户选择了记住卡密）
            password_dialog.save_password()
        else:
            # 用户取消
            return

        # 验证卡密
        self.status_label.setText("状态: 验证卡密中...")
        QApplication.processEvents()  # 更新UI

        if not verify_key(key):
            QMessageBox.critical(self, "错误", "卡密验证失败，程序无法运行。")
            self.status_label.setText("状态: 卡密验证失败。")
            return

        # 获取主机ID
        host_id = get_host_id()

        # 启动心跳线程
        self.heartbeat_thread = HeartbeatThread(key, host_id)
        self.heartbeat_thread.terminate_signal.connect(self.handle_terminate)
        self.heartbeat_thread.start()

        # # 启动执行线程
        # self.execution_thread = ExecutionThread(
        #     selected_tasks,
        #     self.task_configs,
        #     adb_path=adb_path,
        #     device_address=device_address
        # )
        # self.execution_thread.update_status.connect(self.update_status)
        # self.execution_thread.execution_finished.connect(self.execution_finished)
        # self.execution_thread.start()
        #
        # self.status_label.setText("状态: 执行中...")
        # self.start_button.setEnabled(False)
        # self.stop_button.setEnabled(True)  # 启用停止按钮
        #
        # # 保存 adb_path 和 device_address 到历史记录
        # self.add_to_history(adb_path, device_address)
        # 启动执行线程
        self.execution_thread = ExecutionThread(
            selected_tasks,
            self.task_configs,
            adb_path=adb_path,
            device_address=device_address,
            start_time=start_time,
            interval=interval,
            repeat_count=repeat_count
        )
        self.execution_thread.update_status.connect(self.update_status)
        self.execution_thread.execution_finished.connect(self.execution_finished)
        self.execution_thread.start()

        self.status_label.setText("状态: 执行中...")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)  # 启用停止按钮

        # 保存 adb_path 和 device_address 到历史记录
        self.add_to_history(adb_path, device_address)

    def stop_execution(self):
        reply = QMessageBox.question(
            self, '确认停止',
            "您确定要停止任务执行吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.stop_all()

    def handle_terminate(self, message):
        QMessageBox.critical(self, "终止", f"服务器指示终止程序：{message}")
        self.stop_all()

    # def stop_all(self):
    #     if self.heartbeat_thread:
    #         self.heartbeat_thread.stop()
    #         self.heartbeat_thread.wait()
    #         self.heartbeat_thread = None
    #     if self.execution_thread:
    #         self.execution_thread.stop()
    #         self.execution_thread.wait()
    #         self.execution_thread = None
    #     self.status_label.setText("状态: 已停止。")
    #     self.start_button.setEnabled(True)
    #     self.stop_button.setEnabled(False)  # 停用停止按钮
    def stop_all(self):
        if self.heartbeat_thread:
            self.heartbeat_thread.stop()
            self.heartbeat_thread.wait()
            self.heartbeat_thread = None
        if self.execution_thread:
            self.execution_thread.stop()
            self.execution_thread.wait()
            self.execution_thread = None
        self.status_label.setText("状态: 已停止。")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)  # 停用停止按钮

    def update_status(self, message):
        self.status_label.setText(f"状态: {message}")
        QApplication.processEvents()  # 更新UI

    def execution_finished(self):
        QMessageBox.information(self, "完成", "所有选定的任务已执行完毕或被停止。")
        self.status_label.setText("状态: 完成。")
        if self.heartbeat_thread:
            self.heartbeat_thread.stop()
            self.heartbeat_thread.wait()
            self.heartbeat_thread = None
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)  # 停用停止按钮

    def closeEvent(self, event):
        # 在关闭窗口时，确保所有线程被正确停止
        self.stop_all()
        event.accept()

    # 其余方法保持不变...
class HistoryDialog(QDialog):
    def __init__(self, history_list, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(400, 300)
        self.selected_item = None

        self.layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.addItems(history_list)
        self.list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_widget.itemDoubleClicked.connect(self.select_item)

        # 添加右键菜单删除功能
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.open_context_menu)

        self.layout.addWidget(self.list_widget)

        # 按钮布局
        self.buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def open_context_menu(self, position):
        menu = QMenu()
        delete_action = menu.addAction("删除")
        action = menu.exec_(self.list_widget.mapToGlobal(position))
        if action == delete_action:
            item = self.list_widget.itemAt(position)
            if item:
                row = self.list_widget.row(item)
                self.list_widget.takeItem(row)

    def select_item(self, item):
        self.selected_item = item.text()
        self.accept()

    def get_selected_item(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            return selected_items[0].text()
        return None

    def get_updated_history(self):
        history = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            history.append(item.text())
        return history

def main():
    multiprocessing.freeze_support()  # 为了在 Windows 上兼容多进程
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
