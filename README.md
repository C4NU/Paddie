# Paddie。

[![CodeFactor](https://www.codefactor.io/repository/github/c4nu/paddie/badge/main)](https://www.codefactor.io/repository/github/c4nu/paddie/overview/main)
![Stable Version](https://img.shields.io/badge/stable-v3.1.1-blue?style=flat)
[![Github All Releases](https://img.shields.io/github/downloads/c4nu/paddie/total.svg)]()

## Version
### Python Version
![Python 3.10.11](https://img.shields.io/badge/Python-3.10.11-yellow?style=flat)
### Module Version
![PyQt6](https://img.shields.io/badge/PyQt-6.5.3-green?style=flat)
![Pillows](https://img.shields.io/badge/Pillows-10.0.0-yellow?style=flat)
![Pyinstaller](https://img.shields.io/badge/Pyinstaller-6.3.0-red?style=flat)

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
pyinstaller -w -F -n=Paddie --icon='resources/Paddie-Icon.icns' --hidden-import PyQt6 main.py       

# macOS
pyinstaller -w -F -n=Paddie --icon='resources/Paddie-Icon.icns' --hidden-import PyQt6 main.py   
```




- -w
  - 터미널 없이 프로그램 형태로 실행
- -F
  - 프로그램 하나의 파일로 묶음 (.app / .exe)
- -n
  - 프로그램 이름
- --icon
  - resources 폴더 안에있는 ico 파일로 아이콘 표시

## LICENCE
1. ICON: <a href="https://www.flaticon.com/kr/free-icons/" title="폴라로이드 아이콘">폴라로이드 아이콘 제작자: Ekros - Flaticon</a>
2. FONT FILE: Barlow-Light
