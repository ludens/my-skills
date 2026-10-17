---
name: wp-site-health
description: Use when checking WordPress "사이트 건강" (Site Health) status from CLI, or when asked "사이트 건강 확인", "site health", "health check", "상태 점검". No wp-cli site-health command exists; this drives WP_Site_Health directly.
allowed-tools:
  - Bash
---

# wp-site-health

WordPress 사이트 전용. 관리자 `도구 → 사이트 건강` 화면과 동일한 체크를 wp-cli로 실행·요약.

`wp site health` 명령은 **없음**. `WP_Site_Health` 클래스 직접 호출.

사이트별 도메인·DB·런타임 제약은 해당 레포 `AGENTS.md`가 정본.

## 공통 셸 준비

```bash
# 사이트 루트 (미지정 시 현재 디렉터리)
WP_ROOT="${WP_ROOT:-$(pwd)}"
cd "$WP_ROOT"
command -v wp >/dev/null 2>&1 || { echo "wp-cli 미설치: https://wp-cli.org/#installing"; exit 1; }
wp() {
  php -d error_reporting='E_ALL & ~E_DEPRECATED' -d memory_limit=512M "$(which wp)" "$@"
}
```

WP-CLI 2.12 + PHP 8.5 deprecation 노이즈 치명 아님. `2>&1 | grep -viE 'deprecated|^$'` 붙이면 정리됨.

## Step 1: 총점 (good/recommended/critical)

```bash
wp cron event run wp_site_health_scheduled_check
wp transient get health-check-site-status-result
# → {"good":20,"recommended":5,"critical":1}
```

scheduled check가 모든 테스트 실행 후 transient에 카운트 저장.

**transient 빈 결과·만료 시:** `wp transient get`이 아무것도 안 주면 만료된 것. `wp cron event run wp_site_health_scheduled_check` 재실행 후 다시 get. 빈 결과를 "총점 0"으로 오독 금지.

## Step 2: 항목별 상세 (non-good만)

```bash
wp eval '
require_once ABSPATH . "wp-admin/includes/class-wp-site-health.php";
$sh = new WP_Site_Health();
foreach ( $sh->get_tests()["direct"] as $name => $test ) {
  $m = "get_test_" . $test["test"];                 // 콜백은 get_test_<slug> 메서드
  if ( ! method_exists($sh,$m) ) continue;
  $r = call_user_func( array($sh, $m) );
  if ( is_array($r) && isset($r["status"]) && $r["status"] !== "good" ) {
    echo strtoupper($r["status"]) . " | " . $test["label"] . "\n";
    if ( isset($r["description"]) ) echo "   " . strip_tags($r["description"]) . "\n";
  }
}'
```

async 테스트(loopback 등)는 위로 안 나옴. 필요 시 `$sh->get_tests()["async"]` 같은 방식.

## 요약 출력 형식

```
사이트 건강: good N · recommended N · critical N

CRITICAL:
- <label>: <원인·대응>

RECOMMENDED:
- <label>: <원인·대응>
```

## 함정 (이미 밟은 것)

- `WP_Site_Health::get_test_result()` **없음** → Fatal. 위 방식만 씀.
- test 콜백 원문은 `wordpress_version` 같은 slug. 메서드는 `get_test_wordpress_version` → `"get_test_" . $test["test"]` 필수.
- `call_user_func($test["test"])` → "function not found". 반드시 `array($sh, $m)`.

## 알려진 상태 (사이트별)

사이트마다 "의도된 critical/recommended"가 다름 (예: 의도적 WP_DEBUG_LOG, DISABLE_WP_CRON). 알려진 판정은 **스킬에 두지 말고** 해당 레포 `AGENTS.md`에 기록. 스킬은 raw 결과만 요약하고, 수용 여부 판단은 사이트 지식으로.
