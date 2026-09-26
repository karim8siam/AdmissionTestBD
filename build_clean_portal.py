import os
import json

BASE_DIR = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series"
INDEX_FILE = os.path.join(BASE_DIR, "web", "index.html")

with open(os.path.join(BASE_DIR, "data", "medical_100_tests.json")) as f:
    med_test_1 = json.load(f)[0]
med_1_json = json.dumps(med_test_1, ensure_ascii=False)

with open(os.path.join(BASE_DIR, "data", "versity_100_tests.json")) as f:
    var_test_1 = json.load(f)[0]
var_1_json = json.dumps(var_test_1, ensure_ascii=False)

portal_code = """<!DOCTYPE html>
<html lang="bn" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Admission Test BD | AI-Powered Exam Preparation & National Merit Ranking</title>
  <meta name="description" content="বাংলাদেশ শীর্ষস্থানীয় এডমিশন টেস্ট পোর্টাল: মেডিকেল ও ভার্সিটি ১০০ মডেল টেস্ট, বিগত ১৫ বছরের প্রশ্ন, ২০০০ পাঠ্যবই তথ্য এবং রিয়েল-টাইম জাতীয় ও সেশন মেধা তালিকা।">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js for AI Exam Analytics -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- KaTeX for crisp LaTeX Math rendering -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
  <!-- Canvas Confetti -->
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">

  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['Hind Siliguri', 'Plus Jakarta Sans', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          },
          colors: {
            brand: {
              50: '#ecfdf5',
              100: '#d1fae5',
              400: '#34d399',
              500: '#10b981',
              600: '#059669',
              700: '#047857',
              800: '#065f46',
              900: '#064e3b',
              950: '#022c22'
            },
            versity: {
              50: '#eff6ff',
              100: '#dbeafe',
              400: '#60a5fa',
              500: '#3b82f6',
              600: '#2563eb',
              700: '#1d4ed8',
              800: '#1e40af',
              900: '#1e3a8a',
              950: '#0f172a'
            },
            ai: {
              50: '#f5f3ff',
              100: '#ede9fe',
              400: '#a78bfa',
              500: '#8b5cf6',
              600: '#7c3aed',
              700: '#6d28d9',
              800: '#5b21b6',
              900: '#4c1d95',
            }
          }
        }
      }
    }
  </script>

  <style>
    body {
      font-family: 'Hind Siliguri', 'Plus Jakarta Sans', sans-serif;
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: #0f172a;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #334155;
      border-radius: 4px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
      background: #475569;
    }
    .glow-brand {
      box-shadow: 0 0 35px -5px rgba(16, 185, 129, 0.25);
    }
    .glow-versity {
      box-shadow: 0 0 35px -5px rgba(59, 130, 246, 0.25);
    }
    .glow-ai {
      box-shadow: 0 0 35px -5px rgba(139, 92, 246, 0.25);
    }
    .badge-pulse {
      animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    @keyframes pulse-ring {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(1.05); }
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col selection:bg-brand-500 selection:text-white">

  <!-- ============================================== -->
  <!-- TOP NAVIGATION BAR -->
  <!-- ============================================== -->
  <header class="sticky top-0 z-50 bg-slate-900/90 backdrop-blur-md border-b border-slate-800 shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        
        <!-- Logo & Branding -->
        <div class="flex items-center gap-3 cursor-pointer" onclick="switchStream('medical')">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 via-emerald-500 to-teal-400 flex items-center justify-center font-black text-slate-950 text-xl shadow-lg glow-brand shrink-0">
            A
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="font-black text-lg sm:text-xl tracking-tight text-white">ADMISSION TEST <span class="text-brand-400">BD</span></span>
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-ai-900/80 text-ai-300 border border-ai-700 font-bold hidden sm:inline-block">AI 2.0</span>
            </div>
            <p class="text-[11px] text-slate-400 hidden sm:block">বাংলাদেশ অ্যাডমিশন মডেল টেস্ট ও জাতীয় মেধা র‍্যাংকিং</p>
          </div>
        </div>

        <!-- Admission Season Selector (Strictly Season Only - No Name / University) -->
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-2 bg-slate-800/90 px-3 py-1.5 rounded-xl border border-slate-700/80 shadow-inner">
            <span class="text-xs text-brand-400 font-bold flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-brand-400 animate-ping"></span>
              <span class="hidden md:inline">ভর্তি সেশন:</span>
            </span>
            <select id="season-selector" onchange="changeAdmissionSession(this.value)" class="bg-slate-900 border border-slate-700 text-xs sm:text-sm font-extrabold text-white rounded-lg px-2.5 py-1 focus:ring-2 focus:ring-brand-500 focus:outline-none cursor-pointer">
              <option value="2025-26" selected>২০২৫-২৬ সেশন (চলতি ব্যাচ)</option>
              <option value="2026-27">২০২৬-২৭ সেশন (পরবর্তী সেশন)</option>
              <option value="2024-25">২০২৪-২৫ সেশন (বিগত সেশন)</option>
              <option value="2027-28">২০২৭-২৮ সেশন (অগ্রিম ব্যাচ)</option>
            </select>
          </div>

          <!-- Quick Progress Indicator -->
          <div class="hidden lg:flex items-center gap-2 text-xs">
            <span id="med-unlocked-badge" class="px-2.5 py-1 rounded-lg bg-emerald-950/80 text-emerald-300 border border-emerald-800 font-semibold flex items-center gap-1">
              🩺 মেডিকেল: টেস্ট ০১ আনলকড
            </span>
            <span id="var-unlocked-badge" class="px-2.5 py-1 rounded-lg bg-blue-950/80 text-blue-300 border border-blue-800 font-semibold flex items-center gap-1">
              🏛️ ভার্সিটি ও গুচ্ছ: টেস্ট ০১ আনলকড
            </span>
          </div>

          <!-- User Auth Widget (Sign In / Sign Up & Profile) -->
          <div id="user-auth-widget"></div>
        </div>

      </div>

      <!-- Main Navigation Tabs: Stream Order Medical -> Varsity -> Engineering (Last) -> 15 Years -> Textbooks -> Tricks -->
      <nav class="flex items-center space-x-1 sm:space-x-2 overflow-x-auto py-2 custom-scrollbar border-t border-slate-800/60 text-xs sm:text-sm font-semibold">
        <button id="nav-btn-medical" onclick="switchStream('medical')" class="px-3.5 py-2 rounded-xl transition flex items-center gap-2 whitespace-nowrap bg-brand-600 text-white shadow-md font-bold">
          <span>🩺</span>
          <span>মেডিকেল ১০০ মডেল টেস্ট</span>
          <span class="text-[10px] px-1.5 py-0.5 rounded bg-brand-950/80 text-brand-200">লাইভ</span>
        </button>
        
        <button id="nav-btn-versity" onclick="switchStream('versity')" class="px-3.5 py-2 rounded-xl transition flex items-center gap-2 whitespace-nowrap text-slate-300 hover:text-white hover:bg-slate-800/80">
          <span>🏛️</span>
          <span>ভার্সিটি ও গুচ্ছ বিজ্ঞান ১০০ টেস্ট</span>
          <span class="text-[10px] px-1.5 py-0.5 rounded bg-blue-900/60 text-blue-300">DU • GST • Agri</span>
        </button>

        <button id="nav-btn-past" onclick="switchStream('past_15years')" class="px-3.5 py-2 rounded-xl transition flex items-center gap-2 whitespace-nowrap text-slate-300 hover:text-white hover:bg-slate-800/80">
          <span>📜</span>
          <span>বিগত ১৫ বছরের প্রশ্ন (২০১০-২০২৫)</span>
          <span class="text-[10px] px-1.5 py-0.5 rounded bg-purple-900/60 text-purple-300">আনলক মুক্ত</span>
        </button>

        <button id="nav-btn-kb" onclick="switchStream('textbooks')" class="px-3.5 py-2 rounded-xl transition flex items-center gap-2 whitespace-nowrap text-slate-300 hover:text-white hover:bg-slate-800/80">
          <span>📚</span>
          <span>পাঠ্যবই নলেজ বেস (২,০০০ তথ্য)</span>
          <span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-900/60 text-amber-300">এনসিটিবি</span>
        </button>

        <button id="nav-btn-nocalc" onclick="switchStream('nocalc')" class="px-3.5 py-2 rounded-xl transition flex items-center gap-2 whitespace-nowrap text-slate-300 hover:text-white hover:bg-slate-800/80">
          <span>⚡</span>
          <span>ক্যালকুলেটরবিহীন স্পিড ট্রিকস</span>
        </button>

        <!-- Engineering Stream (Placed at the end of the sequence) -->
        <button id="nav-btn-engineering" onclick="switchStream('engineering')" class="px-3.5 py-2 rounded-xl transition flex items-center gap-2 whitespace-nowrap text-slate-400 hover:text-slate-300 hover:bg-slate-800/40">
          <span>📐</span>
          <span>ইঞ্জিনিয়ারিং ভর্তি (BUET/CKRUET)</span>
          <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">শীঘ্রই আসছে</span>
        </button>
      </nav>

    </div>
  </header>

  <!-- ============================================== -->
  <!-- TOAST / NOTIFICATION CONTAINER -->
  <!-- ============================================== -->
  <div id="toast-container" class="fixed top-20 right-4 z-50 flex flex-col gap-2 pointer-events-none"></div>

  <!-- ============================================== -->
  <!-- MAIN CONTENT CONTAINER -->
  <!-- ============================================== -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

    <!-- HERO / BANNER WITH AI VIBE & ILLUSTRATIONS -->
    <section id="hero-banner" class="relative rounded-3xl overflow-hidden bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-slate-800 p-6 sm:p-8 shadow-2xl">
      <div class="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
        <div class="max-w-2xl space-y-3">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-950/80 text-brand-300 border border-brand-800 text-xs font-bold">
            <span class="w-2 h-2 rounded-full bg-brand-400"></span>
            পরবর্তী পরীক্ষা দিতে পূর্ববর্তী পরীক্ষা সম্পন্ন বাধ্যতামূলক
          </div>
          <h1 id="hero-title" class="text-2xl sm:text-4xl font-black text-white tracking-tight">
            মেডিকেল ও ভার্সিটি <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 via-emerald-300 to-teal-200">১০০ মডেল টেস্ট সিরিজ</span>
          </h1>
          <p id="hero-subtitle" class="text-sm sm:text-base text-slate-300 font-medium">
            পরপর সিকোয়েন্সিয়াল টেস্ট আনলক সিস্টেম। প্রতিটি টেস্টে রয়েছে ৬০ মিনিটের রিয়েল-টাইম কাউন্টডাউন টাইমার, সেশন মেধা ও সর্বকালের অল-বাংলাদেশ লাইভ র‍্যাংকিং।
          </p>
          <div class="flex flex-wrap items-center gap-4 text-xs font-semibold text-slate-300 pt-2">
            <div class="flex items-center gap-1.5">
              <span class="text-brand-400">✓</span> ১০,০০০+ এনসিটিবি প্রশ্নব্যাংক
            </div>
            <div class="flex items-center gap-1.5">
              <span class="text-brand-400">✓</span> নেগেটিভ মার্কিং (-০.২৫)
            </div>
            <div class="flex items-center gap-1.5">
              <span class="text-brand-400">✓</span> অটোমেটিক সাবমিট ব্যবস্থা
            </div>
            <div class="flex items-center gap-1.5">
              <span class="text-brand-400">✓</span> নির্ভুল পাঠ্যবই ব্যাখ্যা
            </div>
          </div>
        </div>

        <div class="w-full md:w-auto shrink-0 flex items-center justify-center gap-3">
          <img src="/web/assets/student_studying_ai.jpg" alt="Student Studying" class="w-28 h-28 sm:w-36 sm:h-36 rounded-2xl object-cover border border-slate-700 shadow-xl hidden sm:block">
          <img src="/web/assets/student_ai_analysis.jpg" alt="AI Analysis" class="w-28 h-28 sm:w-36 sm:h-36 rounded-2xl object-cover border border-slate-700 shadow-xl">
        </div>
      </div>
    </section>

    <!-- ============================================== -->
    <!-- VIEW 1: MODEL TEST SIMULATOR (Medical & Varsity) -->
    <!-- ============================================== -->
    <div id="view-model-tests" class="space-y-6">

      <!-- Test Navigation / Selection Bar -->
      <div class="bg-slate-900/90 rounded-2xl p-4 sm:p-5 border border-slate-800 shadow-lg flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        
        <!-- Left: Test Selector & Lock Summary -->
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-teal-500 flex items-center justify-center text-slate-950 font-black text-lg shadow-md shrink-0">
            📝
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h2 id="current-stream-heading" class="text-base sm:text-lg font-black text-white">মেডিকেল পূর্ণাঙ্গ মডেল টেস্ট নির্বাচন</h2>
              <span id="lock-rule-tag" class="text-[10px] px-2 py-0.5 rounded-full bg-amber-950/80 text-amber-300 border border-amber-800 font-bold">সিকোয়েন্সিয়াল লক সক্রিয়</span>
            </div>
            <p id="test-selector-subtext" class="text-xs text-slate-400">টেস্ট ০১ সম্পন্ন করলে টেস্ট ০২ স্বয়ংক্রিয়ভাবে আনলক হবে।</p>
          </div>
        </div>

        <!-- Right: Test Dropdown & Fast Jump -->
        <div class="flex items-center gap-2 sm:gap-3 flex-wrap">
          <div class="flex items-center gap-2 bg-slate-950 px-3 py-1.5 rounded-xl border border-slate-700">
            <span class="text-xs text-slate-400 font-semibold whitespace-nowrap">টেস্ট নম্বর:</span>
            <select id="model-test-dropdown" onchange="onTestDropdownChange(parseInt(this.value))" class="bg-slate-900 border border-slate-700 text-xs sm:text-sm font-bold text-brand-300 rounded-lg px-2.5 py-1 focus:ring-1 focus:ring-brand-500 focus:outline-none">
              <!-- Dynamically populated 1 to 100 with lock icons -->
            </select>
          </div>

          <button onclick="toggleTestGridModal()" class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-white border border-slate-700 transition flex items-center gap-1.5">
            <span>📋</span>
            <span>১০০ টেস্টের গ্রিড তালিকা</span>
          </button>

          <!-- bKash Premium Unlock Button -->
          <button id="btn-open-paywall" onclick="openBkashPaywallModal(appState.currentStream)" class="px-3.5 py-2 rounded-xl bg-gradient-to-r from-pink-600 via-rose-600 to-pink-500 hover:from-pink-500 hover:to-rose-400 text-white font-bold text-xs shadow-lg shadow-pink-500/25 flex items-center gap-1.5 transition">
            <span>👑 প্রিমিয়াম আনলক</span>
            <span class="bg-black/30 px-1.5 py-0.5 rounded text-[10px]">৳৪৯৯</span>
          </button>
        </div>

      </div>

      <!-- ============================================== -->
      <!-- PRE-EXAM START SCREEN (Questions Hidden Initially) -->
      <!-- ============================================== -->
      <div id="exam-start-card" class="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-10 shadow-2xl space-y-6 text-center max-w-3xl mx-auto">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-tr from-brand-600 via-emerald-500 to-teal-400 text-slate-950 text-3xl font-black shadow-xl mx-auto">
          ▶
        </div>

        <div class="space-y-2">
          <div class="flex items-center justify-center gap-2">
            <span id="start-badge-stream" class="text-xs font-bold px-3 py-1 rounded-full bg-brand-950 text-brand-300 border border-brand-800 uppercase tracking-wider">মেডিকেল পূর্ণাঙ্গ মডেল টেস্ট</span>
            <span id="start-badge-session" class="text-xs font-bold px-3 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">সেশন: ২০২৫-২৬</span>
          </div>
          <h2 id="start-exam-title" class="text-2xl sm:text-3xl font-black text-white">মেডিকেল পূর্ণাঙ্গ মডেল টেস্ট ০১</h2>
          <p class="text-xs sm:text-sm text-slate-400 max-w-xl mx-auto">
            পরীক্ষা শুরু বাটনে ক্লিক করার সাথে সাথে প্রশ্ন প্রদর্শিত হবে এবং ব্যাকওয়ার্ড কাউন্টডাউন টাইমার শুরু হবে। সময় শেষ হলে আপনার উত্তরপত্র স্বয়ংক্রিয়ভাবে সাবমিট হবে।
          </p>
        </div>

        <!-- Metrics Overview Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-2xl mx-auto pt-2">
          <div class="bg-slate-950/80 rounded-2xl p-3 border border-slate-800">
            <div class="text-[11px] text-slate-400 font-semibold">মোট প্রশ্ন</div>
            <div id="start-stat-questions" class="text-xl font-black text-white mt-1">১০০টি</div>
          </div>
          <div class="bg-slate-950/80 rounded-2xl p-3 border border-slate-800">
            <div class="text-[11px] text-slate-400 font-semibold">পূর্ণমান</div>
            <div id="start-stat-marks" class="text-xl font-black text-brand-400 mt-1">১০০</div>
          </div>
          <div class="bg-slate-950/80 rounded-2xl p-3 border border-slate-800">
            <div class="text-[11px] text-slate-400 font-semibold">নির্ধারিত সময়</div>
            <div id="start-stat-duration" class="text-xl font-black text-amber-400 mt-1">৬০ মিনিট</div>
          </div>
          <div class="bg-slate-950/80 rounded-2xl p-3 border border-slate-800">
            <div class="text-[11px] text-slate-400 font-semibold">নেগেটিভ মার্ক</div>
            <div class="text-xl font-black text-rose-400 mt-1">-০.২৫</div>
          </div>
        </div>

        <!-- Instructions -->
        <div class="bg-slate-950/60 rounded-2xl p-4 border border-slate-800 text-left text-xs text-slate-300 space-y-2 max-w-2xl mx-auto">
          <div class="font-bold text-white flex items-center gap-1.5 text-sm">
            <span>📌</span> পরীক্ষা শুরুর নিয়মাবলী:
          </div>
          <ul class="list-disc list-inside space-y-1 text-slate-400 pl-1">
            <li>প্রতিটি সঠিক উত্তরের জন্য পাবেন <strong class="text-emerald-400">+১.০০ নম্বর</strong>।</li>
            <li>প্রতিটি ভুল উত্তরের জন্য কাটা যাবে <strong class="text-rose-400">-০.২৫ নম্বর</strong> (নেগেটিভ মার্কিং)।</li>
            <li>টাইমার শূন্য (০০:০০) হওয়ার সাথে সাথে পরীক্ষা <strong class="text-amber-400">স্বয়ংক্রিয়ভাবে সাবমিট</strong> হবে।</li>
            <li>পরীক্ষা সাবমিট করার সাথে সাথেই আপনি <strong class="text-teal-400">চলতি সেশন ও সর্বকালের জাতীয় মেধা তালিকা</strong> দেখতে পাবেন।</li>
            <li>এই পরীক্ষাটি সফলভাবে সম্পন্ন করার পর পরবর্তী টেস্টটি আনলক হবে।</li>
          </ul>
        </div>

        <!-- Big Start Exam CTA Button -->
        <div class="pt-2">
          <button id="btn-start-exam" onclick="startActiveExam()" class="w-full sm:w-auto px-10 py-4 rounded-2xl bg-gradient-to-r from-brand-600 via-emerald-600 to-teal-500 hover:from-brand-500 hover:to-teal-400 text-slate-950 font-black text-lg shadow-xl glow-brand transition transform hover:-translate-y-0.5 active:translate-y-0">
            🚀 পরীক্ষা শুরু করো (Start Exam)
          </button>
        </div>

      </div>

      <!-- ============================================== -->
      <!-- ACTIVE EXAM CONTAINER (Shown only after clicking Start Exam) -->
      <!-- ============================================== -->
      <div id="exam-active-card" class="hidden space-y-6">

        <!-- Sticky Countdown Timer & Control Header -->
        <div class="sticky top-28 z-40 bg-slate-900/95 backdrop-blur-md rounded-2xl p-4 border border-slate-700/80 shadow-2xl flex flex-col gap-3">
          <div class="flex items-center justify-between gap-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/40 flex items-center justify-center font-black text-lg animate-pulse shrink-0">
                ⏳
              </div>
              <div>
                <div class="text-[11px] uppercase tracking-wider text-slate-400 font-bold">অবশিষ্ট সময় (Time Remaining)</div>
                <div id="countdown-timer-display" class="text-2xl sm:text-3xl font-black text-amber-300 font-mono tracking-wider">
                  ৬০:০০
                </div>
              </div>
            </div>

            <!-- Answer Counter Pills -->
            <div class="flex items-center gap-2 text-xs font-bold">
              <span class="px-3 py-1.5 rounded-xl bg-emerald-950/80 text-emerald-300 border border-emerald-800">
                উত্তর: <span id="answered-count-pill" class="text-white text-sm font-black">০</span>/<span id="total-questions-pill">১০০</span>
              </span>
              <span class="hidden sm:inline-block px-3 py-1.5 rounded-xl bg-slate-800 text-slate-300 border border-slate-700">
                বাকি: <span id="unanswered-count-pill" class="text-white text-sm font-black">১০০</span>
              </span>
            </div>

            <!-- Submit Button -->
            <button id="btn-submit-active-exam" onclick="confirmSubmitExam()" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-500 hover:from-emerald-500 hover:to-teal-400 text-white font-extrabold text-xs sm:text-sm shadow-lg shadow-emerald-950 transition flex items-center gap-1.5 border border-emerald-500/40 cursor-pointer">
              <span>📥</span>
              <span>সাবমিট করো</span>
            </button>
          </div>

          <!-- Real-Time Progress Bar -->
          <div class="w-full bg-slate-800/80 h-1.5 rounded-full overflow-hidden">
            <div id="exam-progress-bar" class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-full transition-all duration-300" style="width: 0%;"></div>
          </div>
        </div>

        <!-- Question Filter Tabs -->
        <div class="flex items-center gap-2 overflow-x-auto py-1 custom-scrollbar text-xs font-semibold">
          <button onclick="filterQuestionsBySubject('All', this)" class="q-filter-btn px-3 py-1.5 rounded-lg bg-slate-800 text-white border border-slate-700 active-filter">সব বিষয় (১০০)</button>
          <button id="q-filter-subj1" onclick="filterQuestionsBySubject('Biology', this)" class="q-filter-btn px-3 py-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800">জীববিজ্ঞান</button>
          <button id="q-filter-subj2" onclick="filterQuestionsBySubject('Chemistry', this)" class="q-filter-btn px-3 py-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800">রসায়ন</button>
          <button id="q-filter-subj3" onclick="filterQuestionsBySubject('Physics', this)" class="q-filter-btn px-3 py-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800">পদার্থবিজ্ঞান</button>
          <button id="q-filter-subj4" onclick="filterQuestionsBySubject('English_GK', this)" class="q-filter-btn px-3 py-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800">ইংরেজি ও জিকে</button>
        </div>

        <!-- Question Feed -->
        <div id="questions-feed-container" class="space-y-4">
          <!-- Dynamically generated question cards -->
        </div>

        <!-- Bottom Submit Bar -->
        <div class="bg-slate-900 rounded-2xl p-6 border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
          <div>
            <h4 class="text-sm font-bold text-white">পরীক্ষা শেষ করার আগে সমস্ত উত্তর যাচাই করে নিন</h4>
            <p class="text-xs text-slate-400">সাবমিট করার সাথে সাথেই সেশন মেধা ও সর্বকালের অল-বাংলাদেশ ফলাফল প্রকাশ পাবে।</p>
          </div>
          <button onclick="confirmSubmitExam()" class="w-full sm:w-auto px-8 py-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-500 text-slate-950 font-black text-sm shadow-xl glow-brand hover:from-emerald-500 hover:to-teal-400 transition">
            ফলাফল জমা দিন (Submit Exam)
          </button>
        </div>

      </div>

      <!-- ============================================== -->
      <!-- SCOREBOARD & POST-EXAM AUTOPSY (Shown after Submit) -->
      <!-- ============================================== -->
      <div id="exam-results-card" class="hidden space-y-6">

        <!-- Top Score & Unlock Congratulation Banner -->
        <div id="results-banner-card" class="bg-gradient-to-r from-slate-900 via-emerald-950/40 to-slate-900 rounded-3xl p-6 sm:p-8 border border-emerald-800/80 shadow-2xl relative overflow-hidden">
          
          <div class="flex flex-col md:flex-row items-center justify-between gap-6 relative z-10">
            <div class="space-y-2 text-center md:text-left">
              <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800 text-xs font-bold">
                <span>🏆</span> ফলাফল চূড়ান্তভাবে প্রকাশিত
              </div>
              <h2 id="results-test-name" class="text-2xl sm:text-3xl font-black text-white">মেডিকেল পূর্ণাঙ্গ মডেল টেস্ট ০১</h2>
              <p id="results-unlock-notice" class="text-xs sm:text-sm text-emerald-400 font-bold flex items-center justify-center md:justify-start gap-1.5">
                <span>🎉</span> অভিনন্দন! পরবর্তী টেস্টটি সফলভাবে আনলক হয়েছে!
              </p>
            </div>

            <!-- Score Pill -->
            <div class="bg-slate-950/90 rounded-2xl p-5 border border-slate-700/80 text-center shadow-xl shrink-0 min-w-[200px]">
              <div class="text-xs uppercase font-extrabold text-slate-400 tracking-wider">তোমার মোট প্রাপ্ত নম্বর</div>
              <div id="results-total-score" class="text-4xl font-black text-brand-400 font-mono mt-1">০.০০</div>
              <div class="text-[11px] text-slate-400 mt-1">পূর্ণমান: <span id="results-full-marks">১০০</span></div>
            </div>
          </div>

          <!-- Dual Real-time Ranking Grid: Session Ranking + All-Time Ranking -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-6 pt-6 border-t border-slate-800 relative z-10">
            
            <!-- Session Ranking Card -->
            <div class="bg-slate-950/80 rounded-2xl p-4 border border-brand-500/40 flex items-center justify-between gap-4">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 rounded-xl bg-brand-500/20 text-brand-400 border border-brand-500/40 flex items-center justify-center text-2xl font-black shrink-0">
                  🏅
                </div>
                <div>
                  <div class="text-[11px] text-brand-300 font-bold uppercase tracking-wider">
                    সেশন মেধা স্থান (<span id="results-session-name">২০২৫-২৬</span>)
                  </div>
                  <div id="results-session-rank" class="text-2xl font-black text-white font-mono mt-0.5">
                    -- <span class="text-xs text-slate-400 font-normal">/ মোট -- জন</span>
                  </div>
                </div>
              </div>
              <div class="text-right">
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-brand-950 text-brand-300 border border-brand-800 font-bold">লাইভ সেশন</span>
              </div>
            </div>

            <!-- All-Time National Ranking Card -->
            <div class="bg-slate-950/80 rounded-2xl p-4 border border-teal-500/40 flex items-center justify-between gap-4">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 rounded-xl bg-teal-500/20 text-teal-400 border border-teal-500/40 flex items-center justify-center text-2xl font-black shrink-0">
                  🌍
                </div>
                <div>
                  <div class="text-[11px] text-teal-300 font-bold uppercase tracking-wider">
                    সর্বকালের জাতীয় মেধাক্রম (All-Time)
                  </div>
                  <div id="results-alltime-rank" class="text-2xl font-black text-white font-mono mt-0.5">
                    -- <span class="text-xs text-slate-400 font-normal">/ মোট -- জন</span>
                  </div>
                </div>
              </div>
              <div class="text-right">
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-teal-950 text-teal-300 border border-teal-800 font-bold">অল-বাংলাদেশ</span>
              </div>
            </div>

          </div>

          <!-- Quick Metrics Bar -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
            <div class="bg-slate-950/70 rounded-xl p-3 border border-slate-800 text-center">
              <div class="text-[10px] text-slate-400 font-semibold">সঠিক উত্তর</div>
              <div id="results-correct-count" class="text-lg font-black text-emerald-400 mt-0.5">০</div>
            </div>
            <div class="bg-slate-950/70 rounded-xl p-3 border border-slate-800 text-center">
              <div class="text-[10px] text-slate-400 font-semibold">ভুল উত্তর (-০.২৫)</div>
              <div id="results-wrong-count" class="text-lg font-black text-rose-400 mt-0.5">০</div>
            </div>
            <div class="bg-slate-950/70 rounded-xl p-3 border border-slate-800 text-center">
              <div class="text-[10px] text-slate-400 font-semibold">উত্তর করা হয়নি</div>
              <div id="results-unanswered-count" class="text-lg font-black text-slate-400 mt-0.5">০</div>
            </div>
            <div class="bg-slate-950/70 rounded-xl p-3 border border-slate-800 text-center">
              <div class="text-[10px] text-slate-400 font-semibold">ব্যয়িত সময়</div>
              <div id="results-time-taken" class="text-lg font-black text-amber-300 mt-0.5">০০:০০</div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center justify-between gap-3 mt-6 pt-4 border-t border-slate-800/80 flex-wrap">
            <button onclick="retakeCurrentExam()" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-white border border-slate-700 transition flex items-center gap-1.5">
              <span>🔄</span> আবার পরীক্ষা দিন
            </button>

            <button id="btn-goto-next-test" onclick="loadNextUnlockedExam()" class="px-6 py-2.5 rounded-xl bg-gradient-to-r from-brand-600 to-teal-500 text-slate-950 font-black text-xs sm:text-sm shadow-lg glow-brand hover:from-brand-500 hover:to-teal-400 transition flex items-center gap-1.5">
              <span>পরবর্তী টেস্টে যান (Next Test)</span>
              <span>→</span>
            </button>
          </div>

          <!-- Test 5 Completion Teaser Card (Invites to unlock 95 tests for 499 BDT) -->
          <div id="results-paywall-teaser" class="hidden mt-6 p-6 rounded-3xl bg-gradient-to-br from-pink-950/80 via-slate-900 to-purple-950/80 border-2 border-pink-500/60 text-center relative overflow-hidden shadow-2xl">
            <div class="text-4xl mb-2">🎉</div>
            <h3 class="text-lg sm:text-xl font-black text-white">অভিনন্দন! আপনি সফলভাবে ফ্রি ৫টি মডেল টেস্ট সম্পন্ন করেছেন</h3>
            <p class="text-xs sm:text-sm text-pink-200 mt-2 max-w-xl mx-auto leading-relaxed">
              পরবর্তী ৯৫টি এক্সক্লুসিভ মডেল টেস্ট (টেস্ট ৬ থেকে ১০০), লাইভ জাতীয় মেধা তালিকায় স্থায়ী অবস্থান এবং সম্পূর্ণ পাঠ্যবই ব্যাখ্যা পেতে মাত্র ৳৪৯৯ দিয়ে প্রিমিয়াম ব্যাচ আনলক করুন।
            </p>
            <button onclick="openBkashPaywallModal(appState.currentStream, 6)" class="mt-4 px-8 py-3 rounded-2xl bg-gradient-to-r from-pink-500 via-rose-600 to-pink-600 hover:from-pink-400 hover:to-rose-500 text-white font-black shadow-xl shadow-pink-500/40 text-xs sm:text-sm transition transform hover:scale-105 active:scale-95 inline-flex items-center gap-2">
              <span>📱 bKash দিয়ে বাকি ৯৫টি টেস্ট আনলক করুন (৳৪৯৯)</span>
            </button>
          </div>

        </div>

        <!-- AI Exam Autopsy / Analytics Chart -->
        <div class="bg-slate-900 rounded-3xl p-6 border border-slate-800 shadow-xl space-y-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="text-ai-400 text-lg">📊</span>
              <h3 class="text-base font-bold text-white">AI এক্সাম অটপসি ও বিষয়ভিত্তিক পারফরম্যান্স</h3>
            </div>
            <span class="text-xs text-slate-400">এনসিটিবি পাঠ্যবই ম্যাপিং</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
            <div class="h-64 flex items-center justify-center">
              <canvas id="exam-subject-chart"></canvas>
            </div>
            <div id="subject-performance-list" class="space-y-3">
              <!-- Dynamically populated subject stats -->
            </div>
          </div>
        </div>

        <!-- Detailed Question Review with Right/Wrong Markers & Explanations -->
        <div class="bg-slate-900 rounded-3xl p-6 border border-slate-800 shadow-xl space-y-4">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h3 class="text-base font-bold text-white flex items-center gap-2">
                <span>📖</span> প্রতিটি প্রশ্নের বিস্তারিত উত্তর ও পাঠ্যবই ব্যাখ্যা
              </h3>
              <p class="text-xs text-slate-400">সবুজ রঙ সঠিক উত্তর, লাল রঙ আপনার ভুল উত্তর নির্দেশ করে।</p>
            </div>
            <div class="flex items-center gap-2 text-xs">
              <span class="px-2 py-1 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">✓ সঠিক</span>
              <span class="px-2 py-1 rounded bg-rose-950 text-rose-300 border border-rose-800">✗ ভুল</span>
            </div>
          </div>

          <div id="results-review-feed" class="space-y-4">
            <!-- Review cards will be dynamically rendered here -->
          </div>
        </div>

      </div>

    </div>

    <!-- ============================================== -->
    <!-- VIEW 2: PAST 15 YEARS TESTS (2010 - 2025) -->
    <!-- ============================================== -->
    <div id="view-past-15years" class="hidden space-y-6">
      
      <!-- Past 15 Years Header -->
      <div class="bg-slate-900/90 rounded-2xl p-5 border border-slate-800 shadow-lg flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-purple-600/30 text-purple-400 border border-purple-500/40 flex items-center justify-center text-xl font-bold shrink-0">
            📜
          </div>
          <div>
            <h2 class="text-base sm:text-lg font-black text-white flex items-center gap-2">
              <span id="past-year-stream-title">বিগত ১৫ বছরের প্রশ্নব্যাংক (২০১০ - ২০২৫)</span>
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-purple-950 text-purple-300 border border-purple-800 font-bold">লক মুক্ত / উন্মুক্ত</span>
            </h2>
            <p class="text-xs text-slate-400">মেডিকেল ও ভার্সিটি/গুচ্ছ উভয় শাখার ১৫ বছরের ৩,০০০ প্রশ্নপত্র পূর্ণাঙ্গ টেস্ট ও উত্তরপত্র সহ। যেকোনো সেশন যখন ইচ্ছা পরীক্ষা দিন।</p>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-2">
          <!-- Sub-stream switch: Medical vs Versity -->
          <div class="flex rounded-xl bg-slate-950 p-1 border border-slate-800">
            <button id="past-btn-medical" onclick="switchPastSubStream('medical')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition bg-purple-600 text-white shadow">
              🩺 মেডিকেল (১৫ বছর)
            </button>
            <button id="past-btn-versity" onclick="switchPastSubStream('versity')" class="px-3 py-1.5 rounded-lg text-xs font-bold text-slate-400 hover:text-white transition">
              🏛️ ভার্সিটি ও গুচ্ছ (১৫ বছর)
            </button>
          </div>

          <div class="flex items-center gap-1.5">
            <span class="text-xs text-slate-400 font-semibold">সেশন:</span>
            <select id="past-year-select" onchange="loadPastYearTest(this.value)" class="bg-slate-950 border border-slate-700 text-xs sm:text-sm font-bold text-purple-300 rounded-lg px-2.5 py-1.5 focus:ring-1 focus:ring-purple-500 focus:outline-none">
              <!-- Dynamically populated with 15 sessions -->
            </select>
          </div>
        </div>
      </div>

      <!-- Past Year Mode Switcher: Take Timed Test vs View Answers -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex items-center justify-between gap-4 flex-wrap">
        <div class="flex items-center gap-2">
          <span id="past-year-active-badge" class="px-3 py-1 rounded-xl bg-purple-950 text-purple-300 border border-purple-800 text-xs font-bold">
            সেশন: ২০২৪-২০২৫
          </span>
          <span id="past-year-question-count-badge" class="px-3 py-1 rounded-xl bg-slate-800 text-slate-300 text-xs font-semibold">
            ১০০টি আসল প্রশ্ন
          </span>
        </div>

        <div class="flex items-center gap-2">
          <button id="btn-past-show-answers" onclick="togglePastYearAnswerSheet()" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-white border border-slate-700 transition flex items-center gap-1.5">
            <span>👁️</span>
            <span id="past-show-answer-text">উত্তরপত্র দেখুন (Show Answers)</span>
          </button>
          
          <button onclick="startPastYearExam()" class="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs shadow-lg transition flex items-center gap-1.5">
            <span>⏱️</span>
            <span>টাইমড পরীক্ষা শুরু করো</span>
          </button>
        </div>
      </div>

      <!-- Past Year Question Feed / Answer Sheet -->
      <div id="past-year-questions-container" class="space-y-4">
        <!-- Rendered dynamically -->
      </div>

    </div>

    <!-- ============================================== -->
    <!-- VIEW 3: TEXTBOOK KNOWLEDGE BASE (2,000 Facts) -->
    <!-- ============================================== -->
    <div id="view-textbooks-kb" class="hidden space-y-6">
      
      <!-- Textbook KB Header & Search Bar -->
      <div class="bg-slate-900/90 rounded-2xl p-5 border border-slate-800 shadow-lg space-y-4">
        <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-amber-600/30 text-amber-400 border border-amber-500/40 flex items-center justify-center text-xl font-bold shrink-0">
              📚
            </div>
            <div>
              <h2 class="text-base sm:text-lg font-black text-white flex items-center gap-2">
                এনসিটিবি পাঠ্যবই ভিত্তিক নলেজ বেস
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-amber-950 text-amber-300 border border-amber-800 font-bold">২,০০০টি তথ্য</span>
              </h2>
              <p class="text-xs text-slate-400">আবুল হাসান, গাজী আজমল, হাজারী ও নাগ, শাহজাহান তপন এবং এস ইউ আহাম্মদের বই থেকে সরাসরি উদ্ধৃত।</p>
            </div>
          </div>

          <!-- Live Search Input -->
          <div class="w-full md:w-80">
            <input type="text" id="kb-search-input" oninput="onKbSearch(this.value)" placeholder="অধ্যায়, টপিক বা কি-ওয়ার্ড খুঁজুন..." class="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-700 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 transition shadow-inner">
          </div>
        </div>

        <!-- Subject Filter Chips -->
        <div class="flex items-center gap-2 overflow-x-auto py-1 custom-scrollbar text-xs font-semibold">
          <button onclick="filterKbBySubject('All', this)" class="kb-chip px-3 py-1.5 rounded-lg bg-amber-500 text-slate-950 font-bold active-kb-chip">সব তথ্য (২,০০০)</button>
          <button onclick="filterKbBySubject('Botany', this)" class="kb-chip px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white">উদ্ভিদবিজ্ঞান (আবুল হাসান)</button>
          <button onclick="filterKbBySubject('Zoology', this)" class="kb-chip px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white">প্রাণিবিজ্ঞান (গাজী আজমল)</button>
          <button onclick="filterKbBySubject('Chem1', this)" class="kb-chip px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white">রসায়ন ১ম (হাজারী ও নাগ)</button>
          <button onclick="filterKbBySubject('Chem2', this)" class="kb-chip px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white">রসায়ন ২য় (হাজারী ও নাগ)</button>
          <button onclick="filterKbBySubject('Phys1', this)" class="kb-chip px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white">পদার্থবিজ্ঞান ১ম (তপন)</button>
          <button onclick="filterKbBySubject('Phys2', this)" class="kb-chip px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white">পদার্থবিজ্ঞান ২য় (তপন)</button>
          <button onclick="filterKbBySubject('Math', this)" class="kb-chip px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white">উচ্চতর গণিত (এস ইউ আহাম্মদ)</button>
        </div>
      </div>

      <!-- KB Count & Pagination Header -->
      <div class="flex items-center justify-between text-xs text-slate-400 px-1">
        <div>
          প্রদর্শিত হচ্ছে: <span id="kb-showing-count" class="font-bold text-white">১ - ২৫</span> (মোট <span id="kb-total-count" class="font-bold text-amber-400">২,০০০</span>টি তথ্যের মধ্যে)
        </div>
        <div class="flex items-center gap-2">
          <button id="btn-kb-prev" onclick="prevKbPage()" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-white disabled:opacity-40">পূর্ববর্তী</button>
          <span id="kb-page-indicator" class="font-bold text-slate-300">১ / ৮০</span>
          <button id="btn-kb-next" onclick="nextKbPage()" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-white disabled:opacity-40">পরবর্তী</button>
        </div>
      </div>

      <!-- KB Fact Cards Feed -->
      <div id="kb-facts-container" class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Rendered dynamically -->
      </div>

      <!-- Bottom Pagination -->
      <div class="flex items-center justify-center gap-2 pt-4">
        <button onclick="prevKbPage()" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-white">← পূর্ববর্তী পাতা</button>
        <button onclick="nextKbPage()" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-white">পরবর্তী পাতা →</button>
      </div>

    </div>

    <!-- ============================================== -->
    <!-- VIEW 4: NO-CALCULATOR SPEED TRICKS -->
    <!-- ============================================== -->
    <div id="view-nocalc" class="hidden space-y-6">
      
      <div class="bg-slate-900/90 rounded-2xl p-5 border border-slate-800 shadow-lg flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/40 flex items-center justify-center text-xl font-bold shrink-0">
          ⚡
        </div>
        <div>
          <h2 class="text-base sm:text-lg font-black text-white">ঢাকা বিশ্ববিদ্যালয় 'ক' ইউনিট ও গুচ্ছ স্পিড ম্যাথ ইঞ্জিন</h2>
          <p class="text-xs text-slate-400">ক্যালকুলেটর ছাড়া ১৫ সেকেন্ডে বড় গুণ, লগারিদম, বর্গমূল ও পিএইচ নির্ণয়ের বৈজ্ঞানিক টেকনিক।</p>
        </div>
      </div>

      <div id="nocalc-tricks-grid" class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Rendered dynamically from nocalc_tricks_kb.json -->
      </div>

    </div>

    <!-- ============================================== -->
    <!-- VIEW 5: ENGINEERING STREAM (Placed at sequence end) -->
    <!-- ============================================== -->
    <div id="view-engineering" class="hidden space-y-6">
      
      <div class="bg-slate-900 rounded-3xl p-8 sm:p-12 border border-slate-800 text-center space-y-4 max-w-2xl mx-auto shadow-2xl">
        <div class="w-16 h-16 rounded-2xl bg-slate-800 text-slate-400 border border-slate-700 flex items-center justify-center text-3xl font-black mx-auto">
          📐
        </div>
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800 text-slate-400 border border-slate-700 text-xs font-bold">
          <span>⏳</span> প্রস্তুতি চলছে / Coming Soon
        </div>
        <h2 class="text-2xl sm:text-3xl font-black text-white">ইঞ্জিনিয়ারিং ভর্তি প্রস্তুতি (বুয়েট ও সিকেআরইউইটি)</h2>
        <p class="text-xs sm:text-sm text-slate-400">
          বুয়েট, রুয়েট, কুয়েট ও চুয়েট-এর লিখিত এবং প্রিলিমিনারি কনসেপচুয়াল প্রশ্নব্যাংক এবং স্পেশাল ইঞ্জিনিয়ারিং মডেল টেস্ট তৈরির কাজ প্রক্রিয়াধীন রয়েছে। খুব শীঘ্রই এটি লাইভ হবে।
        </p>
        <div class="pt-4">
          <button onclick="switchStream('medical')" class="px-6 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-bold text-xs shadow-lg transition">
            মেডিকেল ১০০ টেস্টে ফিরে যান
          </button>
        </div>
      </div>

    </div>

  </main>

  <!-- ============================================== -->
  <!-- FOOTER -->
  <!-- ============================================== -->
  <footer class="bg-slate-950 border-t border-slate-900 mt-auto py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-6">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-brand-500/20 text-brand-400 border border-brand-500/40 flex items-center justify-center font-black text-sm">
          A
        </div>
        <div>
          <p class="text-sm font-bold text-white">Admission Test BD &copy; 2025-2026</p>
          <p class="text-xs text-slate-400">বাংলাদেশ জাতীয় মেডিকেল ও ভার্সিটি মেধা যাচাই প্ল্যাটফর্ম</p>
        </div>
      </div>

      <!-- Contact Info -->
      <div class="flex flex-wrap items-center gap-4 text-xs text-slate-300">
        <a href="mailto:shahriyarkarimsiam@gmail.com" class="flex items-center gap-1.5 hover:text-brand-400 transition bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
          <span>📧</span>
          <span>shahriyarkarimsiam@gmail.com</span>
        </a>
        <a href="https://www.facebook.com/profile.php?id=61594973542595" target="_blank" rel="noopener noreferrer" class="flex items-center gap-1.5 hover:text-blue-400 transition bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
          <span>🌐</span>
          <span>Facebook Page</span>
        </a>
      </div>

      <!-- Discrete Admin Entry -->
      <div>
        <button onclick="openAdminModal()" class="text-[11px] text-slate-400 hover:text-brand-400 transition flex items-center gap-1 bg-slate-900/60 hover:bg-slate-800 px-2.5 py-1 rounded-md border border-slate-800">
          <span>🔐</span>
          <span>অ্যাডমিন প্যানেল</span>
        </button>
      </div>
    </div>
  </footer>

  <!-- ============================================== -->
  <!-- 100 TESTS GRID MODAL (All 100 Tests Status) -->
  <!-- ============================================== -->
  <div id="grid-modal" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm hidden flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-800 rounded-3xl max-w-4xl w-full max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
      
      <div class="p-5 border-b border-slate-800 flex items-center justify-between">
        <div>
          <h3 id="grid-modal-title" class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            <span>📋</span> ১০০ মডেল টেস্টের অগ্রগতি ও আনলক স্থিতি
          </h3>
          <p class="text-xs text-slate-400">পূর্ববর্তী টেস্ট সম্পন্ন হলে ক্রমান্বয়ে পরবর্তী টেস্ট আনলক হবে।</p>
        </div>
        <button onclick="toggleTestGridModal()" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center text-sm font-bold">✕</button>
      </div>

      <div class="p-5 overflow-y-auto custom-scrollbar flex-1">
        <div id="test-grid-cards" class="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-5 gap-3">
          <!-- Dynamically populated 1 to 100 cards -->
        </div>
      </div>

      <div class="p-4 border-t border-slate-800 bg-slate-950/50 flex items-center justify-between text-xs text-slate-400">
        <div class="flex items-center gap-3">
          <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> আনলকড / প্রস্তুত</span>
          <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-slate-700"></span> 🔒 লক করা</span>
        </div>
        <button onclick="toggleTestGridModal()" class="px-4 py-1.5 rounded-lg bg-slate-800 text-white font-semibold">বন্ধ করুন</button>
      </div>

    </div>
  </div>

  <!-- ============================================== -->
  <!-- PREMIUM BKASH PAYWALL & ENROLLMENT MODAL -->
  <!-- ============================================== -->
  <div id="bkash-paywall-modal" class="fixed inset-0 z-50 bg-slate-950/85 backdrop-blur-md hidden flex items-center justify-center p-4 transition-all duration-200">
    <div class="fixed inset-0" onclick="closeBkashPaywallModal()"></div>
    <div id="bkash-paywall-card" class="bg-gradient-to-b from-slate-900 to-slate-950 border border-pink-500/40 rounded-3xl max-w-lg w-full p-6 sm:p-7 shadow-2xl shadow-pink-950/60 relative z-10 overflow-hidden transform scale-95 opacity-0 transition-all duration-200 space-y-4">
      
      <!-- Ambient Background Accents -->
      <div class="absolute -top-20 -right-20 w-44 h-44 bg-pink-600/20 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -bottom-20 -left-20 w-44 h-44 bg-purple-600/20 rounded-full blur-3xl pointer-events-none"></div>

      <!-- Header with bKash Badge -->
      <div class="flex items-start justify-between gap-3">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-2xl bg-pink-500/20 border border-pink-500/40 text-pink-400 flex items-center justify-center text-2xl shrink-0 shadow-inner">
            📱
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h3 class="text-lg sm:text-xl font-black text-white">প্রিমিয়াম মডেল টেস্ট আনলক</h3>
              <span class="text-[10px] font-black uppercase px-2 py-0.5 rounded-full bg-pink-600 text-white shadow-sm">bKash</span>
            </div>
            <p class="text-xs text-slate-300 font-medium">প্রথম ৫টি টেস্ট ফ্রি! বাকি ৯৫টি টেস্টের জন্য ফি পরিশোধ করুন</p>
          </div>
        </div>
        <button onclick="closeBkashPaywallModal()" class="w-8 h-8 rounded-full bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700 flex items-center justify-center text-sm font-bold transition">✕</button>
      </div>

      <!-- Package Selector -->
      <div class="space-y-1.5">
        <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">প্যাকেজ নির্বাচন করুন:</div>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
          <!-- Medical Pack -->
          <div id="pkg-opt-medical" onclick="selectBkashPackage('medical')" class="cursor-pointer p-3 rounded-xl border border-pink-500 bg-pink-950/40 text-center transition">
            <div class="text-xs font-bold text-pink-300">🩺 মেডিকেল</div>
            <div class="text-base font-black text-white mt-0.5">৳৪৯৯</div>
            <div class="text-[10px] text-pink-200">৯৫টি পেইড টেস্ট</div>
          </div>
          <!-- Versity Pack -->
          <div id="pkg-opt-versity" onclick="selectBkashPackage('versity')" class="cursor-pointer p-3 rounded-xl border border-slate-700 bg-slate-900/60 text-center hover:border-slate-500 transition opacity-80">
            <div class="text-xs font-bold text-slate-300">🏛️ ভার্সিটি ও গুচ্ছ</div>
            <div class="text-base font-black text-white mt-0.5">৳৪৯৯</div>
            <div class="text-[10px] text-slate-400">৯৫টি পেইড টেস্ট</div>
          </div>
          <!-- Combo Pack -->
          <div id="pkg-opt-combo" onclick="selectBkashPackage('combo')" class="cursor-pointer p-3 rounded-xl border border-purple-500/40 bg-purple-950/30 text-center hover:border-purple-400 transition opacity-80 relative overflow-hidden">
            <span class="absolute top-0 right-0 bg-gradient-to-l from-amber-500 to-pink-500 text-slate-950 text-[9px] font-black px-1.5 py-0.2 rounded-bl">মেগা ছাড়</span>
            <div class="text-xs font-bold text-purple-300">⚡ মেগা কম্বো</div>
            <div class="text-base font-black text-white mt-0.5">৳৭৯৯</div>
            <div class="text-[10px] text-purple-200">২০০ টেস্ট (উভয়)</div>
          </div>
        </div>
      </div>

      <!-- Personal bKash Account Display & Copy Card -->
      <div class="p-3.5 rounded-2xl bg-gradient-to-r from-pink-950/60 via-slate-900 to-pink-950/60 border border-pink-500/40 flex items-center justify-between gap-3">
        <div>
          <div class="text-[11px] font-semibold text-pink-300 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-pink-400 animate-pulse"></span>
            <span>পার্সোনাল বিকাশ একাউন্ট (Send Money):</span>
          </div>
          <div id="bkash-number-text" class="text-xl sm:text-2xl font-black text-white tracking-widest mt-0.5 font-mono">01644265766</div>
        </div>
        <button id="btn-copy-bkash" onclick="copyBkashNumber()" class="px-3.5 py-2 rounded-xl bg-pink-600 hover:bg-pink-500 text-white font-bold text-xs shadow-md shadow-pink-600/30 transition flex items-center gap-1.5 shrink-0">
          <span>📋</span>
          <span id="btn-copy-bkash-text">কপি করুন</span>
        </button>
      </div>

      <!-- Send Money Instructions -->
      <div class="p-3 bg-slate-900/90 rounded-2xl border border-slate-800 space-y-1.5 text-xs text-slate-300 leading-relaxed">
        <div class="font-bold text-slate-200 flex items-center gap-1.5 text-[11px]">
          <span>💡</span> <span>ফি পরিশোধের নিয়মাবলি:</span>
        </div>
        <ol class="list-decimal list-inside space-y-1 text-slate-400 pl-1 text-[11px]">
          <li>আপনার bKash অ্যাপ ওপেন করে <strong class="text-pink-300">Send Money</strong> সিলেক্ট করুন।</li>
          <li>প্রাপক নাম্বারে <strong class="text-white font-mono">01644265766</strong> দিন এবং নির্বাচিত ফি (<span id="instruction-fee-text" class="text-white font-bold">৳৪৯৯</span>) পাঠান।</li>
          <li>টাকা পাঠানোর পর SMS-এ প্রাপ্ত <strong class="text-amber-300 font-mono">TrxID</strong> এবং আপনার বিকাশ নাম্বার নিচে দিয়ে ভেরিফাই করুন।</li>
        </ol>
      </div>

      <!-- Verification Input Form -->
      <div class="space-y-2.5">
        <div>
          <label class="block text-[11px] font-bold text-slate-300 mb-1">আপনার বিকাশ মোবাইল নাম্বার:</label>
          <input id="pay-sender-number" type="tel" placeholder="01XXXXXXXXX (যে নাম্বার থেকে পাঠিয়েছেন)" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-pink-500">
        </div>
        <div>
          <label class="block text-[11px] font-bold text-slate-300 mb-1">bKash Transaction ID (TrxID):</label>
          <input id="pay-trx-id" type="text" placeholder="যেমন: 9K27XZ89 (৮-১২ অক্ষরের TrxID)" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-pink-500 uppercase font-mono">
        </div>
        <div id="paywall-feedback-msg" class="hidden text-xs p-2.5 rounded-xl"></div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center justify-end gap-3 pt-1">
        <button onclick="closeBkashPaywallModal()" class="px-5 py-2 rounded-xl border border-slate-700 text-slate-400 hover:text-white hover:bg-slate-800 font-bold transition text-xs">
          পরে করব
        </button>
        <button id="btn-submit-payment" onclick="submitBkashPayment()" class="px-6 py-2 rounded-xl bg-gradient-to-r from-pink-600 via-rose-600 to-pink-500 hover:from-pink-500 hover:to-rose-400 text-white font-extrabold shadow-lg shadow-pink-600/30 transition text-xs sm:text-sm flex items-center gap-2">
          <span>🚀 ভেরিফাই ও আনলক করো</span>
        </button>
      </div>

    </div>
  </div>

  <!-- ============================================== -->
  <!-- USER AUTH MODAL (LOGIN / SIGN UP) -->
  <!-- ============================================== -->
  <div id="auth-modal" class="fixed inset-0 z-50 bg-slate-950/85 backdrop-blur-md hidden flex items-center justify-center p-4 transition-all duration-200">
    <div class="fixed inset-0" onclick="closeAuthModal()"></div>
    <div id="auth-modal-card" class="bg-gradient-to-b from-slate-900 to-slate-950 border border-slate-700/80 rounded-3xl max-w-md w-full p-6 sm:p-7 shadow-2xl shadow-black/90 relative z-10 overflow-hidden transform scale-95 opacity-0 transition-all duration-200 space-y-4">
      
      <!-- Top glow -->
      <div class="absolute -top-16 -right-16 w-36 h-36 bg-brand-500/20 rounded-full blur-3xl pointer-events-none"></div>

      <!-- Header -->
      <div class="flex items-start justify-between gap-3">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-2xl bg-brand-500/20 border border-brand-500/40 text-brand-300 flex items-center justify-center text-2xl shrink-0 shadow-inner">
            👤
          </div>
          <div>
            <h3 id="auth-modal-title" class="text-lg sm:text-xl font-black text-white">শিক্ষার্থী একাউন্ট</h3>
            <p class="text-xs text-slate-400">ভিন্ন ডিভাইসে আপনার প্রিমিয়াম সাবস্ক্রিপশন সিঙ্ক করুন</p>
          </div>
        </div>
        <button onclick="closeAuthModal()" class="w-8 h-8 rounded-full bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700 flex items-center justify-center text-sm font-bold transition">✕</button>
      </div>

      <!-- Auth Tab Toggle (Login / Signup) -->
      <div class="flex items-center bg-slate-950 p-1 rounded-2xl border border-slate-800 text-xs font-bold">
        <button id="auth-tab-login" onclick="switchAuthTab('login')" class="flex-1 py-2 rounded-xl bg-brand-600 text-white shadow transition">
          লগইন (Sign In)
        </button>
        <button id="auth-tab-signup" onclick="switchAuthTab('signup')" class="flex-1 py-2 rounded-xl text-slate-400 hover:text-white transition">
          নতুন একাউন্ট (Sign Up)
        </button>
      </div>

      <!-- Form Inputs -->
      <form id="auth-form" onsubmit="event.preventDefault(); handleAuthSubmit();" class="space-y-3 pt-1">
        <div id="auth-name-container" class="hidden">
          <label class="block text-[11px] font-bold text-slate-300 mb-1">আপনার নাম (ঐচ্ছিক):</label>
          <input id="auth-input-name" type="text" placeholder="যেমন: আবরার সাকিব" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-brand-500">
        </div>
        <div>
          <label class="block text-[11px] font-bold text-slate-300 mb-1">ইমেইল এড্রেস:</label>
          <input id="auth-input-email" type="email" required placeholder="name@example.com" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-brand-500">
        </div>
        <div>
          <label class="block text-[11px] font-bold text-slate-300 mb-1">পাসওয়ার্ড:</label>
          <input id="auth-input-password" type="password" required minlength="6" placeholder="কমপক্ষে ৬ অক্ষরের পাসওয়ার্ড দিন" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-brand-500">
        </div>

        <div id="auth-feedback-msg" class="hidden text-xs p-2.5 rounded-xl"></div>

        <div class="pt-2">
          <button id="btn-auth-submit" type="submit" class="w-full py-2.5 rounded-xl bg-gradient-to-r from-brand-600 to-teal-500 hover:from-brand-500 hover:to-teal-400 text-slate-950 font-black shadow-lg glow-brand transition text-xs sm:text-sm flex items-center justify-center gap-2">
            <span>লগইন করুন</span>
          </button>
        </div>
      </form>

      <p class="text-[11px] text-center text-slate-500">
        ডিভাইস পরিবর্তন না করলে বারবার লগইন করার প্রয়োজন নেই, ডেটা স্বয়ংক্রিয়ভাবে সংরক্ষিত থাকে।
      </p>

    </div>
  </div>

  <!-- ============================================== -->
  <!-- ADMIN PANEL & PAYMENT APPROVAL MODAL -->
  <!-- ============================================== -->
  <div id="admin-panel-modal" class="fixed inset-0 z-50 bg-slate-950/90 backdrop-blur-md hidden flex items-center justify-center p-3 sm:p-6 transition-all duration-200">
    <div class="fixed inset-0" onclick="closeAdminModal()"></div>
    <div id="admin-modal-card" class="bg-slate-900 border border-slate-800 rounded-3xl max-w-5xl w-full max-h-[90vh] flex flex-col shadow-2xl relative z-10 overflow-hidden transform scale-95 opacity-0 transition-all duration-200">
      
      <!-- Admin Login State (4-Step Security Gate) -->
      <div id="admin-login-view" class="p-6 sm:p-8 max-w-lg mx-auto w-full my-auto space-y-4">
        <div class="text-center space-y-1.5">
          <div class="w-14 h-14 rounded-2xl bg-brand-500/20 border border-brand-500/40 text-brand-400 flex items-center justify-center text-3xl mx-auto shadow-inner">
            🛡️
          </div>
          <div>
            <h3 class="text-lg sm:text-xl font-black text-white">অ্যাডমিন ৪-ধাপ নিরাপত্তা যাচাই</h3>
            <p class="text-xs text-slate-400">অনুমোদিত অ্যাডমিন এক্সেসের জন্য ৪টি সিকিউরিটি লেয়ার পূরণ করুন</p>
          </div>
        </div>

        <!-- 4 Step Mini Cards -->
        <div class="grid grid-cols-4 gap-2 text-center text-[10px] font-bold">
          <div class="p-1.5 rounded-xl bg-slate-950 border border-brand-500/40 text-brand-400">
            <span class="block text-xs">🔑</span>ধাপ ১: Master
          </div>
          <div class="p-1.5 rounded-xl bg-slate-950 border border-teal-500/40 text-teal-400">
            <span class="block text-xs">🛡️</span>ধাপ ২: Secondary
          </div>
          <div class="p-1.5 rounded-xl bg-slate-950 border border-purple-500/40 text-purple-400">
            <span class="block text-xs">🔢</span>ধাপ ৩: PIN
          </div>
          <div class="p-1.5 rounded-xl bg-slate-950 border border-amber-500/40 text-amber-400">
            <span class="block text-xs">🤐</span>ধাপ ৪: Secret
          </div>
        </div>

        <form onsubmit="event.preventDefault(); handleAdminLoginSubmit();" class="space-y-3 pt-1">
          <!-- Step 1: Master Password 1 -->
          <div>
            <label class="block text-[11px] font-bold text-slate-300 mb-1">
              🔑 ধাপ ১: Master Password 1
            </label>
            <input id="admin-input-master" type="password" required placeholder="Master Password 1 লিখুন..." class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-brand-500 font-mono">
          </div>

          <!-- Step 2: Secondary Password 2 -->
          <div>
            <label class="block text-[11px] font-bold text-slate-300 mb-1">
              🛡️ ধাপ ২: Secondary Password 2
            </label>
            <input id="admin-input-secondary" type="password" required placeholder="Secondary Password 2 লিখুন..." class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-brand-500 font-mono">
          </div>

          <!-- Step 3 & 4 in 2 columns -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1">
                🔢 ধাপ ৩: Security PIN
              </label>
              <input id="admin-input-pin" type="password" inputmode="numeric" required placeholder="Security PIN" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-brand-500 font-mono text-center">
            </div>

            <div>
              <label class="block text-[11px] font-bold text-slate-300 mb-1">
                🤐 ধাপ ৪: Secret Word
              </label>
              <input id="admin-input-word" type="text" required placeholder="Secret Word" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-brand-500 text-center font-mono">
            </div>
          </div>

          <div id="admin-login-feedback" class="hidden text-xs p-2.5 rounded-xl"></div>

          <button id="btn-admin-login-submit" type="submit" class="w-full py-2.5 rounded-xl bg-gradient-to-r from-brand-600 via-emerald-600 to-teal-500 hover:from-brand-500 hover:to-teal-400 text-slate-950 font-black text-xs sm:text-sm shadow-lg glow-brand transition flex items-center justify-center gap-2">
            <span>🛡️ ৪-ধাপ নিরাপত্তা যাচাই ও প্রবেশ</span>
          </button>
        </form>
      </div>

      <!-- Admin Dashboard State -->
      <div id="admin-dashboard-view" class="hidden flex flex-col flex-1 overflow-hidden">
        
        <!-- Header -->
        <div class="p-4 sm:p-5 border-b border-slate-800 flex items-center justify-between gap-3 bg-slate-950/60">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-brand-500/20 border border-brand-500/40 text-brand-400 flex items-center justify-center text-xl shrink-0">
              📊
            </div>
            <div>
              <div class="flex items-center gap-2">
                <h3 class="text-base sm:text-lg font-black text-white">অ্যাডমিন ড্যাশবোর্ড</h3>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800 font-bold">লাইভ কন্ট্রোল</span>
              </div>
              <p class="text-xs text-slate-400">পেমেন্ট রিকোয়েস্ট ও বিকাশ SMS ম্যানেজমেন্ট</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="refreshAdminData()" class="p-2 sm:px-3 sm:py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold border border-slate-700 flex items-center gap-1.5 transition">
              <span>↻</span> <span class="hidden sm:inline">রিফ্রেশ</span>
            </button>
            <button onclick="handleAdminLogout()" class="px-3 py-1.5 rounded-xl bg-rose-950/80 hover:bg-rose-900 border border-rose-800 text-rose-300 text-xs font-bold transition">
              লগআউট
            </button>
            <button onclick="closeAdminModal()" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center text-sm font-bold ml-1">✕</button>
          </div>
        </div>

        <!-- Metrics Cards -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 p-4 sm:p-5 bg-slate-950/30 border-b border-slate-800">
          <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-3 sm:p-4 shadow-inner">
            <p class="text-[11px] text-slate-400 font-semibold">মোট সংগৃহীত ফি</p>
            <p id="adm-metric-revenue" class="text-lg sm:text-2xl font-black text-emerald-400 font-mono mt-0.5">৳০</p>
          </div>
          <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-3 sm:p-4 shadow-inner">
            <p class="text-[11px] text-slate-400 font-semibold">অনুমোদিত শিক্ষার্থী</p>
            <p id="adm-metric-verified" class="text-lg sm:text-2xl font-black text-white font-mono mt-0.5">০ জন</p>
          </div>
          <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-3 sm:p-4 shadow-inner">
            <p class="text-[11px] text-amber-400 font-semibold">পেন্ডিং রিকোয়েস্ট</p>
            <p id="adm-metric-pending" class="text-lg sm:text-2xl font-black text-amber-400 font-mono mt-0.5">০ টি</p>
          </div>
          <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-3 sm:p-4 shadow-inner">
            <p class="text-[11px] text-slate-400 font-semibold">মোট সাবমিট পরীক্ষা</p>
            <p id="adm-metric-exams" class="text-lg sm:text-2xl font-black text-teal-400 font-mono mt-0.5">০ টি</p>
          </div>
        </div>

        <!-- Sub Tabs (Claims vs SMS Logs) -->
        <div class="flex items-center px-4 sm:px-5 pt-3 border-b border-slate-800 gap-2 bg-slate-900/50">
          <button id="adm-tab-claims" onclick="switchAdminTab('claims')" class="px-4 py-2 border-b-2 border-brand-500 text-brand-400 font-bold text-xs sm:text-sm flex items-center gap-1.5">
            <span>📋</span> পেমেন্ট রিকোয়েস্ট তালিকা (<span id="adm-claims-count">0</span>)
          </button>
          <button id="adm-tab-sms" onclick="switchAdminTab('sms')" class="px-4 py-2 border-b-2 border-transparent text-slate-400 hover:text-slate-300 font-bold text-xs sm:text-sm flex items-center gap-1.5">
            <span>📱</span> বিকাশ SMS লগ (<span id="adm-sms-count">0</span>)
          </button>
        </div>

        <!-- Table Container -->
        <div class="flex-1 overflow-y-auto custom-scrollbar p-4 sm:p-5">
          <!-- Claims Table -->
          <div id="adm-claims-container" class="space-y-3">
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead>
                  <tr class="text-slate-400 border-b border-slate-800 text-[11px] uppercase tracking-wider">
                    <th class="pb-3 pr-2">তারিখ ও সময়</th>
                    <th class="pb-3 px-2">শিক্ষার্থী / ইমেইল</th>
                    <th class="pb-3 px-2">বিকাশ নাম্বার</th>
                    <th class="pb-3 px-2">প্যাকেজ ও ফি</th>
                    <th class="pb-3 px-2">TrxID</th>
                    <th class="pb-3 px-2">স্ট্যাটাস</th>
                    <th class="pb-3 pl-2 text-right">পদক্ষেপ (Action)</th>
                  </tr>
                </thead>
                <tbody id="adm-claims-tbody" class="divide-y divide-slate-800/60 font-medium">
                  <!-- Populated dynamically -->
                </tbody>
              </table>
            </div>
            <div id="adm-claims-empty" class="hidden text-center py-10 text-slate-500 text-xs">
              কোনো পেমেন্ট রিকোয়েস্ট পাওয়া যায়নি।
            </div>
          </div>

          <!-- SMS Logs Table -->
          <div id="adm-sms-container" class="hidden space-y-3">
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead>
                  <tr class="text-slate-400 border-b border-slate-800 text-[11px] uppercase tracking-wider">
                    <th class="pb-3 pr-2">সময়</th>
                    <th class="pb-3 px-2">প্রেরক নাম্বার</th>
                    <th class="pb-3 px-2">পরিমাণ</th>
                    <th class="pb-3 px-2">TrxID</th>
                    <th class="pb-3 px-2">ম্যাচিং স্ট্যাটাস</th>
                    <th class="pb-3 pl-2">মূল SMS বার্তা</th>
                  </tr>
                </thead>
                <tbody id="adm-sms-tbody" class="divide-y divide-slate-800/60 font-mono text-[11px]">
                  <!-- Populated dynamically -->
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </div>

    </div>
  </div>

  <!-- ============================================== -->
  <!-- PREMIUM CUSTOM ACTION & CONFIRMATION MODAL -->
  <!-- (Replaces all browser native alert/confirm popups) -->
  <!-- ============================================== -->
  <div id="app-action-modal" class="fixed inset-0 z-50 bg-slate-950/85 backdrop-blur-md hidden flex items-center justify-center p-4 transition-all duration-200">
    <div class="fixed inset-0" onclick="closeCustomModal(false)"></div>
    <div id="app-action-modal-card" class="bg-gradient-to-b from-slate-900 to-slate-950 border border-slate-700/80 rounded-3xl max-w-md w-full p-6 sm:p-7 shadow-2xl shadow-black/90 relative z-10 overflow-hidden transform scale-95 opacity-0 transition-all duration-200 space-y-5">
      
      <!-- Ambient Glow Behind Icon -->
      <div id="app-action-modal-glow" class="absolute -top-16 -left-16 w-36 h-36 bg-emerald-500/20 rounded-full blur-3xl pointer-events-none"></div>

      <!-- Icon & Header -->
      <div class="flex items-start gap-4">
        <div id="app-action-modal-icon-container" class="w-14 h-14 rounded-2xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 flex items-center justify-center text-2xl shrink-0 shadow-inner">
          <span id="app-action-modal-icon">📝</span>
        </div>
        <div class="space-y-1">
          <h3 id="app-action-modal-title" class="text-lg sm:text-xl font-black text-white tracking-tight">
            উত্তরপত্র সাবমিট নিশ্চিতকরণ
          </h3>
          <p id="app-action-modal-subtitle" class="text-xs sm:text-sm text-slate-400 font-medium leading-relaxed">
            আপনি কি উত্তরপত্র সাবমিট করতে নিশ্চিত?
          </p>
        </div>
      </div>

      <!-- Custom Dynamic Details Body -->
      <div id="app-action-modal-details" class="space-y-3">
        <!-- Injected dynamically -->
      </div>

      <!-- Action Buttons -->
      <div id="app-action-modal-actions" class="flex items-center justify-end gap-3 pt-2">
        <button id="app-action-modal-btn-cancel" onclick="closeCustomModal(false)" class="px-5 py-2.5 rounded-xl border border-slate-700 text-slate-300 hover:text-white hover:bg-slate-800 font-bold transition text-xs sm:text-sm">
          বাতিল করো
        </button>
        <button id="app-action-modal-btn-confirm" onclick="closeCustomModal(true)" class="px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white font-extrabold shadow-lg shadow-emerald-500/25 transition text-xs sm:text-sm flex items-center gap-2">
          <span>হ্যাঁ, সাবমিট করো</span>
        </button>
      </div>

    </div>
  </div>

  <!-- ============================================== -->
  <!-- FOOTER -->
  <!-- ============================================== -->
  <footer class="bg-slate-900 border-t border-slate-800 py-8 mt-12 text-slate-400 text-xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4 text-center md:text-left">
      <div class="flex items-center gap-2.5 justify-center md:justify-start">
        <div class="w-6 h-6 rounded-lg bg-brand-600 text-slate-950 font-black text-xs flex items-center justify-center">A</div>
        <span class="font-bold text-white">ADMISSION TEST BD</span>
        <span>•</span>
        <span>বাংলাদেশ এডমিশন টেস্ট পোর্টাল ২০২৫-২০২৬</span>
      </div>
      <div>
        প্রস্তুতকৃত: ড. মোহাম্মদ আবুল হাসান, গাজী আজমল, হাজারী ও নাগ, শাহজাহান তপন ও এস ইউ আহাম্মদের পাঠ্যবই নির্দেশিকা অনুসারে।
      </div>
    </div>
  </footer>

  <!-- ============================================== -->
  <!-- CORE JAVASCRIPT APPLICATION LOGIC -->
  <!-- ============================================== -->
  <script>
    const DEFAULT_MED_TEST_1 = __DEFAULT_MED_TEST_1__;
    const DEFAULT_VAR_TEST_1 = __DEFAULT_VAR_TEST_1__;

    const appState = {
      currentStream: 'medical',       // 'medical', 'versity', 'past_15years', 'textbooks', 'nocalc', 'engineering'
      currentTestId: 1,              // 1 to 100
      selectedSession: localStorage.getItem('admission_selected_session') || '2025-26',
      unlockedMed: parseInt(localStorage.getItem('admission_unlocked_med') || '1'),
      unlockedVar: parseInt(localStorage.getItem('admission_unlocked_var') || '1'),
      studentId: localStorage.getItem('admission_student_id') || ('stu_' + Math.random().toString(36).substring(2, 10)),
      
      // Loaded data stores
      medicalTests: [DEFAULT_MED_TEST_1],
      versityTests: [DEFAULT_VAR_TEST_1],
      past15YearsData: { medical: [], versity: [] },
      pastSubStream: 'medical', // 'medical' or 'versity'
      textbookKb: [],
      nocalcTricks: [],

      // Active test runtime
      currentTestObj: DEFAULT_MED_TEST_1,
      examStatus: 'ready',            // 'ready', 'running', 'submitted'
      userAnswers: {},               // { qIndex: optIndex }
      timerSecondsRemaining: 3600,
      timerInterval: null,
      examStartTime: null,

      // Past 15 years state
      activePastYear: '2024-2025',
      pastShowAnswers: false,

      // Textbook KB pagination
      kbSearchQuery: '',
      kbSelectedSubject: 'All',
      kbCurrentPage: 1,
      kbPageSize: 24,

      chartInstance: null,

      // Payment & Enrollment State (Personal bKash Automation)
      isMedicalPaid: localStorage.getItem('admission_paid_med') === 'true',
      isVersityPaid: localStorage.getItem('admission_paid_var') === 'true',
      pendingUnlockTestId: null,

      // User Authentication State
      userToken: localStorage.getItem('admission_user_token') || null,
      userEmail: localStorage.getItem('admission_user_email') || null,
      userName: localStorage.getItem('admission_user_name') || null
    };

    localStorage.setItem('admission_student_id', appState.studentId);

    // ============================================
    // INITIALIZATION & DATA FETCHING
    // ============================================
    function initApp() {
      // Guard: Cap free progression to Test 5 if student has not enrolled/paid
      if (!appState.isMedicalPaid && appState.unlockedMed > 5) {
        appState.unlockedMed = 5;
        localStorage.setItem('admission_unlocked_med', '5');
      }
      if (!appState.isVersityPaid && appState.unlockedVar > 5) {
        appState.unlockedVar = 5;
        localStorage.setItem('admission_unlocked_var', '5');
      }
      if (appState.currentTestId > 5 && !isStreamPaid(appState.currentStream)) {
        appState.currentTestId = 1;
      }

      updateAuthUI();

      // Session state restoration (device resilience)
      const sessionRestored = restoreSessionState();

      const seasonSel = document.getElementById('season-selector');
      if (seasonSel) seasonSel.value = appState.selectedSession;

      updateUnlockedBadges();
      populateTestDropdown();

      if (!sessionRestored || !sessionRestored.shouldResume) {
        if (appState.currentStream === 'medical' || appState.currentStream === 'versity') {
          loadCurrentSelectedTest();
        } else {
          switchStream(appState.currentStream);
        }
      }

      loadAllPlatformData().then(() => {
        if (sessionRestored && sessionRestored.shouldResume) {
          resumeActiveExam();
        }
      });

      syncPaymentStatus();

      // Listeners for seamless session saving
      window.addEventListener('beforeunload', saveSessionState);
      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') saveSessionState();
      });

      // Admin hash listener
      window.addEventListener('hashchange', () => {
        if (window.location.hash === '#admin') openAdminModal();
      });
      if (window.location.hash === '#admin') {
        openAdminModal();
      }
    }

    async function syncPaymentStatus() {
      try {
        const res = await fetch(`/api/payment/status?student_id=${appState.studentId}`);
        if (res.ok) {
          const data = await res.json();
          if (data.medical_enrolled) {
            appState.isMedicalPaid = true;
            localStorage.setItem('admission_paid_med', 'true');
          }
          if (data.versity_enrolled) {
            appState.isVersityPaid = true;
            localStorage.setItem('admission_paid_var', 'true');
          }
          updateUnlockedBadges();
          populateTestDropdown();
          if (typeof renderTestGridModal === 'function') {
            const gridModal = document.getElementById('grid-modal');
            if (gridModal && !gridModal.classList.contains('hidden')) renderTestGridModal();
          }
        }
      } catch (e) {
        console.warn('Payment status sync offline, using local cache.');
      }
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initApp);
    } else {
      initApp();
    }

    async function loadAllPlatformData() {
      // 1. Fetch Medical tests first for immediate UI readiness
      try {
        const medRes = await fetch('/data/medical_100_tests.json');
        appState.medicalTests = await medRes.json();
        populateTestDropdown();
        loadCurrentSelectedTest();
      } catch (err) {
        console.warn("Medical tests load error:", err);
      }

      // 2. Fetch remaining data progressively in background without blocking
      fetch('/data/versity_100_tests.json')
        .then(r => r.json())
        .then(data => {
          appState.versityTests = data;
          if (appState.currentStream === 'versity') {
            populateTestDropdown();
            loadCurrentSelectedTest();
          }
        })
        .catch(e => console.warn("Varsity data error:", e));

      fetch('/data/past_15years_tests.json')
        .then(r => r.json())
        .then(data => {
          if (data && (data.medical || data.versity)) {
            appState.past15YearsData = data;
          } else if (Array.isArray(data)) {
            appState.past15YearsData = { medical: data, versity: [] };
          }
          populatePastYearSelect();
          if (appState.currentStream === 'past_15years') renderPastYearView();
        })
        .catch(e => console.warn("Past 15 years error:", e));

      fetch('/data/nocalc_tricks_kb.json')
        .then(r => r.json())
        .then(data => {
          appState.nocalcTricks = data;
          renderNocalcTricks();
        })
        .catch(e => console.warn("Tricks error:", e));

      fetch('/data/medical_textbooks_kb.json')
        .then(r => r.json())
        .then(data => {
          appState.textbookKb = data;
          if (appState.currentStream === 'textbooks') renderKbFacts();
        })
        .catch(e => console.warn("Textbooks error:", e));
    }

    // ============================================
    // ADMISSION SESSION MANAGEMENT
    // ============================================
    function changeAdmissionSession(newSession) {
      appState.selectedSession = newSession;
      localStorage.setItem('admission_selected_session', newSession);
      
      const badge = document.getElementById('start-badge-session');
      if (badge) badge.innerText = `সেশন: ${newSession}`;

      showToast(`ভর্তি সেশন '${newSession}' নির্বাচিত হয়েছে। মেধা তালিকা এতে রেকর্ড হবে।`, "success");
    }

    function updateUnlockedBadges() {
      const medBadge = document.getElementById('med-unlocked-badge');
      if (medBadge) {
        if (appState.isMedicalPaid) {
          medBadge.innerHTML = `🩺 মেডিকেল: 👑 প্রিমিয়াম (টেস্ট ০${appState.unlockedMed})`;
          medBadge.className = "text-xs font-bold px-3 py-1 rounded-full bg-emerald-950/80 text-emerald-300 border border-emerald-800 shadow-sm";
        } else {
          medBadge.innerHTML = `🩺 মেডিকেল: ফ্রি ট্রায়াল (০${Math.min(5, appState.unlockedMed)}/৫)`;
          medBadge.className = "text-xs font-bold px-3 py-1 rounded-full bg-brand-950/80 text-brand-300 border border-brand-800 shadow-sm";
        }
      }

      const varBadge = document.getElementById('var-unlocked-badge');
      if (varBadge) {
        if (appState.isVersityPaid) {
          varBadge.innerHTML = `🏛️ ভার্সিটি: 👑 প্রিমিয়াম (টেস্ট ০${appState.unlockedVar})`;
          varBadge.className = "text-xs font-bold px-3 py-1 rounded-full bg-teal-950/80 text-teal-300 border border-teal-800 shadow-sm";
        } else {
          varBadge.innerHTML = `🏛️ ভার্সিটি: ফ্রি ট্রায়াল (০${Math.min(5, appState.unlockedVar)}/৫)`;
          varBadge.className = "text-xs font-bold px-3 py-1 rounded-full bg-blue-950/80 text-blue-300 border border-blue-800 shadow-sm";
        }
      }

      const paywallBtn = document.getElementById('btn-open-paywall');
      if (paywallBtn) {
        const stream = appState.currentStream;
        const isPaid = (stream === 'medical') ? appState.isMedicalPaid : ((stream === 'versity') ? appState.isVersityPaid : true);
        if (isPaid && (stream === 'medical' || stream === 'versity')) {
          paywallBtn.className = "px-3.5 py-2 rounded-xl bg-emerald-950/80 border border-emerald-500/60 text-emerald-300 font-bold text-xs flex items-center gap-1.5 transition";
          paywallBtn.innerHTML = `<span>👑 প্রিমিয়াম অ্যাক্টিভ</span><span class="text-[10px] bg-emerald-500/20 px-1.5 py-0.5 rounded text-emerald-200">✓</span>`;
        } else {
          paywallBtn.className = "px-3.5 py-2 rounded-xl bg-gradient-to-r from-pink-600 via-rose-600 to-pink-500 hover:from-pink-500 hover:to-rose-400 text-white font-bold text-xs shadow-lg shadow-pink-500/25 flex items-center gap-1.5 transition animate-pulse";
          paywallBtn.innerHTML = `<span>👑 প্রিমিয়াম আনলক</span><span class="bg-black/30 px-1.5 py-0.5 rounded text-[10px]">৳৪৯৯</span>`;
        }
      }
    }

    // ============================================
    // STREAM SWITCHER (Medical -> Varsity -> Past 15 -> Textbooks -> Tricks -> Engineering)
    // ============================================
    function switchStream(stream) {
      appState.currentStream = stream;

      // Update Nav Button Styles
      const navButtons = [
        { id: 'nav-btn-medical', stream: 'medical' },
        { id: 'nav-btn-versity', stream: 'versity' },
        { id: 'nav-btn-past', stream: 'past_15years' },
        { id: 'nav-btn-kb', stream: 'textbooks' },
        { id: 'nav-btn-nocalc', stream: 'nocalc' },
        { id: 'nav-btn-engineering', stream: 'engineering' }
      ];

      navButtons.forEach(btn => {
        const el = document.getElementById(btn.id);
        if (!el) return;
        if (btn.stream === stream) {
          el.className = "px-3.5 py-2 rounded-xl transition flex items-center gap-2 whitespace-nowrap bg-brand-600 text-white shadow-md font-bold";
        } else {
          el.className = "px-3.5 py-2 rounded-xl transition flex items-center gap-2 whitespace-nowrap text-slate-300 hover:text-white hover:bg-slate-800/80";
        }
      });

      // Hide all views
      ['view-model-tests', 'view-past-15years', 'view-textbooks-kb', 'view-nocalc', 'view-engineering'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.add('hidden');
      });

      // Show selected view
      if (stream === 'medical' || stream === 'versity') {
        document.getElementById('view-model-tests').classList.remove('hidden');
        updateStreamHeadings();
        populateTestDropdown();
        loadCurrentSelectedTest();
      } else if (stream === 'past_15years') {
        document.getElementById('view-past-15years').classList.remove('hidden');
        renderPastYearView();
      } else if (stream === 'textbooks') {
        document.getElementById('view-textbooks-kb').classList.remove('hidden');
        renderKbFacts();
      } else if (stream === 'nocalc') {
        document.getElementById('view-nocalc').classList.remove('hidden');
      } else if (stream === 'engineering') {
        document.getElementById('view-engineering').classList.remove('hidden');
      }

      window.scrollTo({ top: 0, behavior: 'smooth' });
      saveSessionState();
    }

    function updateStreamHeadings() {
      const heading = document.getElementById('current-stream-heading');
      const heroTitle = document.getElementById('hero-title');
      const startBadge = document.getElementById('start-badge-stream');
      const f4 = document.getElementById('q-filter-subj4');

      if (appState.currentStream === 'medical') {
        heading.innerText = "মেডিকেল পূর্ণাঙ্গ মডেল টেস্ট নির্বাচন";
        heroTitle.innerHTML = 'মেডিকেল <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 via-emerald-300 to-teal-200">১০০ মডেল টেস্ট সিরিজ</span>';
        if (startBadge) startBadge.innerText = "মেডিকেল পূর্ণাঙ্গ মডেল টেস্ট";
        if (f4) {
          f4.innerText = "ইংরেজি ও জিকে";
          f4.onclick = function() { filterQuestionsBySubject('English_GK', this); };
        }
      } else {
        heading.innerText = "ভার্সিটি ও সমন্বিত গুচ্ছ বিজ্ঞান ১০০ মডেল টেস্ট নির্বাচন";
        heroTitle.innerHTML = 'ভার্সিটি ও সমন্বিত গুচ্ছ <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-teal-300 to-emerald-200">১০০ মডেল টেস্ট সিরিজ (DU • GST • Agri)</span>';
        if (startBadge) startBadge.innerText = "ভার্সিটি ও গুচ্ছ বিজ্ঞান মডেল টেস্ট";
        if (f4) {
          f4.innerText = "উচ্চতর গণিত";
          f4.onclick = function() { filterQuestionsBySubject('HigherMath', this); };
        }
      }
    }

    // ============================================
    // STREAM PAYMENT & SEQUENTIAL LOCK VERIFICATION
    // (Tests 1-5 are 100% Free; Tests 6-100 require 499 BDT)
    // ============================================
    function isStreamPaid(stream) {
      if (stream === 'medical') return appState.isMedicalPaid;
      if (stream === 'versity') return appState.isVersityPaid;
      return true;
    }

    function isTestUnlocked(stream, testId) {
      if (stream === 'past_15years') return true; // Past 15 years never locked
      
      // Tests 1 to 5 are 100% Free
      if (testId <= 5) {
        if (stream === 'medical') return testId <= appState.unlockedMed;
        if (stream === 'versity') return testId <= appState.unlockedVar;
      }

      // Tests 6 to 100 require 499 BDT Enrollment
      const paid = isStreamPaid(stream);
      if (!paid) return false;

      if (stream === 'medical') return testId <= appState.unlockedMed;
      if (stream === 'versity') return testId <= appState.unlockedVar;
      return false;
    }

    function populateTestDropdown() {
      const dropdown = document.getElementById('model-test-dropdown');
      if (!dropdown) return;
      dropdown.innerHTML = '';

      const maxTest = 100;
      const stream = appState.currentStream;
      const paid = isStreamPaid(stream);

      for (let i = 1; i <= maxTest; i++) {
        const opt = document.createElement('option');
        opt.value = i;
        const unlocked = isTestUnlocked(stream, i);
        const isFree = i <= 5;

        let label = `টেস্ট ${i < 10 ? '০' + i : i} `;
        if (unlocked) {
          label += isFree ? '✓ [ফ্রি]' : '✓ [প্রিমিয়াম]';
        } else {
          if (!isFree && !paid) {
            label += '🔒 [প্রিমিয়াম - ৳৪৯৯]';
          } else {
            label += '🔒 [লক করা]';
          }
        }

        opt.text = label;
        dropdown.appendChild(opt);
      }
      dropdown.value = appState.currentTestId;
    }

    function onTestDropdownChange(testId) {
      const unlocked = isTestUnlocked(appState.currentStream, testId);
      if (!unlocked) {
        if (testId > 5 && !isStreamPaid(appState.currentStream)) {
          openBkashPaywallModal(appState.currentStream, testId);
        } else {
          showLockedModal(testId);
        }
        // Reset dropdown back to current test
        document.getElementById('model-test-dropdown').value = appState.currentTestId;
        return;
      }
      appState.currentTestId = testId;
      loadCurrentSelectedTest();
    }

    // ============================================
    // CUSTOM ACTION / CONFIRMATION MODAL SYSTEM
    // (Replaces native browser alert/confirm popups)
    // ============================================
    let customModalCallback = null;

    function openCustomModal({ title, subtitle, icon, iconTheme = 'emerald', detailsHtml, confirmText = 'নিশ্চিত করুন', cancelText = 'বাতিল', showCancel = true, onConfirm = null }) {
      customModalCallback = onConfirm;

      const modal = document.getElementById('app-action-modal');
      const card = document.getElementById('app-action-modal-card');
      const iconEl = document.getElementById('app-action-modal-icon');
      const iconContainer = document.getElementById('app-action-modal-icon-container');
      const glowEl = document.getElementById('app-action-modal-glow');
      const titleEl = document.getElementById('app-action-modal-title');
      const subtitleEl = document.getElementById('app-action-modal-subtitle');
      const detailsEl = document.getElementById('app-action-modal-details');
      const btnCancel = document.getElementById('app-action-modal-btn-cancel');
      const btnConfirm = document.getElementById('app-action-modal-btn-confirm');

      if (!modal) return;

      iconEl.innerText = icon || '📝';
      titleEl.innerText = title || '';
      subtitleEl.innerText = subtitle || '';
      
      if (detailsHtml) {
        detailsEl.innerHTML = detailsHtml;
        detailsEl.classList.remove('hidden');
      } else {
        detailsEl.classList.add('hidden');
      }

      // Configure Theme Colors
      iconContainer.className = 'w-14 h-14 rounded-2xl flex items-center justify-center text-2xl shrink-0 shadow-inner ';
      glowEl.className = 'absolute -top-16 -left-16 w-36 h-36 rounded-full blur-3xl pointer-events-none ';
      btnConfirm.className = 'px-6 py-2.5 rounded-xl text-white font-extrabold shadow-lg transition text-xs sm:text-sm flex items-center gap-2 ';

      if (iconTheme === 'emerald') {
        iconContainer.classList.add('bg-emerald-500/20', 'border', 'border-emerald-500/40', 'text-emerald-300');
        glowEl.classList.add('bg-emerald-500/20');
        btnConfirm.classList.add('bg-gradient-to-r', 'from-emerald-500', 'to-teal-600', 'hover:from-emerald-400', 'hover:to-teal-500', 'shadow-emerald-500/25');
      } else if (iconTheme === 'amber') {
        iconContainer.classList.add('bg-amber-500/20', 'border', 'border-amber-500/40', 'text-amber-300');
        glowEl.classList.add('bg-amber-500/20');
        btnConfirm.classList.add('bg-gradient-to-r', 'from-amber-500', 'to-orange-600', 'hover:from-amber-400', 'hover:to-orange-500', 'shadow-amber-500/25');
      } else if (iconTheme === 'rose') {
        iconContainer.classList.add('bg-rose-500/20', 'border', 'border-rose-500/40', 'text-rose-300');
        glowEl.classList.add('bg-rose-500/20');
        btnConfirm.classList.add('bg-gradient-to-r', 'from-rose-500', 'to-red-600', 'hover:from-rose-400', 'hover:to-red-500', 'shadow-rose-500/25');
      } else {
        iconContainer.classList.add('bg-blue-500/20', 'border', 'border-blue-500/40', 'text-blue-300');
        glowEl.classList.add('bg-blue-500/20');
        btnConfirm.classList.add('bg-gradient-to-r', 'from-blue-500', 'to-indigo-600', 'hover:from-blue-400', 'hover:to-indigo-500', 'shadow-blue-500/25');
      }

      btnConfirm.innerHTML = `<span>${confirmText}</span>`;
      if (showCancel) {
        btnCancel.innerText = cancelText;
        btnCancel.classList.remove('hidden');
      } else {
        btnCancel.classList.add('hidden');
      }

      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        card.classList.remove('scale-95', 'opacity-0');
        card.classList.add('scale-100', 'opacity-100');
      });
    }

    function closeCustomModal(confirmed) {
      const modal = document.getElementById('app-action-modal');
      const card = document.getElementById('app-action-modal-card');
      if (!modal || modal.classList.contains('hidden')) return;

      if (card) {
        card.classList.remove('scale-100', 'opacity-100');
        card.classList.add('scale-95', 'opacity-0');
      }

      setTimeout(() => {
        modal.classList.add('hidden');
        if (confirmed && typeof customModalCallback === 'function') {
          const cb = customModalCallback;
          customModalCallback = null;
          cb();
        } else {
          customModalCallback = null;
        }
      }, 150);
    }

    // Keyboard accessibility: ESC key closes modal
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeCustomModal(false);
      }
    });

    function showLockedModal(testId) {
      const prevTest = testId - 1;
      openCustomModal({
        title: `টেস্ট #${testId} লক করা আছে`,
        subtitle: "ধারাবাহিক পরীক্ষা আনলক নীতি (Sequential Progression)",
        icon: "🔒",
        iconTheme: "amber",
        detailsHtml: `
          <div class="space-y-3 text-xs leading-relaxed text-slate-300">
            <div class="p-3 bg-amber-950/50 border border-amber-800/60 rounded-2xl text-amber-200">
              সিস্টেম নিয়মানুযায়ী, টেস্ট #${testId} আনলক করতে অনুগ্রহ করে পূর্ববর্তী <strong class="text-white underline underline-offset-2">টেস্ট #${prevTest}</strong> সম্পন্ন ও সাবমিট করুন।
            </div>
            <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 text-slate-400 text-[11px] flex items-start gap-2">
              <span class="text-amber-400 text-sm">💡</span>
              <span>পূর্ববর্তী টেস্টে অংশ নিয়ে ফলাফল সাবমিট করা মাত্রই স্বয়ংক্রিয়ভাবে পরবর্তী সকল টেস্ট ধারাবাহিকভাবে আনলক হয়ে যাবে।</span>
            </div>
          </div>
        `,
        confirmText: "বুঝেছি (Understood)",
        showCancel: false
      });
    }

    // ============================================
    // PERSONAL BKASH PAYWALL & ENROLLMENT CONTROLLER
    // ============================================
    let selectedBkashPackage = 'medical';

    function openBkashPaywallModal(stream = 'medical', targetTestId = null) {
      if (targetTestId) {
        appState.pendingUnlockTestId = targetTestId;
      }
      if (stream === 'combo') {
        selectBkashPackage('combo');
      } else if (stream === 'versity') {
        selectBkashPackage('versity');
      } else {
        selectBkashPackage('medical');
      }

      const modal = document.getElementById('bkash-paywall-modal');
      const card = document.getElementById('bkash-paywall-card');
      const feedback = document.getElementById('paywall-feedback-msg');
      if (feedback) feedback.classList.add('hidden');

      if (!modal) return;
      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        if (card) {
          card.classList.remove('scale-95', 'opacity-0');
          card.classList.add('scale-100', 'opacity-100');
        }
      });
    }

    function closeBkashPaywallModal() {
      const modal = document.getElementById('bkash-paywall-modal');
      const card = document.getElementById('bkash-paywall-card');
      if (!modal || modal.classList.contains('hidden')) return;

      if (card) {
        card.classList.remove('scale-100', 'opacity-100');
        card.classList.add('scale-95', 'opacity-0');
      }
      setTimeout(() => {
        modal.classList.add('hidden');
      }, 150);
    }

    function selectBkashPackage(pkg) {
      selectedBkashPackage = pkg;
      const optMed = document.getElementById('pkg-opt-medical');
      const optVar = document.getElementById('pkg-opt-versity');
      const optCombo = document.getElementById('pkg-opt-combo');
      const feeText = document.getElementById('instruction-fee-text');

      [optMed, optVar, optCombo].forEach(el => {
        if (el) {
          el.className = "cursor-pointer p-3 rounded-xl border border-slate-700 bg-slate-900/60 text-center hover:border-slate-500 transition opacity-80";
        }
      });

      if (pkg === 'medical') {
        if (optMed) optMed.className = "cursor-pointer p-3 rounded-xl border border-pink-500 bg-pink-950/40 text-center transition ring-1 ring-pink-500";
        if (feeText) feeText.innerText = "৳৪৯৯";
      } else if (pkg === 'versity') {
        if (optVar) optVar.className = "cursor-pointer p-3 rounded-xl border border-teal-500 bg-teal-950/40 text-center transition ring-1 ring-teal-500";
        if (feeText) feeText.innerText = "৳৪৯৯";
      } else if (pkg === 'combo') {
        if (optCombo) optCombo.className = "cursor-pointer p-3 rounded-xl border border-purple-500 bg-purple-950/50 text-center transition ring-1 ring-purple-500 relative overflow-hidden";
        if (feeText) feeText.innerText = "৳৭৯৯";
      }
    }

    function copyBkashNumber() {
      const num = "01644265766";
      navigator.clipboard.writeText(num).then(() => {
        const textEl = document.getElementById('btn-copy-bkash-text');
        if (textEl) {
          textEl.innerText = "✓ কপি হয়েছে!";
          setTimeout(() => { textEl.innerText = "কপি করুন"; }, 2500);
        }
        showToast("বিকাশ নাম্বার '01644265766' ক্লিপবোর্ডে কপি করা হয়েছে।", "success");
      }).catch(() => {
        showToast("বিকাশ নাম্বার: 01644265766", "info");
      });
    }

    async function submitBkashPayment() {
      const senderNumber = document.getElementById('pay-sender-number').value.trim();
      const trxId = document.getElementById('pay-trx-id').value.trim().toUpperCase();
      const feedback = document.getElementById('paywall-feedback-msg');
      const btn = document.getElementById('btn-submit-payment');

      if (!trxId || trxId.length < 6) {
        if (feedback) {
          feedback.className = "text-xs p-3 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-200 block";
          feedback.innerText = "⚠️ অনুগ্রহ করে SMS-এ প্রাপ্ত সঠিক ও পূর্ণাঙ্গ TrxID লিখুন (কমপক্ষে ৬-১২ ডিজিট/অক্ষর)।";
        }
        return;
      }

      btn.disabled = true;
      btn.innerHTML = `<span class="inline-block animate-spin mr-1">↻</span> ভেরিফিকেশন চলছে...`;

      try {
        const res = await fetch('/api/payment/verify-trx', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            student_id: appState.studentId,
            student_name: appState.userName || 'পরীক্ষার্থী',
            student_email: appState.userEmail || '',
            package: selectedBkashPackage,
            sender_number: senderNumber || '01644265766',
            trx_id: trxId
          })
        });
        const result = await res.json();

        if (res.ok && (result.success || result.pending)) {
          if (result.success) {
            if (selectedBkashPackage === 'combo') {
              appState.isMedicalPaid = true;
              appState.isVersityPaid = true;
              localStorage.setItem('admission_paid_med', 'true');
              localStorage.setItem('admission_paid_var', 'true');
            } else if (selectedBkashPackage === 'medical') {
              appState.isMedicalPaid = true;
              localStorage.setItem('admission_paid_med', 'true');
            } else if (selectedBkashPackage === 'versity') {
              appState.isVersityPaid = true;
              localStorage.setItem('admission_paid_var', 'true');
            }

            if (feedback) {
              feedback.className = "text-xs p-3 rounded-xl bg-emerald-950/80 border border-emerald-800 text-emerald-200 block";
              feedback.innerText = result.message || "অভিনন্দন! আপনার পেমেন্ট সফলভাবে ভেরিফাই হয়েছে।";
            }

            showToast("🎉 অভিনন্দন! ৯৫টি প্রিমিয়াম মডেল টেস্ট আনলক হয়েছে।", "success");
            updateUnlockedBadges();
            populateTestDropdown();
            if (typeof renderTestGridModal === 'function') {
              const gridModal = document.getElementById('grid-modal');
              if (gridModal && !gridModal.classList.contains('hidden')) renderTestGridModal();
            }

            setTimeout(() => {
              closeBkashPaywallModal();
              if (appState.pendingUnlockTestId) {
                const target = appState.pendingUnlockTestId;
                appState.pendingUnlockTestId = null;
                appState.currentTestId = target;
                document.getElementById('model-test-dropdown').value = target;
                loadCurrentSelectedTest();
              }
            }, 1500);
          } else if (result.pending) {
            if (feedback) {
              feedback.className = "text-xs p-3 rounded-xl bg-amber-950/80 border border-amber-800 text-amber-200 block";
              feedback.innerHTML = `⏳ <strong>পেমেন্ট রিকোয়েস্ট গৃহীত হয়েছে!</strong><br><span class="text-[11px]">${result.message || 'অ্যাডমিন অনুমোদন করলেই টেস্ট স্বয়ংক্রিয়ভাবে আনলক হয়ে যাবে।'}</span>`;
            }
            showToast("পেমেন্ট রিকোয়েস্ট সংরক্ষিত হয়েছে। অ্যাডমিন অনুমোদন করলে আনলক হবে।", "info");
            setTimeout(() => {
              closeBkashPaywallModal();
            }, 2500);
          }
        } else {
          if (feedback) {
            feedback.className = "text-xs p-3 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-200 block";
            feedback.innerText = result.message || "পেমেন্ট ভেরিফিকেশন ব্যর্থ হয়েছে। TrxID সঠিক আছে কিনা যাচাই করুন।";
          }
        }
      } catch (err) {
        if (feedback) {
          feedback.className = "text-xs p-3 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-200 block";
          feedback.innerText = "সার্ভার সংযোগে সমস্যা। অনুগ্রহ করে কিছুক্ষণ পর আবার চেষ্টা করুন।";
        }
      } finally {
        btn.disabled = false;
        btn.innerHTML = `<span>🚀 ভেরিফাই ও আনলক করো</span>`;
      }
    }

    // ============================================
    // LOAD SELECTED TEST DETAILS (Shows Start Card)
    // ============================================
    function loadCurrentSelectedTest() {
      // Stop any existing timer
      if (appState.timerInterval) clearInterval(appState.timerInterval);

      const stream = appState.currentStream;
      const testId = appState.currentTestId;
      const tests = (stream === 'medical') ? appState.medicalTests : appState.versityTests;
      let current = null;
      if (tests && tests.length > 0) {
        current = tests.find(t => t.test_id === testId) || tests[0];
      }
      if (!current) {
        current = (stream === 'medical') ? DEFAULT_MED_TEST_1 : DEFAULT_VAR_TEST_1;
      }
      appState.currentTestObj = current;
      appState.examStatus = 'ready';
      appState.userAnswers = {};

      // Check if current test is unlocked
      const unlocked = isTestUnlocked(stream, testId);
      const isPaid = isStreamPaid(stream);
      const startBtn = document.getElementById('btn-start-exam');

      if (startBtn) {
        if (!unlocked && testId > 5 && !isPaid) {
          startBtn.className = "w-full sm:w-auto px-10 py-4 rounded-2xl bg-gradient-to-r from-pink-600 via-rose-600 to-pink-500 hover:from-pink-500 hover:to-rose-400 text-white font-black text-base sm:text-lg shadow-xl shadow-pink-500/30 transition transform hover:-translate-y-0.5 active:translate-y-0 flex items-center justify-center gap-2 mx-auto animate-pulse";
          startBtn.innerHTML = `<span>👑 বিকাশ দিয়ে টেস্ট ${testId < 10 ? '০' + testId : testId} আনলক করুন (৳৪৯৯)</span>`;
          startBtn.onclick = () => openBkashPaywallModal(stream, testId);
        } else if (!unlocked) {
          startBtn.className = "w-full sm:w-auto px-10 py-4 rounded-2xl bg-slate-800 text-slate-400 font-black text-base sm:text-lg border border-slate-700 transition cursor-not-allowed mx-auto flex items-center justify-center gap-2";
          startBtn.innerHTML = `<span>🔒 টেস্ট ${testId < 10 ? '০' + testId : testId} লকড (পূর্ববর্তী টেস্ট সম্পন্ন করুন)</span>`;
          startBtn.onclick = () => showLockedModal(testId);
        } else {
          startBtn.className = "w-full sm:w-auto px-10 py-4 rounded-2xl bg-gradient-to-r from-brand-600 via-emerald-600 to-teal-500 hover:from-brand-500 hover:to-teal-400 text-slate-950 font-black text-lg shadow-xl glow-brand transition transform hover:-translate-y-0.5 active:translate-y-0 mx-auto";
          startBtn.innerHTML = `🚀 পরীক্ষা শুরু করো (Start Exam)`;
          startBtn.onclick = () => startActiveExam();
        }
      }

      // Update Start Screen Elements
      document.getElementById('start-exam-title').innerText = current.test_name_bn || `মডেল টেস্ট ${testId}`;
      document.getElementById('start-stat-questions').innerText = `${current.total_questions || current.questions.length}টি`;
      document.getElementById('start-stat-marks').innerText = `${current.total_questions || current.questions.length}`;
      document.getElementById('start-stat-duration').innerText = `${current.duration_minutes || 60} মিনিট`;

      // Show Start Card, Hide Active Exam & Results
      document.getElementById('exam-start-card').classList.remove('hidden');
      document.getElementById('exam-active-card').classList.add('hidden');
      document.getElementById('exam-results-card').classList.add('hidden');

      // Auto-trigger paywall modal if user selects unpaid test > 5
      if (!unlocked && testId > 5 && !isPaid) {
        openBkashPaywallModal(stream, testId);
      }
    }

    // ============================================
    // START EXAM FLOW & COUNTDOWN TIMER
    // ============================================
    function startActiveExam() {
      const stream = appState.currentStream;
      const testId = appState.currentTestId;

      // Strict lock and paywall validation
      if (!isTestUnlocked(stream, testId)) {
        if (testId > 5 && !isStreamPaid(stream)) {
          openBkashPaywallModal(stream, testId);
        } else {
          showLockedModal(testId);
        }
        return;
      }
      const current = appState.currentTestObj;
      if (!current || !current.questions) {
        showToast("প্রশ্ন লোড করতে পারছে না।", "error");
        return;
      }

      appState.examStatus = 'running';
      appState.userAnswers = {};
      appState.examStartTime = new Date();
      appState.timerSecondsRemaining = (current.duration_minutes || 60) * 60;

      // Switch containers
      document.getElementById('exam-start-card').classList.add('hidden');
      document.getElementById('exam-results-card').classList.add('hidden');
      document.getElementById('exam-active-card').classList.remove('hidden');

      // Update counters
      document.getElementById('answered-count-pill').innerText = '০';
      document.getElementById('unanswered-count-pill').innerText = current.questions.length;
      document.getElementById('total-questions-pill').innerText = current.questions.length;
      const progBar = document.getElementById('exam-progress-bar');
      if (progBar) progBar.style.width = '0%';

      // Render all questions
      renderQuestionsFeed(current.questions);

      // Start backward countdown timer
      startCountdownTimer();

      window.scrollTo({ top: 180, behavior: 'smooth' });
      showToast("পরীক্ষা শুরু হয়েছে! শুভকামনা।", "success");
    }

    function startCountdownTimer() {
      if (appState.timerInterval) clearInterval(appState.timerInterval);

      updateTimerDisplay();

      appState.timerInterval = setInterval(() => {
        appState.timerSecondsRemaining--;
        updateTimerDisplay();

        if (appState.timerSecondsRemaining <= 0) {
          clearInterval(appState.timerInterval);
          openCustomModal({
            title: "⏱️ পরীক্ষার নির্ধারিত সময় সমাপ্ত!",
            subtitle: "আপনার উত্তরপত্র স্বয়ংক্রিয়ভাবে সাবমিট করা হচ্ছে...",
            icon: "⏱️",
            iconTheme: "rose",
            detailsHtml: `
              <div class="text-center text-xs text-rose-200 space-y-1.5 p-3.5 bg-rose-950/50 border border-rose-800/60 rounded-2xl shadow-inner">
                <p class="font-bold text-sm">পরীক্ষার নির্ধারিত ৬০ মিনিট সময় পূর্ণ হয়েছে।</p>
                <p class="text-slate-400 text-[11px] leading-relaxed">আপনার প্রদত্ত সকল উত্তর ইতিমধ্যে গৃহীত হয়েছে। স্বয়ংক্রিয়ভাবে ফলাফল বোর্ড প্রস্তুত করা হচ্ছে।</p>
              </div>
            `,
            confirmText: "ফলাফল দেখুন",
            showCancel: false,
            onConfirm: () => {
              submitActiveExam(true);
            }
          });
          setTimeout(() => {
            closeCustomModal(true);
            if (appState.examStatus !== 'submitted') {
              submitActiveExam(true);
            }
          }, 2200);
        }
      }, 1000);
    }

    function updateTimerDisplay() {
      const display = document.getElementById('countdown-timer-display');
      if (!display) return;

      const totalSec = Math.max(0, appState.timerSecondsRemaining);
      const mins = Math.floor(totalSec / 60);
      const secs = totalSec % 60;

      const formatted = `${mins < 10 ? '0' + mins : mins}:${secs < 10 ? '0' + secs : secs}`;
      display.innerText = formatted;

      if (totalSec <= 300) { // Last 5 mins
        display.classList.add('text-rose-400', 'animate-pulse');
        display.classList.remove('text-amber-300');
      } else {
        display.classList.remove('text-rose-400', 'animate-pulse');
        display.classList.add('text-amber-300');
      }
    }

    // ============================================
    // RENDER QUESTIONS FEED
    // ============================================
    function renderQuestionsFeed(questions) {
      const container = document.getElementById('questions-feed-container');
      if (!container) return;
      container.innerHTML = '';

      questions.forEach((q, idx) => {
        const card = document.createElement('div');
        card.id = `q-card-${idx}`;
        card.className = "bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-md space-y-3 transition";
        card.dataset.subject = q.subject || 'General';

        // Options array normalizer
        const opts = q.options ? q.options : [q.option_a, q.option_b, q.option_c, q.option_d];

        const optionLetters = ['ক', 'খ', 'গ', 'ঘ'];

        let optionsHtml = '';
        opts.forEach((optText, optIdx) => {
          optionsHtml += `
            <button type="button" onclick="selectQuestionOption(${idx}, ${optIdx})" id="opt-btn-${idx}-${optIdx}" class="opt-btn w-full text-left p-3.5 rounded-xl border border-slate-700/80 bg-slate-950/70 hover:bg-slate-800/80 transition flex items-center gap-3 group">
              <span class="w-7 h-7 rounded-lg bg-slate-800 group-hover:bg-brand-600/30 text-slate-300 group-hover:text-brand-300 border border-slate-700 font-bold text-xs flex items-center justify-center shrink-0">
                ${optionLetters[optIdx]}
              </span>
              <span class="text-xs sm:text-sm text-slate-200 font-medium group-hover:text-white flex-1">${optText || ''}</span>
            </button>
          `;
        });

        card.innerHTML = `
          <div class="flex items-center justify-between text-xs text-slate-400 border-b border-slate-800/80 pb-2">
            <div class="flex items-center gap-2">
              <span class="font-bold text-brand-400 text-sm">প্রশ্ন ${idx + 1}</span>
              <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-semibold">${q.subject || ''}</span>
              ${q.chapter ? `<span class="hidden sm:inline-block px-2 py-0.5 rounded bg-slate-800/60 text-slate-400 font-medium">${q.chapter}</span>` : ''}
            </div>
            <span id="q-status-badge-${idx}" class="text-[11px] font-bold text-slate-500">অনুত্তরিত</span>
          </div>

          <div class="text-sm sm:text-base font-semibold text-white leading-relaxed pt-1">
            ${q.question_bn || ''}
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">
            ${optionsHtml}
          </div>
        `;

        container.appendChild(card);
      });

      // Render KaTeX math if present
      if (window.renderMathInElement) {
        window.renderMathInElement(container, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false}
          ],
          throwOnError: false
        });
      }
    }

    // ============================================
    // SELECT OPTION HANDLER
    // ============================================
    function selectQuestionOption(qIndex, optIndex) {
      if (appState.examStatus !== 'running') return;

      appState.userAnswers[qIndex] = optIndex;

      // Update button visual styles
      for (let i = 0; i < 4; i++) {
        const btn = document.getElementById(`opt-btn-${qIndex}-${i}`);
        if (!btn) continue;
        if (i === optIndex) {
          btn.className = "opt-btn w-full text-left p-3.5 rounded-xl border border-brand-500 bg-brand-950/80 text-white transition flex items-center gap-3 shadow-md glow-brand";
        } else {
          btn.className = "opt-btn w-full text-left p-3.5 rounded-xl border border-slate-700/80 bg-slate-950/70 hover:bg-slate-800/80 transition flex items-center gap-3 group";
        }
      }

      // Update status badge
      const badge = document.getElementById(`q-status-badge-${qIndex}`);
      if (badge) {
        badge.innerText = "✓ উত্তর দেওয়া হয়েছে";
        badge.className = "text-[11px] font-bold text-emerald-400";
      }

      // Update counters & progress
      const totalQ = appState.currentTestObj.questions.length;
      const ansCount = Object.keys(appState.userAnswers).length;
      document.getElementById('answered-count-pill').innerText = ansCount;
      document.getElementById('unanswered-count-pill').innerText = totalQ - ansCount;

      const progBar = document.getElementById('exam-progress-bar');
      if (progBar && totalQ > 0) {
        const pct = Math.round((ansCount / totalQ) * 100);
        progBar.style.width = `${pct}%`;
      }
      saveSessionState();
    }

    // ============================================
    // QUESTION FILTERING
    // ============================================
    function filterQuestionsBySubject(subject, btnEl) {
      const cards = document.querySelectorAll('#questions-feed-container > div');
      cards.forEach(c => {
        const cSubj = (c.dataset.subject || '').toLowerCase();
        let match = false;
        if (subject === 'All') {
          match = true;
        } else if (subject === 'English_GK') {
          match = cSubj.includes('english') || cSubj.includes('gk') || cSubj.includes('general');
        } else if (subject === 'HigherMath') {
          match = cSubj.includes('math') || cSubj.includes('গণিত');
        } else {
          match = cSubj.includes(subject.toLowerCase());
        }
        if (match) c.classList.remove('hidden');
        else c.classList.add('hidden');
      });

      document.querySelectorAll('.q-filter-btn').forEach(btn => {
        btn.classList.remove('active-filter', 'bg-slate-800', 'text-white');
        btn.classList.add('bg-slate-900', 'text-slate-400');
      });
      if (btnEl) {
        btnEl.classList.add('active-filter', 'bg-slate-800', 'text-white');
        btnEl.classList.remove('bg-slate-900', 'text-slate-400');
      } else if (typeof event !== 'undefined' && event && event.target) {
        event.target.classList.add('active-filter', 'bg-slate-800', 'text-white');
        event.target.classList.remove('bg-slate-900', 'text-slate-400');
      }
    }

    // ============================================
    // SUBMISSION, GRADING & DUAL RANKING
    // ============================================
    function confirmSubmitExam() {
      const totalQ = (appState.currentTestObj && appState.currentTestObj.questions) ? appState.currentTestObj.questions.length : 100;
      const ansCount = Object.keys(appState.userAnswers).length;
      const unansCount = Math.max(0, totalQ - ansCount);
      const testName = (appState.currentTestObj && appState.currentTestObj.test_name_bn) ? appState.currentTestObj.test_name_bn : `মডেল টেস্ট ${appState.currentTestId}`;

      openCustomModal({
        title: "উত্তরপত্র সাবমিট নিশ্চিতকরণ",
        subtitle: `${testName} — আপনি কি নিশ্চিত যে পরীক্ষা জমা দিতে চান?`,
        icon: "📝",
        iconTheme: "emerald",
        detailsHtml: `
          <div class="grid grid-cols-2 gap-3 text-center">
            <div class="bg-emerald-950/60 border border-emerald-700/60 rounded-2xl p-3 shadow-inner">
              <div class="text-[11px] text-emerald-300 font-bold uppercase tracking-wider">উত্তর দেওয়া হয়েছে</div>
              <div class="text-2xl font-black text-emerald-400 font-mono mt-1">${ansCount}টি</div>
            </div>
            <div class="bg-amber-950/50 border border-amber-700/60 rounded-2xl p-3 shadow-inner">
              <div class="text-[11px] text-amber-300 font-bold uppercase tracking-wider">উত্তর বাকি আছে</div>
              <div class="text-2xl font-black text-amber-400 font-mono mt-1">${unansCount}টি</div>
            </div>
          </div>
          <div class="p-3 bg-slate-900/90 rounded-xl border border-slate-800 text-[11px] text-slate-300 space-y-1">
            <div class="font-bold text-emerald-400 flex items-center gap-1">
              <span>⚡</span> লাইভ সাবমিশন প্রক্রিয়া:
            </div>
            <p class="leading-relaxed text-slate-400">
              সাবমিট করার সাথে সাথেই ফলাফল ও জাতীয় মেধা স্থান (Session Rank & All-Time Rank) সরাসরি <strong>Neon PostgreSQL</strong> ডেটাবেজে সংরক্ষিত হবে।
            </p>
          </div>
        `,
        confirmText: "✓ হ্যাঁ, ফলাফল জমা দাও",
        cancelText: "না, আরও সময় নেব",
        showCancel: true,
        onConfirm: () => {
          submitActiveExam(false);
        }
      });
    }

    async function submitActiveExam(isAutoTimeout = false) {
      if (appState.timerInterval) clearInterval(appState.timerInterval);
      appState.examStatus = 'submitted';
      saveSessionState();

      const current = appState.currentTestObj;
      const questions = current.questions;
      const totalQuestions = questions.length;

      let correctCount = 0;
      let wrongCount = 0;
      let unansweredCount = 0;

      questions.forEach((q, idx) => {
        const studentAns = appState.userAnswers[idx];
        const correctIndex = (q.correct_index !== undefined) ? q.correct_index : 0;

        if (studentAns === undefined || studentAns === null) {
          unansweredCount++;
        } else if (studentAns === correctIndex) {
          correctCount++;
        } else {
          wrongCount++;
        }
      });

      // Score formula: correct - (wrong * 0.25)
      const rawScore = correctCount - (wrongCount * 0.25);
      const score = Math.max(0, parseFloat(rawScore.toFixed(2)));
      const percentage = parseFloat(((score / totalQuestions) * 100).toFixed(2));

      // Robust timeTaken calculation guaranteed never to be NaN
      const durationMins = (current && current.duration_minutes && !isNaN(current.duration_minutes)) ? Number(current.duration_minutes) : 60;
      const totalDurationSecs = durationMins * 60;
      const remSecs = (typeof appState.timerSecondsRemaining === 'number' && !isNaN(appState.timerSecondsRemaining)) ? appState.timerSecondsRemaining : totalDurationSecs;
      const timeTaken = Math.max(1, Math.min(totalDurationSecs, totalDurationSecs - Math.max(0, remSecs)));

      // Sequential Exam Unlocking Logic - Runs instantly on submit!
      let nextUnlocked = false;
      if (appState.currentStream === 'medical' && appState.currentTestId === appState.unlockedMed) {
        appState.unlockedMed = Math.min(100, appState.unlockedMed + 1);
        localStorage.setItem('admission_unlocked_med', appState.unlockedMed);
        nextUnlocked = true;
      } else if (appState.currentStream === 'versity' && appState.currentTestId === appState.unlockedVar) {
        appState.unlockedVar = Math.min(100, appState.unlockedVar + 1);
        localStorage.setItem('admission_unlocked_var', appState.unlockedVar);
        nextUnlocked = true;
      }

      updateUnlockedBadges();
      populateTestDropdown();

      // Render Scoreboard & Review Feed immediately
      renderExamScoreboard({
        score,
        percentage,
        correctCount,
        wrongCount,
        unansweredCount,
        timeTaken,
        totalQuestions,
        rankingResult: null,
        nextUnlocked
      });

      // Switch to Results view
      document.getElementById('exam-active-card').classList.add('hidden');
      document.getElementById('exam-results-card').classList.remove('hidden');

      window.scrollTo({ top: 120, behavior: 'smooth' });

      // Trigger Confetti Celebration on good score / unlock
      if (typeof confetti === 'function') {
        confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
      }

      // Live ranking sync with Neon PostgreSQL database
      const mode = (appState.currentStream === 'medical') ? 'FullExam' : ((appState.currentStream === 'versity') ? 'GSTExam' : 'Past15Years');
      try {
        const response = await fetch('/api/submit-exam', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            student_id: appState.studentId,
            student_name: 'পরীক্ষার্থী ' + appState.studentId.substring(4, 8).toUpperCase(),
            session: appState.selectedSession,
            test_id: appState.currentTestId,
            test_code: current.test_code || ('MT-' + String(appState.currentTestId).padStart(3, '0')),
            subject_mode: mode,
            total_questions: totalQuestions,
            correct_count: correctCount,
            wrong_count: wrongCount,
            unanswered_count: unansweredCount,
            score: score,
            time_taken_seconds: timeTaken
          })
        });
        const data = await response.json();
        if (data && data.rankings) {
          const r = data.rankings;
          document.getElementById('results-session-rank').innerHTML = `#${r.session_rank} <span class="text-xs text-slate-400 font-normal">/ মোট ${r.session_total} জন</span>`;
          document.getElementById('results-alltime-rank').innerHTML = `#${r.all_time_rank} <span class="text-xs text-slate-400 font-normal">/ মোট ${r.all_time_total} জন</span>`;
        }
      } catch (e) {
        console.warn("Background ranking API sync error:", e);
        // Clean fallback showing actual single submission if offline
        document.getElementById('results-session-rank').innerHTML = `#১ <span class="text-xs text-slate-400 font-normal">/ মোট ১ জন</span>`;
        document.getElementById('results-alltime-rank').innerHTML = `#১ <span class="text-xs text-slate-400 font-normal">/ মোট ১ জন</span>`;
      }
    }

    // ============================================
    // RENDER SCOREBOARD & QUESTION REVIEW
    // ============================================
    function renderExamScoreboard(data) {
      const current = appState.currentTestObj;
      document.getElementById('results-test-name').innerText = current.test_name_bn || `মডেল টেস্ট ${appState.currentTestId}`;
      document.getElementById('results-total-score').innerText = data.score.toFixed(2);
      document.getElementById('results-full-marks').innerText = data.totalQuestions;

      document.getElementById('results-correct-count').innerText = data.correctCount;
      document.getElementById('results-wrong-count').innerText = data.wrongCount;
      document.getElementById('results-unanswered-count').innerText = data.unansweredCount;

      const safeSec = (!isNaN(data.timeTaken) && data.timeTaken > 0) ? Math.floor(data.timeTaken) : 1;
      const mins = Math.floor(safeSec / 60);
      const secs = safeSec % 60;
      document.getElementById('results-time-taken').innerText = `${mins} মিনিট ${secs} সেকেন্ড`;

      // Session Name & Rankings
      document.getElementById('results-session-name').innerText = appState.selectedSession;

      if (data.rankingResult && data.rankingResult.rankings) {
        const r = data.rankingResult.rankings;
        document.getElementById('results-session-rank').innerHTML = `#${r.session_rank} <span class="text-xs text-slate-400 font-normal">/ মোট ${r.session_total} জন</span>`;
        document.getElementById('results-alltime-rank').innerHTML = `#${r.all_time_rank} <span class="text-xs text-slate-400 font-normal">/ মোট ${r.all_time_total} জন</span>`;
      } else {
        // Real-time syncing state: NO hardcoded fake numbers!
        document.getElementById('results-session-rank').innerHTML = `<span class="text-sm font-normal text-amber-400 animate-pulse">হিসাব করা হচ্ছে...</span>`;
        document.getElementById('results-alltime-rank').innerHTML = `<span class="text-sm font-normal text-amber-400 animate-pulse">হিসাব করা হচ্ছে...</span>`;
      }

      // Unlock Notice & Button
      const notice = document.getElementById('results-unlock-notice');
      const nextBtn = document.getElementById('btn-goto-next-test');
      const paywallTeaser = document.getElementById('results-paywall-teaser');

      if (appState.currentTestId === 5 && !isStreamPaid(appState.currentStream)) {
        if (paywallTeaser) paywallTeaser.classList.remove('hidden');
        if (notice) {
          notice.innerHTML = `<span>🎁</span> আপনি সফলভাবে ফ্রি ৫টি মডেল টেস্ট সম্পন্ন করেছেন!`;
          notice.className = "text-xs sm:text-sm text-pink-300 font-bold flex items-center justify-center md:justify-start gap-1.5";
        }
        if (nextBtn) {
          nextBtn.classList.remove('hidden');
          nextBtn.innerHTML = `<span>📱 বাকি ৯৫টি টেস্ট আনলক (৳৪৯৯)</span> <span>→</span>`;
          nextBtn.onclick = () => openBkashPaywallModal(appState.currentStream, 6);
        }
      } else {
        if (paywallTeaser) paywallTeaser.classList.add('hidden');
        if (nextBtn) {
          nextBtn.innerHTML = `<span>পরবর্তী টেস্টে যান (Next Test)</span> <span>→</span>`;
          nextBtn.onclick = () => loadNextUnlockedExam();
        }
        if (data.nextUnlocked) {
          notice.innerHTML = `<span>🎉</span> অভিনন্দন! টেস্ট ০${appState.currentTestId + 1} সফলভাবে আনলক হয়েছে!`;
          notice.className = "text-xs sm:text-sm text-emerald-400 font-bold flex items-center justify-center md:justify-start gap-1.5";
          if (nextBtn) nextBtn.classList.remove('hidden');
        } else {
          notice.innerHTML = `<span>✓</span> টেস্ট সম্পন্ন হয়েছে।`;
          notice.className = "text-xs sm:text-sm text-slate-400 font-bold flex items-center justify-center md:justify-start gap-1.5";
        }
      }

      // Render Review Cards
      renderReviewCards(current.questions);

      // Render Subject Chart
      renderSubjectAutopsyChart(current.questions);
    }

    function renderReviewCards(questions) {
      const container = document.getElementById('results-review-feed');
      if (!container) return;
      container.innerHTML = '';

      const optionLetters = ['ক', 'খ', 'গ', 'ঘ'];

      questions.forEach((q, idx) => {
        const studentAns = appState.userAnswers[idx];
        const correctIndex = (q.correct_index !== undefined) ? q.correct_index : 0;
        const opts = q.options ? q.options : [q.option_a, q.option_b, q.option_c, q.option_d];

        let statusBadge = '';
        let cardBorder = 'border-slate-800';

        if (studentAns === undefined || studentAns === null) {
          statusBadge = '<span class="px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-bold text-xs">উত্তর করা হয়নি (০.০০)</span>';
        } else if (studentAns === correctIndex) {
          statusBadge = '<span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 font-bold text-xs">✓ সঠিক উত্তর (+১.০০)</span>';
          cardBorder = 'border-emerald-900/60 bg-emerald-950/10';
        } else {
          statusBadge = '<span class="px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800 font-bold text-xs">✗ ভুল উত্তর (-০.২৫)</span>';
          cardBorder = 'border-rose-900/60 bg-rose-950/10';
        }

        let optionsHtml = '';
        opts.forEach((optText, optIdx) => {
          let optClass = "p-3 rounded-xl border border-slate-800 bg-slate-950/70 text-slate-300 text-xs sm:text-sm flex items-center gap-2.5";
          let marker = '';

          if (optIdx === correctIndex) {
            optClass = "p-3 rounded-xl border border-emerald-500 bg-emerald-950/80 text-emerald-200 font-bold text-xs sm:text-sm flex items-center gap-2.5 shadow-sm";
            marker = '<span class="ml-auto text-emerald-400 font-bold text-xs">✓ সঠিক</span>';
          } else if (optIdx === studentAns && studentAns !== correctIndex) {
            optClass = "p-3 rounded-xl border border-rose-500 bg-rose-950/80 text-rose-200 font-bold text-xs sm:text-sm flex items-center gap-2.5 shadow-sm";
            marker = '<span class="ml-auto text-rose-400 font-bold text-xs">✗ আপনার উত্তর</span>';
          }

          optionsHtml += `
            <div class="${optClass}">
              <span class="w-6 h-6 rounded bg-slate-800 font-bold text-xs flex items-center justify-center shrink-0">
                ${optionLetters[optIdx]}
              </span>
              <span>${optText || ''}</span>
              ${marker}
            </div>
          `;
        });

        const card = document.createElement('div');
        card.className = `bg-slate-900 border ${cardBorder} rounded-2xl p-5 shadow space-y-3`;
        card.innerHTML = `
          <div class="flex items-center justify-between text-xs text-slate-400 border-b border-slate-800 pb-2">
            <div class="flex items-center gap-2">
              <span class="font-bold text-white text-sm">প্রশ্ন ${idx + 1}</span>
              <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-semibold">${q.subject || ''}</span>
              ${q.chapter ? `<span class="hidden sm:inline-block px-2 py-0.5 rounded bg-slate-800/60 text-slate-400">${q.chapter}</span>` : ''}
            </div>
            ${statusBadge}
          </div>

          <div class="text-sm sm:text-base font-semibold text-white leading-relaxed pt-1">
            ${q.question_bn || ''}
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
            ${optionsHtml}
          </div>

          <div class="mt-3 pt-3 border-t border-slate-800 text-xs text-slate-300 bg-slate-950/50 rounded-xl p-3 space-y-1">
            <div class="font-bold text-brand-400 flex items-center gap-1.5">
              <span>📚 পাঠ্যবই নির্ভুল ব্যাখ্যা:</span>
            </div>
            <p class="leading-relaxed text-slate-300 font-medium">${q.explanation || 'এনসিটিবি পাঠ্যবই অনুসারে সঠিক উত্তর ব্যাখ্যা প্রদান করা হলো।'}</p>
            ${q.book_reference ? `<div class="text-[11px] text-slate-400 font-semibold pt-1">রেফারেন্স: ${q.book_reference}</div>` : ''}
          </div>
        `;

        container.appendChild(card);
      });

      if (window.renderMathInElement) {
        window.renderMathInElement(container, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false}
          ],
          throwOnError: false
        });
      }
    }

    function renderSubjectAutopsyChart(questions) {
      const subjectStats = {};
      questions.forEach((q, idx) => {
        const s = q.subject || 'অন্যান্য';
        if (!subjectStats[s]) subjectStats[s] = { total: 0, correct: 0, wrong: 0 };
        subjectStats[s].total++;

        const studentAns = appState.userAnswers[idx];
        const correctIndex = (q.correct_index !== undefined) ? q.correct_index : 0;
        if (studentAns === correctIndex) subjectStats[s].correct++;
        else if (studentAns !== undefined && studentAns !== null) subjectStats[s].wrong++;
      });

      const labels = Object.keys(subjectStats);
      const accuracies = labels.map(l => {
        const item = subjectStats[l];
        return Math.round((item.correct / item.total) * 100);
      });

      // Render Chart.js
      const canvas = document.getElementById('exam-subject-chart');
      if (!canvas) return;

      if (appState.chartInstance) appState.chartInstance.destroy();

      appState.chartInstance = new Chart(canvas, {
        type: 'radar',
        data: {
          labels: labels,
          datasets: [{
            label: 'নির্ভুলতার হার (%)',
            data: accuracies,
            backgroundColor: 'rgba(16, 185, 129, 0.2)',
            borderColor: '#10b981',
            pointBackgroundColor: '#10b981',
            borderWidth: 2
          }]
        },
        options: {
          scales: {
            r: {
              beginAtZero: true,
              max: 100,
              ticks: { color: '#94a3b8', backdropColor: 'transparent', stepSize: 20 },
              grid: { color: '#334155' },
              angleLines: { color: '#334155' },
              pointLabels: { color: '#f8fafc', font: { size: 11, weight: 'bold' } }
            }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });

      // Render textual subject summary
      const listEl = document.getElementById('subject-performance-list');
      if (!listEl) return;
      listEl.innerHTML = '';

      labels.forEach(subj => {
        const st = subjectStats[subj];
        const pct = Math.round((st.correct / st.total) * 100);
        const item = document.createElement('div');
        item.className = "bg-slate-950/70 rounded-xl p-3 border border-slate-800 flex items-center justify-between text-xs";
        item.innerHTML = `
          <div>
            <div class="font-bold text-white text-sm">${subj}</div>
            <div class="text-slate-400 text-[11px]">মোট: ${st.total} | সঠিক: ${st.correct} | ভুল: ${st.wrong}</div>
          </div>
          <div class="text-right">
            <span class="font-mono font-black text-sm ${pct >= 75 ? 'text-emerald-400' : (pct >= 50 ? 'text-amber-400' : 'text-rose-400')}">${pct}%</span>
            <div class="text-[10px] text-slate-500 font-semibold">নির্ভুলতা</div>
          </div>
        `;
        listEl.appendChild(item);
      });
    }

    function retakeCurrentExam() {
      openCustomModal({
        title: "পরীক্ষা পুনরায় শুরু করবেন?",
        subtitle: "বর্তমান চিহ্নিত উত্তরপত্র রিসেট হবে",
        icon: "🔄",
        iconTheme: "blue",
        detailsHtml: `
          <div class="text-xs text-slate-300 leading-relaxed text-center p-3.5 bg-blue-950/40 border border-blue-800/50 rounded-2xl">
            আপনি কি বর্তমান পরীক্ষাটি আবার নতুন করে শুরু করতে চান? আপনার পূর্ববর্তী চিহ্নিত উত্তরপত্র এবং টাইমার পুনরায় সম্পূর্ণ সময় থেকে শুরু হবে।
          </div>
        `,
        confirmText: "হ্যাঁ, পুনরায় শুরু করো",
        cancelText: "বাতিল",
        showCancel: true,
        onConfirm: () => {
          loadCurrentSelectedTest();
        }
      });
    }

    function loadNextUnlockedExam() {
      const nextId = appState.currentTestId + 1;
      if (nextId <= 100) {
        if (isTestUnlocked(appState.currentStream, nextId)) {
          appState.currentTestId = nextId;
          document.getElementById('model-test-dropdown').value = nextId;
          loadCurrentSelectedTest();
        } else if (nextId > 5 && !isStreamPaid(appState.currentStream)) {
          openBkashPaywallModal(appState.currentStream, nextId);
        } else {
          showLockedModal(nextId);
        }
      } else {
        openCustomModal({
          title: "সর্বশেষ টেস্ট সম্পন্ন",
          subtitle: "১০০ মডেল টেস্ট সফল সমাপ্তি",
          icon: "🎓",
          iconTheme: "emerald",
          detailsHtml: `
            <div class="text-xs text-slate-300 leading-relaxed text-center p-3.5 bg-emerald-950/40 border border-emerald-800/50 rounded-2xl">
              অভিনন্দন! আপনি সফলভাবে এই সিরিজের সকল ১০০টি মডেল টেস্ট সম্পন্ন করেছেন।
            </div>
          `,
          confirmText: "ধন্যবাদ",
          showCancel: false
        });
      }
    }

    // ============================================
    // 100 TESTS GRID MODAL
    // ============================================
    function toggleTestGridModal() {
      const modal = document.getElementById('grid-modal');
      if (!modal) return;

      if (modal.classList.contains('hidden')) {
        renderTestGridCards();
        modal.classList.remove('hidden');
      } else {
        modal.classList.add('hidden');
      }
    }

    function renderTestGridCards() {
      const container = document.getElementById('test-grid-cards');
      if (!container) return;
      container.innerHTML = '';

      const modalTitle = document.getElementById('grid-modal-title');
      modalTitle.innerText = (appState.currentStream === 'medical') 
        ? "📋 মেডিকেল ১০০ মডেল টেস্টের অগ্রগতি (১–৫ ফ্রি • ৬–১০০ প্রিমিয়াম)" 
        : "📋 ভার্সিটি ও সমন্বিত গুচ্ছ ১০০ মডেল টেস্টের অগ্রগতি (১–৫ ফ্রি • ৬–১০০ প্রিমিয়াম)";

      const paid = isStreamPaid(appState.currentStream);

      for (let i = 1; i <= 100; i++) {
        const unlocked = isTestUnlocked(appState.currentStream, i);
        const card = document.createElement('div');
        const isFree = i <= 5;

        if (unlocked) {
          card.className = "cursor-pointer p-3 rounded-xl border border-emerald-500/60 bg-emerald-950/40 hover:bg-emerald-900/60 transition text-center shadow group";
          card.onclick = () => {
            appState.currentTestId = i;
            document.getElementById('model-test-dropdown').value = i;
            toggleTestGridModal();
            loadCurrentSelectedTest();
          };
          card.innerHTML = `
            <div class="flex items-center justify-between text-[10px] font-bold">
              <span class="text-emerald-300">টেস্ট #${i}</span>
              <span class="${isFree ? 'text-teal-300' : 'text-amber-300'}">${isFree ? '🎁 ফ্রি' : '👑 প্রিমিয়াম'}</span>
            </div>
            <div class="text-xs font-black text-white mt-1 group-hover:text-emerald-300">উন্মুক্ত ✓</div>
          `;
        } else {
          if (!isFree && !paid) {
            // Unpurchased Premium Test Card
            card.className = "cursor-pointer p-3 rounded-xl border border-pink-500/50 bg-pink-950/20 hover:border-pink-500 hover:bg-pink-950/40 transition text-center shadow group";
            card.onclick = () => {
              toggleTestGridModal();
              openBkashPaywallModal(appState.currentStream, i);
            };
            card.innerHTML = `
              <div class="flex items-center justify-between text-[10px] font-bold">
                <span class="text-pink-300">টেস্ট #${i}</span>
                <span class="text-pink-400 font-extrabold">👑 ৳৪৯৯</span>
              </div>
              <div class="text-xs font-bold text-pink-200 mt-1 flex items-center justify-center gap-1 group-hover:scale-105 transition">🔒 আনলক করুন</div>
            `;
          } else {
            // Sequentially Locked Test Card
            card.className = "cursor-pointer p-3 rounded-xl border border-slate-800 bg-slate-950/60 text-center opacity-60 hover:opacity-100 transition";
            card.onclick = () => showLockedModal(i);
            card.innerHTML = `
              <div class="flex items-center justify-between text-[10px] font-semibold text-slate-400">
                <span>টেস্ট #${i}</span>
                <span>${isFree ? 'ফ্রি' : 'প্রিমিয়াম'}</span>
              </div>
              <div class="text-xs font-bold text-slate-500 mt-1 flex items-center justify-center gap-1">🔒 লকড</div>
            `;
          }
        }
        container.appendChild(card);
      }
    }

    // ============================================
    // PAST 15 YEARS TESTS FLOW (NO SEQUENTIAL LOCK RULE)
    // ============================================
    function getActivePastYearList() {
      const substream = appState.pastSubStream || 'medical';
      if (appState.past15YearsData && Array.isArray(appState.past15YearsData[substream])) {
        return appState.past15YearsData[substream];
      }
      if (Array.isArray(appState.past15YearsData)) {
        return appState.past15YearsData;
      }
      return [];
    }

    function switchPastSubStream(substream) {
      appState.pastSubStream = substream;
      const btnMed = document.getElementById('past-btn-medical');
      const btnVar = document.getElementById('past-btn-versity');
      const titleEl = document.getElementById('past-year-stream-title');

      if (substream === 'medical') {
        if (btnMed) {
          btnMed.className = "px-3 py-1.5 rounded-lg text-xs font-bold transition bg-purple-600 text-white shadow";
        }
        if (btnVar) {
          btnVar.className = "px-3 py-1.5 rounded-lg text-xs font-bold text-slate-400 hover:text-white transition";
        }
        if (titleEl) titleEl.innerText = "মেডিকেল বিগত ১৫ বছরের প্রশ্নব্যাংক (২০১০ - ২০২৫)";
      } else {
        if (btnMed) {
          btnMed.className = "px-3 py-1.5 rounded-lg text-xs font-bold text-slate-400 hover:text-white transition";
        }
        if (btnVar) {
          btnVar.className = "px-3 py-1.5 rounded-lg text-xs font-bold transition bg-blue-600 text-white shadow";
        }
        if (titleEl) titleEl.innerText = "ভার্সিটি ও গুচ্ছ বিগত ১৫ বছরের প্রশ্নব্যাংক (২০১০ - ২০২৫)";
      }
      populatePastYearSelect();
      renderPastYearView();
    }

    function populatePastYearSelect() {
      const select = document.getElementById('past-year-select');
      const list = getActivePastYearList();
      if (!select || !list) return;
      select.innerHTML = '';

      list.forEach(item => {
        const opt = document.createElement('option');
        opt.value = item.session;
        const totalQ = (item.questions && item.questions.length) ? item.questions.length : (item.total_questions || 100);
        opt.text = `সেশন: ${item.session} (${totalQ}টি প্রশ্ন)`;
        select.appendChild(opt);
      });

      if (list.length > 0) {
        const exists = list.some(p => p.session === appState.activePastYear);
        if (!exists) {
          appState.activePastYear = list[0].session;
        }
        select.value = appState.activePastYear;
      }
    }

    function loadPastYearTest(session) {
      appState.activePastYear = session;
      renderPastYearView();
    }

    function renderPastYearView() {
      const list = getActivePastYearList();
      const pastObj = list.find(p => p.session === appState.activePastYear) || list[0];
      if (!pastObj) return;

      appState.activePastYear = pastObj.session;
      const select = document.getElementById('past-year-select');
      if (select) select.value = pastObj.session;

      document.getElementById('past-year-active-badge').innerText = `সেশন: ${pastObj.session}`;
      const qCount = pastObj.questions ? pastObj.questions.length : (pastObj.total_questions || 100);
      document.getElementById('past-year-question-count-badge').innerText = `${qCount}টি আসল প্রশ্ন`;

      const container = document.getElementById('past-year-questions-container');
      container.innerHTML = '';

      const optionLetters = ['ক', 'খ', 'গ', 'ঘ'];

      (pastObj.questions || []).forEach((q, idx) => {
        const card = document.createElement('div');
        card.className = "bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow space-y-3";

        const correctIndex = (q.correct_index !== undefined) ? q.correct_index : 0;
        const opts = q.options ? q.options : [q.option_a, q.option_b, q.option_c, q.option_d];

        let optionsHtml = '';
        opts.forEach((optText, optIdx) => {
          let optStyle = "p-3 rounded-xl border border-slate-800 bg-slate-950/70 text-slate-300 text-xs sm:text-sm flex items-center gap-2.5";
          let badge = '';

          // If show answers mode is on
          if (appState.pastShowAnswers && optIdx === correctIndex) {
            optStyle = "p-3 rounded-xl border border-purple-500 bg-purple-950/80 text-purple-200 font-bold text-xs sm:text-sm flex items-center gap-2.5 shadow";
            badge = '<span class="ml-auto text-purple-400 font-bold text-xs">✓ সঠিক উত্তর</span>';
          }

          optionsHtml += `
            <div class="${optStyle}">
              <span class="w-6 h-6 rounded bg-slate-800 text-slate-300 font-bold text-xs flex items-center justify-center shrink-0">
                ${optionLetters[optIdx]}
              </span>
              <span>${optText || ''}</span>
              ${badge}
            </div>
          `;
        });

        const examTypeBn = (pastObj.stream === 'versity' || appState.pastSubStream === 'versity') ? 'ভার্সিটি ও গুচ্ছ ভর্তি পরীক্ষা' : 'মেডিকেল ভর্তি পরীক্ষা';

        card.innerHTML = `
          <div class="flex items-center justify-between text-xs text-slate-400 border-b border-slate-800 pb-2">
            <div class="flex items-center gap-2">
              <span class="font-bold text-purple-400 text-sm">প্রশ্ন ${idx + 1}</span>
              <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-semibold">${q.subject || ''}</span>
              ${q.chapter ? `<span class="hidden sm:inline-block px-2 py-0.5 rounded bg-slate-800/60 text-slate-400 font-medium">${q.chapter}</span>` : ''}
            </div>
            <span class="text-[11px] font-semibold text-slate-500">${examTypeBn} ${pastObj.session}</span>
          </div>

          <div class="text-sm sm:text-base font-semibold text-white leading-relaxed pt-1">
            ${q.question_bn || ''}
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
            ${optionsHtml}
          </div>

          ${appState.pastShowAnswers ? `
            <div class="mt-3 pt-3 border-t border-slate-800 text-xs text-slate-300 bg-slate-950/60 rounded-xl p-3 space-y-1">
              <div class="font-bold text-purple-400">💡 সমাধান ও নির্ভুল ব্যাখ্যা:</div>
              <p class="leading-relaxed font-medium">${q.explanation || 'এনসিটিবি পাঠ্যবই ও বিগত বছরের প্রশ্নব্যাংকের ভিত্তিতে সঠিক উত্তর।'}</p>
              ${q.book_reference ? `<div class="text-[11px] text-slate-400 pt-1">রেফারেন্স: ${q.book_reference}</div>` : ''}
            </div>
          ` : ''}
        `;

        container.appendChild(card);
      });

      if (window.renderMathInElement) {
        window.renderMathInElement(container, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false}
          ],
          throwOnError: false
        });
      }
    }

    function togglePastYearAnswerSheet() {
      appState.pastShowAnswers = !appState.pastShowAnswers;
      const btnText = document.getElementById('past-show-answer-text');
      if (btnText) {
        btnText.innerText = appState.pastShowAnswers ? "উত্তরপত্র লুকান (Hide Answers)" : "উত্তরপত্র দেখুন (Show Answers)";
      }
      renderPastYearView();
    }

    function startPastYearExam() {
      const list = getActivePastYearList();
      const pastObj = list.find(p => p.session === appState.activePastYear) || list[0];
      if (!pastObj) return;

      // Switch to model test view with pastObj as active
      appState.currentTestObj = pastObj;
      appState.currentStream = 'past_15years';
      appState.examStatus = 'running';
      appState.userAnswers = {};
      appState.examStartTime = new Date();
      appState.timerSecondsRemaining = (pastObj.duration_minutes || 60) * 60;

      // Switch to model test view tab
      document.getElementById('view-past-15years').classList.add('hidden');
      document.getElementById('view-model-tests').classList.remove('hidden');

      document.getElementById('exam-start-card').classList.add('hidden');
      document.getElementById('exam-results-card').classList.add('hidden');
      document.getElementById('exam-active-card').classList.remove('hidden');

      document.getElementById('answered-count-pill').innerText = '০';
      document.getElementById('unanswered-count-pill').innerText = pastObj.questions.length;
      document.getElementById('total-questions-pill').innerText = pastObj.questions.length;
      const progBar = document.getElementById('exam-progress-bar');
      if (progBar) progBar.style.width = '0%';

      renderQuestionsFeed(pastObj.questions);
      startCountdownTimer();

      window.scrollTo({ top: 180, behavior: 'smooth' });
    }

    // ============================================
    // TEXTBOOK KNOWLEDGE BASE (2,000 FACTS)
    // ============================================
    function onKbSearch(query) {
      appState.kbSearchQuery = query.trim().toLowerCase();
      appState.kbCurrentPage = 1;
      renderKbFacts();
    }

    function filterKbBySubject(subj, btnEl) {
      appState.kbSelectedSubject = subj;
      appState.kbCurrentPage = 1;

      document.querySelectorAll('.kb-chip').forEach(c => {
        c.classList.remove('bg-amber-500', 'text-slate-950', 'active-kb-chip');
        c.classList.add('bg-slate-800', 'text-slate-300');
      });
      if (btnEl) {
        btnEl.classList.add('bg-amber-500', 'text-slate-950', 'active-kb-chip');
        btnEl.classList.remove('bg-slate-800', 'text-slate-300');
      } else if (typeof event !== 'undefined' && event && event.target) {
        event.target.classList.add('bg-amber-500', 'text-slate-950', 'active-kb-chip');
        event.target.classList.remove('bg-slate-800', 'text-slate-300');
      }

      renderKbFacts();
    }

    function renderKbFacts() {
      const container = document.getElementById('kb-facts-container');
      if (!container || !appState.textbookKb) return;
      container.innerHTML = '';

      let filtered = appState.textbookKb;

      // Filter by subject
      if (appState.kbSelectedSubject !== 'All') {
        const s = appState.kbSelectedSubject.toLowerCase();
        filtered = filtered.filter(item => {
          const subDisc = (item.sub_discipline || '').toLowerCase();
          const subj = (item.subject || '').toLowerCase();
          if (s === 'botany') return subDisc.includes('botany');
          if (s === 'zoology') return subDisc.includes('zoology');
          if (s === 'chem1') return subj.includes('chem') && subDisc.includes('1');
          if (s === 'chem2') return subj.includes('chem') && subDisc.includes('2');
          if (s === 'phys1') return subj.includes('phys') && subDisc.includes('1');
          if (s === 'phys2') return subj.includes('phys') && subDisc.includes('2');
          if (s === 'math') return subj.includes('math');
          return true;
        });
      }

      // Filter by search query
      if (appState.kbSearchQuery) {
        const q = appState.kbSearchQuery;
        filtered = filtered.filter(item => {
          return (item.topic && item.topic.toLowerCase().includes(q)) ||
                 (item.chapter && item.chapter.toLowerCase().includes(q)) ||
                 (item.author && item.author.toLowerCase().includes(q)) ||
                 (item.exact_text_bn && item.exact_text_bn.toLowerCase().includes(q)) ||
                 (item.keywords && item.keywords.toLowerCase().includes(q));
        });
      }

      // Pagination
      const totalFiltered = filtered.length;
      const pageSize = appState.kbPageSize;
      const totalPages = Math.max(1, Math.ceil(totalFiltered / pageSize));
      const page = Math.min(appState.kbCurrentPage, totalPages);
      appState.kbCurrentPage = page;

      const startIndex = (page - 1) * pageSize;
      const pageItems = filtered.slice(startIndex, startIndex + pageSize);

      // Update counters
      document.getElementById('kb-showing-count').innerText = `${totalFiltered > 0 ? startIndex + 1 : 0} - ${Math.min(startIndex + pageSize, totalFiltered)}`;
      document.getElementById('kb-total-count').innerText = totalFiltered;
      document.getElementById('kb-page-indicator').innerText = `${page} / ${totalPages}`;

      document.getElementById('btn-kb-prev').disabled = (page <= 1);
      document.getElementById('btn-kb-next').disabled = (page >= totalPages);

      // Render cards
      pageItems.forEach(item => {
        const card = document.createElement('div');
        card.className = "bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow space-y-3 hover:border-slate-700 transition";
        card.innerHTML = `
          <div class="flex items-center justify-between text-xs text-slate-400 border-b border-slate-800 pb-2">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded bg-amber-950 text-amber-300 font-bold border border-amber-800">${item.subject}</span>
              <span class="font-bold text-white text-xs">${item.chapter}</span>
            </div>
            <span class="text-amber-400 font-bold text-[11px]">⭐⭐⭐⭐⭐ প্রায়োরিটি</span>
          </div>

          <div class="text-sm font-bold text-amber-300">
            ${item.topic}
          </div>

          <p class="text-xs sm:text-sm text-slate-200 leading-relaxed font-medium bg-slate-950/60 p-3 rounded-xl border border-slate-800">
            ${item.exact_text_bn}
          </p>

          ${item.common_mcq_trap ? `
            <div class="text-[11px] text-rose-300 font-semibold bg-rose-950/40 p-2.5 rounded-lg border border-rose-900/60">
              ⚠️ ভর্তি পরীক্ষার ট্র্যাপ: ${item.common_mcq_trap}
            </div>
          ` : ''}

          <div class="text-[11px] text-slate-400 pt-1 flex items-center justify-between">
            <span class="font-semibold">লেখক: ${item.author}</span>
            <span class="text-slate-500">${item.book_name}</span>
          </div>
        `;
        container.appendChild(card);
      });

      if (window.renderMathInElement) {
        window.renderMathInElement(container, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false}
          ],
          throwOnError: false
        });
      }
    }

    function prevKbPage() {
      if (appState.kbCurrentPage > 1) {
        appState.kbCurrentPage--;
        renderKbFacts();
        window.scrollTo({ top: 300, behavior: 'smooth' });
      }
    }

    function nextKbPage() {
      appState.kbCurrentPage++;
      renderKbFacts();
      window.scrollTo({ top: 300, behavior: 'smooth' });
    }

    // ============================================
    // NO-CALCULATOR SPEED MATH TRICKS
    // ============================================
    function renderNocalcTricks() {
      const container = document.getElementById('nocalc-tricks-grid');
      if (!container || !appState.nocalcTricks) return;
      container.innerHTML = '';

      appState.nocalcTricks.forEach((trick, idx) => {
        const card = document.createElement('div');
        card.className = "bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow space-y-3";
        card.innerHTML = `
          <div class="flex items-center justify-between text-xs text-slate-400 border-b border-slate-800 pb-2">
            <span class="px-2.5 py-0.5 rounded-full bg-amber-950 text-amber-300 border border-amber-800 font-bold">
              ট্রিক #${idx + 1}
            </span>
            <span class="text-slate-400 font-semibold">${trick.category || 'ঢাবি ক ইউনিট'}</span>
          </div>

          <h3 class="text-sm sm:text-base font-bold text-white">${trick.title_bn || ''}</h3>

          <div class="text-xs sm:text-sm text-slate-300 bg-slate-950 p-3.5 rounded-xl border border-slate-800 font-mono leading-relaxed">
            ${trick.technique || trick.description || ''}
          </div>

          ${trick.example ? `
            <div class="text-xs text-emerald-300 font-medium bg-emerald-950/30 p-3 rounded-xl border border-emerald-900/50">
              <strong class="text-white">উদাহরণ:</strong> ${trick.example}
            </div>
          ` : ''}
        `;
        container.appendChild(card);
      });

      if (window.renderMathInElement) {
        window.renderMathInElement(container, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false}
          ],
          throwOnError: false
        });
      }
    }

    // ============================================
    // SESSION STATE PERSISTENCE (DEVICE RESILIENCE)
    // ============================================
    function saveSessionState() {
      try {
        const sessionData = {
          currentStream: appState.currentStream,
          currentTestId: appState.currentTestId,
          examStatus: appState.examStatus,
          userAnswers: appState.userAnswers,
          timerSecondsRemaining: appState.timerSecondsRemaining,
          savedAt: Date.now()
        };
        localStorage.setItem('admission_active_session', JSON.stringify(sessionData));
      } catch (e) {
        console.warn('Failed to save session state', e);
      }
    }

    function restoreSessionState() {
      try {
        const raw = localStorage.getItem('admission_active_session');
        if (!raw) return false;
        const session = JSON.parse(raw);
        if (!session) return false;

        if (session.currentStream && ['medical', 'versity', 'past_15years', 'textbooks', 'nocalc', 'engineering'].includes(session.currentStream)) {
          appState.currentStream = session.currentStream;
        }
        if (session.currentTestId && session.currentTestId >= 1 && session.currentTestId <= 100) {
          appState.currentTestId = session.currentTestId;
        }

        if (session.examStatus === 'running' && session.savedAt && typeof session.timerSecondsRemaining === 'number') {
          const elapsedSecs = Math.floor((Date.now() - session.savedAt) / 1000);
          const remaining = session.timerSecondsRemaining - elapsedSecs;
          if (remaining > 15) {
            appState.userAnswers = session.userAnswers || {};
            appState.timerSecondsRemaining = remaining;
            return { shouldResume: true };
          }
        }
        return false;
      } catch (e) {
        console.warn('Failed to restore session state', e);
        return false;
      }
    }

    function resumeActiveExam() {
      const current = appState.currentTestObj;
      if (!current || !current.questions) return;

      appState.examStatus = 'running';

      document.getElementById('exam-start-card').classList.add('hidden');
      document.getElementById('exam-results-card').classList.add('hidden');
      document.getElementById('exam-active-card').classList.remove('hidden');

      renderQuestionsFeed(current.questions);

      const totalQ = current.questions.length;
      const answeredKeys = Object.keys(appState.userAnswers);
      answeredKeys.forEach(qIdx => {
        const optIdx = appState.userAnswers[qIdx];
        for (let i = 0; i < 4; i++) {
          const btn = document.getElementById(`opt-btn-${qIdx}-${i}`);
          if (btn) {
            if (i === optIdx) {
              btn.className = "opt-btn w-full text-left p-3.5 rounded-xl border border-brand-500 bg-brand-950/80 text-white transition flex items-center gap-3 shadow-md glow-brand";
            } else {
              btn.className = "opt-btn w-full text-left p-3.5 rounded-xl border border-slate-700/80 bg-slate-950/70 hover:bg-slate-800/80 transition flex items-center gap-3 group";
            }
          }
        }
        const badge = document.getElementById(`q-status-badge-${qIdx}`);
        if (badge) {
          badge.innerText = "✓ উত্তর দেওয়া হয়েছে";
          badge.className = "text-[11px] font-bold text-emerald-400";
        }
      });

      document.getElementById('answered-count-pill').innerText = answeredKeys.length;
      document.getElementById('unanswered-count-pill').innerText = Math.max(0, totalQ - answeredKeys.length);
      document.getElementById('total-questions-pill').innerText = totalQ;
      const progBar = document.getElementById('exam-progress-bar');
      if (progBar && totalQ > 0) {
        progBar.style.width = `${Math.round((answeredKeys.length / totalQ) * 100)}%`;
      }

      startCountdownTimer();
      showToast("পূর্বে রেখে যাওয়া পরীক্ষা থেকে পুনরায় শুরু করা হয়েছে!", "info");
    }

    // ============================================
    // USER AUTHENTICATION & MULTI-DEVICE SYNC
    // ============================================
    let currentAuthMode = 'login';

    function openAuthModal() {
      const modal = document.getElementById('auth-modal');
      const card = document.getElementById('auth-modal-card');
      if (!modal || !card) return;
      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        card.classList.remove('scale-95', 'opacity-0');
        card.classList.add('scale-100', 'opacity-100');
      });
    }

    function closeAuthModal() {
      const modal = document.getElementById('auth-modal');
      const card = document.getElementById('auth-modal-card');
      if (!modal || modal.classList.contains('hidden')) return;
      if (card) {
        card.classList.remove('scale-100', 'opacity-100');
        card.classList.add('scale-95', 'opacity-0');
      }
      setTimeout(() => {
        modal.classList.add('hidden');
      }, 150);
    }

    function switchAuthTab(mode) {
      currentAuthMode = mode;
      const loginTab = document.getElementById('auth-tab-login');
      const signupTab = document.getElementById('auth-tab-signup');
      const nameContainer = document.getElementById('auth-name-container');
      const submitBtn = document.getElementById('btn-auth-submit');
      const feedback = document.getElementById('auth-feedback-msg');
      if (feedback) feedback.classList.add('hidden');

      if (mode === 'signup') {
        loginTab.className = "flex-1 py-2 rounded-xl text-slate-400 hover:text-white transition";
        signupTab.className = "flex-1 py-2 rounded-xl bg-brand-600 text-white shadow transition";
        nameContainer.classList.remove('hidden');
        submitBtn.innerHTML = `<span>নতুন একাউন্ট তৈরি করুন</span>`;
      } else {
        loginTab.className = "flex-1 py-2 rounded-xl bg-brand-600 text-white shadow transition";
        signupTab.className = "flex-1 py-2 rounded-xl text-slate-400 hover:text-white transition";
        nameContainer.classList.add('hidden');
        submitBtn.innerHTML = `<span>লগইন করুন</span>`;
      }
    }

    async function handleAuthSubmit() {
      const emailInput = document.getElementById('auth-input-email');
      const passInput = document.getElementById('auth-input-password');
      const nameInput = document.getElementById('auth-input-name');
      const feedback = document.getElementById('auth-feedback-msg');
      const btn = document.getElementById('btn-auth-submit');

      const email = emailInput ? emailInput.value.trim() : '';
      const password = passInput ? passInput.value.trim() : '';
      const name = nameInput ? nameInput.value.trim() : '';

      if (!email || !password) {
        if (feedback) {
          feedback.className = "text-xs p-2.5 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-200 block";
          feedback.innerText = "ইমেইল এবং পাসওয়ার্ড আবশ্যক।";
        }
        return;
      }

      btn.disabled = true;
      btn.innerHTML = `<span class="inline-block animate-spin mr-1">↻</span> অনুগ্রহ করে অপেক্ষা করুন...`;

      const endpoint = currentAuthMode === 'signup' ? '/api/auth/signup' : '/api/auth/login';
      const payload = {
        email,
        password,
        name: name || undefined,
        student_id: appState.studentId
      };

      try {
        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (res.ok && data.success) {
          localStorage.setItem('admission_user_token', data.token);
          localStorage.setItem('admission_user_email', data.email);
          if (data.name) localStorage.setItem('admission_user_name', data.name);
          if (data.student_id) {
            localStorage.setItem('admission_student_id', data.student_id);
            appState.studentId = data.student_id;
          }
          appState.userToken = data.token;
          appState.userEmail = data.email;
          appState.userName = data.name || data.email;

          if (data.medical_enrolled) {
            appState.isMedicalPaid = true;
            localStorage.setItem('admission_paid_med', 'true');
          }
          if (data.versity_enrolled) {
            appState.isVersityPaid = true;
            localStorage.setItem('admission_paid_var', 'true');
          }

          updateUnlockedBadges();
          populateTestDropdown();
          updateAuthUI();
          closeAuthModal();

          showToast(`স্বাগতম ${data.name || data.email}! আপনার একাউন্ট সক্রিয় হয়েছে।`, "success");
        } else {
          if (feedback) {
            feedback.className = "text-xs p-2.5 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-200 block";
            feedback.innerText = data.error || "প্রক্রিয়াটি সম্পন্ন করা যায়নি।";
          }
        }
      } catch (e) {
        if (feedback) {
          feedback.className = "text-xs p-2.5 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-200 block";
          feedback.innerText = "সার্ভার সংযোগে সমস্যা হয়েছে।";
        }
      } finally {
        btn.disabled = false;
        btn.innerHTML = `<span>${currentAuthMode === 'signup' ? 'নতুন একাউন্ট তৈরি করুন' : 'লগইন করুন'}</span>`;
      }
    }

    function handleUserLogout() {
      localStorage.removeItem('admission_user_token');
      localStorage.removeItem('admission_user_email');
      localStorage.removeItem('admission_user_name');
      appState.userToken = null;
      appState.userEmail = null;
      appState.userName = null;
      updateAuthUI();
      showToast("সফলভাবে লগআউট করা হয়েছে।", "info");
    }

    function updateAuthUI() {
      const container = document.getElementById('user-auth-widget');
      if (!container) return;

      if (appState.userEmail) {
        const isCombo = appState.isMedicalPaid && appState.isVersityPaid;
        const isMed = appState.isMedicalPaid;
        const isVar = appState.isVersityPaid;
        const badgeText = isCombo ? '★ কম্বো' : (isMed ? '★ মেডিকেল' : (isVar ? '★ ভার্সিটি' : 'ফ্রি মেম্বার'));

        container.innerHTML = `
          <div class="relative group">
            <button class="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-800/90 border border-slate-700 hover:border-slate-600 text-xs text-white font-bold transition">
              <span class="w-6 h-6 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/40 flex items-center justify-center text-[11px]">👤</span>
              <span class="max-w-[90px] sm:max-w-[130px] truncate">${appState.userName || appState.userEmail}</span>
              <span class="text-[10px] text-slate-400">▼</span>
            </button>
            <div class="absolute right-0 mt-1 w-56 bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-2 hidden group-hover:block z-50 space-y-1">
              <div class="px-3 py-2 border-b border-slate-800">
                <p class="text-[10px] text-slate-400">লগইন প্রোফাইল</p>
                <p class="text-xs font-bold text-white truncate">${appState.userEmail}</p>
                <p class="text-[10px] text-emerald-400 font-bold mt-1 font-mono">${badgeText}</p>
              </div>
              <button onclick="handleUserLogout()" class="w-full text-left px-3 py-2 text-xs text-rose-400 hover:bg-rose-950/40 hover:text-rose-300 rounded-xl transition flex items-center gap-2">
                <span>🚪</span> লগআউট করুন
              </button>
            </div>
          </div>
        `;
      } else {
        container.innerHTML = `
          <button onclick="openAuthModal()" class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-brand-600/90 to-teal-600/90 hover:from-brand-500 hover:to-teal-500 text-white text-xs font-extrabold shadow-sm transition border border-emerald-500/30">
            <span>👤</span>
            <span class="hidden sm:inline">লগইন / সাইন-আপ</span>
            <span class="sm:hidden">লগইন</span>
          </button>
        `;
      }
    }

    // ============================================
    // ADMIN PANEL & PAYMENT APPROVAL SYSTEM
    // ============================================
    let adminClaimsCache = [];
    let adminSmsCache = [];

    function openAdminModal() {
      const modal = document.getElementById('admin-panel-modal');
      const card = document.getElementById('admin-modal-card');
      if (!modal || !card) return;

      const adminToken = sessionStorage.getItem('admission_admin_token');
      if (adminToken) {
        document.getElementById('admin-login-view').classList.add('hidden');
        document.getElementById('admin-dashboard-view').classList.remove('hidden');
        loadAdminData();
      } else {
        document.getElementById('admin-login-view').classList.remove('hidden');
        document.getElementById('admin-dashboard-view').classList.add('hidden');
        const m = document.getElementById('admin-input-master');
        const s = document.getElementById('admin-input-secondary');
        const p = document.getElementById('admin-input-pin');
        const w = document.getElementById('admin-input-word');
        if (m) m.value = '';
        if (s) s.value = '';
        if (p) p.value = '';
        if (w) w.value = '';
      }

      modal.classList.remove('hidden');
      requestAnimationFrame(() => {
        card.classList.remove('scale-95', 'opacity-0');
        card.classList.add('scale-100', 'opacity-100');
      });
    }

    function closeAdminModal() {
      const modal = document.getElementById('admin-panel-modal');
      const card = document.getElementById('admin-modal-card');
      if (!modal || modal.classList.contains('hidden')) return;

      if (card) {
        card.classList.remove('scale-100', 'opacity-100');
        card.classList.add('scale-95', 'opacity-0');
      }
      setTimeout(() => {
        modal.classList.add('hidden');
        if (window.location.hash === '#admin') {
          history.replaceState(null, null, ' ');
        }
      }, 150);
    }

    async function handleAdminLoginSubmit() {
      const masterInput = document.getElementById('admin-input-master');
      const secondaryInput = document.getElementById('admin-input-secondary');
      const pinInput = document.getElementById('admin-input-pin');
      const wordInput = document.getElementById('admin-input-word');
      const feedback = document.getElementById('admin-login-feedback');
      const btn = document.getElementById('btn-admin-login-submit');

      const master_password_1 = masterInput ? masterInput.value.trim() : '';
      const secondary_password_2 = secondaryInput ? secondaryInput.value.trim() : '';
      const security_pin = pinInput ? pinInput.value.trim() : '';
      const security_word = wordInput ? wordInput.value.trim() : '';

      if (!master_password_1 || !secondary_password_2 || !security_pin || !security_word) {
        if (feedback) {
          feedback.className = "text-xs p-2.5 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-200 block";
          feedback.innerText = "৪টি সিকিউরিটি ফিল্ডই পূরণ করা আবশ্যক!";
        }
        return;
      }

      btn.disabled = true;
      btn.innerHTML = `<span class="inline-block animate-spin mr-1">↻</span> নিরাপত্তা যাচাই চলছে...`;

      try {
        const res = await fetch('/api/admin/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            master_password_1,
            secondary_password_2,
            security_pin,
            security_word
          })
        });
        const data = await res.json();
        if (res.ok && data.success) {
          sessionStorage.setItem('admission_admin_token', data.token);
          if (feedback) feedback.classList.add('hidden');
          document.getElementById('admin-login-view').classList.add('hidden');
          document.getElementById('admin-dashboard-view').classList.remove('hidden');
          loadAdminData();
          showToast("৪-ধাপ নিরাপত্তা যাচাই সফল! অ্যাডমিন প্যানেলে স্বাগতম।", "success");
        } else {
          if (feedback) {
            feedback.className = "text-xs p-2.5 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-200 block";
            feedback.innerText = data.message || "নিরাপত্তা যাচাই ব্যর্থ হয়েছে! তথ্য পরীক্ষা করুন।";
          }
        }
      } catch (e) {
        if (feedback) {
          feedback.className = "text-xs p-2.5 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-200 block";
          feedback.innerText = "সার্ভার সংযোগে ত্রুটি।";
        }
      } finally {
        btn.disabled = false;
        btn.innerHTML = `<span>🛡️ ৪-ধাপ নিরাপত্তা যাচাই ও প্রবেশ</span>`;
      }
    }

    function handleAdminLogout() {
      sessionStorage.removeItem('admission_admin_token');
      document.getElementById('admin-dashboard-view').classList.add('hidden');
      document.getElementById('admin-login-view').classList.remove('hidden');
      showToast("অ্যাডমিন প্যানেল থেকে লগআউট করা হয়েছে।", "info");
    }

    async function loadAdminData() {
      const token = sessionStorage.getItem('admission_admin_token');
      if (!token) return;

      try {
        const res = await fetch('/api/admin/payments', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.status === 401) {
          sessionStorage.removeItem('admission_admin_token');
          document.getElementById('admin-dashboard-view').classList.add('hidden');
          document.getElementById('admin-login-view').classList.remove('hidden');
          return;
        }
        const data = await res.json();
        if (!data.success) return;

        const m = data.metrics || {};
        document.getElementById('adm-metric-revenue').innerText = `৳${(m.total_revenue || 0).toLocaleString()}`;
        document.getElementById('adm-metric-verified').innerText = `${m.verified_students || 0} জন`;
        document.getElementById('adm-metric-pending').innerText = `${m.pending_claims || 0} টি`;
        document.getElementById('adm-metric-exams').innerText = `${m.total_exams || 0} টি`;

        adminClaimsCache = data.claims || [];
        adminSmsCache = data.sms_logs || [];

        document.getElementById('adm-claims-count').innerText = adminClaimsCache.length;
        document.getElementById('adm-sms-count').innerText = adminSmsCache.length;

        renderAdminClaimsTable(adminClaimsCache);
        renderAdminSmsTable(adminSmsCache);
      } catch (e) {
        console.error("Admin data load error:", e);
        showToast("অ্যাডমিন ডেটা লোড করতে সমস্যা হয়েছে।", "error");
      }
    }

    function renderAdminClaimsTable(claims) {
      const tbody = document.getElementById('adm-claims-tbody');
      const empty = document.getElementById('adm-claims-empty');
      if (!tbody) return;
      tbody.innerHTML = '';

      if (!claims || claims.length === 0) {
        if (empty) empty.classList.remove('hidden');
        return;
      }
      if (empty) empty.classList.add('hidden');

      claims.forEach(c => {
        const tr = document.createElement('tr');
        tr.className = "hover:bg-slate-800/40 transition";
        
        let statusBadge = '';
        if (c.status === 'verified') {
          statusBadge = '<span class="px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800 text-[10px] font-bold">✓ অনুমোদিত</span>';
        } else if (c.status === 'rejected') {
          statusBadge = '<span class="px-2 py-0.5 rounded-full bg-rose-950 text-rose-300 border border-rose-800 text-[10px] font-bold">✕ বাতিল</span>';
        } else {
          statusBadge = '<span class="px-2 py-0.5 rounded-full bg-amber-950 text-amber-300 border border-amber-800 text-[10px] font-bold animate-pulse">⏳ অপেক্ষমান</span>';
        }

        let actionButtons = '';
        if (c.status === 'pending') {
          actionButtons = `
            <div class="flex items-center justify-end gap-1.5">
              <button onclick="approveClaim('${c.trx_id}', ${c.id})" class="px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] shadow transition">
                ✓ অনুমোদন
              </button>
              <button onclick="rejectClaim('${c.trx_id}', ${c.id})" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-rose-950 hover:text-rose-300 text-slate-400 font-bold text-[11px] border border-slate-700 transition">
                ✕ বাতিল
              </button>
            </div>
          `;
        } else if (c.status === 'verified') {
          actionButtons = `<span class="text-[11px] text-emerald-400 font-semibold flex items-center justify-end gap-1"><span>🔓</span> টেস্ট আনলকড</span>`;
        } else {
          actionButtons = `
            <div class="flex items-center justify-end gap-1">
              <button onclick="approveClaim('${c.trx_id}', ${c.id})" class="px-2 py-0.5 rounded-lg bg-slate-800 hover:bg-emerald-600 hover:text-white text-slate-400 text-[10px] border border-slate-700 transition">
                পুনরায় অনুমোদন
              </button>
            </div>
          `;
        }

        const dateStr = c.created_at ? new Date(c.created_at).toLocaleString('bn-BD', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : '-';

        tr.innerHTML = `
          <td class="py-2.5 pr-2 text-slate-400 text-[11px] whitespace-nowrap">${dateStr}</td>
          <td class="py-2.5 px-2">
            <div class="font-bold text-white text-xs">${c.student_name || 'পরীক্ষার্থী'}</div>
            <div class="text-[10px] text-slate-400 truncate max-w-[140px]">${c.student_email || c.student_id || '-'}</div>
          </td>
          <td class="py-2.5 px-2 font-mono text-slate-300">${c.sender_number || '-'}</td>
          <td class="py-2.5 px-2">
            <span class="font-bold ${c.package === 'combo' ? 'text-purple-300' : (c.package === 'medical' ? 'text-emerald-300' : 'text-teal-300')} uppercase">${c.package}</span>
            <span class="text-[11px] text-slate-400 ml-1">৳${c.amount || (c.package === 'combo' ? 799 : 499)}</span>
          </td>
          <td class="py-2.5 px-2 font-mono font-bold text-amber-300 text-xs">${c.trx_id || '-'}</td>
          <td class="py-2.5 px-2">${statusBadge}</td>
          <td class="py-2.5 pl-2 text-right">${actionButtons}</td>
        `;
        tbody.appendChild(tr);
      });
    }

    function renderAdminSmsTable(smsLogs) {
      const tbody = document.getElementById('adm-sms-tbody');
      if (!tbody) return;
      tbody.innerHTML = '';

      if (!smsLogs || smsLogs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center py-8 text-slate-500 font-sans text-xs">এখনও কোনো ফরওয়ার্ডেড SMS আসেনি।</td></tr>`;
        return;
      }

      smsLogs.forEach(s => {
        const tr = document.createElement('tr');
        tr.className = "hover:bg-slate-800/40 transition";
        const dateStr = s.received_at ? new Date(s.received_at).toLocaleTimeString('bn-BD', { hour: '2-digit', minute: '2-digit', second: '2-digit' }) : '-';

        tr.innerHTML = `
          <td class="py-2 pr-2 text-slate-400 whitespace-nowrap">${dateStr}</td>
          <td class="py-2 px-2 text-slate-300">${s.sender || '-'}</td>
          <td class="py-2 px-2 font-bold text-emerald-400">৳${s.amount || '০'}</td>
          <td class="py-2 px-2 text-amber-300 font-bold">${s.trx_id || '-'}</td>
          <td class="py-2 px-2">${s.matched_claim_id ? `<span class="text-emerald-400">✓ ক্লেইম #${s.matched_claim_id}</span>` : `<span class="text-slate-500">আনক্লেইমড</span>`}</td>
          <td class="py-2 pl-2 text-slate-400 truncate max-w-xs" title="${s.raw_sms || ''}">${s.raw_sms || '-'}</td>
        `;
        tbody.appendChild(tr);
      });
    }

    function switchAdminTab(tab) {
      const claimsTab = document.getElementById('adm-tab-claims');
      const smsTab = document.getElementById('adm-tab-sms');
      const claimsContainer = document.getElementById('adm-claims-container');
      const smsContainer = document.getElementById('adm-sms-container');

      if (tab === 'claims') {
        claimsTab.className = "px-4 py-2 border-b-2 border-brand-500 text-brand-400 font-bold text-xs sm:text-sm flex items-center gap-1.5";
        smsTab.className = "px-4 py-2 border-b-2 border-transparent text-slate-400 hover:text-slate-300 font-bold text-xs sm:text-sm flex items-center gap-1.5";
        claimsContainer.classList.remove('hidden');
        smsContainer.classList.add('hidden');
      } else {
        smsTab.className = "px-4 py-2 border-b-2 border-brand-500 text-brand-400 font-bold text-xs sm:text-sm flex items-center gap-1.5";
        claimsTab.className = "px-4 py-2 border-b-2 border-transparent text-slate-400 hover:text-slate-300 font-bold text-xs sm:text-sm flex items-center gap-1.5";
        smsContainer.classList.remove('hidden');
        claimsContainer.classList.add('hidden');
      }
    }

    function refreshAdminData() {
      loadAdminData();
      showToast("অ্যাডমিন ডেটা রিফ্রেশ করা হয়েছে।", "info");
    }

    async function approveClaim(trxId, claimId) {
      const token = sessionStorage.getItem('admission_admin_token');
      if (!token) return;

      try {
        const res = await fetch('/api/admin/approve-payment', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ trx_id: trxId, claim_id: claimId })
        });
        const data = await res.json();
        if (res.ok && data.success) {
          showToast(data.message || "পেমেন্ট সফলভাবে অনুমোদিত হয়েছে!", "success");
          loadAdminData();
          syncPaymentStatus();
        } else {
          showToast(data.error || "অনুমোদন ব্যর্থ হয়েছে।", "error");
        }
      } catch (e) {
        showToast("সার্ভার সংযোগে সমস্যা।", "error");
      }
    }

    async function rejectClaim(trxId, claimId) {
      const token = sessionStorage.getItem('admission_admin_token');
      if (!token) return;

      try {
        const res = await fetch('/api/admin/reject-payment', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ trx_id: trxId, claim_id: claimId })
        });
        const data = await res.json();
        if (res.ok && data.success) {
          showToast("পেমেন্ট রিকোয়েস্ট বাতিল করা হয়েছে।", "info");
          loadAdminData();
        } else {
          showToast(data.error || "বাতিল করতে সমস্যা হয়েছে।", "error");
        }
      } catch (e) {
        showToast("সার্ভার সংযোগে সমস্যা।", "error");
      }
    }

    // ============================================
    // TOAST NOTIFICATIONS
    // ============================================
    function showToast(message, type = 'info') {
      const container = document.getElementById('toast-container');
      if (!container) return;

      const toast = document.createElement('div');
      let borderCol = 'border-slate-700 bg-slate-900 text-white';
      if (type === 'success') borderCol = 'border-emerald-500 bg-emerald-950 text-emerald-200';
      if (type === 'error') borderCol = 'border-rose-500 bg-rose-950 text-rose-200';

      toast.className = `px-4 py-3 rounded-2xl border shadow-2xl text-xs sm:text-sm font-bold flex items-center gap-2 transform transition duration-300 translate-x-12 opacity-0 pointer-events-auto ${borderCol}`;
      toast.innerHTML = `<span>${type === 'success' ? '✓' : (type === 'error' ? '⚠️' : 'ℹ️')}</span> <span>${message}</span>`;

      container.appendChild(toast);

      setTimeout(() => {
        toast.classList.remove('translate-x-12', 'opacity-0');
      }, 50);

      setTimeout(() => {
        toast.classList.add('translate-x-12', 'opacity-0');
        setTimeout(() => {
          if (toast && toast.remove) toast.remove();
          else if (toast && toast.parentNode) toast.parentNode.removeChild(toast);
        }, 300);
      }, 4000);
    }
  </script>

</body>
</html>
"""

portal_code = portal_code.replace('__DEFAULT_MED_TEST_1__', med_1_json).replace('__DEFAULT_VAR_TEST_1__', var_1_json)

ROOT_INDEX_FILE = os.path.join(BASE_DIR, "index.html")

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(portal_code)

with open(ROOT_INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(portal_code)

print(f"Successfully generated clean {INDEX_FILE} and {ROOT_INDEX_FILE} (size: {os.path.getsize(INDEX_FILE):,} bytes)")
