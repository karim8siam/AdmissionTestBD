import sqlite3
from init_textbook_db import TEXTBOOK_DB_PATH

BOOKS = [
    {
        "id": "BOOK-BOTANY-HASAN",
        "title_bn": "উচ্চ মাধ্যমিক উদ্ভিদবিজ্ঞান (একাদশ-দ্বাদশ শ্রেণি)",
        "title_en": "Higher Secondary Botany",
        "author": "ড. মোহাম্মদ আবুল হাসান",
        "subject": "Biology",
        "paper": "Botany (১ম পত্র)",
        "publisher": "হাসান বুক হাউস",
        "edition": "Latest Medical Admission Standard Edition",
        "total_chapters": 12,
        "importance_note": "মেডিকেল ভর্তি পরীক্ষায় উদ্ভিদবিজ্ঞানের ১৫ নম্বরের প্রায় ৯৫% প্রশ্ন সরাসরি এই বইয়ের লাইন ও ছক থেকে আসে।"
    },
    {
        "id": "BOOK-ZOOLOGY-AZMAL",
        "title_bn": "উচ্চ মাধ্যমিক প্রাণিবিজ্ঞান (একাদশ-দ্বাদশ শ্রেণি)",
        "title_en": "Higher Secondary Zoology",
        "author": "গাজী আজমল ও গাজী আসমত",
        "subject": "Biology",
        "paper": "Zoology (২য় পত্র)",
        "publisher": "গাজী পাবলিশার্স",
        "edition": "Latest Medical Admission Standard Edition",
        "total_chapters": 12,
        "importance_note": "মেডিকেল ভর্তি পরীক্ষার প্রাণিবিজ্ঞানের ১৫ নম্বরের প্রশ্ন নির্বাচনকারী শিক্ষকদের প্রধান ও আবশ্যকীয় মূল বই।"
    },
    {
        "id": "BOOK-CHEM-HAZARI-1",
        "title_bn": "রসায়ন ১ম পত্র (একাদশ-দ্বাদশ শ্রেণি)",
        "title_en": "Higher Secondary Chemistry 1st Paper",
        "author": "প্রফেসর মহব্বত হাসান হাজারী ও স্বপন কুমার নাগ",
        "subject": "Chemistry",
        "paper": "1st Paper",
        "publisher": "হাসান বুক হাউস",
        "edition": "Latest Medical Admission Standard Edition",
        "total_chapters": 5,
        "importance_note": "গুণগত রসায়ন, পর্যায়বৃত্ত ধর্ম ও কর্মমুখী রসায়নের সরাসরি লাইন, ছক ও অনুশীলনীর প্রশ্ন শতভাগ নির্ভরযোগ্য।"
    },
    {
        "id": "BOOK-CHEM-HAZARI-2",
        "title_bn": "রসায়ন ২য় পত্র (একাদশ-দ্বাদশ শ্রেণি)",
        "title_en": "Higher Secondary Chemistry 2nd Paper",
        "author": "প্রফেসর মহব্বত হাসান হাজারী ও স্বপন কুমার নাগ",
        "subject": "Chemistry",
        "paper": "2nd Paper",
        "publisher": "হাসান বুক হাউস",
        "edition": "Latest Medical Admission Standard Edition",
        "total_chapters": 5,
        "importance_note": "জৈব রসায়নের শনাক্তকারী পরীক্ষা, পলিমার, পরিমাণগত ও পরিবেশ রসায়নের একক ও তথ্যের প্রধান উৎস।"
    },
    {
        "id": "BOOK-PHYS-ISHAQ-1",
        "title_bn": "পদার্থবিজ্ঞান ১ম পত্র (একাদশ-দ্বাদশ শ্রেণি)",
        "title_en": "Higher Secondary Physics 1st Paper",
        "author": "ড. আমির হোসেন খান ও প্রফেসর মোহাম্মদ ইসহাক",
        "subject": "Physics",
        "paper": "1st Paper",
        "publisher": "আইডিয়াল লাইব্রেরী",
        "edition": "Latest Medical Admission Standard Edition",
        "total_chapters": 10,
        "importance_note": "মেডিকেল ভর্তি পরীক্ষায় পদার্থবিজ্ঞানের সংজ্ঞা, একক, মাত্রা এবং অনুধাবনমূলক তথ্যের শীর্ষ উৎস।"
    },
    {
        "id": "BOOK-PHYS-ISHAQ-2",
        "title_bn": "পদার্থবিজ্ঞান ২য় পত্র (একাদশ-দ্বাদশ শ্রেণি)",
        "title_en": "Higher Secondary Physics 2nd Paper",
        "author": "ড. আমির হোসেন খান ও প্রফেসর মোহাম্মদ ইসহাক",
        "subject": "Physics",
        "paper": "2nd Paper",
        "publisher": "আইডিয়াল লাইব্রেরী",
        "edition": "Latest Medical Admission Standard Edition",
        "total_chapters": 11,
        "importance_note": "তাপগতিবিদ্যা, চল তড়িৎ, আধুনিক পদার্থবিজ্ঞান ও সেমিকন্ডাক্টরের মেডিকেল প্যাটার্ন প্রশ্নের ভিত্তি।"
    },
    {
        "id": "BOOK-ENG-MEDICAL",
        "title_bn": "মেডিকেল ইংলিশ রেফারেন্স ও ব্যাকরণ সংকলন",
        "title_en": "Medical English Master Compendium",
        "author": "NCTB English Curriculum & Master Competitive Grammar",
        "subject": "English",
        "paper": "Grammar & Vocabulary",
        "publisher": "Medical Admission Council Reference",
        "edition": "Latest Standard Edition",
        "total_chapters": 8,
        "importance_note": "মেডিকেল পরীক্ষায় ১৫ নম্বরের জন্য এপ্রোপ্রিয়েট প্রিপজিশন, সিনোনিম-অ্যান্টোনিম ও রুলসের উৎস।"
    },
    {
        "id": "BOOK-GK-MEDICAL",
        "title_bn": "মেডিকেল সাধারণ জ্ঞান, মুক্তিযুদ্ধ ও স্বাস্থ্য ইতিহাস",
        "title_en": "Medical General Knowledge & Liberation War Compendium",
        "author": "জাতীয় ইতিহাস পরিষদ ও DGME স্বাস্থ্য আর্কাইভ",
        "subject": "General Knowledge",
        "paper": "Bangladesh & International",
        "publisher": "Govt & National Archives Reference",
        "edition": "Latest Standard Edition",
        "total_chapters": 7,
        "importance_note": "১৯৭১ মুক্তিযুদ্ধ, বঙ্গবন্ধু, সংবিধান, মেগা প্রজেক্ট এবং WHO স্বাস্থ্য খাত সম্পর্কিত ১০ নম্বরের পূর্ণাঙ্গ ডাটাবেজ।"
    }
]

CHAPTERS = [
    # Botany Chapters
    ("HASAN-CH-01", "BOOK-BOTANY-HASAN", 1, "কোষ ও এর গঠন", "Cell and its structure", 5, "২-৩ প্রশ্ন"),
    ("HASAN-CH-02", "BOOK-BOTANY-HASAN", 2, "কোষ বিভাজন", "Cell Division", 5, "১-২ প্রশ্ন"),
    ("HASAN-CH-03", "BOOK-BOTANY-HASAN", 3, "কোষ রসায়ন", "Cell Chemistry", 4, "১ প্রশ্ন"),
    ("HASAN-CH-04", "BOOK-BOTANY-HASAN", 4, "অণুজীব", "Microorganisms", 5, "২-৩ প্রশ্ন"),
    ("HASAN-CH-05", "BOOK-BOTANY-HASAN", 5, "শৈবাল ও ছত্রাক", "Algae and Fungi", 4, "১ প্রশ্ন"),
    ("HASAN-CH-06", "BOOK-BOTANY-HASAN", 6, "ব্রায়োফাইটা ও টেরিডোফাইটা", "Bryophyta & Pteridophyta", 3, "১ প্রশ্ন"),
    ("HASAN-CH-07", "BOOK-BOTANY-HASAN", 7, "নগ্নবীজী ও আবৃতবীজী উদ্ভিদ", "Gymnosperms & Angiosperms", 5, "২ প্রশ্ন"),
    ("HASAN-CH-08", "BOOK-BOTANY-HASAN", 8, "টিস্যু ও টিস্যুতন্ত্র", "Tissue & Tissue System", 5, "১-২ প্রশ্ন"),
    ("HASAN-CH-09", "BOOK-BOTANY-HASAN", 9, "উদ্ভিদ শারীরতত্ত্ব", "Plant Physiology", 5, "২-৩ প্রশ্ন"),
    ("HASAN-CH-10", "BOOK-BOTANY-HASAN", 10, "উদ্ভিদ প্রজনন", "Plant Reproduction", 4, "১ প্রশ্ন"),
    ("HASAN-CH-11", "BOOK-BOTANY-HASAN", 11, "জীবপ্রযুক্তি", "Biotechnology", 5, "১-২ প্রশ্ন"),
    ("HASAN-CH-12", "BOOK-BOTANY-HASAN", 12, "জীবের পরিবেশ, বিস্তার ও সংরক্ষণ", "Ecology & Conservation", 4, "১ প্রশ্ন"),

    # Zoology Chapters
    ("AZMAL-CH-01", "BOOK-ZOOLOGY-AZMAL", 1, "প্রাণীর বিভিন্নতা ও শ্রেণিবিন্যাস", "Animal Diversity & Classification", 5, "২-৩ প্রশ্ন"),
    ("AZMAL-CH-02", "BOOK-ZOOLOGY-AZMAL", 2, "প্রাণীর পরিচিতি (হাইড্রা, ঘাসফড়িং, রুই মাছ)", "Introduction to Animals", 5, "২-৩ প্রশ্ন"),
    ("AZMAL-CH-03", "BOOK-ZOOLOGY-AZMAL", 3, "মানব শারীরতত্ত্ব: পরিপাক ও শোষণ", "Digestion & Absorption", 5, "২ প্রশ্ন"),
    ("AZMAL-CH-04", "BOOK-ZOOLOGY-AZMAL", 4, "মানব শারীরতত্ত্ব: রক্ত ও সংবহন", "Blood & Circulation", 5, "২-৩ প্রশ্ন"),
    ("AZMAL-CH-05", "BOOK-ZOOLOGY-AZMAL", 5, "মানব শারীরতত্ত্ব: শ্বাসক্রিয়া ও শ্বসন", "Respiration & Breathing", 5, "১-২ প্রশ্ন"),
    ("AZMAL-CH-06", "BOOK-ZOOLOGY-AZMAL", 6, "মানব শারীরতত্ত্ব: বর্জ্য ও নিষ্কাশন", "Excretion", 5, "১-২ প্রশ্ন"),
    ("AZMAL-CH-07", "BOOK-ZOOLOGY-AZMAL", 7, "মানব শারীরতত্ত্ব: চলন ও অঙ্গচালনা", "Locomotion & Movement", 4, "১-২ প্রশ্ন"),
    ("AZMAL-CH-08", "BOOK-ZOOLOGY-AZMAL", 8, "মানব শারীরতত্ত্ব: সমন্বয় ও নিয়ন্ত্রণ", "Coordination & Control", 5, "২ প্রশ্ন"),
    ("AZMAL-CH-09", "BOOK-ZOOLOGY-AZMAL", 9, "মানব জীবনের ধারাবাহিকতা", "Human Reproduction", 4, "১ প্রশ্ন"),
    ("AZMAL-CH-10", "BOOK-ZOOLOGY-AZMAL", 10, "মানবদেহের প্রতিরক্ষা", "Human Immunity", 5, "২ প্রশ্ন"),
    ("AZMAL-CH-11", "BOOK-ZOOLOGY-AZMAL", 11, "জিনতত্ত্ব ও বিবর্তন", "Genetics & Evolution", 5, "২-৩ প্রশ্ন"),
    ("AZMAL-CH-12", "BOOK-ZOOLOGY-AZMAL", 12, "প্রাণীর আচরণ", "Animal Behavior", 3, "১ প্রশ্ন"),

    # Chemistry 1st Paper Chapters
    ("HAZARI1-CH-01", "BOOK-CHEM-HAZARI-1", 1, "ল্যাবরেটরির নিরাপদ ব্যবহার", "Safe Use of Laboratory", 3, "১ প্রশ্ন"),
    ("HAZARI1-CH-02", "BOOK-CHEM-HAZARI-1", 2, "গুণগত রসায়ন", "Qualitative Chemistry", 5, "৩-৪ প্রশ্ন"),
    ("HAZARI1-CH-03", "BOOK-CHEM-HAZARI-1", 3, "পর্যায়বৃত্ত ধর্ম ও রাসায়নিক বন্ধন", "Periodic Properties & Bonding", 5, "৩-৪ প্রশ্ন"),
    ("HAZARI1-CH-04", "BOOK-CHEM-HAZARI-1", 4, "রাসায়নিক পরিবর্তন", "Chemical Changes", 5, "২-৩ প্রশ্ন"),
    ("HAZARI1-CH-05", "BOOK-CHEM-HAZARI-1", 5, "কর্মমুখী রসায়ন", "Working Chemistry", 4, "২ প্রশ্ন"),

    # Chemistry 2nd Paper Chapters
    ("HAZARI2-CH-01", "BOOK-CHEM-HAZARI-2", 1, "পরিবেশ রসায়ন", "Environmental Chemistry", 5, "২-৩ প্রশ্ন"),
    ("HAZARI2-CH-02", "BOOK-CHEM-HAZARI-2", 2, "জৈব রসায়ন", "Organic Chemistry", 5, "৪-৫ প্রশ্ন"),
    ("HAZARI2-CH-03", "BOOK-CHEM-HAZARI-2", 3, "পরিমাণগত রসায়ন", "Quantitative Chemistry", 5, "২-৩ প্রশ্ন"),
    ("HAZARI2-CH-04", "BOOK-CHEM-HAZARI-2", 4, "তড়িৎ রসায়ন", "Electrochemistry", 4, "১-২ প্রশ্ন"),
    ("HAZARI2-CH-05", "BOOK-CHEM-HAZARI-2", 5, "অর্থনৈতিক রসায়ন", "Economic Chemistry", 3, "১ প্রশ্ন"),

    # Physics 1st Paper Chapters
    ("ISHAQ1-CH-01", "BOOK-PHYS-ISHAQ-1", 1, "ভৌতজগৎ ও পরিমাপ", "Physical World & Measurement", 3, "১ প্রশ্ন"),
    ("ISHAQ1-CH-02", "BOOK-PHYS-ISHAQ-1", 2, "ভেক্টর", "Vectors", 5, "২ প্রশ্ন"),
    ("ISHAQ1-CH-03", "BOOK-PHYS-ISHAQ-1", 3, "গতিবিদ্যা", "Dynamics", 4, "১ প্রশ্ন"),
    ("ISHAQ1-CH-04", "BOOK-PHYS-ISHAQ-1", 4, "নিউটনিয়ান বলবিদ্যা", "Newtonian Mechanics", 5, "২ প্রশ্ন"),
    ("ISHAQ1-CH-05", "BOOK-PHYS-ISHAQ-1", 5, "কাজ, শক্তি ও ক্ষমতা", "Work, Energy & Power", 5, "১-২ প্রশ্ন"),
    ("ISHAQ1-CH-06", "BOOK-PHYS-ISHAQ-1", 6, "মহাকর্ষ ও অভিকর্ষ", "Gravitation & Gravity", 5, "১-২ প্রশ্ন"),
    ("ISHAQ1-CH-07", "BOOK-PHYS-ISHAQ-1", 7, "পদার্থের গাঠনিক ধর্ম", "Structural Properties of Matter", 5, "২ প্রশ্ন"),
    ("ISHAQ1-CH-08", "BOOK-PHYS-ISHAQ-1", 8, "পর্যায়বৃত্ত গতি", "Periodic Motion", 4, "১ প্রশ্ন"),
    ("ISHAQ1-CH-09", "BOOK-PHYS-ISHAQ-1", 9, "তরঙ্গ", "Waves", 4, "১ প্রশ্ন"),
    ("ISHAQ1-CH-10", "BOOK-PHYS-ISHAQ-1", 10, "আদর্শ গ্যাস ও গতিতত্ত্ব", "Ideal Gas & Kinetic Theory", 5, "২ প্রশ্ন"),

    # Physics 2nd Paper Chapters
    ("ISHAQ2-CH-01", "BOOK-PHYS-ISHAQ-2", 1, "তাপগতিবিদ্যা", "Thermodynamics", 5, "২ প্রশ্ন"),
    ("ISHAQ2-CH-02", "BOOK-PHYS-ISHAQ-2", 2, "স্থির তড়িৎ", "Static Electricity", 4, "১ প্রশ্ন"),
    ("ISHAQ2-CH-03", "BOOK-PHYS-ISHAQ-2", 3, "চল তড়িৎ", "Current Electricity", 5, "২ প্রশ্ন"),
    ("ISHAQ2-CH-04", "BOOK-PHYS-ISHAQ-2", 4, "তড়িৎ প্রবাহের চৌম্বক ক্রিয়া ও চুম্বকত্ব", "Magnetic Effects & Magnetism", 4, "১ প্রশ্ন"),
    ("ISHAQ2-CH-05", "BOOK-PHYS-ISHAQ-2", 5, "তাড়িৎচৌম্বকীয় আবেশ ও পরিবর্তী প্রবাহ", "Electromagnetic Induction & AC", 4, "১ প্রশ্ন"),
    ("ISHAQ2-CH-06", "BOOK-PHYS-ISHAQ-2", 6, "জ্যামিতিক আলোকবিজ্ঞান", "Geometric Optics", 5, "১-২ প্রশ্ন"),
    ("ISHAQ2-CH-07", "BOOK-PHYS-ISHAQ-2", 7, "ভৌত আলোকবিজ্ঞান", "Physical Optics", 4, "১ প্রশ্ন"),
    ("ISHAQ2-CH-08", "BOOK-PHYS-ISHAQ-2", 8, "আধুনিক পদার্থবিজ্ঞানের সূচনা", "Modern Physics", 5, "২ প্রশ্ন"),
    ("ISHAQ2-CH-09", "BOOK-PHYS-ISHAQ-2", 9, "পরমাণু মডেল ও নিউক্লিয়ার পদার্থবিজ্ঞান", "Atomic Model & Nuclear Physics", 5, "২ প্রশ্ন"),
    ("ISHAQ2-CH-10", "BOOK-PHYS-ISHAQ-2", 10, "সেমিকন্ডাক্টর ও ইলেকট্রনিক্স", "Semiconductors & Electronics", 5, "২ প্রশ্ন"),
    ("ISHAQ2-CH-11", "BOOK-PHYS-ISHAQ-2", 11, "জ্যোতির্বিজ্ঞান", "Astronomy", 3, "০-১ প্রশ্ন"),

    # English Modules
    ("ENG-MOD-01", "BOOK-ENG-MEDICAL", 1, "Appropriate Prepositions", "Appropriate Prepositions", 5, "২-৩ প্রশ্ন"),
    ("ENG-MOD-02", "BOOK-ENG-MEDICAL", 2, "Synonyms and Antonyms", "Synonyms and Antonyms", 5, "২-৩ প্রশ্ন"),
    ("ENG-MOD-03", "BOOK-ENG-MEDICAL", 3, "Subject-Verb Agreement", "Subject-Verb Agreement", 5, "১-২ প্রশ্ন"),
    ("ENG-MOD-04", "BOOK-ENG-MEDICAL", 4, "Right Form of Verbs & Conditionals", "Right Form of Verbs", 5, "১-২ প্রশ্ন"),
    ("ENG-MOD-05", "BOOK-ENG-MEDICAL", 5, "Voice and Narration", "Voice and Narration", 4, "১-২ প্রশ্ন"),
    ("ENG-MOD-06", "BOOK-ENG-MEDICAL", 6, "Spelling & Pinpoint Errors", "Spelling", 4, "১ প্রশ্ন"),
    ("ENG-MOD-07", "BOOK-ENG-MEDICAL", 7, "Idioms, Phrases & Proverbs", "Idioms & Phrases", 4, "১-২ প্রশ্ন"),
    ("ENG-MOD-08", "BOOK-ENG-MEDICAL", 8, "Parts of Speech Identification", "Parts of Speech", 5, "২ প্রশ্ন"),

    # GK Modules
    ("GK-MOD-01", "BOOK-GK-MEDICAL", 1, "প্রাচীন বাংলা ও ভাষা আন্দোলন (১৯৫২)", "History & 1952", 5, "১-২ প্রশ্ন"),
    ("GK-MOD-02", "BOOK-GK-MEDICAL", 2, "১৯৭১ মুক্তিযুদ্ধ, সেক্টর ও বীরশ্রেষ্ঠ", "Liberation War 1971", 5, "৩-৪ প্রশ্ন"),
    ("GK-MOD-03", "BOOK-GK-MEDICAL", 3, "বঙ্গবন্ধু শেখ মুজিবুর রহমান - জীবন ও গ্রন্থ", "Bangabandhu", 5, "২ প্রশ্ন"),
    ("GK-MOD-04", "BOOK-GK-MEDICAL", 4, "সংবিধান, ভৌগোলিক সীমানা ও মেগা প্রজেক্ট", "Constitution & Geography", 4, "১-২ প্রশ্ন"),
    ("GK-MOD-05", "BOOK-GK-MEDICAL", 5, "স্বাস্থ্য খাত ও কমিউনিটি ক্লিনিক অর্জন", "Health Sector & DGME", 5, "১-২ প্রশ্ন"),
    ("GK-MOD-06", "BOOK-GK-MEDICAL", 6, "জাতিসংঘ ও আন্তর্জাতিক সংস্থাসমূহ (WHO, UNICEF)", "International Organizations", 5, "১-২ প্রশ্ন"),
    ("GK-MOD-07", "BOOK-GK-MEDICAL", 7, "চিকিৎসাবিজ্ঞানে নোবেল পুরস্কার ও সাম্প্রতিক বিশ্ব", "Nobel in Medicine & Global Affairs", 4, "১ প্রশ্ন")
]

def seed_master_books_and_chapters():
    conn = sqlite3.connect(TEXTBOOK_DB_PATH)
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT OR REPLACE INTO books (id, title_bn, title_en, author, subject, paper, publisher, edition, total_chapters, importance_note)
        VALUES (:id, :title_bn, :title_en, :author, :subject, :paper, :publisher, :edition, :total_chapters, :importance_note)
    """, BOOKS)
    cursor.executemany("""
        INSERT OR REPLACE INTO book_chapters (id, book_id, chapter_num, chapter_name_bn, chapter_name_en, high_yield_score, estimated_exam_weight)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, CHAPTERS)
    conn.commit()
    conn.close()
    print(f"Master Books ({len(BOOKS)}) and Chapters ({len(CHAPTERS)}) registered successfully.")

if __name__ == '__main__':
    seed_master_books_and_chapters()
