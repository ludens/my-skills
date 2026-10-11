---
name: pagespeed-insights
description: 사이트 URL의 PageSpeed Insights 점수(성능·접근성·권장사항·SEO)와 개선 제안을 조회해 한국어 리포트로 정리할 때 사용합니다. /pagespeed-insights
---

# Pagespeed Insights

PageSpeed Insights API로 URL의 Lighthouse 점수, 핵심 지표, 실패한 감사(audit), 개선 기회를 한국어 리포트로 정리한다.

## 사용 시점

- 사용자가 URL을 주고 성능·접근성·SEO 점수나 개선안을 요청할 때
- `/pagespeed-insights` 실행 시

리포트만 만든다. 사이트 코드 수정은 하지 않는다.

## 사전 조건

- `PAGESPEED_API_KEY` 환경변수 **필수**. 없으면 호출하지 않고 중단한다.

```sh
test -n "$PAGESPEED_API_KEY" || { echo "PAGESPEED_API_KEY 없음"; echo "발급: https://console.cloud.google.com/apis/credentials"; echo "설정: export PAGESPEED_API_KEY=..."; exit 1; }
```

## API

- 엔드포인트: `GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed`
- 파라미터:
  - `url` — 필수. 분석할 페이지 URL
  - `strategy` — `desktop`(기본) | `mobile`
  - `category` — 반복 가능. `performance` `accessibility` `best-practices` `seo`
  - `key` — 필수. API key
- 응답: `lighthouseResult.categories`(점수), `lighthouseResult.audits`(감사 상세)

## 작업 순서

1. URL 확인. 없으면 사용자에게 요청.
2. key 확인. 없으면 위 안내 출력 후 중단.
3. curl 호출, 응답을 `/tmp/psi.json`에 저장.
4. 점수·핵심 지표·실패 audit·개선 기회 추출.
5. 한국어 리포트 작성.

## 명령

호출:

```sh
API="https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
curl -sS --get "$API" \
  --data-urlencode "url=$URL" \
  --data-urlencode "strategy=mobile" \
  --data-urlencode "category=performance" \
  --data-urlencode "category=accessibility" \
  --data-urlencode "category=best-practices" \
  --data-urlencode "category=seo" \
  --data-urlencode "key=$PAGESPEED_API_KEY" \
  -o /tmp/psi.json
```

에러 확인 (있으면 여기서 중단):

```sh
jq -r '.error.message // "ok"' /tmp/psi.json
```

카테고리 점수 (0~1 → 100점):

```sh
jq -r '.lighthouseResult.categories | to_entries[] | "\(.key)\t\((.value.score // 0) * 100 | round)"' /tmp/psi.json
```

핵심 지표:

```sh
jq -r '.lighthouseResult.audits | "FCP: \(.["first-contentful-paint"].displayValue)\nLCP: \(.["largest-contentful-paint"].displayValue)\nTBT: \(.["total-blocking-time"].displayValue)\nCLS: \(.["cumulative-layout-shift"].displayValue)\nSI: \(.["speed-index"].displayValue)"' /tmp/psi.json
```

실패 audit (score 0.9 미만, 제안 포함):

```sh
jq -r '.lighthouseResult.audits | to_entries[] | select(.value.score != null and .value.score < 0.9 and .value.scoreDisplayMode != "notApplicable") | "== \(.value.title) [score \(.value.score)]\n\(.value.description)\n"' /tmp/psi.json
```

개선 기회 (절감 ms 있는 opportunity):

```sh
jq -r '.lighthouseResult.audits | to_entries[] | select(.value.details.type == "opportunity" and ((.value.details.overallSavingsMs // 0) > 0)) | "\(.value.title): \(.value.displayValue // "n/a") (~\(.value.details.overallSavingsMs)ms)"' /tmp/psi.json
```

## 리포트 형식

한국어로 다음 순서대로 정리:

1. **점수 표** — 4 카테고리, 100점 만점, `strategy`·`lighthouseVersion` 명시
2. **핵심 지표** — FCP/LCP/TBT/CLS/SI 값 그대로
3. **실패 audit** — 제목 + 개선 제안, 점수 낮은 순
4. **개선 기회** — 절감 ms 큰 순으로 정렬

없는 필드는 `없음`으로 적는다. 추측으로 채우지 않는다.
