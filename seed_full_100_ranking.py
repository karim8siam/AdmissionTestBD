import sqlite3
import random
import uuid

DB_PATH = "data/admission_ranking.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

FIRST_NAMES = [
    "তানভীর", "নুসরাত", "ফাহিম", "সামিয়া", "আরিফুর", "সাদিয়া", "মেহেদী", "তাসনিম",
    "জুবায়ের", "ফারহানা", "আহসান", "শারমিন", "রাকিবুল", "নাবিলা", "মাহির", "আফিয়া",
    "সাব্বির", "সুমাইয়া", "ইমতিয়াজ", "রায়হান", "সাকিব", "তাহমিদ", "আবরার", "ফাইরুজ",
    "নাফিসা", "শাওন", "মুন্না", "আনিকা", "জারিন", "ইশতিয়াক"
]
LAST_NAMES = [
    "আহমেদ", "জাহান", "চৌধুরী", "রহমান", "হাসান", "ফেরদৌস", "হোসেন", "ইসলাম",
    "হাবিব", "সুলতানা", "ফয়সাল", "আনজুম", "খাতুন", "কবীর", "খান", "মাহমুদ"
]

SEASONS = ["2024-25", "2025-26", "2026-27"]
MODES = ["FullExam", "GSTExam"]

print("Seeding all 100 tests for Medical (FullExam) and Varsity (GSTExam)...")

records_to_insert = []
students_to_insert = []

for mode in MODES:
    max_q = 100
    for test_id in range(1, 101):
        # Check how many submissions already exist
        c.execute("SELECT COUNT(*) FROM exam_submissions WHERE test_id = ? AND subject_mode = ?", (test_id, mode))
        existing_cnt = c.fetchone()[0]
        needed = max(0, 35 - existing_cnt)
        
        for _ in range(needed):
            stu_id = f"STU-{uuid.uuid4().hex[:8].upper()}"
            fn = random.choice(FIRST_NAMES)
            ln = random.choice(LAST_NAMES)
            name = f"{fn} {ln}"
            sess = random.choice(SEASONS)
            college = "Dhaka Medical College (DMC)" if mode == "FullExam" else "Dhaka University (DU)"
            
            # Realistic bell-curve score distribution: mean around 72, std 12
            raw_score = random.gauss(72, 12)
            raw_score = max(30.0, min(96.0, raw_score))
            score = round(raw_score, 2)
            
            correct = int(score + random.randint(2, 6))
            correct = min(max_q, max(35, correct))
            wrong = int((correct - score) / 0.25)
            wrong = min(max_q - correct, max(0, wrong))
            unanswered = max(0, max_q - correct - wrong)
            actual_score = round(correct - (wrong * 0.25), 2)
            
            percentage = round((actual_score / max_q) * 100, 2)
            time_taken = random.randint(1800, 3550) # 30 min to 59 min
            sub_code = f"SUB-{uuid.uuid4().hex[:10].upper()}"
            test_code = f"MED-{test_id:03d}" if mode == "FullExam" else f"VAR-{test_id:03d}"
            
            students_to_insert.append((stu_id, name, f"ROLL-{random.randint(10000, 99999)}", college, sess))
            records_to_insert.append((
                sub_code, stu_id, name, college, sess, test_id, test_code, mode,
                max_q, correct, wrong, unanswered, actual_score, percentage, time_taken
            ))

print(f"Generated {len(records_to_insert)} new submissions.")

# Insert students
c.executemany("""
    INSERT OR IGNORE INTO students (student_id, name, roll_number, target_college, session)
    VALUES (?, ?, ?, ?, ?)
""", students_to_insert)

# Insert submissions
c.executemany("""
    INSERT INTO exam_submissions
    (submission_code, student_id, student_name, target_college, session, test_id, test_code, subject_mode,
     total_questions, correct_count, wrong_count, unanswered_count, score, percentage, time_taken_seconds)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", records_to_insert)

conn.commit()

total_sub = c.execute("SELECT COUNT(*) FROM exam_submissions").fetchone()[0]
print(f"Total submissions in DB now: {total_sub}")
conn.close()
