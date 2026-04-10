from pathlib import Path
import json

from .delivery_ready_compilable_runtime_project_delivery_serializer import DeliveryReadyCompilableRuntimeProjectDeliverySerializer


class DeliveryReadyCompilableRuntimeProjectDeliveryWriter:
    def write(self, result: dict, output_dir: Path) -> str:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / 'delivery_ready_compilable_runtime_delivery.json'
        path.write_text(
            json.dumps(
                DeliveryReadyCompilableRuntimeProjectDeliverySerializer.to_dict(result),
                ensure_ascii=False,
                indent=2,
            ),
            encoding='utf-8',
        )
        return str(path)
