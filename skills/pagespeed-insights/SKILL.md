---
name: pagespeed-insights
description: Use when 사용자가 사이트 URL의 페이지 속도·성능·접근성·SEO 점수를 PageSpeed Insights API로 측정해 달라 하거나 Lighthouse 점수·Core Web Vitals·개선 제안을 정리해 달라고 할 때. /pagespeed-insights / Triggers: measure site performance with PageSpeed Insights API, get Lighthouse score, check Core Web Vitals
---

# Pagespeed Insights

PageSpeed Insights API로 URL의 Lighthouse 점수, 핵심 지표, 실패한 감사(audit), 개선 기회를 한국어 리포트로 정리한다.

## 사용 시점

- 사용자가 URL을 주고 성능·접근성·SEO 점수나 개선안을 요청할 때
- `/pagespeed-insights` 실행 시

리포트만 만든다. 사이트 코드 수정은 하지 않는다.

## 사용하지 않을 때

- 사이트 코드를 직접 수정해야 할 때 (이 스킬은 측정·리포팅 전용)
- 로컬에서 Lighthouse CLI로 이미 분석하는 경우

## 사전 조건

- `PAGESPEED_API_KEY` 환경변수 **필수**. 없으면 호출하지 않고 중단한다.

```sh
test -n "$PAGESPEED_API_KEY" || { echo "PAGESPEED_API_KEY 없음"; echo "발급: https://console.cloud.google.com/apis/credentials"; echo "설정: export PAGESPEED_API_KEY=..."; exit 1; }
```

## API

- 엔드포인트: `GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed`
- 파라미터:
  - `url` — 필수. 분석할 페이지 URL
  - `strategy` — `desktop` | `mobile`. 지정 안 하면 둘 다
  - `category` — 반복 가능. `performance` `accessibility` `best-practices` `seo`
  - `key` — 필수. API key
- 응답: `lighthouseResult.categories`(점수), `lighthouseResult.audits`(감사 상세)

## 작업 순서

1. URL 확인. 없으면 사용자에게 요청.
2. `strategy` 확인. 사용자가 지정 안 하면 `mobile`·`desktop` 둘 다.
3. key 확인. 없으면 위 안내 출력 후 중단.
4. 전략별로 curl 호출, 응답을 `/tmp/psi-$STRATEGY.json`에 저장.
5. 전략별로 점수·핵심 지표·실패 audit·개선 기회 추출.
6. 마크다운 리포트 파일로 작성·저장.

## 명령

호출 (전략별 반복):

```sh
API="https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
for STRATEGY in ${STRATEGY:-mobile desktop}; do
  curl -sS --get "$API" \
    --data-urlencode "url=$URL" \
    --data-urlencode "strategy=$STRATEGY" \
    --data-urlencode "category=performance" \
    --data-urlencode "category=accessibility" \
    --data-urlencode "category=best-practices" \
    --data-urlencode "category=seo" \
    --data-urlencode "key=$PAGESPEED_API_KEY" \
    -o "/tmp/psi-$STRATEGY.json"
done
```

아래 추출 명령은 전략별 파일(`/tmp/psi-$STRATEGY.json`)에 각각 적용한다.

에러 확인 (있으면 여기서 중단):

```sh
jq -r '.error.message // "ok"' /tmp/psi-$STRATEGY.json
```

카테고리 점수 (0~1 → 100점):

```sh
jq -r '.lighthouseResult.categories | to_entries[] | "\(.key)\t\((.value.score // 0) * 100 | round)"' /tmp/psi-$STRATEGY.json
```

핵심 지표:

```sh
jq -r '.lighthouseResult.audits | "FCP: \(.["first-contentful-paint"].displayValue)\nLCP: \(.["largest-contentful-paint"].displayValue)\nTBT: \(.["total-blocking-time"].displayValue)\nCLS: \(.["cumulative-layout-shift"].displayValue)\nSI: \(.["speed-index"].displayValue)"' /tmp/psi-$STRATEGY.json
```

실패 audit (score 0.9 미만, 제안 포함):

```sh
jq -r '.lighthouseResult.audits | to_entries[] | select(.value.score != null and .value.score < 0.9 and .value.scoreDisplayMode != "notApplicable") | "== \(.value.title) [score \(.value.score)]\n\(.value.description)\n"' /tmp/psi-$STRATEGY.json
```

개선 기회 (절감 ms 있는 opportunity):

```sh
jq -r '.lighthouseResult.audits | to_entries[] | select(.value.details.type == "opportunity" and ((.value.details.overallSavingsMs // 0) > 0)) | "\(.value.title): \(.value.displayValue // "n/a") (~\(.value.details.overallSavingsMs)ms)"' /tmp/psi-$STRATEGY.json
```

## 자주 하는 실수

- key 없이 curl 호출 → 사전 조건부터 확인한다
- `strategy` 미지정 시 한쪽만 분석 → 둘 다 돌린다
- score `null`(notApplicable)을 실패로 오인 → `score != null` 조건 필수
- 원본 JSON을 통째로 붙여넣기 → 리포트 형식으로 정리한다

## 리포트 형식

한국어로 다음 순서대로 정리:

1. **점수 표** — 전략별(`mobile`/`desktop`) 4 카테고리, 100점 만점, `lighthouseVersion` 명시
2. **핵심 지표** — 전략별 FCP/LCP/TBT/CLS/SI 값 그대로
3. **실패 audit** — 제목 + 개선 제안, 점수 낮은 순
4. **개선 기회** — 절감 ms 큰 순으로 정렬

없는 필드는 `없음`으로 적는다. 추측으로 채우지 않는다.

리포트는 마크다운 파일로 저장한다. 기본 경로는 프로젝트의 `docs/pagespeed/<domain>-<YYYYMMDD>.md` (`<domain>`은 URL 호스트명). 디렉터리 없으면 만든다. 사용자가 경로를 지정하면 그대로 쓴다. `/tmp`는 재부팅 시 사라지므로 쓰지 않는다.

```markdown
# PageSpeed Insights 리포트 — {URL}

- 분석 시각: {analysisUTCTimestamp}
- Lighthouse: {lighthouseVersion}

## 점수

| 카테고리 | mobile | desktop |
| --- | --- | --- |
| performance | 83 | 81 |
| accessibility | 95 | 95 |
| best-practices | 100 | 100 |
| seo | 100 | 100 |

## 핵심 지표

| 지표 | mobile | desktop |
| --- | --- | --- |
| FCP | 3.1 s | ... |
| LCP | 5.1 s | ... |
| TBT | 450 ms | ... |
| CLS | 0 | ... |
| SI | 5.3 s | ... |

## 실패한 감사 (mobile)

### {audit 제목} [score 0.5]

{개선 제안 설명}

## 개선 기회 (절감 순)

- {제목}: {displayValue} (~{overallSavingsMs}ms)
```
