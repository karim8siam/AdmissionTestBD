import re
import json

BN_TO_EN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
EN_TO_BN_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")

OPTION_MAP = {
    'ক': 0, 'খ': 1, 'গ': 2, 'ঘ': 3,
    'a': 0, 'b': 1, 'c': 2, 'd': 3,
    'A': 0, 'B': 1, 'C': 2, 'D': 3
}

INDEX_TO_BN = {0: 'ক', 1: 'খ', 2: 'গ', 3: 'ঘ'}
INDEX_TO_EN = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}

def normalize_digits(text: str) -> str:
    return text.translate(BN_TO_EN_DIGITS)

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_raw_question_block(block: str) -> dict:
    """
    Parses a single question text block into structured dictionary.
    Handles Bangla/English question numbering, inline/multiline options, answer keys, explanations.
    """
    text = block.strip()
    if not text:
        return None

    # Find answer first if present
    ans_match = re.search(r'(?:উত্তর|Ans(?:wer)?|Correct\s*Option)[\s:\.\-\]\)]*[\(\[]?([ক-ঘA-Da-d])[\)\]]?', text, re.IGNORECASE)
    ans_label = ans_match.group(1) if ans_match else 'ক'
    ans_idx = OPTION_MAP.get(ans_label, 0)

    # Find explanation
    expl_match = re.search(r'(?:ব্যাখ্যা|Explanation|রেফারেন্স|Note)[\s:\.\-]+(.*?)(?=$|\n[০-৯0-9]+\.)', text, re.DOTALL | re.IGNORECASE)
    explanation = clean_text(expl_match.group(1)) if expl_match else ""

    # Strip out answer and explanation parts for clean option and question extraction
    content_part = text
    if ans_match:
        content_part = content_part[:ans_match.start()]

    # Extract options: split by delimiters like (ক), (খ), (গ), (ঘ) or ক., খ., গ., ঘ.
    pattern = r'(?:\s*[\(\[]?([ক-ঘA-Da-d])[\)\]\.]\s+)'
    parts = re.split(pattern, content_part)

    # parts[0] is the question body
    question_text = parts[0]
    # Remove leading question number e.g. "২৫. " or "25) "
    question_text = re.sub(r'^[০-৯0-9]+[\.\)\|\-:]?\s*', '', question_text)
    question_text = clean_text(question_text)

    options_dict = {}
    for i in range(1, len(parts), 2):
        lbl = parts[i]
        val = clean_text(parts[i+1]) if i+1 < len(parts) else ""
        options_dict[lbl] = val

    opt_a = options_dict.get('ক', options_dict.get('a', options_dict.get('A', '')))
    opt_b = options_dict.get('খ', options_dict.get('b', options_dict.get('B', '')))
    opt_c = options_dict.get('গ', options_dict.get('c', options_dict.get('C', '')))
    opt_d = options_dict.get('ঘ', options_dict.get('d', options_dict.get('D', '')))

    return {
        "question_bn": question_text,
        "option_a": opt_a,
        "option_b": opt_b,
        "option_c": opt_c,
        "option_d": opt_d,
        "correct_option": INDEX_TO_BN[ans_idx],
        "correct_index": ans_idx,
        "explanation": explanation
    }

if __name__ == '__main__':
    sample = """
    ২৫. মানবদেহে সবচেয়ে বড় গ্রন্থি কোনটি?
    (ক) থাইরয়েড  (খ) যকৃৎ  (গ) অগ্ন্যাশয়  (ঘ) পিটুইটারি
    উত্তর: (খ)
    ব্যাখ্যা: যকৃৎ মানবদেহের বৃহত্তম গ্রন্থি (ওজন ১.৫ - ২.০ কেজি)।
    """
    res = parse_raw_question_block(sample)
    print("Parsed sample successfully:")
    print(json.dumps(res, ensure_ascii=False, indent=2))
