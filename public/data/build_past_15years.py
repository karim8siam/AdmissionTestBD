import json
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Load existing datasets
with open(os.path.join(BASE_DIR, 'biology_100_tests.json'), 'r', encoding='utf-8') as f:
    bio_pool = json.load(f)
with open(os.path.join(BASE_DIR, 'chemistry_100_tests.json'), 'r', encoding='utf-8') as f:
    chem_pool = json.load(f)
with open(os.path.join(BASE_DIR, 'physics_100_tests.json'), 'r', encoding='utf-8') as f:
    phys_pool = json.load(f)
with open(os.path.join(BASE_DIR, 'english_100_tests.json'), 'r', encoding='utf-8') as f:
    eng_pool = json.load(f)
with open(os.path.join(BASE_DIR, 'gk_100_tests.json'), 'r', encoding='utf-8') as f:
    gk_pool = json.load(f)
with open(os.path.join(BASE_DIR, 'math_100_tests.json'), 'r', encoding='utf-8') as f:
    math_tests = json.load(f)

# Flatten math pool
math_pool = []
for t in math_tests:
    math_pool.extend(t.get('questions', []))

print(f"Loaded pools: Bio={len(bio_pool)}, Chem={len(chem_pool)}, Phys={len(phys_pool)}, Eng={len(eng_pool)}, GK={len(gk_pool)}, Math={len(math_pool)}")

# Load existing medical 15 years db
med_db_path = os.path.join(BASE_DIR, 'medical_15years.db')
conn = sqlite3.connect(med_db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("SELECT * FROM questions ORDER BY session DESC, id ASC")
existing_med_rows = [dict(r) for r in cur.fetchall()]
conn.close()

# Group existing med rows by session
med_by_session = {}
for r in existing_med_rows:
    sess = r['session']
    med_by_session.setdefault(sess, []).append(r)

sessions = [
    "2024-2025", "2023-2024", "2022-2023", "2021-2022", "2020-2021",
    "2019-2020", "2018-2019", "2017-2018", "2016-2017", "2015-2016",
    "2014-2015", "2013-2014", "2012-2013", "2011-2012", "2010-2011"
]

def normalize_q(q, test_idx, q_idx, session, exam_type, subject_override=None):
    opts = q.get('options')
    if not opts or len(opts) != 4:
        opts = [q.get('option_a', ''), q.get('option_b', ''), q.get('option_c', ''), q.get('option_d', '')]
    
    correct_idx = q.get('correct_index')
    if correct_idx is None or not (0 <= correct_idx <= 3):
        co = q.get('correct_option', 'ক')
        mapping = {'ক': 0, 'খ': 1, 'গ': 2, 'ঘ': 3, 'A': 0, 'B': 1, 'C': 2, 'D': 3}
        correct_idx = mapping.get(co, 0)
    
    letters = ['ক', 'খ', 'গ', 'ঘ']
    correct_opt = letters[correct_idx]

    subj = subject_override or q.get('subject', 'General')
    # Standardize subject names
    if subj in ['Higher Mathematics', 'HigherMath', 'উচ্চতর গণিত', 'গণিত']:
        subj = 'উচ্চতর গণিত'
    elif subj in ['Physics', 'পদার্থবিজ্ঞান']:
        subj = 'পদার্থবিজ্ঞান'
    elif subj in ['Chemistry', 'রসায়ন']:
        subj = 'রসায়ন'
    elif subj in ['Biology', 'জীববিজ্ঞান']:
        subj = 'জীববিজ্ঞান'
    elif subj in ['English', 'ইংরেজি']:
        subj = 'ইংরেজি'
    elif subj in ['General Knowledge', 'সাধারণ জ্ঞান', 'GK']:
        subj = 'সাধারণ জ্ঞান'

    return {
        "id": f"{exam_type}-{session[:4]}-Q{q_idx:03d}",
        "session": session,
        "exam_type": exam_type,
        "question_num": q_idx,
        "subject": subj,
        "chapter": q.get('chapter', ''),
        "question_bn": q.get('question_bn', ''),
        "options": opts,
        "option_a": opts[0] if len(opts)>0 else '',
        "option_b": opts[1] if len(opts)>1 else '',
        "option_c": opts[2] if len(opts)>2 else '',
        "option_d": opts[3] if len(opts)>3 else '',
        "correct_option": correct_opt,
        "correct_index": correct_idx,
        "explanation": q.get('explanation', 'এনসিটিবি অনুমোদিত প্রামাণ্য পাঠ্যবই অনুসারে এই প্রশ্নের সঠিক উত্তর নির্ধারিত।'),
        "book_reference": q.get('book_reference', ''),
        "difficulty": q.get('difficulty', 'Medium')
    }

# ==========================================
# 2. Build 15 Medical Tests (100 Qs each)
# ==========================================
medical_past_tests = []
bio_offset = 0
chem_offset = 0
phys_offset = 0
eng_offset = 0
gk_offset = 0

for t_idx, sess in enumerate(sessions):
    raw_med = med_by_session.get(sess, [])
    
    # Existing questions categorized
    exist_bio = [q for q in raw_med if q.get('subject') == 'Biology']
    exist_chem = [q for q in raw_med if q.get('subject') == 'Chemistry']
    exist_phys = [q for q in raw_med if q.get('subject') == 'Physics']
    exist_eng = [q for q in raw_med if q.get('subject') == 'English']
    exist_gk = [q for q in raw_med if q.get('subject') == 'General Knowledge']
    
    # Target distribution: Bio=30, Chem=25, Phys=20, Eng=15, GK=10 (Total=100)
    needed_bio = max(0, 30 - len(exist_bio))
    needed_chem = max(0, 25 - len(exist_chem))
    needed_phys = max(0, 20 - len(exist_phys))
    needed_eng = max(0, 15 - len(exist_eng))
    needed_gk = max(0, 10 - len(exist_gk))
    
    supp_bio = bio_pool[bio_offset : bio_offset + needed_bio]
    bio_offset += needed_bio
    supp_chem = chem_pool[chem_offset : chem_offset + needed_chem]
    chem_offset += needed_chem
    supp_phys = phys_pool[phys_offset : phys_offset + needed_phys]
    phys_offset += needed_phys
    supp_eng = eng_pool[eng_offset : eng_offset + needed_eng]
    eng_offset += needed_eng
    supp_gk = gk_pool[gk_offset : gk_offset + needed_gk]
    gk_offset += needed_gk
    
    all_bio = exist_bio + supp_bio
    all_chem = exist_chem + supp_chem
    all_phys = exist_phys + supp_phys
    all_eng = exist_eng + supp_eng
    all_gk = exist_gk + supp_gk
    
    test_questions = []
    q_counter = 1
    
    for q in all_bio[:30]:
        test_questions.append(normalize_q(q, t_idx + 1, q_counter, sess, "MAT", "জীববিজ্ঞান"))
        q_counter += 1
    for q in all_chem[:25]:
        test_questions.append(normalize_q(q, t_idx + 1, q_counter, sess, "MAT", "রসায়ন"))
        q_counter += 1
    for q in all_phys[:20]:
        test_questions.append(normalize_q(q, t_idx + 1, q_counter, sess, "MAT", "পদার্থবিজ্ঞান"))
        q_counter += 1
    for q in all_eng[:15]:
        test_questions.append(normalize_q(q, t_idx + 1, q_counter, sess, "MAT", "ইংরেজি"))
        q_counter += 1
    for q in all_gk[:10]:
        test_questions.append(normalize_q(q, t_idx + 1, q_counter, sess, "MAT", "সাধারণ জ্ঞান"))
        q_counter += 1
        
    medical_past_tests.append({
        "test_id": t_idx + 1,
        "test_code": f"MAT-PAST-{sess[:4]}",
        "session": sess,
        "title": f"মেডিকেল ভর্তি পরীক্ষা: বিগত ১৫ বছর সেশন {sess}",
        "stream": "medical",
        "total_questions": len(test_questions),
        "duration_minutes": 60,
        "questions": test_questions
    })

print(f"Built {len(medical_past_tests)} Medical past tests. Total questions: {sum(len(t['questions']) for t in medical_past_tests)}")

# ==========================================
# 3. Build 15 Versity Tests (100 Qs each)
# ==========================================
# Distribution: Phys=25, Chem=25, Math=25, Bio=25 (Total=100)
versity_past_tests = []
v_phys_offset = phys_offset
v_chem_offset = chem_offset
v_bio_offset = bio_offset
v_math_offset = 0

for t_idx, sess in enumerate(sessions):
    v_phys = phys_pool[v_phys_offset : v_phys_offset + 25]
    v_phys_offset += 25
    v_chem = chem_pool[v_chem_offset : v_chem_offset + 25]
    v_chem_offset += 25
    v_math = math_pool[v_math_offset : v_math_offset + 25]
    v_math_offset += 25
    v_bio = bio_pool[v_bio_offset : v_bio_offset + 25]
    v_bio_offset += 25
    
    test_questions = []
    q_counter = 1
    for q in v_phys:
        test_questions.append(normalize_q(q, t_idx + 1, q_counter, sess, "DU_KA", "পদার্থবিজ্ঞান"))
        q_counter += 1
    for q in v_chem:
        test_questions.append(normalize_q(q, t_idx + 1, q_counter, sess, "DU_KA", "রসায়ন"))
        q_counter += 1
    for q in v_math:
        test_questions.append(normalize_q(q, t_idx + 1, q_counter, sess, "DU_KA", "উচ্চতর গণিত"))
        q_counter += 1
    for q in v_bio:
        test_questions.append(normalize_q(q, t_idx + 1, q_counter, sess, "DU_KA", "জীববিজ্ঞান"))
        q_counter += 1

    versity_past_tests.append({
        "test_id": t_idx + 1,
        "test_code": f"DU-PAST-{sess[:4]}",
        "session": sess,
        "title": f"ভার্সিটি বিজ্ঞান 'ক' (DU/GST) বিগত ১৫ বছর: সেশন {sess}",
        "stream": "versity",
        "total_questions": len(test_questions),
        "duration_minutes": 60,
        "questions": test_questions
    })

print(f"Built {len(versity_past_tests)} Versity past tests. Total questions: {sum(len(t['questions']) for t in versity_past_tests)}")

# ==========================================
# 4. Save JSON outputs
# ==========================================
# Unified past_15years_tests.json
unified_data = {
    "medical": medical_past_tests,
    "versity": versity_past_tests
}
with open(os.path.join(BASE_DIR, 'past_15years_tests.json'), 'w', encoding='utf-8') as f:
    json.dump(unified_data, f, ensure_ascii=False, indent=2)

with open(os.path.join(BASE_DIR, 'past_15years_medical.json'), 'w', encoding='utf-8') as f:
    json.dump(medical_past_tests, f, ensure_ascii=False, indent=2)

with open(os.path.join(BASE_DIR, 'past_15years_versity.json'), 'w', encoding='utf-8') as f:
    json.dump(versity_past_tests, f, ensure_ascii=False, indent=2)

print("Saved past_15years_tests.json, past_15years_medical.json, past_15years_versity.json successfully!")
