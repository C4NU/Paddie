# Paddie。

[![CodeFactor](https://www.codefactor.io/repository/github/c4nu/paddie/badge/main)](https://www.codefactor.io/repository/github/c4nu/paddie/overview/main~)
![Stable Version](https://img.shields.io/badge/stable-v3.4.1-blue?style=flat)
[![Github All Releases](https://img.shields.io/github/downloads/c4nu/paddie/total.svg)]()

## Version
### Python Version
![Python 3](https://img.shields.io/badge/Python-3-yellow?style=flat)
### Module Version
![PySide6](https://img.shields.io/badge/PySide-6.10.3-green?style=flat)
![Pillows](https://img.shields.io/badge/Pillow-11.1.0-yellow?style=flat)
![Pyinstaller](https://img.shields.io/badge/PyInstaller-6.12.0-red?style=flat)

## 홍보
iOS / iPadOS / macOS를 지원하는 New Paddie가 출시되었습니다.

![Download 링크](https://apps.apple.com/us/app/paddie-%EA%B8%B0%EB%A1%9D%EC%9D%84-%EC%83%88%EA%B8%B0%EB%8A%94-%EC%82%AC%EC%A7%84-%ED%94%84%EB%A0%88%EC%9E%84/id6758503800?l=ko)

기존 Paddie 또한 Lite, 혹은 Legacy 버전으로 유지보수는 계속 진행됩니다.
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

로컬 빌드는 OS별 PyInstaller 옵션을 직접 입력하지 않고 공통 스크립트를 사용합니다.

```bash
python -m pip install -r src/requirements.txt
python -m compileall -q src docs scripts
python scripts/build_release.py
python scripts/package_release.py --artifact-name Paddie-local --format zip
```

GitHub Actions는 태그 `v*` push 또는 수동 실행으로 macOS Intel,
macOS Apple Silicon, Windows x64, Linux x64 산출물을 빌드합니다.
태그 빌드에서는 산출물을 첨부한 draft release를 생성합니다.
## 라이선스
| 라이선스 항목      | 설                                                            |
|--------------|--------------------------------------------------------------|
| 아이콘          | <a href=“https://www.flaticon.com/kr/free-icons/“ title=“폴라로이드 아이콘”>폴라로이드 아이콘 제작자: Ekros - Flaticon</a> |
| Barlow-Light |                                                              |
| LineSeedKR   | 넣을 예정                                                        |
| Qt for Python |                                                            |
