#!/usr/bin/env python3
"""Build an SVG sprite of <symbol> blocks from downloaded Bootstrap Icons.

Usage:
  build-sprite.py --dir <svgdir> --out <file> <name...>
  build-sprite.py --dir <svgdir> --fragment <name...>

Each input is <svgdir>/<name>.svg. The outer <svg> element is replaced by
<symbol id="bi-<name>" viewBox="<svg viewBox>" fill="currentColor">, so the
sprite inherits no width, height or Bootstrap class from upstream. A name that
already starts with "bi-" is not prefixed again.

--out writes a complete file with an XML declaration and a <defs> wrapper. The
file is written to a temporary file first and moved into place with
os.replace(), so a failed run never leaves a partial sprite. --fragment prints
only the symbol blocks to stdout, for pasting into an existing <svg><defs>.

Missing or unparseable inputs are reported as "missing: <name>" or
"invalid: <name>" on stderr; the remaining names still produce output and the
run exits 1.

Exit: 0 when every name was converted, 1 when any name failed, 2 for a usage
error.
"""

import argparse
import os
import re
import sys
import tempfile
import textwrap
import xml.etree.ElementTree as ET

DEFAULT_VIEWBOX = "0 0 16 16"

DECL_RE = re.compile(r"^\s*<\?xml.*?\?>", re.S)
DOCTYPE_RE = re.compile(r"<!DOCTYPE[^>\[]*(\[[^\]]*\])?[^>]*>", re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
OPEN_SVG_RE = re.compile(r"<svg\b([^>]*)>", re.S)
VIEWBOX_RE = re.compile(r"""\bviewBox\s*=\s*["']([^"']*)["']""", re.I)


def symbol_id(name):
    return name if name.startswith("bi-") else "bi-" + name


def read_inner(path):
    """Return (viewBox, inner markup) for one icon SVG.

    Raises ValueError when the file is not a single <svg> element. ElementTree
    parses the text only to reject malformed XML; the inner markup is then cut
    out of the original text so it is not re-indented or re-serialized.
    """
    with open(path, encoding="utf-8") as f:
        text = f.read()

    ET.fromstring(text)

    text = DECL_RE.sub("", text, count=1)
    text = DOCTYPE_RE.sub("", text, count=1)
    text = COMMENT_RE.sub("", text)

    match = OPEN_SVG_RE.search(text)
    if not match:
        raise ValueError("no <svg> element")

    start = match.end()
    if text[match.start():start].rstrip().endswith("/>"):
        inner = ""
    else:
        end = text.rfind("</svg>")
        if end < start:
            raise ValueError("unclosed <svg> element")
        inner = text[start:end]

    viewbox = VIEWBOX_RE.search(match.group(1))
    return (viewbox.group(1) if viewbox else DEFAULT_VIEWBOX), inner.strip()


def render_symbol(name, viewbox, inner, indent):
    pad = " " * indent
    inner_pad = " " * (indent + 2)
    lines = [f'{pad}<symbol id="{symbol_id(name)}" viewBox="{viewbox}" fill="currentColor">']
    if inner:
        body = textwrap.indent(textwrap.dedent(inner), inner_pad)
        lines.append(body)
    lines.append(f"{pad}</symbol>")
    return "\n".join(lines)


def build_fragment(names, svgdir):
    blocks = []
    failed = 0
    for name in names:
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
        blocks.append(render_symbol(name, viewbox, inner, 0))
    return "\n".join(blocks), failed


def wrap_sprite(fragment):
    if not fragment:
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg"><defs>\n</defs></svg>\n'
        )
    indented = textwrap.indent(fragment, "  ")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg"><defs>\n'
        f"{indented}\n"
        "</defs></svg>\n"
    )


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

    fragment, failed = build_fragment(args.names, args.dir)

    if args.fragment:
        if fragment:
            print(fragment)
    else:
        write_atomic(args.out, wrap_sprite(fragment))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
