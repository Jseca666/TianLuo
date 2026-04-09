from pathlib import Path


class MaskFileResolver:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def resolve(self) -> Path | None:
        masks_file = self.repo_root / 'tool' / 'masks.json'
        if masks_file.exists():
            return masks_file
        return None
