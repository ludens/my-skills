---
name: usercss
description: Stylus용 UserCSS 스타일(`/* ==UserStyle== */` 메타데이터, `@var` 변수, `@preprocessor` 전처리기, `@-moz-document` 적용 범위)을 작성·수정하거나, `.user.css`/`.user.styl`/`.user.less` 파일을 만들어 설치·배포하려 할 때 사용합니다.
---

# UserCSS

Stylus용 UserCSS 스타일. 메타데이터 블록 + `@-moz-document` 적용 범위 + `@var` 설정 변수로 구성된다. 문서에 없는 필드·문법을 창작하지 않는다.

## 골격

```css
/* ==UserStyle==
@name         스타일 이름
@namespace    작성자/사이트
@version      1.0.0
@license      MIT
@preprocessor stylus

@var checkbox darkMode "다크 모드" 1
==/UserStyle== */

@-moz-document domain("example.com") {
  /* CSS 또는 전처리기 문법 */
}
```

## 전처리기(@preprocessor)를 먼저 정한다

변수 참조 문법·조건문이 전처리기마다 다르다. 분기가 필요하면 `stylus`를 고른다.

| `@preprocessor` | 변수 참조 | 조건문 |
| --- | --- | --- |
| `default` (또는 생략) | `var(--name)` | 없음 |
| `uso` | `/*[[name]]*/` | 없음 |
| `less` | `@name` | `& when (@name = 1) { }` |
| `stylus` | `name` | `if name { }` / `else` |

- `@preprocessor` 생략 + `@var` 없음 → `default`. 생략 + `@var` 있음 → `uso`.
- **체크박스·셀렉트로 분기(조건)하려면 `stylus`가 필요하다.** `default`/`uso`는 조건문이 없어 값 치환만 한다.
- `stylus`는 들여쓰기 기반. 변수 이름에 하이픈(`-`)을 쓰면 뺄셈으로 해석되므로 `camelCase`/`snake_case`를 쓴다.
- `stylus`에서 `url()`은 전처리 함수로 대체된다. base64 data-URI는 리터럴 CSS로 선언한다.

## 메타데이터

| 필드 | 필수 | 설명 |
| --- | --- | --- |
| `@name` | 필수 | 스타일 이름. `@namespace`와 조합이 고유해야 함 |
| `@namespace` | 필수 | 작성자 닉네임/홈페이지. `@name`과 조합이 고유해야 함 |
| `@version` | 필수 | semver. 업데이트 확인에 사용 |
| `@license` | 공유 시 필수 | SPDX 식별자(`MIT`, `CC-BY-SA-4.0` 등). 없으면 사용·배포 불가 간주 |
| `@description` | 선택 | 짧은 설명 |
| `@author` | 선택 | `이름 [<이메일>] [(URL)]` 순서 고정 |
| `@homepageURL` | 선택 | 소스 링크(업데이트 URL 아님) |
| `@supportURL` | 선택 | 이슈/피드백 링크 |
| `@updateURL` | 선택 | 없으면 설치 URL에서 업데이트 |

## @var (설정 변수)

`@var <type> <name> <label> <기본값>` 순서 고정. name은 `[\w-]+`(문자·숫자·`_`·`-`).

| type | 기본값 |
| --- | --- |
| `text` | 문자열. 콜론(`:`) 포함 시 `'"...:..."'`로 감싼다 |
| `color` | hex(3/4/6/8자리)·rgb·rgba |
| `checkbox` | `1`(on) / `0`(off) |
| `select` | JSON 객체 `{ "라벨": "값" }` 또는 배열 `["A", "B*"]`. `*`가 기본값 |

`select` 예:

```css
@var select fontName "글꼴" {
  "시스템": "system-ui, sans-serif",
  "세리프*": "Georgia, serif"
}
```

- 기본값은 필수. `select` 라벨에 공백·특수문자가 있으면 따옴표 필수.
- `!important`는 기본값에 넣지 않는다.

## @-moz-document (적용 범위)

| 함수 | 의미 |
| --- | --- |
| `domain("x.com")` | 도메인 + 서브도메인 |
| `url("...")` | 정확히 일치 |
| `url-prefix("...")` | 접두 일치 |
| `regexp("...")` | 정규식 |

여러 함수는 쉼표로 묶고, 여러 범위는 블록을 여러 개 쓴다.

## 파일명·설치

- 파일명이 `.user.css` / `.user.styl` / `.user.less`로 끝나야 설치 페이지가 뜬다.
- URL·로컬 파일 내용은 **plain text**여야 한다(웹 페이지 금지).
- 설치 페이지에서 `[x] Check for updates` 체크 해제 시 자동 업데이트 중단. 업데이트는 설치 URL 기준.
- 로컬 파일: Firefox는 `Ctrl/Cmd+O`로 열기. Chrome은 Stylus 열린 화면에 드래그앤드롭(자동 업데이트 X) 또는 파일 URL 접근 허용 후 `Ctrl/Cmd+O`.

## 예제

`example.com` 다크 모드. `stylus` + 체크박스·색상·텍스트·셀렉트 전부 사용:

```css
/* ==UserStyle==
@name         Example Dark Mode
@namespace    ludens.my-skills
@version      1.0.0
@description  Configurable dark mode for example.com
@author       ludens
@license      MIT
@preprocessor stylus

@var checkbox darkMode "다크 모드"      1
@var color    bgColor  "배경색"         #0d1117
@var text     fontSize "기본 글자 크기"  14px
@var select   fontName "글꼴" {
  "시스템": "system-ui, sans-serif",
  "세리프": "Georgia, serif"
}
==/UserStyle== */

@-moz-document domain("example.com") {
  body {
    font-size: fontSize !important;
    font-family: fontName !important;
  }
  if darkMode {
    body {
      background-color: bgColor !important;
      color: #c9d1d9 !important;
    }
  }
}
```

## 배포·호스팅

직접 링크 가능한 raw URL을 제공한다. 파일명이 `.user.css`로 끝나야 한다.

- GitHub: `https://raw.githubusercontent.com/{user}/{repo}/main/{name}.user.css`
- Gist: `https://gist.github.com/{user}/{sha}/raw/{name}.user.css`
- 링크가 `.user.css`로 안 끝나면 끝에 `?dummy=.user.css` 파라미터를 붙인다.

## 흔한 실수

| 실수 | 처리 |
| --- | --- |
| `default`/`uso`에 `if` 조건문 작성 | 조건문은 `stylus`(또는 less guard) 전용 |
| `uso` 플레이스홀더를 `[[name]]`으로 작성 | `/*[[name]]*/` — 주석 감싸기 필수 |
| 변수 참조 문법과 `@preprocessor` 불일치 | 표 보고 선언한 전처리기에 맞게 참조 |
| `stylus` 변수 이름에 하이픈 | `camelCase`/`snake_case`(하이픈은 뺄셈) |
| `@license` 누락 | 공유 시 필수, SPDX 식별자 |
| 파일명이 `.user.css`로 안 끝남 | 설치 페이지가 안 뜬다 |
