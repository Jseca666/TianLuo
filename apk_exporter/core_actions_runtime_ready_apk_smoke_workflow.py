from pathlib import Path

from .core_actions_runtime_ready_apk_smoke_summary import CoreActionsRuntimeReadyApkSmokeSummary
from .core_actions_runtime_ready_host_script_writer import CoreActionsRuntimeReadyHostScriptWriter
from .core_actions_runtime_ready_readiness_analyzer import CoreActionsRuntimeReadyReadinessAnalyzer
from .main_export_core_actions_runtime_ready_project_export_report_facade import MainExportCoreActionsRuntimeReadyProjectExportReportFacade


class CoreActionsRuntimeReadyApkSmokeWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.export_facade = MainExportCoreActionsRuntimeReadyProjectExportReportFacade(repo_root)
        self.readiness_analyzer = CoreActionsRuntimeReadyReadinessAnalyzer()
        self.host_script_writer = CoreActionsRuntimeReadyHostScriptWriter()

    def run(self, task_specs: list[dict], output_root: Path) -> dict:
        output_root = Path(output_root)
        export_result = self.export_facade.export(
            task_specs=task_specs,
            output_root=output_root / "project",
            project_name="GeneratedAndroidProjectCoreActionsRuntimeReadySmoke",
            report_output_dir=output_root / "reports",
        )
        readiness = self.readiness_analyzer.analyze(task_specs, export_result)
        project_root = Path(getattr(export_result.get("result"), "project_root", export_result.get("summary").project_root if export_result.get("summary") else output_root))
        host_scripts = self.host_script_writer.write(project_root)

        checks = {
            "generated_tap_covered": getattr(readiness, "generated_tap_count", 0) >= getattr(readiness, "expected_tap_steps", 0),
            "generated_swipe_covered": getattr(readiness, "generated_swipe_count", 0) >= getattr(readiness, "expected_swipe_steps", 0),
            "generated_back_covered": getattr(readiness, "generated_back_count", 0) >= getattr(readiness, "expected_back_steps", 0),
            "generated_delay_covered": getattr(readiness, "generated_delay_count", 0) >= getattr(readiness, "expected_sleep_steps", 0),
            "runtime_fail_checks_present": getattr(readiness, "generated_fail_checks_count", 0) >= (
                getattr(readiness, "expected_tap_steps", 0)
                + getattr(readiness, "expected_swipe_steps", 0)
                + getattr(readiness, "expected_back_steps", 0)
            ),
        }

        commands = [
            "bash host_tools/build_debug.sh",
            "bash host_tools/install_debug.sh",
            "bash host_tools/launch_main_activity.sh",
            "bash host_tools/smoke_core_actions_debug.sh",
        ]
        notes = []
        notes.extend(getattr(readiness, "notes", []) or [])
        notes.append("Host-side smoke scripts are prepared for local Gradle build, adb install, activity launch, and basic smoke log capture")

        smoke = CoreActionsRuntimeReadyApkSmokeSummary(
            project_root=str(project_root),
            package_name=host_scripts.get("package_name", ""),
            main_activity=host_scripts.get("main_activity", ""),
            apk_relative_path=host_scripts.get("apk_relative_path", ""),
            host_scripts=host_scripts,
            checks=checks,
            commands=commands,
            notes=notes,
        )
        return {
            "export_result": export_result,
            "readiness": readiness,
            "smoke": smoke,
        }
