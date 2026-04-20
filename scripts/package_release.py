import argparse
import os
import tarfile
import zipfile
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT_DIR / "dist"
OUTPUT_DIR = ROOT_DIR / "release-artifacts"


def main():
    parser = argparse.ArgumentParser(description="Package a PyInstaller build artifact.")
    parser.add_argument("--artifact-name", required=True, help="Archive name without extension.")
    parser.add_argument("--format", choices=("zip", "tar.gz"), required=True)
    args = parser.parse_args()

    source_path = find_build_output()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.format == "zip":
        archive_path = OUTPUT_DIR / f"{args.artifact_name}.zip"
        write_zip(source_path, archive_path)
    else:
        archive_path = OUTPUT_DIR / f"{args.artifact_name}.tar.gz"
        write_tar(source_path, archive_path)

    print(archive_path)


def find_build_output():
    app_bundle = DIST_DIR / "Paddie.app"
    app_folder = DIST_DIR / "Paddie"
    app_exe = DIST_DIR / "Paddie.exe"

    for path in (app_bundle, app_folder, app_exe):
        if path.exists():
            return path

    raise FileNotFoundError("No PyInstaller output found under dist/.")


def write_zip(source_path, archive_path):
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        if source_path.is_file():
            archive.write(source_path, source_path.name)
            return

        for path in source_path.rglob("*"):
            archive.write(path, Path(source_path.name) / path.relative_to(source_path))


def write_tar(source_path, archive_path):
    with tarfile.open(archive_path, "w:gz") as archive:
        archive.add(source_path, arcname=os.fspath(source_path.name))


if __name__ == "__main__":
    main()
