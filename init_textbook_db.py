import sqlite3
import os

TEXTBOOK_DB_PATH = '/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/medical_textbooks_kb.db'

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- 1. Master Books Table
CREATE TABLE IF NOT EXISTS books (
    id TEXT PRIMARY KEY,                       -- e.g. 'BOOK-BIO-HASAN', 'BOOK-CHEM-HAZARI-1'
    title_bn TEXT NOT NULL,                    -- e.g. 'উচ্চ মাধ্যমিক উদ্ভিদবিজ্ঞান'
    title_en TEXT NOT NULL,                    -- e.g. 'Higher Secondary Botany'
    author TEXT NOT NULL,                      -- e.g. 'ড. মোহাম্মদ আবুল হাসান'
    subject TEXT NOT NULL,                     -- Biology, Chemistry, Physics, English, General Knowledge
    paper TEXT,                                -- 1st Paper, 2nd Paper, etc.
    publisher TEXT,                            -- e.g. 'হাসান বুক হাউস', 'রয়্যাল বুক ডিপো'
    edition TEXT,                              -- e.g. 'Latest NCTB Approved Medical Standard Edition'
    total_chapters INTEGER NOT NULL,
    importance_note TEXT
);

-- 2. Book Chapters Table
CREATE TABLE IF NOT EXISTS book_chapters (
    id TEXT PRIMARY KEY,                       -- e.g. 'HASAN-CH-01'
    book_id TEXT NOT NULL,
    chapter_num INTEGER NOT NULL,
    chapter_name_bn TEXT NOT NULL,             -- e.g. 'কোষ ও এর গঠন'
    chapter_name_en TEXT NOT NULL,             -- e.g. 'Cell and its structure'
    high_yield_score INTEGER DEFAULT 5,        -- 1 to 5 (5 = ultra high yield in DGME exams)
    estimated_exam_weight TEXT,                -- e.g. '2-3 questions per exam'
    FOREIGN KEY(book_id) REFERENCES books(id)
);

-- 3. High-Precision Textbook Knowledge Units (Atomic Facts, Tables, Scientific Names, Exceptions)
CREATE TABLE IF NOT EXISTS knowledge_units (
    id TEXT PRIMARY KEY,                       -- e.g. 'KU-BIO-HASAN-001'
    book_id TEXT NOT NULL,
    chapter_id TEXT NOT NULL,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,                       -- e.g. 'মাইটোকন্ড্রিয়া (Mitochondria)'
    fact_type TEXT NOT NULL,                   -- 'Definition', 'Table_Chart', 'Scientific_Value', 'Exception', 'Discovery', 'Reaction_Mechanism', 'End_Chapter_MCQ'
    exact_text_bn TEXT NOT NULL,               -- Exact statement from textbook in Bengali
    context_en TEXT,                           -- English translation / conceptual summary
    keywords TEXT NOT NULL,                    -- Searchable comma-separated terms (Bengali & English)
    citation TEXT NOT NULL,                    -- Exact citation e.g. 'আবুল হাসান, অধ্যায় ১, অনুচ্ছেদ ১.৩'
    high_yield_priority INTEGER DEFAULT 5,     -- 1 to 5
    common_mcq_trap TEXT,                      -- Common distractor or misconception tested in medical exams
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(book_id) REFERENCES books(id),
    FOREIGN KEY(chapter_id) REFERENCES book_chapters(id)
);

CREATE INDEX IF NOT EXISTS idx_ku_book ON knowledge_units(book_id);
CREATE INDEX IF NOT EXISTS idx_ku_chapter ON knowledge_units(chapter_id);
CREATE INDEX IF NOT EXISTS idx_ku_subject ON knowledge_units(subject);
CREATE INDEX IF NOT EXISTS idx_ku_topic ON knowledge_units(topic);
CREATE INDEX IF NOT EXISTS idx_ku_fact_type ON knowledge_units(fact_type);

-- 4. Full-Text Search (FTS5) for knowledge units
CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_units_fts USING fts5(
    id UNINDEXED,
    exact_text_bn,
    context_en,
    topic,
    keywords,
    citation,
    tokenize='unicode61'
);

-- Triggers to synchronize FTS
CREATE TRIGGER IF NOT EXISTS ku_ai AFTER INSERT ON knowledge_units BEGIN
    INSERT INTO knowledge_units_fts(id, exact_text_bn, context_en, topic, keywords, citation)
    VALUES (new.id, new.exact_text_bn, new.context_en, new.topic, new.keywords, new.citation);
END;

CREATE TRIGGER IF NOT EXISTS ku_ad AFTER DELETE ON knowledge_units BEGIN
    DELETE FROM knowledge_units_fts WHERE id = old.id;
END;
"""

def init_textbook_database():
    os.makedirs(os.path.dirname(TEXTBOOK_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(TEXTBOOK_DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    print(f"Textbook Knowledge Base Database initialized at: {TEXTBOOK_DB_PATH}")

if __name__ == '__main__':
    init_textbook_database()
