import sys
import json
from db_manager import MedicalDBManager
from llm_textbook_rag import TextbookKnowledgeBase

def print_help():
    print("""
Bangladesh Medical Admission Test (MAT) Intelligence System CLI
==============================================================
Commands for Past 15-Year Questions:
  stats                       Show database summary and 15-year analytics
  sessions                    List all 15 exam sessions
  view <session>              View all questions from a specific session (e.g. 2023-2024)
  search <query>              Search past questions instantly via FTS5
  export [json|csv]           Export all 15 years questions to JSON or CSV

Commands for Textbook Knowledge Base & LLM Engine:
  books                       List all authoritative NCTB medical textbooks
  ask <query>                 Query the Textbook Knowledge Base with LLM ground-truth
  prompt <query>              Generate the complete LLM RAG prompt with textbook citations
""")

def main():
    db = MedicalDBManager()
    kb = TextbookKnowledgeBase()
    
    if len(sys.argv) < 2:
        print_help()
        return

    cmd = sys.argv[1].lower()

    if cmd == 'stats':
        analytics = db.get_analytics()
        print("="*60)
        print("  15-YEAR MEDICAL ADMISSION DATABASE SUMMARY")
        print("="*60)
        print(f"Total Questions Indexed : {analytics['total_questions']}")
        print(f"Total Exam Sessions     : {analytics['sessions_count']}")
        print(f"Repeated Questions      : {analytics['repeat_questions']} ({analytics['repeat_percentage']}%)")
        print("\n--- Subject Distribution ---")
        for subj, count in analytics['by_subject'].items():
            print(f"  {subj:<20}: {count:>4} MCQs")
        print("\n--- Top High-Yield Chapters ---")
        for item in analytics['top_chapters']:
            print(f"  [{item['subject']}] {item['chapter']:<35}: {item['cnt']} questions")
        print("="*60)

    elif cmd == 'sessions':
        sessions = db.get_all_sessions()
        print("Indexed Exam Sessions:")
        for s in sessions:
            print(f" - {s}")

    elif cmd == 'view':
        if len(sys.argv) < 3:
            print("Please specify a session, e.g. python3 cli.py view 2023-2024")
            return
        sess = sys.argv[2]
        questions = db.get_questions_by_session(sess)
        print(f"\n--- Questions for Session {sess} (Total {len(questions)}) ---")
        for q in questions[:10]:
            print(f"\nQ{q['question_num']}. [{q['subject']} - {q['chapter']}]")
            print(f"    {q['question_bn']}")
            print(f"    (ক) {q['option_a']}  (খ) {q['option_b']}  (গ) {q['option_c']}  (ঘ) {q['option_d']}")
            print(f"    সঠিক উত্তর: {q['correct_option']} | রেফারেন্স: {q['book_reference']}")

    elif cmd == 'search':
        if len(sys.argv) < 3:
            print("Please provide a search term, e.g. python3 cli.py search রক্ত")
            return
        query = " ".join(sys.argv[2:])
        results = db.search_fts(query)
        print(f"\nFound {len(results)} matches for '{query}':")
        for q in results[:5]:
            print(f"\n[{q['session']} - Q{q['question_num']}] [{q['subject']}]")
            print(f"  {q['question_bn']}")
            print(f"  Ans: {q['correct_option']} - {q['explanation']}")

    elif cmd == 'export':
        fmt = sys.argv[2] if len(sys.argv) > 2 else 'json'
        if fmt == 'json':
            out = '/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/medical_15years_export.json'
            db.export_to_json(out)
        elif fmt == 'csv':
            out = '/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/medical_15years_export.csv'
            db.export_to_csv(out)

    elif cmd == 'books':
        with kb.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title_bn, author, subject, total_chapters, importance_note FROM books")
            print("="*65)
            print("  AUTHORITATIVE NCTB MEDICAL ADMISSION TEXTBOOKS (GROUND TRUTH)")
            print("="*65)
            for r in cursor.fetchall():
                print(f"\n📖 {r['title_bn']}")
                print(f"   লেখক: {r['author']} | বিষয়: {r['subject']} ({r['total_chapters']} অধ্যায়)")
                print(f"   গুরুত্ব: {r['importance_note']}")
            print("="*65)

    elif cmd == 'ask':
        if len(sys.argv) < 3:
            print("Please provide a question, e.g. python3 cli.py ask 'লুকাস বিকারক'")
            return
        q = " ".join(sys.argv[2:])
        print(kb.answer_query(q))

    elif cmd == 'prompt':
        if len(sys.argv) < 3:
            print("Please provide a question, e.g. python3 cli.py prompt 'C4 উদ্ভিদ'")
            return
        q = " ".join(sys.argv[2:])
        res = kb.format_llm_rag_prompt(q)
        print("="*60)
        print("  GENERATED LLM RAG PROMPT WITH EXACT TEXTBOOK CITATION")
        print("="*60)
        print(res['prompt'])
    else:
        print_help()

if __name__ == '__main__':
    main()
