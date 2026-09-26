import subprocess
import re
import json
import time
import os
from html import unescape

BASE_URL = "https://t.me/s/ConfusingQuestions8"
OUTPUT_FILE = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/scraped_gk_questions.json"

FORBIDDEN_BRANDING = [
    "gk phobia", "gkphobia", "@gkphobia",
    "english phobia", "englishphobia", "@englishphobia",
    "physics phobia", "physicsphobia", "@physicsphobia",
    "chemistry phobia", "chemistryphobia", "@chemistryphobia",
    "biology phobia", "biologyphobia", "@biologyphobia", 
    "exam mate", "exammatebd.com", "exammate", 
    "confusingquestions8", "@confusingquestions8", "confusingquestions",
    "telegram", "facebook"
]

def clean_branding(text: str) -> str:
    if not text:
        return ""
    cleaned = text
    for brand in FORBIDDEN_BRANDING:
        cleaned = re.sub(re.escape(brand), "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'https?://[^\s]+', '', cleaned)
    cleaned = re.sub(r'@[A-Za-z0-9_]+', '', cleaned)
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
        
        if not q_clean or len(q_clean) < 5:
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
                options.append("কোনোটিই নয়")

            questions.append({
                "question_bn": q_clean,
                "options": options[:4],
                "probable_ans_idx": min(max(probable_ans_idx, 0), 3),
                "type": "poll_quiz"
            })
    return questions, prev_url

def run_gk_scraper(num_pages: int = 40):
    print(f"Starting scraper for GK on {BASE_URL}...")
    current_url = BASE_URL
    all_questions = []
    seen = set()

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
                all_questions.append(q)
                added += 1

        print(f" -> Added {added} questions (Total: {len(all_questions)})")
        if not prev_url or prev_url == current_url:
            break
        current_url = prev_url
        time.sleep(0.3)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)

    print(f"\nScraping complete! Total unbranded GK questions harvested: {len(all_questions)}")
    print(f"Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_gk_scraper(40)
