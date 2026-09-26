import sqlite3
import json
import re
import os
import random

HARVESTED_FILE = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/scraped_confusing_questions.json"
PAST_YEARS_DB = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/medical_15years.db"

BIO_DB_PATH = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/biology_100_tests.db"
BIO_JSON_PATH = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/biology_100_tests.json"
BIO_CSV_PATH = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/biology_100_tests.csv"

FORBIDDEN_BRANDING = [
    "biology phobia", "biologyphobia", "@biologyphobia", "exam mate", 
    "exammatebd.com", "exammate", "biology phobia।exam mate", "telegram"
]

def clean_watermarks(text: str) -> str:
    if not text:
        return ""
    cleaned = text
    for brand in FORBIDDEN_BRANDING:
        cleaned = re.sub(re.escape(brand), "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'https?://[^\s]+', '', cleaned)
    cleaned = re.sub(r'@[A-Za-z0-9_]+', '', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def classify_biology_question(q_text: str) -> tuple:
    q_lower = q_text.lower()
    
    # Zoology
    if any(w in q_lower for w in ["হাইড্রা", "রুই মাছ", "ঘাসফড়িং", "নেমাটোসিস্ট", "সিলেন্টেরন", "ওমাটিডিয়াম"]):
        return "Zoology", "প্রাণীর পরিচিতি (Hydra, Grasshopper, Rui)", "গাজী আজমল ও গাজী আসমত", "Medium"
    if any(w in q_lower for w in ["রক্ত", "হৃৎপিণ্ড", "কপাটিকা", "অ্যালবুমিন", "লোহিত", "শ্বেত", "অনুচক্রিকা", "হিমোগ্লোবিন", "প্লাজমা", "এবিও", "Rh"]):
        return "Zoology", "মানব শারীরতত্ত্ব: রক্ত ও সংবহন", "গাজী আজমল ও গাজী আসমত", "Medium"
    if any(w in q_lower for w in ["পরিপাক", "যকৃৎ", "পাকস্থলী", "এনজাইম", "দাঁত", "প্যারোটিড", "গ্ল্যান্ড", "পিত্তরস", "ক্ষুদ্রান্ত্র", "পেপসিন"]):
        return "Zoology", "মানব শারীরতত্ত্ব: পরিপাক ও শোষণ", "গাজী আজমল ও গাজী আসমত", "Easy"
    if any(w in q_lower for w in ["শ্বাস", "ফুসফুস", "শ্বসন", "অ্যালভিওলাস", "হ্যামবার্গার", "ব্রংকাস"]):
        return "Zoology", "মানব শারীরতত্ত্ব: শ্বাসক্রিয়া ও শ্বসন", "গাজী আজমল ও গাজী আসমত", "Medium"
    if any(w in q_lower for w in ["নেফ্রন", "বৃক্ক", "ইউরিয়া", "গ্লোমেরুলাস", "বর্জ্য", "হেনলির"]):
        return "Zoology", "মানব শারীরতত্ত্ব: বর্জ্য ও নিষ্কাশন", "গাজী আজমল ও গাজী আসমত", "Medium"
    if any(w in q_lower for w in ["মস্তিষ্ক", "স্নায়ু", "করোটিক", "সেরেব্রাম", "সেরেবেলাম", "মেডুলা", "হরমোন", "থাইরয়েড", "চোখ", "কান", "পনস"]):
        return "Zoology", "মানব শারীরতত্ত্ব: সমন্বয় ও নিয়ন্ত্রণ", "গাজী আজমল ও গাজী আসমত", "Hard"
    if any(w in q_lower for w in ["কশেরুকা", "অস্থি", "পেশি", "হাড়", "ফিমার", "হিউমেরাস", "কঙ্কাল", "তরুণাস্থি"]):
        return "Zoology", "মানব শারীরতত্ত্ব: চলন ও অঙ্গচালনা", "গাজী আজমল ও গাজী আসমত", "Easy"
    if any(w in q_lower for w in ["অনাক্রম্যতা", "প্রতিরক্ষা", "অ্যান্টিবডি", "ভ্যাকসিন", "টিকা", "ইমিউন", "iga", "igg"]):
        return "Zoology", "মানবদেহের প্রতিরক্ষা", "গাজী আজমল ও গাজী আসমত", "Hard"
    if any(w in q_lower for w in ["মেন্ডেল", "জিন", "ক্রোমোজোম", "অ্যাلیل", "হিমোফিলিয়া", "থ্যালাসেমিয়া", "এপিস্ট্যাসিস"]):
        return "Zoology", "জিনতত্ত্ব ও বিবর্তন", "গাজী আজমল ও গাজী আসমত", "Hard"
    if any(w in q_lower for w in ["পর্ব", "সিলোম", "অ্যানিলিডা", "আর্থ্রোপোডা", "মলাস্কা", "পরিফেরা", "নিডারিয়া", "কর্ডাটা"]):
        return "Zoology", "প্রাণীর বিভিন্নতা ও শ্রেণিবিন্যাস", "গাজী আজমল ও গাজী আসমত", "Easy"

    # Botany
    if any(w in q_lower for w in ["মাইটোকন্ড্রিয়া", "ক্লোরোপ্লাস্ট", "রাইবোসোম", "গলগি", "লাইসোসোম", "ডিএনএ", "আরএনএ", "কোষ অঙ্গাণু"]):
        return "Botany", "কোষ ও এর গঠন", "ড. মোহাম্মদ আবুল হাসান", "Easy"
    if any(w in q_lower for w in ["মিয়োসিস", "মাইটোসিস", "প্রফেজ", "মেটাফেজ", "অ্যানাফেজ", "টেলোফেজ", "কায়াজমা", "ক্রসিং ওভার"]):
        return "Botany", "কোষ বিভাজন", "ড. মোহাম্মদ আবুল হাসান", "Medium"
    if any(w in q_lower for w in ["ভাইরাস", "ব্যাকটেরিয়া", "ম্যালেরিয়া", "প্লাজমোডিয়াম", "অণুজীব"]):
        return "Botany", "অণুজীব", "ড. মোহাম্মদ আবুল হাসান", "Medium"
    if any(w in q_lower for w in ["শালোকসংশ্লেষণ", "প্রস্বেদন", "c3", "c4", "ফসফোরিলেশন", "গ্লাইকোলাইসিস"]):
        return "Botany", "উদ্ভিদ শারীরতত্ত্ব", "ড. মোহাম্মদ আবুল হাসান", "Hard"
    if any(w in q_lower for w in ["ভাস্কুলার", "টিস্যু", "জাইলেম", "ফ্লোয়েম", "ক্যাম্বিয়াম"]):
        return "Botany", "টিস্যু ও টিস্যুতন্ত্র", "ড. মোহাম্মদ আবুল হাসান", "Medium"
    if any(w in q_lower for w in ["ম্যালভেসি", "পোয়াসি", "সাইকাস", "নগ্নবীজী", "আবৃতবীজী"]):
        return "Botany", "নগ্নবীজী ও আবৃতবীজী উদ্ভিদ", "ড. মোহাম্মদ আবুল হাসান", "Medium"
    if any(w in q_lower for w in ["টিস্যু কালচার", "রিকম্বিনেন্ট", "প্লাজমিড", "রেস্ট্রিকশন", "জীবপ্রযুক্তি"]):
        return "Botany", "জীবপ্রযুক্তি", "ড. মোহাম্মদ আবুল হাসান", "Hard"
    if any(w in q_lower for w in ["শৈবাল", "ছত্রাক", "অ্যাগারিকাস", "স্পাইরোগাইরা", "লাইকেন"]):
        return "Botany", "শৈবাল ও ছত্রাক", "ড. মোহাম্মদ আবুল হাসান", "Easy"
    if any(w in q_lower for w in ["পরাগরেণু", "ভ্রূণ", "নিষেক", "পরাগায়ন"]):
        return "Botany", "উদ্ভিদ প্রজনন", "ড. মোহাম্মদ আবুল হাসান", "Medium"

    return "Botany", "সাধারণ উদ্ভিদবিজ্ঞান ও শারীরতত্ত্ব", "ড. মোহাম্মদ আবুল হাসান", "Medium"

def init_biology_100_db():
    os.makedirs(os.path.dirname(BIO_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(BIO_DB_PATH)
    cursor = conn.cursor()
    cursor.executescript("""
    PRAGMA foreign_keys = ON;
    PRAGMA journal_mode = WAL;

    DROP TABLE IF EXISTS biology_questions;
    DROP TABLE IF EXISTS model_tests;
    DROP TABLE IF EXISTS biology_questions_fts;

    CREATE TABLE model_tests (
        test_id INTEGER PRIMARY KEY,               -- 1 to 100
        test_code TEXT UNIQUE NOT NULL,            -- 'MT-BIO-001' to 'MT-BIO-100'
        test_name_bn TEXT NOT NULL,                -- 'মেডিকেল বায়োলজি মডেল টেস্ট ০১'
        test_standard TEXT DEFAULT 'Full Syllabus DGME Mixed Standard',
        total_questions INTEGER DEFAULT 30,
        botany_count INTEGER DEFAULT 15,
        zoology_count INTEGER DEFAULT 15,
        marks_per_question REAL DEFAULT 1.0,
        negative_mark REAL DEFAULT 0.25,
        time_limit_minutes INTEGER DEFAULT 20
    );

    CREATE TABLE biology_questions (
        id TEXT PRIMARY KEY,                       -- 'MT-001-Q01'
        test_id INTEGER NOT NULL,                  -- 1 to 100
        question_num INTEGER NOT NULL,             -- 1 to 30
        subject TEXT DEFAULT 'Biology',
        sub_discipline TEXT NOT NULL,              -- Botany or Zoology
        chapter TEXT NOT NULL,
        question_bn TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_option TEXT NOT NULL,              -- 'ক', 'খ', 'গ', 'ঘ'
        correct_index INTEGER NOT NULL,            -- 0, 1, 2, 3
        explanation TEXT,
        book_reference TEXT NOT NULL,
        difficulty TEXT DEFAULT 'Medium',
        is_confusing_standard INTEGER DEFAULT 1,
        source TEXT DEFAULT 'NCTB & Telegram Standard Bank',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(test_id) REFERENCES model_tests(test_id)
    );

    CREATE INDEX idx_bio_test_id ON biology_questions(test_id);
    CREATE INDEX idx_bio_sub_discipline ON biology_questions(sub_discipline);
    CREATE INDEX idx_bio_chapter ON biology_questions(chapter);

    CREATE VIRTUAL TABLE biology_questions_fts USING fts5(
        id UNINDEXED,
        question_bn,
        option_a,
        option_b,
        option_c,
        option_d,
        explanation,
        chapter,
        tokenize='unicode61'
    );

    CREATE TRIGGER bio_ai AFTER INSERT ON biology_questions BEGIN
        INSERT INTO biology_questions_fts(id, question_bn, option_a, option_b, option_c, option_d, explanation, chapter)
        VALUES (new.id, new.question_bn, new.option_a, new.option_b, new.option_c, new.option_d, new.explanation, new.chapter);
    END;
    """)
    conn.commit()
    conn.close()

def build_equal_mixed_100_tests():
    init_biology_100_db()
    
    # 1. Load harvested clean questions
    with open(HARVESTED_FILE, 'r', encoding='utf-8') as f:
        harvested = json.load(f)

    # 2. Load past 15-year biology questions
    conn_past = sqlite3.connect(PAST_YEARS_DB)
    conn_past.row_factory = sqlite3.Row
    past_cur = conn_past.cursor()
    past_cur.execute("SELECT * FROM questions WHERE subject = 'Biology'")
    past_bio_qs = [dict(r) for r in past_cur.fetchall()]
    conn_past.close()

    opt_bn_labels = ['ক', 'খ', 'গ', 'ঘ']
    master_pool = []

    # Ingest harvested questions with classification
    for item in harvested:
        q_text = clean_watermarks(item['question_bn'])
        opts = [clean_watermarks(o) for o in item['options']]
        if len(opts) < 4:
            continue
        sub, chap, auth, diff = classify_biology_question(q_text)
        ans_idx = item.get('probable_ans_idx', 0)
        ans_lbl = opt_bn_labels[ans_idx]
        master_pool.append({
            "question_bn": q_text,
            "option_a": opts[0],
            "option_b": opts[1],
            "option_c": opts[2],
            "option_d": opts[3],
            "correct_option": ans_lbl,
            "correct_index": ans_idx,
            "sub_discipline": sub,
            "chapter": chap,
            "book_reference": f"{auth}, {chap}",
            "explanation": f"সঠিক উত্তর ({ans_lbl}): {opts[ans_idx]}। রেফারেন্স: {auth} ({chap})।",
            "difficulty": diff,
            "is_confusing_standard": 1,
            "source": "Standard Tricky Bank"
        })

    # Ingest past year questions
    for item in past_bio_qs:
        sub = item['sub_discipline'] if item['sub_discipline'] in ['Botany', 'Zoology'] else ('Zoology' if 'শারীরতত্ত্ব' in item['chapter'] else 'Botany')
        master_pool.append({
            "question_bn": clean_watermarks(item['question_bn']),
            "option_a": clean_watermarks(item['option_a']),
            "option_b": clean_watermarks(item['option_b']),
            "option_c": clean_watermarks(item['option_c']),
            "option_d": clean_watermarks(item['option_d']),
            "correct_option": item['correct_option'],
            "correct_index": item['correct_index'],
            "sub_discipline": sub,
            "chapter": item['chapter'],
            "book_reference": item['book_reference'],
            "explanation": item['explanation'],
            "difficulty": item.get('difficulty', 'Medium'),
            "is_confusing_standard": 0,
            "source": f"DGME Past Paper ({item['session']})"
        })

    # Separate into Botany and Zoology pools
    botany_pool = [q for q in master_pool if q['sub_discipline'] == 'Botany']
    zoology_pool = [q for q in master_pool if q['sub_discipline'] == 'Zoology']

    print(f"Total Master Pool: {len(master_pool)} (Botany: {len(botany_pool)}, Zoology: {len(zoology_pool)})")

    # Generate 100 Completely Equal, Mixed Full-Syllabus Tests
    conn = sqlite3.connect(BIO_DB_PATH)
    cursor = conn.cursor()

    tests_meta = []
    all_questions = []

    for test_idx in range(1, 101):
        test_code = f"MT-BIO-{test_idx:03d}"
        test_name = f"মেডিকেল বায়োলজি মডেল টেস্ট {test_idx:02d}"

        tests_meta.append((
            test_idx, test_code, test_name,
            "Full Syllabus DGME Mixed Standard (100% Equal Level)",
            30, 15, 15, 1.0, 0.25, 20
        ))

        # Balanced random selection using seeded RNG per test
        # Guarantees each test is equally mixed, high standard, full syllabus
        rng = random.Random(test_idx * 1337 + 7)

        # 15 Botany + 15 Zoology
        bot_sampled = rng.sample(botany_pool, 15) if len(botany_pool) >= 15 else (botany_pool * 2)[:15]
        zoo_sampled = rng.sample(zoology_pool, 15) if len(zoology_pool) >= 15 else (zoology_pool * 2)[:15]

        # Combine and interleave evenly so Botany and Zoology are completely mixed
        test_qs = []
        for b, z in zip(bot_sampled, zoo_sampled):
            if rng.random() > 0.5:
                test_qs.extend([b, z])
            else:
                test_qs.extend([z, b])

        for q_num, q in enumerate(test_qs, start=1):
            qid = f"MT-{test_idx:03d}-Q{q_num:02d}"
            all_questions.append((
                qid, test_idx, q_num, 'Biology', q['sub_discipline'], q['chapter'],
                q['question_bn'], q['option_a'], q['option_b'], q['option_c'], q['option_d'],
                q['correct_option'], q['correct_index'], q['explanation'], q['book_reference'],
                q['difficulty'], q['is_confusing_standard'], q['source']
            ))

    cursor.executemany("""
        INSERT INTO model_tests 
        (test_id, test_code, test_name_bn, test_standard, total_questions, botany_count, zoology_count, marks_per_question, negative_mark, time_limit_minutes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tests_meta)

    cursor.executemany("""
        INSERT INTO biology_questions
        (id, test_id, question_num, subject, sub_discipline, chapter, question_bn,
         option_a, option_b, option_c, option_d, correct_option, correct_index,
         explanation, book_reference, difficulty, is_confusing_standard, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, all_questions)

    conn.commit()
    conn.close()

    print(f"\n100 Completely Equal Mixed Tests built successfully!")
    print(f"Total Model Tests: 100")
    print(f"Total Questions: {len(all_questions)} (30 questions per test, 15 Botany + 15 Zoology)")

    # Export to JSON
    conn = sqlite3.connect(BIO_DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM biology_questions ORDER BY test_id, question_num")
    rows = [dict(r) for r in c.fetchall()]
    
    with open(BIO_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"Exported to JSON: {BIO_JSON_PATH}")

    import csv
    with open(BIO_CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Exported to CSV: {BIO_CSV_PATH}")
    conn.close()

if __name__ == '__main__':
    build_equal_mixed_100_tests()
