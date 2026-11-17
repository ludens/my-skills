# bugs-track-info 앨범 아티스트 이미지 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `--artist-image` 플래그를 켠 경우에만 앨범 아티스트 이미지 URL을 추가 수집해 `artist.image_url`로 출력한다.

**Architecture:** 앨범 페이지를 한 번 읽을 때 기본정보 `아티스트` 행에서 artist ID를 함께 뽑는다. 플래그가 켜졌을 때만 그 ID로 `/artist/{id}`를 요청하고 JSON-LD `MusicGroup.image`를 읽는다. 기존 `Client.get()`과 `jsonld()`를 재사용하고, 실패는 핵심 조회에 영향을 주지 않는다.

**Tech Stack:** Python 3 표준 라이브러리(`urllib`, `re`, `json`, `unittest`). 새 의존성 없음.

**Spec:** `docs/superpowers/specs/2026-11-18-bugs-artist-image-design.md`

## Global Constraints

- 플래그 이름은 `--artist-image`, 기본값 꺼짐.
- 곡의 대표 아티스트가 아니라 앨범 아티스트 기준.
- 플래그가 꺼져 있으면 `artist` 키를 출력하지 않고 추가 HTTP 요청도 하지 않는다.
- 아티스트 이미지 조회 실패 시 전체 조회를 실패시키지 않는다. `image_url`은 `없음`, `notes`에 경고.
- 벅스 페이지 값만 쓴다. 다른 소스로 보완하지 않는다.
- 사용자 문서는 한국어로 작성한다.

## Review Focus

- 플래그 미사용 시 `artist` 키와 추가 요청이 없어야 한다 → Task 2 실스트립 실행 검증.
- 앨범 아티스트와 곡 아티스트가 다를 때 앨범 쪽 ID를 골라야 한다 → Task 1 테스트에 기본정보 `아티스트` 행과 다른 아티스트 링크를 함께 둔다.
- JSON-LD가 `@graph`形式이거나 다른 `@type`이先是 잘못된 값을 읽지 않아야 한다 → Task 1 `artist_meta` 테스트에 `@graph`를 넣는다.
- 아티스트 페이지 요청이 실패해도 앨범·곡 필드는 유지되어야 한다 → Task 2 fake client 예외 테스트.
- 이미지가 없는 아티스트는 `image_url: "없음"`이어야 한다 → Task 1 테스트.

---

### Task 1: 앨범 아티스트 ID 추출과 아티스트 메타 파서

**Files:**
- Modify: `skills/bugs-track-info/scripts/fetch_bugs.py`
- Test: `skills/bugs-track-info/scripts/test_fetch_bugs.py`

**Interfaces:**
- Consumes: 기존 `Client.get(url) -> str`, `jsonld(doc, want=None) -> dict`, `info_table(doc) -> dict`, `text(fragment) -> str`, `BASE`, `meta(doc, key)`.
- Produces:
  - `album_artist_id(doc: str) -> str | None`
  - `artist_meta(client, artist_id: str) -> dict` — 반환 키 `name`, `image_url`, `url`. 이미지 없으면 `image_url`은 문자열 `없음`.
  - `album_meta(client, aid) -> tuple[dict, list, str | None]` — 기존 2튜플에서 세 번째 값으로 앨범 아티스트 ID 추가.

- [ ] **Step 1: 실패 테스트 작성**

`test_fetch_bugs.py`에 추가:

```python
ALBUM_DOC = '''
<table class="info">
  <tr><th scope="row">아티스트</th><td><a href="https://music.bugs.co.kr/artist/80327438">유나</a></td></tr>
</table>
<a href="https://music.bugs.co.kr/artist/99999999">참여 아티스트</a>
'''

ARTIST_DOC = '''
<script type="application/ld+json">{"@graph":[
  {"@type":"WebPage","name":"무관"},
  {"@type":"MusicGroup","name":"유나",
   "image":"https://image.bugsm.co.kr/artist/images/1200/803274/80327438.jpg",
   "sameAs":"https://music.bugs.co.kr/artist/80327438"}
]}</script>
'''

class FakeClient:
    def get(self, url):
        return ARTIST_DOC

def test_album_artist_id_uses_info_row(self):
    self.assertEqual(fb.album_artist_id(ALBUM_DOC), "80327438")

def test_album_artist_id_missing(self):
    self.assertIsNone(fb.album_artist_id("<html/>"))

def test_artist_meta_from_graph(self):
    got = fb.artist_meta(FakeClient(), "80327438")
    self.assertEqual(got["name"], "유나")
    self.assertEqual(got["image_url"], "https://image.bugsm.co.kr/artist/images/1200/803274/80327438.jpg")
    self.assertEqual(got["url"], "https://music.bugs.co.kr/artist/80327438")

def test_artist_meta_without_image(self):
    class NoImage(FakeClient):
        def get(self, url):
            return '<script type="application/ld+json">{"@type":"MusicGroup","name":"유나"}</script>'
    self.assertEqual(fb.artist_meta(NoImage(), "80327438")["image_url"], "없음")
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `python3 -m unittest discover -s skills/bugs-track-info/scripts -v`
Expected: `AttributeError: module 'fetch_bugs' has no attribute 'album_artist_id'` 등 4건 실패.

- [ ] **Step 3: `album_artist_id` 구현**

`fetch_bugs.py`에 함수를 추가한다. `info_table` 방식과 같이 `<th scope="row">아티스트</th>` 뒤의 `<td>` 블록만 정규식으로 잡고, 그 안의 첫 `/artist/(\d+)`를 반환한다. 블록이 없으면 `None`. 페이지 전체 검색은 쓰지 않는다.

- [ ] **Step 4: `artist_meta` 구현**

`fetch_bugs.py`에 함수를 추가한다. `client.get(BASE + "/artist/" + artist_id)`로 문서를 받고 `jsonld(doc, "MusicGroup")`에서 `name`, `image`, `sameAs`를 읽는다. `image`가 없으면 `meta(doc, "og:image")`를 쓰고, 그것도 없으면 `없음`. `url`은 `sameAs`가 없으면 `BASE + "/artist/" + artist_id`. 네트워크 예외는 이 함수에서 잡지 않고 호출자로 전달한다.

- [ ] **Step 5: `album_meta` 반환값 확장 및 기존 호출부 갱신**

`album_meta(client, aid)`가 `(album dict, rows, album_artist_id(doc))` 3튜플을 반환하게 한다. `track_meta`의 언패킹을 3값으로 바꾸고 세 번째 값은 일단 버린다. `album` 딕셔너리 내용은 기존과 동일하게 유지한다.

- [ ] **Step 6: 테스트 통과 확인**

Run: `python3 -m unittest discover -s skills/bugs-track-info/scripts -v`
Expected: 기존 8건 포함 12건 PASS.

- [ ] **Step 7: 커밋**

```bash
git add skills/bugs-track-info/scripts/fetch_bugs.py skills/bugs-track-info/scripts/test_fetch_bugs.py
git commit -m "feat(bugs-track-info): 앨범 아티스트 ID·이미지 파서 추가"
```

### Task 2: 플래그 연결과 출력·문서 반영

**Files:**
- Modify: `skills/bugs-track-info/scripts/fetch_bugs.py`
- Modify: `skills/bugs-track-info/scripts/test_fetch_bugs.py`
- Modify: `skills/bugs-track-info/SKILL.md`

**Interfaces:**
- Consumes: Task 1의 `album_artist_id`, `artist_meta`, `album_meta -> (dict, list, str|None)`.
- Produces:
  - `track_meta(client, tid, preferred_album=None, want_artist_image=False) -> dict`
  - `main()`의 `--artist-image` (`action="store_true"`)
  - 출력 최상위 `artist` 키는 플래그가 켜졌을 때만 존재.

- [ ] **Step 1: 실패 테스트 작성**

`test_fetch_bugs.py`에 fake client를 이용한 3건을 추가한다. fake client는 `/track/`, `/album/` 요청에는 아래 문서를 주고 `/artist/` 요청에는 Task 1의 `ARTIST_DOC`를 준다.

```python
TRACK_DOC = ('<meta property="og:title" content="Ice Cream / 유나 (ITZY)"/>'
             '<script type="application/ld+json">{"@type":"MusicRecording",'
             '"name":"Ice Cream","inAlbum":{"url":"https://music.bugs.co.kr/album/20798430"}}</script>')
ALBUM_MIN_DOC = ('<script type="application/ld+json">{"@type":"MusicAlbum",'
                 '"name":"Ice Cream","image":"https://img/a.jpg"}</script>' + ALBUM_DOC)

class RoutingClient:
    def get(self, url):
        if "/artist/" in url:
            return ARTIST_DOC
        if "/track/" in url:
            return TRACK_DOC
        if "/album/" in url:
            return ALBUM_MIN_DOC
        raise AssertionError(url)

def test_flag_off_omits_artist_key(self):
    got = fb.track_meta(RoutingClient(), "33878893", want_artist_image=False)
    self.assertNotIn("artist", got)

def test_flag_on_adds_artist_image(self):
    got = fb.track_meta(RoutingClient(), "33878893", want_artist_image=True)
    self.assertEqual(got["artist"]["image_url"],
                     "https://image.bugsm.co.kr/artist/images/1200/803274/80327438.jpg")

def test_artist_failure_keeps_core_fields(self):
    class FailArtist(RoutingClient):
        def get(self, url):
            if "/artist/" in url:
                raise RuntimeError("bot wall")
            return super().get(url)
    got = fb.track_meta(FailArtist(), "33878893", want_artist_image=True)
    self.assertEqual(got["album"]["name"], "Ice Cream")
    self.assertEqual(got["track"]["title"], "Ice Cream")
    self.assertEqual(got["artist"]["image_url"], "없음")
    self.assertTrue(any("아티스트 이미지" in n for n in got["notes"]))
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `python3 -m unittest discover -s skills/bugs-track-info/scripts -v`
Expected: `TypeError: track_meta() got an unexpected keyword argument 'want_artist_image'`.

- [ ] **Step 3: `track_meta` 확장**

시그니처에 `want_artist_image=False`를 추가한다. `album_meta`가 준 artist ID가 있을 때만 아티스트 키를 만든다. ID가 없으면 `artist: {"name": "없음", "image_url": "없음", "url": "없음"}`과 `notes` 경고를 넣는다. `artist_meta` 호출이 예외를 던지면 같은 `없음` 형태와 `notes` 경고로 처리하고 핵심 필드는 유지한다. 플래그가 꺼지면 아티스트 관련 코드 경로를 전혀 실행하지 않는다.

- [ ] **Step 4: `main()`에 플래그 추가**

`argparse`에 `--artist-image` (`action="store_true"`)를 추가하고 `track_meta(..., want_artist_image=args.artist_image)`로 전달한다. 다른 CLI 동작은 바꾸지 않는다.

- [ ] **Step 5: SKILL.md 갱신**

실행 예시에 `--artist-image` 사용법을 추가한다. 필드 출처 표에 `아티스트 이미지` 행(아티스트 페이지 JSON-LD `MusicGroup.image`, 앨범 아티스트 기준)을 추가한다. 출력 템플릿에 `artist` 블록을 플래그 사용 시에만 포함한다는 한 줄과 실패 처리 규칙을 추가한다.

- [ ] **Step 6: 테스트 통과 확인**

Run: `python3 -m unittest discover -s skills/bugs-track-info/scripts -v`
Expected: 15건 PASS.

- [ ] **Step 7: 실제 페이지 검증**

```bash
python3 skills/bugs-track-info/scripts/fetch_bugs.py --track 33878893
python3 skills/bugs-track-info/scripts/fetch_bugs.py --track 33878893 --artist-image
```

Expected: 첫 명령에는 `artist` 키 없음. 두 번째 명령의 `artist.image_url`이 `https://image.bugsm.co.kr/artist/images/1200/803274/80327438.jpg`. 두 명령의 `album.name`과 `track.title`은 모두 `Ice Cream`.

- [ ] **Step 8: 커밋**

```bash
git add skills/bugs-track-info/scripts/fetch_bugs.py skills/bugs-track-info/scripts/test_fetch_bugs.py skills/bugs-track-info/SKILL.md
git commit -m "feat(bugs-track-info): --artist-image 옵션 추가"
```
