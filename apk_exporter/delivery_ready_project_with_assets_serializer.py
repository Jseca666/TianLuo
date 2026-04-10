class DeliveryReadyProjectWithAssetsSerializer:
    @staticmethod
    def to_dict(result) -> dict:
        delivery = result.delivery
        assets = result.assets
        metadata = result.metadata
        return {
            "delivery": {
                "report_path": delivery.get("report_path"),
                "delivery_report_path": delivery.get("delivery_report_path"),
                "summary": {
                    "project_root": getattr(delivery.get("summary"), "project_root", "") if delivery.get("summary") else "",
                    "task_count": getattr(delivery.get("summary"), "task_count", 0) if delivery.get("summary") else 0,
                    "task_ids": getattr(delivery.get("summary"), "task_ids", []) if delivery.get("summary") else [],
                    "files": getattr(delivery.get("summary"), "files", {}) if delivery.get("summary") else {},
                },
            },
            "assets": {
                "manifest_path": assets.get("manifest_path"),
                "copied_files": assets.get("copied_files", []),
                "summary": assets.get("summary", {}),
            },
            "metadata": metadata,
        }
