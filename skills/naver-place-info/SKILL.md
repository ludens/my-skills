---
name: naver-place-info
description: 네이버지도 장소 URL(map.naver.com/p/entry/place/…), naver.me 짧은 링크, 또는 숫자 place ID로 주소·전화·영업시간 등 장소 정보를 조회할 때 사용합니다. /naver-place-info
---

# Naver Place Info

네이버지도 장소 URL, `naver.me` 짧은 링크, 또는 숫자 place ID로 공개된 장소 정보를 고정 형식으로 정리한다.

## 사용 시점

- 사용자가 `map.naver.com` 장소 URL을 붙일 때
- 사용자가 `naver.me` 짧은 링크를 붙일 때
- 숫자 place ID만 줄 때
- `/naver-place-info` 를 실행할 때

상호명 검색, 주소 검색, 공식 오픈 API는 쓰지 않는다.

## 작업 순서

1. 입력에서 숫자 place ID를 뽑는다.
   - `https://map.naver.com/p/entry/place/{id}`
   - 같은 호스트에서 `/place/{id}` 또는 `/entry/place/{id}` 가 있는 URL
   - 숫자만. 예: `2032470851`
2. URL인데 ID가 없으면 리다이렉트를 따라간 뒤, 최종 URL에서 다시 뽑는다. `naver.me`가 여기 해당한다.

```sh
curl -sI -L --max-time 20 -A 'Mozilla/5.0' -o /dev/null -w '%{url_effective}\n' "$url"
```

3. 그래도 ID를 못 뽑으면 허용 입력 형식을 안내하고 조회하지 않는다.
4. markdown.new 스킬로 아래 URL을 읽는다. `map.naver.com` 본문은 SPA라 쓰지 않는다.

```sh
curl -L --fail --silent --show-error "https://markdown.new/https://pcmap.place.naver.com/place/{id}/home"
```

5. 페이지에 보이는 값만 추출한다. 없는 필드는 `없음`이다. 다른 출처로 채우지 않는다.
6. 결과가 비거나 장소를 못 찾으면 원인만 적고 중단한다.

## 필드

| 필드 | 출처 |
| --- | --- |
| 이름 | 제목 / og:title |
| 카테고리 | 본문 카테고리 텍스트 |
| 주소 | 주소 섹션 |
| 전화 | 전화번호 섹션 |
| 영업시간 | 영업시간 섹션 |
| 홈페이지 | 홈페이지 URL |
| SNS | 인스타그램, 블로그 등 링크 |
| 찾아가는 길 | 찾아가는길 섹션 |
| 편의 | 편의 섹션 |
| 리뷰 | og:description 또는 리뷰 링크 텍스트 |
| 좌표 | 길찾기 등 링크의 `latitude` / `longitude` |
| URL | 사용자가 준 URL. ID만 준 경우 `https://map.naver.com/p/entry/place/{id}` |

## 출력

```markdown
# {이름}

- 카테고리: …
- 주소: …
- 전화: …
- 영업시간: …
- 홈페이지: …
- SNS: …
- 찾아가는 길: …
- 편의: …
- 리뷰: …
- 좌표: …
- URL: …
```
