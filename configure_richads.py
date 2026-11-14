#!/usr/bin/env python3
"""Safely configure and integrate RichAds ad tags and service workers across all deployed HTML mirrors.

Usage:
  python3 configure_richads.py --script-tag '<script src="https://richinfo.co/..." async></script>'
  python3 configure_richads.py --worker-url 'https://richpush.co/sw-import.js'
  python3 configure_richads.py --status
  python3 configure_richads.py --remove
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HTML_FILES = [
    ROOT / "index.html", ROOT / "public/index.html", ROOT / "web/index.html",
    ROOT / "about.html", ROOT / "public/about.html", ROOT / "web/about.html",
    ROOT / "contact.html", ROOT / "public/contact.html", ROOT / "web/contact.html",
    ROOT / "terms.html", ROOT / "public/terms.html", ROOT / "web/terms.html",
    ROOT / "privacy.html", ROOT / "public/privacy.html", ROOT / "web/privacy.html",
    ROOT / "study-guide.html", ROOT / "public/study-guide.html", ROOT / "web/study-guide.html",
]
SW_FILES = [ROOT / "sw.js", ROOT / "public/sw.js", ROOT / "web/sw.js"]

HEAD_START = "  <!-- RICHADS-MONETIZATION-START: configured by configure_richads.py -->"
HEAD_END = "  <!-- RICHADS-MONETIZATION-END -->"

SW_START = "// RICHADS-WORKER-IMPORT-START"
SW_END = "// RICHADS-WORKER-IMPORT-END"


def update_html(script_tag: str | None = None, remove: bool = False) -> None:
    head_block_re = re.compile(re.escape(HEAD_START) + r".*?" + re.escape(HEAD_END), re.DOTALL)
    
    if remove or not script_tag:
        replacement = f"{HEAD_START}\n{HEAD_END}"
    else:
        cleaned_tag = script_tag.strip()
        replacement = f"{HEAD_START}\n  {cleaned_tag}\n{HEAD_END}"

    for path in HTML_FILES:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        if not head_block_re.search(content):
            # If marker not present, place it before </head>
            if "</head>" in content:
                content = content.replace("</head>", f"{replacement}\n</head>", 1)
            else:
                raise SystemExit(f"Could not find head closing tag in {path.name}")
        else:
            content = head_block_re.sub(replacement, content, count=1)
        path.write_text(content, encoding="utf-8")


def update_sw(worker_url: str | None = None, remove: bool = False) -> None:
    sw_block_re = re.compile(re.escape(SW_START) + r".*?" + re.escape(SW_END), re.DOTALL)
    
    if remove or not worker_url:
        replacement = f"{SW_START}\n{SW_END}"
    else:
        clean_url = worker_url.strip().strip("'\"")
        replacement = f"{SW_START}\ntry {{\n  importScripts('{clean_url}');\n}} catch (e) {{\n  console.warn('RichAds worker import failed:', e);\n}}\n{SW_END}"

    for path in SW_FILES:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            base_sw = (ROOT / "sw.js").read_text(encoding="utf-8") if (ROOT / "sw.js").exists() else ""
            content = base_sw or f"{replacement}\n"
        else:
            content = path.read_text(encoding="utf-8")
        
        if sw_block_re.search(content):
            content = sw_block_re.sub(replacement, content, count=1)
        else:
            content = f"{replacement}\n" + content
        path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--script-tag", help="RichAds JavaScript tag snippet provided in your RichAds Publisher dashboard")
    parser.add_argument("--worker-url", help="RichAds Service Worker script URL for Push Notification import")
    parser.add_argument("--remove", action="store_true", help="Remove RichAds scripts and worker imports")
    parser.add_argument("--status", action="store_true", help="Check current RichAds integration status")
    args = parser.parse_args()

    if args.status:
        index_content = HTML_FILES[0].read_text(encoding="utf-8") if HTML_FILES[0].exists() else ""
        sw_content = SW_FILES[0].read_text(encoding="utf-8") if SW_FILES[0].exists() else ""
        
        head_match = re.search(re.escape(HEAD_START) + r"\n(.*?)\n" + re.escape(HEAD_END), index_content, re.DOTALL)
        tag = head_match.group(1).strip() if head_match else "None"
        
        sw_block = re.search(re.escape(SW_START) + r"(.*?)" + re.escape(SW_END), sw_content, re.DOTALL)
        worker = "None"
        if sw_block:
            m = re.search(r"importScripts\(['\"]([^'\"]+)['\"]\)", sw_block.group(1))
            if m:
                worker = m.group(1)
        
        print("--- RichAds Integration Status ---")
        print(f"HTML Tag Installed: {'Yes' if tag != 'None' and tag else 'No'}")
        if tag and tag != "None":
            print(f"Tag: {tag}")
        print(f"Service Worker Import: {worker}")
        return

    if not args.script_tag and not args.worker_url and not args.remove:
        parser.print_help()
        return

    if args.remove:
        update_html(remove=True)
        update_sw(remove=True)
        print("RichAds integration removed cleanly from HTML and Service Worker files.")
        return

    if args.script_tag:
        update_html(script_tag=args.script_tag)
        print("RichAds script tag successfully injected into all HTML mirrors.")

    if args.worker_url:
        update_sw(worker_url=args.worker_url)
        print("RichAds worker import successfully updated in sw.js mirrors.")


if __name__ == "__main__":
    main()
