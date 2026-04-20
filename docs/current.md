# 현재 복구 메모

브랜치: `codex/recover-v3.4.1`
기준: `v3.4.1` (`b906a85`)

## 현재 상태

- 안정 버전인 `v3.4.1` 태그에서 직접 브랜치를 만들었다.
- 복구 작업을 추적하기 위해 `docs/`를 추가했다.
- 현재 앱은 PySide6 단일 UI 런타임 기준으로 전환했고, 공통 PyInstaller 빌드 스크립트와 GitHub Actions 릴리즈 빌드 workflow를 추가했다.

## 지금까지 확인한 내용

- 이슈 #66은 Windows에서 `program_data.json` 인코딩 오류가 난 뒤 출력 및 여러 기능에서 강제 종료가 발생한다고 보고했다.
- 이후 들어간 직접적인 인코딩 수정 커밋은 작고 합리적인 범위였다.
- 더 큰 불안정성은 같은 시기에 리소스 이동, 빌드 자동화, 설정/i18n, worker 변환, 업데이트 시스템, 이후 Flet 작업이 함께 섞이면서 생겼다.
- `program_data.json`은 `v3.4.1` 기준에는 없는 파일이므로, 메타데이터/버전 관리 방식을 의도적으로 다시 추가하기 전까지는 도입하지 않는다.

## 다음 단계

1. GitHub Actions를 원격에서 실행해 macOS Intel, macOS Apple Silicon, Windows x64, Linux x64 산출물이 모두 생성되는지 확인한다.
2. 새 빌드 산출물에서 파일 추가, 리사이즈 옵션, 저장 폴더 선택, 색상 선택, EXIF 분리 프리뷰를 실제 이미지로 스모크 테스트한다.
3. 실제 라이선스를 확정한 뒤 `LICENSE` 파일과 정보 창 라이선스 값을 갱신한다.
4. 자동 업데이트 설치는 별도 단계로 검토한다. 현재는 GitHub Releases 최신 버전 확인과 브라우저 열기까지만 구현한다.

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
- 분리 프리뷰 창은 생성된 프리뷰 이미지 크기를 기준으로 화면 안에 맞게 비율 축소하고, 사용자가 창 크기를 바꿀 수 없도록 고정했다.
- `Preferences` 메뉴에 언어 선택만 제공하는 최소 설정 창을 연결했다.
- 언어 변경 시 Qt 번역기를 즉시 교체하고 이미 로드된 `.ui` 창의 텍스트를 다시 번역하도록 했다.
- 영어는 `.ui` 원문 언어이므로 `translations_en.qm`을 설치하지 않고 번역기를 제거한 상태로 표시한다.
- 미완성 번역이 빈 문자열을 반환하는 경우 메뉴/버튼이 사라지지 않도록 `.ui` 원문 텍스트로 fallback한다.
- macOS 메뉴 재배치가 번역 문자열에 따라 달라지지 않도록 `Preferences`, `Information`, `Exit` 액션에 Qt menu role을 명시했다.
- 정보 창을 고정 좌표 `.ui` 레이아웃에서 아이콘, 설명, 버전 배지, 메타데이터 패널을 가진 코드 기반 레이아웃으로 교체했다.
- 정보 창 메타데이터에 라이선스 행을 추가했다. 현재 저장소에 라이선스 파일이 없어 `Unspecified`/`별도 명시 없음`으로 표시한다.
- 정보 창은 현재 언어 코드 기준으로 제목, 설명, 라벨, 닫기 버튼을 다시 적용한다.
- `PySide6`를 `6.10.3`으로 올려 `.venv`에서 발생하던 Qt `neon` 런타임 오류를 해소했다.
- PyInstaller/altgraph가 요구하는 `pkg_resources` 호환성을 위해 `setuptools==80.9.0`을 명시했다.
- 사용자 설정 저장 위치를 번들 내부 `resources/data/user_data.json`에서 OS별 사용자 설정 폴더로 옮겼다.
- `PADDIE_CONFIG_DIR` 환경변수로 테스트/CI 설정 저장 위치를 임시 폴더로 지정할 수 있게 했다.
- `scripts/build_release.py`와 `scripts/package_release.py`를 추가해 OS별 PyInstaller 옵션과 산출물 압축을 공통화했다.
- `.github/workflows/build-release.yml`을 추가해 태그 `v*` push 또는 수동 실행으로 4개 플랫폼 산출물을 만들고, 태그 빌드에서는 draft release를 생성하도록 했다.
- `Options` 메뉴에 GitHub Releases 최신 버전 확인 항목을 추가했다. 새 버전이 있으면 릴리스 페이지를 열 수 있다.

## 검증

- `python3 -m compileall -q src docs`가 통과했다.
- `resize_module` 단독 import가 통과했다.
- `ModelNameMapper.replace_model_name("ILCE-7RM3")`가 `A7RM3`로 매핑되는 것을 확인했다.
- 새 리소스 경로 `resources/ui/webpconvertergui.ui`, `resources/data/model_map.csv`, `resources/barlow-light.ttf`가 해석되는 것을 확인했다.
- `.venv/bin/pyinstaller`가 이전 프로젝트 경로를 가리키는 깨진 shebang 상태였고, 가상환경 빌드 의존성을 재설치해 현재 경로로 복구했다.
- `.venv/bin/python -m PyInstaller ... src/main.py`로 macOS 빌드가 완료되어 `dist/Paddie`, `dist/Paddie.app`이 생성됐다.
- 새 빌드 산출물 안의 `resizeoption.ui`에도 `stringlist` 태그가 제거된 것을 확인했다.
- 파일 열기/저장 폴더/색상 선택 대화상자 호출부가 PySide6 positional API 형태로 정리된 것을 확인했다.
- `PYTHONPYCACHEPREFIX=/tmp/paddie-pycache python3 -m compileall -q src docs`와 `git diff --check`가 통과했다.
- 시스템 Python의 `PySide6==6.10.3` 기준 오프스크린 스모크 테스트에서 설정 언어를 영어/한국어로 바꾸고 현재 창을 재번역하는 흐름이 통과했다.
- 영어 전환 후 `Options`, `Preferences`, `Information`, `Exit`, `Files`, `Add Files`, `Clear List` 메뉴 텍스트가 유지되는 것을 확인했다.
- `Preferences`, `Information`, `Exit` 액션의 menu role이 각각 `PreferencesRole`, `AboutRole`, `QuitRole`로 설정되는 것을 확인했다.
- 오프스크린 Qt 스모크 테스트에서 정보 창 생성과 영어/한국어 재번역이 예외 없이 통과했다.
- `.venv`의 `PySide6==6.10.3` 기준 오프스크린 앱 생성과 영어 전환 스모크 테스트가 통과했다.
- `.venv/bin/python scripts/build_release.py`로 로컬 macOS PyInstaller 빌드가 완료되어 `dist/Paddie`, `dist/Paddie.app`이 생성됐다.
- `.venv/bin/python scripts/package_release.py --artifact-name Paddie-local-macos-arm64 --format zip`로 로컬 zip 산출물을 만들었다.
- Codacy가 지적한 critical/high 항목 중 실제 위험도가 있는 XML 파서,
  업데이트 확인 네트워크 호출, 임시 빌드 캐시, 명시 import 문제를 정리했다.
