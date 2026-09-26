import sqlite3
import os

DB_PATH = '/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/medical_15years.db'

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session TEXT UNIQUE NOT NULL,            -- e.g. '2023-2024', '2022-2023'
    exam_name TEXT NOT NULL,                -- 'MBBS Admission Test'
    exam_date TEXT,
    total_marks INTEGER DEFAULT 100,
    total_questions INTEGER DEFAULT 100,
    biology_marks INTEGER DEFAULT 30,
    chemistry_marks INTEGER DEFAULT 25,
    physics_marks INTEGER DEFAULT 20,
    english_marks INTEGER DEFAULT 15,
    gk_marks INTEGER DEFAULT 10,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    paper TEXT,
    chapter_num INTEGER,
    chapter_name_bn TEXT NOT NULL,
    chapter_name_en TEXT,
    high_yield_rank INTEGER DEFAULT 3
);

CREATE TABLE IF NOT EXISTS questions (
    id TEXT PRIMARY KEY,
    session TEXT NOT NULL,
    exam_type TEXT DEFAULT 'MBBS',
    question_num INTEGER NOT NULL,
    subject TEXT NOT NULL,
    sub_discipline TEXT,
    chapter TEXT,
    question_bn TEXT NOT NULL,
    question_en TEXT,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_option TEXT NOT NULL,
    correct_index INTEGER NOT NULL,
    explanation TEXT,
    book_reference TEXT,
    difficulty TEXT DEFAULT 'Medium',
    is_repeated INTEGER DEFAULT 0,
    repeat_source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session) REFERENCES exams(session)
);

CREATE INDEX IF NOT EXISTS idx_questions_session ON questions(session);
CREATE INDEX IF NOT EXISTS idx_questions_subject ON questions(subject);
CREATE INDEX IF NOT EXISTS idx_questions_chapter ON questions(chapter);
CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions(difficulty);

CREATE VIRTUAL TABLE IF NOT EXISTS questions_fts USING fts5(
    id UNINDEXED,
    question_bn,
    option_a,
    option_b,
    option_c,
    option_d,
    explanation,
    subject,
    chapter,
    tokenize='unicode61'
);

CREATE TRIGGER IF NOT EXISTS questions_ai AFTER INSERT ON questions BEGIN
    INSERT INTO questions_fts(id, question_bn, option_a, option_b, option_c, option_d, explanation, subject, chapter)
    VALUES (new.id, new.question_bn, new.option_a, new.option_b, new.option_c, new.option_d, new.explanation, new.subject, new.chapter);
END;

CREATE TRIGGER IF NOT EXISTS questions_ad AFTER DELETE ON questions BEGIN
    DELETE FROM questions_fts WHERE id = old.id;
END;
"""

def init_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    print(f"Database initialized successfully at: {DB_PATH}")

if __name__ == '__main__':
    init_database()
