import http.server
import json
import os
import sys
import re
import uuid
import decimal
import urllib.parse
from datetime import datetime, date

# Neon PostgreSQL connection URL
NEON_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_YIR9cGa5MqOP@ep-spring-lake-b45687pc-pooler.c-6.us-east-2.aws.neon.tech/neondb?sslmode=require"
)

# Root directory of the repository
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Lazy schema check
_SCHEMA_ENSURED = False

def get_db_connection():
    """Connects to Neon PostgreSQL pooler."""
    import psycopg2
    conn = psycopg2.connect(NEON_URL, connect_timeout=10)
    return conn

def ensure_database_schema(conn):
    """Ensures that all needed tables and indexes exist on the database."""
    global _SCHEMA_ENSURED
    if _SCHEMA_ENSURED:
        return
    try:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id VARCHAR(64) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                roll_number VARCHAR(64),
                target_college VARCHAR(255),
                session VARCHAR(32),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS exam_submissions (
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
            CREATE INDEX IF NOT EXISTS idx_submissions_rank ON exam_submissions (test_id, subject_mode, session, score DESC, time_taken_seconds ASC);
            CREATE INDEX IF NOT EXISTS idx_submissions_alltime ON exam_submissions (test_id, subject_mode, score DESC, time_taken_seconds ASC);
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
        conn.commit()
        _SCHEMA_ENSURED = True
    except Exception as e:
        print(f"[WARN] Failed to ensure schema: {e}")

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


class handler(http.server.BaseHTTPRequestHandler):
    """Vercel Serverless Function & Full-Stack Handler."""

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, HEAD')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_HEAD(self):
        self.do_GET()

    def get_route_path(self):
        """Extracts the actual route path from incoming request URL, supporting Vercel __route rewrite parameter."""
        parsed = urllib.parse.urlparse(self.path or '/')
        query = urllib.parse.parse_qs(parsed.query)

        if '__route' in query:
            route = query['__route'][0]
            clean_route = urllib.parse.urlparse(route).path.rstrip('/') or '/'
            clean_query = {k: v for k, v in query.items() if k != '__route'}
            return clean_route, clean_query

        raw_path = self.headers.get('x-forwarded-uri') or parsed.path or '/'
        path = urllib.parse.urlparse(raw_path).path.rstrip('/') or '/'
        return path, query

    def serve_static_file(self, file_path, content_type):
        """Streams a static file (HTML, JSON, Images) with correct caching and headers."""
        try:
            if not os.path.isfile(file_path):
                self.send_json_response({"status": "error", "message": f"File not found: {file_path}"}, status=404)
                return
            with open(file_path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            if content_type.startswith('text/html'):
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Expires', '0')
            else:
                self.send_header('Cache-Control', 'public, max-age=86400')
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status=500)

    def do_GET(self):
        path, query = self.get_route_path()

        # 1. Root & HTML Page
        if path in ('', '/', '/index', '/index.html'):
            html_path = os.path.join(BASE_DIR, 'index.html')
            self.serve_static_file(html_path, 'text/html; charset=utf-8')
            return

        # 2. Static Assets & Images (Support both /web/assets/ and /assets/)
        if path.startswith('/web/assets/') or path.startswith('/assets/'):
            clean_rel = path.lstrip('/')
            file_path = os.path.join(BASE_DIR, clean_rel)
            if not os.path.isfile(file_path):
                if path.startswith('/assets/'):
                    file_path = os.path.join(BASE_DIR, 'web', clean_rel)
                elif path.startswith('/web/assets/'):
                    file_path = os.path.join(BASE_DIR, clean_rel.replace('web/', ''))
            if os.path.isfile(file_path):
                ctype = 'image/jpeg' if file_path.lower().endswith(('.jpg', '.jpeg')) else ('image/png' if file_path.lower().endswith('.png') else 'application/octet-stream')
                self.serve_static_file(file_path, ctype)
                return
            else:
                self.send_json_response({"status": "error", "message": f"Asset not found: {file_path}"}, status=404)
                return

        # 3. Data Stores (JSON test banks)
        if path.startswith('/data/'):
            clean_rel = path.lstrip('/')
            file_path = os.path.join(BASE_DIR, clean_rel)
            self.serve_static_file(file_path, 'application/json; charset=utf-8')
            return

        # 4. API Endpoints
        if path in ('/api', '/api/health', '/api/index'):
            self.send_json_response({
                "status": "healthy",
                "service": "Admission Test BD Cloud API",
                "database": "Neon PostgreSQL",
                "timestamp": datetime.now().isoformat()
            })
            return

        if path == '/api/payment/sms-webhook':
            self.send_json_response({
                "status": "active",
                "message": "bKash SMS Webhook endpoint is active and listening for POST requests.",
                "webhook_target": "/api/payment/sms-webhook"
            })
            return

        if path == '/api/payment/status':
            self.handle_payment_status(query)
            return

        if path == '/api/leaderboard':
            self.handle_get_leaderboard(query)
            return

        if path == '/api/stats':
            self.handle_get_stats()
            return

        # Fallback for unknown web routes to index.html (SPA routing)
        if not path.startswith('/api/'):
            html_path = os.path.join(BASE_DIR, 'index.html')
            if os.path.exists(html_path):
                self.serve_static_file(html_path, 'text/html; charset=utf-8')
                return

        self.send_json_response({"status": "error", "message": f"Endpoint not found: {path}"}, status=404)

    def do_POST(self):
        path, _ = self.get_route_path()

        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ""

        try:
            try:
                data = json.loads(post_body) if post_body else {}
            except Exception:
                parsed_form = urllib.parse.parse_qs(post_body)
                data = {k: v[0] for k, v in parsed_form.items()}
        except Exception as e:
            self.send_json_response({"status": "error", "message": f"Invalid request body: {str(e)}"}, status=400)
            return

        if path == '/api/payment/sms-webhook':
            self.handle_sms_webhook(data)
            return

        if path == '/api/payment/verify-trx':
            self.handle_verify_trx(data)
            return

        if path == '/api/submit-exam':
            self.handle_submit_exam(data)
            return

        self.send_json_response({"status": "error", "message": f"POST endpoint not found: {path}"}, status=404)

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
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.end_headers()
        self.wfile.write(response_bytes)

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

        import psycopg2.extras
        conn = get_db_connection()
        try:
            ensure_database_schema(conn)
            c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            c.execute("""
                SELECT package_type, amount, sender_number, trx_id, status, enrolled_at
                FROM student_enrollments
                WHERE student_id = %s AND status = 'verified';
            """, (student_id,))
            rows = [dict(r) for r in c.fetchall()]
        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status=500)
            return
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
        sender = data.get('sender') or data.get('from') or data.get('address') or data.get('phone') or 'bKash'
        raw_message = (
            data.get('message') or 
            data.get('text') or 
            data.get('body') or 
            data.get('msg') or 
            data.get('content') or 
            data.get('sms') or ''
        )

        parsed = parse_bkash_sms(raw_message)
        if not parsed:
            self.send_json_response({
                "status": "ignored",
                "message": "No valid bKash TrxID found in the SMS message.",
                "raw": raw_message
            }, status=200)
            return

        conn = get_db_connection()
        try:
            ensure_database_schema(conn)
            c = conn.cursor()
            c.execute("""
                INSERT INTO received_sms_logs (sender, raw_message, parsed_amount, parsed_sender, parsed_trx_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (parsed_trx_id) DO UPDATE SET
                    parsed_amount = EXCLUDED.parsed_amount,
                    parsed_sender = EXCLUDED.parsed_sender;
            """, (sender, raw_message, parsed['amount'], parsed['sender'], parsed['trx_id']))
            conn.commit()
        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status=500)
            return
        finally:
            conn.close()

        self.send_json_response({
            "status": "success",
            "message": "bKash SMS successfully recorded and logged.",
            "parsed": parsed
        })

    def handle_verify_trx(self, data):
        student_id = data.get('student_id', '').strip()
        student_name = data.get('student_name', 'শিক্ষার্থী').strip() or 'শিক্ষার্থী'
        package = (data.get('package') or data.get('package_type') or 'medical').strip().lower()
        sender_number = data.get('sender_number', '').strip()
        trx_id = data.get('trx_id', '').strip().upper()

        if not student_id or not sender_number or not trx_id:
            self.send_json_response({
                "success": False,
                "message": "অনুগ্রহ করে আপনার bKash নাম্বার এবং TrxID সঠিকভাবে প্রদান করুন।"
            }, status=400)
            return

        clean_num = re.sub(r'[\s\-+]', '', sender_number)
        if clean_num.startswith('880'):
            clean_num = clean_num[2:]
        if not re.match(r'^01[3-9]\d{8}$', clean_num):
            self.send_json_response({
                "success": False,
                "message": "সঠিক ১১ ডিজিটের bKash মোবাইল নাম্বার দিন (যেমন: 017xxxxxxxx)।"
            }, status=400)
            return
        sender_number = clean_num

        if len(trx_id) < 6:
            self.send_json_response({
                "success": False,
                "message": "সঠিক Transaction ID (TrxID) প্রদান করুন।"
            }, status=400)
            return

        pricing = {
            'medical': 499.0,
            'versity': 499.0,
            'combo': 799.0
        }
        required_price = pricing.get(package, 499.0)

        import psycopg2.extras
        conn = get_db_connection()
        try:
            ensure_database_schema(conn)
            c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

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

            c.execute("SELECT student_id FROM student_enrollments WHERE trx_id = %s AND status = 'verified';", (trx_id,))
            claimed_other = c.fetchone()
            if claimed_other and claimed_other['student_id'] != student_id:
                self.send_json_response({
                    "success": False,
                    "message": "এই TrxID ইতিপূর্বে অন্য একজন শিক্ষার্থীর একাউন্টে ব্যবহার করা হয়েছে।"
                }, status=400)
                return

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

                c.execute("""
                    UPDATE received_sms_logs
                    SET is_claimed = TRUE, claimed_by_student_id = %s
                    WHERE parsed_trx_id = %s;
                """, (student_id, trx_id))

            c.execute("""
                INSERT INTO student_enrollments (student_id, student_name, package_type, amount, sender_number, trx_id, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'verified')
                ON CONFLICT (trx_id) DO UPDATE SET
                    status = 'verified',
                    package_type = EXCLUDED.package_type,
                    amount = EXCLUDED.amount;
            """, (student_id, student_name, package, required_price, sender_number, trx_id))
            conn.commit()

        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status=500)
            return
        finally:
            conn.close()

        pkg_title = "মেডিকেল ১০০ মডেল টেস্ট" if package == 'medical' else ("ভার্সিটি ও সমন্বিত গুচ্ছ ১০০ মডেল টেস্ট" if package == 'versity' else "মেডিকেল + ভার্সিটি মেগা কম্বো প্যাক")
        self.send_json_response({
            "success": True,
            "package": package,
            "message": f"🎉 অভিনন্দন! আপনার bKash পেমেন্ট সফলভাবে ভেরিফাই হয়েছে। '{pkg_title}'-এর ৯৫টি প্রিমিয়াম টেস্ট সফলভাবে আনলক করা হয়েছে।"
        })

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

        import psycopg2.extras
        conn = get_db_connection()
        try:
            ensure_database_schema(conn)
            c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            c.execute("""
                INSERT INTO students (student_id, name, roll_number, target_college, session)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT(student_id) DO UPDATE SET
                    name=EXCLUDED.name,
                    roll_number=EXCLUDED.roll_number,
                    target_college=EXCLUDED.target_college,
                    session=EXCLUDED.session;
            """, (student_id, student_name, roll, target, session))

            c.execute("""
                INSERT INTO exam_submissions
                (submission_code, student_id, student_name, target_college, session, test_id, test_code, subject_mode,
                 total_questions, correct_count, wrong_count, unanswered_count, score, percentage, time_taken_seconds)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (submission_code, student_id, student_name, target, session, test_id, test_code, subject_mode,
                  total_questions, correct_count, wrong_count, unanswered_count, score, percentage, time_taken_seconds))
            conn.commit()

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

        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status=500)
            return
        finally:
            conn.close()

        result = {
            "status": "success",
            "database": "postgres",
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

        import psycopg2.extras
        conn = get_db_connection()
        try:
            ensure_database_schema(conn)
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
        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status=500)
            return
        finally:
            conn.close()

        self.send_json_response({
            "test_id": test_id,
            "subject_mode": subject_mode,
            "session": session,
            "database": "postgres",
            "leaderboard": rows
        })

    def handle_get_stats(self):
        conn = get_db_connection()
        try:
            ensure_database_schema(conn)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM students;")
            s_count = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM exam_submissions;")
            sub_count = c.fetchone()[0]
            c.execute("SELECT session, COUNT(*) FROM exam_submissions GROUP BY session ORDER BY session;")
            sess_rows = c.fetchall()
        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status=500)
            return
        finally:
            conn.close()

        self.send_json_response({
            "database": "postgres",
            "total_students": s_count,
            "total_submissions": sub_count,
            "sessions": {s: cnt for s, cnt in sess_rows}
        })


if __name__ == '__main__':
    import socketserver
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 8089), handler)
    print("Test Vercel API Handler running at http://127.0.0.1:8089")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
