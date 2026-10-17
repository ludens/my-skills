---
name: codepen-example
description: 간결한 HTML/CSS/JS 코드 예시를 만들어 CodePen 펜으로 게시하고 공유 URL을 반환해야 할 때, 또는 CodePen API v2로 데모·예제를 올려달라는 요청을 받았을 때 사용합니다. "codepen", "예시 코드", "데모"와 함께 예제 제작·게시를 요청받을 때 사용합니다.
---

# CodePen Example

## 개요

간결한 코드 예시 = 파일 1개(`index.html`), 인라인 `<style>`/`<script>`, 읽을 수 있는 코드. CodePen API v2로 게시하고 에디터 URL을 반환한다. 코드만 달라는 요청엔 펜 생성하지 않는다.

## 작업 순서

1. 예시를 `index.html` 하나로 작성. 데모에 필요한 최소 코드만.
2. `.env`에서 `CODEPEN_API_KEY` 로드 (값 출력 금지).
3. `POST https://api.codepen.io/v2/pens`로 펜 생성.
4. 응답의 `build.status == "Success"` 확인.
5. `urls.editor`(공유 링크)와 `urls.preview` 반환.

## API (서브에이전트에 웹 검색 도구 없음 — 사실 전부 여기)

```bash
CODEPEN_API_KEY=$(grep '^CODEPEN_API_KEY=' .env | cut -d= -f2-)

curl -sS -X POST https://api.codepen.io/v2/pens \
  -H "Authorization: Bearer $CODEPEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "예시 제목",
    "description": "한 줄 설명",
    "tags": ["demo"],
    "access": "Public",
    "files": [
      {"path": "index.html", "content": "<style>...</style><h1>...</h1><script>...</script>"}
    ]
  }'
```

- 기본 URL `https://api.codepen.io/v2/`. 인증: `Authorization: Bearer $KEY` 또는 `X-API-Key: $KEY`.
- 생성 응답 `201`. 본문에 `urls.editor`, `urls.preview`, 최상위 `build.status`.
- 파일 여러 개: `files` 배열에 `path`/`content` 추가 (`index.html`, `style.css`, `script.js`).

## 규칙 (간결함)

- 파일 1개. HTML·CSS·JS 전부 `index.html` 인라인. ~100줄 넘을 때만 `style.css`/`script.js` 분리.
- 외부 CDN 라이브러리 금지 (요구 시에만).
- 읽을 수 있는 코드 (줄바꿈·들여쓰기). minify 금지 — "예시"는 읽는 것.
- 데모 하나만. 장식·애니메이션·추가 기능 금지.

## 함정

- **`urls.preview`는 익명 방문자에게 307→에디터 리다이렉트.** 공유 링크는 `urls.editor`.
- **Free 플랜: 3펜/일.** 요청 시에만 생성, 시행착오로 펜 낭비 금지. `access: Private`는 PRO 전용 → Free에선 `403 FORBIDDEN`. `Public`만.
- **키 값 절대 출력 금지.** 사용만, 응답·로그·코드에 노출 안 함.
- **빌드 실패도 201/200.** 파일은 저장됨. `build.status != Success`면 `build.errors` 보고, 수정 후 재작성.
- 컴파일러가 파일을 자동 추가·수정 가능(예: `pen.config.json`, `tsconfig.json` 자동 생성) — 정상이니 그대로 둔다. 재작성 전 `GET /v2/pens/:id/files`로 실제 파일 재조회.

## 검증

게시 후 실제 동작 확인:

- `build.status == "Success"` (응답 본문)
- `GET /v2/pens/:id` → `200`
- `GET /v2/pens/:id/files` → 보낸 `index.html` 내용 일치
