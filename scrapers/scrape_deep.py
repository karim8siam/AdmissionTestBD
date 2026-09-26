import subprocess
import re
import json
import time
import os
from html import unescape

INPUT_FILE = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/scraped_confusing_questions.json"
OUTPUT_FILE = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/scraped_confusing_questions.json"

FORBIDDEN_BRANDING = [
    "biology phobia", "biologyphobia", "@biologyphobia", "exam mate", 
    "exammatebd.com", "exammate", "biology phobia।exam mate"
]

def clean_branding(text: str) -> str:
    if not text:
        return ""
    cleaned = text
    for brand in FORBIDDEN_BRANDING:
        cleaned = re.sub(re.escape(brand), "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'https?://t\.me/[^\s]+', '', cleaned)
    cleaned = re.sub(r'@\w+', '', cleaned)
    cleaned = re.sub(r'https?://[^\s]+', '', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def fetch_page(url: str) -> str:
    cmd = ["curl", "-sL", "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", url]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout

def parse_polls(html: str) -> tuple:
    questions = []
    prev_match = re.search(r'<link rel=\"prev\" href=\"([^\"]+)\"', html)
    prev_url = f"https://t.me{prev_match.group(1)}" if prev_match else None

    poll_blocks = re.findall(
        r'<div class=\"tgme_widget_message_poll_question[^\"]*\">(.*?)</div>(.*?)(?=<div class=\"tgme_widget_message_footer|<div class=\"tgme_widget_message_poll_question|$)',
        html, re.DOTALL
    )

    for q_html, options_html in poll_blocks:
        q_raw = unescape(re.sub(r'<[^>]+>', '', q_html)).strip()
        q_clean = clean_branding(q_raw)
        
        if not q_clean or len(q_clean) < 8:
            continue

        opt_matches = re.findall(
            r'<div class=\"tgme_widget_message_poll_option\">(?:.*?<div class=\"tgme_widget_message_poll_option_percent\">(\d+%)</div>)?.*?<div class=\"tgme_widget_message_poll_option_text[^\"]*\">(.*?)</div>',
            options_html, re.DOTALL
        )

        options = []
        highest_pct = -1
        probable_ans_idx = 0

        for idx, (pct_str, opt_text_html) in enumerate(opt_matches):
            opt_raw = unescape(re.sub(r'<[^>]+>', '', opt_text_html)).strip()
            opt_clean = clean_branding(opt_raw)
            options.append(opt_clean)
            
            if pct_str:
                try:
                    pct = int(pct_str.replace('%', ''))
                    if pct > highest_pct:
                        highest_pct = pct
                        probable_ans_idx = idx
                except ValueError:
                    pass

        if len(options) >= 3:
            while len(options) < 4:
                options.append("উপরের কোনটিই নয়")

            questions.append({
                "question_bn": q_clean,
                "options": options[:4],
                "probable_ans_idx": probable_ans_idx,
                "type": "poll_quiz"
            })
    return questions, prev_url

def run_deep_scraper(num_pages: int = 35):
    # Load existing
    existing = []
    seen = set()
    if os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            existing = json.load(f)
            for item in existing:
                seen.add(item['question_bn'].strip())
    print(f"Already have {len(existing)} unique questions.")

    current_url = "https://t.me/s/ConfusingQuestions5?before=29096"

    for i in range(num_pages):
        print(f"Fetching batch {i+1}/{num_pages}: {current_url} ...")
        html = fetch_page(current_url)
        if not html:
            break

        new_qs, prev_url = parse_polls(html)
        added = 0
        for q in new_qs:
            k = q['question_bn'].strip()
            if k not in seen:
                seen.add(k)
                existing.append(q)
                added += 1

        print(f" -> Added {added} new questions (Total now: {len(existing)})")
        if not prev_url or prev_url == current_url:
            break
        current_url = prev_url
        time.sleep(0.3)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    print(f"\nFinished! Total pool now contains {len(existing)} verified biology questions.")

if __name__ == '__main__':
    run_deep_scraper(30)
