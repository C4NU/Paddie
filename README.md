# Paddie。

[![CodeFactor](https://www.codefactor.io/repository/github/c4nu/paddie/badge/main)](https://www.codefactor.io/repository/github/c4nu/paddie/overview/main)
![Stable Version](https://img.shields.io/badge/stable-v3.1.1-blue?style=flat)
[![Github All Releases](https://img.shields.io/github/downloads/c4nu/paddie/total.svg)]()

## Version
### Python Version
![Python 3.10.11](https://img.shields.io/badge/Python-3.10.11-yellow?style=flat)
### Module Version
![PyQt6](https://img.shields.io/badge/PyQt-NULL-green?style=flat)
![Pillows](https://img.shields.io/badge/Pillows-NULL-yellow?style=flat)
![Pyinstaller](https://img.shields.io/badge/Pyinstaller-NULL-red?style=flat)

## Description

A program that compresses image files into WebP format, or reads EXIF data and writes it to the image border.

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

```python
# Windows
pyinstaller -w -F -n=Paddie --icon='Resources/Icon@64X64_02.ico' --hidden-import PyQt6 main.py       

# macOS
pyinstaller -w -F -n=Paddie --icon='Resources/Icon@64X64_02.ico' --hidden-import PyQt6 main.py   
```




- -w
  - 터미널 없이 프로그램 형태로 실행
- -F
  - 프로그램 하나의 파일로 묶음 (.app / .exe)
- -n
  - 프로그램 이름
- --icon
  - Resources 폴더 안에있는 ico 파일로 아이콘 표시

## Used Resources
1. Barlow-Light Fonts
