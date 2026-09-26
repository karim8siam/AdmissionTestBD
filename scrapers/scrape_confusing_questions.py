import subprocess
import re
import json
import time
import os
from html import unescape

BASE_URL = "https://t.me/s/ConfusingQuestions5"
OUTPUT_FILE = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/scraped_confusing_questions.json"

FORBIDDEN_BRANDING = [
    "biology phobia", "biologyphobia", "@biologyphobia", "exam mate", 
    "exammatebd.com", "exammate", "biology phobia।exam mate"
]

def clean_branding(text: str) -> str:
    """Removes all mentions of Biology Phobia, Exam Mate, and external channel links."""
    if not text:
        return ""
    cleaned = text
    for brand in FORBIDDEN_BRANDING:
        cleaned = re.sub(re.escape(brand), "", cleaned, flags=re.IGNORECASE)
    
    # Remove telegram links e.g. t.me/...
    cleaned = re.sub(r'https?://t\.me/[^\s]+', '', cleaned)
    cleaned = re.sub(r'@\w+', '', cleaned)
    cleaned = re.sub(r'https?://[^\s]+', '', cleaned)
    # Clean extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def fetch_page(url: str) -> str:
    cmd = ["curl", "-sL", "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", url]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout

def parse_polls_and_messages(html: str) -> tuple:
    """
    Extracts polls and text questions from a Telegram channel page.
    Returns: (list_of_questions, prev_page_url)
    """
    questions = []

    # Find prev page link e.g. <link rel="prev" href="/s/ConfusingQuestions5?before=29301">
    prev_match = re.search(r'<link rel=\"prev\" href=\"([^\"]+)\"', html)
    prev_url = f"https://t.me{prev_match.group(1)}" if prev_match else None

    # Pattern for poll blocks
    # Each poll has question, options, and option percentages
    poll_blocks = re.findall(
        r'<div class=\"tgme_widget_message_poll_question[^\"]*\">(.*?)</div>(.*?)(?=<div class=\"tgme_widget_message_footer|<div class=\"tgme_widget_message_poll_question|$)',
        html, re.DOTALL
    )

    for q_html, options_html in poll_blocks:
        q_raw = unescape(re.sub(r'<[^>]+>', '', q_html)).strip()
        q_clean = clean_branding(q_raw)
        
        if not q_clean or len(q_clean) < 10:
            continue

        # Extract options and percentages
        # Option texts
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
            
            # Check percentage
            if pct_str:
                try:
                    pct = int(pct_str.replace('%', ''))
                    if pct > highest_pct:
                        highest_pct = pct
                        probable_ans_idx = idx
                except ValueError:
                    pass

        if len(options) >= 3:
            # Pad to 4 options if 3
            while len(options) < 4:
                options.append("উপরের কোনটিই নয়")

            questions.append({
                "question_bn": q_clean,
                "options": options[:4],
                "probable_ans_idx": probable_ans_idx,
                "type": "poll_quiz"
            })

    # Also extract text-based MCQ questions from message posts
    msg_blocks = re.findall(r'<div[^>]*class=\"[^\"]*js-message_text[^\"]*\"[^>]*>(.*?)</div>', html, re.DOTALL)
    for m in msg_blocks:
        txt = unescape(re.sub(r'<[^>]+>', ' ', m)).strip()
        txt_clean = clean_branding(txt)
        if ('(ক)' in txt_clean or 'ক.' in txt_clean) and ('(খ)' in txt_clean or 'খ.' in txt_clean):
            # Parse text MCQ
            from text_parser import parse_raw_question_block
            parsed = parse_raw_question_block(txt_clean)
            if parsed and parsed.get('option_a') and parsed.get('option_b'):
                questions.append({
                    "question_bn": parsed['question_bn'],
                    "options": [parsed['option_a'], parsed['option_b'], parsed['option_c'], parsed['option_d']],
                    "probable_ans_idx": parsed['correct_index'],
                    "type": "text_mcq",
                    "explanation": parsed.get('explanation', '')
                })

    return questions, prev_url

def run_scraper(max_pages: int = 15):
    print(f"Starting scraper on {BASE_URL} for standard biology questions...")
    current_url = BASE_URL
    all_questions = []
    seen_questions = set()

    for page_idx in range(max_pages):
        print(f"Fetching page {page_idx+1}: {current_url} ...")
        html = fetch_page(current_url)
        if not html:
            break

        new_qs, prev_url = parse_polls_and_messages(html)
        print(f" -> Found {len(new_qs)} questions on page {page_idx+1}")

        for q in new_qs:
            q_key = q['question_bn'].strip()
            if q_key not in seen_questions:
                seen_questions.add(q_key)
                all_questions.append(q)

        if not prev_url or prev_url == current_url:
            break
        current_url = prev_url
        time.sleep(0.5)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)

    print(f"\nScraping complete! Total clean, unbranded questions harvested: {len(all_questions)}")
    print(f"Saved to: {OUTPUT_FILE}")

if __name__ == '__main__':
    run_scraper(max_pages=12)
