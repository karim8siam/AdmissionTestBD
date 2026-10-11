"""Build chapter practice from tagged banks and explicit original practice material.

Retain existing questions and fill deficits with separately attributed original items.
Run from the repository root: python build_chapter_practice.py
"""
import ast
import collections
import copy
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = [
    "biology_100_tests.json", "chemistry_100_tests.json", "physics_100_tests.json",
    "math_100_tests.json", "english_100_tests.json", "gk_100_tests.json",
    "medical_100_tests.json", "versity_100_tests.json", "past_15years_tests.json",
]

def norm(text):
    text = unicodedata.normalize("NFKC", str(text)).replace("\u200b", "").replace("\u200c", "")
    return re.sub(r"\s+", " ", text).strip().casefold()

def chapter_name(text):
    return norm(re.sub(r"\s*\([^)]*\)", "", str(text)))

def walk(value):
    if isinstance(value, dict):
        if "question_bn" in value:
            yield value
        else:
            for child in value.values():
                yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)

def catalog():
    # Read only the literal catalogue, without importing database seed code.
    tree = ast.parse((ROOT / "taxonomy.py").read_text())
    rows = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "TOPICS_DATA" for t in n.targets))
    books = []
    for subject, paper, book_id, title in [
        ("Biology", "Botany", "biology-1", "জীববিজ্ঞান ১ম পত্র · উদ্ভিদবিজ্ঞান"),
        ("Biology", "Zoology", "biology-2", "জীববিজ্ঞান ২য় পত্র · প্রাণিবিজ্ঞান"),
        ("Chemistry", "1st Paper", "chemistry-1", "রসায়ন ১ম পত্র"),
        ("Chemistry", "2nd Paper", "chemistry-2", "রসায়ন ২য় পত্র"),
        ("Physics", "1st Paper", "physics-1", "পদার্থবিজ্ঞান ১ম পত্র"),
        ("Physics", "2nd Paper", "physics-2", "পদার্থবিজ্ঞান ২য় পত্র"),
    ]:
        chapters = [{"id": f"{book_id}-{r[2]:02}", "number": r[2],
                     "title": re.sub(r"\s*\([^)]*\)", "", r[3]).strip()}
                    for r in rows if r[0] == subject and r[1] == paper]
        if book_id == "physics-2":
            chapters.append({"id": "physics-2-11", "number": 11, "title": "জ্যোতির্বিজ্ঞান"})
        books.append({"id": book_id, "subject": subject, "paper": paper, "title": title,
                      "kind": "textbook", "tracks": ["medical", "versity"], "chapters": chapters})
    for book_id, title, chapters in [
        ("math-1", "উচ্চতর গণিত ১ম পত্র", ["ম্যাট্রিক্স ও নির্ণায়ক", "ভেক্টর", "সরলরেখা", "বৃত্ত",
         "বিন্যাস ও সমাবেশ", "ত্রিকোণমিতিক অনুপাত", "সংযুক্ত কোণের ত্রিকোণমিতিক অনুপাত",
         "ফাংশন ও ফাংশনের লেখচিত্র", "অন্তরীকরণ", "যোগজীকরণ"]),
        ("math-2", "উচ্চতর গণিত ২য় পত্র", ["বাস্তব সংখ্যা ও অসমতা", "রৈখিক প্রোগ্রামিং", "জটিল সংখ্যা",
         "বহুপদী ও বহুপদী সমীকরণ", "দ্বিপদী বিস্তৃতি", "কণিক", "বিপরীত ত্রিকোণমিতিক ফাংশন ও ত্রিকোণমিতিক সমীকরণ",
         "স্থিতিবিদ্যা", "সমতলে বস্তুকণার গতি", "বিস্তার পরিমাপ ও সম্ভাবনা"]),
    ]:
        books.append({"id": book_id, "subject": "HigherMath", "paper": book_id,
                      "title": title, "kind": "textbook", "tracks": ["versity"],
                      "chapters": [{"id": f"{book_id}-{i:02}", "number": i, "title": t}
                                   for i, t in enumerate(chapters, 1)]})
    topics = {
        "english": ("English", "ইংরেজি · Grammar & Vocabulary", [
            "Parts of Speech & Identification", "Right Form of Verbs & Conditionals", "Subject-Verb Agreement",
            "Prepositions & Phrasal Verbs", "Voice & Narration", "Synonyms & Antonyms", "Spelling & Pinpoint Errors",
            "Idioms & Phrases", "Clauses, Sentence Structure & Translation", "One-Word Substitution & Lexicon"]),
        "gk": ("General Knowledge", "সাধারণ জ্ঞান · বাংলাদেশ ও আন্তর্জাতিক", [
            "বাংলাদেশ বিষয়াবলী", "মুক্তিযুদ্ধ ও স্বাধীনতা", "ইতিহাস, ঐতিহ্য ও প্রাচীন জনপদ",
            "সংবিধান, সংসদ ও জাতীয় প্রতীক", "ভৌগোলিক পরিচিতি, সীমানা ও প্রকৃতি",
            "চিকিৎসা বিজ্ঞান ও জনস্বাস্থ্য খাত", "আন্তর্জাতিক বিষয়াবলী ও বৈশ্বিক ভূগোল", "আন্তর্জাতিক সংস্থা ও বিশ্ব স্বাস্থ্য"]),
    }
    for book_id, (subject, title, names) in topics.items():
        books.append({"id": book_id, "subject": subject, "paper": "topic", "title": title,
                      "kind": "topics", "tracks": ["medical", "versity"],
                      "chapters": [{"id": f"{book_id}-{i:02}", "number": i, "title": t}
                                   for i, t in enumerate(names, 1)]})
    # Explicit gaps: these subjects may be required by some varsity units, but there is no bank.
    books.extend([
        {"id": "bangla", "subject": "Bangla", "paper": "", "title": "বাংলা · ভর্তি প্রস্তুতি",
         "kind": "topics", "tracks": ["versity"], "chapters": [{"id": f"bangla-{i:02}", "number": i, "title": t} for i,t in enumerate(["ধ্বনি ও বর্ণ", "সন্ধি", "সমাস", "শব্দ ও পদ", "কারক ও বিভক্তি", "বাক্য ও ক্রিয়া", "বানান ও শুদ্ধ প্রয়োগ", "সাহিত্য পরিচিতি"],1)], "note": "ভর্তি প্রস্তুতির বিষয়ভিত্তিক অনুশীলন; বাংলা ১ম পত্রের পূর্ণ পাঠতালিকা নয়।"},
        {"id": "ict", "subject": "ICT", "paper": "", "title": "তথ্য ও যোগাযোগ প্রযুক্তি",
         "kind": "textbook", "tracks": ["versity"], "chapters": [
             {"id": f"ict-{i:02}", "number": i, "title": t} for i,t in enumerate([
                 "তথ্য ও যোগাযোগ প্রযুক্তি: বিশ্ব ও বাংলাদেশ প্রেক্ষিত", "কমিউনিকেশন সিস্টেমস ও নেটওয়ার্কিং",
                 "সংখ্যা পদ্ধতি ও ডিজিটাল ডিভাইস", "ওয়েব ডিজাইন পরিচিতি ও HTML", "প্রোগ্রামিং ভাষা",
                 "ডেটাবেজ ম্যানেজমেন্ট সিস্টেম"],1)]},
    ])
    return books

def build():
    books = catalog()
    mapping = {}
    for book in books:
        for chapter in book["chapters"]:
            mapping[(book["subject"], book["paper"], chapter_name(chapter["title"]))] = chapter["id"]
    aliases = {
        "নগ্নবীজী ও আবৃতবীজী": "biology-1-07",
        "প্রাণীর পরিচিতি": "biology-2-02",
        "মানব শারীরতত্ত্ব: শ্বসন ও শ্বাসক্রিয়া": "biology-2-05",
        "ফাংশন ও লেখচিত্র": "math-1-08",
        "কণিক": "math-2-06", "বিপরীত ত্রিকোণমিতিক ফাংশন": "math-2-07",
        "ত্রিকোণমিতিক সমীকরণ": "math-2-07", "গতিবিদ্যা": "math-2-09",
        "সম্ভাবনা ও বিস্তার": "math-2-10",
        "Appropriate Prepositions & Phrasal Verbs": "english-04", "Spelling Correction": "english-07",
        "Idioms, Phrases & Proverbs": "english-08", "মুক্তিযুদ্ধ ও বীরশ্রেষ্ঠ": "gk-02",
        "সংবিধান ও জাতীয় প্রতীক": "gk-04", "স্বাস্থ্য খাত ও অর্জন": "gk-06",
        "আন্তর্জাতিক সংস্থা ও স্বাস্থ্য খাত": "gk-08",
    }
    records = collections.defaultdict(list)
    report = collections.Counter()
    for filename in SOURCES:
        for q in walk(json.loads((ROOT / "data" / filename).read_text())):
            report["input_entries"] += 1
            subject = q.get("subject", "")
            name = chapter_name(q.get("chapter", ""))
            paper = q.get("sub_discipline", "")
            if subject == "HigherMath":
                paper = "math-1" if name in {chapter_name(c["title"]) for c in books[6]["chapters"]} else "math-2"
            elif subject in ("English", "General Knowledge"):
                paper = "topic"
            cid = mapping.get((subject, paper, name))
            alias = next((v for k,v in aliases.items() if chapter_name(k) == name), None)
            if not cid and alias and alias.startswith({"Biology":"biology", "Chemistry":"chemistry",
                "Physics":"physics", "HigherMath":"math", "English":"english", "General Knowledge":"gk"}.get(subject,"!")):
                cid = alias
            # Broad miscellaneous labels must not masquerade as specific textbook chapters.
            if not cid:
                report["unmapped_entries"] += 1
                continue
            options = q.get("options") or [q.get("option_" + c, "") for c in "abcd"]
            correct = q.get("correct_index")
            if not isinstance(correct, int) or isinstance(correct, bool) or not 0 <= correct < 4 or len(options) != 4 \
                    or not all(isinstance(o, str) and o.strip() for o in options) or not q.get("question_bn", "").strip():
                report["invalid_entries"] += 1
                continue
            # Dedup at subject/question level; compare answer text so reordered options are safe.
            key = (subject, norm(q["question_bn"]))
            records[key].append((cid, options, correct, q, filename))
    pools = collections.defaultdict(list)
    for (subject, stem), candidates in records.items():
        answers = {norm(o[i]) for _,o,i,_,_ in candidates}
        if len(answers) > 1:
            report["conflicting_answer_questions"] += 1
            continue
        chapters = {c[0] for c in candidates}
        if len(chapters) > 1:
            report["conflicting_chapter_questions"] += 1
            continue
        cid, options, correct, q, filename = candidates[0]
        uid = hashlib.sha256((subject + ':' + stem).encode()).hexdigest()[:16]
        pools[cid].append({"id": uid, "question_bn": q["question_bn"], "options": options,
                           "correct_index": correct, "explanation": q.get("explanation", ""),
                           "book_reference": q.get("book_reference", ""),
                           "source_files": sorted({c[4] for c in candidates})})
        report["duplicate_entries_removed"] += len(candidates) - 1
    from original_practice import make_original_questions
    originals = make_original_questions(books)
    for book in books:
        for chapter in book["chapters"]:
            cid = chapter["id"]
            existing = sorted(pools[cid], key=lambda q:q["id"])
            target = 300 if book["subject"] == "Chemistry" else 100
            seen = {norm(q["question_bn"]) for q in existing}
            additions = [q for q in originals[cid] if norm(q["question_bn"]) not in seen]
            questions = existing[:target] + additions[:max(0, target-len(existing))]
            assert len(questions) == target, (cid, len(questions), target)
            chapter["existing_questions"] = min(len(existing), target)
            chapter["original_questions"] = len(questions)-chapter["existing_questions"]
            chapter["question_format_note"] = ("মৌলিক প্রশ্নে দুই-বক্তব্যভিত্তিক ধারণা যাচাই রয়েছে।" if book["subject"] not in ("Physics", "HigherMath") else "মৌলিক প্রশ্নে সূত্রভিত্তিক সংখ্যাগত অনুশীলন রয়েছে; একই ধারণার ভিন্ন সংখ্যাগত সমস্যা থাকতে পারে।")
            report["original_questions_added"] += chapter["original_questions"]
            target = 300 if book["subject"] == "Chemistry" else 100
            chapter["available_questions"] = len(questions)
            chapter["target_questions"] = target
            chapter["questions"] = questions[:target]
            chapter["sets"] = [{"id": f'{chapter["id"]}-set-{i+1}', "number": i+1,
                               "question_ids": [q["id"] for q in questions[i*100:(i+1)*100]]}
                               for i in range(3 if target == 300 else 1)]
        book["available_questions"] = sum(len(c["questions"]) for c in book["chapters"])
    data = {"version": 2, "books": books, "sources": [
        {"title": "College HSC subject/paper syllabus and chapter references", "url": "https://www.skisc.edu.bd/public/Syllabus%202025/National%20Curriculum/HSC-syllabus-science.pdf"},
        {"title": "Chemistry first-paper chapter catalogue", "url": "https://www.oriole.com.bd/academic/class-11-12/class-11-12-chemistry-1"},
        {"title": "Chemistry second-paper chapter catalogue", "url": "https://www.oriole.com.bd/academic/class-11-12/class-11-12-chemistry-2"}], "audit": dict(report)}
    # Keep catalogue tiny; download only the chosen chapter's questions.
    manifest = copy.deepcopy(data)
    for book in manifest["books"]:
        for chapter in book["chapters"]:
            payload = next(c for b in books for c in b["chapters"] if c["id"] == chapter["id"])
            body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
            digest = hashlib.sha256(body.encode()).hexdigest()[:12]
            chapter["questions_url"] = f'/data/chapter_practice/{chapter["id"]}-{digest}.json'
            chapter["question_count"] = len(chapter.pop("questions"))
            for question_set in chapter["sets"]:
                question_set["question_count"] = len(question_set.pop("question_ids"))
            for directory in ["data", "public/data"]:
                destination = ROOT / directory / "chapter_practice"
                destination.mkdir(exist_ok=True)
                (destination / f'{chapter["id"]}-{digest}.json').write_text(body)
    for directory in ["data", "public/data"]:
        (ROOT / directory / "chapter_practice.json").write_text(json.dumps(manifest, ensure_ascii=False, separators=(",", ":")))
    rows = ["# Chapter practice coverage", "", "Existing repository questions plus original chapter practice. No book PDFs or claimed textbook quotations were imported.", "",
            "100 questions per chapter target; chemistry targets three disjoint 100-question sets per chapter.",
            "Every listed chapter/topic has exactly 100 questions; chemistry has three disjoint 100-question sets. Broad/conflicting legacy labels are excluded.", "",
            "Original items use explicit concept/misconception pairs and worked numerical templates. Distinct items may test shared concepts; numerical variants are not distinct learning outcomes. Structural and arithmetic checks do not replace independent educational review.", "", "| Book | Chapter | Existing retained | Original added | Published | Target |", "|---|---|---:|---:|---:|---:|"]
    for book in books:
        for c in book["chapters"]:
            rows.append(f'| {book["title"]} | {c["number"]}. {c["title"]} | {c["existing_questions"]} | {c["original_questions"]} | {len(c["questions"])} | {c["target_questions"]} |')
    rows += ["", "## Audit", ""] + [f"- {k}: {v}" for k,v in report.items()]
    (ROOT / "CHAPTER_PRACTICE_COVERAGE.md").write_text('\n'.join(rows) + '\n')
    print(json.dumps({"books": len(books), "chapters": sum(len(b["chapters"]) for b in books),
                      "published_questions": sum(b["available_questions"] for b in books), "audit":dict(report)},indent=2))

if __name__ == "__main__":
    build()
