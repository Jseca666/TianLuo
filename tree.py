import os

def print_directory_tree(root_dir, prefix=''):
    """
    递归打印目录树结构，排除 .venv 目录。

    Args:
        root_dir (str): 要遍历的根目录路径。
        prefix (str): 当前前缀，用于格式化树结构。
    """
    # 获取目录中的所有项目，并排序
    try:
        items = sorted(os.listdir(root_dir))
    except PermissionError:
        print(prefix + "└── [权限不足]")
        return

    # 遍历每个项目
    exculed=['.venv','hooks']
    for index, item in enumerate(items):
        # 跳过 .venv 目录
        if item in '.venv':
            continue

        path = os.path.join(root_dir, item)
        # 判断是否为最后一个项目
        is_last = index == len(items) - 1
        # 选择连接符
        connector = '└── ' if is_last else '├── '
        print(prefix + connector + item)

        # 如果是目录，则递归调用
        if os.path.isdir(path):
            # 根据是否为最后一个项目，决定下一层的前缀
            extension = '    ' if is_last else '│   '
            print_directory_tree(path, prefix + extension)

def main():
    """
    主函数，获取当前工作目录并打印其目录树结构。
    """
    current_dir = os.getcwd()
    project_name = os.path.basename(current_dir)
    print(project_name + '/')
    print_directory_tree(current_dir)

if __name__ == '__main__':
        main()
