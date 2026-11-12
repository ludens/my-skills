#!/usr/bin/env bash
# Build the Bootstrap Icons name catalog from two upstream snapshots.
#
# Usage:
#   bash build-catalog.sh > references/icon-names.txt
#
# Names come from the pinned jsDelivr file listing of the npm package, so the
# catalog can never contain an icon that the pinned release does not ship.
# Categories come from the project site's index.json. Icons missing from the
# pinned release are dropped with a warning on stderr.
#
# Exits nonzero if either fetch fails.

set -euo pipefail

VERSION="1.13.2"
SNAPSHOT="2026-11-12"
NPM_URL="https://data.jsdelivr.com/v1/packages/npm/bootstrap-icons@${VERSION}?structure=flat"
SITE_URL="https://icons.getbootstrap.com/icons/index.json"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

curl -fsSL --retry 3 --retry-delay 2 "$NPM_URL" -o "$tmp/npm.json"
curl -fsSL --retry 3 --retry-delay 2 "$SITE_URL" -o "$tmp/site.json"

python3 - "$tmp/npm.json" "$tmp/site.json" "$VERSION" "$SNAPSHOT" <<'PY'
import json
import sys

npm_path, site_path, version, snapshot = sys.argv[1:5]

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
    if not slugs:
        uncategorized.append(name)
        print(f"warning: no category for {name}", file=sys.stderr)
    for slug in slugs:
        buckets[slug].append(name)

# Report pinned names the site does not know about; they stay uncategorized.
known = {e.get("n") for e in site}
for name in sorted(names - known):
    uncategorized.append(name)
    print(f"warning: no category for {name}", file=sys.stderr)

print(f"# bootstrap-icons {version} · {snapshot} · {len(names)} icons")

for slug in ORDER:
    items = sorted(set(buckets[slug]))
    if not items:
        continue
    print(f"## {LABEL[slug]} ({len(items)})")
    for name in items:
        print(name)

if uncategorized:
    items = sorted(set(uncategorized))
    print(f"## Uncategorized ({len(items)})")
    for name in items:
        print(name)
PY
