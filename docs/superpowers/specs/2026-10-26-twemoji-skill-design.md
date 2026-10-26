# twemoji 스킬 설계 (짧은 설계문)

날짜: 2026-10-26 · 이슈: #6 · 브랜치: `issue-6-twemoji-skill`

## 의도·이유

SVG 구조도·다이어그램에 이모지 아이콘을 쓸 때, 코드포인트 변환과 CDN 경로를 매번 잘못 계산하는 문제를 스킬로 해결한다. `aws-icons`와 같은 자리의 카탈로그형 레퍼런스 스킬.

## 접근 방식

| 방식 | 내용 | 판정 |
| --- | --- | --- |
| 1. 레퍼런스 + 경량 스크립트 | SKILL.md + `fetch-emoji.sh` | **선택됨** — 코드포인트 변환(ZWJ·skin tone·fe0f)은 손계산이 자주 틀려 스크립트가 필요 |
| 2. 순수 레퍼런스 (스크립트 없음) | SKILL.md만 | 기각 — 사람·에이전트 모두 변환 실수 잦음 |

## 사실 확인 (실동작 검증 완료)

- 원본 `twitter/twemoji`는 보관(archived)됨 (마지막 v14.0.2). 유지보수 포크 **`jdecked/twemoji`** 사용, 최신 **v17.0.3** (2026-06-01).
- CDN: `https://cdn.jsdelivr.net/gh/jdecked/twemoji@17.0.3/assets/svg/<codepoint>.svg` → 🇰🇷(`1f1f0-1f1f7`), ZWJ 가족(`1f468-200d-1f469-200d-1f466`) 200 확인.
- **fe0f(변이 선택자 U+FE0F)는 파일명에서 제거**: `2764-fe0f.svg` 404, `2764.svg` 200 확인. (일부 예외 대비: 제거 실패 시 원본 코드포인트로 재시도)
- 파일명 규칙: 코드포인트 hex 소문자, 앞자리 0 없음(`00a9`→`a9`… 단 실제 예외는 스크립트 폴백이 처리), ZWJ(`200d`)·skin tone(`1f3fb`–`1f3ff`)은 `-`로 연결.
- 모든 SVG 통일: `viewBox="0 0 36 36"`, 크기 변형 없음, 색은 파일 안에 있음.

## 스킬 구성

```
skills/twemoji/
  SKILL.md          # 소스·URL 패턴, 코드포인트 규칙, symbol 인라인 규칙, 배치·주의사항
  fetch-emoji.sh    # 이모지 → 코드포인트 변환 → CDN 다운로드 + 캐시
```

### SKILL.md 담을 내용

1. 소스(포크 사유, 버전 고정 v17.0.3), CDN 패턴, GitHub raw 대체 URL
2. 코드포인트 변환 규칙 표(이모지 → 파일명 예시: `1f600`, `2764`, `1f1f0-1f1f7`, ZWJ, skin tone) — 실제 틀리는 사례 중심
3. SVG 인라인 규칙: `viewBox="0 0 36 36"` 그대로 `<symbol>`로, gradient/clipPath `id` 충돌 슬러그 네임스페이싱, 재색칠하지 않음
4. 배치: 이모지 크기 균일(24–48px 권장), 텍스트 라벨과 조합, aws-icons·cloudflare-icons와의 병행 사용
5. 빠른 선택 표: 다이어그램 상황별 이모지
6. 자주 틀리는 것 + 검증 방법(xmllint, 렌더 확인)

### fetch-emoji.sh 시그니처

```bash
bash scripts/fetch-emoji.sh assets/twemoji "🇰🇷" "❤️" "🧑‍💻"   # 저장 디렉터리 지정
bash scripts/fetch-emoji.sh assets/twemoji --list 1f1f0-1f1f7   # 파일명 확인만
```

이미지 ↔ 파일명 변환은 셸(sed 등)에서 안정적으로 불가능한 유니코드 연산이므로 내부적으로 `python3` 한 줄(`codePointAt` 방식) 사용 — 추가 의존성 없음. 캐시: `~/.cache/twemoji/<version>/`.

이미지 프레젠테이션 변화(v17) — Emoji_Presentation=No 이모지가 텍스트 표기와 다른 검증 필요하면 폴백으로 흡수.

## 목표·비목표

- 목표: 다이어그램용 이모지 SVG 다운로드·삽입 스킬 하나.
- 비목표: HTML 웹삽입(`<img>`/twemoji 라이브러리 API)·PNG 변형·node 라이브러리 사용법·원본(twitter/twemoji 대응).

## 남은 것 (작성자 몫)

- 정확한 빠른 선택 이모지 목록 — SKILL.md 작성 중 선정
- upload 방식은 저장소 관례 따름

## 테스트 (writing-skills TDD)

1. RED: 스킬 없이 하위 에이전트가 "🇰🇷 ❤️ 🧑‍💻 넣은 SVG" 만들라고 요청 → 실패 패턴 기록
2. GREEN: 스킬+스크립트 작성, 스크립트로 실제 다운로드 검증(이슈 체크리스트)
3. 스킬 적용 시나리오 재테스트
