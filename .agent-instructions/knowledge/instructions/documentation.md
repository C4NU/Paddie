## 문서 규칙

**모든 프로젝트는 저장소 안에 `docs/`를 둔다.** 문서는 코드와 같이 커밋한다.

```
docs/
├── product.md      제품 정의 (또는 README.md — 문서 색인)
├── plan/           revenue.md만 쓴다 · archive/ (할 일은 Studio Ops 보드)
├── tech-docs/      마일스톤이 끝나도 남는 지식 (설계·제약·함정)
├── guide/          반복 실행하는 절차 (배포·검증)
├── version/        버전별 결과
└── appstore/       스토어 문안·스크린샷 (앱 프로젝트만)
```

### 할 일은 보드, 지식은 tech-docs

🔴 **할 일은 Studio Ops 보드에 두고 `tech-docs/`는 마크다운으로 쌓는다.** 이 둘을 섞지 않는다.

| | 독자 | 성격 |
|---|---|---|
| Studio Ops 보드 | 사람·에이전트 | 할 일. 카드가 상태 열을 옮겨 다닌다. **끝나면 `done`으로** |
| `tech-docs/` | AI | 장기 기억. 쌓인다. **지우지 않는다** |

예전에는 `plan/`의 current·backlog·roadmap·code-review 마크다운으로 할 일을 관리했다.
Obsidian 동기화가 복잡하고 에이전트마다 읽는 방식이 달라 2026-10에 보드로 옮겼다.
기존 파일은 동결한다 — 고치지도 지우지도 않고, 보드로 옮긴 뒤 사용자가 `plan/archive/`로 내린다.

### 보드 — 예전 문서와의 대응

| 예전 문서 | 보드에서 |
|---|---|
| `current.md` 현재 진행중 | `in_progress` 카드. 두어 개를 넘기지 않는다 |
| `current.md` 진행 예정 · `backlog.md` | 이번 버전 릴리즈에 묶인 `planned` 카드, 언젠가 할 것은 `backlog` |
| `current.md` 진행 불가 | 라벨 `blocked` + 설명에 원인 |
| `roadmap.md` | 예정 릴리즈(버전·제목·목표일) + 아이디어함 |
| `code-review.md` | `bug` 카드(라벨 `code-review`, 우선순위 = 등급). 재현·원인·고친 코드는 `tech-docs/review/` |

**카드 하나 = 할 일 하나.** 제목은 결과가 보이게 쓴다(「위젯 크래시 수정」). 설명에는 맥락과 완료 조건만 —
교훈은 `tech-docs/`로 보낸다. 같은 일을 두 카드로 만들지 않는다(`list_work_items`의 `q`로 먼저 찾는다).

🔴 **작업을 한 번 끝낼 때마다 카드를 옮긴다.** 세션이 끝날 때 몰아서 하지 않는다 — 그러면 빠진다.
MCP `studio`가 연결돼 있지 않으면 마크다운에 대신 적지 않고, 반영하지 못한 것을 끝에 사용자에게 알린다.

처음 보드를 쓰는 저장소는 studio-ops의 `npm run import:development`로 기존 plan 문서를 한 번 가져온다.

### revenue.md — plan/에 남는 마크다운

스토어 상품이 없는 프로젝트는 `revenue.md`와 아래 ASC·RevenueCat 절차를 적용하지 않는다.

**`revenue.md`는 기억이 아니라 조회 결과를 적는다.** 상품 ID·가격·상태를 손으로 적어두면
곧 실제와 어긋난다. 아래 명령의 출력을 그대로 옮기고 **조회한 날짜를 함께 적는다.** 200줄을 넘기지 않는다.

```bash
asc iap list --app <APP_ID>                                  # 상품과 상태
asc iap pricing summary --app <APP_ID> --territory KOR       # 지역 가격
```

RevenueCat 쪽(entitlement · offering · package)은 MCP로 읽는다. 원화 가격은 달러 환산이
아니라 **ASC가 주는 값**이므로 계산하지 않는다.

이 파일이 답해야 하는 질문은 넷이다 — **무엇을 파는가 · 얼마인가 · 사면 무엇이 열리는가 ·
지금 어떤 상태인가.** 정책의 근거와 개정 이력은 `tech-docs/product/`에 둔다.

### 약어

🔴 **새 약어 체계를 만들지 않는다.** 지금 같은 `P`가 Paddie에서는 우선순위이고
Rollie에서는 작업 번호다. 문서를 가로질러 읽을 수 없게 된 원인이다.

**약어를 단독으로 쓰지 않는다. 항상 이름을 병기한다.**

```
❌  W4를 먼저 닫는다
✅  W4 라이브 액티비티를 먼저 닫는다
```

프로젝트를 가로질러 뜻이 같은 약어는 다음 셋뿐이다.

| 약어 | 뜻 |
|---|---|
| `P0`~`P3` | 우선순위. 0이 가장 급하다 |
| `CR-##` | 코드리뷰 항목 번호 |
| `vX.Y.Z` | 버전 |

그 밖의 알파벳+숫자(`W4` · `M1` · `S1` · `Q4` …)는 **그 프로젝트 안에서만** 쓴다.
쓴다면 저장소 `AGENTS.md`에 무엇의 약자인지 한 줄로 적는다. 적지 않을 거면 쓰지 않는다.

### tech-docs/ — 기억의 궁전

AI가 매번 같은 경로로 찾아가도록 **방 이름을 프로젝트 간에 통일한다.**

🔴 **대소문자가 성격을 가른다. 소문자는 공통, 대문자는 그 앱 전용이다.**
이 구분이 "다른 앱에서도 찾을 수 있는 지식인가"를 한눈에 보여준다.

```
tech-docs/
├── README.md      입구 — 방 목록과 각 방에 무엇이 있는지
├── build/         빌드·아카이브·서명·생성 스크립트
├── core/          아키텍처·렌더링 코어·성능
├── platform/      OS 분기·Catalyst·하드웨어·버전 대응
├── data/          저장·마이그레이션
├── store/         ASC·심사·과금·RevenueCat
├── ui/            레이아웃·애니메이션·제스처
├── product/       제품 방향과 결정 로그 · 정책의 근거
├── review/        코드리뷰 상세 기록 (남은 항목은 보드의 bug 카드)
└── <전용>/        대문자. 그 앱만의 도메인
```

**문서가 없는 방은 만들지 않는다.** 빈 방은 찾는 사람을 헷갈리게 한다.

전용 방 이름은 각 저장소의 AGENTS.md에서 정한다.

**문서 이름은 kebab-case로 통일한다.** `snake_case`나 `PascalCase`를 섞지 않는다.

한 문서는 한 주제만 담고, 형식을 고정한다.

```markdown
---
room: store
tags: [asc, dsym, crash-report]
verified: 2026-09-04
severity: high
---

# ASC는 dSYM을 되돌려주지 않는다

**증상** — `asc builds dsyms`가 모든 빌드에서 `No dSYM files available`.
**원인** — Bitcode 폐기 후 Apple은 내려줄 dSYM을 만들지 않는다.
**대응** — 출시·심사 버전의 dSYM은 로컬 `archives/dsyms/`에 zip으로 보관한다.
**재발 방지** — 아카이브를 지우기 전 dSYM을 먼저 빼낸다.

관련: [[build/archive-retention]]
```

`verified` 날짜는 그 지식을 마지막으로 확인한 날이다. 오래된 문서를 만나면 다시 검증한다.

새 문서가 필요하면 성격에 맞는 폴더로 보낸다. 시점 스냅샷(핸드오프·컨텍스트 덤프)은
`plan/archive/`로 내린다.

**같은 정보를 두 곳에 두지 않는다.** 목록을 두 곳에 두면 한쪽만 지워도 티가 안 난다.
필요하면 상대 경로로 참조한다.
