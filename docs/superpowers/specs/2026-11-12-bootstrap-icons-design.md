# Bootstrap Icons 스킬 설계

**날짜:** 2026-11-12
**이슈:** #14

## 목적

SVG 구조도·문서에 Bootstrap Icons를 넣을 때, 의도에 맞는 아이콘 이름을 빠르게 찾고, 내려받고, 인라인 심볼로 삽입하는 카탈로그 스킬. `aws-icons`, `cloudflare-icons`와 같은 형태를 따른다.

## 사실 확인 (2026-11-12)

| 항목 | 값 |
| --- | --- |
| 사이트 | <https://icons.getbootstrap.com/> |
| 버전 | v1.13.2 |
| 아이콘 수 | 2,078개 |
| 카테고리 | 29개 |
| 라이선스 | MIT (브랜드 로고는 상표) |
| SVG 규격 | 전부 `viewBox="0 0 16 16"`, `fill="currentColor"` |
| 내부 구조 | `id`, `url(#...)`, 주석 없음 → 심볼 변환 단순 |
| 개별 SVG URL | `https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.2/icons/<name>.svg` |
| 스프라이트 | `bootstrap-icons.svg` (2,078개 `<symbol>`, id = 아이콘 이름) |
| 메타데이터 | `https://icons.getbootstrap.com/icons/index.json` (이름·검색어·카테고리·태그, 312KB) |

`index.json`의 카테고리 소속 합계가 정확히 2,078이므로 아이콘당 카테고리는 하나다.

## 목표

- 다이어그램 의도 → 아이콘 이름 매핑을 빠르게 제공
- 2,078개 전체 이름을 grep 가능한 형태로 제공
- 다운로드 스크립트가 실패를 숨기지 않음 (HTML 저장 방지)
- SVG → `<symbol>` 삽입 절차와 gotcha 제공
- 버전업 시 카탈로그 재생성 경로 제공

## 비목표

- 웹 UI용 아이콘 폰트, CDN 설치, 접근성(`aria-hidden`, `role="img"`), React/Vue 사용법
- 2,078행짜리 마크다운 카탈로그 표
- 아이콘 파일 자체를 저장소에 커밋

## 접근 (선택됨)

세 가지안 중 **2번: aws-icons 형태** 선택.

1. 얇은 스킬 — 의도→이름 표 + 스크립트만
2. **aws-icons 형태** — 1번 + 전체 이름 카탈로그 (**선택**)
3. 웹 UI까지 확장

카탈로그는 md 표 대신 `references/icon-names.txt`(카테고리 헤더 + 한 줄 한 이름)로 둔다. 2,078행을 md 표로 만들면 읽기·grep 둘 다 나빠진다.

## 구성

```
skills/bootstrap-icons/
  SKILL.md
  references/icon-names.txt      # 2,078개, 카테고리별 (생성물)
  scripts/fetch-icons.sh         # 이름/--all/--category 다운로드
  scripts/build-sprite.py        # SVG → <symbol> 스프라이트
  scripts/build-catalog.sh       # icon-names.txt 재생성
```

## 결정

- **이름 정본은 npm 고정본**(`bootstrap-icons@1.13.2`), 카테고리는 사이트 `index.json`. 사이트는 라이브라 이름이 앞설 수 있으므로 npm 목록에 없는 이름은 카탈로그에서 제외한다.
- 스냅샷 날짜와 버전을 SKILL.md 헤더에 명시한다. 버전업은 `build-catalog.sh` 재실행.
- fetch 스크립트의 이름 검증은 `icon-names.txt` 파싱(오프라인 동작). `--category`도 같은 파일을 파싱한다.
- `build-sprite.py`는 cloudflare-icons 스크립트에서 id 네임스페이싱·dangling ref 처리를 제거한 단순 버전. Bootstrap Icons에 `id`/`url(#)`가 없기 때문.
- 스프라이트 symbol id는 `bi-<name>`.
- 아이콘 16×16 얇은 선 → 구조도에서는 24–32px 권장, AWS/Cloudflare의 채워진 아이콘과 같은 행에 같은 크기로 섞지 않는다.

## 리스크

| 리스크 | 대응 |
| --- | --- |
| 사이트 index.json과 npm 고정본 불일치 | npm 이름 목록과 교차 확인, 불일치 이름 제외 |
| `--all` 2,078개 다운로드가 느림 | 기본은 선택 다운로드, `--all`은 명시 요청 시 |
| 존재하지 않는 이름이 HTML로 저장 | content-type + `<svg` 검증, 실패 목록 출력 후 exit 1 |
| 16×16 확대 시 선이 가늘어 보임 | SKILL.md 크기 지침에 명시 |
| 브랜드 아이콘 상표 | 서비스 노드에 쓰지 않는다고 명시 |
