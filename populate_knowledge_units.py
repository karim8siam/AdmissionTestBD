import sqlite3
from init_textbook_db import TEXTBOOK_DB_PATH

KNOWLEDGE_UNITS = [
    # ==========================================
    # BIOLOGY - BOTANY (ড. মোহাম্মদ আবুল হাসান)
    # ==========================================
    {
        "id": "KU-BOT-001",
        "book_id": "BOOK-BOTANY-HASAN",
        "chapter_id": "HASAN-CH-01",
        "subject": "Biology",
        "topic": "মাইটোকন্ড্রিয়া (Mitochondria)",
        "fact_type": "Definition",
        "exact_text_bn": "মাইটোকন্ড্রিয়া হলো কোষের শ্বসন ও শক্তি উৎপাদনের প্রধান অঙ্গাণু। একে কোষের 'পাওয়ার হাউস' (Power House) বলা হয়। এতে নিজস্ব বৃত্তাকার ডিএনএ (Circular DNA) এবং ৭০S রাইবোসোম থাকে। অন্তঃপর্দা ভেতরের দিকে ভাঁজ হয়ে যে প্রবর্ধক সৃষ্টি করে তাকে ক্রিস্টি (Cristae) বলে।",
        "context_en": "Mitochondria is known as the powerhouse of the cell. It possesses its own circular DNA and 70S ribosomes. Inner membrane folds are called cristae.",
        "keywords": "মাইটোকন্ড্রিয়া, mitochondria, power house, cristae, 70S ribosome, circular DNA",
        "citation": "ড. মোহাম্মদ আবুল হাসান, উদ্ভিদবিজ্ঞান ১ম পত্র, অধ্যায় ১: কোষ ও এর গঠন",
        "high_yield_priority": 5,
        "common_mcq_trap": "শিক্ষার্থীরা প্রায়ই ভুল করে মাইটোকন্ড্রিয়ায় 80S রাইবোসোম দাগায়, কিন্তু এতে প্রোক্যারিওটিক প্রকৃতির 70S রাইবোসোম থাকে।"
    },
    {
        "id": "KU-BOT-002",
        "book_id": "BOOK-BOTANY-HASAN",
        "chapter_id": "HASAN-CH-01",
        "subject": "Biology",
        "topic": "ক্লোরোপ্লাস্ট ও প্লাস্টিড (Chloroplast)",
        "fact_type": "Table_Chart",
        "exact_text_bn": "ক্লোরোপ্লাস্ট হলো উদ্ভিদের সাইটোপ্লাজমের বৃহত্তম অঙ্গাণু এবং একে 'কোষের রান্নাঘর' ও 'শর্করা জাতীয় খাদ্যের কারখানা' বলা হয়। ক্লোরোপ্লাস্টের থাইলাকয়েডের ভেতরে কোয়ান্টাসোম থাকে। গ্রানাগুলো পরস্পর স্ট্রমা ল্যামেলি দ্বারা যুক্ত থাকে। স্ট্রোমাতে কার্বন বিজারণের এনজাইম (যেমন রুবিস্কো - RuBisCO) বিদ্যমান।",
        "context_en": "Chloroplast is the largest cytoplasmic organelle in plants and the kitchen of the cell. Stroma contains carbon fixation enzymes like RuBisCO.",
        "keywords": "ক্লোরোপ্লাস্ট, chloroplast, plastid, কোয়ান্টাসোম, RuBisCO, কোষের রান্নাঘর",
        "citation": "ড. মোহাম্মদ আবুল হাসান, উদ্ভিদবিজ্ঞান ১ম পত্র, অধ্যায় ১",
        "high_yield_priority": 5,
        "common_mcq_trap": "সবুজ প্লাস্টিড হলো ক্লোরোপ্লাস্ট, রঙিন (অসবুজ) হলো ক্রোমোপ্লাস্ট, এবং বর্ণহীন খাদ্য সঞ্চয়ী হলো লিউকোপ্লাস্ট।"
    },
    {
        "id": "KU-BOT-003",
        "book_id": "BOOK-BOTANY-HASAN",
        "chapter_id": "HASAN-CH-02",
        "subject": "Biology",
        "topic": "মিয়োসিস ক্রসিং ওভার (Crossing Over in Meiosis-1)",
        "fact_type": "Process_Mechanism",
        "exact_text_bn": "মিয়োসিস-১ এর প্রফেজ-১ এর প্যাকাইটিন (Pachytene) উপপর্যায়ে হোমোলোগাস ক্রোমোজোমের দুটি নন-সিস্টার ক্রোমাটিডের মধ্যে অংশের বিনিময়কে ক্রসিং ওভার বলে। এতে এন্ডোনিউক্লিয়েজ এনজাইম দ্বারা ডিএনএ সূত্র কেটে যায় এবং লাইগেজ এনজাইম দ্বারা পুনঃজোড়া লাগে। সংযোগস্থলে X-আকৃতির কায়াজমা (Chiasma) গঠিত হয়।",
        "context_en": "Crossing over occurs in the Pachytene stage of Prophase-1 of Meiosis-1 between non-sister chromatids of homologous chromosomes.",
        "keywords": "ক্রসিং ওভার, crossing over, প্যাকাইটিন, pachytene, কায়াজমা, chiasma, এন্ডোনিউক্লিয়েজ, লাইগেজ",
        "citation": "ড. মোহাম্মদ আবুল হাসান, অধ্যায় ২: কোষ বিভাজন",
        "high_yield_priority": 5,
        "common_mcq_trap": "অপশনে জাইগোটিন (সিন্যাপসিস/বাইভ্যালেন্ট) এবং ডিপ্লোটিন (প্রান্তীয়করণ) দিয়ে বিভ্রান্ত করা হয়। ক্রসিং ওভার ঘটে কেবল প্যাকাইটিনে।"
    },
    {
        "id": "KU-BOT-004",
        "book_id": "BOOK-BOTANY-HASAN",
        "chapter_id": "HASAN-CH-04",
        "subject": "Biology",
        "topic": "ম্যালেরিয়া পরজীবী ও রোগ (Malarial Parasite)",
        "fact_type": "Table_Chart",
        "exact_text_bn": "মানুষে ম্যালেরিয়া সৃষ্টিকারী প্রধান ৪টি প্রজাতি: ১. Plasmodium vivax (বেনাইন টারশিয়ান ম্যালেরিয়া, সুপ্তাবস্থা ১২-২০ দিন), ২. Plasmodium falciparum (ম্যালিগন্যান্ট টারশিয়ান ম্যালেরিয়া - সবচেয়ে মারাত্মক, সুপ্তাবস্থা ৮-১৫ দিন), ৩. Plasmodium malariae (কোয়ার্টান ম্যালেরিয়া, সুপ্তাবস্থা ১৮-৪০ দিন), ৪. Plasmodium ovale (ওভাল টারশিয়ান ম্যালেরিয়া, সুপ্তাবস্থা ১১-১৬ দিন)।",
        "context_en": "Malarial parasite species and incubation periods: P. vivax (12-20 days), P. falciparum (8-15 days, most lethal malignant tertian), P. malariae (18-40 days), P. ovale (11-16 days).",
        "keywords": "ম্যালেরিয়া, Plasmodium falciparum, vivax, ম্যালিগন্যান্ট, সুপ্তাবস্থা, টারশিয়ান",
        "citation": "ড. মোহাম্মদ আবুল হাসান, অধ্যায় ৪: অণুজীব",
        "high_yield_priority": 5,
        "common_mcq_trap": "সবচেয়ে মারাত্মক ও সেরিব্রাল ম্যালেরিয়া সৃষ্টি করে Plasmodium falciparum।"
    },
    {
        "id": "KU-BOT-005",
        "book_id": "BOOK-BOTANY-HASAN",
        "chapter_id": "HASAN-CH-07",
        "subject": "Biology",
        "topic": "ম্যালভেসি গোত্রের বৈশিষ্ট্য (Malvaceae Family)",
        "fact_type": "Definition",
        "exact_text_bn": "ম্যালভেসি গোত্রের শনাক্তকারী বৈশিষ্ট্য: ১. উদ্ভিদের কচি অংশ রোমশ ও পিচ্ছিল (মিউসিলেজযুক্ত)। ২. উপপত্র মুক্ত পার্শ্বীয়। ৩. দলমণ্ডল টুইস্টেড (Twisted/পাকানো)। ৪. পুংকেশর বহু এবং একগুচ্ছক (Monadelphous)। ৫. পরাগধানী একপ্রকোষ্ঠী ও বৃক্কাকার (Kidney-shaped)। ৬. পরাগরেণু বৃহৎ ও কণ্টকিত। উদাহরণ: জবা (Hibiscus rosa-sinensis), ঢেঁড়শ, তুলা, কেনাফ।",
        "context_en": "Key diagnostic traits of Malvaceae: Mucilaginous sap, monadelphous stamens, reniform (kidney-shaped) 1-locular anthers, large spiny pollen grains.",
        "keywords": "ম্যালভেসি, Malvaceae, বৃক্কাকার পরাগধানী, একগুচ্ছক পুংকেশর, টুইস্টেড, জবা",
        "citation": "ড. মোহাম্মদ আবুল হাসান, অধ্যায় ৭: নগ্নবীজী ও আবৃতবীজী",
        "high_yield_priority": 5,
        "common_mcq_trap": "ধান/ঘাস হলো Poaceae গোত্র (লডিক্যুল, পালকের ন্যায় গর্ভমুণ্ড)। জবা হলো Malvaceae (বৃক্কাকার পরাগধানী)।"
    },
    {
        "id": "KU-BOT-006",
        "book_id": "BOOK-BOTANY-HASAN",
        "chapter_id": "HASAN-CH-08",
        "subject": "Biology",
        "topic": "ভাস্কুলার বান্ডলের প্রকারভেদ (Vascular Bundles)",
        "fact_type": "Table_Chart",
        "exact_text_bn": "ভাস্কুলার বান্ডলের প্রধান তিন ধরন: ১. সংযুক্ত (Conjoint): কান্ডে থাকে (সমপার্শ্বীয় ও সমদ্বিপার্শ্বীয়)। একবীজপত্রী কাণ্ডে ক্যাম্বিয়ামহীন 'সমপার্শ্বীয় বদ্ধ'; দ্বিবীজপত্রী কাণ্ডে ক্যাম্বিয়ামযুক্ত 'সমপার্শ্বীয় মুক্ত'; লাউ-কুমড়ায় 'সমদ্বিপার্শ্বীয়'। ২. অরীয় (Radial): উদ্ভিদের মূলে জাইলেম ও ফ্লোয়েম ভিন্ন ভিন্ন ব্যাসার্ধে থাকে। ৩. কেন্দ্রিক (Concentric): হ্যাড্রোসেন্ট্রিক (টেরিস/ফার্ন) ও লেপ্টোসেন্ট্রিক (ড্রাসিনা, ইউক্কা)।",
        "context_en": "Vascular bundle classification: Monocot stem = collateral closed; Dicot stem = collateral open; Cucurbita = bicollateral; Roots = radial; Pteris = hadrocentric.",
        "keywords": "ভাস্কুলার বান্ডল, সমপার্শ্বীয় বদ্ধ, সমপার্শ্বীয় মুক্ত, অরীয়, কেন্দ্রিক, ক্যাম্বিয়াম",
        "citation": "ড. মোহাম্মদ আবুল হাসান, অধ্যায় ৮: টিস্যু ও টিস্যুতন্ত্র",
        "high_yield_priority": 5,
        "common_mcq_trap": "মূলে সর্বদা অরীয় (Radial) বান্ডল থাকে; কাণ্ডে কখনো অরীয় বান্ডল থাকে না।"
    },
    {
        "id": "KU-BOT-007",
        "book_id": "BOOK-BOTANY-HASAN",
        "chapter_id": "HASAN-CH-09",
        "subject": "Biology",
        "topic": "C3 ও C4 উদ্ভিদের পার্থক্য (C3 vs C4 Plants)",
        "fact_type": "Table_Chart",
        "exact_text_bn": "C3 উদ্ভিদে CO2 গ্রহীতা RuBP (৫ কার্বন) এবং ১ম স্থায়ী পদার্থ ৩-ফসফোগ্লিসারিক এসিড (৩-পিজিএ, ৩ কার্বন)। C4 উদ্ভিদে CO2 গ্রহীতা ফসফোইনল পাইরুভিক এসিড (PEP, ৩ কার্বন) এবং ১ম স্থায়ী পদার্থ অক্সালো অ্যাসিটিক এসিড (OAA, ৪ কার্বন)। C4 উদ্ভিদের পাতায় বিশেষ বান্ডল সিথ কোষযুক্ত ক্র্যাঞ্জ অ্যানাটমি (Kranz anatomy) থাকে এবং এর সালোকসংশ্লেষণের দক্ষতা বেশি। উদাহরণ C4: ভুট্টা, আখ, চিনা, কাউন, সাইপেরাস।",
        "context_en": "C3: CO2 acceptor RuBP, 1st product 3-PGA. C4: CO2 acceptor PEP, 1st product OAA. C4 plants possess Kranz anatomy. Examples: Maize, Sugarcane.",
        "keywords": "C3 উদ্ভিদ, C4 উদ্ভিদ, RuBP, PEP, অক্সালো অ্যাসিটিক এসিড, ক্র্যাঞ্জ অ্যানাটমি, Kranz",
        "citation": "ড. মোহাম্মদ আবুল হাসান, অধ্যায় ৯: উদ্ভিদ শারীরতত্ত্ব",
        "high_yield_priority": 5,
        "common_mcq_trap": "C4 উদ্ভিদের ১ম স্থায়ী পদার্থ ৪ কার্বনবিশিষ্ট অক্সালো অ্যাসিটিক এসিড (OAA), ৩ কার্বনবিশিষ্ট পিজিএ নয়।"
    },

    # ==========================================
    # BIOLOGY - ZOOLOGY (গাজী আজমল ও গাজী আসমত)
    # ==========================================
    {
        "id": "KU-ZOO-001",
        "book_id": "BOOK-ZOOLOGY-AZMAL",
        "chapter_id": "AZMAL-CH-01",
        "subject": "Biology",
        "topic": "প্রধান প্রাণিপর্বের বৈশিষ্ট্য (Non-Chordata Phyla Diagnostic Traits)",
        "fact_type": "Table_Chart",
        "exact_text_bn": "১. পরিফেরা (Porifera): অস্টিয়া ছিদ্র, কোয়ানোসাইট কোষ, স্পিকিউল ও স্পঞ্জিন। ২. নিডারিয়া (Cnidaria): নিডোসাইট কোষে নেমাটোসিস্ট, সিলেন্টেরন বা গ্যাস্ট্রোভাস্কুলার গহ্বর। ৩. প্লাটিহেলমিনথিস (Platyhelminthes): শিখা কোষ (Flame cell) রেচন অঙ্গ, রক্ত ও সংবহনতন্ত্রহীন চ্যাপ্টাকৃমি। ৪. নেমাটোডা (Nematoda): সিউডোসিলোমেট, পৌষ্টিকনালি সোজা ও মুখ-পায়ুযুক্ত নলের ভেতর নল। ৫. অ্যানিলিডা (Annelida): মেটামেরিজম বা প্রকৃত খণ্ডকায়ন, নেফ্রিডিয়া রেচন অঙ্গ, সিটা বা প্যারাপোডিয়া চলন অঙ্গ। ৬. আর্থ্রোপোডা (Arthropoda): বৃহত্তম পর্ব, কাইটিনযুক্ত বহিঃকঙ্কাল, হিমোসিল, ট্রাকিয়া, ম্যালপিজিয়ান নালিকা। ৭. মলাস্কা (Mollusca): ম্যান্টল পর্দা, রেডুলা (Radula) রেতিজিহ্বা, খোলক। ৮. একাইনোডার্মাটা (Echinodermata): পূর্ণাঙ্গ প্রাণী পঞ্চ-অরীয় প্রতিসম, নালিকা পদ (Tube feet), পানি সংবহনতন্ত্র।",
        "context_en": "Diagnostic phylum traits: Porifera=choanocytes; Cnidaria=cnidocytes; Platyhelminthes=flame cells; Annelida=nephridia/setae; Arthropoda=Malpighian tubules; Mollusca=radula/mantle; Echinodermata=water vascular system/tube feet.",
        "keywords": "পর্বের বৈশিষ্ট্য, শিখা কোষ, নেফ্রিডিয়া, নিডোসাইট, ম্যালপিজিয়ান নালিকা, রেডুলা, সিলেন্ট্রন",
        "citation": "গাজী আজমল ও গাজী আসমত, অধ্যায় ১: প্রাণীর বিভিন্নতা ও শ্রেণিবিন্যাস",
        "high_yield_priority": 5,
        "common_mcq_trap": "শিখা কোষ হলো প্লাটিহেলমিনথিসের রেচন অঙ্গ, অ্যানিলিডার নয় (অ্যানিলিডার হলো নেফ্রিডিয়া)।"
    },
    {
        "id": "KU-ZOO-002",
        "book_id": "BOOK-ZOOLOGY-AZMAL",
        "chapter_id": "AZMAL-CH-04",
        "subject": "Biology",
        "topic": "রক্ত তঞ্চন ফ্যাক্টরসমূহ (Blood Clotting Factors)",
        "fact_type": "Table_Chart",
        "exact_text_bn": "রক্ত তঞ্চনে মোট ১৩টি ক্লটিং ফ্যাক্টর সক্রিয় ভূমিকা রাখে, যার মধ্যে প্রধান ৪টি মনে রাখার টেকনিক 'ফুল পড়ে টুপ করে': ১. ফ্যাক্টর I = ফাইব্রিনোজেন, ২. ফ্যাক্টর II = প্রোথ্রম্বিন, ৩. ফ্যাক্টর III = থ্রম্বোপ্লাস্টিন, ৪. ফ্যাক্টর IV = ক্যালসিয়াম আয়ন (Ca2+)। ফ্যাক্টর VIII = অ্যান্টিহিমোফিলিক ফ্যাক্টর (অভাবে হিমোফিলিয়া-এ হয়)। ফ্যাক্টর IX = ক্রিসমাস ফ্যাক্টর (অভাবে হিমোফিলিয়া-বি হয়)। ফ্যাক্টর XII = হেগম্যান ফ্যাক্টর।",
        "context_en": "Primary blood clotting factors: I=Fibrinogen, II=Prothrombin, III=Thromboplastin, IV=Calcium. Factor VIII deficiency causes Hemophilia A; Factor IX deficiency causes Christmas Disease (Hemophilia B).",
        "keywords": "রক্ত তঞ্চন ফ্যাক্টর, clotting factors, ক্রিসমাস ফ্যাক্টর, হিমোফিলিয়া, ফাইব্রিনোজেন, ক্যালসিয়াম আয়ন",
        "citation": "গাজী আজমল ও গাজী আসমত, অধ্যায় ৪: রক্ত ও সংবহন",
        "high_yield_priority": 5,
        "common_mcq_trap": "ফ্যাক্টর IV হলো ক্যালসিয়াম আয়ন (Ca2+)। পরীক্ষায় ধাতব আয়ন হিসেবে এটি সবচেয়ে বেশি আসে।"
    },
    {
        "id": "KU-ZOO-003",
        "book_id": "BOOK-ZOOLOGY-AZMAL",
        "chapter_id": "AZMAL-CH-04",
        "subject": "Biology",
        "topic": "হৃৎপিণ্ডের কপাটিকাসমূহ (Heart Valves)",
        "fact_type": "Table_Chart",
        "exact_text_bn": "১. ট্রাইকাসপিড কপাটিকা: ডান অলিন্দ ও ডান নিলয়ের মাঝে (৩টি পাল্লা বা কাস্প)। ২. বাইকাসপিড বা মাইট্রাল কপাটিকা: বাম অলিন্দ ও বাম নিলয়ের মাঝে (২টি পাল্লা)। ৩. অ্যাওর্টিক সেমিলুনার কপাটিকা: বাম নিলয় ও মহাধমনির সংযোগস্থলে (৩টি অর্ধচন্দ্রাকার কাস্প)। ৪. পালমোনারি সেমিলুনার কপাটিকা: ডান নিলয় ও পালমোনারি ধমনির সংযোগস্থলে (৩টি অর্ধচন্দ্রাকার কাস্প)। ৫. ইউস্টেচিয়ান কপাটিকা: নিম্ন মহাশিরা ও ডান অলিন্দের সংযোগে। ৬. থিবেসিয়ান কপাটিকা: করোনারি সাইনাস ও ডান অলিন্দের সংযোগে।",
        "context_en": "Heart valves: Bicuspid/Mitral has 2 cusps (left AV); Tricuspid has 3 cusps (right AV); Aortic and Pulmonary semilunar valves have 3 cusps each.",
        "keywords": "কপাটিকা, মাইট্রাল, ট্রাইকাসপিড, সেমিলুনার, থিবেসিয়ান, ইউস্টেচিয়ান, কাস্প",
        "citation": "গাজী আজমল, মানব শারীরতত্ত্ব: রক্ত ও সংবহন",
        "high_yield_priority": 5,
        "common_mcq_trap": "কেবল বাইকাসপিড (মাইট্রাল) কপাটিকায় ২টি কাস্প থাকে, অন্যসব প্রধান কপাটিকায় ৩টি কাস্প থাকে।"
    },
    {
        "id": "KU-ZOO-004",
        "book_id": "BOOK-ZOOLOGY-AZMAL",
        "chapter_id": "AZMAL-CH-10",
        "subject": "Biology",
        "topic": "অ্যান্টিবডির শ্রেণিবিভাগ (Antibody Classes: IgG, IgA, IgM, IgD, IgE)",
        "fact_type": "Table_Chart",
        "exact_text_bn": "অ্যান্টিবডির শ্রেণিবিভাগ ও বৈশিষ্ট্য: ১. IgG: রক্তরসের প্রধান অ্যান্টিবডি (৭৫-৮০%)। একমাত্র অ্যান্টিবডি যা অমরা বা প্লাসেন্টা ভেদ করে মায়ের দেহ থেকে ভ্রূণে প্রবেশ করে। ২. IgA: মায়ের শালদুধ (Colostrum), লালা ও অশ্রুতে থাকে (১০-১৫%)। ৩. IgM: মানবদেহের বৃহত্তম অ্যান্টিবডি (পেন্টামার), সংক্রমণের শুরুতে সর্বপ্রথম উৎপাদিত হয়। ৪. IgE: অ্যালার্জি ও কৃমির সংক্রমণে সাড়া দেয় এবং হিস্টামিন ক্ষরণ ঘটায়। ৫. IgD: B-লিম্ফোসাইটের সক্রিয়করণে ভূমিকা রাখে।",
        "context_en": "Antibodies: IgG crosses placenta (most abundant 80%); IgA secreted in breast milk/colostrum and tears; IgM largest pentamer, first responder; IgE triggers allergy/histamine release.",
        "keywords": "অ্যান্টিবডি, IgG, IgA, IgM, IgE, প্লাসেন্টা, শালদুধ, হিস্টামিন, ইমিউনোগ্লোবুলিন",
        "citation": "গাজী আজমল, অধ্যায় ১০: মানবদেহের প্রতিরক্ষা",
        "high_yield_priority": 5,
        "common_mcq_trap": "অমরা ভেদ করে কেবল IgG, আর শালদুধে সবচেয়ে বেশি থাকে IgA।"
    },

    # ==========================================
    # CHEMISTRY - 1ST & 2ND PAPER (হাজারী ও নাগ)
    # ==========================================
    {
        "id": "KU-CHEM-001",
        "book_id": "BOOK-CHEM-HAZARI-1",
        "chapter_id": "HAZARI1-CH-02",
        "subject": "Chemistry",
        "topic": "শিখা পরীক্ষায় ক্ষার ও মৃৎক্ষার ধাতুর বর্ণ (Flame Test Colors)",
        "fact_type": "Table_Chart",
        "exact_text_bn": "বুনসেন শিখা পরীক্ষায় বিভিন্ন ধাতব আয়নের বৈশিষ্ট্যপূর্ণ বর্ণ: ১. সোডিয়াম (Na+): উজ্জ্বল সোনালী হলুদ (Golden yellow)। ২. পটাসিয়াম (K+): হালকা বেগুনি বা নীলচে বেগুনি (কোবাল্ট কাঁচের মধ্য দিয়ে গোলাপী)। ৩. ক্যালসিয়াম (Ca2+): ইটের মতো লাল (Brick red)। ৪. বেরিয়াম (Ba2+): কাঁচা আপেলের মতো সবুজ (Apple green)। ৫. স্ট্রনশিয়াম (Sr2+): টকটকে লাল (Crimson red)। ৬. কপার (Cu2+): নীলাভ সবুজ। ব্যতিক্রম: বেরিলিয়াম (Be) ও ম্যাগনেসিয়াম (Mg) উচ্চ আয়নীকরণ শক্তির কারণে শিখা পরীক্ষায় কোনো বর্ণ দেখায় না।",
        "context_en": "Flame test colors: Na=Golden Yellow, K=Violet, Ca=Brick Red, Ba=Apple Green, Sr=Crimson Red. Be and Mg do not give flame color due to high ionization energy.",
        "keywords": "শিখা পরীক্ষা, flame test, বেরিয়াম, সোডিয়াম, ক্যালসিয়াম, আপেল সবুজ, সোনালী হলুদ",
        "citation": "হাজারী ও নাগ, রসায়ন ১ম পত্র, অধ্যায় ২: গুণগত রসায়ন",
        "high_yield_priority": 5,
        "common_mcq_trap": "কোন ধাতু শিখা পরীক্ষায় বর্ণ দেখায় না? সঠিক উত্তর: Be অথবা Mg।"
    },
    {
        "id": "KU-CHEM-002",
        "book_id": "BOOK-CHEM-HAZARI-1",
        "chapter_id": "HAZARI1-CH-03",
        "subject": "Chemistry",
        "topic": "সংকরায়ণ ও অণুর আকৃতি (Hybridization & Geometry)",
        "fact_type": "Table_Chart",
        "exact_text_bn": "সংকরায়ণ ও অণুর জ্যামিতিক গঠন: ১. sp: সরলরৈখিক, বন্ধন কোণ ১৮০° (BeCl2, C2H2)। ২. sp2: সমতলীয় ত্রিকোণাকার, বন্ধন কোণ ১২০° (BF3, C2H4)। ৩. sp3: চতুস্তলকীয়, মুক্তজোড়হীন হলে ১০৯.৫° (CH4)। ১টি মুক্তজোড় থাকলে ত্রিকোণীয় পিরামিড ১০৭° (NH3); ২টি মুক্তজোড় থাকলে কৌণিক বা V-আকৃতি ১০৪.৫° (H2O)। ৪. sp3d: ত্রিকোণীয় দ্বিপিরামিডীয় (PCl5)। ৫. sp3d2: অষ্টতলকীয়, কোণ ৯০° (SF6)। ৬. sp3d3: পঞ্চকোণীয় দ্বিপিরামিডীয় (IF7)।",
        "context_en": "Hybridization shapes: sp=linear (180°); sp2=trigonal planar (120°); sp3=tetrahedral (109.5°), pyramidal (NH3 107°), bent (H2O 104.5°); sp3d=trigonal bipyramidal (PCl5); sp3d2=octahedral (SF6).",
        "keywords": "সংকরায়ণ, hybridization, বন্ধন কোণ, চতুস্তলকীয়, অষ্টতলকীয়, PCl5, NH3, H2O",
        "citation": "হাজারী ও নাগ, রসায়ন ১ম পত্র, অধ্যায় ৩",
        "high_yield_priority": 5,
        "common_mcq_trap": "পানির সংকরায়ণ sp3 হওয়া সত্ত্বেও লোনপেয়ার-লোনপেয়ার বিকর্ষণের কারণে কোণ ১০৯.৫° না হয়ে ১০৪.৫° হয়।"
    },
    {
        "id": "KU-CHEM-003",
        "book_id": "BOOK-CHEM-HAZARI-2",
        "chapter_id": "HAZARI2-CH-02",
        "subject": "Chemistry",
        "topic": "লুকাস বিকারক দ্বারা অ্যালকোহল শনাক্তকরণ (Lucas Test for Alcohols)",
        "fact_type": "Reaction_Mechanism",
        "exact_text_bn": "অনার্দ্র জিংক ক্লোরাইড (ZnCl2) এবং গাঢ় হাইড্রোক্লোরিক এসিডের (HCl) দ্রবণকে 'লুকাস বিকারক' বলে। অ্যালকোহলের সাথে বিক্রিয়ায়: ১. টারশিয়ারী (৩°) অ্যালকোহল: কক্ষ তাপমাত্রায় তৎক্ষণাৎ (১ মিনিটের মধ্যে) অ্যালকাইল হ্যালাইডের তৈলাক্ত সাদা অধঃক্ষেপ ফেলে। ২. সেকেন্ডারি (২°) অ্যালকোহল: ৫-১০ মিনিট পর ধীরে ধীরে ঘোলাটে অধঃক্ষেপ সৃষ্টি করে। ৩. প্রাইমারি (১°) অ্যালকোহল: স্বাভাবিক তাপমাত্রায় কোনো অধঃক্ষেপ ফেলে না (উত্তপ্ত করলে দীর্ঘ সময় পর বিক্রিয়া করে)।",
        "context_en": "Lucas reagent is anhydrous ZnCl2 in conc. HCl. 3° alcohol reacts immediately with white turbidity; 2° alcohol reacts in 5-10 minutes; 1° alcohol does not react at room temperature.",
        "keywords": "লুকাস বিকারক, Lucas reagent, ৩ ডিগ্রি অ্যালকোহল, টারশিয়ারী অ্যালকোহল, ZnCl2, সাদা অধঃক্ষেপ",
        "citation": "হাজারী ও নাগ, রসায়ন ২য় পত্র, অধ্যায় ২: জৈব রসায়ন",
        "high_yield_priority": 5,
        "common_mcq_trap": "তৎক্ষণাৎ বিক্রিয়া দেয় ৩° অ্যালকোহল (যেমন ২-মিথাইল প্রোপানল-২)। ১° কখনোই সাথে সাথে বিক্রিয়া দেয় না।"
    },
    {
        "id": "KU-CHEM-004",
        "book_id": "BOOK-CHEM-HAZARI-2",
        "chapter_id": "HAZARI2-CH-03",
        "subject": "Chemistry",
        "topic": "প্রাইমারি ও সেকেন্ডারি স্ট্যান্ডার্ড পদার্থ (Primary vs Secondary Standards)",
        "fact_type": "Table_Chart",
        "exact_text_bn": "১. প্রাইমারি স্ট্যান্ডার্ড পদার্থ: বিশুদ্ধ অবস্থায় পাওয়া যায়, বায়ুর O2, CO2 বা আর্দ্রতা দ্বারা আক্রান্ত হয় না, দ্রবণের ঘনমাত্রা দীর্ঘদিন অপরিবর্তিত থাকে। মনে রাখার কৌশল: সংকেতে 'C' বর্ণ থাকে (ব্যতিক্রম HCl)। উদাহরণ: Na2CO3 (অনার্দ্র সোডিয়াম কার্বনেট), H2C2O4·2H2O (অক্সালিক এসিড), Na2C2O4 (সোডিয়াম অক্সালেট), K2Cr2O7 (পটাসিয়াম ডাইক্রোমেট)। ২. সেকেন্ডারি স্ট্যান্ডার্ড পদার্থ: বায়ুমণ্ডলের উপাদান দ্বারা পরিবর্তিত হয়, ঘনমাত্রা দ্রুত হ্রাস/বৃদ্ধি পায়। উদাহরণ: NaOH, KOH, HCl, H2SO4, KMnO4, Na2S2O3।",
        "context_en": "Primary standards: Na2CO3, Oxalic acid, K2Cr2O7, Na2C2O4. Secondary standards: NaOH, HCl, H2SO4, KMnO4, Na2S2O3.",
        "keywords": "প্রাইমারি স্ট্যান্ডার্ড, সেকেন্ডারি স্ট্যান্ডার্ড, Na2CO3, K2Cr2O7, NaOH, KMnO4",
        "citation": "হাজারী ও নাগ, রসায়ন ২য় পত্র, অধ্যায় ৩: পরিমাণগত রসায়ন",
        "high_yield_priority": 5,
        "common_mcq_trap": "HCl এ 'C' থাকা সত্ত্বেও এটি গ্যাসীয় ও উদ্বায়ী হওয়ায় প্রাইমারি নয়, সেকেন্ডারি স্ট্যান্ডার্ড পদার্থ।"
    },

    # ==========================================
    # PHYSICS - 1ST & 2ND PAPER (প্রফেসর ইসহাক স্যার)
    # ==========================================
    {
        "id": "KU-PHYS-001",
        "book_id": "BOOK-PHYS-ISHAQ-1",
        "chapter_id": "ISHAQ1-CH-06",
        "subject": "Physics",
        "topic": "মুক্তিবেগ ও মহাকর্ষীয় ধ্রুবক (Escape Velocity & G)",
        "fact_type": "Scientific_Value",
        "exact_text_bn": "১. পৃথিবীর পৃষ্ঠে মুক্তিবেগের সমীকরণ ve = √(2gR) = √(2GM/R)। পৃথিবীর ক্ষেত্রে মুক্তিবেগের মান ১১.২ কিমি/সেকেন্ড (11.2 km/s)। চাঁদের ক্ষেত্রে মুক্তিবেগ ২.৪ কিমি/সেকেন্ড। ২. মহাকর্ষীয় ধ্রুবক G = 6.673 × 10^-11 N m^2 kg^-2, মাত্রা [M^-1 L^3 T^-2]। ৩. অভিকর্ষজ ত্বরণ g এর মান মেরু অঞ্চলে সর্বাধিক (9.832 m/s^2), বিষুব অঞ্চলে সর্বনিম্ন (9.780 m/s^2) এবং আদর্শ মান ধরা হয় 9.80665 m/s^2 (45° অক্ষাংশে)।",
        "context_en": "Escape velocity formula ve = sqrt(2gR). Earth escape velocity = 11.2 km/s, Moon = 2.4 km/s. Gravitational constant G = 6.673 x 10^-11 N m^2 kg^-2.",
        "keywords": "মুক্তিবেগ, escape velocity, 11.2 km/s, মহাকর্ষীয় ধ্রুবক, G, অভিকর্ষজ ত্বরণ",
        "citation": "আমির হোসেন খান ও মোহাম্মদ ইসহাক, পদার্থবিজ্ঞান ১ম পত্র, অধ্যায় ৬: মহাকর্ষ ও অভিকর্ষ",
        "high_yield_priority": 5,
        "common_mcq_trap": "মুক্তিবেগের মান নিক্ষিপ্ত বস্তুর ভরের ওপর নির্ভর করে না; এটি কেবল গ্রহের ভর ও ব্যাসার্ধের ওপর নির্ভরশীল।"
    },
    {
        "id": "KU-PHYS-002",
        "book_id": "BOOK-PHYS-ISHAQ-2",
        "chapter_id": "ISHAQ2-CH-01",
        "subject": "Physics",
        "topic": "কার্নো ইঞ্জিন ও তাপগতিবিদ্যার সূত্র (Carnot Engine & Thermodynamics)",
        "fact_type": "Process_Mechanism",
        "exact_text_bn": "১. কার্নো চক্র একটি প্রত্যাবর্তী প্রক্রিয়া যাতে ৪টি ধাপ থাকে: সমোষ্ণ প্রসারণ, রুদ্ধতাপীয় প্রসারণ, সমোষ্ণ সংকোচন এবং রুদ্ধতাপীয় সংকোচন। ২. কার্নো ইঞ্জিনের কর্মদক্ষতা η = 1 - (T2/T1) = 1 - (Q2/Q1)। কর্মদক্ষতা ১০০% হতে হলে গ্রাহকের তাপমাত্রা T2 = 0 K (পরম শূন্য) হতে হবে যা বাস্তবে অসম্ভব। ৩. রুদ্ধতাপীয় পরিবর্তনে সিস্টেম ও পরিবেশের মাঝে তাপের আদান-প্রদান হয় না (dQ = 0), ফলে এন্ট্রপি স্থির থাকে (dS = 0)।",
        "context_en": "Carnot cycle consists of 4 steps (2 isothermal, 2 adiabatic). Efficiency eta = 1 - T2/T1. In adiabatic reversible process, entropy change dS = 0 (isentropic).",
        "keywords": "কার্নো ইঞ্জিন, কর্মদক্ষতা, এন্ট্রপি, রুদ্ধতাপীয়, সমোষ্ণ, পরম শূন্য তাপমাত্রা",
        "citation": "মোহাম্মদ ইসহাক, পদার্থবিজ্ঞান ২য় পত্র, অধ্যায় ১: তাপগতিবিদ্যা",
        "high_yield_priority": 5,
        "common_mcq_trap": "তাপমাত্রাকে সর্বদা কেলভিনে (Kelvin) রূপান্তর করতে হবে। সেলসিয়াসে হিসাব করলে সম্পূর্ণ ভুল উত্তর আসবে।"
    },
    {
        "id": "KU-PHYS-003",
        "book_id": "BOOK-PHYS-ISHAQ-2",
        "chapter_id": "ISHAQ2-CH-10",
        "subject": "Physics",
        "topic": "অর্ধপরিবাহী ও ডায়োড (Semiconductor & Diodes)",
        "fact_type": "Definition",
        "exact_text_bn": "১. বিশুদ্ধ বা সহজাত অর্ধপরিবাহী (সিলিকন, জার্মেনিয়াম) এর সাথে ত্রিযোজী মৌল (যেমন বোরন, অ্যালুমিনিয়াম, গ্যালিয়াম, ইন্ডিয়াম) ডোপিং করলে p-টাইপ অর্ধপরিবাহী তৈরি হয় (সংখ্যাগরিষ্ঠ চার্জ বাহক হোল)। ২. পঞ্চযোজী মৌল (ফসফরাস, আর্সেনিক, অ্যান্টিমণি) ডোপিং করলে n-টাইপ অর্ধপরিবাহী গঠিত হয় (সংখ্যাগরিষ্ঠ চার্জ বাহক ইলেকট্রন)। ৩. p-n জংশনে সম্মুখী বায়াস (Forward bias) দিলে ডিপ্লেশন স্তর হ্রাস পায় ও তড়িৎ প্রবাহিত হয়। বিমুখী বায়াসে (Reverse bias) ডিপ্লেশন স্তর বৃদ্ধি পায়।",
        "context_en": "Trivalent impurity doping forms p-type (majority carrier hole); Pentavalent impurity doping forms n-type (majority carrier electron). Forward bias narrows depletion layer.",
        "keywords": "সেমিকন্ডাক্টর, p-টাইপ, n-টাইপ, ডোপিং, ত্রিযোজী, পঞ্চযোজী, ডিপ্লেশন স্তর, ফরওয়ার্ড বায়াস",
        "citation": "মোহাম্মদ ইসহাক, পদার্থবিজ্ঞান ২য় পত্র, অধ্যায় ১০: সেমিকন্ডাক্টর ও ইলেকট্রনিক্স",
        "high_yield_priority": 5,
        "common_mcq_trap": "p-টাইপ বা n-টাইপ সেমিকন্ডাক্টর সামগ্রিকভাবে তড়িৎ নিরপেক্ষ (Neutral), চার্জিত নয়।"
    },

    # ==========================================
    # ENGLISH & GENERAL KNOWLEDGE COMPENDIUM
    # ==========================================
    {
        "id": "KU-ENG-001",
        "book_id": "BOOK-ENG-MEDICAL",
        "chapter_id": "ENG-MOD-01",
        "subject": "English",
        "topic": "মেডিকেলে সর্বাধিক আসা Appropriate Prepositions",
        "fact_type": "Table_Chart",
        "exact_text_bn": "মেডিকেল ভর্তি পরীক্ষায় বিগত ১৫ বছরে সবচেয়ে বেশি আসা প্রিপজিশন তালিকা: ১. Abstain from / Refrain from (বিরত থাকা)। ২. Abide by (মেনে চলা)। ৩. Adjacent to (সংলগ্ন)। ৪. Blind of (চোখে অন্ধ), Blind to (দোষে অন্ধ)। ৫. Congratulate on (অভিনন্দন জানানো)। ৬. Die of (রোগে মরা), Die from (অতিরিক্ত কোনো কারণে মরা), Die for (দেশের জন্য আত্মত্যাগ), Die by (বিষপানে/আত্মহত্যা)। ৭. Preferable to / Senior to / Junior to (তুলনায় to বসে, than নয়)। ৮. Look down upon (ঘৃণা করা)।",
        "context_en": "High frequency medical prepositions: Abstain from, Abide by, Blind of/to, Die of (disease)/from/for/by, Preferable to, Look down upon.",
        "keywords": "preposition, abstain from, die of, blind to, preferable to, abide by",
        "citation": "মেডিকেল ইংলিশ ব্যাকরণ সংকলন, মডিউল ১",
        "high_yield_priority": 5,
        "common_mcq_trap": "He died ___ cholera. রোগে মারা গেলে 'of' বসে (Die of), 'from' নয়।"
    },
    {
        "id": "KU-GK-001",
        "book_id": "BOOK-GK-MEDICAL",
        "chapter_id": "GK-MOD-02",
        "subject": "General Knowledge",
        "topic": "১৯৭১ মুক্তিযুদ্ধ: সেক্টর ও বীরশ্রেষ্ঠ সারসংক্ষেপ",
        "fact_type": "Table_Chart",
        "exact_text_bn": "১. মুক্তিযুদ্ধের ১১টি সেক্টর: সেক্টর ১০ ছিল নৌ-সেক্টর (সমগ্র জলপথ ও উপকূলীয় এলাকা, কোনো নিয়মিত কমান্ডার ছিল না)। ২. ৭ জন বীরশ্রেষ্ঠের তালিকা ও বাহিনী: ক. সিপাহী মোস্তফা কামাল (সেনাবাহিনী), খ. ল্যান্স নায়েক মুন্সী আব্দুর রউফ (বিডিআর/ইপিআর), গ. ফ্লাইট লেফটেন্যান্ট মতিউর রহমান (বিমানবাহিনী), ঘ. ল্যান্স নায়েক নূর মোহাম্মদ শেখ (বিডিআর/ইপিআর), ঙ. সিপাহী হামিদুর রহমান (সেনাবাহিনী), চ. ইঞ্জিনরুম আর্টিফিসার মোহাম্মদ রুহুল আমিন (নৌবাহিনী), ছ. ক্যাপ্টেন মহিউদ্দীন জাহাঙ্গীর (সেনাবাহিনী)। ৩. সর্বোচ্চ খেতাব বীরশ্রেষ্ঠ (৭ জন), দ্বিতীয় সর্বোচ্চ বীর উত্তম (৬৮ জন)।",
        "context_en": "Liberation War 1971: 11 sectors; Sector 10 was naval commando (no regular commander). 7 Bir Sreshtho (names and forces).",
        "keywords": "মুক্তিযুদ্ধ, ১৯৭১, বীরশ্রেষ্ঠ, ৭ জন, সেক্টর ১০, নৌ-কমান্ডো, মতিউর রহমান, রুহুল আমিন",
        "citation": "মেডিকেল মুক্তিযুদ্ধ ও ইতিহাস বিশ্বকোষ, মডিউল ২",
        "high_yield_priority": 5,
        "common_mcq_trap": "কোন সেক্টরে নিয়মিত কোনো কমান্ডার ছিল না? সঠিক উত্তর: ১০ নম্বর সেক্টর।"
    },
    {
        "id": "KU-GK-002",
        "book_id": "BOOK-GK-MEDICAL",
        "chapter_id": "GK-MOD-06",
        "subject": "General Knowledge",
        "topic": "বিশ্ব স্বাস্থ্য সংস্থা (WHO) ও স্বাস্থ্য মাইলফলক",
        "fact_type": "Definition",
        "exact_text_bn": "১. বিশ্ব স্বাস্থ্য সংস্থা (World Health Organization - WHO): প্রতিষ্ঠিত হয় ৭ এপ্রিল ১৯৪৮ সালে। সদর দপ্তর সুইজারল্যান্ডের জেনেভায়। প্রতি বছর ৭ এপ্রিল 'বিশ্ব স্বাস্থ্য দিবস' পালিত হয়। ২. বাংলাদেশে সম্প্রসারিত টিকাদান কর্মসূচি (EPI) চালু হয় ৭ এপ্রিল ১৯৭৯ সালে। শিশুদের মারাত্মক ১০টি সংক্রামক রোগের বিরুদ্ধে বিনামূল্যে টিকা প্রদান করা হয়। ৩. UNICEF এর সদর দপ্তর নিউইয়র্ক, যুক্তরাষ্ট্র। ৪. রেড ক্রিসেন্ট/রেড ক্রস এর সদর দপ্তর জেনেভা, সুইজারল্যান্ড।",
        "context_en": "WHO established April 7, 1948 in Geneva, Switzerland. April 7 is World Health Day. EPI launched in Bangladesh on April 7, 1979.",
        "keywords": "WHO, বিশ্ব স্বাস্থ্য সংস্থা, জেনেভা, ৭ এপ্রিল, EPI টিকাদান, স্বাস্থ্য দিবস",
        "citation": "মেডিকেল স্বাস্থ্য ইতিহাস ও আন্তর্জাতিক সংস্থা, মডিউল ৬",
        "high_yield_priority": 5,
        "common_mcq_trap": "WHO এর সদর দপ্তর জেনেভা (সুইজারল্যান্ড), নিউইয়র্ক নয় (নিউইয়র্কে হলো জাতিসংঘ ও ইউনিসেফ)।"
    }
]

def seed_knowledge_units():
    conn = sqlite3.connect(TEXTBOOK_DB_PATH)
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT OR REPLACE INTO knowledge_units
        (id, book_id, chapter_id, subject, topic, fact_type, exact_text_bn, context_en, keywords, citation, high_yield_priority, common_mcq_trap)
        VALUES (:id, :book_id, :chapter_id, :subject, :topic, :fact_type, :exact_text_bn, :context_en, :keywords, :citation, :high_yield_priority, :common_mcq_trap)
    """, KNOWLEDGE_UNITS)
    conn.commit()
    conn.close()
    print(f"Seeded {len(KNOWLEDGE_UNITS)} high-precision textbook knowledge units with full-text search indexing.")

if __name__ == '__main__':
    seed_knowledge_units()
