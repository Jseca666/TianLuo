from pathlib import Path

from .core_actions_runtime_ready_readiness_summary import CoreActionsRuntimeReadyReadinessSummary


class CoreActionsRuntimeReadyReadinessAnalyzer:
    def analyze(self, task_specs: list[dict], export_payload: dict) -> CoreActionsRuntimeReadyReadinessSummary:
        project_root = self._project_root(export_payload)
        task_files = self._task_files(export_payload)
        task_ids = list(task_files.keys())

        expected_tap_steps = 0
        expected_swipe_steps = 0
        expected_back_steps = 0
        expected_sleep_steps = 0
        for spec in task_specs:
            for call in spec.get("api_calls", []) or []:
                api_name = str(call.get("api_name", ""))
                if api_name in {"tap_point", "tap", "tap_xy", "tap_coordinate", "click_point", "click_xy"}:
                    expected_tap_steps += 1
                elif api_name in {"swipe_points", "swipe", "swipe_xy", "swipe_points_xy"}:
                    expected_swipe_steps += 1
                elif api_name in {"back", "back_key", "press_back", "go_back"}:
                    expected_back_steps += 1
                elif api_name in {"sleep", "sleep_seconds", "wait_seconds", "sleep_ms", "wait_ms", "delay_ms"}:
                    expected_sleep_steps += 1

        generated_tap_count = 0
        generated_swipe_count = 0
        generated_back_count = 0
        generated_delay_count = 0
        generated_fail_checks_count = 0
        task_file_counts = {}
        notes = []

        for task_id, file_path in task_files.items():
            path = Path(file_path)
            if not path.exists():
                notes.append(f"Task file missing for core-actions runtime-ready readiness analysis: {path}")
                continue
            text = path.read_text(encoding="utf-8")
            tap_count = text.count("gestureEngine.tap(")
            swipe_count = text.count("gestureEngine.swipe(")
            back_count = text.count("gestureEngine.back()")
            delay_count = text.count("kotlinx.coroutines.delay(")
            fail_checks = text.count("TaskResult.fail(")
            generated_tap_count += tap_count
            generated_swipe_count += swipe_count
            generated_back_count += back_count
            generated_delay_count += delay_count
            generated_fail_checks_count += fail_checks
            task_file_counts[task_id] = {
                "tap": tap_count,
                "swipe": swipe_count,
                "back": back_count,
                "delay": delay_count,
                "fail_checks": fail_checks,
            }

        if generated_tap_count >= expected_tap_steps and expected_tap_steps > 0:
            notes.append("Generated code covers expected tap_point steps")
        if generated_swipe_count >= expected_swipe_steps and expected_swipe_steps > 0:
            notes.append("Generated code covers expected swipe_points steps")
        if generated_back_count >= expected_back_steps and expected_back_steps > 0:
            notes.append("Generated code covers expected back steps")
        if generated_delay_count >= expected_sleep_steps and expected_sleep_steps > 0:
            notes.append("Generated code covers expected sleep steps")
        if generated_fail_checks_count >= expected_tap_steps + expected_swipe_steps + expected_back_steps:
            notes.append("Generated code includes runtime failure checks for interactive core actions")

        return CoreActionsRuntimeReadyReadinessSummary(
            project_root=project_root,
            task_count=len(task_ids),
            task_ids=task_ids,
            expected_tap_steps=expected_tap_steps,
            expected_swipe_steps=expected_swipe_steps,
            expected_back_steps=expected_back_steps,
            expected_sleep_steps=expected_sleep_steps,
            generated_tap_count=generated_tap_count,
            generated_swipe_count=generated_swipe_count,
            generated_back_count=generated_back_count,
            generated_delay_count=generated_delay_count,
            generated_fail_checks_count=generated_fail_checks_count,
            task_file_counts=task_file_counts,
            files=task_files,
            notes=notes,
        )

    def _project_root(self, export_payload: dict) -> str:
        result = export_payload.get("result")
        if result is not None and getattr(result, "project_root", None):
            return str(getattr(result, "project_root"))
        summary = export_payload.get("summary")
        if summary is not None and getattr(summary, "project_root", None):
            return str(getattr(summary, "project_root"))
        return ""

    def _task_files(self, export_payload: dict) -> dict[str, str]:
        result = export_payload.get("result")
        if result is not None:
            write_result = getattr(result, "write_result", None)
            if write_result is not None:
                task_files = getattr(write_result, "task_files", None)
                if isinstance(task_files, dict):
                    return dict(task_files)
        summary = export_payload.get("summary")
        if summary is not None:
            task_ids = list(getattr(summary, "task_ids", []) or [])
            files = dict(getattr(summary, "files", {}) or {})
            return {task_id: str(files.get(task_id, "")) for task_id in task_ids if files.get(task_id)}
        return {}
