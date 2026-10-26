# twemoji 스킬 구현 계획 (issue #6)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** SVG 도식화에 twemoji 이모지 아이콘을 찾고 받아 삽입하는 `skills/twemoji` 스킬(SKILL.md + fetch-emoji.sh)을 추가한다.

**Architecture:** aws-icons 스킬과 같은 카탈로그형 레퍼런스 스킬. 소스는 유지보수 포크 `jdecked/twemoji` v17.0.3 고정, CDN(jsdelivr)에서 코드포인트 파일명으로 다운로드. 코드포인트 변환은 셸보다 python3 표준 라이브러리가 안정적이라 fetch-emoji.sh 내부에서 python3 한 통으로 처리.

**Tech Stack:** bash + curl + python3(표준 라이브러리만, 추가 의존성 없음), xmllint 검증.

**Spec:** `docs/superpowers/specs/2026-10-26-twemoji-skill-design.md`

## Global Constraints

- 소스·버전 고정: `https://cdn.jsdelivr.net/gh/jdecked/twemoji@17.0.3/assets/svg/<codepoint>.svg` (v17.0.3, 2026-06-01 릴리스)
- 대체 raw URL: `https://raw.githubusercontent.com/jdecked/twemoji/v17.0.3/assets/svg/<codepoint>.svg`
- 모든 SVG는 `viewBox="0 0 36 36"`, 크기 변형 없음, 색은 파일에 포함(재색칠 금지)
- 캐시: `~/.cache/twemoji/17.0.3/`
- 문서·주석 언어는 한국어(저장소 관례), 스크립트 에러 메시지 영문 허용
- 비목표: HTML 웹삽입, PNG, twemoji node 라이브러리, 원본 twitter/twemoji 지원

## Review Focus

- fe0f(변이 선택자) 제거 규칙 누락: `❤️`는 `2764.svg`여야 하며 `2764-fe0f.svg`는 404다 → Task 2가 `❤️`·`©️` 실다운로드로 고정
- ZWJ·skin tone 시퀀스 `200d`/`1f3fb`-`1f3ff`는 `-` 연결 대상이다 → Task 2가 `🧑‍💻`, `👍🏽`로 고정
- `🇰🇷` 같은 국기는 지역 인디케이터 페어로 계산된다 → Task 2가 `1f1f0-1f1f7.svg`를 고정
- SVG 내 gradient/clipPath `id`가 여러 이모지 인라인 시 충돌한다 → Task 3가 네임스페이싱 규칙과 xmllint 검증으로 고정
- 존재하지 않는 코드포인트(404)가 스크립트에서 조용히 성공처럼 보이면 안 된다 → Task 2가 404 시 비종료·명시적 실패 출력 요구

---

### Task 1: RED — 스킬 없는 기준(baseline) 테스트

**Files:** 없음(결과만 문서화)

**Interfaces:** Produces — baseline 실패 패턴 요약(텍스트), Task 4의 판정 기준.

- [ ] **Step 1:** 사람 이모지 3개(🇰🇷, ❤️, 🧑‍💻)를 포함한 SVG 도식을 만들라는 과제를, 스킬 없는 신규 하위 에이전트(`subagent`, agent: "general")에 지시한다. 프롬프트: "twemoji 아이콘(https://github.com/jdecked/twemoji)의 SVG를 사용해 🇰🇷 ❤️ 🧑‍💻 세 개가 가로로 배치된 SVG 다이어그램을 만들어 /tmp/twemoji-baseline.svg 로 저장해라. 실제 twemoji 에셋 경로/URL을 사용해야 한다."
- [ ] **Step 2:** 결과 확인 — 저장된 SVG가 실제 twemoji 에셋(올바른 코드포인트 파일명·URL)을 참조하는지 평가. 참조 실패·잘못된 파일명·이미지 없는 자체 원 그리기 등 실패 패턴을 기록.
- [ ] **Step 3:** baseline 결과(사용한 URL, 틀린 부분)를 이슈 댓글로 기록: `gh issue comment 6 --body "<..."`

### Task 2: fetch-emoji.sh 스크립트

**Files:**
- Create: `skills/twemoji/scripts/fetch-emoji.sh`

**Interfaces:**
- Produces: `bash skills/twemoji/scripts/fetch-emoji.sh <저장디렉터리> <emoji...>`, 및 `--list <codepoint>...` 모드. 저장 파일명은 `<codepoint>.svg`. Task 3·4가 이 경로·동작을 그대로 사용.

- [ ] **Step 1:** 스크립트 작성. 시그니처: `fetch-emoji.sh <out-dir> <emoji>... | --list <codepoint>...`. 동작: (a) 이모지 → python3로 코드포인트 hex 소문자 `-` 연결 파일명, fe0f 제거 우선 → 404면 원본(fe0f 포함) 재시도; (b) `~/.cache/twemoji/17.0.3/` 캐시 후 out-dir로 복사; (c) 404는 전체 exit 1이 아니라 실패 목록 출력 후 스크립트가 계속 진행(받은 것은 캐시 저장); (d) `--list`는 파일명만 출력. CDN URL은 Global Constraints 값 그대로.
- [ ] **Step 2:** 실다운로드 검증:

```bash
bash skills/twemoji/scripts/fetch-emoji.sh /tmp/twemoji-test "🇰🇷" "❤️" "👍" "🧑‍💻" "👍🏽" "©️"
ls /tmp/twemoji-test
```

Expected: `1f1f0-1f1f7.svg 2764.svg 1f44d.svg 1f9d1-200d-1f4bb.svg 1f44d-1f3fd.svg a9.svg` 전부 존재(©️는 fe0f 제거 폴백으로 a9.svg).
- [ ] **Step 3:** 미지 코드포인트 거동 확인: `bash skills/twemoji/scripts/fetch-emoji.sh /tmp/twemoji-test "🫩" 2>&1` — 실패 출력이 명시적이고 스크립트가 hang 하지 않는다. (🫩는 도입 시기에 따라 404일 수 있음)
- [ ] **Step 4:** `xmllint --noout /tmp/twemoji-test/*.svg` 로 SVG 유효성 확인.
- [ ] **Step 5:** Commit

```bash
git add skills/twemoji/scripts/fetch-emoji.sh
git commit -m "feat(skills): add twemoji fetch script (#6)"
```

### Task 3: SKILL.md

**Files:**
- Create: `skills/twemoji/SKILL.md`

**Interfaces:**
- Consumes: Task 2의 스크립트 경로 `skills/twemoji/scripts/fetch-emoji.sh`(톤: `bash scripts/fetch-emoji.sh <dir> <emoji>...`).
- Produces: 없음(문서). Task 4 시나리오가 이 문서로 판정.

- [ ] **Step 1:** 프론트매터 작성. `name: twemoji`, `description`은 "Use when..." 시작 + 트리거: SVG 도식·다이어그램·문서에 twemoji 이모지 아이콘을 찾고 넣을 때, 이모지 → 파일명(코드포인트) 변환이 필요할 때. 저장소 기존 스킬(aws-icons)과 동일 스타일.
- [ ] **Step 2:** 본문 작성 — 설계 문서 구성 그대로: 소스 표(포크 사유·v17.0.3·CDN·raw 대체), 코드포인트 변환 규칙 표(실제 예시 중심: `1f600`, `2764`(fe0f 제거), `1f1f0-1f1f7`, `1f9d1-200d-1f4bb`, `1f44d-1f3fd`, fe0f 폴백), SVG 인라인 규칙(`viewBox="0 0 36 36"` symbol, gradient/clipPath id 슬러그 네임스페이싱, 재색칠 금지), 배치(이모지 크기 균일 24–48px, 라벨 조합), 빠른 선택 표(인터넷/사용자 표시에 🌐👤, 성공/실패에 ✅❌ 등), 자주 틀리는 것 표, 검증(xmllint + 렌더). 코드 예시는 Task 3 테스트에서 만든 3개 이모지 심볼 인라인 하나(하나의 뛰어난 예시 원칙).
- [ ] **Step 3:** 예시 인라인 규칙과 실제 다운로드 일치 확인 — Task 2에서 받은 `/tmp/twemoji-test` SVG를 예시에 사용, `xmllint --noout` 통과.
- [ ] **Step 4:** Commit

```bash
git add skills/twemoji/SKILL.md
git commit -m "feat(skills): add twemoji SKILL.md (#6)"
```

### Task 4: GREEN — 스킬 적용 시나리오 재테스트

**Files:** 없음(판정만)

**Interfaces:**
- Consumes: Task 1의 baseline 패턴, Task 3의 SKILL.md.

- [ ] **Step 1:** 같은 과제를 신규 하위 에이전트에게 재지시하되, `skills/twemoji/SKILL.md` 내용을 프롬프트에 포함(스킬 명세상 "SKILL.md 전문 + 과제").
- [ ] **Step 2:** 결과가 baseline 실패 패턴을 해소했는지 판정 — 올바른 코드포인트 URL/파일명 사용, fe0f 규칙 준수, symbol 인라인·id 충돌 없음. `xmllint --noout`으로 저장 SVG 검증.
- [ ] **Step 3:** 새로운 루프 구멍(에이전트의 우회 논리) 발견 시 SKILL.md에 명시적 반문(해당 규칙표) 추가 후 Step 1 재실행. (writing-skills REFACTOR)
- [ ] **Step 4:** 최종 검증·커밋 상태를 이슈에 보고: `gh issue comment 6 --body "<..."`, 체크박스 갱신.

### Task 5: 브랜치 마무리

**Files:** 없음

- [ ] **Step 1:** REFACTOR(완료는 Task 4에서 시행)와 이슈 체크리스트 갱신 포함 — `gh issue edit 6` 또는 comment.
- [ ] **Step 2:** push 이전 pre-push-review(저장소 스킬) 통과 후 `git push -u origin issue-6-twemoji-skill`, PR 생성 링크 보고.
