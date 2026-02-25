# Paddie。

[![CodeFactor](https://www.codefactor.io/repository/github/c4nu/paddie/badge/main)](https://www.codefactor.io/repository/github/c4nu/paddie/overview/main)

![](https://img.shields.io/badge/stable-v3.4.2-blue?style=flat)

[![Github All Releases](https://img.shields.io/github/downloads/c4nu/paddie/total.svg)]()

## Package Version

Python 3.9+

PyQt6

Pillows

Pyinstaller

## Description

이미지 포맷 변환 및 EXIF 정보 기반 프레임(레터박스) 합성 프로그램.

### 주요 기능

1. **WebP 변환**: JPG, PNG, TIFF 등을 WebP로 일괄 변환 (무손실, 품질, EXIF/ICC 보존 옵션 제공)
2. **EXIF 프레임**: 사진 하단 또는 전체에 촬영 정보(바디, 렌즈, 설정값 등)가 포함된 프레임 합성
3. **멀티스레딩 지원**: 변환 작업 중 UI 멈춤 현상 없앰 및 진행률 실시간 표시
4. **다국어 지원**: 한국어, 영어, 일본어, 중국어 지원
5. **설정 UI**: 메인 화면 ⚙️ 버튼을 통해 언어 및 사용자 설정 직접 관리

## Build

### 자동 빌드 (추천)
```bash
python3 build_paddie.py
```

### 수동 빌드
```bash
# macOS
pyinstaller --windowed --noconfirm --clean \
--hidden-import PyQt6 \
--name "Paddie" \
--icon resources/icon.icns \
--add-data "resources/ui:resources/ui" \
--add-data "resources/fonts:resources/fonts" \
--add-data "resources/model_map.csv:resources" \
--add-data "resources/user_data.json:resources" \
--add-data "resources/Barlow-Light.ttf:resources" \
--add-binary "/opt/homebrew/lib/libzstd.1.dylib:." \
--osx-bundle-identifier "paddie_legacy" \
src/main.py
```
