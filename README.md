# Paddie。

[![CodeFactor](https://www.codefactor.io/repository/github/c4nu/paddie/badge/main)](https://www.codefactor.io/repository/github/c4nu/paddie/overview/main~)
![Stable Version](https://img.shields.io/badge/stable-v3.1.1-blue?style=flat)
[![Github All Releases](https://img.shields.io/github/downloads/c4nu/paddie/total.svg)]()

## Version
### Python Version
![Python 3.10.11](https://img.shields.io/badge/Python-3.10.11-yellow?style=flat)
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
pyinstaller --windowed --onefile --add-data --noconfirm --clean --name "Paddie" --icon "resources\icon.ico" --hidden-import PyQt6 "resources\ui;resources\ui" --add-data "resources\fonts;resources\fonts" --add-data "resources\model_map.csv;resources" --add-data "resources\user_data.json;resources" --add-data "resources\Barlow-Light.ttf;resources" src\main.py
```
#### 폰트 추가 기능 O
```python
pyinstaller --noconfirm --clean --name "Paddie" --icon "resources\icon.ico" --hidden-import PyQt6 --add-data "resources\ui;ui" --add-data "resources\fonts;fonts" --add-data "resources\model_map.csv;model_map" --add-data "resources\user_data.json;user_data" --add-data "resources\Barlow-Light.ttf;Barlow-Light" src\main.py
```
### macOS

```python
#Paddie.spec 파일로 빌드 가능
pyinstaller --windowed --noconfirm --clean \
--name "Paddie" \
--icon resources/icon.icns \
--add-data "resources/ui:ui" \
--add-data "resources/fonts:fonts" \
--add-data "resources/model_map.csv:model_map" \
--add-data "resources/user_data.json:user_data" \
--add-data "resources/Barlow-Light.ttf:Barlow-Light" \
--target-arch universal2 \ # Universal 앱 빌드
src/main.py
```
## 라이선스
| 라이선스 항목      | 설                                                            |
|--------------|--------------------------------------------------------------|
| 아이콘          | <a href=“https://www.flaticon.com/kr/free-icons/“ title=“폴라로이드 아이콘”>폴라로이드 아이콘 제작자: Ekros - Flaticon</a> |
| Barlow-Light |                                                              |
| LineSeedKR   | 넣을 예정                                                        |
| Qt6          |                                                              |


