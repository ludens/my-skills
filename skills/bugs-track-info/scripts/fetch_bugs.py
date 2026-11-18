#!/usr/bin/env python3
"""Fetch audio-file tag metadata from music.bugs.co.kr.

Usage:
  python3 fetch_bugs.py --artist "유나 (ITZY)" --song "Ice Cream"
  python3 fetch_bugs.py --track 33878893
  python3 fetch_bugs.py --track https://music.bugs.co.kr/track/33878893

Prints one JSON object to stdout. Standard library only.
"""

import argparse
import html
import http.cookiejar
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://music.bugs.co.kr"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")


class Client:
    """Bugs answers the first request with 429 + a bw_v cookie. Reuse the jar."""

    def __init__(self):
        jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(jar)
        )

    def get(self, url):
        last = ""
        for _ in range(5):
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept-Language": "ko-KR,ko;q=0.9",
            })
            try:
                with self.opener.open(req, timeout=25) as resp:
                    body = resp.read().decode("utf-8", "replace")
                if "잠시만 기다려 주세요" not in body:
                    return body
                last = "bot wall"
            except urllib.error.HTTPError as exc:
                if exc.code != 429:
                    raise
                last = "HTTP 429"
            time.sleep(1)
        raise RuntimeError("Bugs fetch failed: " + last + " " + url)


def text(fragment):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fragment))).strip()


def meta(doc, key):
    m = re.search(r'<meta[^>]+(?:property|name)="%s"[^>]+content="([^"]*)"' % re.escape(key), doc)
    return html.unescape(m.group(1)) if m else None


def jsonld(doc, want=None):
    m = re.search(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', doc, re.S)
    if not m:
        return {}
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError:
        return {}
    nodes = data if isinstance(data, list) else (
        data.get("@graph", [data]) if isinstance(data, dict) else []
    )
    for node in nodes:
        if isinstance(node, dict) and (not want or node.get("@type") == want):
            return node
    return {}


def child(value, key):
    value = value.get(key) if isinstance(value, dict) else None
    return value if isinstance(value, dict) else {}


def info_table(doc):
    m = re.search(r'<table class="info"[^>]*>(.*?)</table>', doc, re.S)
    if not m:
        return {}
    out = {}
    for row in re.finditer(r'<th scope="row">(.*?)</th>\s*<td[^>]*>(.*?)</td>', m.group(1), re.S):
        out[text(row.group(1))] = text(row.group(2))
    return out


def norm(value):
    return re.sub(r"[^0-9a-z가-힣]", "", unicodedata.normalize("NFKC", value).lower())


def id_from(value, kind):
    if not value:
        return None
    m = re.search(r"/%s/(\d+)" % kind, value)
    return m.group(1) if m else (value.strip() if value.strip().isdigit() else None)


def album_id(value):
    m = re.search(r"/album/(\d+)", value)
    return m.group(1) if m else None


def search(client, artist, song):
    query = " ".join(x for x in (artist, song) if x)
    doc = client.get(BASE + "/search/track?q=" + urllib.parse.quote(query))
    na, ns = norm(artist or ""), norm(song or "")
    candidates = []
    seen = set()
    order = 0
    for row in re.finditer(r'<tr[^>]*trackId="(\d+)"[^>]*>(.*?)</tr>', doc, re.S):
        tid, seg = row.group(1), row.group(2)
        if tid in seen:
            continue
        seen.add(tid)
        t = re.search(r'<p class="title"[^>]*>\s*<a[^>]*title="([^"]*)"', seg, re.S)
        a = re.search(r'<p class="artist"[^>]*>\s*<a[^>]*title="([^"]*)"', seg, re.S)
        if not (t and a):
            continue
        title, art = html.unescape(t.group(1)), html.unescape(a.group(1))
        nt = norm(title)
        score = 0
        if na and na in norm(art):
            score += 2
        if ns and ns == nt:
            score += 3
        elif ns and ns in nt:
            score += 1
        if re.search(r"inst\.|ver\.|remix|sped|slowed|cover|live", title, re.I):
            score -= 1
        aid = re.search(r'href="[^"]*/album/(\d+)', seg)
        candidates.append({
            "track_id": tid,
            "title": title,
            "artist": art,
            "album_id": aid.group(1) if aid else None,
            "score": score,
            "order": order,
        })
        order += 1
    candidates.sort(key=lambda c: (-c["score"], c["order"]))
    return query, candidates


def album_artist_id(doc):
    table = re.search(r'<table class="info"[^>]*>(.*?)</table>', doc, re.S)
    if not table:
        return None
    m = re.search(r'<th scope="row">아티스트</th>\s*<td[^>]*>(.*?)</td>', table.group(1), re.S)
    if not m:
        return None
    a = re.search(r"/artist/(\d+)", m.group(1))
    return a.group(1) if a else None


def artist_meta(client, artist_id):
    doc = client.get(BASE + "/artist/" + artist_id)
    ld = jsonld(doc, "MusicGroup")
    return {
        "name": ld.get("name") or "없음",
        "image_url": ld.get("image") or meta(doc, "og:image") or "없음",
        "url": ld.get("sameAs") or BASE + "/artist/" + artist_id,
    }


def album_meta(client, aid):
    doc = client.get(BASE + "/album/" + aid)
    ld, info = jsonld(doc, "MusicAlbum"), info_table(doc)
    rows = []
    for row in re.finditer(r'<tr[^>]*trackId="(\d+)"[^>]*>(.*?)</tr>', doc, re.S):
        seg = row.group(2)
        disc = re.search(r'disc_id="(\d+)"', seg)
        no = re.search(r"<em>(\d+)</em>", seg, re.S)
        rows.append((row.group(1), disc.group(1) if disc else None,
                     no.group(1) if no else None))
    discs = sorted({d for _, d, _ in rows if d})
    return {
        "name": ld.get("name") or (meta(doc, "og:title") or "").split(" / ")[0],
        "cover_url": ld.get("image") or meta(doc, "og:image"),
        "artist": child(ld, "byArtist").get("name") or info.get("아티스트"),
        "release_date": ld.get("datePublished") or info.get("발매일"),
        "total_tracks": len(rows),
        "total_discs": len(discs),
        "genre": info.get("장르"),
        "url": BASE + "/album/" + aid,
    }, rows, album_artist_id(doc)


def participants(doc):
    """'전체 보기' layer holds the full credits; the visible row is truncated."""
    aside = re.search(r'<aside id="participatingArtists".*?</aside>', doc, re.S)
    if not aside:
        return {}, False
    out = {}
    for row in re.finditer(r'<th scope="row">(.*?)</th>\s*<td[^>]*>(.*?)</td>', aside.group(0), re.S):
        key = text(row.group(1))
        cell = row.group(2)
        anchors = re.findall(r"<a[^>]*>(.*?)</a>", cell, re.S)
        names = [text(n) for n in anchors] if anchors else [
            n.strip() for n in text(cell).split(",") if n.strip()
        ]
        out[key] = names
    return out, True


def track_meta(client, tid, preferred_album=None, want_artist_image=False):
    doc = client.get(BASE + "/track/" + tid)
    ld, info = jsonld(doc, "MusicRecording"), info_table(doc)
    part, full = participants(doc)
    aid = preferred_album or album_id(child(ld, "inAlbum").get("url") or "")
    album, rows, _artist_id = (album_meta(client, aid) if aid else ({}, [], None))
    match = next((r for r in rows if r[0] == tid), (None, None, None))
    number = meta(doc, "sc:track_no") or match[2]
    result = {
        "album": album,
        "track": {
            "title": ld.get("name") or (meta(doc, "og:title") or "").split(" / ")[0],
            "artist": child(ld, "byArtist").get("name") or info.get("아티스트"),
            "track_number": number,
            "disc_number": match[1],
            "composer": part.get("작곡", []),
            "lyricist": part.get("작사", []),
            "arranger": part.get("편곡", []),
            "url": BASE + "/track/" + tid,
        },
        "notes": [],
    }
    if not full:
        result["notes"].append("전체 보기 레이어 없음: 작곡/작사/편곡이 없을 수 있음")
    if not aid:
        result["notes"].append("앨범 ID 없음: 앨범/디스크 정보 수집 불가")
    if want_artist_image:
        if not _artist_id:
            result["artist"] = {"name": "없음", "image_url": "없음", "url": "없음"}
            result["notes"].append("앨범 아티스트 ID 없음: 아티스트 이미지 조회 불가")
        else:
            try:
                result["artist"] = artist_meta(client, _artist_id)
            except (RuntimeError, OSError, urllib.error.URLError) as exc:
                result["artist"] = {"name": "없음", "image_url": "없음", "url": "없음"}
                result["notes"].append("아티스트 이미지 조회 실패: " + str(exc))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artist")
    ap.add_argument("--song")
    ap.add_argument("--track")
    ap.add_argument("--album")
    ap.add_argument("--artist-image", action="store_true")
    args = ap.parse_args()

    tid = id_from(args.track, "track")
    aid = id_from(args.album, "album")
    if not tid and not (args.artist or args.song):
        print(json.dumps({"error": "--artist/--song 또는 --track 필요"}, ensure_ascii=False))
        return 2
    try:
        client = Client()
        out = {}
        if not tid:
            query, candidates = search(client, args.artist, args.song)
            out["query"] = query
            out["candidates"] = [
                {k: v for k, v in c.items() if k != "order"} for c in candidates[:5]
            ]
            if not candidates:
                print(json.dumps({"error": "검색 결과 없음", "query": query}, ensure_ascii=False))
                return 1
            tid = candidates[0]["track_id"]
            out["notes"] = []
        out.update(track_meta(client, tid, aid, want_artist_image=args.artist_image))
        if "candidates" in out and out["candidates"][0]["score"] < 5:
            out["notes"].append("검색 1위가 정확 일치 아님: 후보 확인 필요")
    except (RuntimeError, OSError, urllib.error.URLError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
