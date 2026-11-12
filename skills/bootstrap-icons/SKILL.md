---
name: bootstrap-icons
description: Use when SVG 구조도·문서에 Bootstrap Icons를 넣을 때, 또는 의도에 맞는 아이콘 이름·SVG URL·다운로드·심볼 삽입 방법이 필요할 때. 사용자·데이터베이스·서버·방화벽 같은 범용 UI 글리프를 구조도 노드로 쓰는 경우를 포함한다. / Triggers - add Bootstrap Icons to SVG diagram, find bootstrap icon name and svg url
---

# Bootstrap Icons

범용 UI 글리프가 필요할 때 Bootstrap Icons에서 아이콘을 찾고, 내려받고, SVG 구조도에 심볼로 삽입할 때 참조하는 카탈로그.

## 소스

| 항목 | 값 |
| --- | --- |
| 아이콘 사이트 | <https://icons.getbootstrap.com/> |
| 버전 | `1.13.2` (고정) |
| 아이콘 수 | 2,078개 |
| 카테고리 | 29개 |
| 라이선스 | MIT. 단 브랜드 로고는 각 상표권자의 상표다. |
| 개별 SVG URL | `https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.2/icons/<name>.svg` |
| 스프라이트 | `bootstrap-icons.svg` (`<symbol id="bi-<name>">`) |
| 메타데이터 | <https://icons.getbootstrap.com/icons/index.json> |
| 이름 카탈로그 | [references/icon-names.txt](references/icon-names.txt) |
| 스냅샷 | 2026-11-12 |

모든 아이콘은 `viewBox="0 0 16 16"`, 1px 선 기반이다. 이름은 케밥 케이스이고, 전체 2,078개 이름과 29개 카테고리는 `references/icon-names.txt`에 있다. 새 이름은 그 파일에 있는 것만 쓴다.

## 빠른 선택

| 다이어그램 의도 | 아이콘 | 메모 |
| --- | --- | --- |
| 사용자 | `person` | 단일 사용자 실루엣 |
| 사용자 그룹 | `people` | 여러 명 실루엣. `person` 여러 개를 나열하지 않는다 |
| 인증 / 권한 | `shield-check` | 접근 허용·인증 경계 |
| 관리자 | `person-gear` | 운영자·어드민 계정 |
| 데이터베이스 | `database` | 실린더 |
| 캐시 | `database-fill` | 전용 캐시 아이콘 없음. 라벨로 구분한다 |
| 큐 | `inboxes` | 적재된 트레이. `list-task`도 가능 |
| 스토리지 | `hdd-stack` | 디스크 스택 |
| 파일 | `file-earmark` | 낱개 파일 |
| 폴더 | `folder` | 디렉터리 |
| 서버 | `server` | 랙 1대 |
| 클라우드 | `cloud` | 추상 클라우드 경계 |
| 네트워크 | `diagram-3` | 노드 3개 연결 |
| API | `braces` | `{}`. `code-slash`도 가능 |
| 방화벽 / 보안 | `shield-lock` | `firewall` 아이콘은 없다. 아래 설명 참조 |
| 경고 | `exclamation-triangle` | 주의·위험 |
| 오류 | `x-circle` | 실패·예외 |
| 성공 | `check-circle` | 완료·정상 |
| 알림 | `bell` | 이벤트 통지 |
| 검색 | `search` | 돋보기 |
| 설정 | `gear` | 구성·환경설정 |
| 로그 | `journal-text` | 줄 단위 기록 |
| 모니터링 | `activity` | 심박 그래프 |
| 시계 / 스케줄 | `clock` | 주기 실행·타이머 |
| 배포 / 릴리스 | `rocket` | 릴리스 파이프라인 |
| 컨테이너 | `boxes` | 여러 컨테이너. `box`는 단일 패키지 |
| 브랜치 | `git` | 분기·버전 관리 |
| 문서 | `file-earmark-text` | 텍스트 문서 |
| 이메일 | `envelope` | 메일 발송·수신 |
| 결제 | `credit-card` | 과금·카드 |
| 분석 | `bar-chart` | 집계·대시보드 |
| 잠금 | `lock` | 비밀·보호 구간 |
| 키 | `key` | 자격 증명·암호 키 |
| 백업 | `archive` | 아카이브 보관 |
| 외부 링크 | `box-arrow-up-right` | 시스템 경계 밖 이동 |
| 다운로드 | `download` | 인바운드 전송 |
| 업로드 | `upload` | 아웃바운드 전송 |
| 재시도 | `arrow-clockwise` | 반복·리플레이 |
| 웹훅 | `broadcast` | 외부로 밀어내는 이벤트 |
| 메시지 | `chat-dots` | 대화·메시지 버스 |
| 로봇 / AI | `robot` | 자동화·에이전트. `cpu`는 연산 노드 |
| 사람 / 팀 | `people-fill` | 조직 단위 강조 |
| 건물 / 오피스 | `building` | 사무실·거점 |
| 위치 | `geo-alt` | 지도 핀 |
| 이동 / 트래픽 | `arrow-left-right` | 양방향 흐름. `signpost-split`은 분기 경로 |
| 중지 | `stop-circle` | 정지·비활성 |
| 재생 | `play-circle` | 시작·활성 |
| CDN / 엣지 | `globe2` | 지구본. `globe`는 DNS·인터넷 |
| 터미널 / CLI | `terminal` | 셸·명령 실행 |

방화벽 아이콘은 Bootstrap Icons에 없다. 의도가 "경계 차단"이면 `shield-lock`, "검사 후 통과"면 `shield-check`, "정책 위반 경고"면 `shield-exclamation`으로 매핑하고, 노드 라벨에 `Firewall`을 적어 의미를 고정한다.

## 선택 기준

- 기본은 아웃라인. `-fill`은 같은 아이콘의 채운 변형이고, 강조·범례·작은 배지처럼 선이 뭉개지는 자리에만 쓴다. 한 구조도 안에서 같은 종류의 노드는 아웃라인으로 통일한다.
- `-fill`이 모든 아이콘에 있는 것은 아니다. `check-lg`, `info-lg`, `exclamation-lg`, `arrow-left`처럼 채운 변형이 없는 이름이 739개 있다. 짝이 있다고 가정하고 이름을 만들지 말고 `references/icon-names.txt`에서 확인한다.
- 브랜드 아이콘 85개(`github`, `slack` 등)는 실제 제품·회사 노드에만 쓴다. "서버", "클라우드", "결제" 같은 일반 노드에 브랜드 로고를 대신 쓰지 않는다. 상표이므로 재배포·변형에 주의한다.
- 의미가 겹치는 사람 계열은 이렇게 나눈다. `person`은 단일 사용자, `people`은 다수 사용자 그룹, `person-circle`은 아바타 자리(원형 프레임), `person-badge`는 신원·프로필 카드, `person-check`는 승인된 사용자다. 노드 라벨 없이 아이콘만으로 구분되지 않으므로 라벨을 함께 적는다.
- `server`와 `hdd-stack`, `database`는 다르다. 컴퓨트는 `server`, 블록 스토리지는 `hdd-stack`, 질의 가능한 저장소는 `database`다.
- `cloud`는 클라우드 경계(점선 박스)에, `globe`는 인터넷·DNS에 쓴다. 서로 바꿔 쓰지 않는다.

## 크기·색

- 원본은 16×16에 1px 선이다. 구조도에서는 24–32px를 권장한다. 32px까지는 선이 유지되고, 40px를 넘기면 선이 상대적으로 가늘어 보인다.
- 48px가 필요하면 아이콘을 확대하지 말고 노드 크기를 줄이거나, 선이 두꺼운 다른 세트를 쓴다. 48px로 늘리면 선 굵기가 3px로 보여 AWS·Cloudflare의 채워진 아이콘 옆에서 흐릿해진다.
- AWS·Cloudflare 아이콘은 타일·면 기반이고 Bootstrap Icons는 선 기반이다. 같은 행에 같은 크기로 섞지 않는다. 섞어야 하면 Bootstrap Icons를 24px, 상대를 32–40px로 두어 시각 무게를 맞춘다.
- 색은 `fill="currentColor"` 상속을 기본으로 한다. `<symbol>`에 `fill="currentColor"`를 넣고 상위에서 `color`를 정하면 `<use>`마다 색을 반복하지 않아도 된다.
- 기본 색은 Bootstrap primary `#0d6efd`, 중립 노드는 `#495057`. 배경과 대비가 부족하면 `#212529`까지 어둡게 한다. 상태색은 경고 `#ffc107`, 오류 `#dc3545`, 성공 `#198754`를 쓰되 아이콘과 라벨에 같은 색을 적용한다.
- `stroke`를 따로 주지 않는다. Bootstrap Icons는 `fill` 경로로 그려져 있어 `stroke`를 추가하면 형태가 뭉개진다.

## 다운로드

```bash
# 하나
bash scripts/fetch-icons.sh assets/bootstrap-icons database

# 여러 개
bash scripts/fetch-icons.sh assets/bootstrap-icons database server shield-lock cloud

# 카테고리 단위 (Data 12개)
bash scripts/fetch-icons.sh assets/bootstrap-icons --category data

# 전체 2,078개
bash scripts/fetch-icons.sh assets/bootstrap-icons --all

# 카탈로그의 이름만 출력
bash scripts/fetch-icons.sh --list
```

`fetch-icons.sh`는 `references/icon-names.txt`에 없는 이름을 `unknown icon: <name>`으로 보고하고, `image/svg+xml`이 아니거나 본문에 `<svg`가 없으면 저장하지 않는다. 실패는 마지막에 목록으로 출력하고 exit 1로 끝난다. 이미 받은 파일은 건너뛴다.

`--category`는 카테고리 표시 이름을 소문자·하이픈 슬러그로 바꿔 받는다. `data`, `security`, `files-and-folders`, `alerts-and-status`, `ui-and-keyboard`, `real-world`처럼 쓴다. 없는 카테고리는 `unknown category`로 실패한다.

개별 파일을 직접 받아도 된다.

```bash
curl -fsSL "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.2/icons/database.svg" -o database.svg
```

## SVG에 삽입

최종 구조도는 자기완결적이어야 한다. 아이콘을 원격 URL로 참조하지 말고 SVG 안에 심볼로 넣는다.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 160">
  <defs>
    <!-- database.svg의 <?xml?>, 바깥 <svg>, class/width/height를 제거한 내부 -->
    <symbol id="bi-database" viewBox="0 0 16 16" fill="currentColor">
      <path d="..."/>
    </symbol>
    <symbol id="bi-server" viewBox="0 0 16 16" fill="currentColor">
      <path d="..."/>
    </symbol>
  </defs>

  <rect x="30" y="45" width="120" height="80" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>
  <use href="#bi-database" x="52" y="63" width="28" height="28" fill="#495057"/>
  <text x="90" y="112" font-size="12" text-anchor="middle" fill="#334155">Database</text>
</svg>
```

삽입 규칙:

1. 원본의 바깥 `<svg ...>`를 `<symbol id="bi-<name>" viewBox="0 0 16 16" fill="currentColor">`로 바꾼다. `viewBox`는 원본 값을 그대로 옮긴다.
2. `class="bi bi-database"`, `width="16"`, `height="16"`은 남기지 않는다. 남기면 문서 CSS·레이아웃과 충돌하고, `<use>`의 크기 지정을 덮어쓴다.
3. `<?xml ...?>`, `<!DOCTYPE ...>`, 주석은 제거한다. `<symbol>` 안에 두면 XML 선언이 중첩되어 파싱이 깨진다.
4. 크기와 색은 `<use>`에 준다. `<use href="#bi-database" width="28" height="28" fill="#495057"/>`. `x`/`y`로 위치를 잡는다.
5. 기본은 `href`만 쓴다. 구형 렌더러가 필요할 때만 `xmlns:xlink`와 `xlink:href`를 함께 넣는다.
6. 같은 아이콘을 여러 번 쓰면 `<symbol>`은 한 번만 정의하고 `<use>`를 반복한다.

심볼 생성은 스크립트로 처리한다.

```bash
python3 scripts/build-sprite.py --dir assets/bootstrap-icons \
  --out assets/bootstrap-sprite.svg database server shield-lock cloud

# <symbol> 블록만 출력해 기존 <defs>에 붙이기
python3 scripts/build-sprite.py --dir assets/bootstrap-icons --fragment \
  database server shield-lock cloud
```

`build-sprite.py`는 XML 선언·DOCTYPE·바깥 `<svg>`를 제거하고, `viewBox`를 심볼로 옮기며, `class`/`width`/`height`를 넣지 않는다. id는 `bi-<name>`이고, `bi-` 접두가 붙은 이름에는 다시 붙이지 않는다. 없는 파일은 `missing: <name>`으로 보고하고 exit 1로 끝난다.

## 자주 틀리는 것

| 오해·증상 | 실제 |
| --- | --- |
| `firewall` 아이콘이 있다 | 없다. `shield-lock`, `shield-check`, `shield-exclamation`으로 매핑하고 라벨에 Firewall을 적는다. |
| URL에 버전을 넣지 않는다 | `.../bootstrap-icons@latest/icons/x.svg`는 내용이 바뀐다. `@1.13.2`로 고정한다. |
| CDN에서 받은 HTML을 `.svg`로 저장한다 | 404·SPA 응답은 `text/html`이다. `content-type`과 본문 `<svg`를 확인하고, `fetch-icons.sh`를 쓴다. |
| `<symbol>`에 `class="bi bi-x"`를 남긴다 | Bootstrap CSS가 없으면 무의미하고, 있으면 크기·색을 덮어쓴다. 제거한다. |
| `<symbol>`에 `width`/`height`를 남긴다 | `<use>`의 크기 지정이 무시된다. `viewBox`만 남긴다. |
| 16×16 아이콘을 48px로 확대한다 | 선이 상대적으로 가늘어져 흐릿하다. 24–32px를 쓰거나 노드를 줄인다. |
| 브랜드 아이콘을 일반 노드에 쓴다 | `github`, `slack`은 제품 노드용이다. 서버·클라우드 일반 노드에는 `server`, `cloud`를 쓴다. |
| 모든 아이콘에 `-fill` 짝이 있다 | 아니다. 739개는 채운 변형이 없다. 이름을 추측하지 말고 카탈로그에서 확인한다. |
| 정적 SVG에 `bi bi-*` 폰트 클래스를 쓴다 | 그 클래스는 웹폰트용이다. 파일 하나로 끝내려면 `<symbol>`+`<use>`로 인라인한다. |
| `href` 대신 `<image href="...svg">`로 원격 참조한다 | 파일을 옮기거나 오프라인에서 깨진다. 자기완결성을 위해 심볼로 넣는다. |

## 검증

```bash
# 내려받은 아이콘이 XML로 유효한지
xmllint --noout assets/bootstrap-icons/*.svg

# CDN이 SVG를 주는지 (Content-Type + 본문)
curl -fsSI "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.2/icons/database.svg" | grep -i '^content-type: image/svg+xml'
curl -fsSL "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.2/icons/database.svg" | grep -m1 '<svg'

# 스프라이트/최종 구조도의 XML 검증
xmllint --noout assets/bootstrap-sprite.svg
xmllint --noout diagram.svg
```

브라우저나 `qlmanage -t -s 1024 -o . diagram.svg`로 실제 렌더링을 확인한다. ImageMagick의 내장 SVG 렌더러는 path와 `currentColor` 상속을 정확히 처리하지 못하므로 판정 기준으로 쓰지 않는다. `fill` 누락·선 굵기·`<use>` 크기는 브라우저에서 확인한다.

## 스냅샷

이 카탈로그는 2026-11-12 기준 `bootstrap-icons@1.13.2` 스냅샷이다. 이름·카테고리·아이콘 수는 이 버전에 고정되어 있다.

버전을 올릴 때는 `build-catalog.sh`와 `fetch-icons.sh`의 `VERSION`을 함께 고치고 카탈로그를 다시 만든다.

```bash
SNAPSHOT=$(date +%F) bash skills/bootstrap-icons/scripts/build-catalog.sh skills/bootstrap-icons/references/icon-names.txt
head -1 skills/bootstrap-icons/references/icon-names.txt
```

`build-catalog.sh`는 고정된 npm 파일 목록과 사이트 `index.json`을 대조하므로, 새 버전이 실제로 배포하지 않는 이름은 카탈로그에 들어가지 않는다. 중요한 산출물이면 내려받은 SVG를 저장소에 커밋해 고정한다.
