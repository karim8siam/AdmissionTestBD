#!/usr/bin/env python3
"""Safely add real Google service IDs to every deployed HTML mirror.

Usage:
  python3 configure_google_services.py --publisher-id ca-pub-1234567890123456
  python3 configure_google_services.py --search-console-token TOKEN
  python3 configure_google_services.py --publisher-id ca-pub-... --search-console-token TOKEN

The script never writes placeholder IDs. When a publisher ID is provided it also
creates the valid ads.txt files required for the same publisher.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HTML_FILES = [ROOT / "index.html", ROOT / "public/index.html", ROOT / "web/index.html"]
ADS_FILES = [ROOT / "ads.txt", ROOT / "public/ads.txt", ROOT / "web/ads.txt"]
START = "  <!-- GOOGLE-SERVICES-START: configured by configure_google_services.py -->"
END = "  <!-- GOOGLE-SERVICES-END -->"
PUBLISHER_RE = re.compile(r"^ca-pub-\d{16}$")
TOKEN_RE = re.compile(r"^[A-Za-z0-9_-]{20,200}$")


def existing_value(pattern: str, html: str) -> str | None:
    match = re.search(pattern, html)
    return match.group(1) if match else None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publisher-id", help="AdSense publisher ID, for example ca-pub-1234567890123456")
    parser.add_argument("--search-console-token", help="Value from Google's HTML meta-tag verification method")
    args = parser.parse_args()

    if not args.publisher_id and not args.search_console_token:
        parser.error("provide --publisher-id, --search-console-token, or both")
    if args.publisher_id and not PUBLISHER_RE.fullmatch(args.publisher_id):
        parser.error("publisher ID must match ca-pub- followed by exactly 16 digits")
    if args.search_console_token and not TOKEN_RE.fullmatch(args.search_console_token):
        parser.error("Search Console token contains invalid characters or has an unexpected length")

    current = HTML_FILES[0].read_text(encoding="utf-8")
    publisher_id = args.publisher_id or existing_value(r'google-adsense-account" content="(ca-pub-\d{16})"', current)
    search_token = args.search_console_token or existing_value(r'google-site-verification" content="([A-Za-z0-9_-]+)"', current)

    lines: list[str] = [START]
    if search_token:
        lines.append(f'  <meta name="google-site-verification" content="{search_token}">')
    if publisher_id:
        lines.extend([
            f'  <meta name="google-adsense-account" content="{publisher_id}">',
            '  <script>',
            '    (function() {',
            '      var adLoaded = false;',
            '      function loadAdSense() {',
            '        if (adLoaded) return;',
            '        adLoaded = true;',
            '        var s = document.createElement("script");',
            f'        s.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={publisher_id}";',
            '        s.async = true;',
            '        s.crossOrigin = "anonymous";',
            '        document.head.appendChild(s);',
            '      }',
            '      if (/bot|google|crawler|spider|mediapartners/i.test(navigator.userAgent)) {',
            '        loadAdSense();',
            '      } else {',
            '        ["scroll", "touchstart", "mousemove", "keydown", "click"].forEach(function(e) {',
            '          window.addEventListener(e, loadAdSense, { once: true, passive: true });',
            '        });',
            '        if ("requestIdleCallback" in window) {',
            '          requestIdleCallback(function() { setTimeout(loadAdSense, 3000); });',
            '        } else {',
            '          setTimeout(loadAdSense, 3500);',
            '        }',
            '      }',
            '    })();',
            '  </script>',
        ])
    lines.append(END)
    replacement = "\n".join(lines)

    block_re = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    for path in HTML_FILES:
        html = path.read_text(encoding="utf-8")
        if not block_re.search(html):
            raise SystemExit(f"Google services marker block is missing from {path.relative_to(ROOT)}")
        path.write_text(block_re.sub(replacement, html, count=1), encoding="utf-8")

    if publisher_id:
        ads_line = f"google.com, {publisher_id.removeprefix('ca-')}, DIRECT, f08c47fec0942fa0\n"
        for path in ADS_FILES:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(ads_line, encoding="utf-8")

    print("Google service configuration updated safely.")
    if not publisher_id:
        print("AdSense was not changed because no publisher ID is configured.")


if __name__ == "__main__":
    main()
