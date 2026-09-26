import http.server
import socketserver
import os
import sys
import json
import sqlite3
import psycopg2
import psycopg2.extras
import uuid
import urllib.parse
import re
import decimal
from datetime import datetime, date

PORT = 8080
BASE_DIR = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series"
DB_PATH = os.path.join(BASE_DIR, "data", "admission_ranking.db")
NEON_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_YIR9cGa5MqOP@ep-spring-lake-b45687pc-pooler.c-6.us-east-2.aws.neon.tech/neondb?sslmode=require"
)

def parse_bkash_sms(text):
    """
    Parses official bKash incoming SMS for payment verification.
    Common formats:
    - 'You have received Tk 499.00 from 01644265766. Ref ... Fee Tk 0.00. Balance Tk ... TrxID 9K27X89 at 26/09/2026 05:30'
    - 'You have received Tk 499 from 01712345678. Ref Admission. Fee Tk 0.00. Balance Tk 10499.00. TrxID BL7A2X99 at 26/09/2026'
    - 'Received Tk 499.00 from 01812345678. TrxID 8A291ZX'
    """
    if not text:
        return None
    amount = None
    amt_match = re.search(r'(?:received|recharge)\s+(?:tk\.?|bdt)?\s*([0-9,]+(?:\.[0-9]{1,2})?)', text, re.IGNORECASE)
    if amt_match:
        try:
            amount = float(amt_match.group(1).replace(',', ''))
        except ValueError:
            pass

    sender = None
    sender_match = re.search(r'from\s+(01[3-9]\d{8})', text, re.IGNORECASE)
    if sender_match:
        sender = sender_match.group(1)

    trx_id = None
    trx_match = re.search(r'TrxID[:\s]+([A-Z0-9]{6,16})', text, re.IGNORECASE)
    if trx_match:
        trx_id = trx_match.group(1).strip().upper()

    if trx_id:
        return {
            "amount": amount or 0.0,
            "sender": sender or "unknown",
            "trx_id": trx_id,
            "raw": text
        }
    return None

def ensure_database_schema(conn, db_type):
    """Ensures payment and submission tables exist."""
    try:
        c = conn.cursor()
        if db_type == 'postgres':
            c.execute("""
                CREATE TABLE IF NOT EXISTS received_sms_logs (
                    id SERIAL PRIMARY KEY,
                    sender VARCHAR(32) NOT NULL,
                    raw_message TEXT NOT NULL,
                    parsed_amount NUMERIC(10, 2),
                    parsed_sender VARCHAR(32),
                    parsed_trx_id VARCHAR(64) UNIQUE,
                    is_claimed BOOLEAN DEFAULT FALSE,
                    claimed_by_student_id VARCHAR(64),
                    received_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS student_enrollments (
                    id SERIAL PRIMARY KEY,
                    student_id VARCHAR(64) NOT NULL,
                    student_name VARCHAR(255),
                    package_type VARCHAR(32) NOT NULL,
                    amount NUMERIC(10, 2) NOT NULL,
                    sender_number VARCHAR(32) NOT NULL,
                    trx_id VARCHAR(64) UNIQUE NOT NULL,
                    status VARCHAR(32) DEFAULT 'verified',
                    enrolled_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
        else:
            c.execute("""
                CREATE TABLE IF NOT EXISTS received_sms_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    raw_message TEXT NOT NULL,
                    parsed_amount REAL,
                    parsed_sender TEXT,
                    parsed_trx_id TEXT UNIQUE,
                    is_claimed INTEGER DEFAULT 0,
                    claimed_by_student_id TEXT,
                    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS student_enrollments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    student_name TEXT,
                    package_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    sender_number TEXT NOT NULL,
                    trx_id TEXT UNIQUE NOT NULL,
                    status TEXT DEFAULT 'verified',
                    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        conn.commit()
    except Exception as e:
        print(f"[WARN] Error ensuring schema: {e}")

def get_db_connection():
    """Returns a database connection and its type ('postgres' or 'sqlite')."""
    try:
        conn = psycopg2.connect(NEON_URL, connect_timeout=5)
        return conn, 'postgres'
    except Exception as e:
        print(f"[WARN] Neon PostgreSQL connection error: {e}. Falling back to SQLite.")
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn, 'sqlite'

class AdmissionApiHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)

        if path == '/' or path == '':
            self.path = '/web/index.html'
            return super().do_GET()

        # API: Get Leaderboard
        if path == '/api/leaderboard':
            self.handle_get_leaderboard(query)
            return

        # API: Platform Stats
        if path == '/api/stats':
            self.handle_get_stats()
            return

        # API: Payment Status
        if path == '/api/payment/status':
            self.handle_payment_status(query)
            return

        return super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == '/api/submit-exam':
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(post_body)
                self.handle_submit_exam(data)
            except Exception as e:
                self.send_json_response({"status": "error", "message": str(e)}, status=400)
            return

        if path == '/api/payment/sms-webhook':
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length).decode('utf-8')
            try:
                try:
                    data = json.loads(post_body)
                except Exception:
                    data = {k: v[0] for k, v in urllib.parse.parse_qs(post_body).items()}
                self.handle_sms_webhook(data)
            except Exception as e:
                self.send_json_response({"status": "error", "message": str(e)}, status=400)
            return

        if path == '/api/payment/verify-trx':
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(post_body)
                self.handle_verify_trx(data)
            except Exception as e:
                self.send_json_response({"status": "error", "message": str(e)}, status=400)
            return

        self.send_json_response({"status": "error", "message": "Endpoint not found"}, status=404)

    def send_json_response(self, data, status=200):
        def default_serializer(o):
            if hasattr(o, 'isoformat'):
                return o.isoformat()
            if isinstance(o, decimal.Decimal):
                return float(o)
            return str(o)

        response_bytes = json.dumps(data, ensure_ascii=False, default=default_serializer).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(response_bytes)
        self.close_connection = True

    def handle_submit_exam(self, data):
        student_name = data.get('student_name', 'পরীক্ষার্থী').strip() or 'পরীক্ষার্থী'
        student_id = data.get('student_id') or f"STU-{uuid.uuid4().hex[:8].upper()}"
        roll = data.get('roll_number', 'ROLL-2025')
        target = data.get('target_college', 'জাতীয় মেধা তালিকা')
        session = data.get('session', '2025-26')
        try:
            test_id = int(data.get('test_id', 1))
        except (ValueError, TypeError):
            test_id = 1
        test_code = data.get('test_code', f"MT-FULL-{test_id:03d}")
        subject_mode = data.get('subject_mode', 'FullExam')
        try:
            total_questions = max(1, int(data.get('total_questions', 100)))
        except (ValueError, TypeError):
            total_questions = 100
        try:
            correct_count = max(0, int(data.get('correct_count', 0)))
        except (ValueError, TypeError):
            correct_count = 0
        try:
            wrong_count = max(0, int(data.get('wrong_count', 0)))
        except (ValueError, TypeError):
            wrong_count = 0
        try:
            unanswered_count = max(0, int(data.get('unanswered_count', 0)))
        except (ValueError, TypeError):
            unanswered_count = 0
        try:
            score = float(data.get('score', 0.0))
            if str(score) == 'nan' or score != score:
                score = 0.0
        except (ValueError, TypeError):
            score = 0.0
        percentage = round((score / total_questions) * 100, 2) if total_questions > 0 else 0.0
        try:
            raw_time = data.get('time_taken_seconds')
            time_taken_seconds = int(float(raw_time)) if (raw_time is not None and str(raw_time) != 'nan') else 60
            if time_taken_seconds <= 0:
                time_taken_seconds = 1
        except (ValueError, TypeError):
            time_taken_seconds = 60
        submission_code = f"SUB-{uuid.uuid4().hex[:10].upper()}"

        conn, db_type = get_db_connection()

        try:
            if db_type == 'postgres':
                c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

                # Upsert student
                c.execute("""
                    INSERT INTO students (student_id, name, roll_number, target_college, session)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT(student_id) DO UPDATE SET
                        name=EXCLUDED.name,
                        roll_number=EXCLUDED.roll_number,
                        target_college=EXCLUDED.target_college,
                        session=EXCLUDED.session;
                """, (student_id, student_name, roll, target, session))

                # Insert submission
                c.execute("""
                    INSERT INTO exam_submissions
                    (submission_code, student_id, student_name, target_college, session, test_id, test_code, subject_mode,
                     total_questions, correct_count, wrong_count, unanswered_count, score, percentage, time_taken_seconds)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (submission_code, student_id, student_name, target, session, test_id, test_code, subject_mode,
                      total_questions, correct_count, wrong_count, unanswered_count, score, percentage, time_taken_seconds))
                conn.commit()

                # Session Rank
                c.execute("""
                    SELECT COUNT(*) + 1 AS rank FROM exam_submissions
                    WHERE test_id = %s AND subject_mode = %s AND session = %s
                      AND (score > %s OR (score = %s AND time_taken_seconds < %s));
                """, (test_id, subject_mode, session, score, score, time_taken_seconds))
                session_rank = c.fetchone()['rank']

                c.execute("SELECT COUNT(*) AS total FROM exam_submissions WHERE test_id = %s AND subject_mode = %s AND session = %s;",
                          (test_id, subject_mode, session))
                session_total = c.fetchone()['total']
                session_percentile = round(((session_total - session_rank) / session_total) * 100, 2) if session_total > 0 else 100.0

                # All-Time National Rank
                c.execute("""
                    SELECT COUNT(*) + 1 AS rank FROM exam_submissions
                    WHERE test_id = %s AND subject_mode = %s
                      AND (score > %s OR (score = %s AND time_taken_seconds < %s));
                """, (test_id, subject_mode, score, score, time_taken_seconds))
                all_time_rank = c.fetchone()['rank']

                c.execute("SELECT COUNT(*) AS total FROM exam_submissions WHERE test_id = %s AND subject_mode = %s;",
                          (test_id, subject_mode))
                all_time_total = c.fetchone()['total']
                all_time_percentile = round(((all_time_total - all_time_rank) / all_time_total) * 100, 2) if all_time_total > 0 else 100.0

                # Leaderboards
                c.execute("""
                    SELECT student_id, student_name, target_college, session, score, percentage, time_taken_seconds, submitted_at
                    FROM exam_submissions
                    WHERE test_id = %s AND subject_mode = %s AND session = %s
                    ORDER BY score DESC, time_taken_seconds ASC
                    LIMIT 10;
                """, (test_id, subject_mode, session))
                session_leaderboard = [dict(r) for r in c.fetchall()]

                c.execute("""
                    SELECT student_id, student_name, target_college, session, score, percentage, time_taken_seconds, submitted_at
                    FROM exam_submissions
                    WHERE test_id = %s AND subject_mode = %s
                    ORDER BY score DESC, time_taken_seconds ASC
                    LIMIT 10;
                """, (test_id, subject_mode))
                all_time_leaderboard = [dict(r) for r in c.fetchall()]

            else:
                # SQLite Fallback
                c = conn.cursor()
                c.execute("""
                    INSERT INTO students (student_id, name, roll_number, target_college, session)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(student_id) DO UPDATE SET
                        name=excluded.name,
                        roll_number=excluded.roll_number,
                        target_college=excluded.target_college,
                        session=excluded.session
                """, (student_id, student_name, roll, target, session))

                c.execute("""
                    INSERT INTO exam_submissions
                    (submission_code, student_id, student_name, target_college, session, test_id, test_code, subject_mode,
                     total_questions, correct_count, wrong_count, unanswered_count, score, percentage, time_taken_seconds)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (submission_code, student_id, student_name, target, session, test_id, test_code, subject_mode,
                      total_questions, correct_count, wrong_count, unanswered_count, score, percentage, time_taken_seconds))
                conn.commit()

                c.execute("""
                    SELECT COUNT(*) + 1 FROM exam_submissions
                    WHERE test_id = ? AND subject_mode = ? AND session = ?
                      AND (score > ? OR (score = ? AND time_taken_seconds < ?))
                """, (test_id, subject_mode, session, score, score, time_taken_seconds))
                session_rank = c.fetchone()[0]

                c.execute("SELECT COUNT(*) FROM exam_submissions WHERE test_id = ? AND subject_mode = ? AND session = ?",
                          (test_id, subject_mode, session))
                session_total = c.fetchone()[0]
                session_percentile = round(((session_total - session_rank) / session_total) * 100, 2) if session_total > 0 else 100.0

                c.execute("""
                    SELECT COUNT(*) + 1 FROM exam_submissions
                    WHERE test_id = ? AND subject_mode = ?
                      AND (score > ? OR (score = ? AND time_taken_seconds < ?))
                """, (test_id, subject_mode, score, score, time_taken_seconds))
                all_time_rank = c.fetchone()[0]

                c.execute("SELECT COUNT(*) FROM exam_submissions WHERE test_id = ? AND subject_mode = ?",
                          (test_id, subject_mode))
                all_time_total = c.fetchone()[0]
                all_time_percentile = round(((all_time_total - all_time_rank) / all_time_total) * 100, 2) if all_time_total > 0 else 100.0

                c.execute("""
                    SELECT student_id, student_name, target_college, session, score, percentage, time_taken_seconds, submitted_at
                    FROM exam_submissions
                    WHERE test_id = ? AND subject_mode = ? AND session = ?
                    ORDER BY score DESC, time_taken_seconds ASC
                    LIMIT 10
                """, (test_id, subject_mode, session))
                session_leaderboard = [dict(r) for r in c.fetchall()]

                c.execute("""
                    SELECT student_id, student_name, target_college, session, score, percentage, time_taken_seconds, submitted_at
                    FROM exam_submissions
                    WHERE test_id = ? AND subject_mode = ?
                    ORDER BY score DESC, time_taken_seconds ASC
                    LIMIT 10
                """, (test_id, subject_mode))
                all_time_leaderboard = [dict(r) for r in c.fetchall()]

        finally:
            conn.close()

        result = {
            "status": "success",
            "database": db_type,
            "student_id": student_id,
            "submission_code": submission_code,
            "exam_details": {
                "test_id": test_id,
                "test_code": test_code,
                "subject_mode": subject_mode,
                "score": score,
                "percentage": percentage,
                "time_taken_seconds": time_taken_seconds,
                "session": session
            },
            "rankings": {
                "session": session,
                "session_rank": session_rank,
                "session_total": session_total,
                "session_percentile": session_percentile,
                "all_time_rank": all_time_rank,
                "all_time_total": all_time_total,
                "all_time_percentile": all_time_percentile
            },
            "leaderboards": {
                "session": session_leaderboard,
                "all_time": all_time_leaderboard
            }
        }
        self.send_json_response(result)

    def handle_get_leaderboard(self, query):
        test_id = int(query.get('test_id', [1])[0])
        subject_mode = query.get('subject_mode', ['FullExam'])[0]
        session = query.get('session', ['all'])[0]

        conn, db_type = get_db_connection()
        try:
            if db_type == 'postgres':
                c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                if session == 'all':
                    c.execute("""
                        SELECT student_id, student_name, target_college, session, score, percentage, time_taken_seconds, submitted_at
                        FROM exam_submissions
                        WHERE test_id = %s AND subject_mode = %s
                        ORDER BY score DESC, time_taken_seconds ASC
                        LIMIT 20;
                    """, (test_id, subject_mode))
                else:
                    c.execute("""
                        SELECT student_id, student_name, target_college, session, score, percentage, time_taken_seconds, submitted_at
                        FROM exam_submissions
                        WHERE test_id = %s AND subject_mode = %s AND session = %s
                        ORDER BY score DESC, time_taken_seconds ASC
                        LIMIT 20;
                    """, (test_id, subject_mode, session))
                rows = [dict(r) for r in c.fetchall()]
            else:
                c = conn.cursor()
                if session == 'all':
                    c.execute("""
                        SELECT student_id, student_name, target_college, session, score, percentage, time_taken_seconds, submitted_at
                        FROM exam_submissions
                        WHERE test_id = ? AND subject_mode = ?
                        ORDER BY score DESC, time_taken_seconds ASC
                        LIMIT 20
                    """, (test_id, subject_mode))
                else:
                    c.execute("""
                        SELECT student_id, student_name, target_college, session, score, percentage, time_taken_seconds, submitted_at
                        FROM exam_submissions
                        WHERE test_id = ? AND subject_mode = ? AND session = ?
                        ORDER BY score DESC, time_taken_seconds ASC
                        LIMIT 20
                    """, (test_id, subject_mode, session))
                rows = [dict(r) for r in c.fetchall()]
        finally:
            conn.close()

        self.send_json_response({
            "test_id": test_id,
            "subject_mode": subject_mode,
            "session": session,
            "database": db_type,
            "leaderboard": rows
        })

    def handle_get_stats(self):
        conn, db_type = get_db_connection()
        try:
            if db_type == 'postgres':
                c = conn.cursor()
                c.execute("SELECT COUNT(*) FROM students;")
                s_count = c.fetchone()[0]
                c.execute("SELECT COUNT(*) FROM exam_submissions;")
                sub_count = c.fetchone()[0]
                c.execute("SELECT session, COUNT(*) FROM exam_submissions GROUP BY session ORDER BY session;")
                sess_rows = c.fetchall()
            else:
                c = conn.cursor()
                c.execute("SELECT count(*) FROM students")
                s_count = c.fetchone()[0]
                c.execute("SELECT count(*) FROM exam_submissions")
                sub_count = c.fetchone()[0]
                c.execute("SELECT session, count(*) FROM exam_submissions GROUP BY session")
                sess_rows = c.fetchall()
        finally:
            conn.close()

        self.send_json_response({
            "database": db_type,
            "total_students": s_count,
            "total_submissions": sub_count,
            "sessions": {s: cnt for s, cnt in sess_rows}
        })

    def handle_payment_status(self, query):
        student_id = query.get('student_id', [''])[0].strip()
        if not student_id:
            self.send_json_response({
                "student_id": "",
                "medical_enrolled": False,
                "versity_enrolled": False,
                "combo_enrolled": False,
                "enrollments": []
            })
            return

        conn, db_type = get_db_connection()
        try:
            if db_type == 'postgres':
                c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                c.execute("""
                    SELECT package_type, amount, sender_number, trx_id, status, enrolled_at
                    FROM student_enrollments
                    WHERE student_id = %s AND status = 'verified';
                """, (student_id,))
                rows = [dict(r) for r in c.fetchall()]
            else:
                c = conn.cursor()
                c.execute("""
                    SELECT package_type, amount, sender_number, trx_id, status, enrolled_at
                    FROM student_enrollments
                    WHERE student_id = ? AND status = 'verified';
                """, (student_id,))
                rows = [{
                    "package_type": r[0],
                    "amount": float(r[1]),
                    "sender_number": r[2],
                    "trx_id": r[3],
                    "status": r[4],
                    "enrolled_at": r[5]
                } for r in c.fetchall()]
        finally:
            conn.close()

        packages = [r['package_type'].lower() for r in rows]
        combo = 'combo' in packages
        med = combo or ('medical' in packages)
        var = combo or ('versity' in packages)

        self.send_json_response({
            "student_id": student_id,
            "medical_enrolled": med,
            "versity_enrolled": var,
            "combo_enrolled": combo,
            "enrollments": rows
        })

    def handle_sms_webhook(self, data):
        sender = data.get('sender') or data.get('from') or data.get('address') or 'bKash'
        raw_message = data.get('message') or data.get('text') or data.get('body') or data.get('msg') or ''
        
        parsed = parse_bkash_sms(raw_message)
        if not parsed:
            self.send_json_response({
                "status": "ignored",
                "message": "No valid bKash TrxID found in the SMS message.",
                "raw": raw_message
            }, status=200)
            return

        conn, db_type = get_db_connection()
        try:
            if db_type == 'postgres':
                c = conn.cursor()
                c.execute("""
                    INSERT INTO received_sms_logs (sender, raw_message, parsed_amount, parsed_sender, parsed_trx_id)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (parsed_trx_id) DO NOTHING;
                """, (sender, raw_message, parsed['amount'], parsed['sender'], parsed['trx_id']))
                conn.commit()

                # Auto-verify any pending enrollments waiting for this TrxID
                c.execute("""
                    UPDATE student_enrollments
                    SET status = 'verified'
                    WHERE trx_id = %s AND status = 'pending';
                """, (parsed['trx_id'],))
                conn.commit()
            else:
                c = conn.cursor()
                c.execute("""
                    INSERT OR IGNORE INTO received_sms_logs (sender, raw_message, parsed_amount, parsed_sender, parsed_trx_id)
                    VALUES (?, ?, ?, ?, ?);
                """, (sender, raw_message, parsed['amount'], parsed['sender'], parsed['trx_id']))
                conn.commit()

                c.execute("""
                    UPDATE student_enrollments
                    SET status = 'verified'
                    WHERE trx_id = ? AND status = 'pending';
                """, (parsed['trx_id'],))
                conn.commit()
        finally:
            conn.close()

        self.send_json_response({
            "status": "success",
            "message": "bKash SMS logged and indexed successfully.",
            "parsed": parsed
        })

    def handle_verify_trx(self, data):
        student_id = data.get('student_id', '').strip()
        student_name = data.get('student_name', 'পরীক্ষার্থী').strip() or 'পরীক্ষার্থী'
        package = data.get('package', 'medical').strip().lower()
        sender_number = data.get('sender_number', '').strip()
        trx_id = data.get('trx_id', '').strip().upper()

        if not student_id:
            student_id = f"STU-{uuid.uuid4().hex[:8].upper()}"

        if not trx_id or len(trx_id) < 6:
            self.send_json_response({
                "success": False,
                "message": "অনুগ্রহ করে একটি সঠিক ও পূর্ণাঙ্গ TrxID লিখুন (কমপক্ষে ৬-১২ অক্ষর)।"
            }, status=400)
            return

        # Price rules
        price_map = {
            'medical': 499.0,
            'versity': 499.0,
            'combo': 799.0
        }
        required_price = price_map.get(package, 499.0)

        conn, db_type = get_db_connection()
        try:
            if db_type == 'postgres':
                c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

                # 1. Check if student is already enrolled in this package
                c.execute("""
                    SELECT package_type FROM student_enrollments
                    WHERE student_id = %s AND (package_type = %s OR package_type = 'combo') AND status = 'verified';
                """, (student_id, package))
                already = c.fetchone()
                if already:
                    self.send_json_response({
                        "success": True,
                        "already_enrolled": True,
                        "package": already['package_type'],
                        "message": "আপনি ইতিমধ্যে এই প্যাকেজে সফলভাবে এনরোল্ড আছেন!"
                    })
                    return

                # 2. Check if this TrxID has already been claimed by another student
                c.execute("SELECT student_id, student_name FROM student_enrollments WHERE trx_id = %s AND status = 'verified';", (trx_id,))
                claimed_other = c.fetchone()
                if claimed_other and claimed_other['student_id'] != student_id:
                    self.send_json_response({
                        "success": False,
                        "message": "এই TrxID ইতিপূর্বে অন্য একজন শিক্ষার্থীর একাউন্টে ব্যবহার করা হয়েছে। প্রতিটি পেমেন্টের জন্য ইউনিক TrxID প্রয়োজন।"
                    }, status=400)
                    return

                # 3. Check received SMS logs if available
                c.execute("SELECT * FROM received_sms_logs WHERE parsed_trx_id = %s;", (trx_id,))
                sms_log = c.fetchone()
                if sms_log:
                    if sms_log['is_claimed'] and sms_log['claimed_by_student_id'] and sms_log['claimed_by_student_id'] != student_id:
                        self.send_json_response({
                            "success": False,
                            "message": "এই TrxID-এর পেমেন্ট ইতিপূর্বে অন্য একাউন্টে ক্লেইম করা হয়েছে।"
                        }, status=400)
                        return
                    if sms_log['parsed_amount'] is not None and float(sms_log['parsed_amount']) < required_price:
                        self.send_json_response({
                            "success": False,
                            "message": f"পেমেন্ট ফি অপর্যাপ্ত! এই প্যাকেজের জন্য ৳{int(required_price)} প্রয়োজন, কিন্তু TrxID-তে পাওয়া গেছে ৳{float(sms_log['parsed_amount'])}।"
                        }, status=400)
                        return

                    # Mark claimed in SMS logs
                    c.execute("""
                        UPDATE received_sms_logs
                        SET is_claimed = TRUE, claimed_by_student_id = %s
                        WHERE parsed_trx_id = %s;
                    """, (student_id, trx_id))

                # 4. Insert or update student enrollment
                c.execute("""
                    INSERT INTO student_enrollments (student_id, student_name, package_type, amount, sender_number, trx_id, status)
                    VALUES (%s, %s, %s, %s, %s, %s, 'verified')
                    ON CONFLICT (trx_id) DO UPDATE SET
                        status = 'verified',
                        package_type = EXCLUDED.package_type,
                        amount = EXCLUDED.amount;
                """, (student_id, student_name, package, required_price, sender_number, trx_id))
                conn.commit()

            else:
                # SQLite fallback
                c = conn.cursor()
                c.execute("""
                    SELECT package_type FROM student_enrollments
                    WHERE student_id = ? AND (package_type = ? OR package_type = 'combo') AND status = 'verified';
                """, (student_id, package))
                already = c.fetchone()
                if already:
                    self.send_json_response({
                        "success": True,
                        "already_enrolled": True,
                        "package": already[0],
                        "message": "আপনি ইতিমধ্যে এই প্যাকেজে সফলভাবে এনরোল্ড আছেন!"
                    })
                    return

                c.execute("SELECT student_id FROM student_enrollments WHERE trx_id = ? AND status = 'verified';", (trx_id,))
                claimed_other = c.fetchone()
                if claimed_other and claimed_other[0] != student_id:
                    self.send_json_response({
                        "success": False,
                        "message": "এই TrxID ইতিপূর্বে অন্য একজন শিক্ষার্থীর একাউন্টে ব্যবহার করা হয়েছে।"
                    }, status=400)
                    return

                c.execute("SELECT is_claimed, claimed_by_student_id, parsed_amount FROM received_sms_logs WHERE parsed_trx_id = ?;", (trx_id,))
                sms_log = c.fetchone()
                if sms_log:
                    if sms_log[0] and sms_log[1] and sms_log[1] != student_id:
                        self.send_json_response({
                            "success": False,
                            "message": "এই TrxID-এর পেমেন্ট ইতিমধ্যে ক্লেইম করা হয়েছে।"
                        }, status=400)
                        return
                    if sms_log[2] is not None and float(sms_log[2]) < required_price:
                        self.send_json_response({
                            "success": False,
                            "message": f"পেমেন্ট ফি অপর্যাপ্ত! প্রয়োজন ৳{int(required_price)}, কিন্তু পাওয়া গেছে ৳{float(sms_log[2])}।"
                        }, status=400)
                        return
                    c.execute("""
                        UPDATE received_sms_logs
                        SET is_claimed = 1, claimed_by_student_id = ?
                        WHERE parsed_trx_id = ?;
                    """, (student_id, trx_id))

                c.execute("""
                    INSERT OR REPLACE INTO student_enrollments (student_id, student_name, package_type, amount, sender_number, trx_id, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'verified');
                """, (student_id, student_name, package, required_price, sender_number, trx_id))
                conn.commit()

        finally:
            conn.close()

        pkg_title = "মেডিকেল ১০০ মডেল টেস্ট" if package == 'medical' else ("ভার্সিটি ও সমন্বিত গুচ্ছ ১০০ মডেল টেস্ট" if package == 'versity' else "মেডিকেল + ভার্সিটি মেগা কম্বো প্যাক")
        self.send_json_response({
            "success": True,
            "package": package,
            "message": f"🎉 অভিনন্দন! আপনার bKash পেমেন্ট সফলভাবে ভেরিফাই হয়েছে। '{pkg_title}'-এর ৯৫টি প্রিমিয়াম টেস্ট সফলভাবে আনলক করা হয়েছে।"
        })

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

if __name__ == '__main__':
    print(f"Connecting to Neon PostgreSQL: {NEON_URL.split('@')[1].split('/')[0]}...")
    test_conn, test_db = get_db_connection()
    print(f"Primary ranking database: {test_db.upper()}")
    ensure_database_schema(test_conn, test_db)
    test_conn.close()

    with ThreadedTCPServer(("127.0.0.1", PORT), AdmissionApiHandler) as httpd:
        print(f"Admission Test BD Server & API running at http://127.0.0.1:{PORT}")
        httpd.serve_forever()
