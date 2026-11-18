---
name: bugs-track-info
description: 벅스뮤직(music.bugs.co.kr)에서 음원 파일 태그용 앨범·곡 정보를 가져올 때 사용합니다. 가수명+곡명, 곡 URL(/track/{id}), 앨범 URL(/album/{id})을 받아 앨범명·커버·앨범 아티스트·발매일·총 트랙수·총 디스크수·장르와 곡 제목·아티스트·작곡·작사·편곡·트랙 번호·디스크 번호·가사를 추출합니다. / Triggers - 벅스 태그 정보, 벅스 곡 정보, bugs music metadata, audio tagging from Korean music site
---

# Bugs Track Info

벅스 페이지에 보이는 값만 골라 음원 태그용 고정 형식으로 정리한다. 다른 사이트로 보완하지 않는다.

## 입력

- 가수명 + 곡명. 예: `유나`, `Ice Cream`
- 곡 URL 또는 숫자 ID. 예: `https://music.bugs.co.kr/track/33878893`, `33878893`
- 앨범 URL 또는 숫자 ID와 곡 ID 조합. 예: `--album 20798430 --track 33878893`
- 아티스트 이미지가 필요하면 `--artist-image`를 붙인다. 기본은 끄기. 곡의 대표 아티스트가 아니라 앨범 아티스트 기준.

## 실행

```sh
python3 skills/bugs-track-info/scripts/fetch_bugs.py --artist "유나 (ITZY)" --song "Ice Cream"
python3 skills/bugs-track-info/scripts/fetch_bugs.py --track 33878893
python3 skills/bugs-track-info/scripts/fetch_bugs.py --album 20798430 --track 33878893
python3 skills/bugs-track-info/scripts/fetch_bugs.py --track 33878893 --artist-image
```

stdout에 JSON 하나가 나온다. 표준 라이브러리만 쓴다. 설치할 의존성 없다.

벅스는 첫 요청에 `429`와 `bw_v` 쿠키를 주고 재요청을 요구한다. 스크립트가 쿠키 재사용으로 처리한다. `webfetch`나 단발 `curl`로 직접 긁지 않는다. 429가 계속되면 실패를 보고하고 멈춘다.

가수+곡명으로 검색하면 `candidates`가 나온다. `notes`에 "후보 확인 필요"가 있으면 1위가 정확 일치가 아니다. 이때 후보 제목·아티스트를 사용자에게 보여주고 어떤 곡인지 확인한다. 임의로 넘어가지 않는다. 곡명을 한글로만 줬는데 벅스 제목이 영문이면 이 경고가 뜰 수 있다. 사용자가 영문 제목도 같이 알려줬으면 `--song`에 그 영문 제목을 쓴다.

## 필드 출처

| 필드 | 출처 |
| --- | --- |
| 앨범명 | JSON-LD `name`. 없으면 `og:title`의 ` / ` 앞 부분 |
| 앨범 커버 | JSON-LD `image` (`og:image`, 1200x1200) |
| 앨범 아티스트 | JSON-LD `byArtist.name`. 없으면 기본정보 표 `아티스트` |
| 아티스트 이미지 (`--artist-image`) | 앨범 기본정보 `아티스트` 링크의 ID로 `/artist/{id}`를 요청, JSON-LD `MusicGroup.image` (1200x1200) |
| 발매일 | JSON-LD `datePublished`. 페이지 표기는 `YYYY.MM.DD` |
| 총 트랙수 | 앨범 수록곡 표의 `trackId` 행 수 |
| 총 디스크수 | 수록곡 `disc_id`의 서로 다른 값 개수 |
| 장르 | 앨범 기본정보 표 `장르`. `스타일`이나 소개문의 장르로 대체하지 않는다 |
| 곡 제목 | JSON-LD `name`. 없으면 `og:title` 앞 부분 |
| 곡 아티스트 | JSON-LD `byArtist.name`. 없으면 곡 정보 표 `아티스트` |
| 트랙 번호 | `meta[sc:track_no]`. 없으면 앨범 수록곡 `<em>` |
| 디스크 번호 | 같은 `trackId` 행의 `disc_id` |
| 작곡 / 작사 / 편곡 | 곡 페이지의 참여 정보 레이어 전체 표 |
| 가사 | `div.lyricsContainer > xmp`. 없으면 `없음` |

## 전체 보기 (참여 정보)

곡 페이지의 보이는 "참여 정보" 줄은 보컬·작곡·작사만 보여주고 잘린다. 작곡·작사·편곡 전체는 `전체 보기` 버튼이 여는 레이어에 있다. 이 레이어는 `<aside id="participatingArtists">`로 HTML에 이미 들어 있다. 브라우저 클릭 없이 이 표를 파싱한다. `편곡`은 여기서만 나온다.

레이어가 없으면 크레딧이 없는 곡이다. 빈 배열로 두고 `notes`를 확인한다. 소개문의 Credit 표기(예: `FEYI`, `EXY`)로 이름을 바꾸거나 합치지 않는다. 벅스 참여 정보 표의 이름을 그대로 쓴다.

## 출력

```markdown
# {곡 제목} — {아티스트}

## 앨범
- 앨범명: …
- 커버: …
- 앨범 아티스트: …
- 발매일: …
- 총 트랙수: …
- 총 디스크수: …
- 장르: …

## 곡
- 곡 제목: …
- 아티스트: …
- 트랙 번호: …
- 디스크 번호: …
- 작곡: A, B
- 작사: C, D
- 편곡: E

### 가사
…

## 아티스트 이미지 (`--artist-image` 사용 시에만)
- 이름: …
- 이미지 URL: …

## 출처
- 곡: https://music.bugs.co.kr/track/{id}
- 앨범: https://music.bugs.co.kr/album/{id}
```

없는 값은 `없음`이다. 추측으로 채우지 않는다. 총 디스크수와 디스크 번호는 페이지에 명시된 필드가 아니라 `disc_id`에서 유도한 값임을 출력에 한 줄로 적는다. `--artist-image`가 없으면 아티스트 이미지 블록과 JSON의 `artist` 키를 출력하지 않는다.

## 실패 처리

- 검색 결과 없음: 질의를 다시 적거나 URL을 달라고 한다.
- 429 반복: 벅스 차단으로 보고하고 중단한다. 우회 위해 다른 사이트를 쓰지 않는다.
- 앨범 ID 없음: 곡 정보만 출력하고 앨범·디스크 필드는 `없음`으로 둔다.
- 아티스트 이미지 조회 실패: 전체 조회는 유지하고 `artist.image_url`을 `없음`으로 두고 `notes`에 경고를 적는다. 앨범 아티스트 ID가 없을 때도 같다.
