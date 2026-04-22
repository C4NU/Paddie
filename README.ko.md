# Paddie。

[![CodeFactor](https://www.codefactor.io/repository/github/c4nu/paddie/badge/main)](https://www.codefactor.io/repository/github/c4nu/paddie/overview/main)

![Stable Version](https://img.shields.io/badge/stable-v3.4.1-blue?style=flat)

[![Github All Releases](https://img.shields.io/github/downloads/c4nu/paddie/total.svg)]()

## Package Version

Python 3.11 for release builds

PySide6 6.10.3

Pillow 11.1.0

PyInstaller 6.12.0

## Description

JPG, PNG등의 이미지 사진을 변환시켜주는 프로그램.

### Functions

1. JPG, PNG, TIFF 이미지 파일을 WebP로 변환시키는 기능.
   1. Loseless Option
   2. Image Quality Option
   3. Save Exif Option
   4. Save ICC Profile Option
   5. Save RGBA data(?) Option
2. EXIF 데이터가 존재하는 이미지파일을 레터박스를 씌워 JPG / PNG / WebP 형태로 저장시키는 기능
   1. 아무튼 여러가지 옵션 있음 ㅅㄱ


## Build

```bash
python -m pip install -r src/requirements.txt
python -m compileall -q src docs scripts
python scripts/build_release.py
python scripts/package_release.py --artifact-name Paddie-local --format zip
```




GitHub Actions는 태그 `v*` push 또는 수동 실행으로 macOS Intel,
macOS Apple Silicon, Windows x64, Linux x64 산출물을 빌드합니다.
태그 빌드에서는 산출물을 첨부한 draft release를 생성합니다.
