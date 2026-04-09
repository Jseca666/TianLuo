from pathlib import Path

from .path_normalizer import PathNormalizer


class TemplatePathResolver:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.tool_root = self.repo_root / 'tool'

    def resolve(self, image_path: str) -> Path:
        normalized = PathNormalizer.normalize_asset_path(image_path)
        return self.tool_root / normalized
