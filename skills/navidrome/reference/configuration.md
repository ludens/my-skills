# Navidrome 설정

공식 문서: https://www.navidrome.org/docs/usage/configuration/options/

## 설정 방법과 우선순위

같은 옵션을 여러 방법으로 지정하면 **환경변수 > CLI 인자 > 설정 파일** 순으로 적용된다.

### 설정 파일

- 기본 위치: 작업 디렉터리의 `navidrome.toml`. `toml`, `json`, `yml`, `ini` 지원.
- 다른 경로: `navidrome --configfile /path/navidrome.toml` 또는 `-c`.
- Docker: `/data/navidrome.toml`을 자동으로 찾는다. 명시하려면 `ND_CONFIGFILE=/data/navidrome.toml`.
- Windows 경로는 작은따옴표 사용: `MusicFolder = 'C:\Users\JohnDoe\Music'`.

예:

```toml
LogLevel = 'DEBUG'
Scanner.Schedule = '@every 24h'
TranscodingCacheSize = '150MiB'
MusicFolder = '/mnt/music'
```

### CLI 인자

대부분의 옵션을 넘길 수 있다. **전부 소문자**로 쓴다. 목록은 `navidrome --help`.

```bash
navidrome --musicfolder "/mnt/music"
```

### 환경변수

옵션 이름을 대문자로 바꾸고 접두사 `ND_`를 붙인다. 점(`.`)은 밑줄로 바뀐다. 예: `Backup.Path` → `ND_BACKUP_PATH`.

- 기간: 숫자 + 단위(`s`, `m`, `h`). 예: `24h`, `30s`, `1h10m`.
- 크기: 숫자 + 선택적 단위. 기본 단위는 바이트. `1KB = 1000`, `1KiB = 1024`. 예: `150MiB`, `1GB`.

## 기본 설정

| 설정 파일 | 환경변수 | 설명 | 기본값 |
| --- | --- | --- | --- |
| — | `ND_CONFIGFILE` | 외부 설정 파일 경로 | `./navidrome.toml` |
| `MusicFolder` | `ND_MUSICFOLDER` | 음악 라이브러리 폴더(읽기 전용 가능). 멀티라이브러리에서 기본 라이브러리 | `./music` |
| `DataFolder` | `ND_DATAFOLDER` | DB 등 애플리케이션 데이터(쓰기 필요) | `./data` |
| `CacheFolder` | `ND_CACHEFOLDER` | 트랜스코딩·이미지 캐시 | `<DataFolder>/cache` |
| `LogLevel` | `ND_LOGLEVEL` | `error`, `warn`, `info`, `debug`, `trace` | `info` |
| `LogFile` | `ND_LOGFILE` | 지정하면 stderr 대신 파일에 기록 | 비어 있음(stderr) |
| `Address` | `ND_ADDRESS` | 바인드 주소. IPv4/IPv6/유닉스 소켓(`unix:/path`) | `0.0.0.0`, `::` |
| `BaseUrl` | `ND_BASEURL` | 프록시 뒤 경로/URL. 예: `/music` | 비어 있음 |
| `Port` | `ND_PORT` | HTTP 포트 | `4533` |
| `EnableInsightsCollector` | `ND_ENABLEINSIGHTSCOLLECTOR` | 익명 데이터 수집 | `true` |

## 스캐너와 라이브러리

| 설정 파일 | 환경변수 | 설명 | 기본값 |
| --- | --- | --- | --- |
| `Scanner.Enabled` | `ND_SCANNER_ENABLED` | 자동 스캔 활성화 | `true` |
| `Scanner.Schedule` | `ND_SCANNER_SCHEDULE` | cron 구문 예약. `0`이면 비활성 | `0` |
| `Scanner.WatcherWait` | `ND_SCANNER_WATCHERWAIT` | 파일 변경 감지 후 대기. `0`이면 watcher 비활성 | `5s` |
| `Scanner.ScanOnStartup` | `ND_SCANNER_SCANONSTARTUP` | 시작 시 스캔 | `true` |
| `Scanner.PurgeMissing` | `ND_SCANNER_PURGEMISSING` | `never`(표시만), `always`, `full`(전체 스캔 후) | `never` |
| `Scanner.FollowSymlinks` | `ND_SCANNER_FOLLOWSYMLINKS` | 심볼릭 링크 따라가기 | `true` |
| `Scanner.IgnoreDotFolders` | `ND_SCANNER_IGNOREDOTFOLDERS` | 점으로 시작하는 폴더 무시 | `true` |
| `Scanner.ArtistJoiner` | `ND_SCANNER_ARTISTJOINER` | 다중 아티스트 표시명 연결 문자열 | ` • ` |
| `Scanner.ArtistSplitExceptions` | `ND_SCANNER_ARTISTSPLITEXCEPTIONS` | 아티스트 구분자로 쪼개지 않을 이름 목록(예: `AC/DC`) | 비어 있음 |
| `AutoImportPlaylists` | `ND_AUTOIMPORTPLAYLISTS` | `.m3u` 자동 가져오기 | `true` |
| `PlaylistsPath` | `ND_PLAYLISTSPATH` | 재생목록 검색 경로. `MusicFolder` 기준 상대 경로만 | 비어 있음(전체) |
| `PID.Album` | `ND_PID_ALBUM` | 앨범 ID에 쓸 태그 | `musicbrainz_albumid\|albumartistid,album,albumversion,releasedate` |
| `PID.Track` | `ND_PID_TRACK` | 트랙 ID에 쓸 태그 | `musicbrainz_trackid\|albumid,discnumber,tracknumber,title` |
| `IgnoredArticles` | `ND_IGNOREDARTICLES` | 정렬 시 무시할 관사 | `The El La Los Las Le Les Os As O A` |
| `RecentlyAddedByModTime` | `ND_RECENTLYADDEDBYMODTIME` | Recently Added 정렬에 수정 시간 사용 | `false` |
| `Search.Backend` | `ND_SEARCH_BACKEND` | `fts`(FTS5+BM25) 또는 `legacy` | `fts` |
| `Search.FullString` | `ND_SEARCH_FULLSTRING` | 단어 경계가 아닌 임의 위치 검색 | `false` |

`Tags`와 `Jukebox.Devices`는 환경변수로 설정할 수 없다.

## 인증과 보안

| 설정 파일 | 환경변수 | 설명 | 기본값 |
| --- | --- | --- | --- |
| `ExtAuth.TrustedSources` | `ND_EXTAUTH_TRUSTEDSOURCES` | 프록시 인증 신뢰 CIDR 목록. 유닉스 소켓은 `@`. 빈 값은 전부 거부 | 비어 있음 |
| `ExtAuth.UserHeader` | `ND_EXTAUTH_USERHEADER` | 인증된 사용자 이름을 담는 헤더 | `Remote-User` |
| `ExtAuth.LogoutURL` | `ND_EXTAUTH_LOGOUTURL` | 로그아웃 후 리다이렉트할 URL | 비어 있음 |
| `EnableUserEditing` | `ND_ENABLEUSEREDITING` | 일반 사용자의 정보·비밀번호 변경 허용 | `true` |
| `AuthRequestLimit` | `ND_AUTHREQUESTLIMIT` | `AuthWindowLength` 동안 IP당 로그인 횟수. `0`이면 비활성 | `5` |
| `AuthWindowLength` | `ND_AUTHWINDOWLENGTH` | 로그인 제한 시간 창 | `20s` |
| `SessionTimeout` | `ND_SESSIONTIMEOUT` | 유휴 웹 세션 만료 | `48h` |
| `PasswordEncryptionKey` | `ND_PASSWORDENCRYPTIONKEY` | DB 비밀번호 암호화에 쓸 구문 | — |
| `EnableLogRedacting` | `ND_ENABLELOGREDACTING` | 로그에서 토큰·비밀번호 숨기기 | `true` |
| `TLSCert` / `TLSKey` | `ND_TLSCERT` / `ND_TLSKEY` | TLS 인증서/키 경로. 비어 있으면 TLS 비활성 | 비어 있음 |
| `HTTPHeaders.FrameOptions` | `ND_HTTPHEADERS_FRAMEOPTIONS` | `X-Frame-Options` 값 | `DENY` |
| `UnixSocketPerm` | `ND_UNIXSOCKETPERM` | 유닉스 소켓 권한 | `0660` |
| `EnforceNonRootUser` | `ND_ENFORCENONROOTUSER` | root 실행 시 종료(Unix만) | `false` |
| `EnableTranscodingConfig` | `ND_ENABLETRANSCODINGCONFIG` | UI에서 트랜스코딩 설정 허용 | `false` |

## 기능과 연동

| 설정 파일 | 환경변수 | 설명 | 기본값 |
| --- | --- | --- | --- |
| `Jellyfin.Enabled` | `ND_JELLYFIN_ENABLED` | 실험적 Jellyfin API 활성화 | `false` |
| `Jellyfin.ServerName` | `ND_JELLYFIN_SERVERNAME` | 클라이언트에 표시할 서버 이름 | `Navidrome <version>` |
| `Jellyfin.AutoDiscovery` | `ND_JELLYFIN_AUTODISCOVERY` | UDP 7359로 로컬 검색 응답(Docker는 host networking 필요) | `false` |
| `Jellyfin.QuickConnect` | `ND_JELLYFIN_QUICKCONNECT` | 6자리 코드 로그인 | `true` |
| `Jellyfin.ExposedPublicUsers` | `ND_JELLYFIN_EXPOSEDPUBLICUSERS` | 로그인 화면에 노출할 사용자 | 비어 있음 |
| `Jukebox.Enabled` | `ND_JUKEBOX_ENABLED` | 서버 hardware 재생 | `false` |
| `Jukebox.AdminOnly` | `ND_JUKEBOX_ADMINONLY` | 관리자만 주크박스 제어 | `true` |
| `Jukebox.Default` | `ND_JUKEBOX_DEFAULT` | 기본 장치 | 비어 있음(자동) |
| `MPVPath` | `ND_MPVPATH` | `mpv` 실행 파일 경로 | 비어 있음(PATH 검색) |
| `EnableSharing` | `ND_ENABLESHARING` | 공유 링크 기능 | `true` |
| `DefaultShareExpiration` | `ND_DEFAULTSHAREEXPIRATION` | 새 공유 만료 기간 | `8760h` |
| `DefaultDownloadableShare` | `ND_DEFAULTDOWNLOADABLESHARE` | 새 공유의 다운로드 허용 | `false` |
| `ShareURL` | `ND_SHAREURL` | 공유 링크 기준 URL | 비어 있음 |
| `EnableScrobbleHistory` | `ND_ENABLESCROBBLEHISTORY` | 스크로블 기록 | `true` |
| `LastFM.Enabled` | `ND_LASTFM_ENABLED` | Last.fm 연동 | `true` |
| `LastFM.ApiKey` | `ND_LASTFM_APIKEY` | Last.fm API 키 | 비어 있음 |
| `LastFM.Secret` | `ND_LASTFM_SECRET` | Last.fm API 시크릿 | 비어 있음 |
| `LastFM.ScrobbleFirstArtistOnly` | `ND_LASTFM_SCROBBLEFIRSTARTISTONLY` | 여러 아티스트 시 첫 아티스트만 스크로블 | `false` |
| `ListenBrainz.Enabled` | `ND_LISTENBRAINZ_ENABLED` | ListenBrainz 연동 | `true` |
| `ListenBrainz.BaseURL` | `ND_LISTENBRAINZ_BASEURL` | ListenBrainz API 주소 | `https://api.listenbrainz.org/1/` |
| `Agents` | `ND_AGENTS` | 메타데이터 에이전트 우선순위 | `deezer,lastfm,listenbrainz` |
| `EnableExternalServices` | `ND_ENABLEEXTERNALSERVICES` | 모든 외부 연동 비활성화 | `true` |
| `Plugins.Enabled` | `ND_PLUGINS_ENABLED` | 플러그인 시스템 | `true` |
| `Plugins.Folder` | `ND_PLUGINS_FOLDER` | `.ndp` 파일 폴더 | `<DataFolder>/plugins` |
| `Plugins.AutoReload` | `ND_PLUGINS_AUTORELOAD` | `.ndp` 변경 시 즉시 재로드 | `false` |
| `Plugins.CacheSize` | `ND_PLUGINS_CACHESIZE` | 플러그인 컴파일 캐시 | `200MB` |
| `SmartPlaylistRefreshDelay` | `ND_SMARTPLAYLISTREFRESHDELAY` | 스마트 플레이리스트 갱신 주기 | `5s` |
| `Backup.Path` | `ND_BACKUP_PATH` | 백업 폴더. `""`이면 비활성 | `""` |
| `Backup.Schedule` | `ND_BACKUP_SCHEDULE` | 자동 백업 cron | `""` |
| `Backup.Count` | `ND_BACKUP_COUNT` | 유지할 백업 수 | `0` |
| `Prometheus.Enabled` | `ND_PROMETHEUS_ENABLED` | Prometheus 엔드포인트 | `false` |
| `Prometheus.MetricsPath` | `ND_PROMETHEUS_METRICSPATH` | 메트릭 경로 | `/metrics` |
| `Prometheus.Password` | `ND_PROMETHEUS_PASSWORD` | Basic Auth 비밀번호(사용자 `navidrome`) | 비어 있음 |

## 아트워크·트랜스코딩·UI

| 설정 파일 | 환경변수 | 설명 | 기본값 |
| --- | --- | --- | --- |
| `CoverArtPriority` | `ND_COVERARTPRIORITY` | 커버 아트 탐색 순서. `embedded`는 파일 내장 이미지 | `cover.*, folder.*, front.*, embedded, external` |
| `ArtistArtPriority` | `ND_ARTISTARTPRIORITY` | 아티스트 이미지 탐색 순서 | `artist.*, album/artist.*, external` |
| `ArtistImageFolder` | `ND_ARTISTIMAGEFOLDER` | 아티스트 이미지 중앙 폴더. `ArtistArtPriority`에 `image-folder`가 있어야 쓴다 | 비어 있음 |
| `DiscArtPriority` | `ND_DISCARTPRIORITY` | 다중 디스크 앨범의 디스크별 아트워크 탐색 순서. 빈 값이면 앨범 아트로 통일 | `disc*.*, cd*.*, cover.*, folder.*, front.*, discsubtitle, embedded` |
| `LyricsPriority` | `ND_LYRICSPRIORITY` | 가사 소스 순서 | `.ttml,.yaml,.yml,.elrc,.lrc,.srt,.txt,embedded` |
| `EnableArtworkUpload` | `ND_ENABLEARTWORKUPLOAD` | UI에서 아트워크 업로드(JPEG/PNG/WebP/GIF, 최대 10MB) | `true` |
| `MaxImageUploadSize` | `ND_MAXIMAGEUPLOADSIZE` | 업로드 최대 크기 | `10MB` |
| `MaxImageSize` | `ND_MAXIMAGESIZE` | 읽을 이미지 최대 크기 | `20MB` |
| `TranscodingCacheSize` | `ND_TRANSCODINGCACHESIZE` | 트랜스코딩 캐시. `0`이면 비활성 | `100MB` |
| `Transcoding.MaxConcurrent` | `ND_TRANSCODING_MAXCONCURRENT` | 서버 전체 동시 트랜스코드. `0`이면 무제한 | `0` |
| `Transcoding.MaxConcurrentPerUser` | `ND_TRANSCODING_MAXCONCURRENTPERUSER` | 사용자별 동시 트랜스코드 | `0` |
| `DefaultDownsamplingFormat` | `ND_DEFAULTDOWNSAMPLINGFORMAT` | 다운샘플링 기본 포맷 | `opus` |
| `FFmpegPath` | `ND_FFMPEGPATH` | `ffmpeg` 경로 | 비어 있음(PATH 검색) |
| `EnableWebPEncoding` | `ND_ENABLEWEBPENCODING` | 리사이즈 이미지를 WebP로 | `false` |
| `UICoverArtSize` | `ND_UICOVERARTSIZE` | UI 커버 픽셀(200~1200으로 제한) | `300` |
| `DefaultTheme` | `ND_DEFAULTTHEME` | 새 브라우저 기본 테마 | `Dark` |
| `DefaultLanguage` | `ND_DEFAULTLANGUAGE` | 기본 UI 언어. i18n 파일명과 일치(예: `zh-Hans`) | `en` |
| `DefaultUIVolume` | `ND_DEFAULTUIVOLUME` | 기본 볼륨(0~100) | `100` |
| `UIWelcomeMessage` | `ND_UIWELCOMEMESSAGE` | 로그인 화면 메시지 | 비어 있음 |
| `EnableDownloads` | `ND_ENABLEDOWNLOADS` | UI 다운로드 메뉴 | `true` |
| `EnableFavourites` | `ND_ENABLEFAVOURITES` | 즐겨찾기(Subsonic Star) | `true` |
| `EnableStarRating` | `ND_ENABLESTARRATING` | 5점 별점 | `true` |
| `EnableNowPlaying` | `ND_ENABLENOWPLAYING` | Now Playing 기능 | `true` |
| `EnableReplayGain` | `ND_ENABLEREPLAYGAIN` | ReplayGain 옵션 | `true` |
| `UIPlaybackReportInterval` | `ND_UIPLAYBACKREPORTINTERVAL` | 재생 위치 보고 주기 | `1m` |

전체 옵션과 최신 기본값은 공식 문서와 `navidrome --help`에서 확인한다.
