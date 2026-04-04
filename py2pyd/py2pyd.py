import os
import sys
import subprocess
from pathlib import Path
from setuptools import Extension
from Cython.Build import cythonize
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import sysconfig
import tempfile
import json

# 定义历史记录文件名
HISTORY_FILENAME = "py_to_pyd_converter_history.json"


def get_history_file_path():
    """
    获取历史记录文件的完整路径，存储在脚本所在的目录中。
    """
    script_dir = Path(__file__).parent.resolve()
    history_file = script_dir / HISTORY_FILENAME
    return history_file


def load_history():
    """
    从历史记录文件中加载历史记录。
    """
    history_file = get_history_file_path()
    if history_file.exists():
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
                if isinstance(history, list):
                    return history
        except Exception as e:
            print(f"无法加载历史记录: {e}")
    return []


def save_history(history):
    """
    将历史记录保存到历史记录文件中。
    """
    history_file = get_history_file_path()
    try:
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"无法保存历史记录: {e}")


def add_to_history(input_dir, output_dir, history):
    """
    将新的输入和输出目录添加到历史记录中，避免重复。
    """
    record = {"input_dir": input_dir, "output_dir": output_dir}
    if record not in history:
        history.append(record)
        save_history(history)


def find_py_files(directory):
    """
    递归查找指定目录下的所有 .py 文件。
    """
    return list(Path(directory).rglob("*.py"))


def compile_py_file(py_file, output_dir, input_dir, log_callback=None):
    """
    使用 Cython 将单个 .py 文件编译为 .pyd 文件，并将其输出到指定的输出目录。
    不在源代码或输出目录中生成任何 build 文件。
    使用独立的进程进行编译，以避免多次调用 setuptools.setup() 的问题。
    """
    try:
        # 确保 py_file 是 Path 对象
        py_file = Path(py_file)

        # 计算相对于输入目录的相对路径，并移除文件后缀
        relative_path = py_file.relative_to(input_dir).with_suffix('')

        # 模块名称，包含包结构
        module_name = '.'.join(relative_path.parts)

        # 目标输出目录对应的相对路径
        target_dir = Path(output_dir) / relative_path.parent
        target_dir.mkdir(parents=True, exist_ok=True)

        # 获取扩展模块的后缀（例如 .pyd）
        ext_suffix = sysconfig.get_config_var('EXT_SUFFIX')
        if not ext_suffix:
            ext_suffix = '.pyd'  # 默认值

        # 目标 .pyd 文件路径
        compiled_file = target_dir / f"{py_file.stem}{ext_suffix}"

        # 如果已存在且更新时间相近，跳过编译
        if compiled_file.exists() and compiled_file.stat().st_mtime >= py_file.stat().st_mtime:
            if log_callback:
                log_callback(f"跳过编译 {py_file}，因为已存在最新的 .pyd 文件。\n")
            return True

        # 创建临时目录用于编译
        with tempfile.TemporaryDirectory() as temp_build_dir:
            temp_build_path = Path(temp_build_dir)

            # 创建临时 setup.py
            setup_py_content = f"""
from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    name="{module_name}",
    ext_modules=cythonize(
        Extension(
            "{module_name}",
            ["{py_file.as_posix()}"],
        ),
        compiler_directives={{
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True
        }},
    ),
    script_args=["build_ext", "--build-lib", "{target_dir.as_posix()}", "--build-temp", "{temp_build_path.as_posix()}"],
)
"""
            setup_py_path = temp_build_path / "setup.py"
            with open(setup_py_path, 'w', encoding='utf-8') as f:
                f.write(setup_py_content)

            # 运行编译命令，指定编码为 utf-8 并处理解码错误
            process = subprocess.run(
                [sys.executable, "setup.py"],
                cwd=temp_build_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',  # 明确指定使用 'utf-8' 编码
                errors='replace'  # 替换无法解码的字节
            )

            # 捕捉编译过程中的输出
            compile_output = process.stdout + "\n" + process.stderr

            if process.returncode != 0:
                if log_callback:
                    log_callback(f"编译 {py_file} 失败：\n{compile_output}\n")
                return False
            else:
                # 检查 .pyd 文件是否生成
                if compiled_file.exists():
                    # 删除编译生成的 .c 文件
                    for c_file in target_dir.glob("*.c"):
                        try:
                            c_file.unlink()
                            if log_callback:
                                log_callback(f"已删除临时文件: {c_file}\n")
                        except Exception as e:
                            if log_callback:
                                log_callback(f"无法删除临时文件 {c_file}: {e}\n")

                    if log_callback:
                        log_callback(f"成功编译 {py_file} 为 .pyd 文件。\n")
                        log_callback(compile_output + "\n")
                    return True
                else:
                    if log_callback:
                        log_callback(f"编译 {py_file} 失败：未找到生成的 .pyd 文件。\n")
                    return False
    except Exception as e:
        if log_callback:
            log_callback(f"编译 {py_file} 失败: {e}\n")
        return False


class PyToPydConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Py to Pyd Converter")

        # 加载历史记录
        self.history = load_history()

        # 定义变量
        self.input_directory = tk.StringVar()
        self.output_directory = tk.StringVar()

        # 配置网格布局
        master.columnconfigure(1, weight=1)

        # 输入目录部分
        self.input_label = tk.Label(master, text="源代码目录:")
        self.input_label.grid(row=0, column=0, padx=10, pady=5, sticky='e')

        self.input_entry = tk.Entry(master, textvariable=self.input_directory, width=50)
        self.input_entry.grid(row=0, column=1, padx=10, pady=5, sticky='we')

        self.input_browse_button = tk.Button(master, text="浏览", command=self.browse_input_directory)
        self.input_browse_button.grid(row=0, column=2, padx=10, pady=5)

        # 输出目录部分
        self.output_label = tk.Label(master, text="输出目录:")
        self.output_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')

        self.output_entry = tk.Entry(master, textvariable=self.output_directory, width=50)
        self.output_entry.grid(row=1, column=1, padx=10, pady=5, sticky='we')

        self.output_browse_button = tk.Button(master, text="浏览", command=self.browse_output_directory)
        self.output_browse_button.grid(row=1, column=2, padx=10, pady=5)

        # 开始编译按钮
        self.compile_button = tk.Button(master, text="开始编译", command=self.start_compilation)
        self.compile_button.grid(row=2, column=1, pady=10)

        # 历史记录标签
        self.history_label = tk.Label(master, text="历史记录:")
        self.history_label.grid(row=3, column=0, padx=10, pady=5, sticky='ne')

        # 历史记录列表框
        self.history_listbox = tk.Listbox(master, selectmode=tk.SINGLE, width=50, height=10)
        self.history_listbox.grid(row=3, column=1, padx=10, pady=5, sticky='we')

        # 滚动条
        self.history_scrollbar = tk.Scrollbar(master, orient=tk.VERTICAL, command=self.history_listbox.yview)
        self.history_scrollbar.grid(row=3, column=2, padx=(0, 10), pady=5, sticky='ns')
        self.history_listbox.config(yscrollcommand=self.history_scrollbar.set)

        # 历史记录控制按钮
        self.use_history_button = tk.Button(master, text="使用选定记录", command=self.use_selected_history)
        self.use_history_button.grid(row=4, column=1, padx=10, pady=5, sticky='w')

        self.delete_history_button = tk.Button(master, text="删除选定记录", command=self.delete_selected_history)
        self.delete_history_button.grid(row=4, column=1, padx=10, pady=5, sticky='e')

        # 日志显示区域
        self.log_text = scrolledtext.ScrolledText(master, width=80, height=20, state='disabled')
        self.log_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        # 填充权重
        master.rowconfigure(5, weight=1)

        # 加载历史记录到列表框
        self.load_history_into_listbox()

    def load_history_into_listbox(self):
        """
        将历史记录加载到列表框中显示。
        """
        self.history_listbox.delete(0, tk.END)
        for idx, record in enumerate(self.history, start=1):
            display_text = f"{idx}. 输入: {record['input_dir']} | 输出: {record['output_dir']}"
            self.history_listbox.insert(tk.END, display_text)

    def browse_input_directory(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.input_directory.set(selected_dir)

    def browse_output_directory(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.output_directory.set(selected_dir)

    def log(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')

    def start_compilation(self):
        input_dir = self.input_directory.get()
        output_dir = self.output_directory.get()

        if not input_dir or not os.path.isdir(input_dir):
            messagebox.showerror("错误", "请指定一个有效的源代码目录。")
            return

        if not output_dir or not os.path.isdir(output_dir):
            messagebox.showerror("错误", "请指定一个有效的输出目录。")
            return

        # 防止输出目录是源代码目录的子目录
        try:
            common_path = os.path.commonpath([input_dir, output_dir])
            if common_path == input_dir:
                messagebox.showerror("错误", "输出目录不能是源代码目录的子目录。")
                return
        except ValueError:
            # 没有公共路径，忽略
            pass

        # 禁用按钮，防止多次点击
        self.compile_button.config(state='disabled')
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')

        # 运行编译过程在一个单独的线程，以避免冻结 GUI
        threading.Thread(target=self.compile_all_py_files, args=(input_dir, output_dir), daemon=True).start()

    def compile_all_py_files(self, input_dir, output_dir):
        py_files = find_py_files(input_dir)
        if not py_files:
            self.log("未在指定源代码目录中找到任何 .py 文件。\n")
            self.compile_button.config(state='normal')
            return

        self.log(f"找到 {len(py_files)} 个 .py 文件，开始编译...\n")

        for py_file in py_files:
            self.log(f"编译 {py_file} ...\n")
            success = compile_py_file(py_file, output_dir, input_dir, log_callback=self.log)
            if success:
                self.log(f"成功编译 {py_file} 为 .pyd 文件。\n")
            else:
                self.log(f"编译 {py_file} 失败。\n")

        self.log("编译过程完成。\n")
        self.compile_button.config(state='normal')

        # 添加到历史记录
        add_to_history(input_dir, output_dir, self.history)
        self.load_history_into_listbox()

    def use_selected_history(self):
        """
        使用选定的历史记录，将其输入和输出目录设置为当前选择。
        """
        selected_indices = self.history_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("警告", "请选择一条历史记录。")
            return
        index = selected_indices[0]
        record = self.history[index]
        self.input_directory.set(record['input_dir'])
        self.output_directory.set(record['output_dir'])

    def delete_selected_history(self):
        """
        删除选定的历史记录。
        """
        selected_indices = self.history_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("警告", "请选择一条历史记录。")
            return
        index = selected_indices[0]
        confirm = messagebox.askyesno("确认删除", "确定要删除选定的历史记录吗？")
        if confirm:
            del self.history[index]
            save_history(self.history)
            self.load_history_into_listbox()
            self.log("已删除选定的历史记录。\n")


def main():
    root = tk.Tk()
    app = PyToPydConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
