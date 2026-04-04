from pathlib import Path
def find_project_root():
    """
    查找项目的根目录，假设项目根目录包含 'main.py' 文件。

    :return: 项目的根目录路径。
    """
    current_path = Path(__file__).resolve()

    # 向上递归查找，直到找到包含 'main.py' 的目录
    while current_path != current_path.parent:
        if (current_path / 'main.py').exists():
            print(current_path)
            return current_path
        current_path = current_path.parent

    raise FileNotFoundError("未能找到项目的根目录，请确保项目包含 'main.py' 文件")
