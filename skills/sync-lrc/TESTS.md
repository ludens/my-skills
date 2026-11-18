# sync-lrc 테스트 기록

실행일: 2026-11-18
환경: Apple M1, RAM 8GB, macOS, Python 3.15.2, ffmpeg/ffprobe (`/opt/homebrew/bin`)
네트워크: LRCLIB 공개 API (`https://lrclib.net/api`)

## 테스트 곡

| 역할 | 곡 | 로컬 파일 | 길이 | 출처 |
|------|-----|-----------|------|------|
| 한국어, 후렴 반복 | IU - Celebrity | `IU - Celebrity.m4a` (AAC 129kbps, 태그 있음) | 198.1초 | YouTube `0-q1KafFCLU` |
| 영어, 태그 없음 | Imagine Dragons - Thunder | `Imagine Dragons - Thunder.m4a` (AAC, 태그 없음) | 183.4초 | YouTube `GtEvysh1654` |

두 번째 곡은 태그를 일부러 비웠다. 파일명 `아티스트 - 제목` 파싱 경로를 검증하기 위해서다.

## 결과 요약

| 케이스 | 기대 | 실제 | 판정 |
|--------|------|------|------|
| IU, 일반 실행 | synced `.lrc` 생성 | `lrclib-synced`, id 2116041, 51줄, exit 0 | 통과 |
| Thunder, 일반 실행 | 태그 없이 파일명 파싱 후 생성 | `lrclib-synced`, id 3721096, 54줄, exit 0 | 통과 |
| IU 재실행 | `.lrc.bak` 백업 | `IU - Celebrity.lrc.bak` 생성, exit 0 | 통과 |
| `--lyrics` 일반 가사(타임스탬프 없음) | 거부, 파일 미생성 | `가사 파일에 타임스탬프가 없음... 저장하지 않는다.`, exit 2 | 통과 |
| 감소 타임스탬프 | 중단, 파일 미생성 | `타임스탬프가 감소하는 줄: [00:05.00] b`, exit 3, 출력 디렉터리 미생성 | 통과 |
| 마지막 타임스탬프가 곡 길이 초과 | 중단 | 길이(198.1초) 1초 초과 메시지, exit 3 | 통과 |
| 메타데이터 없는 미등록 곡 | 중단, 가사 요청 | exit 2, `.lrc` 미생성 | 통과 |

## 구조 검증 (자체 파서)

| 곡 | 타임스탬프 줄 수 | 단조 증가 | 마지막 타임스탬프 | 곡 길이 | CRLF |
|----|------------------|-----------|-------------------|---------|------|
| IU - Celebrity | 51 | True | 191.37초 | 198.1초 | 없음 |
| Imagine Dragons - Thunder | 54 | True | 170.67초 | 183.4초 | 없음 |

## 가사 샘플 10줄 육안 대조

`.lrc`에서 무작위로 10줄씩 뽑아 해당 시점 오디오의 음량을 쟀다. 무음 구간에 타임스탬프가 찍히지 않았는지 확인하는 용도다.

IU - Celebrity:

| 타임스탬프 | 음량 | 가사 |
|------------|------|------|
| 00:10.32 | -12.1 dB | 걸음걸이, 옷차림, |
| 00:13.10 | -9.1 dB | 이어폰 너머 play list |
| 00:20.11 | -8.9 dB | 넌 모르지 |
| 00:27.20 | -10.7 dB | 어딜 비추는지 |
| 01:15.89 | -7.0 dB | You are my celebrity |
| 01:22.59 | -11.9 dB | 심장소린 too quiet |
| 01:29.77 | -7.3 dB | 상상력, identity |
| 01:54.36 | -8.5 dB | You are my celebrity |
| 02:06.70 | -7.7 dB | 보이니 그 유일함이 얼마나 |
| 02:20.16 | -9.6 dB | 그 서투른 걸음이 새겨놓은 밑그림 |

Imagine Dragons - Thunder:

| 타임스탬프 | 음량 | 가사 |
|------------|------|------|
| 00:06.27 | -11.1 dB | I was dreaming of bigger things and |
| 00:08.76 | -11.7 dB | Wanna leave my own life behind |
| 00:11.96 | -11.5 dB | Not a "Yes, sir", not a follower |
| 00:14.72 | -12.5 dB | Fit the box, fit the mold, have a seat |
| 00:37.60 | -6.4 dB | Lightning then the thunder |
| 00:43.12 | -7.7 dB | Lightning then the thunder, thunder |
| 01:14.45 | -7.6 dB | Thunder, thunder, thun- |
| 01:17.05 | -7.8 dB | Thunder, th-th-thunder, thunder |
| 01:31.66 | -7.5 dB | Thunder, feel the thunder |
| 02:40.25 | -7.0 dB | (Whoa-oh-oh) thunder, thunder, thun- |

가사 텍스트는 두 곡 모두 실제 곡 가사와 일치한다. 후렴 반복 구간(01:15, 01:54의 동일 후렴 / 00:37, 00:43, 01:31의 반복)도 각 위치에 맞게 들어갔다.

## 처리 시간

LRCLIB 조회만 하므로 곡당 1초 미만이다.

```
IU - Celebrity: 0.73초 total (0.10 user)
```

전사 모델을 쓰지 않으므로 모델 다운로드·추론 시간이 없다. 이 스킬 이전 버전에서 검토했던 mlx-whisper 경로는 스코프에서 제외되어 설치·검증하지 않았다.

## 검증하지 못한 것

- **±1초 청취 오차 확인은 하지 않았다.** 이 환경은 오디오를 들어볼 수 없다. 타임스탬프 정확도는 LRCLIB DB 값에 그대로 의존하며, 위 음량 검사는 "무음 아님"만 증명한다.
- 로컬 파일과 LRCLIB 재생시간이 다른 버전(라이브·편집본·리마스터) 케이스는 실측하지 않았다. 코드상 `/api/search` 폴백이 ±2초 필터로 걸러내지만, 통과한 다른 버전이 실제로 어긋나는지는 확인하지 않았다.
- Windows/Linux, ffprobe 미설치 환경은 확인하지 않았다.
- plain 가사만 있는 LRCLIB 곡은 중단 메시지 경로만 코드로 확인했다. 실제 그런 곡으로는 돌려보지 않았다.
