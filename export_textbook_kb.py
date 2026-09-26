import sqlite3
import json
import csv
from init_textbook_db import TEXTBOOK_DB_PATH

def export_kb():
    conn = sqlite3.connect(TEXTBOOK_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch all knowledge units with book and chapter details
    cursor.execute("""
        SELECT k.id, k.subject, b.title_bn as book_name, b.author, c.chapter_name_bn as chapter,
               k.topic, k.fact_type, k.exact_text_bn, k.context_en, k.keywords, k.citation,
               k.high_yield_priority, k.common_mcq_trap
        FROM knowledge_units k
        JOIN books b ON k.book_id = b.id
        JOIN book_chapters c ON k.chapter_id = c.id
        ORDER BY k.subject, c.chapter_num
    """)
    rows = [dict(r) for r in cursor.fetchall()]

    json_path = '/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/medical_textbooks_kb.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(rows)} textbook knowledge units to {json_path}")

    csv_path = '/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/medical_textbooks_kb.csv'
    if rows:
        headers = rows[0].keys()
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Exported textbook knowledge units to CSV at {csv_path}")

    conn.close()

if __name__ == '__main__':
    export_kb()
