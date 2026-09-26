import sqlite3
import json
from db_manager import MedicalDBManager

EXAM_SESSIONS = [
    {"session": "2024-2025", "exam_name": "MBBS Admission Test 2024-2025", "exam_date": "2025-01-17", "notes": "Short + Full syllabus mix, high emphasis on Biology"},
    {"session": "2023-2024", "exam_name": "MBBS Admission Test 2023-2024", "exam_date": "2024-02-09", "notes": "DGME standard format, 100 MCQs"},
    {"session": "2022-2023", "exam_name": "MBBS Admission Test 2022-2023", "exam_date": "2023-03-10", "notes": "Post-pandemic full/short alignment"},
    {"session": "2021-2022", "exam_name": "MBBS Admission Test 2021-2022", "exam_date": "2022-04-01", "notes": "HSC revised curriculum cohort"},
    {"session": "2020-2021", "exam_name": "MBBS Admission Test 2020-2021", "exam_date": "2021-04-02", "notes": "COVID-19 rescheduled session"},
    {"session": "2019-2020", "exam_name": "MBBS Admission Test 2019-2020", "exam_date": "2019-10-11", "notes": "Standard NCTB curriculum"},
    {"session": "2018-2019", "exam_name": "MBBS Admission Test 2018-2019", "exam_date": "2018-10-05", "notes": "High GK and English weightage"},
    {"session": "2017-2018", "exam_name": "MBBS Admission Test 2017-2018", "exam_date": "2017-10-06", "notes": "Increased negative marking scrutiny"},
    {"session": "2016-2017", "exam_name": "MBBS Admission Test 2016-2017", "exam_date": "2016-10-07", "notes": "Direct textbook lines from Hazari-Nag and Azmal"},
    {"session": "2015-2016", "exam_name": "MBBS Admission Test 2015-2016", "exam_date": "2015-09-18", "notes": "Strict nationwide central exam"},
    {"session": "2014-2015", "exam_name": "MBBS Admission Test 2014-2015", "exam_date": "2014-10-24", "notes": "Biology conceptual emphasis"},
    {"session": "2013-2014", "exam_name": "MBBS Admission Test 2013-2014", "exam_date": "2013-11-08", "notes": "NCTB syllabus revision milestone"},
    {"session": "2012-2013", "exam_name": "MBBS Admission Test 2012-2013", "exam_date": "2012-10-05", "notes": "National entrance testing"},
    {"session": "2011-2012", "exam_name": "MBBS Admission Test 2011-2012", "exam_date": "2011-09-23", "notes": "Classic question distribution"},
    {"session": "2010-2011", "exam_name": "MBBS Admission Test 2010-2011", "exam_date": "2010-10-15", "notes": "Benchmark year for past 15-year tracking"}
]

def seed_exams_and_questions():
    db = MedicalDBManager()
    
    # 1. Insert Exam Sessions
    for s in EXAM_SESSIONS:
        s.setdefault("total_marks", 100)
        s.setdefault("total_questions", 100)
        s.setdefault("biology_marks", 30)
        s.setdefault("chemistry_marks", 25)
        s.setdefault("physics_marks", 20)
        s.setdefault("english_marks", 15)
        s.setdefault("gk_marks", 10)
        db.insert_exam(s)
    print(f"Seeded {len(EXAM_SESSIONS)} exam sessions.")

if __name__ == '__main__':
    seed_exams_and_questions()
