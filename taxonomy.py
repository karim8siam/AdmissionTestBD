import sqlite3
from init_db import DB_PATH

TOPICS_DATA = [
    # Biology - Botany (উদ্ভিদবিজ্ঞান)
    ("Biology", "Botany", 1, "কোষ ও এর গঠন (Cell and its structure)", "Cell and its structure", 1),
    ("Biology", "Botany", 2, "কোষ বিভাজন (Cell Division)", "Cell Division", 1),
    ("Biology", "Botany", 3, "কোষ রসায়ন (Cell Chemistry)", "Cell Chemistry", 2),
    ("Biology", "Botany", 4, "অণুজীব (Microorganisms)", "Microorganisms", 1),
    ("Biology", "Botany", 5, "শৈবাল ও ছত্রাক (Algae and Fungi)", "Algae and Fungi", 2),
    ("Biology", "Botany", 6, "ব্রায়োফাইটা ও টেরিডোফাইটা (Bryophyta & Pteridophyta)", "Bryophyta & Pteridophyta", 3),
    ("Biology", "Botany", 7, "নগ্নবীজী ও আবৃতবীজী উদ্ভিদ (Gymnosperms & Angiosperms)", "Gymnosperms & Angiosperms", 1),
    ("Biology", "Botany", 8, "টিস্যু ও টিস্যুতন্ত্র (Tissue & Tissue System)", "Tissue & Tissue System", 1),
    ("Biology", "Botany", 9, "উদ্ভিদ শারীরতত্ত্ব (Plant Physiology)", "Plant Physiology", 1),
    ("Biology", "Botany", 10, "উদ্ভিদ প্রজনন (Plant Reproduction)", "Plant Reproduction", 2),
    ("Biology", "Botany", 11, "জীবপ্রযুক্তি (Biotechnology)", "Biotechnology", 1),
    ("Biology", "Botany", 12, "জীবের পরিবেশ, বিস্তার ও সংরক্ষণ (Ecology & Conservation)", "Ecology & Conservation", 2),

    # Biology - Zoology (প্রাণিবিজ্ঞান)
    ("Biology", "Zoology", 1, "প্রাণীর বিভিন্নতা ও শ্রেণিবিন্যাস (Animal Diversity & Classification)", "Animal Diversity & Classification", 1),
    ("Biology", "Zoology", 2, "প্রাণীর পরিচিতি (Introduction to Animals - Hydra, Grasshopper, Rohu)", "Introduction to Animals", 1),
    ("Biology", "Zoology", 3, "মানব শারীরতত্ত্ব: পরিপাক ও শোষণ (Digestion & Absorption)", "Digestion & Absorption", 1),
    ("Biology", "Zoology", 4, "মানব শারীরতত্ত্ব: রক্ত ও সংবহন (Blood & Circulation)", "Blood & Circulation", 1),
    ("Biology", "Zoology", 5, "মানব শারীরতত্ত্ব: শ্বাসক্রিয়া ও শ্বসন (Respiration & Breathing)", "Respiration & Breathing", 1),
    ("Biology", "Zoology", 6, "মানব শারীরতত্ত্ব: বর্জ্য ও নিষ্কাশন (Excretion)", "Excretion", 1),
    ("Biology", "Zoology", 7, "মানব শারীরতত্ত্ব: চলন ও অঙ্গচালনা (Locomotion & Movement)", "Locomotion & Movement", 2),
    ("Biology", "Zoology", 8, "মানব শারীরতত্ত্ব: সমন্বয় ও নিয়ন্ত্রণ (Coordination & Control)", "Coordination & Control", 1),
    ("Biology", "Zoology", 9, "মানব জীবনের ধারাবাহিকতা (Human Reproduction)", "Human Reproduction", 2),
    ("Biology", "Zoology", 10, "মানবদেহের প্রতিরক্ষা (Human Immunity)", "Human Immunity", 1),
    ("Biology", "Zoology", 11, "জিনতত্ত্ব ও বিবর্তন (Genetics & Evolution)", "Genetics & Evolution", 1),
    ("Biology", "Zoology", 12, "প্রাণীর আচরণ (Animal Behavior)", "Animal Behavior", 3),

    # Chemistry - 1st Paper (রসায়ন ১ম পত্র)
    ("Chemistry", "1st Paper", 1, "ল্যাবরেটরির নিরাপদ ব্যবহার (Safe Use of Laboratory)", "Safe Use of Laboratory", 3),
    ("Chemistry", "1st Paper", 2, "গুণগত রসায়ন (Qualitative Chemistry)", "Qualitative Chemistry", 1),
    ("Chemistry", "1st Paper", 3, "পর্যায়বৃত্ত ধর্ম ও রাসায়নিক বন্ধন (Periodic Properties & Bonding)", "Periodic Properties & Bonding", 1),
    ("Chemistry", "1st Paper", 4, "রাসায়নিক পরিবর্তন (Chemical Changes)", "Chemical Changes", 1),
    ("Chemistry", "1st Paper", 5, "কর্মমুখী রসায়ন (Working Chemistry)", "Working Chemistry", 2),

    # Chemistry - 2nd Paper (রসায়ন ২য় পত্র)
    ("Chemistry", "2nd Paper", 1, "পরিবেশ রসায়ন (Environmental Chemistry)", "Environmental Chemistry", 1),
    ("Chemistry", "2nd Paper", 2, "জৈব রসায়ন (Organic Chemistry)", "Organic Chemistry", 1),
    ("Chemistry", "2nd Paper", 3, "পরিমাণগত রসায়ন (Quantitative Chemistry)", "Quantitative Chemistry", 1),
    ("Chemistry", "2nd Paper", 4, "তড়িৎ রসায়ন (Electrochemistry)", "Electrochemistry", 1),
    ("Chemistry", "2nd Paper", 5, "অর্থনৈতিক রসায়ন (Economic Chemistry)", "Economic Chemistry", 2),

    # Physics - 1st Paper (পদার্থবিজ্ঞান ১ম পত্র)
    ("Physics", "1st Paper", 1, "ভৌতজগৎ ও পরিমাপ (Physical World & Measurement)", "Physical World & Measurement", 3),
    ("Physics", "1st Paper", 2, "ভেক্টর (Vectors)", "Vectors", 1),
    ("Physics", "1st Paper", 3, "গতিবিদ্যা (Dynamics)", "Dynamics", 2),
    ("Physics", "1st Paper", 4, "নিউটনিয়ান বলবিদ্যা (Newtonian Mechanics)", "Newtonian Mechanics", 1),
    ("Physics", "1st Paper", 5, "কাজ, শক্তি ও ক্ষমতা (Work, Energy & Power)", "Work, Energy & Power", 1),
    ("Physics", "1st Paper", 6, "মহাকর্ষ ও অভিকর্ষ (Gravitation & Gravity)", "Gravitation & Gravity", 1),
    ("Physics", "1st Paper", 7, "পদার্থের গাঠনিক ধর্ম (Structural Properties of Matter)", "Structural Properties of Matter", 1),
    ("Physics", "1st Paper", 8, "পর্যায়বৃত্ত গতি (Periodic Motion)", "Periodic Motion", 2),
    ("Physics", "1st Paper", 9, "তরঙ্গ (Waves)", "Waves", 2),
    ("Physics", "1st Paper", 10, "আদর্শ গ্যাস ও গতিতত্ত্ব (Ideal Gas & Kinetic Theory)", "Ideal Gas & Kinetic Theory", 1),

    # Physics - 2nd Paper (পদার্থবিজ্ঞান ২য় পত্র)
    ("Physics", "2nd Paper", 1, "তাপগতিবিদ্যা (Thermodynamics)", "Thermodynamics", 1),
    ("Physics", "2nd Paper", 2, "স্থির তড়িৎ (Static Electricity)", "Static Electricity", 2),
    ("Physics", "2nd Paper", 3, "চল তড়িৎ (Current Electricity)", "Current Electricity", 1),
    ("Physics", "2nd Paper", 4, "তড়িৎ প্রবাহের চৌম্বক ক্রিয়া ও চুম্বকত্ব (Magnetic Effects & Magnetism)", "Magnetic Effects & Magnetism", 2),
    ("Physics", "2nd Paper", 5, "তাড়িৎচৌম্বকীয় আবেশ ও পরিবর্তী প্রবাহ (Electromagnetic Induction & AC)", "Electromagnetic Induction & AC", 2),
    ("Physics", "2nd Paper", 6, "জ্যামিতিক আলোকবিজ্ঞান (Geometric Optics)", "Geometric Optics", 1),
    ("Physics", "2nd Paper", 7, "ভৌত আলোকবিজ্ঞান (Physical Optics)", "Physical Optics", 2),
    ("Physics", "2nd Paper", 8, "আধুনিক পদার্থবিজ্ঞানের সূচনা (Modern Physics)", "Modern Physics", 1),
    ("Physics", "2nd Paper", 9, "পরমাণু মডেল ও নিউক্লিয়ার পদার্থবিজ্ঞান (Atomic Model & Nuclear Physics)", "Atomic Model & Nuclear Physics", 1),
    ("Physics", "2nd Paper", 10, "সেমিকন্ডাক্টর ও ইলেকট্রনিক্স (Semiconductors & Electronics)", "Semiconductors & Electronics", 1),

    # English
    ("English", "Grammar", 1, "Parts of Speech & Identification", "Parts of Speech", 1),
    ("English", "Grammar", 2, "Right Form of Verbs & Conditionals", "Right Form of Verbs", 1),
    ("English", "Grammar", 3, "Subject-Verb Agreement", "Subject-Verb Agreement", 1),
    ("English", "Grammar", 4, "Prepositions & Phrasal Verbs", "Prepositions", 1),
    ("English", "Grammar", 5, "Voice & Narration", "Voice & Narration", 1),
    ("English", "Vocabulary", 6, "Synonyms & Antonyms", "Synonyms & Antonyms", 1),
    ("English", "Vocabulary", 7, "Spelling & Pinpoint Errors", "Spelling", 2),
    ("English", "Vocabulary", 8, "Idioms & Phrases", "Idioms & Phrases", 2),

    # General Knowledge
    ("General Knowledge", "Bangladesh Affairs", 1, "ইতিহাস ও ভাষা আন্দোলন (History & Language Movement 1952)", "History & 1952", 1),
    ("General Knowledge", "Bangladesh Affairs", 2, "মুক্তিযুদ্ধ ও স্বাধীনতা (Liberation War 1971 & Bir Sreshtho)", "Liberation War 1971", 1),
    ("General Knowledge", "Bangladesh Affairs", 3, "বঙ্গবন্ধু শেখ মুজিবুর রহমান (Bangabandhu Life & Works)", "Bangabandhu", 1),
    ("General Knowledge", "Bangladesh Affairs", 4, "সংবিধান, ভৌগোলিক সীমানা ও জাতীয় অর্জন (Constitution, Geography & Mega Projects)", "National Affairs", 1),
    ("General Knowledge", "Bangladesh Affairs", 5, "বাংলাদেশের স্বাস্থ্য খাত (Healthcare Milestones in Bangladesh)", "Health Sector", 1),
    ("General Knowledge", "International Affairs", 6, "আন্তর্জাতিক সংস্থা ও জাতিসংঘ (UN & Global Organizations - WHO, UNICEF)", "International Organizations", 1),
    ("General Knowledge", "International Affairs", 7, "নোবেল পুরস্কার ও সাম্প্রতিক বিশ্ব (Nobel Prize & Global Affairs)", "Nobel & Global Affairs", 1)
]

def seed_taxonomy():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO topics (subject, paper, chapter_num, chapter_name_bn, chapter_name_en, high_yield_rank)
        VALUES (?, ?, ?, ?, ?, ?)
    """, TOPICS_DATA)
    conn.commit()
    conn.close()
    print(f"Taxonomy populated with {len(TOPICS_DATA)} chapters and high-yield topics.")

if __name__ == '__main__':
    seed_taxonomy()
