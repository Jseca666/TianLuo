# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import shutil
from PyInstaller.utils.hooks import collect_submodules

# 获取项目根目录
project_dir = os.path.abspath('E:\\PyProjects\\text2')

# 虚拟环境的 site-packages 目录
site_packages_dirs = [os.path.join(project_dir, '.venv', 'Lib', 'site-packages')]


a = Analysis(
    ['RC_ui.py'],
    pathex=[
        project_dir
        # 如果需要，可以在这里添加更多路径
    ],
    binaries=[],
    datas=[
        # 在这里添加需要包含的数据文件或文件夹
        # 例如：(os.path.join(project_dir, 'assignment'), 'assignment'),
        #       (os.path.join(project_dir, 'tool'), 'tool')
    ],
    hiddenimports=[
        # 根据需要添加隐藏导入的模块
    ],
    hookspath=[
        # 根据需要添加自定义的 hook 文件路径
    ],
    runtime_hooks=[],
    excludes=[
        # 根据需要排除不需要的模块
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RC_ui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # 如果是 GUI 应用，设置为 False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RC_ui',
)

# 自定义步骤：复制 site-packages 到 dist/RC_ui/_internal
def copy_site_packages():
    source_dirs = site_packages_dirs  # 这是一个列表
    dist_dir = os.path.join('dist', 'RC_ui', '_internal')

    # 如果目标目录不存在，则创建
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
        print(f"创建目标目录：{dist_dir}")

    # 遍历每个 source_dir
    for source_dir in source_dirs:
        if not os.path.exists(source_dir):
            print(f"源目录不存在：{source_dir}")
            continue

        # 遍历 source_dir 中的所有文件和文件夹
        for root, dirs, files in os.walk(source_dir):
            # 计算相对于 source_dir 的路径
            rel_path = os.path.relpath(root, source_dir)
            dest_root = os.path.join(dist_dir, rel_path)

            # 创建目标子目录
            for dir_ in dirs:
                dest_sub_dir = os.path.join(dest_root, dir_)
                if not os.path.exists(dest_sub_dir):
                    os.makedirs(dest_sub_dir)
                    print(f"创建子目录：{dest_sub_dir}")

            # 复制文件
            for file_ in files:
                source_file = os.path.join(root, file_)
                dest_file = os.path.join(dest_root, file_)
                try:
                    shutil.copy2(source_file, dest_file)  # copy2 保留元数据
                    print(f"复制文件：{source_file} -> {dest_file}")
                except Exception as e:
                    print(f"复制文件失败：{source_file} -> {dest_file}\n错误信息：{e}")

# 调用复制函数
copy_site_packages()
