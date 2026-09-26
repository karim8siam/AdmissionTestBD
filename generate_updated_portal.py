import os

PORTAL_SCRIPT = "/Users/karimsiam/.gemini/antigravity/scratch/medical-100-test-series/build_full_portal.py"

with open(PORTAL_SCRIPT, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect where to insert the student profile bar and ranking cards
# 1. Search for test info banner
profile_bar_html = """
      <!-- Student Identity & Admission Season Bar -->
      <div class="bg-slate-800/90 rounded-2xl p-5 border border-slate-700/80 shadow-lg flex flex-col md:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-3 w-full md:w-auto">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-ai-600 flex items-center justify-center font-bold text-white text-lg shrink-0 shadow-md">
            🎓
          </div>
          <div>
            <h3 class="text-sm font-bold text-white flex items-center gap-2">
              পরীক্ষার্থীর প্রোফাইল ও সেশন নির্বাচন
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-ai-900/80 text-ai-300 border border-ai-700 font-semibold">লাইভ র‍্যাংকিং সক্রিয়</span>
            </h3>
            <p class="text-xs text-slate-400">তোমার স্কোর সরাসরি চলতি সেশন এবং সর্বকালের জাতীয় মেধা তালিকায় রেকর্ড হবে।</p>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full md:w-auto">
          <!-- Student Name -->
          <div>
            <label class="block text-[10px] uppercase font-bold text-slate-400 mb-1">পরীক্ষার্থীর নাম</label>
            <input type="text" id="student-name-input" placeholder="তোমার নাম লিখুন..." value="সাকিব আহমেদ" 
                   class="w-full px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-900 text-white text-xs font-semibold focus:outline-none focus:ring-1 focus:ring-brand-500">
          </div>

          <!-- Target College -->
          <div>
            <label class="block text-[10px] uppercase font-bold text-slate-400 mb-1">টার্গেট মেডিকেল কলেজ</label>
            <select id="student-target-select" class="w-full px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-900 text-white text-xs font-semibold focus:outline-none focus:ring-1 focus:ring-brand-500">
              <option value="Dhaka Medical College (DMC)" selected>ঢাকা মেডিকেল কলেজ (DMC)</option>
              <option value="Sir Salimullah Medical College (SSMC)">স্যার সলিমুল্লাহ মেডিকেল কলেজ (SSMC)</option>
              <option value="Shaheed Suhrawardy Medical College (ShSMC)">শহীদ সোহরাওয়ার্দী মেডিকেল কলেজ</option>
              <option value="Chittagong Medical College (CMC)">চট্টগ্রাম মেডিকেল কলেজ (CMC)</option>
              <option value="Rajshahi Medical College (RMC)">রাজশাহী মেডিকেল কলেজ (RMC)</option>
              <option value="Mymensingh Medical College (MMC)">ময়মনসিংহ মেডিকেল কলেজ (MMC)</option>
              <option value="MAG Osmani Medical College (SOMC)">সিলেট এমএজি ওসমানী মেডিকেল কলেজ</option>
              <option value="Sher-e-Bangla Medical College (SBMC)">শের-ই-বাংলা মেডিকেল কলেজ (বরিশাল)</option>
              <option value="Top Government Medical College">শীর্ষ সরকারি মেডিকেল কলেজ</option>
            </select>
          </div>

          <!-- Admission Season -->
          <div>
            <label class="block text-[10px] uppercase font-bold text-brand-400 mb-1 flex items-center gap-1">
              <span>ভর্তি সেশন / Season</span>
              <span class="w-1.5 h-1.5 rounded-full bg-brand-400 animate-pulse"></span>
            </label>
            <select id="student-session-select" class="w-full px-3 py-1.5 rounded-lg border border-brand-500/60 bg-slate-900 text-brand-300 text-xs font-bold focus:outline-none focus:ring-1 focus:ring-brand-500">
              <option value="2025-26" selected>২০২৫-২৬ সেশন (চলতি সেশন)</option>
              <option value="2026-27">২০২৬-২৭ সেশন (পরবর্তী সেশন / Next Year)</option>
              <option value="2024-25">২০২৪-২৫ সেশন (বিগত সেশন)</option>
              <option value="2027-28">২০২৭-২৮ সেশন (ভবিষ্যৎ সেশন)</option>
            </select>
          </div>
        </div>
      </div>
"""

ranking_cards_html = """
        <!-- National Merit Ranking Highlight Banner -->
        <div class="p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950/60 to-slate-900 border border-indigo-800/60 shadow-xl space-y-4">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
            <div>
              <span class="text-[10px] uppercase tracking-wider font-extrabold px-2.5 py-0.5 rounded-full bg-indigo-900/80 text-indigo-300 border border-indigo-700">
                Official National Admission Ranking
              </span>
              <h4 class="text-xl font-extrabold text-white mt-1 flex items-center gap-2">
                <span>তোমার জাতীয় মেধা অবস্থান ও পার্সেন্টাইল</span>
                <span class="text-xs font-normal text-slate-400">(সেশন ও সর্বকালের সমন্বিত)</span>
              </h4>
            </div>
            <button onclick="openLeaderboardModal()" class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs transition shadow-lg shadow-indigo-600/30 flex items-center gap-2">
              <span>🏅 মেধা তালিকা ও লিডারবোর্ড দেখুন</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            <!-- All-Time Merit Stand -->
            <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-700/80 space-y-2 relative overflow-hidden group">
              <div class="absolute -right-4 -bottom-4 w-20 h-20 bg-amber-500/10 rounded-full blur-xl"></div>
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-amber-400 flex items-center gap-1.5">
                  <span>🏆 সর্বকালের মেধা অবস্থান (All-Time Rank)</span>
                </span>
                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-950 text-amber-300 border border-amber-800" id="alltime-percentile-badge">
                  টপ ০.৫%
                </span>
              </div>
              <div class="flex items-baseline gap-2">
                <span class="text-3xl sm:text-4xl font-black text-white" id="alltime-rank-display">#--</span>
                <span class="text-xs text-slate-400 font-medium" id="alltime-total-display">সর্বমোট -- জন পরীক্ষার্থীর মধ্যে</span>
              </div>
              <p class="text-xs text-slate-400" id="alltime-rank-summary">
                প্ল্যাটফর্মে আজ পর্যন্ত সকল সেশনের যত শিক্ষার্থী এই মডেল টেস্ট দিয়েছে তাদের সম্মিলিত মেধা তালিকায় তোমার অবস্থান।
              </p>
            </div>

            <!-- Season Merit Stand -->
            <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-700/80 space-y-2 relative overflow-hidden group">
              <div class="absolute -right-4 -bottom-4 w-20 h-20 bg-emerald-500/10 rounded-full blur-xl"></div>
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-brand-400 flex items-center gap-1.5">
                  <span id="season-rank-title">🎓 চলতি সেশন (২০২৫-২৬) মেধা অবস্থান</span>
                </span>
                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-brand-950 text-brand-300 border border-brand-800" id="season-percentile-badge">
                  টপ ০.৩%
                </span>
              </div>
              <div class="flex items-baseline gap-2">
                <span class="text-3xl sm:text-4xl font-black text-brand-300" id="season-rank-display">#--</span>
                <span class="text-xs text-slate-400 font-medium" id="season-total-display">এই সেশনের -- জন পরীক্ষার্থীর মধ্যে</span>
              </div>
              <p class="text-xs text-slate-400" id="season-rank-summary">
                নির্দিষ্ট এই ভর্তি সেশনের পরীক্ষার্থীদের মধ্যে তোমার তাৎক্ষণিক অবস্থান ও মেধা পার্সেন্টাইল।
              </p>
            </div>

          </div>
        </div>
"""

leaderboard_modal_html = """
  <!-- ============================================== -->
  <!-- MODAL: NATIONAL MERIT LEADERBOARD -->
  <!-- ============================================== -->
  <div id="leaderboard-modal" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm hidden flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 rounded-3xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col shadow-2xl animate-in fade-in zoom-in duration-200">
      
      <!-- Modal Header -->
      <div class="p-6 border-b border-slate-800 flex items-center justify-between bg-slate-900/90">
        <div>
          <div class="flex items-center gap-2">
            <span class="text-xl">🏆</span>
            <h3 class="text-xl font-bold text-white">জাতীয় মেধা তালিকা ও লিডারবোর্ড (Merit Standings)</h3>
          </div>
          <p class="text-xs text-slate-400 mt-1" id="leaderboard-modal-subtitle">মডেল টেস্ট ০১ • ডিজিএমই সেন্ট্রাল স্ট্যান্ডার্ড</p>
        </div>
        <button onclick="closeLeaderboardModal()" class="w-8 h-8 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center text-sm font-bold transition">
          ✕
        </button>
      </div>

      <!-- Leaderboard Tabs Switcher -->
      <div class="px-6 py-3 bg-slate-950/60 border-b border-slate-800 flex items-center justify-between gap-4">
        <div class="inline-flex rounded-xl bg-slate-800/80 p-1 border border-slate-700 text-xs font-semibold">
          <button onclick="switchLeaderboardTab('session')" id="lb-tab-session" class="px-4 py-1.5 rounded-lg bg-brand-600 text-white shadow transition">
            🎓 চলতি সেশন (<span id="lb-session-label">2025-26</span>) মেধা তালিকা
          </button>
          <button onclick="switchLeaderboardTab('all_time')" id="lb-tab-alltime" class="px-4 py-1.5 rounded-lg text-slate-400 hover:text-white transition">
            🌟 সর্বকালের সেরা (All-Time Hall of Fame)
          </button>
        </div>
        <div class="text-xs text-slate-400 hidden sm:block">
          <span class="w-2 h-2 rounded-full bg-brand-400 inline-block mr-1"></span> লাইভ ডাটাবেজ আপডেট
        </div>
      </div>

      <!-- Leaderboard Table Container -->
      <div class="p-6 overflow-y-auto flex-1 custom-scrollbar">
        <div class="rounded-2xl border border-slate-800 overflow-hidden">
          <table class="w-full text-left text-xs text-slate-300">
            <thead class="bg-slate-950 text-slate-400 uppercase font-bold text-[10px] tracking-wider">
              <tr>
                <th class="p-3.5 text-center w-16">মেধাক্রম</th>
                <th class="p-3.5">পরীক্ষার্থীর নাম</th>
                <th class="p-3.5">টার্গেট কলেজ</th>
                <th class="p-3.5 text-center">সেশন</th>
                <th class="p-3.5 text-center">স্কোর</th>
                <th class="p-3.5 text-center">সময়</th>
              </tr>
            </thead>
            <tbody id="leaderboard-table-body" class="divide-y divide-slate-800/60 bg-slate-900/60 font-medium">
              <!-- Injected by JS -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="p-4 border-t border-slate-800 bg-slate-950/80 flex items-center justify-between text-xs text-slate-400">
        <p>প্রতিটি সাবমিশন ডাটাবেজে সংরক্ষণ করে রিয়েল-টাইম টাই-ব্রেকার (স্কোর ও সময়) অনুযায়ী মেধাক্রম নির্ধারিত হয়।</p>
        <button onclick="closeLeaderboardModal()" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold transition">
          বন্ধ করুন
        </button>
      </div>

    </div>
  </div>
"""

print("Writing modified build_full_portal.py...")

# Inject profile_bar_html right before Top Test Info Banner
if 'id="current-test-title"' in content:
    # Insert profile bar above Top Test Info Banner
    target_pos = content.find('<!-- Top Test Info Banner -->')
    if target_pos != -1:
        content = content[:target_pos] + profile_bar_html + "\n\n      " + content[target_pos:]
        print("Injected Student Identity & Session Selector bar.")

# Inject ranking_cards_html inside exam-scoreboard right after the 4 metric cards
target_scoreboard = content.find('<!-- College Prediction & AI 24-Hour Prescription -->')
if target_scoreboard != -1:
    content = content[:target_scoreboard] + ranking_cards_html + "\n\n        " + content[target_scoreboard:]
    print("Injected National Merit Ranking highlight cards.")

# Inject leaderboard modal right before </body>
target_body_end = content.find('</body>')
if target_body_end != -1:
    content = content[:target_body_end] + leaderboard_modal_html + "\n" + content[target_body_end:]
    print("Injected Leaderboard Modal.")

with open(PORTAL_SCRIPT, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated build_full_portal.py structure successfully!")
