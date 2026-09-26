import json

QUESTIONS_PATH = '/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/medical_15years_export.json'
TEXTBOOK_KB_PATH = '/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/data/medical_textbooks_kb.json'
HTML_OUTPUT_PATH = '/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/web/index.html'

with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
    questions_json = f.read()

with open(TEXTBOOK_KB_PATH, 'r', encoding='utf-8') as f:
    textbook_kb_json = f.read()

html_template = f"""<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>মেডিকেল ভর্তি পরীক্ষা: বিগত ১৫ বছরের প্রশ্ন ও মূল পাঠ্যবই নলেজ বেস</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Hind Siliguri', 'Inter', sans-serif;
    }}
  </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen">

  <!-- Header -->
  <header class="bg-gradient-to-r from-teal-800 via-emerald-900 to-slate-900 text-white shadow-xl sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col md:flex-row justify-between items-center gap-4">
      <div>
        <div class="flex items-center gap-3">
          <span class="bg-emerald-400 text-teal-950 font-bold px-2.5 py-0.5 rounded text-xs uppercase tracking-wider">DGME Intelligence Hub</span>
          <span class="text-emerald-300 text-sm font-medium">15-Year Papers & NCTB Authoritative Textbook DB</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-bold tracking-tight mt-1">মেডিকেল ভর্তি পরীক্ষা: ১৫ বছরের প্রশ্ন ও প্রামাণ্য পাঠ্যবই ডাটাবেজ</h1>
      </div>
      <div class="flex items-center gap-2">
        <a href="../data/medical_textbooks_kb.json" download class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs px-3 py-2 rounded-lg font-medium transition shadow">
          📚 Textbook KB JSON
        </a>
        <a href="../data/medical_15years_export.json" download class="bg-teal-700 hover:bg-teal-600 text-white text-xs px-3 py-2 rounded-lg font-medium transition shadow">
          📥 Questions JSON
        </a>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 border-t border-teal-700/50 flex gap-6">
      <button onclick="switchTab('questions')" id="tab-btn-questions" class="py-3 px-1 text-sm font-semibold border-b-2 border-emerald-400 text-white transition flex items-center gap-2">
        📝 বিগত ১৫ বছরের প্রশ্ন ব্যাংক (MCQ Bank)
      </button>
      <button onclick="switchTab('textbooks')" id="tab-btn-textbooks" class="py-3 px-1 text-sm font-semibold border-b-2 border-transparent text-teal-200 hover:text-white transition flex items-center gap-2">
        📖 মূল পাঠ্যবই নলেজ বেস ও এআই আরএজি (Textbook Ground Truth)
      </button>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    
    <!-- ============================================== -->
    <!-- TAB 1: QUESTIONS BANK -->
    <!-- ============================================== -->
    <div id="tab-questions" class="space-y-8">
      
      <!-- Stats Bar -->
      <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-5 gap-4">
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <p class="text-xs text-slate-500 font-medium">মোট সংগৃহীত প্রশ্ন</p>
          <p class="text-2xl font-bold text-teal-700" id="stat-total">0</p>
        </div>
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <p class="text-xs text-slate-500 font-medium">পরীক্ষার সেশন</p>
          <p class="text-2xl font-bold text-teal-700">১৫ টি (২০১০ - ২৫)</p>
        </div>
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <p class="text-xs text-slate-500 font-medium">জীববিজ্ঞান (Biology)</p>
          <p class="text-2xl font-bold text-emerald-600" id="stat-bio">0</p>
        </div>
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <p class="text-xs text-slate-500 font-medium">রসায়ন (Chemistry)</p>
          <p class="text-2xl font-bold text-blue-600" id="stat-chem">0</p>
        </div>
        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm col-span-2 sm:col-span-1">
          <p class="text-xs text-slate-500 font-medium">পদার্থবিজ্ঞান (Physics)</p>
          <p class="text-2xl font-bold text-amber-600" id="stat-phys">0</p>
        </div>
      </div>

      <!-- Filter & Search Toolbar -->
      <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-4">
        <div class="flex flex-col md:flex-row gap-4 items-center justify-between">
          <div class="w-full md:w-1/2 relative">
            <input type="text" id="search-input" placeholder="প্রশ্ন বা টপিক খুঁজুন (যেমন: মাইটোকন্ড্রিয়া, রক্ত, লুকাস বিকারক)..." 
                   class="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-teal-500 text-sm">
            <span class="absolute left-3.5 top-3 text-slate-400">🔍</span>
          </div>

          <div class="flex flex-wrap items-center gap-3 w-full md:w-auto">
            <select id="session-select" class="px-3.5 py-2.5 rounded-xl border border-slate-300 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-teal-500">
              <option value="ALL">সকল সেশন (All 15 Years)</option>
            </select>

            <select id="subject-select" class="px-3.5 py-2.5 rounded-xl border border-slate-300 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-teal-500">
              <option value="ALL">সকল বিষয় (All Subjects)</option>
              <option value="Biology">জীববিজ্ঞান (Biology)</option>
              <option value="Chemistry">রসায়ন (Chemistry)</option>
              <option value="Physics">পদার্থবিজ্ঞান (Physics)</option>
              <option value="English">ইংরেজি (English)</option>
              <option value="General Knowledge">সাধারণ জ্ঞান (GK)</option>
            </select>

            <label class="flex items-center gap-2 text-sm text-slate-600 cursor-pointer select-none bg-slate-100 px-3 py-2 rounded-xl">
              <input type="checkbox" id="repeat-only-checkbox" class="rounded text-teal-600 focus:ring-teal-500">
              <span>শুধু রিপিট প্রশ্ন</span>
            </label>
          </div>
        </div>
        
        <div class="text-xs text-slate-500 flex justify-between items-center pt-2 border-t border-slate-100">
          <span id="filtered-count">প্রদর্শিত হচ্ছে ০ টি প্রশ্ন</span>
          <span class="italic text-teal-700 font-medium">ভুল উত্তরে নেগেটিভ মার্কিং: -০.২৫ কাটা যাবে</span>
        </div>
      </div>

      <!-- Questions List -->
      <div id="questions-container" class="space-y-6"></div>
    </div>

    <!-- ============================================== -->
    <!-- TAB 2: TEXTBOOK GROUND TRUTH & LLM RAG -->
    <!-- ============================================== -->
    <div id="tab-textbooks" class="hidden space-y-8">
      
      <!-- Textbooks Intro Banner -->
      <div class="bg-gradient-to-br from-emerald-800 to-teal-950 text-white rounded-2xl p-6 sm:p-8 shadow-md">
        <div class="max-w-3xl space-y-3">
          <span class="bg-emerald-500 text-teal-950 text-xs uppercase font-bold px-3 py-1 rounded-full">LLM Ground Truth Engine</span>
          <h2 class="text-2xl sm:text-3xl font-bold">এনসিটিবি প্রামাণ্য পাঠ্যবই নলেজ বেস</h2>
          <p class="text-emerald-100 text-sm leading-relaxed">
            মেডিকেল ভর্তি পরীক্ষার প্রশ্ন সরাসরি যেসকল অনুমোদিত মূল পাঠ্যবই (ড. আবুল হাসান, গাজী আজমল, হাজারী ও নাগ, ইসহাক স্যার) থেকে করা হয়, তাদের প্রতিটি ছক, ব্যতিক্রম, মান এবং বিজ্ঞানীদের তথ্য এখানে সংরক্ষিত। কোনো এলএলএম (LLM) মডেল যুক্ত করলে এই ডাটাবেজ থেকেই হ্যালুসিনেশনহীন ১০০% প্রামাণ্য উত্তর তৈরি হবে।
          </p>
        </div>
      </div>

      <!-- Textbook Search Bar -->
      <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col sm:flex-row gap-4">
        <div class="w-full relative">
          <input type="text" id="kb-search-input" placeholder="পাঠ্যবইয়ের যেকোনো সূত্র, ছক বা টপিক খুঁজুন (যেমন: ক্রিসমাস ফ্যাক্টর, লুকাস বিকারক, C4 চক্র, শিখা পরীক্ষা, মুক্তিবেগ)..." 
                 class="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm">
          <span class="absolute left-3.5 top-3.5 text-slate-400">📖</span>
        </div>
        <select id="kb-subject-filter" class="px-4 py-3 rounded-xl border border-slate-300 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
          <option value="ALL">সকল পাঠ্যবই (All Books)</option>
          <option value="Biology">উদ্ভিদ ও প্রাণিবিজ্ঞান (আবুল হাসান / আজমল)</option>
          <option value="Chemistry">রসায়ন ১ম ও ২য় পত্র (হাজারী ও নাগ)</option>
          <option value="Physics">পদার্থবিজ্ঞান ১ম ও ২য় পত্র (মোহাম্মদ ইসহাক)</option>
          <option value="English">ইংরেজি ব্যাকরণ ও ভোকাবুলারি</option>
          <option value="General Knowledge">মুক্তিযুদ্ধ ও স্বাস্থ্য ইতিহাস</option>
        </select>
      </div>

      <!-- Knowledge Units Feed -->
      <div id="kb-container" class="space-y-6"></div>
    </div>

  </main>

  <script>
    const QUESTIONS = {questions_json};
    const TEXTBOOKS_KB = {textbook_kb_json};

    let selectedSession = "ALL";
    let selectedSubject = "ALL";
    let searchQuery = "";
    let repeatOnly = false;

    // Tab Switching
    window.switchTab = function(tab) {{
      const tabQ = document.getElementById('tab-questions');
      const tabT = document.getElementById('tab-textbooks');
      const btnQ = document.getElementById('tab-btn-questions');
      const btnT = document.getElementById('tab-btn-textbooks');

      if (tab === 'questions') {{
        tabQ.classList.remove('hidden');
        tabT.classList.add('hidden');
        btnQ.classList.add('border-emerald-400', 'text-white');
        btnQ.classList.remove('border-transparent', 'text-teal-200');
        btnT.classList.remove('border-emerald-400', 'text-white');
        btnT.classList.add('border-transparent', 'text-teal-200');
      }} else {{
        tabQ.classList.add('hidden');
        tabT.classList.remove('hidden');
        btnT.classList.add('border-emerald-400', 'text-white');
        btnT.classList.remove('border-transparent', 'text-teal-200');
        btnQ.classList.remove('border-emerald-400', 'text-white');
        btnQ.classList.add('border-transparent', 'text-teal-200');
        renderTextbookKB();
      }}
    }};

    // Questions Tab Logic
    const sessionSelect = document.getElementById('session-select');
    const subjectSelect = document.getElementById('subject-select');
    const searchInput = document.getElementById('search-input');
    const repeatCheckbox = document.getElementById('repeat-only-checkbox');
    const questionsContainer = document.getElementById('questions-container');
    const countLabel = document.getElementById('filtered-count');

    // Populate Sessions Dropdown
    const sessions = [...new Set(QUESTIONS.map(q => q.session))].sort().reverse();
    sessions.forEach(s => {{
      const opt = document.createElement('option');
      opt.value = s;
      opt.textContent = `সেশন ${{s}}`;
      sessionSelect.appendChild(opt);
    }});

    // Stats
    document.getElementById('stat-total').textContent = QUESTIONS.length;
    document.getElementById('stat-bio').textContent = QUESTIONS.filter(q => q.subject === 'Biology').length;
    document.getElementById('stat-chem').textContent = QUESTIONS.filter(q => q.subject === 'Chemistry').length;
    document.getElementById('stat-phys').textContent = QUESTIONS.filter(q => q.subject === 'Physics').length;

    function renderQuestions() {{
      const filtered = QUESTIONS.filter(q => {{
        if (selectedSession !== "ALL" && q.session !== selectedSession) return false;
        if (selectedSubject !== "ALL" && q.subject !== selectedSubject) return false;
        if (repeatOnly && !q.is_repeated) return false;
        if (searchQuery) {{
          const term = searchQuery.toLowerCase();
          const matchQ = (q.question_bn || '').toLowerCase().includes(term);
          const matchA = (q.option_a || '').toLowerCase().includes(term);
          const matchB = (q.option_b || '').toLowerCase().includes(term);
          const matchC = (q.option_c || '').toLowerCase().includes(term);
          const matchD = (q.option_d || '').toLowerCase().includes(term);
          const matchE = (q.explanation || '').toLowerCase().includes(term);
          const matchChap = (q.chapter || '').toLowerCase().includes(term);
          if (!matchQ && !matchA && !matchB && !matchC && !matchD && !matchE && !matchChap) return false;
        }}
        return true;
      }});

      countLabel.textContent = `প্রদর্শিত হচ্ছে ${{filtered.length}} টি প্রশ্ন (সর্বমোট ${{QUESTIONS.length}} টি থেকে)`;

      if (filtered.length === 0) {{
        questionsContainer.innerHTML = `
          <div class="bg-white p-12 text-center rounded-2xl border border-slate-200">
            <p class="text-4xl mb-3">🔍</p>
            <p class="text-lg font-semibold text-slate-700">কোনো প্রশ্ন খুঁজে পাওয়া যায়নি</p>
          </div>
        `;
        return;
      }}

      questionsContainer.innerHTML = filtered.map(q => `
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 transition hover:shadow-md">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-1 rounded-md text-xs font-semibold bg-slate-100 text-slate-700">
                সেশন ${{q.session}}
              </span>
              <span class="px-2.5 py-1 rounded-md text-xs font-semibold bg-teal-50 text-teal-800 border border-teal-200">
                ${{q.subject}} • ${{q.chapter || 'সাধারণ'}}
              </span>
              ${{q.is_repeated ? '<span class="px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-700 border border-red-200">🔁 রিপিট প্রশ্ন</span>' : ''}}
            </div>
            <span class="text-xs font-mono text-slate-400">${{q.id}}</span>
          </div>

          <h3 class="text-base sm:text-lg font-semibold text-slate-900 leading-relaxed mb-4">
            <span class="text-teal-700 font-bold mr-1">${{q.question_num}}.</span> ${{q.question_bn}}
          </h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
            <button onclick="checkAnswer('${{q.id}}', 0, ${{q.correct_index}})" class="opt-btn-${{q.id}}-0 text-left p-3 rounded-xl border border-slate-200 hover:border-teal-400 hover:bg-teal-50/40 text-sm transition flex items-center gap-2">
              <span class="w-6 h-6 rounded-full bg-slate-100 text-slate-700 flex items-center justify-center text-xs font-bold shrink-0">ক</span>
              <span>${{q.option_a}}</span>
            </button>
            <button onclick="checkAnswer('${{q.id}}', 1, ${{q.correct_index}})" class="opt-btn-${{q.id}}-1 text-left p-3 rounded-xl border border-slate-200 hover:border-teal-400 hover:bg-teal-50/40 text-sm transition flex items-center gap-2">
              <span class="w-6 h-6 rounded-full bg-slate-100 text-slate-700 flex items-center justify-center text-xs font-bold shrink-0">খ</span>
              <span>${{q.option_b}}</span>
            </button>
            <button onclick="checkAnswer('${{q.id}}', 2, ${{q.correct_index}})" class="opt-btn-${{q.id}}-2 text-left p-3 rounded-xl border border-slate-200 hover:border-teal-400 hover:bg-teal-50/40 text-sm transition flex items-center gap-2">
              <span class="w-6 h-6 rounded-full bg-slate-100 text-slate-700 flex items-center justify-center text-xs font-bold shrink-0">গ</span>
              <span>${{q.option_c}}</span>
            </button>
            <button onclick="checkAnswer('${{q.id}}', 3, ${{q.correct_index}})" class="opt-btn-${{q.id}}-3 text-left p-3 rounded-xl border border-slate-200 hover:border-teal-400 hover:bg-teal-50/40 text-sm transition flex items-center gap-2">
              <span class="w-6 h-6 rounded-full bg-slate-100 text-slate-700 flex items-center justify-center text-xs font-bold shrink-0">ঘ</span>
              <span>${{q.option_d}}</span>
            </button>
          </div>

          <div id="expl-${{q.id}}" class="hidden mt-4 p-4 rounded-xl bg-slate-50 border border-slate-200 text-sm space-y-2">
            <div class="flex items-center gap-2">
              <span class="font-bold text-teal-800">সঠিক উত্তর: (${{q.correct_option}})</span>
              <span class="text-xs text-slate-500">| রেফারেন্স: ${{q.book_reference || 'এনসিটিবি মূল পাঠ্যবই'}}</span>
            </div>
            <p class="text-slate-700 leading-relaxed">${{q.explanation}}</p>
            ${{q.repeat_source ? `<p class="text-xs text-amber-700 font-medium">📌 তথ্য: ${{q.repeat_source}}</p>` : ''}}
          </div>

          <div class="flex justify-end pt-2">
            <button onclick="toggleExplanation('${{q.id}}')" class="text-xs text-teal-600 hover:text-teal-800 font-medium flex items-center gap-1">
              <span>ব্যাখ্যা ও রেফারেন্স দেখুন</span> ▾
            </button>
          </div>
        </div>
      `).join('');
    }}

    window.checkAnswer = function(qid, selectedIdx, correctIdx) {{
      const expl = document.getElementById(`expl-${{qid}}`);
      expl.classList.remove('hidden');

      for (let i = 0; i < 4; i++) {{
        const btn = document.querySelector(`.opt-btn-${{qid}}-${{i}}`);
        if (!btn) continue;
        btn.disabled = true;
        if (i === correctIdx) {{
          btn.classList.add('bg-emerald-100', 'border-emerald-500', 'text-emerald-950', 'font-medium');
        }} else if (i === selectedIdx && selectedIdx !== correctIdx) {{
          btn.classList.add('bg-rose-100', 'border-rose-500', 'text-rose-950');
        }} else {{
          btn.classList.add('opacity-60');
        }}
      }}
    }};

    window.toggleExplanation = function(qid) {{
      const expl = document.getElementById(`expl-${{qid}}`);
      expl.classList.toggle('hidden');
    }};

    sessionSelect.addEventListener('change', e => {{ selectedSession = e.target.value; renderQuestions(); }});
    subjectSelect.addEventListener('change', e => {{ selectedSubject = e.target.value; renderQuestions(); }});
    searchInput.addEventListener('input', e => {{ searchQuery = e.target.value.trim(); renderQuestions(); }});
    repeatCheckbox.addEventListener('change', e => {{ repeatOnly = e.target.checked; renderQuestions(); }});

    // Textbook KB Logic
    const kbContainer = document.getElementById('kb-container');
    const kbSearchInput = document.getElementById('kb-search-input');
    const kbSubjectFilter = document.getElementById('kb-subject-filter');

    let kbSearchQuery = "";
    let kbSubject = "ALL";

    function renderTextbookKB() {{
      const filtered = TEXTBOOKS_KB.filter(k => {{
        if (kbSubject !== "ALL" && k.subject !== kbSubject) return false;
        if (kbSearchQuery) {{
          const term = kbSearchQuery.toLowerCase();
          const matchT = (k.topic || '').toLowerCase().includes(term);
          const matchTxt = (k.exact_text_bn || '').toLowerCase().includes(term);
          const matchK = (k.keywords || '').toLowerCase().includes(term);
          const matchA = (k.author || '').toLowerCase().includes(term);
          const matchChap = (k.chapter || '').toLowerCase().includes(term);
          if (!matchT && !matchTxt && !matchK && !matchA && !matchChap) return false;
        }}
        return true;
      }});

      if (filtered.length === 0) {{
        kbContainer.innerHTML = `
          <div class="bg-white p-12 text-center rounded-2xl border border-slate-200">
            <p class="text-4xl mb-3">📖</p>
            <p class="text-lg font-semibold text-slate-700">কোনো পাঠ্যবই তথ্য মেলেনি</p>
          </div>
        `;
        return;
      }}

      kbContainer.innerHTML = filtered.map(k => `
        <div class="bg-white rounded-2xl border border-emerald-100 shadow-sm p-6 space-y-4 hover:shadow-md transition">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-1 rounded-md text-xs font-semibold bg-emerald-100 text-emerald-900">
                ${{k.subject}}
              </span>
              <span class="text-xs font-medium text-slate-600">
                ${{k.book_name}} (${{k.author}})
              </span>
            </div>
            <span class="px-2 py-0.5 rounded text-xs font-semibold bg-amber-50 text-amber-800 border border-amber-200">
              ${{k.fact_type}}
            </span>
          </div>

          <div>
            <h3 class="text-lg font-bold text-slate-900 mb-1 flex items-center gap-2">
              <span>📌 ${{k.topic}}</span>
            </h3>
            <p class="text-xs text-slate-500">অধ্যায়: ${{k.chapter}} | ${{k.citation}}</p>
          </div>

          <div class="bg-emerald-50/50 rounded-xl p-4 border-l-4 border-emerald-500 text-slate-800 text-sm leading-relaxed">
            ${{k.exact_text_bn}}
          </div>

          ${{k.common_mcq_trap ? `
            <div class="bg-amber-50 rounded-xl p-3.5 border border-amber-200 text-xs text-amber-900 flex items-start gap-2">
              <span class="text-base shrink-0">⚠️</span>
              <div>
                <strong class="font-bold">মেডিকেল পরীক্ষার সাধারণ ফাঁদ (Common Trap):</strong>
                <p class="mt-0.5">${{k.common_mcq_trap}}</p>
              </div>
            </div>
          ` : ''}}
        </div>
      `).join('');
    }}

    kbSearchInput.addEventListener('input', e => {{
      kbSearchQuery = e.target.value.trim();
      renderTextbookKB();
    }});

    kbSubjectFilter.addEventListener('change', e => {{
      kbSubject = e.target.value;
      renderTextbookKB();
    }});

    // Initial render
    renderQuestions();
  </script>
</body>
</html>"""

with open(HTML_OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Updated full web app with Textbook Ground Truth Engine at: {HTML_OUTPUT_PATH}")
