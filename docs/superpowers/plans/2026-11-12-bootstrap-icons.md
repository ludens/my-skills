# Bootstrap Icons 스킬 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `skills/bootstrap-icons/`에 다이어그램용 Bootstrap Icons 카탈로그 스킬을 추가한다.

**Architecture:** SKILL.md + 생성된 이름 카탈로그 + 다운로드/스프라이트 스크립트. `aws-icons` 패턴을 따르고 웹 UI 배포 방식은 범위 밖이다.

**Tech Stack:** Bash (curl), Python 3 (표준 라이브러리만), Markdown.

**Spec:** `docs/superpowers/specs/2026-11-12-bootstrap-icons-design.md`

## Global Constraints

- 문서는 한국어. `description`은 `Use when ...` + `/ Triggers - ...` 형식.
- YAML plain scalar에 `: ` 금지 (issue #12 재발 방지).
- 버전 고정: `bootstrap-icons@1.13.2`. 스냅샷 날짜 `2026-11-12`.
- 아이콘 2,078개, 카테고리 29개, 전부 `viewBox="0 0 16 16"`, `fill="currentColor"`.
- 스크립트는 실패를 숨기지 않는다: `image/svg+xml` + `<svg` 검증, 실패 목록 출력 후 exit 1.
- 편집은 이 worktree에만. `~/.agents/skills`, `~/.pi/agent/skills`는 건드리지 않는다.

## Review Focus

1. 존재하지 않는 아이콘 이름 → 0바이트/HTML 저장 없이 실패.
2. `--all` 부분 실패 → 성공분 저장, 실패분 보고, exit 1.
3. `<symbol>` 변환 시 `class`/`width`/`height` 잔존 → CSS 충돌.
4. 사이트 `index.json`과 npm 고정본 이름 불일치 → 카탈로그에 없는 이름 노출.
5. 16×16 아이콘을 48px로 확대 → 선이 가늘어 보임. SKILL.md가 경고하는지.

---

### Task 1: 카탈로그 생성

**Files:**
- Create: `skills/bootstrap-icons/scripts/build-catalog.sh`
- Create: `skills/bootstrap-icons/references/icon-names.txt` (생성물)

**Interfaces:**
- Produces: `references/icon-names.txt`. 첫 줄 `# bootstrap-icons 1.13.2 · 2026-11-12 · 2078 icons`, 카테고리마다 `## <Category Name> (<count>)`, 그 아래 한 줄에 아이콘 이름 하나. Task 2, 3, 4가 이 파일을 읽는다.

- [ ] **Step 1: 스크립트 작성**

`build-catalog.sh`는 다음을 수행한다:
- `curl -fsSL "https://registry.npmjs.org/bootstrap-icons/1.13.2"` 의 `dist.tarball` 대신 jsDelivr 파일 목록 API를 쓴다: `https://data.jsdelivr.com/v1/packages/npm/bootstrap-icons@1.13.2?structure=flat` → `files[].name` 중 `/icons/*.svg`에서 이름 추출 (`/icons/` 접두와 `.svg` 접미 제거).
- `curl -fsSL "https://icons.getbootstrap.com/icons/index.json"` → 각 항목 `{n, s, c, t}`.
- npm 이름 집합에 있는 항목만 남긴다.
- 카테고리 슬러그를 사이트 표기 이름으로 매핑한다 (`alerts-and-status` → `Alerts & Status`, `ui-and-keyboard` → `UI & Keyboard` 등 29개, 사이트 좌측 내비게이션 표기 기준).
- 카테고리는 사이트 내비 순서(`All Icons` 다음 순서)대로, 각 카테고리 안 이름은 사전순.
- 어느 카테고리에도 없는 이름이 있으면 `## Uncategorized`로 마지막에 넣고 stderr에 경고.
- 출력은 stdout, 리다이렉트로 `references/icon-names.txt`에 저장.

- [ ] **Step 2: 생성 및 검증**

```bash
bash skills/bootstrap-icons/scripts/build-catalog.sh > skills/bootstrap-icons/references/icon-names.txt
head -1 skills/bootstrap-icons/references/icon-names.txt
grep -c '^## ' skills/bootstrap-icons/references/icon-names.txt
grep -vc '^#\|^$' skills/bootstrap-icons/references/icon-names.txt
```

Expected: 헤더 버전 `1.13.2`, `29`, `2078`.

- [ ] **Step 3: 커밋**

```bash
git add skills/bootstrap-icons
git commit -m "feat(bootstrap-icons): add icon name catalog and generator"
```

---

### Task 2: fetch 스크립트

**Files:**
- Create: `skills/bootstrap-icons/scripts/fetch-icons.sh`

**Interfaces:**
- Consumes: `references/icon-names.txt` (Task 1)
- Produces: `<outdir>/<name>.svg` 파일들. 실패 시 exit 1.

- [ ] **Step 1: 스크립트 작성**

사용법:
```
fetch-icons.sh <outdir> <name...>
fetch-icons.sh <outdir> --all
fetch-icons.sh <outdir> --category <slug>
fetch-icons.sh --list
```
- `VERSION=1.13.2`, URL `https://cdn.jsdelivr.net/npm/bootstrap-icons@$VERSION/icons/<name>.svg`.
- 이름은 `icon-names.txt`에 있는 것만 허용. 없으면 `unknown icon: <name>` 출력 후 집계.
- 다운로드 후 content-type이 `image/svg+xml`이고 본문에 `<svg`가 있어야 저장. 아니면 실패 집계.
- 실패 목록을 마지막에 출력하고, 하나라도 있으면 exit 1.
- `--list`는 카탈로그의 이름만 출력.

- [ ] **Step 2: 검증**

```bash
bash skills/bootstrap-icons/scripts/fetch-icons.sh /tmp/bi-check database person exclamation-triangle
ls /tmp/bi-check
xmllint --noout /tmp/bi-check/*.svg
bash skills/bootstrap-icons/scripts/fetch-icons.sh /tmp/bi-check no-such-icon-xyz; echo "exit=$?"
bash skills/bootstrap-icons/scripts/fetch-icons.sh /tmp/bi-check --category data
ls /tmp/bi-check | wc -l
```

Expected: 첫 명령 3개 파일, `xmllint` 무출력, 두 번째 `unknown icon` + `exit=1`, `--category data` 추가 12개.

- [ ] **Step 3: 커밋**

```bash
git add skills/bootstrap-icons/scripts/fetch-icons.sh
git commit -m "feat(bootstrap-icons): add fetch script with validation"
```

---

### Task 3: 스프라이트 빌더

**Files:**
- Create: `skills/bootstrap-icons/scripts/build-sprite.py`

**Interfaces:**
- Consumes: 내려받은 SVG 디렉터리
- Produces: `<symbol id="bi-<name>" viewBox="0 0 16 16" fill="currentColor">` 블록. `--fragment`면 symbol 블록만, 아니면 `<svg><defs>`로 감싼 완전한 파일.

- [ ] **Step 1: 스크립트 작성**

```
build-sprite.py --dir <svgdir> --out <file> <name...>
build-sprite.py --dir <svgdir> --fragment <name...>
```
- 입력 SVG에서 XML 선언, DOCTYPE, 바깥 `<svg ...>`/`</svg>` 제거. 내부 요소만 남긴다.
- 바깥 `<svg>`의 `viewBox` 값을 symbol로 옮긴다(없으면 `0 0 16 16`).
- `class="bi ..."`, `width`, `height` 속성은 symbol에 넣지 않는다.
- symbol id는 `bi-<name>`.
- 이름이 `bi-`로 시작해도 중복 접두를 만들지 않는다.
- 파일이 없으면 해당 이름을 실패 목록에 넣고 마지막에 exit 1.

- [ ] **Step 2: 검증**

```bash
python3 skills/bootstrap-icons/scripts/build-sprite.py --dir /tmp/bi-check --out /tmp/bi-sprite.svg database person
xmllint --noout /tmp/bi-sprite.svg
grep -c '<symbol' /tmp/bi-sprite.svg
grep -o 'id="bi-database"' /tmp/bi-sprite.svg
grep -c 'class="bi\|width="16"' /tmp/bi-sprite.svg || true
```

Expected: `xmllint` 무출력, symbol 2개, `id="bi-database"`, class/width 0건.

- [ ] **Step 3: 커밋**

```bash
git add skills/bootstrap-icons/scripts/build-sprite.py
git commit -m "feat(bootstrap-icons): add SVG sprite builder"
```

---

### Task 4: SKILL.md + README

**Files:**
- Create: `skills/bootstrap-icons/SKILL.md`
- Modify: `README.md` (스킬 표에 행 추가)

**Interfaces:**
- Consumes: Task 1 카탈로그, Task 2·3 스크립트 경로

- [ ] **Step 1: SKILL.md 작성**

frontmatter:

```yaml
---
name: bootstrap-icons
description: Use when SVG 구조도·문서에 Bootstrap Icons를 넣을 때, 또는 의도에 맞는 아이콘 이름·SVG URL·다운로드·심볼 삽입 방법이 필요할 때. 사용자·데이터베이스·서버·방화벽 같은 범용 UI 글리프를 구조도 노드로 쓰는 경우를 포함한다. / Triggers - add Bootstrap Icons to SVG diagram, find bootstrap icon name and svg url
---
```

본문 섹션:
1. 소스 표 (사이트, 버전, 아이콘 2,078, 라이선스, SVG URL, 스프라이트, `index.json`, 스냅샷 날짜)
2. 빠른 선택 표 40–50개: 다이어그램 의도 → 아이콘 이름. 모든 이름은 `icon-names.txt`에 존재해야 한다.
3. 선택 기준: 아웃라인 vs `-fill`, `-fill` 없는 아이콘 존재, 브랜드 아이콘은 서비스 노드에 쓰지 않음, 의미가 겹치는 이름(`person`/`people`/`person-circle`) 구분
4. 크기·색: 16×16 얇은 선, 24–32px 권장, AWS/Cloudflare 아이콘과 같은 행에 같은 크기로 섞지 않음, `currentColor` 상속, Bootstrap primary `#0d6efd` 또는 중립 `#495057`
5. 다운로드: 단일/여러 개/카테고리/전체/목록
6. SVG 삽입: `<symbol id="bi-x" viewBox="0 0 16 16" fill="currentColor">`, 바깥 `<svg>`/`class`/`width`/`height` 제거, `<use>`에 크기·색, `build-sprite.py` 사용법
7. 자주 틀리는 것 표
8. 검증
9. 스냅샷 고지

- [ ] **Step 2: 빠른 선택 표 이름 검증**

```bash
for n in <표에 쓴 이름들>; do grep -qx "$n" skills/bootstrap-icons/references/icon-names.txt || echo "MISSING $n"; done
```

Expected: 출력 없음.

- [ ] **Step 3: frontmatter YAML 파싱 확인**

```bash
python3 -c "import yaml,sys; d=yaml.safe_load(open('skills/bootstrap-icons/SKILL.md').read().split('---')[1]); print(d['name'], len(d['description']))"
```

Expected: `bootstrap-icons <숫자>`. pyyaml이 없으면 `ruby -ryaml -e`로 대체.

- [ ] **Step 4: README 표에 행 추가 후 커밋**

```bash
git add skills/bootstrap-icons/SKILL.md README.md
git commit -m "feat(bootstrap-icons): add skill guide"
```

---

### Task 5: 스킬 적용 검증 (GREEN)

**Files:** 없음 (검증만)

- [ ] **Step 1: 기준선 과제 재실행**

Task 1 baseline과 같은 과제를 fresh subagent에 준다. `skills/bootstrap-icons/SKILL.md`를 읽고 따르라고 지시한다. 산출물은 `/private/var/folders/75/65d9txqn3lgg9w3tb721gcn40000gn/T/opencode/green/`에 쓴다.

- [ ] **Step 2: 준수 확인**

- 카탈로그에 있는 이름만 사용했는가
- 인라인 `<symbol>` + `<use>`를 썼는가 (폰트 클래스 아님)
- `class`/`width`/`height`가 symbol에 남지 않았는가
- 24–32px 권장을 지켰는가
- `fill="currentColor"` 상속 또는 명시 색을 썼는가

- [ ] **Step 3: 미준수 항목 보강 후 재검증**

새 합리화가 나오면 SKILL.md에 명시적 카운터를 추가하고 다시 실행한다.

- [ ] **Step 4: 이슈 댓글 기록 + 커밋 + PR**

검증 결과를 이슈에 남기고, `git push -u origin issue/14` 후 PR 생성.
