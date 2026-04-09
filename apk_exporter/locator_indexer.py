import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from .path_normalizer import PathNormalizer


@dataclass
class LocatorRecord:
    locator_name: str
    image_path: str
    source_file: str


@dataclass
class LocatorIndex:
    files: List[str] = field(default_factory=list)
    records: List[LocatorRecord] = field(default_factory=list)


class LocatorIndexer:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.location_root = self.repo_root / 'tool' / 'location'

    def scan(self) -> LocatorIndex:
        index = LocatorIndex()
        if not self.location_root.exists():
            return index

        for json_file in sorted(self.location_root.rglob('*.json')):
            index.files.append(str(json_file))
            for record in self._read_locator_file(json_file):
                index.records.append(record)
        return index

    def _read_locator_file(self, json_file: Path) -> List[LocatorRecord]:
        with open(json_file, 'r', encoding='utf-8') as fh:
            data: Dict[str, dict] = json.load(fh)

        records: List[LocatorRecord] = []
        for locator_name, payload in data.items():
            image_path = payload.get('image_path', '')
            if not image_path:
                continue
            records.append(
                LocatorRecord(
                    locator_name=str(locator_name),
                    image_path=PathNormalizer.normalize_asset_path(str(image_path)),
                    source_file=str(json_file),
                )
            )
        return records
