#!/usr/bin/env python3
"""Build an inline <symbol> sprite from downloaded AWS Architecture Icons.

AWS service icons are colored tiles (a category-colored background rect plus a
white glyph); the colors are baked into each file, so this script keeps every
file's own fills instead of recoloring.

Usage:
  python3 build-sprite.py --dir assets/aws-icons --out sprite.svg \
      Arch_Amazon-EC2_48.svg Arch_Amazon-Simple-Storage-Service_48.svg
  python3 build-sprite.py --dir assets/aws-icons --fragment <files...>
  python3 build-sprite.py --dir assets/aws-icons --all --out sprite.svg

The output symbols use ids like ``aws-Arch_Amazon-EC2_48``. Paste the
<symbol> block into a diagram's <defs> and reference it with
``<use href="#aws-Arch_Amazon-EC2_48" width="48" height="48"/>``.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

XML_DECL = re.compile(r"^\s*<\?xml[^>]*\?>\s*", re.IGNORECASE)
OUTER_SVG = re.compile(r"^\s*<svg\b[^>]*>", re.IGNORECASE | re.DOTALL)
TITLE = re.compile(r"<title>.*?</title>", re.IGNORECASE | re.DOTALL)
ID_ATTR = re.compile(r'\bid="([^"]+)"')
URL_REF = re.compile(r"url\(#([^)]+)\)")
HREF_REF = re.compile(r'\b(?:xlink:)?href="#([^"]+)"')
CLIP_REF = re.compile(r'\s(?:clip-path|fill|stroke)="url\(#([^)]+)\)"')


def extract(svg_text: str) -> tuple[str, str]:
    """Return (viewBox, inner markup) from a standalone SVG."""
    view_box_match = re.search(r'\bviewBox="([^"]+)"', svg_text)
    if not view_box_match:
        raise ValueError("missing viewBox")

    body = XML_DECL.sub("", svg_text, count=1)
    body = OUTER_SVG.sub("", body, count=1)
    body = re.sub(r"</svg>\s*$", "", body, count=1, flags=re.IGNORECASE)
    body = TITLE.sub("", body)
    return view_box_match.group(1), body.strip()


def namespace_ids(body: str, slug: str) -> str:
    """Remove unreferenced label ids; rename referenced ids so symbols coexist.

    AWS files carry several label-only ids ("Rectangle", "Fill-1",
    "Icon-Architecture/48/...", "..._Squid") that are never referenced and
    collide when inlined. Only ids targeted by url(#...) / href="#..." (the
    clipPath ids in a handful of files) are real and must be kept unique.
    """
    referenced = set(URL_REF.findall(body)) | set(HREF_REF.findall(body))

    # Drop label-only ids.
    def drop_id(m: re.Match) -> str:
        return "" if m.group(1) not in referenced else m.group(0)

    body = ID_ATTR.sub(drop_id, body)

    # Rename the remaining referenced ids with a per-symbol prefix.
    for local_id in sorted(referenced, key=len, reverse=True):
        renamed = f"aws-{slug}__{local_id}"
        body = body.replace(f'id="{local_id}"', f'id="{renamed}"')
        body = URL_REF.sub(
            lambda m, lid=local_id, rid=renamed: f"url(#{rid})" if m.group(1) == lid else m.group(0),
            body,
        )
        body = HREF_REF.sub(
            lambda m, lid=local_id, rid=renamed: f'href="#{rid}"' if m.group(1) == lid else m.group(0),
            body,
        )

    # Drop any dangling paint-server references (target id was not defined).
    defined = set(ID_ATTR.findall(body))
    body = CLIP_REF.sub(
        lambda m: m.group(0) if m.group(1) in defined else "",
        body,
    )
    return body


def build_symbol(path: Path) -> str:
    slug = path.stem
    view_box, body = extract(path.read_text(encoding="utf-8"))
    body = namespace_ids(body, slug)
    return f'  <symbol id="aws-{slug}" viewBox="{view_box}">\n{body}\n  </symbol>'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="icon file names (with .svg)")
    parser.add_argument("--dir", default="assets/aws-icons", help="directory containing the SVGs")
    parser.add_argument("--out", help="write output here instead of stdout")
    parser.add_argument("--fragment", action="store_true", help="emit only <symbol> elements")
    parser.add_argument("--all", action="store_true", help="use every .svg in --dir")
    args = parser.parse_args()

    icon_dir = Path(args.dir)
    if args.all:
        paths = sorted(icon_dir.glob("*.svg"))
    else:
        if not args.files:
            parser.error("provide at least one file name, or pass --all")
        paths = [icon_dir / name for name in args.files]

    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        print("Missing icon files:\n  " + "\n  ".join(missing), file=sys.stderr)
        return 1

    symbols = [build_symbol(path) for path in paths]
    if args.fragment:
        output = "\n".join(symbols) + "\n"
    else:
        output = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0">\n'
            "  <defs>\n"
            + "\n".join(symbols)
            + "\n  </defs>\n</svg>\n"
        )

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {len(symbols)} symbols to {args.out}")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
