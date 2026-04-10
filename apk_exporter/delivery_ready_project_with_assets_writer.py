from pathlib import Path
import json

from .delivery_ready_project_with_assets_serializer import DeliveryReadyProjectWithAssetsSerializer


class DeliveryReadyProjectWithAssetsWriter:
    def write(self, result, output_dir: Path) -> str:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / 'delivery_ready_project_with_assets.json'
        path.write_text(
            json.dumps(
                DeliveryReadyProjectWithAssetsSerializer.to_dict(result),
                ensure_ascii=False,
                indent=2,
            ),
            encoding='utf-8',
        )
        return str(path)
