# 현재 복구 메모

브랜치: `codex/recover-v3.4.1`
기준: `v3.4.1` (`b906a85`)

## 현재 상태

- 안정 버전인 `v3.4.1` 태그에서 직접 브랜치를 만들었다.
- 복구 작업을 추적하기 위해 `docs/`를 추가했다.
- 현재 앱은 PySide6 단일 UI 런타임 기준으로 전환했고, macOS PyInstaller 빌드까지 통과했다.

## 지금까지 확인한 내용

- 이슈 #66은 Windows에서 `program_data.json` 인코딩 오류가 난 뒤 출력 및 여러 기능에서 강제 종료가 발생한다고 보고했다.
- 이후 들어간 직접적인 인코딩 수정 커밋은 작고 합리적인 범위였다.
- 더 큰 불안정성은 같은 시기에 리소스 이동, 빌드 자동화, 설정/i18n, worker 변환, 업데이트 시스템, 이후 Flet 작업이 함께 섞이면서 생겼다.
- `program_data.json`은 `v3.4.1` 기준에는 없는 파일이므로, 메타데이터/버전 관리 방식을 의도적으로 다시 추가하기 전까지는 도입하지 않는다.

## 다음 단계

1. 새 빌드 산출물에서 파일 추가, 리사이즈 옵션, 저장 폴더 선택, 색상 선택, EXIF 분리 프리뷰를 실제 이미지로 스모크 테스트한다.
2. 언어 설정 UI는 별도 단계로 추가한다. 현재는 `UserConfig.language`와 시스템 언어 기준으로 앱 시작 시 번역 파일을 적용한다.
3. 업데이트 기능은 자동 설치가 아니라 GitHub Releases 최신 버전 확인과 브라우저 열기부터 구현한다.
4. `program_data.json`은 정보 창 메타데이터와 업데이트 확인이 필요해지는 시점에 읽기 전용 데이터 파일로 다시 도입한다.

## 적용한 변경

- `resources/data/model_map.csv`를 읽을 때 UTF-8 디코딩을 명시했다.
- `resources/data/user_data.json`을 읽고 쓸 때 UTF-8 인코딩/디코딩을 명시했다.
- `user_data.json` 입출력에 context manager를 적용해 파일 핸들이 닫히도록 했다.
- `src/exif_module.py`, `src/resize_module.py`의 정수 비교를 `is`에서 `==`로 바꿨다.
- 정보 창의 프로그램명, 버전, 연락처 표시값을 `v3.4.1` 기준으로 코드에서 보정했다.
- 기존 리소스를 `resources/data`, `resources/fonts`, `resources/icons`, `resources/ui` 구조로 재배치했다.
- EXIF 미리보기를 항상 별도 프리뷰 창으로 표시하도록 했다.
- UI 런타임을 PyQt6/PySide6 혼재 상태에서 PySide6 단일 의존성으로 정리했다.
- PySide6에서 `.ui` 파일을 읽기 위해 `QUiLoader` 기반 로더를 추가했다.
- `resources/i18n`의 Qt 번역 파일을 복원하고 앱 시작 시 시스템/설정 언어에 맞춰 `QTranslator`를 설치하도록 했다.
- `resources/ui/resizeoption.ui`의 중복 `stringlist` 태그를 제거해 PySide6 `QUiLoader`가 파일을 읽지 못하는 문제를 정리했다.
- PySide6에서 keyword 인자를 받지 않는 `QFileDialog`, `QColorDialog` static 호출을 positional 호출로 변경했다.

## 검증

- `python3 -m compileall -q src docs`가 통과했다.
- `resize_module` 단독 import가 통과했다.
- `ModelNameMapper.replace_model_name("ILCE-7RM3")`가 `A7RM3`로 매핑되는 것을 확인했다.
- 새 리소스 경로 `resources/ui/webpconvertergui.ui`, `resources/data/model_map.csv`, `resources/barlow-light.ttf`가 해석되는 것을 확인했다.
- `.venv/bin/pyinstaller`가 이전 프로젝트 경로를 가리키는 깨진 shebang 상태였고, 가상환경 빌드 의존성을 재설치해 현재 경로로 복구했다.
- `.venv/bin/python -m PyInstaller ... src/main.py`로 macOS 빌드가 완료되어 `dist/Paddie`, `dist/Paddie.app`이 생성됐다.
- 새 빌드 산출물 안의 `resizeoption.ui`에도 `stringlist` 태그가 제거된 것을 확인했다.
- 파일 열기/저장 폴더/색상 선택 대화상자 호출부가 PySide6 positional API 형태로 정리된 것을 확인했다.
- `python3 -m compileall -q src docs`와 `git diff --check`가 통과했다.
