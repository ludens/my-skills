# Navidrome CLI

공식 문서: https://www.navidrome.org/docs/usage/admin/cli/

## 기본

명령 없이 `navidrome`을 실행하면 서버가 시작된다.

```bash
navidrome --help                 # 명령 목록
navidrome <command> --help       # 명령 도움말
navidrome <command> <subcommand> --help
```

전역 플래그(모든 명령이 사용):

| 플래그 | 설명 |
| --- | --- |
| `-c, --configfile` | 설정 파일. 기본 `./navidrome.toml` |
| `-n, --nobanner` | 시작 배너 숨김 |
| `--musicfolder` | 음악 폴더 |
| `--datafolder` | 데이터 폴더(쓰기 필요) |
| `--cachefolder` | 캐시 폴더(쓰기 필요) |
| `-l, --loglevel` | `error`, `info`, `debug`, `trace` |
| `--logfile` | 로그 파일. 없으면 stderr |

명령은 서버와 같은 설정 파일과 `ND_` 환경변수를 읽는다. 다른 설정이면 다른 DB를 본다.

```bash
navidrome -c /etc/navidrome/navidrome.toml --nobanner user list
```

## 명령 목록

| 명령 | 역할 |
| --- | --- |
| `artwork` | 아트워크 확인 및 다시 해석 |
| `backup` | DB 백업 생성·정리·복원 |
| `doctor` | DB 문제 검사 |
| `inspect` | 음악 파일 태그를 Navidrome이 읽는 대로 출력 |
| `missing` | 누락 파일 목록 및 기존 파일로 재매핑 |
| `plugin` | 플러그인 목록·설정·활성화·비활성화 |
| `pls` | 재생목록 목록·내보내기·가져오기 |
| `scan` | 음악 라이브러리 스캔 |
| `search` | 전체 텍스트 검색 색인 재구축 |
| `service` | OS 서비스로 설치·제어 |
| `user` | 사용자 생성·수정·목록·삭제 |

## user

첫 관리자는 웹 UI에서 만든다. 이 명령은 DB에 관리자가 있어야 동작한다.

```bash
navidrome user create --username alice --email alice@example.com --admin
navidrome user create --username bob --name "Bob Smith" --library-ids 1,3
navidrome user edit --user alice --set-password     # 새 비밀번호를 묻는다
navidrome user edit --user alice --set-regular
navidrome user edit --user bob --library-ids 1,2
navidrome user list --format json
navidrome user delete --user alice
```

세부:

- 하위 명령: `create`(`c`), `edit`(`e`), `list`, `delete`(`d`).
- `create`는 비밀번호를 두 번 묻는다. 플래그로 비밀번호를 넘길 수 없다. 터미널에서 실행한다.
- `edit`의 `--set-admin`/`--set-regular`, `--email`/`--remove-email`, `--name`/`--remove-name`은 짝 중 하나만 쓴다.
- `--set-password`는 플래그 값이 아니라 새 비밀번호를 프롬프트로 받는다.
- `delete`는 확인을 묻지 않고 마지막 사용자는 삭제하지 않는다.
- 관리자는 `--library-ids`를 무시하고 항상 모든 라이브러리에 접근한다.

비밀번호를 잊은 관리자는 `user edit --user <username> --set-password`로 재설정한다.

## backup

백업 파일 이름 형식: `navidrome_backup_2026.04.01_04.00.00.db`. 저장 위치는 `Backup.Path`.

```bash
navidrome backup create
navidrome backup create --backup-dir /mnt/backups/navidrome
navidrome backup prune --keep-count 7
navidrome backup prune --keep-count 0 --force
navidrome backup restore --backup-file navidrome_backup_2026.04.01_04.00.00.db
```

- 하위 명령: `create`, `prune`, `restore`. 별칭 `bkp`도 된다.
- `create`는 오래된 백업을 지우지 않는다. `prune`을 따로 실행한다.
- `prune`은 `navidrome_backup_<date>_<time>.db` 형식만 본다. 전부 삭제 시 `YES` 확인 또는 `--force`.
- `restore`는 `YES` 확인 또는 `--force`. 상대 경로는 `Backup.Path` 기준.
- **`restore` 전에 Navidrome을 중지한다.** 백업 이후의 사용자·재생 횟수·재생목록 변경은 사라진다.

되돌릴 수 없는 명령: `backup restore`, `backup prune`(백업 삭제), `missing fix`. 실행 전 `backup create`를 먼저 한다.

## scan

라이브러리의 새 파일·변경 파일·삭제된 파일을 찾는다.

```bash
navidrome scan                          # 변경분 스캔
navidrome scan --full                   # 모든 폴더 검사, mtime 무시
navidrome scan -t 1:Music/Rock          # 라이브러리 1의 Music/Rock만
navidrome scan -t 1:Music/Rock -t 2:Audiobooks
navidrome scan --target-file ./targets.txt
```

- `-f, --full`: mtime을 무시하고 전부 다시 읽는다. 태그를 일괄 수정한 뒤 쓴다.
- `-t, --target`: `libraryID:folderPath`. 경로는 라이브러리 루트 기준. 반복 지정 가능.
- `--target-file`: 한 줄에 하나씩 target. `--target`과 함께 주면 파일만 쓴다.
- `--subprocess`는 서버 내부용이다. 직접 넘기지 않는다.
- 라이브러리 ID는 `user list`의 libraries 열에서 확인한다.

## missing

스캔이 찾지 못한 파일은 DB에 남아 missing으로 표시된다. 재생 횟수·별점·북마크를 새 파일로 옮기려면 `fix`를 쓴다.

```bash
navidrome missing list                      # CSV: id, library id, title, album, artist, path
navidrome missing list --format json
navidrome missing fix "Rock/Old/track01.mp3" "Rock/New/track01.mp3"
navidrome missing fix 3Unsdwsei9i2ZvRtFKRfwA 7KpqZmXe4Ab2NvTuGHRcxQ
navidrome missing fix 2:"Podcasts/ep01.mp3" 2:"Podcasts/episode-01.mp3"
```

- 첫 인자는 missing 파일, 두 번째는 데이터를 받을 파일.
- 인자는 media file ID, 라이브러리 상대 경로, `libraryID:path` 중 하나.
- 대상 파일은 이미 스캔되어 있어야 하고 missing이 아니어야 한다.
- `fix`는 되돌릴 수 없다. 대량 작업 전 `backup create`.
- DB에서 영구 삭제하는 방법은 `Scanner.PurgeMissing` 또는 관리자 UI의 Missing Files 메뉴다. 둘 다 재생 기록을 지운다.

## inspect

파일 태그를 Navidrome이 읽는 형태로 출력한다. 원본 태그와 매핑된 태그를 함께 보여준다.

```bash
navidrome inspect "Artist/Album/01 Track.flac"
navidrome inspect --format pretty "/music/Artist/Album/01 Track.flac"
navidrome inspect --format yaml /music/Artist/Album/*.mp3
docker compose run --rm navidrome inspect "/music/Artist/Album/01 Track.flac"
```

- `-f, --format`: `pretty`, `toml`, `yaml`, `json`, `jsonindent`(기본).
- 오디오가 아니거나 읽을 수 없는 파일은 경고를 남기고 건너뛴다.
- Docker에서는 컨테이너 안 경로를 넘긴다.

## 기타

```bash
navidrome search rebuild       # 검색 색인 재구축 (서버 중지 후)
navidrome doctor               # DB 문제 검사
```

플래그는 릴리스마다 바뀔 수 있으므로 설치 버전에서 `--help`로 확인한다.

## Docker에서 CLI 실행

컨테이너 밖에서 실행하면 다른 `/data`를 보거나 DB가 없을 수 있다. 반드시 같은 이미지·볼륨·환경변수를 사용한다.

```bash
# Docker Compose: 일회성 컨테이너
docker compose run --rm navidrome --help
docker compose run --rm navidrome scan --full
docker compose run --rm navidrome user list

# 이미 실행 중인 컨테이너: navidrome 바이너리 이름을 앞에 붙임
docker compose exec navidrome navidrome user list
```

비밀번호를 묻는 명령은 `-it`가 필요하다.

```bash
docker run --rm -it \
  --user $(id -u):$(id -g) \
  -v /path/to/music:/music:ro \
  -v /path/to/data:/data \
  --env-file /path/to/navidrome.env \
  -e ND_CONFIGFILE=/data/navidrome.toml \
  navidrome/navidrome:latest \
  user create --username alice --admin
```

Compose에서 DB 복원 예:

```bash
docker compose stop navidrome
docker compose run --rm navidrome backup restore --backup-file navidrome_backup_2026.04.01_04.00.00.db
docker compose start navidrome
```

스크립트에서는 `--configfile`을 명시해 어떤 설정을 읽는지 고정한다.
