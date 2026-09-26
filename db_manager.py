import sqlite3
import json
import csv
import os
from typing import List, Dict, Any, Optional

DB_PATH = '/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/medical_15years.db'

class MedicalDBManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def insert_exam(self, exam_data: Dict[str, Any]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO exams 
                (session, exam_name, exam_date, total_marks, total_questions, biology_marks, chemistry_marks, physics_marks, english_marks, gk_marks, notes)
                VALUES (:session, :exam_name, :exam_date, :total_marks, :total_questions, :biology_marks, :chemistry_marks, :physics_marks, :english_marks, :gk_marks, :notes)
            """, exam_data)
            conn.commit()

    def insert_question(self, q: Dict[str, Any]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO questions
                (id, session, exam_type, question_num, subject, sub_discipline, chapter, 
                 question_bn, question_en, option_a, option_b, option_c, option_d, 
                 correct_option, correct_index, explanation, book_reference, difficulty, is_repeated, repeat_source)
                VALUES 
                (:id, :session, :exam_type, :question_num, :subject, :sub_discipline, :chapter,
                 :question_bn, :question_en, :option_a, :option_b, :option_c, :option_d,
                 :correct_option, :correct_index, :explanation, :book_reference, :difficulty, :is_repeated, :repeat_source)
            """, q)
            conn.commit()

    def bulk_insert_questions(self, questions: List[Dict[str, Any]]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany("""
                INSERT OR REPLACE INTO questions
                (id, session, exam_type, question_num, subject, sub_discipline, chapter, 
                 question_bn, question_en, option_a, option_b, option_c, option_d, 
                 correct_option, correct_index, explanation, book_reference, difficulty, is_repeated, repeat_source)
                VALUES 
                (:id, :session, :exam_type, :question_num, :subject, :sub_discipline, :chapter,
                 :question_bn, :question_en, :option_a, :option_b, :option_c, :option_d,
                 :correct_option, :correct_index, :explanation, :book_reference, :difficulty, :is_repeated, :repeat_source)
            """, questions)
            conn.commit()

    def get_all_sessions(self) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT session FROM exams ORDER BY session DESC")
            return [r[0] for r in cursor.fetchall()]

    def get_questions_by_session(self, session: str) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM questions 
                WHERE session = ? 
                ORDER BY question_num ASC
            """, (session,))
            return [dict(r) for r in cursor.fetchall()]

    def get_questions_by_subject(self, subject: str, limit: int = 100) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM questions 
                WHERE subject LIKE ? 
                ORDER BY session DESC, question_num ASC
                LIMIT ?
            """, (f"%{subject}%", limit))
            return [dict(r) for r in cursor.fetchall()]

    def search_fts(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Search using SQLite FTS5
            cursor.execute("""
                SELECT q.* 
                FROM questions_fts f
                JOIN questions q ON f.id = q.id
                WHERE questions_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, limit))
            return [dict(r) for r in cursor.fetchall()]

    def get_analytics(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total questions
            cursor.execute("SELECT COUNT(*) FROM questions")
            total_questions = cursor.fetchone()[0]

            # By Subject
            cursor.execute("SELECT subject, COUNT(*) as cnt FROM questions GROUP BY subject ORDER BY cnt DESC")
            by_subject = {r['subject']: r['cnt'] for r in cursor.fetchall()}

            # By Session
            cursor.execute("SELECT session, COUNT(*) as cnt FROM questions GROUP BY session ORDER BY session DESC")
            by_session = {r['session']: r['cnt'] for r in cursor.fetchall()}

            # Top Chapters
            cursor.execute("""
                SELECT chapter, subject, COUNT(*) as cnt 
                FROM questions 
                WHERE chapter IS NOT NULL AND chapter != ''
                GROUP BY chapter, subject 
                ORDER BY cnt DESC 
                LIMIT 15
            """)
            top_chapters = [dict(r) for r in cursor.fetchall()]

            # Repeat Questions Count
            cursor.execute("SELECT COUNT(*) FROM questions WHERE is_repeated = 1")
            repeat_count = cursor.fetchone()[0]

            # Difficulty
            cursor.execute("SELECT difficulty, COUNT(*) as cnt FROM questions GROUP BY difficulty")
            by_difficulty = {r['difficulty']: r['cnt'] for r in cursor.fetchall()}

            return {
                "total_questions": total_questions,
                "sessions_count": len(by_session),
                "by_subject": by_subject,
                "by_session": by_session,
                "top_chapters": top_chapters,
                "repeat_questions": repeat_count,
                "repeat_percentage": round((repeat_count / total_questions * 100), 2) if total_questions > 0 else 0,
                "by_difficulty": by_difficulty
            }

    def export_to_json(self, output_path: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM questions ORDER BY session DESC, question_num ASC")
            rows = [dict(r) for r in cursor.fetchall()]
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(rows, f, ensure_ascii=False, indent=2)
            print(f"Exported {len(rows)} questions to {output_path}")

    def export_to_csv(self, output_path: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM questions ORDER BY session DESC, question_num ASC")
            rows = cursor.fetchall()
            if not rows:
                print("No questions to export.")
                return
            headers = rows[0].keys()
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for r in rows:
                    writer.writerow(tuple(r))
            print(f"Exported {len(rows)} questions to CSV at {output_path}")

if __name__ == '__main__':
    db = MedicalDBManager()
    print("DB Manager initialized successfully.")
    print("Analytics:", db.get_analytics())
