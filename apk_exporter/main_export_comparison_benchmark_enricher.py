class MainExportComparisonBenchmarkEnricher:
    def enrich(self, task_specs: list[dict], comparison_result: dict) -> dict:
        expected_task_ids = [str(spec.get("task_id", "")) for spec in task_specs if spec.get("task_id")]

        baseline = comparison_result.get("baseline", {})
        quality = comparison_result.get("quality", {})
        summary = comparison_result.get("summary")

        baseline_summary = baseline.get("summary")
        quality_summary = quality.get("summary")
        baseline_validation = baseline.get("deep_validation")
        quality_validation = quality.get("deep_validation")

        baseline_task_ids = list(getattr(baseline_summary, "task_ids", []) or [])
        quality_task_ids = list(getattr(quality_summary, "task_ids", []) or [])

        expected_set = set(expected_task_ids)
        baseline_set = set(baseline_task_ids)
        quality_set = set(quality_task_ids)

        shared_task_ids = [task_id for task_id in expected_task_ids if task_id in baseline_set and task_id in quality_set]
        baseline_only_task_ids = sorted(baseline_set - quality_set)
        quality_only_task_ids = sorted(quality_set - baseline_set)
        missing_in_baseline = [task_id for task_id in expected_task_ids if task_id not in baseline_set]
        missing_in_quality = [task_id for task_id in expected_task_ids if task_id not in quality_set]

        notes = []
        if len(baseline_task_ids) == len(expected_task_ids):
            notes.append("Baseline export keeps expected task count")
        if len(quality_task_ids) == len(expected_task_ids):
            notes.append("Quality export keeps expected task count")
        if not missing_in_baseline:
            notes.append("Baseline export keeps expected task ids")
        if not missing_in_quality:
            notes.append("Quality export keeps expected task ids")
        if getattr(summary, "quality_unsupported_count", 0) < getattr(summary, "baseline_unsupported_count", 0):
            notes.append("Quality export reduces unsupported count on benchmark set")
        if getattr(summary, "quality_todo_count", 0) < getattr(summary, "baseline_todo_count", 0):
            notes.append("Quality export reduces TODO count on benchmark set")
        if getattr(baseline_validation, "is_valid", False):
            notes.append("Baseline benchmark export passes deep validation")
        if getattr(quality_validation, "is_valid", False):
            notes.append("Quality benchmark export passes deep validation")

        return {
            "expected_task_count": len(expected_task_ids),
            "expected_task_ids": expected_task_ids,
            "baseline_task_count": len(baseline_task_ids),
            "quality_task_count": len(quality_task_ids),
            "baseline_task_ids": baseline_task_ids,
            "quality_task_ids": quality_task_ids,
            "shared_task_ids": shared_task_ids,
            "baseline_only_task_ids": baseline_only_task_ids,
            "quality_only_task_ids": quality_only_task_ids,
            "missing_in_baseline": missing_in_baseline,
            "missing_in_quality": missing_in_quality,
            "baseline_todo_count": getattr(summary, "baseline_todo_count", 0) if summary else 0,
            "quality_todo_count": getattr(summary, "quality_todo_count", 0) if summary else 0,
            "baseline_unsupported_count": getattr(summary, "baseline_unsupported_count", 0) if summary else 0,
            "quality_unsupported_count": getattr(summary, "quality_unsupported_count", 0) if summary else 0,
            "baseline_asset_file_count": getattr(summary, "baseline_asset_file_count", 0) if summary else 0,
            "quality_asset_file_count": getattr(summary, "quality_asset_file_count", 0) if summary else 0,
            "baseline_validation_ok": getattr(baseline_validation, "is_valid", False),
            "quality_validation_ok": getattr(quality_validation, "is_valid", False),
            "notes": notes,
            "comparison_report_files": getattr(summary, "files", {}) if summary else {},
        }
