import json
from dataclasses import asdict

from .export_manifest import ExportManifest


class ExportManifestSerializer:
    @staticmethod
    def to_dict(manifest: ExportManifest) -> dict:
        return asdict(manifest)

    @staticmethod
    def to_json(manifest: ExportManifest, ensure_ascii: bool = False, indent: int = 2) -> str:
        return json.dumps(
            ExportManifestSerializer.to_dict(manifest),
            ensure_ascii=ensure_ascii,
            indent=indent,
        )
