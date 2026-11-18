# fetch-lrc 테스트 기록

실행일: 2026-11-18
환경: Apple M1, RAM 8GB, macOS, Python 3.15.2, ffmpeg/ffprobe (`/opt/homebrew/bin`)
네트워크: LRCLIB 공개 API (`https://lrclib.net/api`)

## 테스트 곡

| 역할 | 곡 | 로컬 파일 | 길이 | 출처 |
|------|-----|-----------|------|------|
| 한국어, 앨범 버전 | IU - Celebrity | `IU - Celebrity.m4a` (AAC, 태그 없음) | 195.7초 | YouTube 공식 오디오 |
| 영어, 태그 없음 | Imagine Dragons - Thunder | `Imagine Dragons - Thunder.m4a` (AAC, 태그 없음) | 183.4초 | YouTube `GtEvysh1654` |
| 한국어, MV 버전 | IU - Celebrity | `IU - Celebrity.m4a` (MV, 198.1초) | 198.1초 | YouTube `0-q1KafFCLU` |

두 곡 모두 태그를 비웠다. 파일명 `아티스트 - 제목` 파싱 경로를 검증하기 위해서다. MV 버전은 길이 불일치 케이스용이다.

## 결과 요약

| 케이스 | 기대 | 실제 | 판정 |
|--------|------|------|------|
| IU 앨범 버전 (195.7초) | 길이 일치 → synced `.lrc` 생성 | `lrclib-synced`, id 2116041, 51줄, exit 0 | 통과 |
| Thunder (183.4초) | 태그 없이 파일명 파싱 후 생성 | `lrclib-synced`, id 3721096, 54줄, exit 0 | 통과 |
| IU MV 버전 (198.1초) | 길이 불일치 → 저장 안 함 | `196.0초` vs `198.1초` 2.1초 차이 메시지, exit 4, `.lrc` 미생성 | 통과 |
| IU 재실행 | `.lrc.bak` 백업 | `IU - Celebrity.lrc.bak` 생성, 내용 보존 | 통과 |
| `--lyrics` 일반 가사(타임스탬프 없음) | 거부, 파일 미생성 | `타임스탬프가 없음... 저장하지 않는다.`, exit 2 | 통과 |
| 감소 타임스탬프 `--lyrics` | 중단, 파일 미생성 | `타임스탬프가 감소하는 줄: [00:05.00] b`, exit 3 | 통과 |
| 마지막 타임스탬프가 곡 길이 초과 | 중단 | 길이(198.1초) 1초 초과 메시지, exit 3 | 통과 |
| 메타데이터 없는 미등록 곡 | 중단, 가사 요청 | exit 2, `.lrc` 미생성 | 통과 |

## 타이밍 대조: 곡 전체 길이만

줄별 오프셋은 재지 않는다. 아래 길이 비교가 유일한 타이밍 검증이다.

| 곡 | 로컬 길이 | LRCLIB 길이 | 차이 | 저장 |
|----|-----------|-------------|------|------|
| IU - Celebrity (앨범) | 195.7초 | 196.0초 | 0.3초 | 함 |
| Imagine Dragons - Thunder | 183.4초 | 183.0초 | 0.4초 | 함 |
| IU - Celebrity (MV) | 198.1초 | 196.0초 | 2.1초 | 거부 |

## 구조 검증 (자체 파서)

| 곡 | 타임스탬프 줄 수 | 단조 증가 | 마지막 타임스탬프 | 곡 길이 | CRLF |
|----|------------------|-----------|-------------------|---------|------|
| IU - Celebrity | 51 | True | 191.37초 | 195.7초 | 없음 |
| Imagine Dragons - Thunder | 54 | True | 170.67초 | 183.4초 | 없음 |

## 가사 내용 대조

`.lrc`에서 뽑은 줄이 실제 곡 가사와 일치하는지만 눈으로 확인했다. 시각 대조는 하지 않았다.

IU - Celebrity: `세상의 모서리` / `You are my celebrity` / `보이니 그 유일함이 얼마나` / `발자국마다 이어진 별자리`
Imagine Dragons - Thunder: `Just a young gun with a quick fuse` / `Fit the box, fit the mold, have a seat` / `Thunder, feel the thunder` / `Lightning then the thunder`

두 곡 모두 후렴 반복 구간이 각 위치에 맞게 들어갔고, 가사 전문이 원곡과 일치한다.

## 처리 시간

LRCLIB 조회만 하므로 곡당 1초 미만이다.

```
IU - Celebrity: 0.73초 total (0.10 user)
```

## 검증하지 못한 것

- **줄별 시각 오프셋은 확인하지 않았다.** 길이 비교만 한다는 방침에 따른 것이다. 정확도는 LRCLIB DB 값에 의존한다.
- LRCLIB이 plain만 제공하는 실제 곡, 검색 폴백이 다른 버전을 잡는 경우는 실측하지 않았다.
- Windows/Linux, ffprobe 미설치 환경은 확인하지 않았다.
