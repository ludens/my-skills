#!/usr/bin/env bash
# Extract AWS Architecture Icon SVGs from the official Asset Package ZIP.
#
# AWS icons have no per-file URL; they ship inside one quarterly ZIP. This
# script caches that ZIP and pulls individual icons out of it.
#
# Usage:
#   bash fetch-icons.sh OUTPUT_DIR SLUG [SLUG...]   # extract by slug
#   bash fetch-icons.sh OUTPUT_DIR --list [PATTERN] # print matching paths
#   bash fetch-icons.sh OUTPUT_DIR --all            # every service icon at SIZE
#
# SLUG matches case-insensitively against the service name inside the ZIP.
# A slug that is ambiguous (e.g. "ec2" hits EC2, EC2-Auto-Scaling,
# EC2-Image-Builder) fails and lists the candidates; use the full name
# ("amazon-ec2", "aws-lambda") to extract an exact match.
#
# Env:
#   AWS_ICONS_URL        ZIP URL (default: 2025-07-31 Asset Package)
#   AWS_ICONS_CACHE_DIR  cache directory (default: ~/.cache/aws-icons)
#   AWS_ICONS_SIZE       size suffix: 16|32|48|64 (default: 48)

set -euo pipefail

URL="${AWS_ICONS_URL:-https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/architecture/approved/architecture-icons/Asset-Package_07312025.49d3aab7f9e6131e51ade8f7c6c8b961ee7d3bb1.zip}"
CACHE_DIR="${AWS_ICONS_CACHE_DIR:-$HOME/.cache/aws-icons}"
SIZE="${AWS_ICONS_SIZE:-48}"
ZIP="$CACHE_DIR/asset-package.zip"

usage() {
  sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'
  exit 2
}

[ "$#" -ge 2 ] || usage

OUT_DIR="$1"
shift

# Cache the ZIP once.
mkdir -p "$CACHE_DIR"
if [ ! -f "$ZIP" ]; then
  echo "Downloading asset package..." >&2
  curl -fsSL --retry 3 --retry-delay 2 "$URL" -o "$ZIP.tmp"
  mv "$ZIP.tmp" "$ZIP"
fi

# Enumerate SVG entries, skipping macOS junk.
entries() {
  unzip -Z1 "$ZIP" 2>/dev/null | grep '\.svg$' | grep -v '__MACOSX'
}

# Strip the "Arch_"/"Res_" prefix and "_<size>.svg" suffix from an icon
# basename. Group/category icons are returned unchanged.
service_name() {
  local b="$1"
  case "$b" in
    Arch_*_[0-9][0-9].svg|Arch_*_[0-9][0-9][0-9][0-9].svg|Res_*_[0-9][0-9].svg|Res_*_[0-9][0-9][0-9][0-9].svg)
      printf '%s' "$b" | sed -E 's/^(Arch|Res)_//; s/_[0-9]+\.svg$//' ;;
    *) printf '%s' "$b" ;;
  esac
}

# Lowercase and collapse "_" to "-" so resource names like
# "Elastic-Load-Balancing_Application-Load-Balancer" match a hyphenated slug.
normalize() {
  printf '%s' "$1" | tr '[:upper:]_' '[:lower:]-'
}

resolve() {
  # Resolve one slug to a single zip entry. Echoes the entry path or returns 1.
  local slug="$1" needle
  needle="$(normalize "$slug")"
  local cand=()
  while IFS= read -r e; do
    local b; b="$(basename "$e")"
    # Only consider the requested size for service icons.
    case "$b" in
      *_"$SIZE".svg) : ;;
      *) continue ;;
    esac
    local n; n="$(normalize "$(service_name "$b")")"
    case "$n" in
      *"$needle"*) cand+=("$e") ;;
    esac
  done < <(entries)

  [ "${#cand[@]}" -gt 0 ] || return 1

  if [ "${#cand[@]}" -gt 1 ]; then
    # Prefer an exact service-name match.
    local exact=()
    for e in "${cand[@]}"; do
      local b; b="$(basename "$e")"
      if [ "$(normalize "$(service_name "$b")")" = "$needle" ]; then
        exact+=("$e")
      fi
    done
    if [ "${#exact[@]}" -eq 1 ]; then
      printf '%s' "${exact[0]}"
      return 0
    fi
    printf '%s' "$(IFS=$'\n'; echo "${cand[*]}")" >&2
    return 2
  fi

  printf '%s' "${cand[0]}"
}

if [ "$1" = "--list" ]; then
  shift || true
  pat="${1:-}"
  while IFS= read -r e; do
    if [ -z "$pat" ]; then
      echo "$e"
    else
      case "$(printf '%s' "$e" | tr '[:upper:]' '[:lower:]')" in
        *"$(printf '%s' "$pat" | tr '[:upper:]' '[:lower:]')"*) echo "$e" ;;
      esac
    fi
  done < <(entries)
  exit 0
fi

if [ "$1" = "--all" ]; then
  shift || true
  mkdir -p "$OUT_DIR"
  count=0
  while IFS= read -r e; do
    local b; b="$(basename "$e")"
    case "$b" in
      Arch_*_"$SIZE".svg) : ;;
      *) continue ;;
    esac
    unzip -p "$ZIP" "$e" > "$OUT_DIR/$b"
    count=$((count + 1))
  done < <(entries)
  echo "Extracted $count service icons to $OUT_DIR"
  exit 0
fi

mkdir -p "$OUT_DIR"
ok=0
failed=()
for slug in "$@"; do
  rm -f /tmp/aws-icons-ambig
  if entry="$(resolve "$slug" 2>/tmp/aws-icons-ambig)"; then
    b="$(basename "$entry")"
    unzip -p "$ZIP" "$entry" > "$OUT_DIR/$b"
    ok=$((ok + 1))
  else
    if [ -s /tmp/aws-icons-ambig ]; then
      failed+=("$slug (ambiguous; candidates: $(tr '\n' ' ' < /tmp/aws-icons-ambig))")
      rm -f /tmp/aws-icons-ambig
    else
      failed+=("$slug (no match at size $SIZE)")
    fi
  fi
done

echo "Extracted $ok/${#@} icons to $OUT_DIR"

if [ "${#failed[@]}" -gt 0 ]; then
  echo "Failed:" >&2
  printf '  - %s\n' "${failed[@]}" >&2
  exit 1
fi
