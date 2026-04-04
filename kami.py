import sys
import uuid
import json
import logging
from datetime import datetime, timedelta

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QSpinBox, QMessageBox, QTableWidget, QTableWidgetItem
)

import paramiko  # 用于通过 SSH 上传文件

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("client.log"),
        logging.StreamHandler()
    ]
)

# 客户端配置
SERVER_IP = '8.138.167.2'  # 替换为您的服务器公网 IP
USERNAME = 'root'  # 替换为您的服务器用户名
PRIVATE_KEY_PATH = r'D:\py_project\longzu2\longzu.pem'  # 替换为您的私钥路径
REMOTE_KEY_PATH = '/root/longzuserve/keys1.json'  # 服务器上卡密文件的路径


# 卡密生成函数
def generate_unique_key(max_clients, expiry_days):
    while True:
        # 生成特定格式的卡密，例如 XXXX-XXXX-XXXX
        key = '-'.join([''.join([uuid.uuid4().hex.upper()[i] for i in range(4)]) for _ in range(3)])
        # 假设本地不需要检查重复，可以简化
        break
    created_at = datetime.utcnow()
    expiry_at = created_at + timedelta(days=expiry_days)
    key_info = {
        key: {
            'max_clients': max_clients,
            'created_at': created_at.isoformat(),
            'expiry_at': expiry_at.isoformat()
        }
    }
    logging.info(f"生成新卡密: {key}, 最大使用数量: {max_clients}, 过期时间: {expiry_at.isoformat()}")
    return key, key_info


# 卡密生成工作线程
class KeyGenerationWorker(QThread):
    key_generated = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, max_clients, expiry_days):
        super().__init__()
        self.max_clients = max_clients
        self.expiry_days = expiry_days

    def run(self):
        try:
            # 生成新卡密
            key, key_info = generate_unique_key(self.max_clients, self.expiry_days)

            # 创建 SSH 客户端并连接
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            private_key = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_PATH)
            ssh.connect(SERVER_IP, username=USERNAME, pkey=private_key)

            # 打开 SFTP 会话
            sftp = ssh.open_sftp()

            keys = {}
            try:
                # 尝试下载现有的 keys1.json 文件
                with sftp.file(REMOTE_KEY_PATH, 'r') as remote_file:
                    keys = json.load(remote_file)
                    logging.info("已下载现有卡密数据。")
            except IOError as e:
                if e.errno == 2:  # 文件不存在
                    logging.info("远程卡密文件不存在，将创建新的文件。")
                else:
                    raise e

            # 添加新生成的卡密
            keys.update(key_info)
            logging.info(f"添加新卡密: {key}")

            # 将更新后的卡密数据保存到本地 keys.json 文件
            with open('keys.json', 'w', encoding='utf-8') as f:
                json.dump(keys, f, ensure_ascii=False, indent=4)
                logging.info("保存卡密数据成功。")

            # 上传更新后的 keys.json 文件到服务器，覆盖原有的 keys1.json
            sftp.put('keys.json', REMOTE_KEY_PATH)
            logging.info(f"卡密文件已上传到服务器 {SERVER_IP}:{REMOTE_KEY_PATH}")

            # 关闭 SFTP 和 SSH 连接
            sftp.close()
            ssh.close()

            # 发射信号表示生成成功
            self.key_generated.emit(key)
        except Exception as e:
            logging.error(f"生成或上传卡密时发生错误: {e}")
            self.error_occurred.emit(str(e))


# 卡密读取工作线程
class KeyReadingWorker(QThread):
    keys_loaded = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            # 创建 SSH 客户端并连接
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            private_key = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_PATH)
            ssh.connect(SERVER_IP, username=USERNAME, pkey=private_key)

            # 打开 SFTP 会话
            sftp = ssh.open_sftp()

            keys = {}
            try:
                # 尝试下载现有的 keys1.json 文件
                with sftp.file(REMOTE_KEY_PATH, 'r') as remote_file:
                    keys = json.load(remote_file)
                    logging.info("已下载现有卡密数据。")
            except IOError as e:
                if e.errno == 2:  # 文件不存在
                    logging.info("远程卡密文件不存在。")
                else:
                    raise e

            # 关闭连接
            sftp.close()
            ssh.close()

            # 发射信号表示读取成功
            self.keys_loaded.emit(keys)
        except Exception as e:
            logging.error(f"读取卡密文件时发生错误: {e}")
            self.error_occurred.emit(str(e))


# 卡密删除工作线程
class KeyDeletionWorker(QThread):
    deletion_success = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, key_to_delete):
        super().__init__()
        self.key_to_delete = key_to_delete

    def run(self):
        try:
            # 创建 SSH 客户端并连接
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            private_key = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_PATH)
            ssh.connect(SERVER_IP, username=USERNAME, pkey=private_key)

            # 打开 SFTP 会话
            sftp = ssh.open_sftp()

            keys = {}
            try:
                # 尝试下载现有的 keys1.json 文件
                with sftp.file(REMOTE_KEY_PATH, 'r') as remote_file:
                    keys = json.load(remote_file)
                    logging.info("已下载现有卡密数据。")
            except IOError as e:
                if e.errno == 2:  # 文件不存在
                    logging.info("远程卡密文件不存在。")
                    self.error_occurred.emit("远程卡密文件不存在，无法删除卡密。")
                    sftp.close()
                    ssh.close()
                    return
                else:
                    raise e

            if self.key_to_delete in keys:
                del keys[self.key_to_delete]
                logging.info(f"删除卡密: {self.key_to_delete}")
            else:
                logging.warning(f"卡密 {self.key_to_delete} 不存在。")
                self.error_occurred.emit(f"卡密 {self.key_to_delete} 不存在。")
                sftp.close()
                ssh.close()
                return

            # 将更新后的卡密数据保存到本地 keys.json 文件
            with open('keys.json', 'w', encoding='utf-8') as f:
                json.dump(keys, f, ensure_ascii=False, indent=4)
                logging.info("保存卡密数据成功。")

            # 上传更新后的 keys.json 文件到服务器，覆盖原有的 keys1.json
            sftp.put('keys.json', REMOTE_KEY_PATH)
            logging.info(f"卡密文件已上传到服务器 {SERVER_IP}:{REMOTE_KEY_PATH}")

            # 关闭 SFTP 和 SSH 连接
            sftp.close()
            ssh.close()

            # 发射信号表示删除成功
            self.deletion_success.emit(self.key_to_delete)
        except Exception as e:
            logging.error(f"删除卡密时发生错误: {e}")
            self.error_occurred.emit(str(e))


# GUI 主窗口类
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("卡密生成与上传")
        self.setGeometry(100, 100, 800, 600)  # 调整窗口大小以容纳新控件
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # 卡密生成部分
        generate_layout = QHBoxLayout()

        # 最大使用数量
        max_clients_label = QLabel("最大使用数量:")
        self.max_clients_spin = QSpinBox()
        self.max_clients_spin.setMinimum(1)
        self.max_clients_spin.setMaximum(1000)
        self.max_clients_spin.setValue(1)

        # 时限（天）
        expiry_label = QLabel("时限（天）:")
        self.expiry_spin = QSpinBox()
        self.expiry_spin.setMinimum(1)
        self.expiry_spin.setMaximum(365)
        self.expiry_spin.setValue(30)

        # 生成按钮
        self.generate_button = QPushButton("生成并上传卡密")
        self.generate_button.clicked.connect(self.generate_key)

        generate_layout.addWidget(max_clients_label)
        generate_layout.addWidget(self.max_clients_spin)
        generate_layout.addWidget(expiry_label)
        generate_layout.addWidget(self.expiry_spin)
        generate_layout.addWidget(self.generate_button)

        main_layout.addLayout(generate_layout)

        # 生成的卡密显示
        self.generated_key_label = QLabel("生成的卡密:")
        self.generated_key_text = QLineEdit()
        self.generated_key_text.setReadOnly(True)

        main_layout.addWidget(self.generated_key_label)
        main_layout.addWidget(self.generated_key_text)

        # 复制按钮
        self.copy_button = QPushButton("复制卡密")
        self.copy_button.clicked.connect(self.copy_key)
        main_layout.addWidget(self.copy_button)

        # 读取已有卡密按钮
        self.read_keys_button = QPushButton("读取已有卡密")
        self.read_keys_button.clicked.connect(self.read_existing_keys)
        main_layout.addWidget(self.read_keys_button)

        # 删除选中卡密按钮
        self.delete_key_button = QPushButton("删除选中卡密")
        self.delete_key_button.clicked.connect(self.delete_selected_key)
        main_layout.addWidget(self.delete_key_button)

        # 搜索布局
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入卡密进行搜索")
        self.search_button = QPushButton("搜索")
        self.search_button.clicked.connect(self.search_keys)
        self.reset_search_button = QPushButton("重置")
        self.reset_search_button.clicked.connect(self.reset_search)

        search_layout.addWidget(QLabel("搜索卡密:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.reset_search_button)

        main_layout.addLayout(search_layout)

        # 显示卡密的表格
        self.keys_table = QTableWidget()
        self.keys_table.setColumnCount(4)
        self.keys_table.setHorizontalHeaderLabels(["卡密", "最大使用数量", "创建时间", "过期时间"])
        self.keys_table.horizontalHeader().setStretchLastSection(True)
        self.keys_table.setEditTriggers(QTableWidget.NoEditTriggers)  # 禁止编辑
        self.keys_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.keys_table.setSelectionMode(QTableWidget.SingleSelection)  # 单选模式
        main_layout.addWidget(self.keys_table)

        central_widget.setLayout(main_layout)

    def generate_key(self):
        max_clients = self.max_clients_spin.value()
        expiry_days = self.expiry_spin.value()
        self.generate_button.setEnabled(False)
        self.generated_key_text.setText("正在生成并上传卡密，请稍候...")
        self.worker = KeyGenerationWorker(max_clients, expiry_days)
        self.worker.key_generated.connect(self.on_key_generated)
        self.worker.error_occurred.connect(self.on_key_generation_error)
        self.worker.start()

    def on_key_generated(self, key):
        self.generate_button.setEnabled(True)
        self.generated_key_text.setText(key)
        QMessageBox.information(self, "成功", f"生成并上传卡密成功:\n{key}")
        # 自动刷新卡密列表
        self.read_existing_keys()

    def on_key_generation_error(self, error_message):
        self.generate_button.setEnabled(True)
        self.generated_key_text.setText("")
        QMessageBox.critical(self, "错误", f"生成或上传卡密时发生错误:\n{error_message}")

    def copy_key(self):
        key = self.generated_key_text.text()
        if key and key != "正在生成并上传卡密，请稍候...":
            clipboard = QApplication.clipboard()
            clipboard.setText(key)
            QMessageBox.information(self, "复制成功", "卡密已复制到剪贴板。")
        else:
            QMessageBox.warning(self, "警告", "没有生成的卡密可复制。")

    def read_existing_keys(self):
        self.read_keys_button.setEnabled(False)
        self.read_keys_button.setText("读取中，请稍候...")
        self.worker_read = KeyReadingWorker()
        self.worker_read.keys_loaded.connect(self.on_keys_loaded)
        self.worker_read.error_occurred.connect(self.on_keys_read_error)
        self.worker_read.start()

    def on_keys_loaded(self, keys):
        self.read_keys_button.setEnabled(True)
        self.read_keys_button.setText("读取已有卡密")
        self.keys_table.setRowCount(0)  # 清空现有表格

        for key, info in keys.items():
            row_position = self.keys_table.rowCount()
            self.keys_table.insertRow(row_position)
            self.keys_table.setItem(row_position, 0, QTableWidgetItem(key))
            self.keys_table.setItem(row_position, 1, QTableWidgetItem(str(info.get('max_clients', ''))))
            self.keys_table.setItem(row_position, 2, QTableWidgetItem(info.get('created_at', '')))
            self.keys_table.setItem(row_position, 3, QTableWidgetItem(info.get('expiry_at', '')))

        QMessageBox.information(self, "成功", "已成功读取并显示服务器上的卡密。")

    def on_keys_read_error(self, error_message):
        self.read_keys_button.setEnabled(True)
        self.read_keys_button.setText("读取已有卡密")
        QMessageBox.critical(self, "错误", f"读取卡密时发生错误:\n{error_message}")

    def delete_selected_key(self):
        selected_items = self.keys_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请先选择要删除的卡密。")
            return

        # 获取选中的卡密（假设卡密在第一列）
        selected_row = selected_items[0].row()
        key = self.keys_table.item(selected_row, 0).text()

        reply = QMessageBox.question(
            self,
            "确认删除",
            f"您确定要删除卡密 '{key}' 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.delete_key_button.setEnabled(False)
            self.delete_key_button.setText("删除中，请稍候...")
            self.deletion_worker = KeyDeletionWorker(key)
            self.deletion_worker.deletion_success.connect(self.on_key_deleted)
            self.deletion_worker.error_occurred.connect(self.on_key_deletion_error)
            self.deletion_worker.start()

    def on_key_deleted(self, key):
        self.delete_key_button.setEnabled(True)
        self.delete_key_button.setText("删除选中卡密")
        QMessageBox.information(self, "成功", f"卡密 '{key}' 已成功删除。")
        self.read_existing_keys()  # 刷新卡密列表

    def on_key_deletion_error(self, error_message):
        self.delete_key_button.setEnabled(True)
        self.delete_key_button.setText("删除选中卡密")
        QMessageBox.critical(self, "错误", f"删除卡密时发生错误:\n{error_message}")

    def search_keys(self):
        search_term = self.search_input.text().strip().upper()
        if not search_term:
            QMessageBox.warning(self, "警告", "请输入要搜索的卡密。")
            return

        row_count = self.keys_table.rowCount()
        found = False
        for row in range(row_count):
            item = self.keys_table.item(row, 0)  # 假设卡密在第一列
            if item and search_term in item.text().upper():
                self.keys_table.selectRow(row)
                found = True
                break

        if not found:
            QMessageBox.information(self, "未找到", f"未找到包含 '{search_term}' 的卡密。")

    def reset_search(self):
        self.search_input.clear()
        self.keys_table.clearSelection()

    def closeEvent(self, event):
        event.accept()


def main():
    app_gui = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app_gui.exec_())


if __name__ == '__main__':
    main()
