import sqlite3
import json
import os
from typing import List, Dict, Any, Optional

TEXTBOOK_DB_PATH = '/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/medical_textbooks_kb.db'

SYSTEM_INSTRUCTION = """
You are the Official Medical Admission AI Evaluator for the Bangladesh MBBS Central Admission Test (DGME).
You must answer questions strictly based on the standard Higher Secondary NCTB textbooks:
1. Botany: Dr. Mohammad Abul Hasan (ড. মোহাম্মদ আবুল হাসান)
2. Zoology: Gazi Azmal & Gazi Asmat (গাজী আজমল ও গাজী আসমত)
3. Chemistry 1st & 2nd Paper: Prof. Mahbub Hasan Hazari & Swapan Kumar Nag (প্রফেসর মহব্বত হাসান হাজারী ও স্বপন কুমার নাগ)
4. Physics 1st & 2nd Paper: Prof. Md. Ishaq & Dr. Amir Hossain Khan (ড. আমির হোসেন খান ও প্রফেসর মোহাম্মদ ইসহাক)
5. English & General Knowledge: Medical Admission Standard Syllabus

RULES:
1. Do not use external American/Indian conventions if they conflict with NCTB textbook lines.
2. Provide the direct textbook fact, followed by the exact book citation (Author, Chapter, Topic).
3. Highlight any common MCQ traps or deceptive distractors that DGME examiners frequently test.
"""

class TextbookKnowledgeBase:
    def __init__(self, db_path: str = TEXTBOOK_DB_PATH):
        self.db_path = db_path

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def search_facts(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves top factual knowledge units using SQLite FTS5 search across Bengali and English terms.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT k.*, b.title_bn as book_title, b.author as book_author, c.chapter_name_bn
                FROM knowledge_units_fts f
                JOIN knowledge_units k ON f.id = k.id
                JOIN books b ON k.book_id = b.id
                JOIN book_chapters c ON k.chapter_id = c.id
                WHERE knowledge_units_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, limit))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_chapter_facts(self, chapter_id: str) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT k.*, b.title_bn as book_title, b.author as book_author
                FROM knowledge_units k
                JOIN books b ON k.book_id = b.id
                WHERE k.chapter_id = ?
                ORDER BY k.high_yield_priority DESC
            """, (chapter_id,))
            return [dict(r) for r in cursor.fetchall()]

    def format_llm_rag_prompt(self, user_question: str) -> Dict[str, Any]:
        """
        Constructs an optimized RAG context payload for any LLM (Gemini, Claude, GPT).
        """
        # Clean query terms for FTS
        search_terms = user_question.replace('?', '').replace('!', '').strip()
        facts = self.search_facts(search_terms, limit=4)
        
        # Fallback if no direct match: search key tokens
        if not facts:
            tokens = [t for t in search_terms.split() if len(t) > 2]
            if tokens:
                facts = self.search_facts(" OR ".join(tokens[:3]), limit=3)

        context_blocks = []
        citations = []
        for f in facts:
            block = f"""
---
[পাঠ্যবই রেফারেন্স]: {f['citation']}
[লেখক ও বই]: {f['book_author']} ({f['book_title']})
[মূল তথ্য/লাইন]: {f['exact_text_bn']}
[মেডিকেল ফাঁদ/সতর্কতা]: {f.get('common_mcq_trap', 'N/A')}
"""
            context_blocks.append(block)
            citations.append(f"{f['book_author']} - {f['topic']}")

        context_text = "\n".join(context_blocks) if context_blocks else "কোনো সরাসরি পাঠ্যবই লাইন মেলেনি। সাধারণ এনসিটিবি পাঠ্যক্রম অনুযায়ী উত্তর দিন।"

        prompt = f"""
{SYSTEM_INSTRUCTION}

=== এনসিটিবি অনুমোদিত মূল বইয়ের প্রমাণ্য তথ্য (GROUND TRUTH TEXTBOOK CONTEXT) ===
{context_text}
================================================================================

[শিক্ষার্থীর প্রশ্ন]:
{user_question}

দয়া করে পাঠ্যবইয়ের উপরিউক্ত প্রামাণ্য তথ্যের ভিত্তিতে সংক্ষিপ্ত, নির্ভুল এবং সরাসরি মেডিকেল ভর্তি পরীক্ষার মানসম্মত উত্তর প্রদান করুন।
"""
        return {
            "system_instruction": SYSTEM_INSTRUCTION,
            "ground_truth_context": context_text,
            "prompt": prompt,
            "citations": citations,
            "retrieved_facts_count": len(facts)
        }

    def answer_query(self, user_question: str) -> str:
        """
        Local inference / demonstration answering engine powered by grounded textbook units.
        """
        rag_payload = self.format_llm_rag_prompt(user_question)
        facts = self.search_facts(user_question, limit=2)

        if facts:
            f = facts[0]
            output = f"""
📌 **সরাসরি মূল পাঠ্যবই থেকে উত্তর:**
{f['exact_text_bn']}

📖 **রেফারেন্স:** {f['citation']} ({f['book_author']})
⚠️ **মেডিকেল পরীক্ষার ট্র্যাপ (MCQ Warning):** {f.get('common_mcq_trap', '')}
"""
        else:
            output = f"এই প্রশ্নটির জন্য সরাসরি পাঠ্যবই রেফারেন্সের সন্ধান পাওয়া যায়নি।\nপ্রশ্ন: {user_question}"
        return output

if __name__ == '__main__':
    kb = TextbookKnowledgeBase()
    
    print("--- Test 1: Query on Mitochondria ---")
    print(kb.answer_query("মাইটোকন্ড্রিয়া"))

    print("\n--- Test 2: Query on Blood Clotting Factor (ক্রিসমাস ফ্যাক্টর) ---")
    print(kb.answer_query("ক্রিসমাস ফ্যাক্টর"))

    print("\n--- Test 3: Query on Lucas Reagent ---")
    print(kb.answer_query("লুকাস বিকারক"))

    print("\n--- Test 4: Query on Flame Test (শিখা পরীক্ষা) ---")
    print(kb.answer_query("বেরিয়াম"))
