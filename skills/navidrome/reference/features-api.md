# 기능·연동·API

공식 문서: https://www.navidrome.org/docs/usage/features/ , https://www.navidrome.org/docs/developers/subsonic-api/ , https://www.navidrome.org/docs/faq/

## 주요 기능

| 기능 | 요점 | 관련 설정 |
| --- | --- | --- |
| Smart Playlists (Beta) | 조건식으로 곡을 모으는 동적 재생목록 | `SmartPlaylistRefreshDelay` |
| Multi-Library | 별도 라이브러리와 사용자별 접근 제어. `MusicFolder`가 기본 라이브러리 | `user create/edit --library-ids` |
| Jukebox | 서버 hardware에서 재생(`mpv`). Snapcast 연동 가능 | `Jukebox.Enabled`(기본 `false`), `Jukebox.AdminOnly`, `MPVPath`, `MPVCmdTemplate` |
| Sharing | 인증 없는 공유 링크 | `EnableSharing`, `DefaultShareExpiration`, `ShareURL` |
| Scrobbling | Last.fm, ListenBrainz로 재생 기록 전송 | `LastFM.*`, `ListenBrainz.*` |
| Plugins | `.ndp` 플러그인. CLI `navidrome plugin` | `Plugins.Enabled`, `Plugins.Folder`, `Plugins.AutoReload` |
| Jellyfin API (실험적) | Finamp·Jellify 등 Jellyfin 음악 클라이언트 연결 | `ND_JELLYFIN_ENABLED=true`, `Jellyfin.AutoDiscovery` |
| 외부 메타데이터 | 아티스트 정보·이미지·비슷한 곡. 순서대로 시도 | `Agents` = `deezer,lastfm,listenbrainz` |

`EnableExternalServices=false`는 익명 데이터 수집을 포함한 모든 외부 연동을 끈다.

## 외부 인증 (리버스 프록시/SSO)

기본값은 비활성. Navidrome은 프록시 뒤에서 외부 인증 없이도 동작한다. 프록시가 인증을 맡길 때만 켠다. 잘못 설정하면 사용자 위조가 가능하다.

설정:

- `ExtAuth.TrustedSources` — 신뢰할 프록시 IP CIDR 목록. 유닉스 소켓은 `@`. 빈 값은 모두 거부(기본).
- `ExtAuth.UserHeader` — 사용자 이름 헤더. 기본 `Remote-User`.
- `ExtAuth.LogoutURL` — 로그아웃 후 SSO 로그아웃 엔드포인트로 리다이렉트.

동작:

- 신뢰 소스의 요청만 헤더를 사용한다. 그렇지 않으면 일반 인증으로 폴백한다.
- 프록시 인증에 성공했지만 DB에 없는 사용자는 임의 비밀번호로 생성된다. 첫 사용자는 항상 관리자.
- 공유 기능을 쓰면 `/share/*`를 프록시 인증에서 제외한다.
- Subsonic 엔드포인트(`/rest/*`)의 `u`, `p`, `t`, `s` 파라미터는 헤더가 있으면 무시된다.
- 웹 앱은 Subsonic 클라이언트 `NavidromeUI`로 요청한다. 이 요청은 세션 쿠키로 인증하거나 프록시에서 인증을 우회하도록 처리한다.
- `-e ND_ENABLEUSEREDITING=false`로 사용자의 Navidrome 비밀번호 변경 UI를 숨길 수 있다.

보안 필수 조건:

1. 신뢰 프록시가 클라이언트가 보낸 사용자 헤더를 제거한다.
2. 인증되지 않은 요청에는 헤더를 설정하지 않는다(특히 `/rest/*` 우회 시).

예시 구성은 공식 문서 참조: Caddy `forward_auth` + Authentik, Traefik `ForwardAuth` + Authelia.

## Subsonic API 호환성

Subsonic API **v1.16.1** 호환. OpenSubsonic 확장은 계속 추가 중(https://github.com/navidrome/navidrome/issues/2695).

주요 차이:

- 비디오 기능 없음(음악 전용).
- 멀티라이브러리를 `getMusicFolders`로 노출.
- 폴더 탐색 미지원. `getIndexes`, `getMusicDirectory`는 `/Artist/Album/01 - Song.mp3` 형태의 가상 트리를 반환.
- `stream` 호출은 재생 처리하지 않는다. `submission=true`인 `scrobble`만 기록한다.
- ID는 항상 문자열(MD5 해시 또는 UUID). 정수로 변환하는 클라이언트는 오작동한다.

지원 엔드포인트 그룹:

| 그룹 | 엔드포인트 | 비고 |
| --- | --- | --- |
| System | `ping`, `getLicense` | 라이선스는 항상 유효 |
| Browsing | `getMusicFolders`, `getIndexes`, `getMusicDirectory`, `getSong`, `getArtists`, `getArtist`, `getAlbum`, `getGenres` | `getIndexes`는 `shortcuts`/직계 자식 미지원 |
| Browsing(외부 연동 필요) | `getArtistInfo(2)`, `getAlbumInfo(2)`, `getTopSongs`, `getSimilarSongs(2)` | Last.fm 등 활성화 필요 |
| Lists | `getAlbumList(2)`, `getStarred(2)`, `getNowPlaying`, `getRandomSongs`, `getSongsByGenre` | |
| Search | `search2`, `search3` | Lucene 쿼리 미지원, 단순 자동완성만 |
| Playlists | `getPlaylists`, `getPlaylist`, `createPlaylist`, `updatePlaylist`, `deletePlaylist` | `getPlaylists`는 `username` 파라미터 미구현 |
| Media | `stream`, `download`, `getCoverArt`, `getLyrics`, `getAvatar` | `download`은 곡/앨범/아티스트/재생목록 ID와 트랜스코딩 옵션 허용 |
| Annotation | `star`, `unstar`, `setRating`, `scrobble` | |
| Bookmarks | `getBookmarks`, `createBookmark`, `deleteBookmark`, `getPlayQueue`, `savePlayQueue` | `getPlayQueue`의 `current`는 문자열 ID |
| Sharing | `getShares`, `createShare`, `updateShare`, `deleteShare` | `EnableSharing=true`일 때 |
| Radio | `getInternetRadioStations`, `create/update/deleteInternetRadioStation` | |
| Users | `getUser`, `getUsers` | `getUser`는 username 무시하고 인증 사용자 반환. `getUsers`는 인증 사용자만 반환 |
| Scan | `getScanStatus`, `startScan` | `getScanStatus`에 `lastScan`, `folderCount` 추가. `startScan`에 `fullScan` 불리언 추가 |

클라이언트별 동작 보정 설정: `Subsonic.LegacyClients`(기본 `DSub`), `Subsonic.MinimalClients`(기본 `SubMusic`), `Subsonic.AppendSubtitle`, `Subsonic.AppendAlbumVersion`, `Subsonic.DefaultReportRealPath`(보안상 기본 `false`).

## FAQ 요약

- **폴더 탐색**: 설계상 미지원. 태그, 멀티라이브러리, Persistent IDs(`PID.Album="folder"`)로 대체.
- **Various Artists 컴필레이션이 쪼개짐**: 모든 트랙에 `TCMP=1`(ID3) 또는 `COMPILATION=1`(FLAC) 설정. 아티스트별 다른 곡은 `Album Artist`를 동일하게 맞춘다.
- **태그 편집·파일 이동**: Navidrome은 음악 폴더에 쓰지 않는다. beets 또는 MusicBrainz Picard를 사용.
- **음악 업로드**: 내장 기능 없음. FileBrowser, SFTP, 네트워크 공유를 사용. 멀티라이브러리로 전용 Upload 라이브러리를 만드는 방법도 있다.
- **로그 위치**: stdout 전용. Docker `docker logs`, Linux `journalctl -u navidrome.service`, FreeBSD `/var/log/debug.log`, Windows MSI `C:\ProgramData\Navidrome\navidrome.log`.
- **AAC/M4A 다중값 태그가 안 읽힘**: 태그 편집기가 중복 atom을 만든 경우. Picard로 재저장하거나 Mp3tag에서 *Use single MP4 atom for multiple values*를 켠 뒤 저장하고 재스캔.
- **M3U 가져온 재생목록이 읽기 전용**: Auto-import가 켜져 있으면 파일이 곡 목록을 소유한다. 파일을 수정하거나 재생목록별 Auto-import 토글을 끈다. `AutoImportPlaylists=false`는 이미 가져온 목록을 편집 가능하게 만들지 않는다.
- **아트워크 원인 확인**: `navidrome artwork` 명령과 공식 아트워크 문제 해결 문서를 사용.
- **macOS "navidrome is damaged"**: `sudo xattr -d com.apple.quarantine /path/to/navidrome`.
