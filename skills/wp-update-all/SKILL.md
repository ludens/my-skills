---
name: wp-update-all
description: Use when updating WordPress core, plugins, themes, or translations to their latest versions via WP-CLI. Triggers include "워드프레스 업데이트", "코어 업데이트", "core update", "플러그인/테마 최신화", "번역 업데이트", "다 업데이트해줘".
allowed-tools:
  - Bash
---

# wp-update-all

WordPress 사이트 전용. WP core / plugin / theme / translation 전체 최신화.

도메인·DB·런타임 제약은 레포 `AGENTS.md`가 정본.

## When to use

- "워드프레스 업데이트", "core 업데이트", "전부 최신화"
- `wp core check-update`에 남은 버전이 보일 때
- "번역 업데이트", "플러그인/테마 업데이트"

## When NOT to use

- WP 코어 아닌 단일 글/옵션 편집 → `wp-cli` 스킬
- 다국어 글 번역 발행 → `translate-wp-post` 스킬
- 업그레이드 없이 상태만 확인 → 그냥 `wp core check-update`

## 고정 업데이트 순서

```
1. core minor  (현재 major 내 최신 패치)
2. core major  (다음 major)
3. plugin      (--all)
4. theme       (--all)
5. core-translation
6. plugin-translation
7. theme-translation
```

core 업데이트 **각 단계 전** 백업, **후** 검증. plugin/theme/번역은 백업 불필요(DB·코어 이미 백업됨).

## 공통 셸 준비

```bash
set -euo pipefail
WP_ROOT="${WP_ROOT:-$(pwd)}"
cd "$WP_ROOT"
command -v wp >/dev/null 2>&1 || { echo "wp-cli 미설치: https://wp-cli.org/#installing"; exit 1; }
command -v mysql >/dev/null 2>&1 || echo "경고: mysql client 없음 — wp db * 사용 시 필요"
WP_LOCALE="${WP_LOCALE:-}"   # 비어있으면 사이트 기본 로케일

wp() {
  php -d error_reporting='E_ALL & ~E_DEPRECATED' -d memory_limit=512M "$(which wp)" "$@"
}
```

WP-CLI 2.12 + PHP 8.5 deprecation 노이즈는 치명 아님. 출력이 지저분하면 `2>&1 | grep -viE 'deprecated|^$'` 붙임.

## Step 0: 사전 확인

```bash
wp core version                       # 현재 버전
wp core check-update --format=table   # version / update_type (minor|major)
wp maintenance-mode status            # 업데이트 전 inactive 확인
```

`check-update`에서 `update_type`으로 minor/major 식별. minor 있으면 1단계, 없으면 2단계로 건너뜀.

## Step 1: core minor 업데이트

### 백업

```bash
RUN_TS=$(date +%Y%m%d-%H%M%S)
mkdir -p "$HOME/wp-backups"
DB_BACKUP="$HOME/wp-backups/wp-db-$RUN_TS.sql"
CORE_BACKUP="$HOME/wp-backups/wp-core-$RUN_TS.tar.gz"

wp db export "$DB_BACKUP"
tar -czf "$CORE_BACKUP" \
  --exclude='wp-content' \
  --exclude='.git' \
  --exclude='.env' \
  --exclude='wp-config.php' \
  .

# 백업 검증
test -s "$DB_BACKUP" && echo "db ok: $(du -h "$DB_BACKUP" | cut -f1)"
grep -c "CREATE TABLE" "$DB_BACKUP"
tar -tzf "$CORE_BACKUP" | grep -E '^\./(wp-admin|wp-includes)/' | head -3
```

### 업데이트

```bash
wp maintenance-mode activate

# minor는 정확한 패치 버전으로 고정 (check-update의 minor version 값)
wp core update --version=<minor-version> ${WP_LOCALE:+--locale=$WP_LOCALE}

wp core update-db
wp rewrite flush
# PHP-FPM 재시작 (opcache 갱신). 환경별: brew services restart php / systemctl restart php-fpm / docker restart <컨테이너>
wp maintenance-mode deactivate || true   # core update가 이미 해제했으면 "already deactivated" → 무시
```

### 검증 (통과해야 다음 단계)

```bash
wp core version                      # 기대: 업데이트한 minor 버전
wp core verify-checksums ${WP_LOCALE:+--locale=$WP_LOCALE}
wp db query "SELECT 1"

# 공개 URL 기준 확인. 로컬 origin만 점검하려면 --resolve 분기 사용.
SITE_URL="$(wp option get home)"
curl -sS -L -o /tmp/wp-upd-home.html -w 'home:%{http_code}\n' "$SITE_URL"
grep -q '<html' /tmp/wp-upd-home.html \
  && echo "homepage html ok" \
  || { echo "homepage html 없음 — 확인 필요"; exit 1; }

test -f wp-content/debug.log \
  && tail -n 150 wp-content/debug.log | grep -E 'Fatal error|Parse error|WordPress database error' \
  || echo "no new fatal/db errors (debug.log 없음)"
```

검증 실패 시: 직전 `CORE_BACKUP`/`DB_BACKUP`으로 롤백.

```bash
wp db import "$DB_BACKUP"
tar -xzf "$CORE_BACKUP" -C "$WP_ROOT"
# PHP-FPM 재시작 (환경별)
wp maintenance-mode deactivate || true
```

## Step 2: core major 업데이트

Step 1과 동일하되 `--version`을 major로 고정하고, **백업은 다시** 새로 만든다 (major 직전 스냅샷 = 롤백 지점).

```bash
wp core update --version=<major-version> ${WP_LOCALE:+--locale=$WP_LOCALE}
```

이후 `update-db` → `rewrite flush` → PHP-FPM 재시작 → 검증은 Step 1 동일.

## Step 3: plugin

```bash
wp plugin update --all
wp plugin list --fields=name,status,update,version --format=table
```

## Step 4: theme

```bash
wp theme update --all
wp theme list --fields=name,status,update,version --format=table
```

비활성 기본 테마 삭제했다면 코어 업데이트 때 자동 재설치됨. 유지하려면 업데이트 후 재삭제.

## Step 5–7: translation (core → plugin → theme 순서 고정)

```bash
wp language core update
wp language plugin update --all
wp language theme update --all
```

## 최종 검증: 남은 업데이트 없음

```bash
wp core check-update                 # "at the latest version"
wp plugin list --fields=name,update --format=table
wp theme list --fields=name,update --format=table
wp language core update --dry-run    # "up to date"
wp language plugin update --all --dry-run
wp language theme update --all --dry-run
```

모두 `update: none` / "up to date" / "at the latest version" 이어야 완료. 하나라도 남으면 해당 단계 재실행.

## Troubleshooting

- **`core update` lock**: `Error: Another update is currently in progress.` → `wp option delete core_updater.lock` 후 재실행.
- **verify-checksums 경고 `File should not exist: ...`**: 코어 외 잔여 파일. 정식 파일 존재 확인 후 잔여 파일 삭제, 재확인.
  ```bash
  wp core verify-checksums ${WP_LOCALE:+--locale=$WP_LOCALE}
  ```
- **`wp db query` auth 에러 (`mysql_native_password`)** = `mysql` 클라이언트 없거나 버전 불일치. PATH에 mysql client 확인.
- **`wp-login.php` 302** = HTTPS 강제 리다이렉트일 수 있음(정상). 사이트 HTTPS 정책 확인.
- **object cache**: drop-in 있으면 `wp cache flush` (`test -f wp-content/object-cache.php`). 없으면 생략.
- **번역 남는 것처럼 보임**: `wp language * list --all`의 `update` 컬럼 기준. `uninstalled` 행은 무시(미설치 언어).
