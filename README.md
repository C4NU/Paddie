# WebP Converter GUI

## Package Version

Python 3.10.11

PyQt5, Pillows

## Description

파이썬으로 작성된 JPG, PNG등의 이미지 사진을 WebP로 변환해주는 GUI 변환기

## Windows 빌드할 때 (pyinstaller)
### 1. EXE 빌드

#### 명령어

```python
pyinstaller -w -F 'main.py 경로' --icon=.\Resources\Icon@64X64_02.ico -n='빌드 exe 이름'
```

#### Sample

```python
pyinstaller -w -F 'C:\Users\canu1\Documents\Development\#1 Python Projects\WebPConverterGUI\main.py' --icon=.\Resources\Icon@64X64_02.ico -n='WebP Converter'
```

### 2. .spec 파일 수정
```
...
    datas=[('WebPConverterGUI.ui', '.')],
...
```

### 3. .spec 파일로 다시 빌드
```python
pyinstaller "WebP Converter.spec"
```

## macOS 빌드할 때 (pyinstaller)
### 1. app 빌드

#### 명령어

```python
pyinstaller -w -F '/Users/jeonhyojae/Dev/Python Projects/WebP-Converter-GUI/main.py' --icon=./Resources/Icon@64X64_02.ico -n='WebP Converter'
```

#### Sample

```python
pyinstaller -w -F '/Users/jeonhyojae/Dev/Python Projects/WebP-Converter-GUI/main.py' --icon=./Resources/Icon@64X64_02.ico -n='WebP Converter' -d all
```

### 2. .spec 파일 수정
    ...
        datas=[('WebPConverterGUI.ui', '.')],
    ...

### 3. .spec 파일로 다시 빌드

```python
pyinstaller "WebP Converter.spec"
```

워터마크 관련 구현 기능
1. 워터마크 폰트 고르는 기능
2. 워터마크 기본 폰트 설정
3. 워터마크 위치 조정, 폰트 크기 설정, 미리보기 지원?