---
name: seoul-metro-realtime
description: Query Seoul subway realtime arrival information for a station name with `uvx seoul-metro-realtime`. Use when Codex needs current Seoul subway arrivals, realtime subway status for a station, or JSON arrival data from the Seoul Open API.
---

# Seoul Metro Realtime

서울 지하철 역명을 받아 `uvx seoul-metro-realtime`로 서울시 실시간 도착정보를 조회한다.

## 사용 시점

- 특정 역의 실시간 도착 예정 열차를 확인해야 할 때
- 서울시 Open API 기반 지하철 도착정보가 필요할 때
- 사람이 읽는 요약 또는 JSON 구조화 데이터가 필요할 때

## 기본 사용법

- 조회: `uvx seoul-metro-realtime "<역명>"`
- 예: `uvx seoul-metro-realtime "서울역"`
- JSON 출력: `uvx seoul-metro-realtime --json "<역명>"`
- 최초 API 키 저장: `uvx seoul-metro-realtime configure`

## API 키

`seoul-metro-realtime`은 아래 순서로 API 키를 찾는다.

1. `SEOUL_OPEN_API_KEY` 환경변수
2. 현재 작업 디렉터리의 `.env`
3. `~/.config/seoul-metro-realtime/config.env`
4. 패키지 루트의 `.env`

키가 없으면 먼저 아래 명령을 실행한다.

```bash
uvx seoul-metro-realtime configure
```

환경변수로 직접 지정해도 된다.

```bash
export SEOUL_OPEN_API_KEY=your_api_key_here
```

## 출력 원칙

- 기본 출력은 한국어 텍스트 요약이다.
- 사용자가 구조화된 처리, 비교, 필터링을 원하면 `--json`을 사용한다.
- JSON 응답의 주요 필드:
  - `station_name`: 조회 역명
  - `generated_at`: 결과 생성 시각
  - `arrivals`: 도착 예정 정보 배열
  - `line_name`: 호선 이름
  - `direction`: 방면
  - `destination`: 행선지
  - `eta`: 사람이 읽는 도착 문구
  - `seconds`: 남은 초
  - `status`: 열차 상태
  - `is_last_train`: 막차 여부

## 사용 예

텍스트 요약:

```bash
uvx seoul-metro-realtime "서울역"
```

JSON 조회:

```bash
uvx seoul-metro-realtime --json "서울역"
```

JSON에서 특정 정보만 골라야 하면 `jq` 같은 표준 도구로 후처리한다.

```bash
uvx seoul-metro-realtime --json "서울역" | jq '.arrivals[] | {line_name, direction, destination, eta}'
```

## 문제 해결

- `uvx`가 없으면 `uv` 설치가 필요하다.
- API 키 오류가 나면 `uvx seoul-metro-realtime configure`로 키를 다시 저장하거나 `SEOUL_OPEN_API_KEY`를 확인한다.
- 현재 작업 디렉터리의 `.env`를 쓸 때는 `SEOUL_OPEN_API_KEY=<발급받은_키>` 형식을 사용한다.

## 검증

- 키 저장: `uvx seoul-metro-realtime configure`
- 키 없는 상태 확인: `uvx seoul-metro-realtime "서울역"` 실행 시 API 키 설정 안내가 나온다.
- 키 있는 상태 조회: `uvx seoul-metro-realtime "서울역"`
