#!/usr/bin/env python3
"""Build an SVG sprite of <symbol> blocks from downloaded Bootstrap Icons.

Usage:
  build-sprite.py --dir <svgdir> --out <file> <name...>
  build-sprite.py --dir <svgdir> --fragment <name...>

Each input is <svgdir>/<name>.svg. Names are restricted to letters, digits,
"_" and "-", so a name can never reach outside --dir or break the id attribute.
The outer <svg> element is replaced by
<symbol id="bi-<name>" viewBox="<svg viewBox>" fill="currentColor">, so the
sprite inherits no width, height or Bootstrap class from upstream. A name that
already starts with "bi-" is not prefixed again, and a repeated name is emitted
once.

--out writes a complete file with an XML declaration and a <defs> wrapper. The
file is written to a temporary file first and moved into place with
os.replace(), so a failed run never leaves a partial sprite. --fragment prints
only the symbol blocks to stdout, for pasting into an existing <svg><defs>.

Invalid names, missing or unparseable inputs are reported as
"invalid name: <name>", "missing: <name>" or "invalid: <name>" on stderr; the
remaining names still produce output and the run exits 1. When every name
fails, an existing --out file is left untouched.

Inner markup runs to the last uncommented </svg>, so a nested <svg> or a
comment mentioning </svg> never truncates a symbol.

Exit: 0 when every name was converted, 1 when any name failed, 2 for a usage
error.
"""

import argparse
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET

DEFAULT_VIEWBOX = "0 0 16 16"

NAME_RE = re.compile(r"[A-Za-z0-9_-]+")
OPEN_SVG_RE = re.compile(r"<\s*svg\b", re.I)
CLOSE_SVG_RE = re.compile(r"</\s*svg\s*>", re.I)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
VIEWBOX_RE = re.compile(r"""\bviewBox\s*=\s*["']([^"']*)["']""", re.I)


def symbol_id(name):
    return name if name.startswith("bi-") else "bi-" + name


def mask_comments(text):
    """Blank out comment spans so tag searches cannot match inside a comment.

    The replacement is space-filled and the same length, so indices into the
    masked text are valid indices into the original.
    """
    return COMMENT_RE.sub(lambda m: " " * (m.end() - m.start()), text)


def scan_open_tag(text, masked):
    """Return (attributes, index after ">", self_closing) for the outer <svg>.

    index after ">" for the outer <svg>. Attributes are scanned by hand on
    the original text because a quoted value may contain ">", which a plain
    regular expression would treat as the end of the tag.
    """
    match = OPEN_SVG_RE.search(masked)
    if not match:
        raise ValueError("no <svg> element")

    i = match.end()
    quote = None
    while i < len(text):
        char = text[i]
        if quote:
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
        elif char == ">":
            return text[match.end():i], i + 1, text[i - 1] == "/"
        i += 1
    raise ValueError("unterminated <svg> tag")


def read_inner(path):
    """Return (viewBox, inner markup) for one icon SVG.

    Raises ValueError when the file is not a single <svg> element. ElementTree
    parses the text only to reject malformed XML; the inner markup is then cut
    out of the original text, so comments and whitespace inside the icon are
    preserved byte for byte.

    Inner markup runs to the last uncommented </svg>, so a comment mentioning
    </svg> or a nested <svg> cannot truncate a symbol.
    """
    with open(path, encoding="utf-8") as f:
        text = f.read()

    ET.fromstring(text)

    masked = mask_comments(text)
    attributes, inner_start, self_closing = scan_open_tag(text, masked)
    if self_closing:
        inner = ""
    else:
        closes = list(CLOSE_SVG_RE.finditer(masked, inner_start))
        if not closes:
            raise ValueError("unclosed <svg> element")
        inner = text[inner_start:closes[-1].start()]

    viewbox = VIEWBOX_RE.search(attributes)
    return (viewbox.group(1) if viewbox else DEFAULT_VIEWBOX), inner


def render_symbol(name, viewbox, inner, indent):
    """Render one <symbol>. Inner markup is emitted exactly as it was read."""
    pad = " " * indent
    body = ""
    if inner.strip():
        if not inner.startswith("\n"):
            body += "\n"
        body += inner
        if not body.endswith("\n"):
            body += "\n"
    head = f'{pad}<symbol id="{symbol_id(name)}" viewBox="{viewbox}" fill="currentColor">'
    return f"{head}{body}{pad}</symbol>\n"


def build_fragment(names, svgdir, indent):
    blocks = []
    failed = 0
    seen = set()
    for name in names:
        if name in seen:
            print(f"duplicate: {name}", file=sys.stderr)
            continue
        seen.add(name)

        if not NAME_RE.fullmatch(name):
            print(f"invalid name: {name}", file=sys.stderr)
            failed += 1
            continue

        path = os.path.join(svgdir, name + ".svg")
        if not os.path.isfile(path):
            print(f"missing: {name}", file=sys.stderr)
            failed += 1
            continue
        try:
            viewbox, inner = read_inner(path)
        except (ET.ParseError, ValueError, UnicodeDecodeError) as exc:
            print(f"invalid: {name}: {exc}", file=sys.stderr)
            failed += 1
            continue
        blocks.append(render_symbol(name, viewbox, inner, indent))
    return "".join(blocks), failed


def wrap_sprite(fragment):
    open_tag = '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg"><defs>\n'
    return open_tag + fragment + "</defs></svg>\n"


def write_atomic(path, data):
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".build-sprite.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(data)
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def main(argv):
    parser = argparse.ArgumentParser(
        description="Build an SVG sprite from downloaded Bootstrap Icons.",
    )
    parser.add_argument("--dir", required=True, metavar="SVGDIR", help="directory holding <name>.svg files")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--out", metavar="FILE", help="write a complete sprite file")
    mode.add_argument("--fragment", action="store_true", help="print symbol blocks to stdout")
    parser.add_argument("names", nargs="+", metavar="name", help="icon names")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.dir):
        print(f"not a directory: {args.dir}", file=sys.stderr)
        return 2

    if not args.fragment:
        if os.path.isdir(args.out):
            print(f"is a directory: {args.out}", file=sys.stderr)
            return 2
        out_dir = os.path.dirname(os.path.abspath(args.out))
        if not os.path.isdir(out_dir):
            print(f"not a directory: {out_dir}", file=sys.stderr)
            return 2

    fragment, failed = build_fragment(args.names, args.dir, 0 if args.fragment else 2)

    if failed and not fragment:
        return 1

    if args.fragment:
        print(fragment, end="")
    else:
        write_atomic(args.out, wrap_sprite(fragment))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
