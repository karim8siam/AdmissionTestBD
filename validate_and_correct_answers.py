import sqlite3
import json
import re

DB_PATH = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/biology_100_tests.db"
JSON_PATH = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/biology_100_tests.json"
CSV_PATH = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/biology_100_tests.csv"

# Definitive NCTB Ground Truth Rules: (Pattern / Key topic in Bengali, Target correct option text, Explanation)
GROUND_TRUTH_RULES = [
    (
        r'শ্বাস-প্রশ্বাস.*স্পন্দনহার|স্পন্দনহার.*শ্বাস-প্রশ্বাস',
        'মেডুলা',
        'মেডুলা অবলংগাটা মানবদেহের শ্বাসক্রিয়া (শ্বসন কেন্দ্র), হৃৎস্পন্দন, রক্তচাপ এবং স্বয়ংক্রিয় কার্যাবলি নিয়ন্ত্রণ করে। পনস কেবল নিউমোট্যাক্সিক কেন্দ্র বহন করে। (রেফারেন্স: গাজী আজমল, সমন্বয় ও নিয়ন্ত্রণ)।'
    ),
    (
        r'অধিকাংশ আবৃতবীজী উদ্ভিদে কোন ধরনের ভ্রূনথলি',
        'পলিগোনাম',
        'অধিকাংশ আবৃতবীজী উদ্ভিদে (প্রায় ৭৫%) মনোস্পোরিক পলিগোনাম (Polygonum) প্রকৃতির ভ্রূণথলি দেখা যায় যা ৭টি কোষ ও ৮টি নিউক্লিয়াসবিশিষ্ট। (রেফারেন্স: ড. আবুল হাসান, উদ্ভিদ প্রজনন)।'
    ),
    (
        r'শাপলা কোন ধরণের উদ্ভিদ',
        'হাইড্রোফাইট',
        'শাপলা (Nymphaea nouchali) একটি মূলবদ্ধ ভাসমান জলজ উদ্ভিদ বা হাইড্রোফাইট (Hydrophyte)। (রেফারেন্স: ড. আবুল হাসান, জীবের পরিবেশ ও বিস্তার)।'
    ),
    (
        r'টাঙ্গুয়ার হাওর',
        'সুনামগঞ্জ',
        'টাঙ্গুয়ার হাওর সুনামগঞ্জ জেলার ধর্মপাশা ও তাহিরপুর উপজেলায় অবস্থিত বাংলাদেশের একটি রামসার সাইট। (সাধারণ জ্ঞান)।'
    ),
    (
        r'পরিপাকে সাহায্যকারী উৎসেচক কোনটি|পরিপাকে সাহায্যকারী',
        'সিক্রেটিন',
        'সিক্রেটিন একটি পেপটাইড হরমোন যা ডিওডেনাম থেকে ক্ষরিত হয়ে অগ্ন্যাশয় রস ও পিত্ত ক্ষরণ উদ্দীপিত করে পরিপাকে সহায়তা করে। (রেফারেন্স: গাজী আজমল, পরিপাক অধ্যায়)।'
    ),
    (
        r'হাইড্রার দেহে বিদ‍্যমান|কোনটি হাইড্রার দেহে',
        'মেসোগ্লিয়া',
        'হাইড্রা একটি দ্বিস্তরী বা ডিপ্লোব্লাস্টিক প্রাণী, এর একটোডার্ম ও এন্ডোডার্মের মাঝে অকোষীয় আঠালো মেসোগ্লিয়া স্তর থাকে। (রেফারেন্স: গাজী আজমল, হাইড্রা অধ্যায়)।'
    ),
    (
        r'রুই মাছের বক্ষ পাখনা থেকে রক্ত গৃহীত হয়',
        'সাবক্ল্যাভিয়ান',
        'রুই মাছের বক্ষ পাখনা ও বক্ষ চক্র থেকে রক্ত সাবক্ল্যাভিয়ান (Subclavian) শিরার মাধ্যমে সংগৃহীত হয়ে কুভিয়ের ডাক্টে প্রবেশ করে। (রেফারেন্স: গাজী আজমল, রুই মাছ অধ্যায়)।'
    ),
    (
        r'মানুষের গ্রীবাদেশীয় কশেরুকা',
        '৭',
        'মানুষের গ্রীবাদেশীয় বা সারভাইকাল (Cervical) কশেরুকা ৭টি। প্রথমটি অ্যাটলাস এবং দ্বিতীয়টি অ্যাক্সিস নামে পরিচিত। (রেফারেন্স: গাজী আজমল, চলন ও অঙ্গচালনা)।'
    ),
    (
        r'পাকস্থলীর প্যারাইটাল.*কোষ থেকে|অক্সিন্টিক কোষ থেকে',
        'হাইড্রোক্লোরিক এসিড',
        'পাকস্থলীর অক্সিন্টিক বা প্যারাইটাল কোষ থেকে হাইড্রোক্লোরিক এসিড (HCl) ক্ষরিত হয় যা পেপসিনোজেনকে সক্রিয় পেপসিনে রূপান্তর করে। (রেফারেন্স: গাজী আজমল, পরিপাক ও শোষণ)।'
    ),
    (
        r'মায়ের দুধের মাধ্যমে.*কোন অ্যান্টিবডি|শালদুধে',
        'IgA',
        'মায়ের শালদুধে (Colostrum) সিক্রেটরি IgA অ্যান্টিবডি প্রচুর পরিমাণে থাকে যা নবজাতককে অন্ত্রীয় নিষ্ক্রিয় অনাক্রম্যতা প্রদান করে। অমরা ভেদ করে IgG। (রেফারেন্স: গাজী আজমল, প্রতিরক্ষা অধ্যায়)।'
    ),
    (
        r'রক্ত তঞ্চনের কত নম্বর ফ্যাক্টরটি ক্রিসমাস ফ্যাক্টর',
        'ফ্যাক্টর IX',
        'ফ্যাক্টর IX (নয় নম্বর ফ্যাক্টর) কে ক্রিসমাস ফ্যাক্টর বলা হয়। এর বংশগত ঘাটতিতে হিমোফিলিয়া-বি বা ক্রিসমাস রোগ হয়। (রেফারেন্স: গাজী আজমল, রক্ত ও সংবহন)।'
    ),
    (
        r'কোন কপাটিকায় তিনটি কাস্প.*থাকে না|কোন কপাটিকায় দুটি কাস্প',
        'বাইকাসপিড',
        'হৃৎপিণ্ডের বাম অলিন্দ ও বাম নিলয়ের মাঝে অবস্থিত বাইকাসপিড বা মাইট্রাল কপাটিকায় ২টি কাস্প থাকে। বাকি সব কপাটিকায় ৩টি কাস্প থাকে। (রেফারেন্স: গাজী আজমল)।'
    ),
    (
        r'মিয়োসিস-১ এর.*কায়াজমা ও ক্রসিং ওভার',
        'প্যাকাইটিন',
        'মিয়োসিস-১ এর প্রফেজ-১ এর প্যাকাইটিন দশায় নন-সিস্টার ক্রোমাটিডের মধ্যে কায়াজমা ও ক্রসিং ওভার সংঘটিত হয়। (রেফারেন্স: ড. আবুল হাসান, কোষ বিভাজন)।'
    ),
    (
        r'C4 চক্রে কার্বন ডাই-অক্সাইডের প্রথম গ্রহীতা',
        'ফসফোইনল পাইরুভিক এসিড',
        'C4 চক্রে CO2 এর প্রথম গ্রহীতা ফসফোইনল পাইরুভিক এসিড (PEP, ৩ কার্বন)। C3 চক্রে RuBP। (রেফারেন্স: ড. আবুল হাসান, উদ্ভিদ শারীরতত্ত্ব)।'
    ),
    (
        r'একবীজপত্রী উদ্ভিদের কাণ্ডের ভাস্কুলার বান্ডল',
        'সমপার্শ্বীয় বদ্ধ',
        'একবীজপত্রী কাণ্ডের ভাস্কুলার বান্ডল সমপার্শ্বীয় বদ্ধ (Collateral closed) প্রকৃতির অর্থাৎ এতে ক্যাম্বিয়াম অনুপস্থিত থাকে। (রেফারেন্স: ড. আবুল হাসান, টিস্যুতন্ত্র)।'
    ),
    (
        r'আণবিক কাঁচি হিসেবে কাজ করে|আণবিক কাঁচি',
        'রেস্ট্রিকশন এন্ডোনিউক্লিয়েজ',
        'রেস্ট্রিকশন এন্ডোনিউক্লিয়েজ এনজাইম ডিএনএ অণুর নির্দিষ্ট ক্ষারীয় ক্রম চিনে দ্বিসূত্রক কাটে বিধায় একে আণবিক কাঁচি বলে। লাইগেজ হলো আণবিক আঠা। (রেফারেন্স: ড. আবুল হাসান, জীবপ্রযুক্তি)।'
    ),
    (
        r'ম্যালভেসি.*গোত্রের উদ্ভিদের পুংকেশর|ম্যালভেসি.*গোত্রের শনাক্তকারী',
        'একগুচ্ছক',
        'ম্যালভেসি গোত্রের পুংকেশর বহু এবং একগুচ্ছক (Monadelphous), এবং পরাগধানী একপ্রকোষ্ঠী ও বৃক্কাকার। (রেফারেন্স: ড. আবুল হাসান, নগ্নবীজী ও আবৃতবীজী)।'
    ),
    (
        r'হুইটস্টোন ব্রিজের সাম্যাবস্থার শর্ত',
        'P/Q = R/S',
        'হুইটস্টোন ব্রিজের সাম্যাবস্থার ক্ষেত্রে গ্যালভানোমিটার প্রবাহ শূন্য হলে রোধের অনুপাত P/Q = R/S হয়। (রেফারেন্স: মোহাম্মদ ইসহাক, চল তড়িৎ)।'
    ),
    (
        r'ক্লোরাইড শিফট বা হ্যামবার্গার শিফটের মূল উদ্দেশ্য',
        'তড়িৎ নিরপেক্ষতা',
        'লোহিত রক্তকণিকা ও প্লাজমার মধ্যে HCO3- ও Cl- আয়নের বিনিময়ের মাধ্যমে রক্তের তড়িৎ নিরপেক্ষতা ও অ্যাসিড-ক্ষার সমতা অক্ষুণ্ণ থাকে। (রেফারেন্স: গাজী আজমল)।'
    ),
    (
        r'নেফ্রনের কোন অংশে গ্লোমেরুলার ফিল্ট্রেটের সর্বাধিক.*পুনঃশোষিত',
        'নিকটবর্তী পেঁচানো নালিকা',
        'প্রক্সিমাল কনভোলুটেড টিউবিউল বা নিকটবর্তী পেঁচানো নালিকায় ফিল্ট্রেটের প্রায় ৬৫-৮০% পানি ও প্রয়োজনীয় খাদ্য উপাদান পুনঃশোষিত হয়। (রেফারেন্স: গাজী আজমল)।'
    )
]

def audit_and_correct_all_questions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, question_bn, option_a, option_b, option_c, option_d, correct_option, correct_index FROM biology_questions")
    rows = cursor.fetchall()

    print(f"Auditing all {len(rows)} questions against NCTB Ground Truth Rules...")

    opt_labels = ['ক', 'খ', 'গ', 'ঘ']
    corrected_count = 0
    updates = []

    for r in rows:
        qid, q_text, opt_a, opt_b, opt_c, opt_d, curr_opt, curr_idx = r
        opts = [opt_a, opt_b, opt_c, opt_d]

        for pattern, target_keyword, expl in GROUND_TRUTH_RULES:
            if re.search(pattern, q_text, re.IGNORECASE):
                # Find which option contains the target keyword
                found_idx = None
                for idx, o in enumerate(opts):
                    if target_keyword.lower() in o.lower():
                        found_idx = idx
                        break

                if found_idx is not None and found_idx != curr_idx:
                    new_lbl = opt_labels[found_idx]
                    updates.append((new_lbl, found_idx, expl, qid))
                    corrected_count += 1
                break

    print(f"Identified {corrected_count} questions needing fact-checked answer key alignment.")

    if updates:
        cursor.executemany("""
            UPDATE biology_questions 
            SET correct_option = ?, correct_index = ?, explanation = ?
            WHERE id = ?
        """, updates)
        conn.commit()
        print("All corrections applied successfully to SQLite database.")

    conn.close()

    # Re-export JSON and CSV
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM biology_questions ORDER BY test_id, question_num")
    updated_rows = [dict(r) for r in c.fetchall()]
    conn.close()

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(updated_rows, f, ensure_ascii=False, indent=2)
    print(f"Updated JSON export at {JSON_PATH}")

    import csv
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=updated_rows[0].keys())
        writer.writeheader()
        writer.writerows(updated_rows)
    print(f"Updated CSV export at {CSV_PATH}")

if __name__ == '__main__':
    audit_and_correct_all_questions()
