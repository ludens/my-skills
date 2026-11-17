#!/usr/bin/env python3
"""Offline self-check for the Bugs parsers: python3 -m unittest discover -s skills/bugs-track-info/scripts"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fetch_bugs as fb


ALBUM_DOC = '''
<table class="info">
  <tr><th scope="row">아티스트</th><td><a href="https://music.bugs.co.kr/artist/80327438">유나</a></td></tr>
</table>
<a href="https://music.bugs.co.kr/artist/99999999">참여 아티스트</a>
'''

ARTIST_DOC = '''
<script type="application/ld+json">{"@graph":[
  {"@type":"WebPage","name":"무관"},
  {"@type":"MusicGroup","name":"유나",
   "image":"https://image.bugsm.co.kr/artist/images/1200/803274/80327438.jpg",
   "sameAs":"https://music.bugs.co.kr/artist/80327438"}
]}</script>
'''

class FakeClient:
    def get(self, url):
        return ARTIST_DOC


DOC = """
<meta property="sc:track_no" content="1"/>
<meta property="og:title" content="Ice Cream / 유나 (ITZY)"/>
<script type="application/ld+json">{"name":"Ice Cream","image":"https://img/x.jpg"}</script>
<table class="info"><tr><th scope="row">아티스트</th><td>유나</td></tr></table>
<aside id="participatingArtists">
  <table><tr><th scope="row">작곡</th><td><a>A</a>, <a>B</a></td></tr>
  <tr><th scope="row">편곡</th><td><a>C</a></td></tr></table>
</aside>
<div class="lyricsContainer"><xmp>한 줄 가사</xmp></div>
"""


class ParserTest(unittest.TestCase):
    def test_meta_and_jsonld(self):
        self.assertEqual(fb.meta(DOC, "sc:track_no"), "1")
        self.assertEqual(fb.jsonld(DOC)["name"], "Ice Cream")

    def test_hidden_participation_layer(self):
        part, found = fb.participants(DOC)
        self.assertTrue(found)
        self.assertEqual(part["작곡"], ["A", "B"])
        self.assertEqual(part["편곡"], ["C"])

    def test_lyrics(self):
        self.assertEqual(fb.lyrics(DOC), "한 줄 가사")
        self.assertEqual(fb.lyrics("<html/>"), "없음")

    def test_no_layer(self):
        part, found = fb.participants("<html/>")
        self.assertFalse(found)
        self.assertEqual(part, {})

    def test_plain_text_credits(self):
        doc = '<aside id="participatingArtists"><table><tr><th scope="row">작곡</th><td>A, B</td></tr></table></aside>'
        part, found = fb.participants(doc)
        self.assertTrue(found)
        self.assertEqual(part["작곡"], ["A", "B"])

    def test_jsonld_graph_pick(self):
        doc = ('<script type="application/ld+json">'
               '{"@graph":[{"@type":"WebPage"},'
               '{"@type":"MusicAlbum","name":"앨범"}]}</script>')
        self.assertEqual(fb.jsonld(doc, "MusicAlbum")["name"], "앨범")
        self.assertEqual(fb.jsonld(doc, "MusicRecording"), {})

    def test_id_from(self):
        self.assertEqual(fb.id_from("https://music.bugs.co.kr/track/33878893", "track"), "33878893")
        self.assertEqual(fb.id_from("33878893", "track"), "33878893")
        self.assertIsNone(fb.id_from("https://x:8080/t/1", "track"))

    def test_lyrics_with_attributes(self):
        doc = '<div class="foo lyricsContainer bar"><span>x</span><xmp>가사</xmp></div>'
        self.assertEqual(fb.lyrics(doc), "가사")

    def test_album_artist_id_uses_info_row(self):
        self.assertEqual(fb.album_artist_id(ALBUM_DOC), "80327438")

    def test_album_artist_id_missing(self):
        self.assertIsNone(fb.album_artist_id("<html/>"))

    def test_artist_meta_from_graph(self):
        got = fb.artist_meta(FakeClient(), "80327438")
        self.assertEqual(got["name"], "유나")
        self.assertEqual(got["image_url"], "https://image.bugsm.co.kr/artist/images/1200/803274/80327438.jpg")
        self.assertEqual(got["url"], "https://music.bugs.co.kr/artist/80327438")

    def test_artist_meta_without_image(self):
        class NoImage(FakeClient):
            def get(self, url):
                return '<script type="application/ld+json">{"@type":"MusicGroup","name":"유나"}</script>'
        self.assertEqual(fb.artist_meta(NoImage(), "80327438")["image_url"], "없음")


if __name__ == "__main__":
    unittest.main()
