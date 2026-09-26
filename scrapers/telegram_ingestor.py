import json
import re
import os
import sys

try:
    from .text_parser import parse_raw_question_block, clean_text
except ImportError:
    from text_parser import parse_raw_question_block, clean_text

class TelegramIngestor:
    """
    Ingests and normalizes question streams from Telegram:
    1. Telegram Chat Export JSON (Desktop export format)
    2. Telegram Poll Objects (Native quiz polls)
    3. Telegram Text Dump / Message logs
    """

    @staticmethod
    def parse_telegram_json_export(file_path: str) -> list:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Export file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        messages = data.get('messages', [])
        extracted_questions = []

        for msg in messages:
            # Case A: Poll message
            poll = msg.get('poll')
            if poll:
                q_text = clean_text(poll.get('question', ''))
                answers = poll.get('answers', [])
                if len(answers) >= 4:
                    opts = [a.get('text', '') for a in answers[:4]]
                    correct_idx = 0
                    for idx, a in enumerate(answers[:4]):
                        if a.get('chosen') or a.get('correct'):
                            correct_idx = idx
                            break
                    
                    extracted_questions.append({
                        "question_bn": q_text,
                        "option_a": opts[0],
                        "option_b": opts[1],
                        "option_c": opts[2],
                        "option_d": opts[3],
                        "correct_option": ['ক', 'খ', 'গ', 'ঘ'][correct_idx],
                        "correct_index": correct_idx,
                        "explanation": clean_text(poll.get('explanation', ''))
                    })
                continue

            # Case B: Plain text message formatted with MCQs
            text_content = msg.get('text', '')
            if isinstance(text_content, list):
                flat_text = ""
                for part in text_content:
                    if isinstance(part, str):
                        flat_text += part
                    elif isinstance(part, dict):
                        flat_text += part.get('text', '')
                text_content = flat_text

            if text_content and ('(ক)' in text_content or 'ক.' in text_content or 'Ans' in text_content or 'উত্তর' in text_content):
                parsed = parse_raw_question_block(text_content)
                if parsed and parsed.get('option_a') and parsed.get('option_b'):
                    extracted_questions.append(parsed)

        return extracted_questions

    @staticmethod
    def parse_text_stream(text_stream: str) -> list:
        blocks = re.split(r'\n(?=(?:[০-৯0-9]+[\.\)\|\-:]\s*))', text_stream)
        results = []
        for blk in blocks:
            if blk.strip():
                parsed = parse_raw_question_block(blk)
                if parsed and parsed.get('option_a'):
                    results.append(parsed)
        return results

if __name__ == '__main__':
    sample_text = """
    ১. শালোকসংশ্লেষণের অন্ধকার দশায় প্রথম স্থায়ী পদার্থ কোনটি?
    (ক) ৩-ফসফোগ্লিসারিক এসিড (খ) অক্সালো অ্যাসিটিক এসিড (গ) গ্লুকোজ (ঘ) পাইরুভিক এসিড
    উত্তর: (ক)
    ব্যাখ্যা: C3 উদ্ভিদে প্রথম স্থায়ী পদার্থ ৩-ফসফোগ্লিসারিক এসিড (৩-পিজিএ)। ড আবুল হাসান স্যার।

    ২. নিচের কোনটি ভেক্টর রাশি নয়?
    (ক) বেগ (খ) বল (গ) কাজ (ঘ) ত্বরন
    উত্তর: (গ)
    ব্যাখ্যা: কাজ একটি স্কেলার রাশি, এর নির্দিষ্ট কোনো দিক নেই।
    """
    qs = TelegramIngestor.parse_text_stream(sample_text)
    print(f"Parsed {len(qs)} questions from stream successfully!")
