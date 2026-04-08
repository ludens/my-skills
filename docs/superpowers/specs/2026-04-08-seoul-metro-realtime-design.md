## 개요

`seoul-metro-realtime` 스킬은 사용자가 특정 지하철 역명을 입력했을 때 서울시 실시간 도착정보 API를 조회해 도착 예정 열차를 한국어로 요약해서 보여준다.

목표는 다음과 같다.

- API 키를 `.env`로 안전하게 관리한다.
- 역명 입력만으로 조회 가능하게 한다.
- 동명이역은 호선별 결과를 한 번에 보여준다.
- API 원본 응답을 사람이 읽기 쉬운 문장으로 정리한다.

## 범위

포함:

- 실시간 도착정보 조회
- 역명 정규화
- CSV 기반 역 후보 조회
- `.env` 기반 API 키 로딩
- 동명이역 다중 결과 표시
- API 오류 및 빈 결과 처리

제외:

- 즐겨찾기, 캐시, UI
- 서울시 외 구간 도착정보 보완
- 자연어에서 복잡한 의도 추론

## 사용자 입력 예시

- `서울역 도착시각 알려줘`
- `회기역 실시간 도착`
- `청량리 열차 언제 와?`

## 접근 방식

`uv` 기반 Python 프로젝트로 구성하고, 모듈 2개 이상으로 역할을 분리한다.

- `scripts/station_lookup.py`
  - 역명 정규화
  - CSV 로드 및 인덱싱
  - 동명이역 후보 반환
- `scripts/get_arrivals.py`
  - `.env`에서 API 키 로드
  - 서울시 API 호출
  - 응답 파싱 및 포맷

필요 시 출력 포맷 관련 함수는 `get_arrivals.py` 내부 함수로 시작하고, 복잡해지면 별도 모듈로 분리한다.

사용 라이브러리:

- `httpx`: API 호출
- `python-dotenv`: `.env` 로드
- `pytest`: 테스트

## 데이터 소스

### 1. 실시간 도착 API

- 문서: `skills/seoul-metro-realtime/references/서울시 지하철 실시간 도착정보 API 명세서.md`
- 엔드포인트:
  `http://swopenAPI.seoul.go.kr/api/subway/{KEY}/json/realtimeStationArrival/0/100/{statnNm}`

사용 필드:

- `subwayId`
- `updnLine`
- `trainLineNm`
- `statnId`
- `statnNm`
- `btrainSttus`
- `barvlDt`
- `recptnDt`
- `arvlMsg2`
- `arvlMsg3`
- `arvlCd`
- `lstcarAt`

### 2. 역정보 CSV

- 문서: `skills/seoul-metro-realtime/references/실시간도착_역정보(20260108).csv`
- 사용 컬럼:
  - `SUBWAY_ID`
  - `STATN_ID`
  - `STATN_NM`
  - `호선이름`

CSV는 API 호출용 기본키가 아니라, 역명 후보 확인과 호선명 보강에 사용한다.

## 역명 처리 규칙

### 1. 기본 정규화

- 입력 끝의 `역`은 제거한다.
- 앞뒤 공백을 제거한다.

예:

- `서울역` -> `서울`
- `회기역` -> `회기`

### 2. API 예외 역명 매핑

명세서의 예외 표를 하드코딩한 별칭 맵으로 관리한다.

예:

- `공릉` -> `공릉(서울산업대입구)`
- `천호` -> `천호(풍납토성)`
- `응암` -> `응암순환(상선)`

### 3. 동명이역 정책

역명에 대응하는 CSV 후보가 여러 개면 결과를 호선별로 모두 보여준다. 사용자에게 호선을 다시 묻지 않는다.

예:

- `청량리` 입력 시 1호선, 경의중앙선, 수인분당선 등 가능한 결과를 함께 표시한다.

## API 키 관리

스킬 루트에 `.env.example`을 둔다.

예:

```env
SEOUL_OPEN_API_KEY=your_api_key_here
```

실제 키는 `.env`에만 저장하고 저장소에는 커밋하지 않는다.

로딩 규칙:

1. `skills/seoul-metro-realtime/.env`
2. 필요 시 repo root `.env`

`.env` 로딩은 `python-dotenv`를 사용한다. 직접 파서는 구현하지 않는다.

## 처리 흐름

1. 사용자 입력에서 역명 문자열을 받는다.
2. 역명을 정규화하고 API 예외 역명 맵을 적용한다.
3. CSV에서 후보 역들을 찾는다.
4. 후보가 없으면 역명 확인 메시지를 반환한다.
5. 정규화된 `statnNm`으로 API를 1회 호출한다.
6. 응답을 파싱하고 오류 코드 또는 빈 결과를 확인한다.
7. `recptnDt`와 현재 시각 차이를 계산해 `barvlDt`를 보정한다.
8. 도착정보를 호선별, 상하행별로 정렬한다.
9. 한국어 요약 문장으로 출력한다.

## 출력 형식

출력은 사람이 빠르게 읽을 수 있는 짧은 목록으로 만든다.

예시:

```text
서울 실시간 도착정보

1호선
- 인천행: 2분 후 도착
- 소요산행: 7분 후 도착

경의중앙선
- 문산행: 4분 후 도착
```

가능하면 다음 정보를 포함한다.

- 호선명
- 행선지 또는 방면
- 도착까지 남은 시간
- 급행/일반 여부
- 막차 여부

`barvlDt`가 없거나 부정확하면 `arvlMsg2`, `arvlMsg3`를 보조 문구로 사용한다.

## stale 데이터 보정

명세서 주의사항에 따라 `recptnDt`는 현재 시각과 차이가 날 수 있다.

보정 규칙:

- `delay = now - recptnDt`
- `adjusted_barvl = max(0, barvlDt - delay_seconds)`

보정 가능한 경우 `adjusted_barvl` 기준으로 정렬하고 출력한다.

## 오류 처리

### 설정 오류

- `.env` 없음
- `SEOUL_OPEN_API_KEY` 없음

대응:

- 설정 방법을 짧게 안내하고 종료

### API 오류

- `INFO-100`: 인증키 오류
- `INFO-200`: 해당 데이터 없음
- `ERROR-300` 계열: 요청 파라미터 오류
- `ERROR-500` 계열: 서버 오류

대응:

- 코드와 요약 메시지를 함께 반환

### 도메인 제한

- 서울시 외 구간은 미제공 가능

대응:

- 미지원 가능성을 명시

## 파일 구조

```text
skills/seoul-metro-realtime/
├── pyproject.toml
├── SKILL.md
├── .env.example
├── scripts/
│   ├── get_arrivals.py
│   └── station_lookup.py
├── tests/
│   ├── test_station_lookup.py
│   └── test_arrival_formatting.py
└── references/
    ├── 서울시 지하철 실시간 도착정보 API 명세서.md
    └── 실시간도착_역정보(20260108).csv
```

## SKILL.md 핵심 지침

- 이 스킬은 서울 지하철 실시간 도착정보 조회에 사용한다.
- 먼저 역명을 정규화한다.
- 명세서의 예외 역명 표를 우선 적용한다.
- CSV로 역 후보와 호선 정보를 확인한다.
- `uv run python scripts/get_arrivals.py "<역명>"`로 실제 조회를 수행한다.
- 동명이역은 전 호선 결과를 한 번에 보여준다.
- API 키가 없으면 `.env` 설정 안내를 반환한다.

## 테스트 계획

단위 테스트:

- 역명 정규화
- 예외 역명 매핑
- CSV 후보 검색
- stale 데이터 보정 함수

통합 테스트:

- 실제 키로 `서울`, `청량리`, `공릉` 조회
- `광명` 같은 서울시 외 구간 예외 확인
- 키 누락 상태 확인

## 구현 메모

- 초기 버전은 `uv` 기반 CLI 스크립트로 구현한다.
- 스킬은 스크립트를 실행하는 래퍼 역할에 집중한다.
- 응답 포맷은 짧고 안정적으로 유지한다.
- HTTP 호출은 `httpx`를 사용한다.
- `.env` 로딩은 `python-dotenv`를 사용한다.
