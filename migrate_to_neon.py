import sqlite3
import psycopg2
import psycopg2.extras
import os

NEON_URL = "postgresql://neondb_owner:npg_YIR9cGa5MqOP@ep-spring-lake-b45687pc-pooler.c-6.us-east-2.aws.neon.tech/neondb?sslmode=require"
SQLITE_PATH = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/admission_ranking.db"

print("Connecting to Neon PostgreSQL...")
neon_conn = psycopg2.connect(NEON_URL)
neon_cur = neon_conn.cursor()

print("Recreating clean schema in Neon PostgreSQL...")
neon_cur.execute("""
DROP TABLE IF EXISTS exam_submissions CASCADE;
DROP TABLE IF EXISTS students CASCADE;

CREATE TABLE students (
    student_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    roll_number VARCHAR(64),
    target_college VARCHAR(255) DEFAULT 'Dhaka Medical College (DMC)',
    session VARCHAR(32) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE exam_submissions (
    id SERIAL PRIMARY KEY,
    submission_code VARCHAR(64) UNIQUE NOT NULL,
    student_id VARCHAR(64) NOT NULL,
    student_name VARCHAR(255) NOT NULL,
    target_college VARCHAR(255),
    session VARCHAR(32) NOT NULL,
    test_id INTEGER NOT NULL,
    test_code VARCHAR(64) NOT NULL,
    subject_mode VARCHAR(64) NOT NULL,
    total_questions INTEGER NOT NULL,
    correct_count INTEGER NOT NULL,
    wrong_count INTEGER NOT NULL,
    unanswered_count INTEGER NOT NULL,
    score NUMERIC(6, 2) NOT NULL,
    percentage NUMERIC(6, 2) NOT NULL,
    time_taken_seconds INTEGER NOT NULL,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_neon_rank_alltime ON exam_submissions(test_id, subject_mode, score DESC, time_taken_seconds ASC);
CREATE INDEX idx_neon_rank_session ON exam_submissions(test_id, subject_mode, session, score DESC, time_taken_seconds ASC);
CREATE INDEX idx_neon_student_subs ON exam_submissions(student_id, submitted_at DESC);
CREATE INDEX idx_neon_session_test ON exam_submissions(session, test_id);
""")
neon_conn.commit()
print("✓ Schema and indexes created successfully in Neon!")

if os.path.exists(SQLITE_PATH):
    print("Reading data from SQLite admission_ranking.db...")
    sqlite_conn = sqlite3.connect(SQLITE_PATH)
    sqlite_conn.row_factory = sqlite3.Row
    sq_cur = sqlite_conn.cursor()

    # 1. Fetch Submissions
    sq_cur.execute("""
        SELECT submission_code, student_id, student_name, target_college, session,
               test_id, test_code, subject_mode, total_questions, correct_count,
               wrong_count, unanswered_count, score, percentage, time_taken_seconds, submitted_at
        FROM exam_submissions;
    """)
    submissions = [dict(r) for r in sq_cur.fetchall()]

    # 2. Fetch Students
    sq_cur.execute("SELECT student_id, name, roll_number, target_college, session, created_at FROM students;")
    students_dict = {r["student_id"]: dict(r) for r in sq_cur.fetchall()}

    # Ensure all students in submissions exist in students_dict
    for s in submissions:
        sid = s["student_id"]
        if sid not in students_dict:
            students_dict[sid] = {
                "student_id": sid,
                "name": s["student_name"],
                "roll_number": "ROLL-000",
                "target_college": s["target_college"] or "Dhaka Medical College (DMC)",
                "session": s["session"],
                "created_at": s["submitted_at"]
            }

    print(f"Migrating {len(students_dict)} students to Neon...")
    student_records = [
        (s["student_id"], s["name"], s["roll_number"], s["target_college"], s["session"], s["created_at"])
        for s in students_dict.values()
    ]
    psycopg2.extras.execute_batch(neon_cur, """
        INSERT INTO students (student_id, name, roll_number, target_college, session, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (student_id) DO NOTHING;
    """, student_records, page_size=1000)
    neon_conn.commit()

    print(f"Migrating {len(submissions)} exam submissions to Neon...")
    sub_records = [
        (
            s["submission_code"], s["student_id"], s["student_name"], s["target_college"],
            s["session"], s["test_id"], s["test_code"], s["subject_mode"], s["total_questions"],
            s["correct_count"], s["wrong_count"], s["unanswered_count"], s["score"],
            s["percentage"], s["time_taken_seconds"], s["submitted_at"]
        )
        for s in submissions
    ]
    psycopg2.extras.execute_batch(neon_cur, """
        INSERT INTO exam_submissions
        (submission_code, student_id, student_name, target_college, session,
         test_id, test_code, subject_mode, total_questions, correct_count,
         wrong_count, unanswered_count, score, percentage, time_taken_seconds, submitted_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (submission_code) DO NOTHING;
    """, sub_records, page_size=1000)
    neon_conn.commit()
    sqlite_conn.close()

# Verify in Neon
neon_cur.execute("SELECT COUNT(*) FROM students;")
total_students = neon_cur.fetchone()[0]
neon_cur.execute("SELECT COUNT(*) FROM exam_submissions;")
total_subs = neon_cur.fetchone()[0]
neon_cur.execute("SELECT session, COUNT(*) FROM exam_submissions GROUP BY session ORDER BY session;")
session_stats = neon_cur.fetchall()

print("\n================ Neon PostgreSQL Verification ================")
print(f"✓ Total Students in Neon: {total_students}")
print(f"✓ Total Submissions in Neon: {total_subs}")
print("Submissions by Session:")
for sess, cnt in session_stats:
    print(f"  • {sess}: {cnt} submissions")

# Test live ranking query on Neon PostgreSQL
neon_cur.execute("""
    SELECT COUNT(*) + 1 FROM exam_submissions
    WHERE test_id = 1 AND subject_mode = 'FullExam' AND session = '2025-26'
      AND (score > 80.0 OR (score = 80.0 AND time_taken_seconds < 2400));
""")
sample_rank = neon_cur.fetchone()[0]
print(f"✓ Sample Live Rank computation for Score 80.0 on Neon: Rank #{sample_rank}")
print("==============================================================")

neon_conn.close()
