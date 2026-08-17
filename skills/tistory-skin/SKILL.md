---
name: tistory-skin
description: 티스토리 스킨(skin.html, index.xml, style.css)을 만들거나 수정하거나, 치환자·그룹치환자·홈 커버·사이드바·댓글·방명록·리스트·페이징을 조회할 때 사용합니다. /tistory-skin
---

# Tistory Skin

티스토리 스킨은 치환자 템플릿이다. 문서에 없는 치환자를 만들지 않는다. 치환자 정의·예제는 `references/`만 본다.

## 작업 순서

1. 대상 파일을 고른다. 필수 구성은 `references/common/files.md`.
2. 필요한 화면/기능을 고르고 아래 표의 해당 문서만 연다.
3. 문서의 그룹치환자·값치환자 이름과 중첩을 그대로 쓴다.
4. `index.xml`을 건드리면 스킨 설정이 전부 초기화된다. 기본값·커버·옵션·리스트 스타일 정의도 이 파일에 있다.

## 치환자 형태

`references/common/basic.md`

- 그룹: `<s_NAME>…</s_NAME>` — 조건/반복 영역
- 값: `[##_NAME_##]` — 치환될 값

`<s_t3>`는 `skin.html`의 `<body>` 안에 필수다. `references/common/global.md`

## 참조 지도

| 할 일 | 문서 |
| --- | --- |
| 파일 구성, preview | `references/common/files.md` |
| `index.xml` 스키마·기본값 | `references/common/index.xml.md` |
| 블로그 정보, 메뉴, `body_id`, 광고 | `references/common/global.md` |
| 홈 커버 | `references/common/cover.md` |
| 스킨 옵션 `s_if_var_*` / `[##_var_*_##]` | `references/common/variable.md` |
| 글, 퍼머링크/인덱스, 관련글, 이전/다음 | `references/contents/post.md` |
| 댓글 (커스텀 / `[##_comment_group_##]`) | `references/contents/comment.md` |
| 공지 | `references/contents/notice.md` |
| 보호글 | `references/contents/protected.md` |
| 페이지 | `references/contents/page.md` |
| 태그 클라우드 `/tag` | `references/contents/tag.md` |
| 방명록 (커스텀 / `[##_guestbook_group_##]`) | `references/contents/guestbook.md` |
| 카테고리·검색·태그 리스트 | `references/list/list.md` |
| 페이징 | `references/list/paging.md` |
| 사이드바 골격 | `references/sidebar/basic.md` |
| 최근 공지/글, 인기글, 최근 댓글 | `references/sidebar/recent_notice.md`, `recent_post.md`, `popular_post.md`, `recent_comment.md` |
| 카테고리, 랜덤태그, 방문자, 검색 | `references/sidebar/category.md`, `random_tag.md`, `count.md`, `search.md` |
| 목차 | `references/SUMMARY.md` |

## 규칙

- `skin.html`에 없는 화면은 다른 치환자로 떨어진다. 페이지 치환자가 없으면 글 치환자에 페이지가 섞인다.
- `<s_permalink_article_rep>` / `<s_index_article_rep>` 밖 치환자는 두 화면 모두에 나온다.
- 사이드바 모듈은 `<s_sidebar>` > `<s_sidebar_element>` 안. 엘리먼트 첫 주석 `<!-- TITLE -->`이 사이드바 제목이다.
- 기본 댓글/방명록 치환자(`[##_comment_group_##]`, `[##_guestbook_group_##]`)는 서버가 React 앱으로 렌더한다. 마크업을 직접 짜지 않아도 된다.
- 홈 커버는 `index.xml`의 `<cover>`에 정의한 `name`만 `<s_cover name="…">`에 쓴다. 기본값 JSON은 `RECENT` 또는 `CUSTOM`만.

## 흔한 실수

| 실수 | 처리 |
| --- | --- |
| 문서에 없는 치환자 창작 | 해당 `references/`를 열고 있는 이름만 쓴다 |
| `<s_t3>` 누락 | `body` 안에 넣는다 |
| `index.xml`을 가볍게 수정 | 적용 시 설정 초기화를 먼저 알린다 |
| 사이드바를 `s_sidebar_element` 없이 작성 | 모듈마다 감싼다 |
| 페이지/공지/보호글을 글 반복에만 넣음 | 전용 그룹 치환자를 쓴다 |
