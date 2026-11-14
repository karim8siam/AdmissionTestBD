#!/usr/bin/env python3
"""Validate deployable Search Console and AdSense readiness files."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASE = "https://www.admissiontestbd.online"
PUBLIC_PAGES = {
    "/": ROOT / "index.html",
    "/study-guide.html": ROOT / "study-guide.html",
    "/about.html": ROOT / "about.html",
    "/privacy.html": ROOT / "privacy.html",
    "/terms.html": ROOT / "terms.html",
    "/contact.html": ROOT / "contact.html",
}


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._title = False
        self.meta: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.json_ld: list[str] = []
        self._json_script = False
        self._json_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if tag == "title":
            self._title = True
        elif tag == "meta":
            self.meta.append(values)
        elif tag == "link":
            self.links.append(values)
        elif tag == "script" and values.get("type") == "application/ld+json":
            self._json_script = True
            self._json_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._title = False
        elif tag == "script" and self._json_script:
            self.json_ld.append("".join(self._json_parts))
            self._json_script = False

    def handle_data(self, data: str) -> None:
        if self._title:
            self.title += data
        if self._json_script:
            self._json_parts.append(data)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def parse(path: Path) -> tuple[str, HeadParser]:
    text = path.read_text(encoding="utf-8")
    parser = HeadParser()
    parser.feed(text)
    return text, parser


def meta_value(parser: HeadParser, key: str, value: str) -> str | None:
    for item in parser.meta:
        if item.get(key) == value:
            return item.get("content")
    return None


def main() -> None:
    expected_urls = set()
    for route, path in PUBLIC_PAGES.items():
        if not path.exists():
            fail(f"missing public page: {path.name}")
        text, parser = parse(path)
        expected = BASE + route
        expected_urls.add(expected)
        canonical = next((x.get("href") for x in parser.links if x.get("rel") == "canonical"), None)
        if canonical != expected:
            fail(f"{path.name} canonical is {canonical!r}; expected {expected!r}")
        if not parser.title.strip() or not meta_value(parser, "name", "description"):
            fail(f"{path.name} needs a title and meta description")
        robots = meta_value(parser, "name", "robots") or ""
        if "index" not in robots or "follow" not in robots:
            fail(f"{path.name} must be indexable and followable")
        if not parser.json_ld:
            fail(f"{path.name} has no JSON-LD")
        for block in parser.json_ld:
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                fail(f"invalid JSON-LD in {path.name}: {exc}")
        if path.name != "index.html" and len(re.sub(r"<[^>]+>", " ", text).split()) < 80:
            fail(f"{path.name} is too thin to be a useful trust page")

    root_html = (ROOT / "index.html").read_bytes()
    for mirror in (ROOT / "public/index.html", ROOT / "web/index.html"):
        if mirror.read_bytes() != root_html:
            fail(f"{mirror.relative_to(ROOT)} is not identical to index.html")

    for name in ("study-guide.html", "about.html", "privacy.html", "terms.html", "contact.html", "robots.txt", "sitemap.xml"):
        source = (ROOT / name).read_bytes()
        for prefix in ("public", "web"):
            mirror = ROOT / prefix / name
            if not mirror.exists() or mirror.read_bytes() != source:
                fail(f"{mirror.relative_to(ROOT)} is missing or differs from {name}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {BASE}/sitemap.xml" not in robots or "Disallow: /" + "\n" in robots:
        fail("robots.txt must allow the site and announce the sitemap")

    try:
        tree = ET.parse(ROOT / "sitemap.xml")
    except ET.ParseError as exc:
        fail(f"invalid sitemap XML: {exc}")
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = {node.text for node in tree.findall("s:url/s:loc", namespace)}
    if sitemap_urls != expected_urls:
        fail(f"sitemap URLs differ: {sitemap_urls ^ expected_urls}")

    config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    rendered_config = json.dumps(config)
    for required in ("X-Robots-Tag", "X-Content-Type-Options", "Referrer-Policy"):
        if required not in rendered_config:
            fail(f"vercel.json is missing {required}")

    all_deployed = "\n".join(path.read_text(encoding="utf-8") for path in PUBLIC_PAGES.values())
    if "ca-pub-1234567890123456" in all_deployed or "YOUR_REAL_TOKEN" in all_deployed:
        fail("placeholder Google credentials must never be deployed")

    ads_path = ROOT / "ads.txt"
    if ads_path.exists():
        ads = ads_path.read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"google\.com, pub-\d{16}, DIRECT, f08c47fec0942fa0", ads):
            fail("ads.txt exists but does not contain one valid Google publisher record")
        for mirror in (ROOT / "public/ads.txt", ROOT / "web/ads.txt"):
            if not mirror.exists() or mirror.read_bytes() != ads_path.read_bytes():
                fail("ads.txt mirrors are missing or inconsistent")

    print("PASS: SEO, sitemap, crawl, structured-data, trust-page, and Google-service safety checks passed.")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        fail(str(exc))
