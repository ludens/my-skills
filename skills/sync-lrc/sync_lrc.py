#!/usr/bin/env python3
"""오디오 옆에 Navidrome 사이드카 .lrc 파일을 만든다.

LRCLIB나 사용자가 준 가사를 그대로 옮겨 적기만 한다.
전사, 강제 정렬, 타임스탬프 생성은 하지 않는다.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

FFPROBE = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"
API = "https://lrclib.net/api"
USER_AGENT = "sync-lrc/1.0 (https://github.com/ludens/my-skills)"
TIME_TAG = re.compile(r"\[(\d{1,3}):(\d{2})(?:[.:](\d{1,3}))?\]")


def die(code, message):
    print(message, file=sys.stderr)
    sys.exit(code)


def probe(audio):
    """ffprobe로 태그와 길이를 읽는다. 태그가 없으면 파일명에서 유추한다."""
    try:
        raw = subprocess.run(
            [FFPROBE, "-v", "quiet", "-print_format", "json", "-show_format", str(audio)],
            capture_output=True, text=True, check=True,
        ).stdout
        fmt = json.loads(raw)["format"]
    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError) as exc:
        die(1, f"ffprobe 실패: {audio}: {exc}")

    tags = {key.lower(): value for key, value in (fmt.get("tags") or {}).items()}
    title, artist = tags.get("title"), tags.get("artist")
    if not title or not artist:
        parts = Path(audio).stem.split(" - ", 1)
        if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
            die(1, f"제목/아티스트 태그가 없고 파일명도 'Artist - Title' 형식이 아님: {audio.name}")
        artist = artist or parts[0].strip()
        title = title or parts[1].strip()

    duration = fmt.get("duration")
    if not duration:
        die(1, f"ffprobe 결과에 duration이 없음: {audio}")
    return {"title": title, "artist": artist, "album": tags.get("album"),
            "duration": float(duration)}


def fetch_json(url, warnings):
    """LRCLIB GET. 404는 정상적인 '없음', 그 외 오류는 1회 재시도 후 포기."""
    error = None
    for attempt in (0, 1):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=20) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            error = f"HTTP {exc.code}"
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            error = str(exc)
        if attempt == 0:
            time.sleep(2)
    warnings.append(f"LRCLIB 요청 실패({error})")
    return None


def timestamps(line):
    """줄 앞에 붙은 모든 [mm:ss.xx] 타임스탬프를 밀리초로 변환한다."""
    found, position = [], 0
    while match := TIME_TAG.match(line, position):
        minute, second, fraction = match.group(1), match.group(2), match.group(3) or ""
        ms = int(minute) * 60000 + int(second) * 1000 + int(fraction.ljust(3, "0")[:3])
        found.append(ms)
        position = match.end()
    return found


def validate(text, duration):
    """(위반 줄 또는 None, 마지막 타임스탬프 ms, 타임스탬프 있는 줄 수)"""
    previous, counted, last, bad_line = -1, 0, None, None
    for line in text.splitlines():
        marks = timestamps(line)
        if not marks:
            continue
        counted += 1
        for mark in marks:
            if mark < previous:
                return line, None, counted
            previous = mark
            last = mark
    if last is not None and last > (duration + 1.0) * 1000:
        return "<마지막 타임스탬프>", last, counted
    return None, last, counted


def pick_search_result(hits, duration):
    """길이가 ±2.0초 안에 드는 첫 결과를 고르고, 동기화 가사를 우선한다."""
    near = [hit for hit in hits or []
            if hit.get("duration") and abs(float(hit["duration"]) - duration) <= 2.0]
    for key in ("syncedLyrics", "plainLyrics"):
        for hit in near:
            if hit.get(key):
                return hit
    return near[0] if near else None


def main():
    parser = argparse.ArgumentParser(description="LRCLIB 가사로 사이드카 .lrc 생성")
    parser.add_argument("audio_path")
    parser.add_argument("--lyrics", help="직접 준비한 가사 파일 (LRCLIB보다 우선)")
    parser.add_argument("--out", help="출력 .lrc 경로")
    args = parser.parse_args()

    audio = Path(args.audio_path)
    if not audio.is_file():
        die(1, f"오디오 파일 없음: {audio}")
    meta = probe(audio)
    duration = meta["duration"]
    warnings = []
    record, source, text = None, None, None

    if args.lyrics:
        try:
            text = Path(args.lyrics).read_text(encoding="utf-8-sig")
        except OSError as exc:
            die(1, f"가사 파일 읽기 실패: {exc}")
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        if not TIME_TAG.search(text):
            die(2, "가사 파일에 타임스탬프가 없음. 타이밍을 지어내지 않으므로 저장하지 않는다.")
        source = "local-file-synced"
    else:
        params = {"track_name": meta["title"], "artist_name": meta["artist"],
                  "duration": str(round(duration))}
        if meta["album"]:
            params["album_name"] = meta["album"]
        record = fetch_json(f"{API}/get?{urllib.parse.urlencode(params)}", warnings)

        if record and record.get("instrumental"):
            print(f"LRCLIB가 연주곡(instrumental)으로 표시: {meta['artist']} - {meta['title']}")
            sys.exit(2)
        if record and record.get("syncedLyrics"):
            source, text = "lrclib-synced", record["syncedLyrics"]

        if source is None:
            query = urllib.parse.urlencode({"q": f"{meta['artist']} {meta['title']}"})
            warnings.append("LRCLIB /api/get 결과 없음 → /api/search 대체 사용")
            record = pick_search_result(fetch_json(f"{API}/search?{query}", warnings), duration)
            if record and record.get("syncedLyrics"):
                source, text = "lrclib-synced", record["syncedLyrics"]

        if source is None:
            if record and record.get("plainLyrics"):
                print("LRCLIB에 일반 가사만 있고 싱크 가사가 없습니다. 저장하지 않습니다.")
            else:
                print("가사를 찾지 못했습니다.")
            print("타이밍을 지어내지 않는다. 준비한 싱크 가사(.lrc)가 있으면 --lyrics로 넘겨 주세요.")
            sys.exit(2)

    bad, _, line_count = validate(text, duration)
    if bad is not None:
        if bad == "<마지막 타임스탬프>":
            die(3, f"마지막 타임스탬프가 길이({duration:.1f}초)를 1초 넘게 초과함")
        die(3, f"타임스탬프가 감소하는 줄: {bad}")

    target = Path(args.out) if args.out else audio.with_suffix(".lrc")
    target.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    if target.exists():
        backup = target.with_name(target.name + ".bak")
        shutil.copyfile(target, backup)

    body = text.replace("\r\n", "\n").replace("\r", "\n")
    target.write_text(body.rstrip("\n") + "\n", encoding="utf-8", newline="\n")

    print(f"곡: {meta['artist']} - {meta['title']}")
    print(f"앨범: {meta['album'] or '(없음)'}")
    print(f"길이: {duration:.1f}초")
    print(f"가사 출처: {source}")
    if record:
        print(f"LRCLIB id: {record.get('id')} / 앨범: {record.get('albumName') or '(없음)'}")
    print(f"줄 수: {line_count}")
    print(f"출력: {target}")
    print(f".bak 백업: {backup if backup else '없음'}")
    for warning in warnings:
        print(f"경고: {warning}")


if __name__ == "__main__":
    main()
