---
name: cloudflare-icons
description: Cloudflare 서비스가 포함된 구조도·아키텍처 다이어그램을 그릴 때, 또는 Cloudflare 서비스 아이콘의 slug·SVG URL·다운로드·삽입 방법이 필요할 때 사용합니다. WAF, Workers, R2, D1, Zero Trust, Magic Transit 같은 공식 서비스 아이콘을 찾는 경우를 포함합니다.
---

# Cloudflare Icons

Cloudflare 서비스 아이콘을 찾고, 내려받고, SVG 구조도에 삽입할 때 참조하는 카탈로그.

## 소스

| 항목 | 값 |
| --- | --- |
| 아이콘 URL | `https://cf-icons.pages.dev/<slug>.svg` |
| 라이브러리 | <https://cf-icons.pages.dev/> |
| 원본 패키지 | `@cloudflare/component-icon`, `@cloudflare/component-logo` |
| 미러 저장소 | <https://github.com/kyouheicf/cf-icons> |
| 공식 문서 대체 경로 | `https://raw.githubusercontent.com/cloudflare/cloudflare-docs/production/src/icons/<slug>.svg` |

서비스 아이콘 78개, 구조도 기호·Zero Trust·디바이스·로고 29개. 전체 목록과 `viewBox`는 [references/icon-catalog.md](references/icon-catalog.md)에 있다.

같은 URL 패턴으로 접근되는 컴포넌트 아이콘도 있다. `cloudflare-access`, `gateway`, `teams`, `dlp`, `cloudflare-zero-trust`, `workers-kv`, `server-origin`처럼 구조도에 유용한 것이 포함된다. 전체 선별 목록은 카탈로그의 "추가 컴포넌트 아이콘"에 있다. `add`, `edit`, `search` 같은 UI 아이콘은 구조도에 쓰지 않는다.

## 빠른 선택

| 구조도 노드 | slug |
| --- | --- |
| 인터넷 / 사용자 | `internet-globe`, `cloud-internet` |
| 기업·지사 | `office-headquarters` |
| 라우터 | `router` |
| DNS | `dns` |
| WAF | `waf` |
| DDoS 보호 | `ddos-protection` |
| SSL/TLS | `ssl` |
| 로드 밸런서 | `load-balancing` |
| 대기실 | `waiting-room` |
| API Shield | `api-shield` |
| Bot Management | `bots` |
| Turnstile | `turnstile` |
| Workers | `workers` |
| Workers AI | `workers-ai` |
| Pages | `pages` |
| Durable Objects | `durable-objects` |
| Queues | `queues` |
| Pub/Sub | `pub-sub` |
| R2 | `r2` |
| D1 | `d1` |
| Workers KV | `kv` |
| Hyperdrive | `hyperdrive` |
| Vectorize | `vectorize` |
| AI Gateway | `ai-gateway` |
| Images | `images` |
| Stream | `stream` |
| Cloudflare One | `cloudflare-one` |
| WARP Client | `warp-client` |
| cloudflared | `Cloudflared` |
| Zero Trust | `ZeroTrustLogo` |
| Magic Transit | `magic-transit` |
| Magic WAN | `magic-wan` |
| Magic Firewall | `magic-firewall` |
| Spectrum | `spectrum` |
| Network Interconnect | `network-interconnect` |
| Analytics | `analytics` |
| Logs | `logs` |
| Radar | `radar` |
| Registrar | `registrar` |
| Terraform | `terraform` |
| Pulumi | `pulumi` |

서비스 아이콘과 브랜드 로고를 섞지 않는다. `logo`, `logo-inline`, `logo-cloud`는 "Cloudflare" 브랜드 표기용이고, 서비스 노드에는 쓰지 않는다.

선택 기준:

- 최종 사용자·클라이언트는 `internet-globe`. 인터넷 경계나 추상적인 "인터넷"은 `cloud-internet`.
- 외부 서드파티 시스템에는 Cloudflare 아이콘을 쓰지 않는다. 중립적인 서버/클라우드 도형을 그린다.
- DNS/WAF처럼 한 단계에 여러 제품이 있으면 아이콘을 겹치지 말고, 제품별 노드를 나란히 두거나 대표 아이콘 하나만 쓴다.
- `ZeroTrustLogo`는 브랜드 워드마크다. 제품 노드에는 `cloudflare-one`, `cloudflare-access`, `gateway` 등을 쓴다.

## 모양 메모

| slug | 실제 모양 |
| --- | --- |
| `dns` | 조직도/토폴로지 트리 |
| `waf` | 벽돌 벽 |
| `workers` | 겹친 화살표(chevron) 다이아몬드 |
| `d1` | 줄무늬가 있는 데이터베이스 실린더 |
| `r2` | 데이터베이스 실린더 |
| `magic-transit` | 별표가 들어간 방패 |
| `hyperdrive` | 로켓 |
| `api-shield` | 열쇠 구멍이 있는 방패 |
| `cloudflare-one` | 오른쪽 화살표가 들어간 방패 |
| `turnstile` | 회전 화살표와 체크 |
| `queues` | 좌우 화살표가 붙은 막대 더미 |
| `analytics` | 원형 차트 |
| `internet-globe` | 경선이 있는 지구본 |
| `cloud-internet` | 구름 윤곽 |
| `server-database` | 서버 랙 |
| `router` | 화살표가 있는 라우터 상자 |

## 다운로드

```bash
# 하나
curl -fsSL "https://cf-icons.pages.dev/waf.svg" -o waf.svg

# 여러 개
bash scripts/fetch-icons.sh assets/cloudflare-icons dns waf workers d1 r2

# 전체 서비스 아이콘 78개
bash scripts/fetch-icons.sh assets/cloudflare-icons --all

# 구조도 기호·Zero Trust·로고 29개
bash scripts/fetch-icons.sh assets/cloudflare-icons --extras

# 선별 컴포넌트 아이콘
bash scripts/fetch-icons.sh assets/cloudflare-icons --components

# 위 전부
bash scripts/fetch-icons.sh assets/cloudflare-icons --everything
```

`fetch-icons.sh`는 실패한 slug를 모아 마지막에 보고하고, 200 HTML(SPA fallback)을 SVG로 저장하지 않는다. 존재하지 않는 slug는 보통 `404 text/plain`, 알 수 없는 경로는 `200 text/html`이다. 어느 쪽이든 `image/svg+xml`이 아니면 실패로 취급한다.

### 전체 다운로드에 관한 사실

- `https://cf-icons.pages.dev/fde7d32d-a0d7-4306-9d20-95de6da5404a` 같은 UUID 경로는 정적 ZIP이 아니다. SPA의 `blob:` 다운로드 흔적이거나 임의 경로이며, `200 text/html`로 index.html을 돌려준다.
- 사이트의 **Save All SVG as ZIP** 버튼은 브라우저에서 JSZip으로 만든다. 이 ZIP에는 UI/컴포넌트 아이콘 161개가 들어 있고, 서비스 아이콘 78개 중 61개가 빠진다. 대신 `cloudflare-access`, `gateway`, `teams`, `dlp` 같은 유용한 컴포넌트 아이콘은 들어 있다. 서비스 아이콘 전체가 필요하면 `--all`을 쓴다.
- GitHub 저장소의 `src/data/*.svg`를 그대로 복사하지 않는다. 일부 파일이 비어 있다(`hyperdrive.svg` 등). 배포된 `<slug>.svg` URL이 기준이다.

## SVG에 삽입

최종 구조도는 자기완결적이어야 한다. 아이콘을 원격 URL로 참조하지 말고, SVG 안에 심볼로 넣는다.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 160">
  <defs>
    <!-- waf.svg의 <?xml?>, 바깥 <svg>, class 속성을 제거한 내부 -->
    <symbol id="cf-waf" viewBox="0 0 48 49" fill="#0051c3">
      <path d="..."/>
    </symbol>
  </defs>

  <rect x="30" y="45" width="120" height="80" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>
  <use href="#cf-waf" x="52" y="63" width="48" height="48"/>
  <text x="120" y="92" font-size="12" text-anchor="middle" fill="#334155">WAF</text>
</svg>
```

삽입 규칙:

1. 바깥 `<svg>`의 `viewBox`를 `<symbol viewBox="...">`로 옮긴다.
2. 바깥 `<svg>`의 `fill="#0051c3"`은 내부 요소로 상속되지 않는다. `<symbol>`이나 `<use>`에 `fill`을 지정한다.
3. `<use>`에 `width`/`height`를 주고, 아이콘은 48×48 슬롯에 맞춘다. `viewBox`가 정사각형이 아니어도 기본 `preserveAspectRatio="xMidYMid meet"`가 비율을 지킨다.
4. `id`/`url(#...)`가 있는 아이콘은 심볼마다 접두사를 붙인다. `cloud-internet`의 `clipPath id="a"`가 대표적이다. `web3`는 원본에 정의되지 않은 `url(#a)`가 있으므로 스크립트가 dangling 참조를 제거한다.
5. `class="c_a ..."`는 사이트 전용 스타일이므로 제거한다. 남기면 문서의 CSS와 충돌할 수 있다.
6. 기본은 `href`만 쓴다. 구형 렌더러를 지원해야 할 때만 `xmlns:xlink`와 `xlink:href`를 함께 넣는다.

심볼 생성은 스크립트로 처리할 수 있다.

```bash
python3 scripts/build-sprite.py --dir assets/cloudflare-icons \
  --out assets/cloudflare-sprite.svg waf workers d1 r2

# <symbol> 블록만 출력해 기존 <defs>에 붙이기
python3 scripts/build-sprite.py --dir assets/cloudflare-icons --fragment waf workers d1 r2
```

단일 파일로만 배포해야 하고 수정 가능성이 없으면 `data:image/svg+xml;base64,...`를 `<image href="...">`에 넣는 방법도 있다. 다만 재색칠·검색·유지보수가 어려우므로 기본은 심볼이다.

## 배치

- 아이콘은 32–48px. 같은 구조도 안에서 크기를 통일한다.
- 아이콘만 두지 말고 서비스명을 함께 적는다. `workers`와 `workers-ai`, `api`와 `api-shield`는 아이콘만으로 구분하기 어렵다.
- 기본 색은 Cloudflare blue `#0051c3`. 어두운 배경이나 대비가 필요하면 orange `#F6821F`를 쓴다. 로고와 디바이스 아이콘은 원래 색을 유지한다.
- 엣지·코어·데이터 계층은 점선 그룹 박스로 묶고, 아이콘은 박스 안 노드에 둔다.
- 화살표가 아이콘을 관통하지 않게 한다. 아이콘과 텍스트 사이는 8–12px.
- 기본 타이포: 제품명 12–13px, 보조 설명 10–11px. 아이콘 48px, 라벨이 두 줄이면 노드 높이를 90px 이상으로 잡는다.
- 16×16 컴포넌트 아이콘(`cloudflare-access` 등)은 선이 얇아 48px에서 가볍게 보인다. 같은 행에 48/64 기반 아이콘이 있으면 40px로 낮추거나 64×64 변형을 쓴다.

## 자주 틀리는 것

| 오해·증상 | 실제 |
| --- | --- |
| UUID 링크가 전체 ZIP이다 | SPA fallback HTML이다. `content-type`을 확인한다. |
| Save All ZIP에 모든 서비스 아이콘이 있다 | UI 아이콘 161개만 있고 서비스 아이콘 다수가 빠진다. |
| 모든 아이콘이 48×48이다 | `r2`, `d1`, `magic-transit`은 16×16, `hyperdrive`는 64×65, `cloudflare-for-platforms`는 192×192다. `viewBox`를 읽는다. |
| `api`를 API Shield로 쓴다 | API Shield는 `api-shield`다. |
| `pages-logo`를 Pages 서비스로 쓴다 | Pages 서비스는 `pages`, `pages-logo`는 로고다. |
| `warp-client`가 WARP Connector다 | WARP Connector는 `WarpConnector`다. |
| slug는 모두 소문자다 | `Cloudflared`, `ZeroTrustLogo`, `Onetimepin`, `WarpConnector`, 디바이스 아이콘은 PascalCase다. |
| 200이면 성공이다 | `text/html`이면 SPA fallback이다. 존재하지 않는 slug는 `404 text/plain`일 수도 있다. `image/svg+xml`과 `<svg`를 확인한다. |

## 검증

```bash
# Content-Type 확인
curl -fsSI "https://cf-icons.pages.dev/waf.svg" | grep -i '^content-type: image/svg+xml'

# SVG 본문 확인
curl -fsSL "https://cf-icons.pages.dev/waf.svg" | grep -m1 '<svg'

# 결과 구조도 XML 검증
xmllint --noout diagram.svg
```

브라우저나 `qlmanage`로 실제 렌더링을 확인한다. ImageMagick의 내장 SVG 렌더러는 일부 path와 폰트를 처리하지 못하므로 판정 기준으로 쓰지 않는다.

이 카탈로그는 2026-10 스냅샷이다. URL에 버전 해시가 없어 아이콘 내용은 바뀔 수 있다. 중요한 산출물이면 내려받은 SVG를 저장소에 커밋해 고정한다.
