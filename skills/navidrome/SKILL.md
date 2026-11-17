---
name: navidrome
description: Navidrome 서버와 음악 라이브러리를 운영할 때 사용합니다. 스캔·누락 파일·DB 백업/복구·재생목록·멀티라이브러리·사용자 관리와 태그 기반 앨범 그룹핑(컴필레이션, 다중 디스크, 다중 아티스트, Persistent ID)을 다룹니다. / Triggers - 네이비드롬 운영, 라이브러리 스캔, 앨범이 쪼개짐, 태그 반영, 누락 파일, DB 백업·복구, ND_ 환경변수, navidrome CLI, Subsonic API, M3U 재생목록, 아트워크
---

# Navidrome 운영

## 개요

Navidrome은 음악 파일을 읽기만 하고 쓰지 않는다. 라이브러리 구조는 전부 태그에서 나오고, 사용자 상태(재생 횟수·별점·재생목록·즐겨찾기)는 DB에 남는다.

운영은 두 저장소를 다루는 일이다.

| 저장소 | 내용 | 수정 수단 |
| --- | --- | --- |
| 음악 폴더 | 오디오 파일과 태그, 커버 이미지, `.m3u`, `.ndignore` | 외부 태거(Picard, beets, Mp3tag) |
| `DataFolder` (`/data`) | `navidrome.db`, 캐시, `navidrome.toml` | Navidrome 자체, `navidrome backup` |

**핵심 원칙: 태그 수정과 파일 이동을 같은 스캔에 넣지 않는다.** 둘을 한 번에 하면 Navidrome이 기존 파일과 새 파일을 연결하지 못해 재생 횟수·별점이 끊긴다. 순서는 "태그 수정 절차"를 따른다.

## 자주 틀리는 사실

- 공식 이미지 `navidrome/navidrome:latest`. `deluan/navidrome` 아님.
- 컨테이너 경로: `/music`(읽기 전용 권장), `/data`(쓰기 필요, DB·설정·캐시).
- 설정 우선순위: 환경변수 > CLI 인자 > 설정 파일.
- CLI는 서버와 같은 `-c/--configfile`·`ND_` 값을 봐야 같은 DB를 본다. Docker에서는 컨테이너 안에서 실행한다.
- 앨범·트랙 ID는 계산값이다. `PID.Album`/`PID.Track` 입력 태그가 바뀌면 ID도 바뀐다.
- 기본값: `PID.Album = musicbrainz_albumid|albumartistid,album,albumversion,releasedate`, `PID.Track = musicbrainz_trackid|albumid,discnumber,tracknumber,title`.
- 누락 파일은 기본적으로 DB에서 지우지 않는다(`Scanner.PurgeMissing=never`). 지우면 재생 횟수·별점·재생목록 항목이 함께 사라진다.
- 첫 관리자는 웹 UI에서 만든다. CLI `user` 명령은 관리자가 이미 있어야 동작한다.

## 태그와 앨범 그룹핑

Navidrome은 폴더·파일명을 무시하고 태그만 본다. 앨범이 쪼개지거나 합쳐지는 문제는 거의 항상 태그 불일치다.

앨범의 모든 트랙에서 같아야 하는 값:

- `Album` (`TALB` / `ALBUM` / `©alb`)
- `Album Artist` (`TPE2` / `ALBUMARTIST` / `aART`)
- `Release Date` (`YEAR` 또는 `RELEASEDATE`. `DATE`는 **recording date**라 다른 필드다)
- `Album Version` (`ALBUMVERSION`/`MUSICBRAINZ_ALBUMCOMMENT`) — 같은 이름 앨범 구분에 쓰인다

트랙마다 달라도 되는 값: `Title`, `Artist`, `Track Number`, `Disc Number`, `Genre`.

규칙:

- Various Artists 컴필레이션: 모든 트랙 `Album Artist = Various Artists`, 그리고 `TCMP=1`(ID3) / `COMPILATION=1`(Vorbis).
- 다중 디스크: `Album` 제목을 디스크별로 바꾸지 않는다. `DISCNUMBER=1/2`, `2/2`(`TPOS`)만 다르게 준다.
- 다중 아티스트: 단일 `ARTIST`를 구분자로 쪼개는 것보다 다중값 `ARTISTS`가 정확하다. 둘 다 있으면 `ARTIST`는 표시명으로만 쓰이고 쪼개지지 않는다.
- 태그를 고친 뒤 반드시 스캔한다. 전체 스캔(`navidrome scan --full`)은 mtime을 무시하고 모든 파일을 다시 읽는다.
- 태그가 실제로 어떻게 읽히는지 확인: `navidrome inspect "<file>"` (`--format pretty|yaml|json`). 원본 태그와 매핑된 값을 함께 보여준다. UI에서는 곡 정보 → Raw Tags.

태그 이름·포맷별 차이·PID 동작은 `reference/tagging.md`에 정리돼 있다.

## 스캔과 누락 파일

스캔은 새 파일·변경 파일·사라진 파일을 찾는다. 사라진 파일은 "missing"으로 표시만 하고 DB에 남긴다.

주요 설정 (전체는 `reference/configuration.md`):

| 설정 | 기본값 | 운영 의미 |
| --- | --- | --- |
| `Scanner.Enabled` | `true` | 자동 스캔 |
| `Scanner.Schedule` | `0` | cron 예약. `0`이면 비활성 |
| `Scanner.ScanOnStartup` | `true` | 시작 시 스캔 |
| `Scanner.WatcherWait` | `5s` | 파일 변경 후 대기. `0`이면 watcher 끔 |
| `Scanner.PurgeMissing` | `never` | `always`/`full`은 누락 항목을 DB에서 영구 삭제 |
| `AutoImportPlaylists` | `true` | `.m3u` 파일을 재생목록으로 가져옴 |

```bash
navidrome scan                      # 변경분 스캔
navidrome scan --full               # 전체 재읽기 (태그 일괄 수정 후)
navidrome scan -t 1:Music/Rock      # 특정 라이브러리:폴더만
navidrome missing list --format json
navidrome missing fix "Rock/Old/track01.mp3" "Rock/New/track01.mp3"
```

- `missing fix`는 누락 파일의 재생 횟수·별점·즐겨찾기·북마크를 새 파일로 옮긴다. 대상 파일은 이미 스캔되어 있어야 한다.
- 대량 `missing fix` 전에는 `navidrome backup create`를 먼저 한다. 되돌릴 수 없다.
- `Scanner.PurgeMissing=always`는 파일이 잠깐 없어진 것만으로도 기록을 삭제한다. 마운트가 불안정하면 `never`를 유지한다.
- 라이브러리에서 폴더·패턴을 빼려면 음악 폴더에 `.ndignore`(`.gitignore` 문법)를 둔다. 빈 파일이면 그 폴더 전체를 무시한다.

## 백업과 복구

백업 대상은 **DB만**이다. 음악 파일과 `navidrome.toml`은 별도로 백업한다.

```toml
[Backup]
Path = "/backup"
Schedule = "0 3 * * *"
Count = 7
```

```bash
navidrome backup create                      # 지금 백업
navidrome backup prune --keep-count 7        # 오래된 백업 정리
navidrome backup restore --backup-file navidrome_backup_YYYY.MM.DD_HH.MM.SS.db
```

복구 순서 — 서버를 먼저 멈춘다:

```bash
docker compose stop navidrome
docker compose run --rm navidrome backup restore --backup-file navidrome_backup_YYYY.MM.DD_HH.MM.SS.db
docker compose start navidrome
```

- `backup create`는 오래된 백업을 지우지 않는다. `prune`을 따로 실행한다.
- `restore`는 백업 이후의 사용자·재생 횟수·재생목록 변경을 모두 버린다.
- 되돌릴 수 없는 명령: `backup restore`, `backup prune --keep-count 0`, `missing fix`, `user delete`. 실행 전 `backup create`.
- PID 설정을 바꾸면 전체 스캔이 필요하고 ID가 재할당된다. 재생목록·별점·재생 횟수는 보존되지만 먼저 백업한다.

## 재생목록·멀티라이브러리·아트워크

- `.m3u` 자동 가져오기: 파일이 곡 목록을 소유하므로 UI에서 편집할 수 없다. 편집하려면 해당 목록의 auto-import를 끈다. `AutoImportPlaylists=false`는 이미 가져온 목록을 편집 가능하게 만들지 않는다.
- 멀티라이브러리: `MusicFolder`가 기본 라이브러리. 사용자별 접근은 `user create/edit --library-ids`. 관리자는 항상 전체 접근.
- 아트워크 우선순위: 앨범 `CoverArtPriority` = `cover.*, folder.*, front.*, embedded, external`. 아티스트 `ArtistArtPriority` = `artist.*, album/artist.*, external`. 원인 추적은 `navidrome artwork`.
- 로그는 stdout 전용. Docker `docker logs`, systemd `journalctl -u navidrome.service`.

## 태그 수정 절차

재생 기록을 잃지 않으려면 이 순서를 지킨다.

1. `navidrome backup create`로 DB를 백업한다.
2. 태그만 수정하고 저장한다. 파일 이동·이름 변경은 하지 않는다.
3. `navidrome scan`을 실행한다. 전체 재읽기가 필요하면 `--full`.
4. `navidrome inspect` 또는 UI Raw Tags로 의도대로 읽혔는지 확인한다.
5. 파일을 옮기거나 이름을 바꾼다.
6. 다시 `navidrome scan`을 실행한다.

이동과 재태깅을 한 스캔에 넣으면 매칭이 실패한다. 실패한 항목은 `missing list`에 남고 `missing fix`로 수동 재연결한다.

## 증상 → 원인과 조치

| 증상 | 원인과 조치 |
| --- | --- |
| 컴필레이션이 트랙 아티스트별 앨범으로 쪼개짐 | `Album Artist`가 제각각. `Various Artists`로 통일 + `TCMP`/`COMPILATION=1` |
| 같은 앨범이 두 개로 보임 | `Album`·`Album Artist`·`Release Date`·`Album Version` 중 하나가 다름. 두 트랙을 `navidrome inspect`로 비교 |
| 다중 디스크가 두 앨범으로 보임 | 디스크별로 `Album` 제목을 바꿨거나 `Album Artist`가 다름. 제목은 같게, `DISCNUMBER`만 다르게 |
| 같은 이름 앨범(일반판·Deluxe)이 하나로 합쳐짐 | `Album Version` 또는 MusicBrainz 앨범 ID가 없음. `albumversion`을 다르게 준다 |
| 다중 아티스트 중 첫 이름만 보임 | 단일 `ARTIST`에 구분자 없는 값. `ARTISTS` 다중값 사용. M4A는 중복 atom 문제 확인 |
| 재생목록·별점이 갑자기 끊김 | 태그와 파일 이동을 한 스캔에 처리. `missing list` → `missing fix` |
| DB 오류·손상 | `navidrome doctor`. 서버 중지 후 `backup restore` |
| 아트워크가 없음 | `CoverArtPriority` 순서와 파일명 확인. `navidrome artwork` |
| 스캔이 끝나지 않음 | `Scanner.WatcherWait=0`으로 watcher를 끄고 원인 분리. `LogLevel=debug` |
| 웹 UI는 뜨는데 라이브러리가 빔 | `/music` 읽기 권한. `chmod -R a+rX /path/to/music` |
| DB 파일을 열 수 없음 | `/data` 쓰기 권한. 소유주를 실행 UID:GID로 변경 |
| 브라우저 접속 불가 | 포트 `4533` 매핑·방화벽 |

## 흔한 실수

- CLI 플래그는 소문자다(`--musicfolder`, `--full`). 전체 목록은 `navidrome --help`.
- 서버가 실행 중인데 `backup restore`를 실행하면 데이터가 깨진다. 반드시 중지 후 실행.
- `/data`를 백업 없이 지우거나 컨테이너를 새 볼륨으로 재생성하면 사용자·재생 기록이 사라진다.
- 음악 폴더를 쓰기 가능으로 열어두고 Navidrome이 정리해 주길 기대하지 않는다. 태그·파일 관리는 외부 도구 몫이다.

## 참조 파일

| 범위 | 파일 |
| --- | --- |
| 태그→필드 매핑, 포맷별 태그명, 다중 아티스트, PID, 태거 워크플로 | `reference/tagging.md` |
| CLI 명령 전체, scan/missing/inspect/backup/user, Docker 실행 | `reference/cli.md` |
| 전체 옵션·환경변수·기본값, 기간/크기 형식 | `reference/configuration.md` |
| 기능, 외부 연동, Subsonic API, 외부 인증, FAQ | `reference/features-api.md` |

출처: https://www.navidrome.org/docs/ (문서 기준 2026-11). 버전별 플래그·기본값은 `navidrome --help`와 설정 파일에서 확인한다.
