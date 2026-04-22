# 현재 복구 메모

브랜치: `codex/recover-v3.4.1`
기준: `v3.4.1` (`b906a85`)

## 현재 상태

- 안정 버전인 `v3.4.1` 태그에서 복구 브랜치를 만들었다.
- 복구 이력 추적을 위해 `docs/`를 추가했다.
- 앱 UI 런타임은 PySide6 단일 기준으로 정리했다.
- 공통 빌드 스크립트와 GitHub Actions workflow를 추가했다.

## 확인한 회귀 원인

- 이슈 #66은 Windows의 메타데이터 인코딩 오류에서 시작됐다.
- 직접적인 UTF-8 수정은 작고 합리적인 범위였다.
- 같은 시기에 리소스 이동, 빌드 자동화, 설정/i18n이 섞였다.
- worker 변환, 업데이트 확인, 이후 Flet 실험도 함께 들어왔다.
- `program_data.json`은 `v3.4.1` 기준에는 없는 파일이다.
- 버전 메타데이터는 일단 보류한다.

## 다음 단계

1. GitHub Actions 원격 빌드를 실행한다.
2. macOS Intel, Apple Silicon, Windows x64, Linux x64 빌드를 확인한다.
3. 새 빌드에서 파일 추가와 저장 경로 선택을 테스트한다.
4. 실제 이미지로 리사이즈와 EXIF 프리뷰를 확인한다.
5. 라이선스를 확정한 뒤 `LICENSE`와 정보 창 값을 갱신한다.
6. 자동 업데이트 설치는 별도 단계로 검토한다.

## 적용한 변경

- JSON/CSV 파일 읽기와 쓰기에 UTF-8 인코딩을 명시했다.
- `user_data.json` 입출력에 context manager를 적용했다.
- `src/exif_module.py`와 `src/resize_module.py`의 `is` 비교를 고쳤다.
- 정보 창의 프로그램명, 버전, 연락처 표시값을 보정했다.
- 기존 리소스를 `resources/data`, `fonts`, `icons`, `ui`로 옮겼다.
- EXIF 미리보기를 항상 별도 프리뷰 창으로 표시한다.
- UI 런타임을 PySide6 단일 의존성으로 정리했다.
- `.ui` 파일을 읽기 위해 `QUiLoader` 기반 로더를 추가했다.
- Qt 번역 파일을 복원하고 앱 시작 시 번역기를 설치한다.
- 언어 변경 시 이미 로드된 Qt UI 텍스트를 다시 번역한다.
- 영어는 원문 UI 언어로 처리한다.
- 빈 번역 문자열은 `.ui` 원문 텍스트로 fallback한다.
- macOS 앱 메뉴 액션은 Qt menu role로 위치를 고정했다.
- 정보 창을 코드 기반 레이아웃으로 교체했다.
- 정보 창 메타데이터에 라이선스 행을 추가했다.
- 라이선스 파일이 없어 `Unspecified`로 표시한다.
- `PySide6`를 `6.10.3`으로 올려 Qt 런타임 오류를 해소했다.
- `setuptools==80.9.0`으로 `pkg_resources` 호환성을 고정했다.
- 사용자 설정 저장 위치를 OS별 사용자 설정 폴더로 옮겼다.
- `PADDIE_CONFIG_DIR`로 테스트 설정 폴더를 지정할 수 있게 했다.
- OS별 PyInstaller 빌드와 패키징 스크립트를 추가했다.
- 태그 빌드에서 draft release를 만드는 workflow를 추가했다.
- `Options` 메뉴에 최신 버전 확인 항목을 추가했다.

## 검증

- `python3 -m compileall -q src docs`가 통과했다.
- `resize_module` 단독 import가 통과했다.
- `ILCE-7RM3` 모델명이 `A7RM3`로 매핑되는 것을 확인했다.
- 새 리소스 경로와 `resources/barlow-light.ttf` 해석을 확인했다.
- 깨진 `.venv/bin/pyinstaller` shebang을 의존성 재설치로 복구했다.
- macOS PyInstaller 빌드로 `dist/Paddie.app`을 생성했다.
- 새 빌드 산출물의 `resizeoption.ui` 수정 반영을 확인했다.
- 파일 열기, 저장 폴더, 색상 선택 호출을 정리했다.
- `compileall`과 `git diff --check`가 통과했다.
- 오프스크린 Qt 스모크 테스트에서 언어 전환이 통과했다.
- 영어 전환 후 주요 메뉴 텍스트가 유지되는 것을 확인했다.
- `Preferences`, `Information`, `Exit` menu role을 확인했다.
- 정보 창 생성과 영어/한국어 재번역이 예외 없이 통과했다.
- `.venv/bin/python scripts/build_release.py`가 통과했다.
- 로컬 zip 산출물 `Paddie-local-macos-arm64.zip`을 만들었다.
- Codacy critical/high 중 XML 파서와 네트워크 호출을 정리했다.
- 임시 빌드 캐시, 명시 import, 패키징 경로도 함께 정리했다.
