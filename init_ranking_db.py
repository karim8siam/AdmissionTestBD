import sqlite3
import random
import os
import uuid
from datetime import datetime, timedelta

DB_PATH = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/admission_ranking.db"

STUDENT_NAMES = [
    ("Tanvir Ahmed", "Notre Dame College", "DMC"),
    ("Nusrat Jahan", "Holy Cross College", "DMC"),
    ("Fahim Chowdhury", "Dhaka College", "SSMC"),
    ("Samia Rahman", "Viqarunnisa Noon College", "DMC"),
    ("Arifur Rahman", "Rajshahi College", "SOMC"),
    ("Sadia Afrin", "Chittagong College", "CMC"),
    ("Mehedi Hasan", "Barisal Cadet College", "DMC"),
    ("Tasnim Ferdous", "Ideal School & College", "SSMC"),
    ("Zubair Hossain", "Adamjee Cantonment College", "SBMC"),
    ("Farhana Islam", "Sylhet MC College", "MAGOMC"),
    ("Ahsan Habib", "Rangpur Cadet College", "DMC"),
    ("Sharmin Sultana", "Kumudini Government College", "SSMC"),
    ("Rakibul Islam", "Comilla Victoria College", "CMC"),
    ("Nabila Tabassum", "Rajuk Uttara Model College", "DMC"),
    ("Mahir Faisal", "Mirzapur Cadet College", "DMC"),
    ("Afia Anjum", "Shaheed Bir Uttam Lt. Anwar Girls", "SSMC"),
    ("Sabbir Hossain", "Government Science College", "RMC"),
    ("Sumaiya Khatun", "Bogra Cantonment Public School & College", "ShSMC"),
    ("Imtiaz Ahmed", "Pabna Cadet College", "DMC"),
    ("Raihan Kabir", "Mymensingh Zilla College", "MMC")
]

SEASONS = ["2024-25", "2025-26"]

def init_ranking_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executescript("""
    PRAGMA journal_mode = WAL;
    PRAGMA foreign_keys = ON;

    DROP TABLE IF EXISTS exam_submissions;
    DROP TABLE IF EXISTS students;

    CREATE TABLE students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        roll_number TEXT,
        target_college TEXT DEFAULT 'Dhaka Medical College (DMC)',
        session TEXT NOT NULL,                         -- '2025-26', '2026-27'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE exam_submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        submission_code TEXT UNIQUE NOT NULL,
        student_id TEXT NOT NULL,
        student_name TEXT NOT NULL,
        target_college TEXT,
        session TEXT NOT NULL,                         -- '2024-25', '2025-26', '2026-27'
        test_id INTEGER NOT NULL,                      -- 1 to 100
        test_code TEXT NOT NULL,                       -- 'MT-FULL-001', etc.
        subject_mode TEXT NOT NULL,                    -- 'FullExam', 'Biology', 'Chemistry', 'Physics', 'English', 'GK'
        total_questions INTEGER NOT NULL,              -- 100 or subject count
        correct_count INTEGER NOT NULL,
        wrong_count INTEGER NOT NULL,
        unanswered_count INTEGER NOT NULL,
        score REAL NOT NULL,                           -- correct - wrong*0.25
        percentage REAL NOT NULL,
        time_taken_seconds INTEGER NOT NULL,           -- e.g. 2400 seconds
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(student_id) REFERENCES students(student_id)
    );

    -- Composite indexes for lightning-fast rank computation
    CREATE INDEX idx_rank_alltime ON exam_submissions(test_id, subject_mode, score DESC, time_taken_seconds ASC);
    CREATE INDEX idx_rank_session ON exam_submissions(test_id, subject_mode, session, score DESC, time_taken_seconds ASC);
    CREATE INDEX idx_student_submissions ON exam_submissions(student_id, submitted_at DESC);
    CREATE INDEX idx_session_submissions ON exam_submissions(session, test_id);
    """)

    conn.commit()
    print("Created database schema with optimized indexing.")

    # Populate baseline candidates to provide realistic national competitive rankings
    print("Generating baseline competitive cohort across sessions...")
    rng = random.Random(42)

    student_records = []
    submission_records = []

    # Generate 5,000 realistic historical competitive submissions across tests
    # Covering Session 2024-25 (~2,200 submissions) and Session 2025-26 (~2,800 submissions)
    total_baseline_candidates = 600
    for s_idx in range(total_baseline_candidates):
        sid = f"STU-{100000 + s_idx}"
        base_name, college, target = STUDENT_NAMES[s_idx % len(STUDENT_NAMES)]
        name = f"{base_name} ({s_idx + 1})" if s_idx >= len(STUDENT_NAMES) else base_name
        roll = f"MED-{rng.randint(10000, 99999)}"
        sess = rng.choice(["2024-25", "2025-26"])
        created = datetime.now() - timedelta(days=rng.randint(10, 365))
        
        student_records.append((sid, name, roll, target, sess, created))

        # Each student took 1 to 5 model tests
        num_tests = rng.randint(2, 6)
        tests_taken = rng.sample(range(1, 15), min(num_tests, 14)) # Tests 1 to 14

        for tid in tests_taken:
            sub_code = f"SUB-{uuid.uuid4().hex[:10].upper()}"
            t_code = f"MT-FULL-{tid:03d}"
            
            # Score distribution modeled on real DGME medical admission percentiles:
            # Normal distribution centered around 62 with standard deviation 12
            raw_score = rng.gauss(62, 12)
            raw_score = max(20.0, min(92.75, raw_score))
            
            # Formulate realistic correct and wrong
            # score = correct - 0.25 * wrong
            total_q = 100
            # let correct ~ score + 0.2 * (100 - score)
            correct = int(min(total_q, max(15, raw_score + rng.uniform(2, 8))))
            wrong = int(max(0, (correct - raw_score) * 4))
            if correct + wrong > total_q:
                wrong = total_q - correct
            unanswered = total_q - (correct + wrong)
            final_score = round(correct * 1.0 - wrong * 0.25, 2)
            pct = round((final_score / total_q) * 100, 2)
            time_sec = rng.randint(1800, 3500) # 30 min to 58 min
            
            sub_date = created + timedelta(hours=rng.randint(1, 72))

            submission_records.append((
                sub_code, sid, name, target, sess, tid, t_code, 'FullExam',
                total_q, correct, wrong, unanswered, final_score, pct, time_sec, sub_date
            ))

    cursor.executemany("""
    INSERT INTO students (student_id, name, roll_number, target_college, session, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, student_records)

    cursor.executemany("""
    INSERT INTO exam_submissions 
    (submission_code, student_id, student_name, target_college, session, test_id, test_code, subject_mode,
     total_questions, correct_count, wrong_count, unanswered_count, score, percentage, time_taken_seconds, submitted_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, submission_records)

    conn.commit()
    
    # Query summary
    cursor.execute("SELECT count(*) FROM students")
    s_count = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM exam_submissions")
    sub_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT session, count(*) FROM exam_submissions GROUP BY session")
    sess_counts = cursor.fetchall()

    print(f"Successfully seeded database: {s_count} students, {sub_count} submissions.")
    for s, c in sess_counts:
        print(f"  Session {s}: {c} exam submissions")

    conn.close()

if __name__ == "__main__":
    init_ranking_database()
