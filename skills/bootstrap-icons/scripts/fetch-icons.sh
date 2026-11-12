#!/usr/bin/env bash
# Download Bootstrap Icons SVGs into a directory.
#
# Usage:
#   bash fetch-icons.sh <outdir> <name...>
#   bash fetch-icons.sh <outdir> --all
#   bash fetch-icons.sh <outdir> --category <slug>
#   bash fetch-icons.sh --list
#
# Only names from references/icon-names.txt are accepted, so a typo or a name
# that the pinned release does not ship fails instead of saving an HTML error
# page. A response is written only when curl reports image/svg+xml and the body
# actually contains an <svg> element; downloads go to a temporary file first,
# so a failed fetch never leaves a partial or empty <name>.svg behind.
#
# Exit: 0 when every name was fetched or skipped, 1 when any fetch failed
# (including an unknown category), 2 for a usage error.

set -euo pipefail

VERSION="1.13.2"
BASE_URL="https://cdn.jsdelivr.net/npm/bootstrap-icons@${VERSION}/icons"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CATALOG="$SCRIPT_DIR/../references/icon-names.txt"

usage() {
  cat <<EOF
usage: fetch-icons.sh <outdir> <name...>
       fetch-icons.sh <outdir> --all
       fetch-icons.sh <outdir> --category <slug|name>
       fetch-icons.sh --list
EOF
}

# --retry-all-errors needs curl 7.71; macOS 11 ships 7.64.1 and rejects the
# flag outright, which would fail every fetch.
RETRY_ALL_ERRORS=""
curl_version="$(curl --version 2>/dev/null | awk 'NR == 1 { print $2 }')"
if [ -n "$curl_version" ] && awk -v v="$curl_version" 'BEGIN {
    split(v, p, ".")
    exit !(p[1] > 7 || (p[1] == 7 && p[2] >= 71))
  }'; then
  RETRY_ALL_ERRORS="--retry-all-errors"
fi

if [ ! -f "$CATALOG" ]; then
  echo "missing catalog: $CATALOG" >&2
  exit 2
fi

# Name lines only: drop the version header, category headers and blank lines.
names_of_catalog() {
  grep -v '^#' "$CATALOG" | grep -v '^[[:space:]]*$'
}

# Print the icons under one ## section. The section key is the display label
# lowercased with "&" expanded, so "Real world" and "real-world" both match.
names_of_category() {
  awk -v want="$1" '
    function key(s,   t) {
      t = tolower(s)
      gsub(/&/, " and ", t)
      gsub(/[^a-z0-9]+/, "-", t)
      gsub(/^-+|-+$/, "", t)
      return t
    }
    /^## / {
      label = substr($0, 4)
      sub(/ \([0-9]+\)$/, "", label)
      insec = (key(label) == want)
      next
    }
    /^#/ { next }
    $0 != "" && insec { print }
  ' "$CATALOG"
}

normalize_key() {
  printf '%s\n' "$1" | tr '[:upper:]' '[:lower:]' \
    | sed -e 's/&/ and /g' -e 's/[^a-z0-9][^a-z0-9]*/-/g' -e 's/^-//' -e 's/-$//'
}

for arg in "$@"; do
  case "$arg" in
    -h|--help)
      usage
      exit 0
      ;;
  esac
done

case "${1:-}" in
  --list)
    [ $# -eq 1 ] || { usage >&2; exit 2; }
    names_of_catalog
    exit 0
    ;;
  "")
    usage >&2
    exit 2
    ;;
esac

OUT_DIR="$1"
case "$OUT_DIR" in
  -*) usage >&2; exit 2 ;;
esac
shift
[ $# -gt 0 ] || { usage >&2; exit 2; }

TMP_DIR="$(mktemp -d)"
PART_FILE=""
cleanup() {
  rm -rf "$TMP_DIR"
  if [ -n "$PART_FILE" ]; then
    rm -f "$PART_FILE"
  fi
}
trap cleanup EXIT
trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

NAMES_FILE="$TMP_DIR/names"
FAILED_FILE="$TMP_DIR/failed"
names_of_catalog > "$NAMES_FILE"
: > "$FAILED_FILE"

mkdir -p -- "$OUT_DIR"

fetched=0
skipped=0

fetch_one() {
  name="$1"
  dest="$OUT_DIR/$name.svg"

  if [ -s "$dest" ] && grep -q '<svg' "$dest" 2>/dev/null; then
    echo "skip $name"
    skipped=$((skipped + 1))
    return 0
  fi

  part="$(mktemp "$OUT_DIR/.fetch.XXXXXX")"
  PART_FILE="$part"
  # stderr stays visible so a rejected flag, TLS or HTTP error is diagnosable.
  ctype="$(curl -fsSL --max-time 60 --retry 3 --retry-delay 2 $RETRY_ALL_ERRORS \
    -w '%{content_type}' -o "$part" "$BASE_URL/$name.svg")" || ctype=""
  ctype="${ctype%%;*}"

  if [ "$ctype" != "image/svg+xml" ] || ! grep -q '<svg' "$part" 2>/dev/null; then
    rm -f "$part"
    PART_FILE=""
    echo "$name" >> "$FAILED_FILE"
    return 0
  fi

  chmod 644 "$part"
  mv -f "$part" "$dest"
  PART_FILE=""
  fetched=$((fetched + 1))
}

case "$1" in
  --all)
    [ $# -eq 1 ] || { usage >&2; exit 2; }
    while IFS= read -r name; do
      fetch_one "$name"
    done < "$NAMES_FILE"
    ;;
  --category)
    [ $# -eq 2 ] || { usage >&2; exit 2; }
    key="$(normalize_key "$2")"
    list="$TMP_DIR/category"
    names_of_category "$key" > "$list"
    if [ ! -s "$list" ]; then
      echo "unknown category: $2" >&2
      exit 1
    fi
    while IFS= read -r name; do
      fetch_one "$name"
    done < "$list"
    ;;
  *)
    for name in "$@"; do
      if ! grep -qxF -- "$name" "$NAMES_FILE"; then
        echo "unknown icon: $name" >&2
        echo "$name" >> "$FAILED_FILE"
        continue
      fi
      fetch_one "$name"
    done
    ;;
esac

failed="$(wc -l < "$FAILED_FILE" | tr -d ' ')"
echo "fetched $fetched, skipped $skipped, failed $failed"

if [ "$failed" -gt 0 ]; then
  cat "$FAILED_FILE"
  exit 1
fi
