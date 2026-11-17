# 태깅 레퍼런스

공식 문서: https://www.navidrome.org/docs/usage/library/tagging/ , https://www.navidrome.org/docs/usage/configuration/persistent-ids/ , https://github.com/navidrome/navidrome/blob/master/resources/mappings.yaml

## 원칙

- Navidrome은 음악 파일을 **읽기만** 한다. 태그 편집·파일 이동은 외부 도구(Picard, beets, Mp3tag)가 한다.
- 폴더·파일명은 라이브러리 구조에 쓰이지 않는다. 같은 태그면 어느 폴더에 있어도 같은 앨범이다.
- 태그를 바꾼 뒤에는 스캔이 필요하다. 전체 재읽기는 `navidrome scan --full`.

## 필드 → 태그

자주 쓰는 필드만 정리했다. 전체 목록은 Navidrome의 `resources/mappings.yaml` 참고.

| Navidrome 필드 | ID3 (MP3) | Vorbis (FLAC/Ogg/Opus) | MP4 (M4A/AAC) | 비고 |
| --- | --- | --- | --- | --- |
| title | `TIT2` | `TITLE` | `©nam` | |
| artist | `TPE1` | `ARTIST` | `©ART` | 표시명 |
| artists | `TXXX:Artists` | `ARTISTS` | `----:com.apple.itunes:artists` | 다중값. 권장 |
| albumartist | `TPE2` | `ALBUMARTIST` | `aART` | 앨범 그룹핑 핵심 |
| albumartists | `TXXX:Album Artists` | `ALBUMARTISTS` | — | 다중값 |
| album | `TALB` | `ALBUM` | `©alb` | |
| albumversion | `ALBUMVERSION` | `ALBUMVERSION` | — | 같은 이름 앨범 구분 |
| track | `TRCK` | `TRACKNUMBER` | `trkn` | `5` 또는 `5/12` |
| tracktotal | `TRACKTOTAL` | `TRACKTOTAL` | `trkn` | 앨범 단위 값 |
| disc | `TPOS` | `DISCNUMBER` | `disk` | `1/2` |
| disctotal | `DISCTOTAL` | `DISCTOTAL` | `disk` | 앨범 단위 값 |
| compilation | `TCMP` | `COMPILATION` | `cpil` | `1`이면 컴필레이션 |
| genre | `TCON` | `GENRE` | `©gen` | 다중값, `;` `/` `,`로 분리 |
| mood | `TMOO` | `MOOD` | `----:com.apple.itunes:mood` | 다중값 |
| releasedate | `TDRL` | `RELEASEDATE`, `YEAR` | `©day` | 발매일 |
| recordingdate | `TDRC` | `DATE` | — | 녹음일 |
| originaldate | `TDOR` | `ORIGINALDATE`, `ORIGINALYEAR` | `----:com.apple.itunes:originaldate` | 원발매일 |
| composer | `TCOM` | `COMPOSER` | `©wrt` | 역할 태그 |
| lyricist | `TEXT` | `LYRICIST` | `----:com.apple.itunes:lyricist` | 역할 태그 |
| conductor | `TPE3` | `CONDUCTOR` | `----:com.apple.itunes:conductor` | 역할 태그 |
| musicbrainz_recordingid | `UFID:http://musicbrainz.org` | `MUSICBRAINZ_TRACKID` | `----:com.apple.itunes:musicbrainz track id` | Picard의 MusicBrainz Track Id |
| musicbrainz_trackid | `TXXX:MusicBrainz Release Track Id` | `MUSICBRAINZ_RELEASETRACKID` | `----:com.apple.itunes:musicbrainz release track id` | `PID.Track` 우선순위 1 |
| musicbrainz_albumid | `TXXX:MusicBrainz Album Id` | `MUSICBRAINZ_ALBUMID` | `----:com.apple.itunes:musicbrainz album id` | |
| musicbrainz_artistid | `TXXX:MusicBrainz Artist Id` | `MUSICBRAINZ_ARTISTID` | `----:com.apple.itunes:musicbrainz artist id` | |
| musicbrainz_albumartistid | `TXXX:MusicBrainz Album Artist Id` | `MUSICBRAINZ_ALBUMARTISTID` | `----:com.apple.itunes:musicbrainz album artist id` | |
| catalognumber | `TXXX:CATALOGNUMBER` | `CATALOGNUMBER` | `----:com.apple.itunes:catalognumber` | |
| releasetype | `TXXX:MusicBrainz Album Type` | `RELEASETYPE`, `MUSICBRAINZ_ALBUMTYPE` | — | `album`, `compilation` 등 |
| lyrics | `USLT` | `LYRICS` | `©lyr` | |
| comment | `COMM` | `COMMENT` | `©cmt` | |
| replaygain_* | `TXXX:REPLAYGAIN_*` | `REPLAYGAIN_*` | `----:com.apple.itunes:replaygain_*` | |

추가 태그(`barcode`, `isrc`, `media`, `recordlabel`, `releasecountry`, `releasestatus`, `script`, `subtitle`, `work`, `website` 등)는 스마트 플레이리스트 필드로도 쓰인다. 이름을 바꾸거나 별칭을 추가하려면 `Tags` 설정을 쓴다. `Tags`는 환경변수로 설정할 수 없다.

## 날짜 3종 구분

세 필드는 서로 다른 값이다. 섞으면 앨범 PID가 흔들린다.

| 태그 | 필드 | 의미 |
| --- | --- | --- |
| `DATE` | `recordingdate` | 트랙 녹음일 |
| `YEAR`, `RELEASEDATE` | `releasedate` | 앨범 발매일. 기본 앨범 PID에 포함 |
| `ORIGINALDATE`, `ORIGINALYEAR` | `originaldate` | 원발매일 |

형식은 `YYYY`, `YYYY-MM`, `YYYY-MM-DD` 모두 된다. `YEAR`는 발매일 별칭이고 녹음일이 아니다.

## 다중 아티스트

단일값 `ARTIST`/`ALBUMARTIST`와 다중값 `ARTISTS`/`ALBUMARTISTS`가 있다.

우선순위와 표시:

1. `ARTISTS` 다중값이 있으면 각 아티스트를 개별 엔티티로 인식한다.
2. `ARTIST`도 함께 있으면 `ARTIST`는 **표시명으로만** 쓰고 쪼개지 않는다.
3. `ARTISTS`만 있으면 표시명을 값들을 `Scanner.ArtistJoiner`(기본 ` • `)로 이어 만든다.
4. 단일값 `ARTIST`만 있으면 기본 구분자로 쪼갠다.

단일값 아티스트 구분자 (기본):

```text
" / "  " feat. "  " feat "  " ft. "  " ft "  "; "
```

- 대소문자 무시. `" / "`는 공백 포함이라 `AC/DC`를 쪼개지 않는다.
- `"; "`는 뒤 공백만 필요하므로 `Foo; Bar`는 쪼개진다.
- 쪼개면 안 되는 이름은 `Scanner.ArtistSplitExceptions = "AC/DC,!!!,..."`로 보호한다.

역할 태그(`COMPOSER`, `LYRICIST`, `ARRANGER`, `ENGINEER`, `PRODUCER`, `PERFORMER` 등)는 다중값 별칭이 없고 구분자가 `"/"`, `";"`(공백 불필요)다. 그래서 `AC/DC` 같은 값은 역할 태그에서 쪼개진다. 다중값으로 넣으면 쪼개지 않는다.

포맷별 다중값 지원:

- Vorbis(FLAC/Ogg/Opus): 완전 지원. 같은 필드를 여러 줄 쓴다.
- ID3v2.4: 지원.
- ID3v2.3: 공식 지원 없음. `"; "` 같은 구분자로 합치는 차선책. 가능하면 v2.4로 저장한다.
- MP4/M4A: 지원하지만 편집기가 중복 atom을 만들면 첫 값만 읽힌다. Picard로 재저장하거나 Mp3tag의 *Use single MP4 atom for multiple values*를 켠다.

예 (FLAC):

```text
TITLE=Sunshine
ARTIST=Alice feat. Bob
ARTISTS=Alice
ARTISTS=Bob
ALBUM=Brighter Days
ALBUMARTIST=Alice
TRACKNUMBER=7
```

## 앨범 그룹핑

앨범 정체성은 `PID.Album` 입력 태그로 정해진다. 기본값은 MusicBrainz 앨범 ID가 있으면 그것, 없으면 `albumartistid, album, albumversion, releasedate` 조합이다.

따라서 다음 값은 앨범의 모든 트랙에서 같아야 한다.

- `ALBUM`
- `ALBUMARTIST` (`ALBUMARTISTS` 포함)
- `RELEASEDATE`/`YEAR`
- `ALBUMVERSION` (있는 경우)

체크리스트:

- Various Artists: `ALBUMARTIST=Various Artists` + `COMPILATION=1`/`TCMP=1`. 트랙별 `ARTIST`는 그대로 둔다.
- 다중 디스크: `ALBUM`은 동일, `DISCNUMBER=1/2`·`2/2`만 다르게. 앨범 제목에 `(Disc 2)`를 붙이지 않는다.
- 같은 이름 앨범(일반판·Deluxe·리마스터): `ALBUMVERSION` 또는 `MUSICBRAINZ_ALBUMID`로 구분한다. 구분 값이 없으면 하나로 합쳐진다.
- 발매일이 트랙마다 다르면 앨범이 쪼개진다. 컴필레이션에서 트랙별 발매일을 넣었다면 앨범 발매일과 분리한다.
- 아티스트 표기(공백, 대소문자, `The`)를 통일한다. `The Beatles`와 `The Beatles `는 다른 아티스트다.

## Persistent IDs (PID)

ID는 저장된 상수가 아니라 태그에서 계산된다. PID는 그 계산 규칙이다.

기본값:

```toml
PID.Track = "musicbrainz_trackid|albumid,discnumber,tracknumber,title"
PID.Album = "musicbrainz_albumid|albumartistid,album,albumversion,releasedate"
```

문법:

- `|` 앞은 선호 값. 있으면 그것만 쓴다.
- `|` 뒤는 대체 조합. 쉼표로 이어 붙인다.
- `albumid`는 `PID.Album` 결과를 가리킨다.

예:

```toml
PID.Album = "folder"                       # 폴더 기준으로 묶기
PID.Album = "discogs_release_id|albumartistid,album,albumversion,releasedate"
PID.Album = "album_legacy"                 # 0.55.0 이전 방식
PID.Track = "track_legacy"
```

동작:

- PID 설정을 바꾸면 전체 스캔이 필요하고 ID가 재할당된다. 재생목록·별점·재생 횟수·공유는 보존된다. 그래도 먼저 `navidrome backup create`.
- 파일 이동 시 매칭 순서: 정확히 같은 태그 → 같은 PID → 확장자를 뺀 원래 경로.
- 재태깅과 이동을 한 스캔에 넣으면 매칭되지 않는다. 재태깅 → 스캔 → 이동 → 스캔.
- 아티스트 ID는 이름 기반이라 설정할 수 없다. 이름을 바꾸면 별도 아티스트가 된다.

## 읽힌 태그 확인

```bash
navidrome inspect "Artist/Album/01 Track.flac"
navidrome inspect --format pretty "Artist/Album/01 Track.flac"
navidrome inspect --format yaml /music/Artist/Album/*.mp3
docker compose run --rm navidrome inspect "/music/Artist/Album/01 Track.flac"
```

출력은 파일의 원본 태그와 Navidrome이 매핑한 태그를 함께 보여준다. `--format`은 `pretty`, `toml`, `yaml`, `json`, `jsonindent`(기본).

Docker에서는 컨테이너 안 경로(`/music/...`)를 넘긴다.

## 자주 나는 태깅 실패

| 증상 | 확인할 태그 | 조치 |
| --- | --- | --- |
| 컴필레이션이 곡마다 다른 앨범 | `ALBUMARTIST`, `COMPILATION` | `Various Artists` + `1` |
| 같은 앨범이 둘로 갈라짐 | 두 트랙의 `inspect` 출력 비교 | `ALBUM`, `ALBUMARTIST`, `RELEASEDATE`, `ALBUMVERSION` 통일 |
| 다중 디스크가 둘로 갈라짐 | `ALBUM`, `DISCNUMBER` | 제목 통일, 디스크 번호만 분리 |
| Deluxe판이 일반판과 합쳐짐 | `ALBUMVERSION` | 다르게 지정 |
| `feat.` 아티스트가 안 쪼개짐 | `ARTIST` 값 | `ARTISTS` 다중값 사용 |
| `AC/DC`가 `AC`, `DC`로 쪼개짐 | 역할 태그 구분자 | `Scanner.ArtistSplitExceptions`, 또는 다중값 사용 |
| M4A에서 두 번째 아티스트 무시 | 중복 atom | Picard 재저장, Mp3tag 단일 atom 옵션 |
| 태그를 고쳤는데 UI가 그대로 | 스캔 여부, mtime | `navidrome scan --full` |
| 앨범 연도가 다르게 표시 | `DATE` vs `YEAR` | `DATE`는 녹음일, `YEAR`는 발매일 |
| 앨범 ID가 계속 바뀜 | PID 입력 태그 | 태그 고정, PID 변경 시 전체 스캔 |

## 태거 워크플로

1. 대량 수정 전에 음악 파일과 DB를 백업한다.
2. 앨범 단위로 작업한다. 같은 앨범 트랙의 `ALBUM`·`ALBUMARTIST`·발매일을 한 번에 맞춘다.
3. 자동 태깅(Picard, beets) 결과를 검토한다. 데이터베이스 표기와 원하는 표기가 다를 수 있다.
4. 태그만 저장하고 스캔한다. 파일 이동은 그다음 스캔에서 한다.
5. `navidrome inspect`로 의도한 필드가 나오는지 확인한다.

Picard에서 Navidrome에 유리한 태그를 채우는 스크립트:

```text
# Multiple artists
$setmulti(albumartists,%_albumartists%)
$setmulti(albumartistssort,%_albumartists_sort%)
$setmulti(artistssort,%_artists_sort%)

# Album version and subtitle
$set(musicbrainz_albumcomment,%_releasecomment%)
$if(%_recordingcomment%, $set(subtitle,%_recordingcomment%))

# Release and original dates
$set(releasedate,%date%)
$set(date,%_recording_firstreleasedate%)
$set(originaldate,%originaldate%)
$delete(originalyear)
```

Picard 설정에서 *Use standardized artist names*를 켜면 아티스트 이름 표기가 안정된다.

## 태깅으로 해결되지 않는 것

- 폴더 탐색: 설계상 미지원. 태그·멀티라이브러리·`PID.Album="folder"`로 대체한다.
- 태그·파일 자동 정리: Navidrome은 쓰지 않는다. 외부 도구를 쓴다.
- 특정 폴더 제외: 태그가 아니라 `.ndignore`.
- 음악 업로드: 내장 기능 없음. FileBrowser·SFTP·네트워크 공유, 또는 전용 라이브러리.
