import argparse
import os
import platform
import subprocess  # nosec B404
import sys
import tempfile
from pathlib import Path


APP_NAME = "Paddie"
APP_ID = "com.canu.paddie"
ROOT_DIR = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(
        description="Build Paddie with PyInstaller.",
    )
    parser.add_argument(
        "--onefile",
        action="store_true",
        help="Build a single executable instead of an app folder.",
    )
    args = parser.parse_args()

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--windowed",
        "--name",
        APP_NAME,
        "--hidden-import",
        "PySide6.QtUiTools",
        "--exclude-module",
        "PyQt6",
        "--exclude-module",
        "PyQt5",
        "--exclude-module",
        "PyQt6.QtCore",
        "--exclude-module",
        "PyQt5.QtCore",
    ]

    if args.onefile:
        command.append("--onefile")

    icon_path = icon_for_platform()
    if icon_path is not None:
        command.extend(["--icon", str(icon_path)])

    if sys.platform == "darwin":
        command.extend(["--osx-bundle-identifier", APP_ID])

    for source, target in data_paths():
        command.extend(["--add-data", f"{source}{data_separator()}{target}"])

    command.append(str(ROOT_DIR / "src" / "main.py"))
    env = os.environ.copy()
    # Command arguments are fixed by this script; no user input is executed.
    with tempfile.TemporaryDirectory(
        prefix="paddie-pyinstaller-cache-",
    ) as cache_dir:
        env.setdefault("PYINSTALLER_CONFIG_DIR", cache_dir)
        subprocess.run(command, cwd=ROOT_DIR, check=True, env=env)  # nosec B603


def icon_for_platform():
    if sys.platform == "darwin":
        return ROOT_DIR / "resources" / "icons" / "icon.icns"
    if sys.platform == "win32":
        return ROOT_DIR / "resources" / "icons" / "icon.ico"

    png_icon = ROOT_DIR / "resources" / "icons" / "paddie.png"
    return png_icon if png_icon.exists() else None


def data_paths():
    resources = ROOT_DIR / "resources"
    return [
        (resources / "ui", "resources/ui"),
        (resources / "fonts", "resources/fonts"),
        (resources / "data", "resources/data"),
        (resources / "i18n", "resources/i18n"),
        (resources / "icons", "resources/icons"),
        (resources / "barlow-light.ttf", "resources"),
    ]


def data_separator():
    return ";" if platform.system() == "Windows" else ":"


if __name__ == "__main__":
    main()
