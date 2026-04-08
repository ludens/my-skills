---
name: seoul-metro-realtime
description: Query Seoul subway realtime arrival information for a station name using the Seoul open API. Use when Codex needs to look up train arrival times, realtime subway status for a station, or summarize arrivals across duplicate station names. Supports `.env`-managed API keys and station alias normalization for Seoul Metro names.
---

# Seoul Metro Realtime

서울 지하철 역명을 받아 서울시 실시간 도착정보 API를 조회하고, 같은 역명이 여러 노선에 걸쳐 있으면 한 번에 묶어서 요약한다.

## 사용 시점

- 특정 역의 실시간 도착 예정 열차를 확인해야 할 때
- 동명이역 포함 결과를 한 번에 정리해야 할 때
- 서울시 open API 기반 지하철 도착정보가 필요할 때

## 기본 사용법

- 스킬 루트에서 실행: `uv run python scripts/get_arrivals.py "<역명>"`
- 예: `uv run python scripts/get_arrivals.py "서울역"`
- 역명 끝의 `역`은 자동 정규화된다.
- 일부 예외 역명은 `scripts/station_lookup.py`의 alias map으로 보정한다.

## 파일 역할

- `scripts/station_lookup.py`: 역명 정규화, alias 처리, CSV 기반 역 후보 조회
- `scripts/get_arrivals.py`: `.env` 로드, API 호출, payload 파싱, stale 시간 보정, 출력 포맷
- `references/실시간도착_역정보(20260108).csv`: 역/노선 기준 데이터 소스
- `references/서울시 지하철 실시간 도착정보 API 명세서.md`: API 필드와 응답 구조 확인용 참고 문서

## 실행 규칙

1. 먼저 `scripts/station_lookup.py`로 역명 정규화와 후보 조회를 수행한다.
2. API 키는 아래 순서로 찾는다.
   - `skills/seoul-metro-realtime/.env`
   - 필요 시 repo root `.env`
3. 환경변수 이름은 `SEOUL_OPEN_API_KEY`를 사용한다.
4. API 응답은 `extract_arrival_rows()`로 해석한다.
   - `INFO-200`이면 빈 결과로 처리한다.
   - 다른 에러 코드는 사용자에게 드러나는 오류로 변환한다.
5. 도착 시간은 `adjust_arrival_seconds()`로 수신 시각 기준 stale 보정을 적용한다.
6. 최종 응답은 `format_arrivals_summary()` 형식으로 한국어 요약을 출력한다.

## 출력 원칙

- 헤더는 `<역명> 실시간 도착정보`
- 노선별로 그룹화해서 출력
- 같은 역명이 여러 노선에 있으면 모두 포함
- 급행/막차 여부를 괄호 메타데이터로 표시
- 데이터가 없으면 빈 결과임을 명확히 설명

## 문제 해결

- `.env` 또는 `SEOUL_OPEN_API_KEY`가 없으면 `skills/seoul-metro-realtime/.env` 파일을 만들고 `SEOUL_OPEN_API_KEY=...`를 넣도록 안내한다.
- API 필드 의미가 헷갈리면 `references/서울시 지하철 실시간 도착정보 API 명세서.md`만 추가로 읽는다.
- 역명 예외 처리가 필요하면 `scripts/station_lookup.py`의 alias map과 CSV 데이터를 함께 확인한다.

## 검증

- 테스트: `uv run pytest -v`
- 단일 실행: `uv run python scripts/get_arrivals.py "서울역"`
