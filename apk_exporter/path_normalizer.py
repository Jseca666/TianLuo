class PathNormalizer:
    """V3 路径规范化骨架。"""

    @staticmethod
    def normalize_asset_path(path: str) -> str:
        value = str(path).strip()
        value = value.replace(chr(92), '/')
        while value.startswith('./'):
            value = value[2:]
        return value
