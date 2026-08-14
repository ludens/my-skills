#!/usr/bin/env python3
"""Render a Naver place page in Chromium and print weekly hours from the DOM."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

BROWSERS = (
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
)


def find_browser() -> str:
    for path in BROWSERS:
        if Path(path).is_file():
            return path
    raise SystemExit("browser not found: install Chromium or Chrome")


def dump_dom(place_id: str) -> str:
    url = f"https://pcmap.place.naver.com/place/{place_id}/home"
    browser = find_browser()
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        out = Path(tmp.name)
    try:
        proc = subprocess.run(
            [
                browser,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--virtual-time-budget=15000",
                "--timeout=20000",
                "--dump-dom",
                url,
            ],
            check=False,
            stdout=out.open("w"),
            stderr=subprocess.DEVNULL,
        )
        html = out.read_text("utf-8", errors="ignore")
    finally:
        out.unlink(missing_ok=True)
    if proc.returncode != 0 and not html.strip():
        raise SystemExit(f"browser dump failed: {proc.returncode}")
    return html


def extract_hours_blob(html: str):
    idx = html.find('"newBusinessHours')
    if idx < 0:
        raise SystemExit("no newBusinessHours in rendered DOM")
    start = html.find(":[", idx)
    if start < 0:
        raise SystemExit("could not parse hours JSON")
    raw = html[start + 1 :].replace(r"\/", "/")
    try:
        data, _ = json.JSONDecoder().raw_decode(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"could not parse hours JSON: {exc}") from exc
    return data


def fmt_range(item: dict | None) -> str:
    if not item:
        return ""
    return f"{item.get('start', '')}-{item.get('end', '')}"


def print_hours(data) -> None:
    blocks = data if isinstance(data, list) else [data]
    if blocks and isinstance(blocks[0], dict) and blocks[0].get("__typename") == "NewBusinessHour":
        hour = blocks[0]
        status = hour.get("businessStatusDescription") or {}
        if status.get("description") or status.get("status"):
            print(f"status: {status.get('status', '')} {status.get('description', '')}".strip())
        if hour.get("freeText"):
            print(f"note: {hour['freeText']}")
        days = hour.get("businessHours") or []
    else:
        days = blocks
    for day in days:
        if not isinstance(day, dict):
            continue
        name = day.get("day", "")
        hours = fmt_range(day.get("businessHours"))
        breaks = ", ".join(fmt_range(b) for b in day.get("breakHours") or [] if b)
        lasts = ", ".join(
            f"{x.get('time', '')}" for x in day.get("lastOrderTimes") or [] if x
        )
        parts = [hours] if hours else []
        if breaks:
            parts.append(f"브레이크 {breaks}")
        if lasts:
            parts.append(f"라스트오더 {lasts}")
        print(f"{name}: {' / '.join(parts) if parts else '없음'}")


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        raise SystemExit("usage: expand-hours.py <placeId>")
    print_hours(extract_hours_blob(dump_dom(sys.argv[1])))


if __name__ == "__main__":
    main()
