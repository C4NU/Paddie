# WebP Converter GUI

Python 3.10.11

## Description

파이썬으로 작성된 JPG, PNG등의 이미지 사진을 WebP로 변환해주는 GUI 변환기

## Windows 빌드할 때 (pyinstaller)
### 1. EXE 빌드
pyinstaller -w -F 'C:\Users\canu1\Documents\Development\#1 Python Projects\WebPConverterGUI\main.py' --icon=.\Resources\Icon@64X64_02.ico -n='WebP Converter'

### 2. .spec 파일 수정
...
    datas=[('WebPConverterGUI.ui', '.')],
...

### 3. .spec 파일로 다시 빌드
pyinstaller.exe "WebP Converter.spec"