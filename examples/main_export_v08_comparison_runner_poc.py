from pathlib import Path

from apk_exporter.main_export_v08_comparison_runner import run


def main():
    repo_root = Path(__file__).resolve().parents[1]
    print(run(repo_root))


if __name__ == "__main__":
    main()
