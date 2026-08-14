# naver-place-info 설계

## 목적

네이버지도 장소 URL 또는 숫자 place ID를 받아, 해당 장소의 공개 정보를 고정 형식으로 정리한다.

## 위치

- 스킬: `skills/naver-place-info/SKILL.md`
- README 스킬 표에 한 줄 추가
- 스크립트, API 키, `agents/` 설정은 두지 않는다

## 입력

다음만 받는다.

- `https://map.naver.com/p/entry/place/{id}` 형태 URL
- 같은 호스트의 변형 URL에서 `/place/{id}` 또는 `/entry/place/{id}` 로 추출 가능한 링크
- `https://naver.me/...` 처럼 장소 페이지로 리다이렉트되는 짧은 링크
- 숫자만 있는 place ID. 예: `2032470851`

상호명 검색, 주소 검색, 공식 오픈 API는 범위 밖이다.

## 조회

1. 입력에서 숫자 place ID를 추출한다. URL에 ID가 없으면 리다이렉트를 따라간 뒤 최종 URL에서 다시 추출한다.
2. markdown.new 스킬을 사용해 아래 URL을 읽는다.

```text
https://pcmap.place.naver.com/place/{id}/home
```

3. 페이지에서 보이는 값만 추출한다. 없는 필드는 추측하지 않고 `없음`으로 둔다.

`map.naver.com` 본문은 SPA라 쓰지 않는다. `pcmap.place.naver.com/place/{id}/home`은 음식점 ID에도 동작한다.

## 출력 필드

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
| 리뷰 수 | og:description 또는 리뷰 링크 텍스트 |
| 좌표 | 길찾기 등 링크의 `latitude` / `longitude`. 없으면 `없음` |
| 원본 URL | 사용자가 준 URL. ID만 준 경우 `https://map.naver.com/p/entry/place/{id}` |

## 출력 형식

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

## 실패

- place ID를 못 뽑으면 허용 입력 형식을 안내하고 조회하지 않는다.
- markdown.new 결과가 비거나 장소를 못 찾으면 원인만 적고 중단한다.
- 필드가 페이지에 없으면 `없음`이다. 다른 출처로 채우지 않는다.

## description

네이버지도 장소 URL(`map.naver.com/p/entry/place/…`)이나 숫자 place ID로 주소·전화·영업시간 등 장소 정보를 조회할 때 사용합니다. `/naver-place-info`

## 검증

- 샘플 `https://map.naver.com/p/entry/place/2032470851` 로 이름 `보스김밥`, 주소 `서울 마포구 성미산로 138 1층`이 나오는지 확인한다.
- README에 `naver-place-info`가 보이는지 확인한다.
- 저장소에 옛 이름 `naver-place`가 남지 않는지 검색한다.
