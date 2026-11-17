---
name: navidrome
description: Use when installing, configuring, administering, or troubleshooting Navidrome (self-hosted Subsonic-compatible music server), including Docker setup, ND_ environment variables and config options, navidrome CLI commands, Subsonic/OpenSubsonic API compatibility, smart playlists, multi-library, scrobbling, plugins, Jukebox, Jellyfin API, reverse-proxy authentication, or library, playlist, and artwork problems. / 트리거 - 네이비드롬 설치·설정·운영·트러블슈팅, ND_ 환경변수, navidrome CLI, Subsonic API, 리버스 프록시 인증, M3U 재생목록, 아트워크
---

# Navidrome

## 개요

자체 호스팅 음악 서버. 태그 기반으로 라이브러리를 구성하고 음악 파일을 쓰지 않는다. Subsonic API v1.16.1 호환 클라이언트를 지원한다.

자주 틀리는 사실 — 먼저 확인:

- 공식 이미지는 `navidrome/navidrome:latest`. `deluan/navidrome` 아님.
- 기본 포트 `4533`.
- 컨테이너 경로: `/music`(읽기 전용 권장), `/data`(DB·캐시, 쓰기 필요).
- 설정 우선순위: 환경변수 > CLI 인자 > 설정 파일.
- Jellyfin API 활성화 변수: `ND_JELLYFIN_ENABLED`(기본 `false`).
- 프록시 인증: `ExtAuth.TrustedSources` + `ExtAuth.UserHeader`(기본 `Remote-User`). `ReverseProxyHeader` 아님.
- 첫 관리자는 웹 UI에서 생성. CLI 사용자 명령은 기존 관리자가 필요하다.

## 사용 시점

- 설치·Docker 배포·권한 오류·첫 실행
- 설정값, 환경변수, 기본값 확인
- 사용자·백업·스캔 등 CLI 작업
- 기능 설정, 외부 연동, Subsonic 클라이언트 호환성
- 리버스 프록시/SSO, 재생목록·아트워크·스캔 문제

## 참조 파일

관련 범위면 해당 파일을 읽는다.

| 범위 | 파일 |
| --- | --- |
| 설정 방법, 전체 옵션·환경변수·기본값, 기간/크기 형식 | `reference/configuration.md` |
| CLI 명령 전체, 사용자·백업·스캔, Docker에서 CLI 실행 | `reference/cli.md` |
| 기능, 외부 연동, Subsonic API, 외부 인증, FAQ | `reference/features-api.md` |

## 빠른 시작 (Docker)

```yaml
services:
  navidrome:
    image: navidrome/navidrome:latest
    user: 1000:1000  # /data 소유주이자 /music을 읽을 수 있는 UID:GID
    ports:
      - "4533:4533"
    restart: unless-stopped
    volumes:
      - "/path/to/data:/data"
      - "/path/to/music:/music:ro"
```

`docker compose up -d`. `user` 값은 `id -u`, `id -g`, `ls -n /path/to/music`으로 맞춘다. `PUID`/`PGID`는 무시된다. `user`를 빼면 root로 실행되므로 운영 환경에서 하지 않는다.

첫 실행:

1. `docker logs navidrome`에서 `Navidrome server is ready!` 확인.
2. `http://localhost:4533` 접속 → 관리자 생성.
3. 백그라운드 스캔 대기(1천 곡 미만 1분 내, 1만 곡 1~5분).
4. Albums → 앨범 → 재생.

설정 파일을 쓰면 `navidrome.toml`을 `/data`에 두고 `ND_CONFIGFILE=/data/navidrome.toml`을 지정한다.

## 문제 해결

| 증상 | 원인과 조치 |
| --- | --- |
| `unable to open database file: no such file or directory`로 종료 | `/data` 쓰기 권한 없음. `sudo chown -R $(id -u):$(id -g) /path/to/data` |
| 웹 UI는 뜨는데 라이브러리가 비어 있음 | `/music` 읽기 권한 없음. `sudo chmod -R a+rX /path/to/music` 또는 소유주 변경 |
| 브라우저 접속 불가 | 포트 `4533` 방화벽·매핑(`-p 4533:4533`) 확인 |
| M3U 재생목록이 안 보임 | 관리자 먼저 생성, `touch /path/to/music/*.m3u` 후 재스캔 |
| 아트워크가 없음 | `navidrome artwork` 명령으로 탐색 경로 확인 |

로그는 stdout만 출력한다. Docker는 `docker logs`, systemd는 `journalctl -u navidrome.service`.

## 흔한 실수

- CLI 플래그는 소문자로만 쓴다(`--musicfolder`). 전체 목록은 `navidrome --help`.
- `backup restore`, `backup prune`, `missing fix`는 되돌릴 수 없다. 먼저 `backup create`.
- Docker에서 CLI는 반드시 컨테이너 안에서 실행해야 같은 `/data`와 설정을 본다.

출처: https://www.navidrome.org/docs/ (문서 기준 2026-11). 상세 항목은 참조 파일과 공식 문서에서 최신값을 확인한다.
