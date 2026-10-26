#!/usr/bin/env bash
# twemoji(https://github.com/jdecked/twemoji) 이모지 SVG를 내려받는다.
#
# Usage:
#   bash fetch-emoji.sh OUTPUT_DIR EMOJI [EMOJI...]   # 이모지별 SVG 추출
#   bash fetch-emoji.sh OUTPUT_DIR --list [CODEPOINT...] # 코드포인트 파일명 출력
#
# 파일명은 코드포인트(소문자 hex, 선행 0 없음)를 '-'로 연결한 값이다.
# 본문한 이모지는 U+FE0F(variation selector)를 제거한 이름을 먼저 시도하고,
# 404면 U+FE0F를 포함한 원본 이름으로 재시도한다.
# 404가 나도 전체를 중단하지 않고 실패 목록을 출력한 뒤 계속 진행한다.
# 받은 파일은 OUTPUT_DIR에 복사하기 전에 캐시 디렉터리에 저장된다.
#
# Env:
#   TWEMOJI_CACHE_DIR  캐시 디렉터리 (기본: ~/.cache/twemoji/17.0.3)

set -euo pipefail

VERSION="17.0.3"
CDN="https://cdn.jsdelivr.net/gh/jdecked/twemoji@${VERSION}/assets/svg"
FALLBACK="https://raw.githubusercontent.com/jdecked/twemoji/v${VERSION}/assets/svg"
CACHE_DIR="${TWEMOJI_CACHE_DIR:-$HOME/.cache/twemoji/${VERSION}}"

usage() {
  sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'
  exit 2
}

[ "$#" -ge 2 ] || usage

OUT_DIR="$1"
shift

# 이모지를 twemoji 파일명으로 변환한다. 이모지의 각 코드포인트를
# 소문자 hex로 바꾸어 '-'로 연결한다(ZWJ U+200D, 피부 톤 1f3fb-1f3ff 그대로 유지).
PYCODE='
import sys
s = sys.argv[1]
if not s:
    sys.exit(1)
print("-".join(format(ord(c), "x") for c in s))
print("-".join(format(ord(c), "x") for c in s if ord(c) != 0xFE0F))
'
emoji_to_name() {
  # 첫 줄: 원본(제거 없음), 둘째 줄: U+FE0F 제거본. 나머지는 실패로 처리.
  python3 -c "$PYCODE" "$1"
}

if [ "$1" = "--list" ]; then
  shift || true
  for cp in "$@"; do
    printf '%s.svg\n' "$cp"
  done
  exit 0
fi

mkdir -p "$OUT_DIR" "$CACHE_DIR"

# 한 URL에서 내려받는다. 실패(404 등)면 0이 아닌 값을 돌려준다.
fetch_url() {
  local url="$1" tmp="$2"
  # 임시 파일에 내려받는다. 실패(404 등)는 curl 메시지를 숨기고 0이 아닌
# 종료값으로만 알려 주고, 실패 목록 출력은 호출부가 맡는다.
curl -fsSL --retry 2 --retry-delay 1 --max-time 30 "$url" -o "$tmp" 2>/dev/null
}

ok=0
failed=()
for emoji in "$@"; do
  if ! names="$(emoji_to_name "$emoji")"; then
    failed+=("$emoji (변환 실패: 빈 입력)")
    continue
  fi
  full="${names%%$'\n'*}"
  stripped="${names##*$'\n'}"
  # U+FE0F 제거본을 우선 시도하고, 없는 경우 원본(fe0f 포함)으로 재시도한다.
  if [ "$stripped" != "$full" ]; then
    candidates=("$stripped" "$full")
  else
    candidates=("$stripped")
  fi

  got=""
  for name in "${candidates[@]}"; do
    cache_file="$CACHE_DIR/$name.svg"
    if [ -f "$cache_file" ]; then
      got="$name"
      break
    fi
    tmp="$cache_file.tmp"
    if fetch_url "$CDN/$name.svg" "$tmp" || fetch_url "$FALLBACK/$name.svg" "$tmp"; then
      mv "$tmp" "$cache_file"
      got="$name"
      break
    fi
    rm -f "$tmp"
  done

  if [ -n "$got" ]; then
    cp "$CACHE_DIR/$got.svg" "$OUT_DIR/$got.svg"
    ok=$((ok + 1))
  else
    tried="${candidates[*]}"
    failed+=("$emoji (404: 시도한 파일명: $tried)")
  fi
done

echo "Fetched $ok/${#@} emoji to $OUT_DIR"

if [ "${#failed[@]}" -gt 0 ]; then
  echo "Failed:" >&2
  printf '  - %s\n' "${failed[@]}" >&2
  exit 1
fi
