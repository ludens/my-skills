#!/usr/bin/env bash
# Build the Bootstrap Icons name catalog from two upstream snapshots.
#
# Usage:
#   bash build-catalog.sh [OUTPUT_FILE]
#
# With OUTPUT_FILE the catalog is written to a temporary file next to it and
# moved into place only after a successful build, so a failed run never leaves
# a partial or empty catalog. Without it the catalog goes to stdout.
#
# Names come from the pinned jsDelivr file listing of the npm package, so the
# catalog can never contain an icon that the pinned release does not ship.
# Categories come from the project site's index.json. Icons missing from the
# pinned release are dropped with a warning on stderr.
#
# Env:
#   SNAPSHOT  catalog date (default: today, `date +%F`)
#   NPM_URL   override the pinned npm file-listing URL
#   SITE_URL  override the site index.json URL
#
# Exits nonzero if either fetch fails.

set -euo pipefail

VERSION="1.13.2"
SNAPSHOT="${SNAPSHOT:-$(date +%F)}"
NPM_URL="${NPM_URL:-https://data.jsdelivr.com/v1/packages/npm/bootstrap-icons@${VERSION}?structure=flat}"
SITE_URL="${SITE_URL:-https://icons.getbootstrap.com/icons/index.json}"
EXPECTED_TOTAL=2078

out="${1:-}"
out_tmp=""

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"; [ -n "$out_tmp" ] && rm -f "$out_tmp"' EXIT

curl -fsSL --retry 3 --retry-delay 2 --retry-connrefused --retry-all-errors \
  --max-time 60 "$NPM_URL" -o "$tmp/npm.json"
curl -fsSL --retry 3 --retry-delay 2 --retry-connrefused --retry-all-errors \
  --max-time 60 "$SITE_URL" -o "$tmp/site.json"

generate() {
  python3 - "$tmp/npm.json" "$tmp/site.json" "$VERSION" "$SNAPSHOT" "$EXPECTED_TOTAL" <<'PY'
import json
import sys

npm_path, site_path, version, snapshot, expected = sys.argv[1:6]
expected = int(expected)

# Site navigation order, not alphabetical.
CATEGORIES = [
    ("alerts-and-status", "Alerts & Status"),
    ("apps", "Apps"),
    ("arrows", "Arrows"),
    ("badges", "Badges"),
    ("brand", "Brand"),
    ("buildings", "Buildings"),
    ("commerce", "Commerce"),
    ("communications", "Communications"),
    ("data", "Data"),
    ("date-and-time", "Date & Time"),
    ("devices", "Devices"),
    ("emoji", "Emoji"),
    ("entertainment", "Entertainment"),
    ("files-and-folders", "Files & Folders"),
    ("geo", "Geo"),
    ("graphics", "Graphics"),
    ("layout", "Layout"),
    ("media", "Media"),
    ("medical", "Medical"),
    ("people", "People"),
    ("real-world", "Real world"),
    ("security", "Security"),
    ("shapes", "Shapes"),
    ("tools", "Tools"),
    ("transportation", "Transportation"),
    ("travel", "Travel"),
    ("typography", "Typography"),
    ("ui-and-keyboard", "UI & Keyboard"),
    ("weather", "Weather"),
]
ORDER = [slug for slug, _ in CATEGORIES]
LABEL = dict(CATEGORIES)
RANK = {slug: i for i, slug in enumerate(ORDER)}

with open(npm_path, encoding="utf-8") as f:
    npm = json.load(f)

names = set()
for entry in npm.get("files", []):
    path = entry.get("name", "")
    if path.startswith("/icons/") and path.endswith(".svg"):
        names.add(path[len("/icons/"):-len(".svg")])

with open(site_path, encoding="utf-8") as f:
    site = json.load(f)

buckets = {slug: [] for slug in ORDER}
uncategorized = []

for entry in site:
    name = entry.get("n")
    if not name:
        continue
    if name not in names:
        print(f"warning: dropping {name}: not in bootstrap-icons {version}", file=sys.stderr)
        continue
    slugs = [s for s in (entry.get("c") or []) if s in buckets]
    if len(slugs) > 1:
        print(f"warning: {name} lists {len(slugs)} categories, using {slugs[0]}", file=sys.stderr)
    if not slugs:
        uncategorized.append(name)
        print(f"warning: no category for {name}", file=sys.stderr)
        continue
    # One bucket per name keeps the catalog free of duplicate lines.
    buckets[min(slugs, key=RANK.__getitem__)].append(name)

# Report pinned names the site does not know about; they stay uncategorized.
known = {e.get("n") for e in site}
for name in sorted(names - known):
    uncategorized.append(name)
    print(f"warning: no category for {name}", file=sys.stderr)

total = 0
sections = []
for slug in ORDER:
    items = sorted(buckets[slug])
    if not items:
        print(f"warning: known category {slug} is empty", file=sys.stderr)
        continue
    total += len(items)
    sections.append((LABEL[slug], items))

if uncategorized:
    items = sorted(set(uncategorized))
    total += len(items)
    sections.append(("Uncategorized", items))

if total != expected:
    print(f"warning: catalog has {total} icons, expected {expected}", file=sys.stderr)

print(f"# bootstrap-icons {version} · {snapshot} · {len(names)} icons")
for label, items in sections:
    print(f"## {label} ({len(items)})")
    for name in items:
        print(name)
PY
}

if [ -n "$out" ]; then
  mkdir -p "$(dirname "$out")"
  out_tmp="$(mktemp "$out.XXXXXX")"
  generate > "$out_tmp"
  mv -f "$out_tmp" "$out"
  out_tmp=""
else
  generate
fi
