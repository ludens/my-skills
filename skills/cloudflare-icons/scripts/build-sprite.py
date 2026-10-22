#!/usr/bin/env python3
"""Build an inline <symbol> sprite from downloaded Cloudflare icon SVGs.

Usage:
  python3 build-sprite.py --dir cloudflare-icons --out sprite.svg waf workers d1
  python3 build-sprite.py --dir cloudflare-icons --fragment waf workers d1
  python3 build-sprite.py --dir cloudflare-icons --out sprite.svg --all
  python3 build-sprite.py --dir cloudflare-icons --out logos.svg --no-fill logo logo-cloud

The output symbols use ids like ``cf-waf``. Paste the <symbol> block into a
diagram's <defs> and reference it with ``<use href="#cf-waf" width="48" height="48"/>``.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

XML_DECL = re.compile(r"^\s*<\?xml[^>]*\?>\s*", re.IGNORECASE)
OUTER_SVG = re.compile(r"^\s*<svg\b[^>]*>", re.IGNORECASE | re.DOTALL)
CLASS_ATTR = re.compile(r"\sclass=\"[^\"]*\"")
ID_ATTR = re.compile(r'\bid="([^"]+)"')
URL_REF = re.compile(r"url\(#([^)]+)\)")
HREF_REF = re.compile(r'\b(?:xlink:)?href="#([^"]+)"')


def extract(svg_text: str) -> tuple[str, str]:
    """Return (viewBox, inner markup) from a standalone SVG."""
    view_box_match = re.search(r'\bviewBox="([^"]+)"', svg_text)
    if not view_box_match:
        raise ValueError("missing viewBox")

    body = XML_DECL.sub("", svg_text, count=1)
    body = OUTER_SVG.sub("", body, count=1)
    body = re.sub(r"</svg>\s*$", "", body, count=1, flags=re.IGNORECASE)
    body = CLASS_ATTR.sub("", body)
    return view_box_match.group(1), body.strip()


def namespace_ids(body: str, slug: str) -> str:
    """Prefix local ids and references so multiple symbols can coexist."""
    ids = sorted(set(ID_ATTR.findall(body)), key=len, reverse=True)
    for local_id in ids:
        renamed = f"cf-{slug}__{local_id}"
        body = body.replace(f'id="{local_id}"', f'id="{renamed}"')
        body = URL_REF.sub(
            lambda m: f"url(#{renamed})" if m.group(1) == local_id else m.group(0),
            body,
        )
        body = HREF_REF.sub(
            lambda m: f'href="#{renamed}"' if m.group(1) == local_id else m.group(0),
            body,
        )

    # A few upstream files reference a clipPath id that they do not define
    # (for example web3.svg uses url(#a) with id="web3_svg__a"). Drop only
    # those dangling paint-server references; the icon still renders.
    defined = set(ID_ATTR.findall(body))
    body = re.sub(
        r'\s(?:clip-path|fill|stroke)="url\(#([^)]+)\)"',
        lambda m: m.group(0) if m.group(1) in defined else "",
        body,
    )
    return body


def build_symbol(path: Path, fill: str | None) -> str:
    slug = path.stem
    view_box, body = extract(path.read_text(encoding="utf-8"))
    body = namespace_ids(body, slug)
    fill_attr = f' fill="{fill}"' if fill else ""
    return f'  <symbol id="cf-{slug}" viewBox="{view_box}"{fill_attr}>\n{body}\n  </symbol>'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slugs", nargs="*", help="icon file stems (without .svg)")
    parser.add_argument("--dir", default="cloudflare-icons", help="directory containing <slug>.svg")
    parser.add_argument("--out", help="write output here instead of stdout")
    parser.add_argument("--fragment", action="store_true", help="emit only <symbol> elements")
    parser.add_argument("--all", action="store_true", help="use every .svg in --dir")
    parser.add_argument("--fill", default="#0051c3", help="default fill for service icons")
    parser.add_argument("--no-fill", action="store_true", help="keep each icon's own fills (logos)")
    args = parser.parse_args()

    icon_dir = Path(args.dir)
    if args.all:
        paths = sorted(icon_dir.glob("*.svg"))
    else:
        if not args.slugs:
            parser.error("provide at least one slug, or pass --all")
        paths = [icon_dir / f"{slug}.svg" for slug in args.slugs]

    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        print("Missing icon files:\n  " + "\n  ".join(missing), file=sys.stderr)
        return 1

    symbols = [build_symbol(path, None if args.no_fill else args.fill) for path in paths]
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
