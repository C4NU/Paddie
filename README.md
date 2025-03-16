# Paddie。

[![CodeFactor](https://www.codefactor.io/repository/github/c4nu/paddie/badge/main)](https://www.codefactor.io/repository/github/c4nu/paddie/overview/main~)
![Stable Version](https://img.shields.io/badge/stable-v3.4.0-blue?style=flat)
[![Github All Releases](https://img.shields.io/github/downloads/c4nu/paddie/total.svg)]()

## Version
### Python Version
![Python 3](https://img.shields.io/badge/Python-3-yellow?style=flat)
### Module Version
![PyQt6](https://img.shields.io/badge/PyQt-6.5.3-green?style=flat)
![Pillows](https://img.shields.io/badge/Pillows-10.0.0-yellow?style=flat)
![Pyinstaller](https://img.shields.io/badge/Pyinstaller-6.3.0-red?style=flat)

## 기능
| 이름       | 설명                                                           |
|----------|--------------------------------------------------------------|
| 리사이징     | 이미지 해상도 리사이징 기능                                              |
| WebP 변환  | - 이미지파일 -> WebP 변환 기능<br>   - 무손실 옵션<br>   - 이미지 퀄리티 옵션<br>   - 변환시 EXIF 데이터 저장 옵션<br>   - 변환시 ICC 프로파일 저장 옵션<br>   - 변환시 RGBA 데이터 저장 옵션 |
| EXIF 프레임 | - EXIF 데이터가 존재하는 이미지파일에 카메라 정보를 기입하는 기능<br>   - JPG \| PNG \| WebP 형태로 저장 가능, 이미지 퀄리티 선택 기능<br>   - 패딩 없음 \| 하단부 패딩 \| 전체 패딩 선택 기능<br>   - 정방형 비율 \| 4:5 비율 선택 기능<br>   - 카메라 기종 \| 렌즈 이름 \| 초점 거리 \| 조리개 \| ISO \| 셔터스피드 기입 기능<br>   - 기입 폰트 선택 기능 \| 폰트 추가 기능<br>   - 텍스트 색상 및 프레임 색상 선택 기능<br>   - 왼쪽 \| 중간 \| 오른쪽 텍스트 위치 선택 기능 |

| 명령어                             | 기능 설명                             |
|---------------------------------|-----------------------------------|
| {body}                          | 카메라 바디 정보                         |
| {lens}                          | 카메라 렌즈 정보                         |
| {focal_f}                       | ?                                 |
| {iso}                           | 촬영 ISO 정보                         |
| {ss}                            | 촬영 셔터스피드 정보                       |
| {focal}                         | 촬영 초점 거리 정보                       |
| {aper}                          | 촬영 조리개 정보                         |
| {ev}                            | 촬영 노출값 정보                         |
| {meter}                         | ?                                 |
| {mode}<br>{mode_s}<br>{mode_cr} | 촬영 모드 정보<br>- _s: 소니<br>- _cr: 캐논 |
| {time}                          | 촬영 타임스탬프 정보                       |
| {wb}                            | 촬영 화이트밸런스 정보                      |
| {cr}<br>{ar}                    | 저작권 정보                            |
| {mf}                            | 카메라 제조사 정보                        |
| {mf_l}                          | 렌즈 제조사 정보                         |

## 빌드
윈도우 및 macOS 빌드 방법이 다릅니다. (파일 경로 문제)
각 OS 별 빌드 방법에 맞춰주세요.
### 공통
| 순서  | 내용           |
|-----|--------------|
| 1   | Python 설치    |
| 2   | pip install  |
| 3   |              |
| 4   | dist 폴더 확인   |
### Windows
#### 폰트 추가 기능 X
```python
pyinstaller --windowed --onefile --noconfirm --clean --name "Paddie" --icon "resources\icon.ico" --hidden-import PyQt6 "resources\ui;resources\ui" --add-data "resources\fonts;resources\fonts" --add-data "resources\model_map.csv;resources" --add-data "resources\user_data.json;resources" --add-data "resources\Barlow-Light.ttf;resources" src\main.py
```
#### 폰트 추가 기능 O
```python
pyinstaller --noconfirm --clean --name "Paddie" --icon "resources\icon.ico" --hidden-import PyQt6 --add-data "resources\ui;resources\ui" --add-data "resources\fonts;resources\fonts" --add-data "resources\model_map.csv;resources" --add-data "resources\user_data.json;resources" --add-data "resources\Barlow-Light.ttf;resources" src\main.py
```
### macOS

```python
#Paddie.spec 파일로 빌드 가능
pyinstaller --windowed --noconfirm --clean \
--hidden-import PyQt6 \
--name "Paddie" \
--icon resources/icon.icns \
--add-data "resources/ui:resources/ui" \
--add-data "resources/fonts:resources/fonts" \
--add-data "resources/model_map.csv:resources" \
--add-data "resources/user_data.json:resources" \
--add-data "resources/Barlow-Light.ttf:resources" \
--add-binary "/opt/homebrew/lib/libzstd.1.dylib:."
--osx-bundle-identifier "com.canu.paddie" \
src/main.py
```
빌드 후 Paddie.spec 파일의 BUNDLE 항목에 version='버전명' 추가.
## 라이선스
| 라이선스 항목      | 설                                                            |
|--------------|--------------------------------------------------------------|
| 아이콘          | <a href=“https://www.flaticon.com/kr/free-icons/“ title=“폴라로이드 아이콘”>폴라로이드 아이콘 제작자: Ekros - Flaticon</a> |
| Barlow-Light |                                                              |
| LineSeedKR   | 넣을 예정                                                        |
| Qt6          |                                                              |


