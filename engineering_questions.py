"""Original PCM exercises. Parameterised families, not authenticated past papers.
Each chapter mixes four foundation families and two application families.
"""
from fractions import Fraction as F
from original_practice import numeric, physics, higher_math, conceptual, read_facts


def application(cid, k, mode):
    # All quantities and domains are stated; rational answers stay exact.
    tables = {
      'math-1-01': [
        (f'A=[[{k},1],[2,3]] এবং B=2A⁻¹। det(B) কত?', F(4,3*k-2),'det(A)=3k−2; det(2A⁻¹)=2²/det(A)।'),
        (f'A=[[1,{k}],[0,1]]। A^{k+2}-এর প্রথম সারি, দ্বিতীয় কলামের উপাদান কত?',k*(k+2),'A=I+N, N²=0। তাই A^n=I+nN।')],
      'math-1-02': [
        (f'a=({k},2,0), b=(2,−{k},0)। |a×b|² কত?',(k*k+4)**2,'a×b=(0,0,−k²−4); এর মানের বর্গ (k²+4)²।'),
        (f'a=({k},2,0), b=(1,1,0)। a-এর b বরাবর ভেক্টর অভিক্ষেপের x উপাংশ কত?',F(k+2,2),'অভিক্ষেপ = (a·b)/|b|² ×b; a·b=k+2, |b|²=2।')],
      'math-1-03': [
        (f'({k},0), (0,{k+2}), (2,3) বিন্দু তিনটি দ্বারা গঠিত ত্রিভুজের ক্ষেত্রফল কত? সমরেখ হলে ক্ষেত্রফল শূন্য ধরো।',F(k*k-3*k-4,2) if k>=4 else F(abs(k*k-3*k-4),2),'ক্ষেত্রফল = ½|k(k+2)−3k−2(k+2)|।'),
        (f'({k},2) বিন্দু থেকে 3x+4y−{3*k+18}=0 রেখার দূরত্ব কত?',2,'বিন্দু-রেখা দূরত্ব = |3k+8−(3k+18)|/√(3²+4²)=10/5।')],
      'math-1-04': [
        (f'x²+y²−{2*k}x−4y+{k*k-21}=0 বৃত্তে কেন্দ্র থেকে 3 একক দূরের জ্যার দৈর্ঘ্য কত?',8,'কেন্দ্র (k,2), r²=k²+4−(k²−21)=25। জ্যা=2√(25−9)=8।'),
        (f'x²+y²={k*k} বৃত্তে ({k+3},0) থেকে অঙ্কিত স্পর্শকের দৈর্ঘ্যের বর্গ কত?',6*k+9,'স্পর্শকের দৈর্ঘ্যের বর্গ = OP²−r²=(k+3)²−k²।')],
      'math-1-05': [
        (f'{k+3} জনের মধ্যে নির্দিষ্ট 2 জনকে অবশ্যই নিয়ে 4 জনের কমিটি কতভাবে হবে?',(k+1)*k//2,'নির্দিষ্ট 2 জন স্থির। বাকি k+1 জন থেকে 2 জন নিতে হয়: C(k+1,2)।'),
        (f'{k+2}টি ভিন্ন বই থেকে 3টি একটি সারিতে সাজাতে হবে। নির্দিষ্ট একটি বই অবশ্যই থাকবে। কতভাবে সাজানো যায়?',3*(k+1)*k,'নির্দিষ্ট বইয়ের স্থান 3ভাবে; বাকি দুই স্থান P(k+1,2)ভাবে।')],
      'math-1-06': [
        (f'ত্রিভুজে a={3*k}, b={4*k}, c={5*k}। বৃহত্তম কোণের বিপরীত বাহুর উপর অঙ্কিত উচ্চতা কত?',F(12*k,5),'3:4:5 ত্রিভুজ সমকোণী। ক্ষেত্রফল=½(3k)(4k)=½(5k)h।'),
        (f'ত্রিভুজে a={k}, b={k+1}, অন্তর্ভুক্ত কোণ 60°। তৃতীয় বাহুর দৈর্ঘ্যের বর্গ কত?',k*k+k+1,'কোসাইন সূত্র: c²=a²+b²−2ab cos60°=a²+b²−ab।')],
      'math-1-07': [
        (f'θ সূক্ষ্মকোণ, tanθ={k}। cos2θ কত?',F(1-k*k,1+k*k),'cos2θ=(1−tan²θ)/(1+tan²θ)।'),
        (f'α,β সূক্ষ্মকোণ এবং tanα={k}, tanβ=1/{k+1}। tan(α−β) কত?',F(k*(k+1)-1,2*k+1),'tan(α−β)=(tanα−tanβ)/(1+tanαtanβ)।')],
      'math-1-08': [
        (f'f(x)=({k}x+1)/(x+1), x≠−1। f⁻¹(2) কত?',F(1,k-2) if k!=2 else 'অস্তিত্ব নেই','y=(kx+1)/(x+1) থেকে x=(1−y)/(y−k)। k=2 হলে 2 মানটি range-এ নেই।'),
        (f'f(x)=x²−{2*k}x+{k*k+3}। বাস্তব x-এর জন্য f-এর সর্বনিম্ন মান কত?',3,'পূর্ণবর্গে f(x)=(x−k)²+3; x=k-এ সর্বনিম্ন 3।')],
      'math-1-09': [
        (f'y=x^{k}e^(−x)। x={k}-এ y-এর একটি stationary point। ঐ বিন্দুতে y″/y কত?',F(-1,k),'ln y=k ln x−x; (ln y)′=k/x−1। stationary point-এ y″/y=(ln y)″=−k/x²।'),
        (f'x²+xy+y²={3*k*k} বক্ররেখায় ({k},{k}) বিন্দুতে d²y/dx² কত?',F(-2,3*k),'প্রথম অন্তরীকরণে 2x+y+(x+2y)y′=0, ফলে y′=−1। আবার অন্তরীকরণে 2+2y′+2(y′)²+(x+2y)y″=0।')],
      'math-1-10': [
        (f'∫₀¹ x(1−x)^{k} dx-এর মান কত?',F(1,(k+1)*(k+2)),'u=1−x দিলে ∫₀¹ (u^k−u^(k+1))du=1/(k+1)−1/(k+2)।'),
        (f'y=x ও y={k}x² বক্ররেখা দুটি দ্বারা আবদ্ধ ক্ষেত্রফল কত?',F(1,6*k*k),'ছেদবিন্দুর x=0 ও 1/k। ক্ষেত্রফল=∫₀^(1/k)(x−kx²)dx=1/(6k²)।')],
      'math-2-01': [
        (f'|2x−{2*k}|<{k} অসমতার সমাধান ব্যবধানের দৈর্ঘ্য কত?',k,'−k<2x−2k<k থেকে k/2<x<3k/2; দৈর্ঘ্য k।'),
        (f'x>0 হলে x+{k*k}/x-এর সর্বনিম্ন মান কত?',2*k,'AM≥GM থেকে x+k²/x≥2k; x=k-এ সমতা।')],
      'math-2-02': [
        (f'x,y≥0, x+y≤{k}, 2x+y≤{k+2}। 3x+2y-এর সর্বোচ্চ মান কত?',2*k+2,'কোণবিন্দু (0,0),(0,k),((k+2)/2,0),(2,k−2)। লক্ষ্যমানের সর্বোচ্চ 2k+2 (k≥2)।'),
        (f'x,y≥0, x+2y≥{2*k}, 2x+y≥{2*k}। x+y-এর সর্বনিম্ন মান কত?',F(4*k,3),'অসমতা যোগে 3(x+y)≥4k। x=y=2k/3-এ অর্জিত।')],
      'math-2-03': [
        (f'z=({k}+i)/({k}−i)। Im(z) কত?',F(2*k,k*k+1),'হরকে অনুবন্ধী দিয়ে বাস্তব করলে z=(k²−1+2ki)/(k²+1)।'),
        (f'z={k}+i। z²+z̄² কত?',2*(k*k-1),'z²=k²−1+2ki ও z̄²=k²−1−2ki; যোগে কাল্পনিক অংশ বাতিল।')],
      'math-2-04': [
        (f'x²−{k}x+1=0-এর মূল α,β। α³+β³ কত?',k**3-3*k,'α+β=k, αβ=1; α³+β³=(α+β)³−3αβ(α+β)।'),
        (f'x²−{k}x+2=0-এর মূল α,β। মূল α+1 ও β+1 বিশিষ্ট monic বহুপদীর ধ্রুব পদ কত?',k+3,'নতুন মূলের গুণফল = αβ+(α+β)+1=2+k+1।')],
      'math-2-05': [
        (f'(1+x)^{k+3}(1−x)²-এর বিস্তৃতিতে x²-এর সহগ কত?',(k+3)*(k+2)//2-2*(k+3)+1,'x² সহগ = C(k+3,2)−2C(k+3,1)+1।'),
        (f'(x+1/x)^{2*k}-এর বিস্তৃতিতে ধ্রুব পদটি কত নম্বর পদ? প্রথম পদ ১ নম্বর ধরা হবে।',k+1,'সাধারণ পদ C(2k,r)x^(2k−2r)। ধ্রুবের জন্য r=k; এটি (r+1) অর্থাৎ (k+1) নম্বর পদ।')],
      'math-2-06': [
        (f'x²/{25*k*k}+y²/{16*k*k}=1 উপবৃত্তের দীর্ঘ অক্ষের লম্ব ও উপকেন্দ্রগামী জ্যার দৈর্ঘ্য কত?',F(32*k,5),'উপবৃত্তে a=5k,b=4k; latus rectum-এর দৈর্ঘ্য 2b²/a=32k/5।'),
        (f'y²={4*k}x পরাবৃত্তে y={2*k} বিন্দুতে স্পর্শক x-অক্ষকে যেখানে ছেদ করে, তার x স্থানাঙ্ক কত?',-k,'বিন্দু (k,2k)। yy₁=2a(x+x₁) থেকে y=x+k; y=0 হলে x=−k।')],
      'math-2-07': [
        (f'0≤x<2π-এ sin({k}x)=1/2-এর সমাধান কতটি? k={k} একটি ধনাত্মক পূর্ণসংখ্যা।',2*k,'প্রতি পূর্ণ 2π চক্রে দুটি সমাধান; kx-এর ব্যবধান 0≤kx<2kπ।'),
        (f'tan⁻¹({k})+tan⁻¹(1/{k})-এর মানকে π দিয়ে ভাগ করে কত হয়? প্রধান মান রেডিয়ানে।',F(1,2),'k>0 হলে দুটি সূক্ষ্মকোণ পরস্পরের পূরক; যোগ π/2।')],
      'math-2-08': [
        (f'{k} N ও {k+4} N একই দিকের সমান্তরাল বলের ক্রিয়ারেখা 2 m দূরে। ছোট বলের রেখা থেকে লব্ধির দূরত্ব কত m?',F(k+4,k+2),'ছোট বলের রেখার সাপেক্ষে মুহূর্ত: R d=2(k+4), R=2k+4।'),
        (f'4 m সমসত্ত্ব অনুভূমিক বিমের ওজন {10*k} N। দুই প্রান্তে সমর্থন আছে। বাম প্রান্ত থেকে 1 m দূরে {20*k} N ভার ঝুলছে। ডান সমর্থনের প্রতিক্রিয়া কত N?',10*k,'বাম প্রান্তের সাপেক্ষে মুহূর্ত: 4R=2(10k)+1(20k), ফলে R=10k।')],
      'math-2-09': [
        (f'একই উচ্চতা থেকে নিক্ষিপ্ত প্রক্ষেপকের ux={3*k} m/s, uy={4*k} m/s। g=10 m/s² ও বায়ুর বাধা উপেক্ষণীয়। পাল্লা কত m?',F(12*k*k,5),'উড্ডয়নকাল 2uy/g=4k/5; R=ux×T।'),
        (f'এক কণার x(t)={k}t³−{3*k}t², x মিটারে ও t সেকেন্ডে। 0 থেকে 3 s-এ মোট অতিক্রান্ত পথ কত m?',8*k,'v=3kt(t−2); t=2-এ দিক বদলায়। x(0)=0,x(2)=−4k,x(3)=0; মোট পথ 8k।')],
      'math-2-10': [
        (f'ব্যাগে {k}টি লাল ও 3টি নীল বল। প্রতিস্থাপন ছাড়া দুটি তোলা হলে উভয়টি লাল হওয়ার সম্ভাবনা কত?',F(k*(k-1),(k+3)*(k+2)),'প্রথম লাল k/(k+3), এরপর লাল (k−1)/(k+2); গুণ করতে হবে।'),
        (f'এক চলকের variance={k}। Y=3X+{k+2} হলে Y-এর variance কত?',9*k,'Var(aX+b)=a²Var(X); ধ্রুবক বিচ্যুতি পরিবর্তন করে না।')],
      'physics-1-01': [
        (f'গোলকের ব্যাসার্ধ {k} cm ও তার আপেক্ষিক পরম ত্রুটি 0.02। প্রথম ক্রমে আয়তনের শতকরা ত্রুটি কত?',6,'V∝r³; dV/V≈3dr/r=0.06।'),
        (f'v={2*k} m/s এবং t={k} s; দুটির আপেক্ষিক ত্রুটি যথাক্রমে 0.02 ও 0.03। s=vt-তে প্রথম ক্রমের সর্বোচ্চ শতকরা ত্রুটি কত?',5,'গুণফলে সর্বোচ্চ আপেক্ষিক ত্রুটি যোগ হয়: 2%+3%=5%।')],
      'physics-1-02': [
        (f'A=({k},2,0), B=(2,−{k},0)। |A+B|² কত?',2*k*k+8,'A+B=(k+2,2−k,0); বর্গমান (k+2)²+(2−k)²।'),
        (f'একই মান {k} N-এর দুটি বলের মধ্যবর্তী কোণ 120°। লব্ধির মান কত N?',k,'R²=F²+F²+2F²cos120°=F²।')],
      'physics-1-03': [
        (f'ট্রেনের বেগ {2*k} m/s। ব্রেক দিলে 2 m/s² ধ্রুব মন্দন হয়। থামার আগে কত m যাবে?',k*k,'v²=u²+2as; v=0,a=−2 থেকে s=u²/4=k²।'),
        (f'একই উচ্চতা থেকে ux={3*k}, uy={4*k} m/s-এ প্রক্ষেপণ করা হলো। g=10 m/s²। সর্বোচ্চ উচ্চতা কত m?',F(4*k*k,5),'শীর্ষে উল্লম্ব বেগ শূন্য; H=uy²/(2g)=16k²/20।')],
      'physics-1-04': [
        (f'মসৃণ তলে {k} kg ভরের বস্তু 6 m/s-এ এসে স্থির {2*k} kg বস্তুর সঙ্গে সম্পূর্ণ অস্থিতিস্থাপক সংঘর্ষ করে। যৌথ বেগ কত m/s?',2,'ভরবেগ সংরক্ষণে k×6=(k+2k)v; v=2।'),
        (f'মসৃণ তলে সংযুক্ত {k} kg ও {2*k} kg দুই ব্লককে মোট {12*k} N বল দিয়ে টানা হয়। ক্ষুদ্র ব্লকের উপর লব্ধি বল কত N?',4*k,'সমগ্র সিস্টেমের ত্বরণ=12k/(3k)=4; ছোট ব্লকের লব্ধি F=k×4।')],
      'physics-1-05': [
        (f'{k} kg বস্তু 6 m/s থেকে 2 m/s-এ ধীর হয়। ঘর্ষণ ছাড়া অন্য কোনো বল কাজ না করলে ঘর্ষণের কাজ কত J?',-16*k,'কাজ-শক্তি উপপাদ্য W=½m(v²−u²)=½k(4−36)।'),
        (f'{20*k} N/m স্প্রিংকে 0.2 m সংকুচিত করে মসৃণ তলে {k} kg বস্তু ছাড়া হলো। স্প্রিংয়ের স্বাভাবিক দৈর্ঘ্যে বস্তুর বেগের বর্গ কত m²/s²?',F(4,5),'½Kx²=½mv²; v²=Kx²/m=(20k)(0.04)/k=0.8।')],
      'physics-1-06': [
        (f'এক গোলাকার গ্রহের ব্যাসার্ধ R, পৃষ্ঠে g={10*k} m/s²। কেন্দ্র থেকে 3R ব্যাসার্ধের বৃত্তাকার কক্ষপথে v²/R কত m/s²?',F(10*k,3),'v²=GM/(3R), g=GM/R²; v²/R=g/3।'),
        (f'সমঘনত্বের এক গোলাকার গ্রহের পৃষ্ঠে g={10*k} m/s²। R/4 গভীরতায় g কত m/s²?',F(15*k,2),'সমঘনত্বের মডেলে g(d)=g₀(1−d/R); d=R/4 হলে 3g₀/4।')],
      'physics-1-07': [
        (f'এক তারের দৈর্ঘ্য {k} m, ক্ষেত্রফল 2×10⁻⁶ m², Young modulus 2×10¹¹ Pa। 40 N টানে দৈর্ঘ্য বৃদ্ধি কত mm?',F(k,10),'ΔL=FL/(AY)=40k/(4×10⁵) m=k×10⁻⁴ m=0.1k mm।'),
        (f'ঘনত্ব {600*k} kg/m³ বস্তুকে ঘনত্ব {1000*k} kg/m³ তরলে ভাসালে আয়তনের কত অংশ ডুবে থাকবে?',F(3,5),'ভাসমান সাম্যে ρবস্তু Vg=ρতরল Vডুব g; অনুপাত=ρবস্তু/ρতরল।')],
      'physics-1-08': [
        (f'দুটি সমান স্প্রিংয়ের প্রত্যেকটির ধ্রুবক {20*k} N/m। একই ভরকে একবার শ্রেণিতে, একবার সমান্তরালে যুক্ত করে দোলালে Tশ্রেণি/Tসমান্তরাল কত?',2,'Kশ্রেণি=K/2, Kসমান্তরাল=2K; T∝1/√K, অনুপাত √4=2।'),
        (f'SHM-এ বিস্তার {2*k} cm এবং ω=5 rad/s। সাম্য থেকে {k} cm দূরে বেগের বর্গ কত cm²/s²?',75*k*k,'v²=ω²(A²−x²)=25(4k²−k²)।')],
      'physics-1-09': [
        (f'তারের টান {10*k} N-এ কম্পাঙ্ক 200 Hz। একই তারে টান {40*k} N হলে কম্পাঙ্ক কত Hz?',400,'f∝√T; টান 4 গুণ হলে কম্পাঙ্ক 2 গুণ।'),
        (f'স্থির শ্রোতার দিকে উৎস {k} m/s বেগে আসে। শব্দের বেগ 340 m/s, উৎসের কম্পাঙ্ক 680 Hz। পর্যবেক্ষিত কম্পাঙ্ক কত Hz?',F(231200,340-k),'ডপলার সূত্র f′=fv/(v−vs); এখানে vs<v।')],
      'physics-1-10': [
        (f'{k} mol আদর্শ গ্যাসের তাপমাত্রা 300 K থেকে 600 K ও চাপ P থেকে 3P হয়। Vশেষ/Vপ্রথম কত?',F(2,3),'PV=nRT; একই n-এ V₂/V₁=(T₂/T₁)(P₁/P₂)=2/3।'),
        (f'একই তাপমাত্রায় ভিন্ন দুটি গ্যাসের molar mass {4*k} ও {9*k} g/mol। প্রথমটির rms বেগ/দ্বিতীয়টির rms বেগ কত?',F(3,2),'vrms=√(3RT/M); অনুপাত √(M₂/M₁)=3/2।')],
      'physics-2-01': [
        (f'কার্নো ইঞ্জিন Th={k+400} K, Tc={k+200} K। উষ্ণ উৎস থেকে {10*(k+400)} J তাপ নিলে প্রতি চক্রে কাজ কত J?',2000,'η=1−Tc/Th=200/(k+400); W=ηQh=2000 J।'),
        (f'{k} mol একপরমাণুক আদর্শ গ্যাসকে সমচাপে 20 K উত্তপ্ত করা হলো। R=8 J mol⁻¹ K⁻¹। গ্যাসের কাজ কত J?',160*k,'সমচাপীয় কাজে W=PΔV=nRΔT; 20×8k।')],
      'physics-2-02': [
        (f'একটি পাতলা লেন্সের বায়ুতে ফোকাস দৈর্ঘ্য {k} cm। দুটি একই লেন্স সংস্পর্শে রাখলে যৌথ ফোকাস দৈর্ঘ্য কত cm?',F(k,2),'সংস্পর্শে লেন্সের ক্ষমতা যোগ হয়: 1/F=1/f+1/f।'),
        (f'উত্তল লেন্সে বাস্তব বস্তুর দূরত্ব {3*k} cm ও ফোকাস {k} cm। পর্দায় বাস্তব বিম্বের দূরত্ব কত cm?',F(3*k,2),'দূরত্বের ধনাত্মক মানে 1/f=1/u+1/v; 1/v=1/k−1/(3k)।')],
      'physics-2-03': [
        (f'প্রতিটি {k} μF-এর তিনটি ধারক: দুটি সমান্তরালে, সেই সমন্বয় তৃতীয়টির সঙ্গে শ্রেণিতে। তুল্য ধারকত্ব কত μF?',F(2*k,3),'সমান্তরালে 2C; শ্রেণিতে Ceq=(2C×C)/(2C+C)=2C/3।'),
        (f'এক ধারকে C={k} μF, V=20 V। উৎস বিচ্ছিন্ন করে dielectric constant 4-এর পদার্থ সম্পূর্ণ ঢোকালে নতুন বিভব কত V?',5,'উৎস বিচ্ছিন্ন বলে Q স্থির; C′=4C, V′=Q/C′=V/4।')],
      'physics-2-04': [
        (f'EMF={k+10} V, অভ্যন্তরীণ রোধ 2 Ω। বাহ্যিক রোধ 3 Ω। টার্মিনাল বিভব কত V?',F(3*(k+10),5),'I=E/(R+r)=E/5; টার্মিনাল বিভব IR=3E/5।'),
        (f'{k} Ω ও {2*k} Ω রোধ সমান্তরালে যুক্ত। সমন্বয়ে 6 A প্রবেশ করলে ছোট রোধে প্রবাহ কত A?',4,'সমান্তরালে বিভব সমান; Iছোট:Iবড়=2:1। মোট 6 A হলে 4 A ও 2 A।')],
      'physics-2-05': [
        (f'চার্জ q={k} C, বেগ v=3 m/s ও B=4 T পরস্পর লম্ব। কণা একই B-তে দ্বিগুণ বেগে গেলে বলের মান কত N?',24*k,'চৌম্বক বল F=qvB sin90°; নতুন v=6, তাই F=24k।'),
        (f'এক আধানের ভর {2*k} kg, আধান {k} C, বেগ 6 m/s। বেগ 3 T ক্ষেত্রের লম্ব। বৃত্তাকার পথের ব্যাসার্ধ কত m?',4,'qvB=mv²/r; r=mv/(qB)=(2k×6)/(k×3)।')],
      'physics-2-06': [
        (f'কয়েলের পাক {k+10}, ক্ষেত্রফল 0.02 m²। লম্ব B 0.5 T থেকে 0.1 T-এ 0.2 s-এ নামে। গড় আবিষ্ট EMF-এর মান কত V?',F(k+10,25),'|E|=NA|ΔB|/Δt=N×0.02×0.4/0.2=0.04N।'),
        (f'আদর্শ ট্রান্সফরমারে Np:Ns=5:1। প্রাথমিক বিভব {10*k} V এবং গৌণ প্রবাহ 2 A। প্রাথমিক প্রবাহ কত A?',F(2,5),'আদর্শ ট্রান্সফরমারে Ip/Is=Ns/Np=1/5; বিভব অনুপাত আলাদা তথ্য।')],
      'physics-2-07': [
        (f'ইয়ং পরীক্ষায় λ=500 nm, D={k} m, d=0.5 mm। সমগ্র পথ জল (n=4/3) দিয়ে পূর্ণ করলে fringe width কত mm?',F(3*k,4),'বায়ুতে β=λD/d=k mm। মাধ্যমে λ′=λ/n, ফলে β′=3k/4 mm।'),
        (f'দুটি polarizer-এর অক্ষ 60° কোণে। প্রথম polarizer-এর পরে তীব্রতা {8*k} W/m²। দ্বিতীয়টির পরে তীব্রতা কত W/m²?',2*k,'ম্যালাসের সূত্র I=I₁ cos²60°=I₁/4। প্রথমটির পরের তীব্রতা দেওয়া আছে।')],
      'physics-2-08': [
        (f'এক ধাতুর work function 2 eV। {k+4} eV ফোটনে নির্গত ইলেকট্রনের stopping potential কত V?',k+2,'Kmax=hν−φ=(k+4)−2 eV। eVs=Kmax; eV-এ শক্তির সংখ্যামান volt-এ বিভব।'),
        (f'এক অ-আপেক্ষিক কণার গতিশক্তি {k} J থেকে {4*k} J করা হলো। নতুন de Broglie তরঙ্গদৈর্ঘ্য/পুরনো তরঙ্গদৈর্ঘ্য কত?',F(1,2),'λ=h/√(2mK); একই ভরে K চারগুণ হলে λ অর্ধেক।')],
      'physics-2-09': [
        (f'একটি নমুনার অর্ধায়ু {k} দিন। মূল নমুনার 7/8 ক্ষয় হতে কত দিন লাগবে?',3*k,'অবশিষ্ট 1/8=1/2³; তিন অর্ধায়ু সময় লাগে।'),
        (f'প্রথমে সক্রিয়তা {8*k} Bq। 3টি অর্ধায়ু পরে প্রতি সেকেন্ডে ক্ষয়সংখ্যা কত?',k,'A=A₀(1/2)³=8k/8।')],
      'physics-2-10': [
        (f'ট্রানজিস্টরের β={k+20}। common-base current gain α কত?',F(k+20,k+21),'β=Ic/Ib; Ie=Ic+Ib। α=Ic/Ie=β/(β+1)।'),
        (f'0.7 V forward-drop মডেলের ডায়োড 1 kΩ রোধের সঙ্গে {k+1.7:g} V উৎসে forward biased। রোধে ক্ষমতা কত mW?',(k+1)**2,'I=(Vs−0.7)/1kΩ=(k+1)mA; P=I²R=(k+1)² mW।')],
      'physics-2-11': [
        (f'এক নক্ষত্রের একই আলোকক্ষমতায় দূরত্ব {k} pc থেকে {3*k} pc করলে apparent intensity-এর অনুপাত Iশেষ/Iপ্রথম কত?',F(1,9),'I=L/(4πr²); দূরত্ব 3 গুণ হলে তীব্রতা 1/9।'),
        (f'এক নক্ষত্রের parallax angle 1/{k} arcsecond। দূরত্ব কত parsec?',k,'d(pc)=1/p(arcsecond); p=1/k হলে d=k।')],
      'chemistry-1-02': [
        (f'হাইড্রোজেন-সদৃশ আয়নে nuclear charge Z={k}। n=2 স্তরে শক্তি কত eV? Eₙ=−13.6Z²/n²।',F(-17*k*k,5),'n=2 বসালে E=−13.6k²/4=−3.4k² eV।'),
        (f'প্রধান quantum number n={k} স্তরে সর্বোচ্চ কত electron থাকতে পারে?',2*k*k,'একটি shell-এর সর্বোচ্চ electron capacity 2n²; subshell capacity নয়।')],
      'chemistry-1-03': [
        (f'{k} mol NH₄⁺ আয়নের সব valence electron একত্রে গণনা করলে কত mol electron হয়?',8*k,'প্রতি NH₄⁺-এ N-এর 5+চার H-এর 4−চার্জের 1=8 valence electron। k mol আয়নে 8k mol electron।'),
        (f'এক homonuclear diatomic ion-এ bonding electron {2*k+4}, antibonding electron {2*k}। bond order কত?',2,'bond order=(Nb−Na)/2=(2k+4−2k)/2=2।')],
      'chemistry-1-04': [
        (f'A⇌B বিক্রিয়ার K={k}। একই তাপমাত্রায় 2B⇌2A-এর equilibrium constant কত?',F(1,k*k),'বিক্রিয়া উল্টালে K→1/K; সহগ দ্বিগুণ হলে square, তাই 1/K²।'),
        (f'প্রথম ক্রমের বিক্রিয়ার অর্ধায়ু {k} min। 75% reactant ক্ষয় হতে কত min?',2*k,'25%=1/4 অবশিষ্ট মানে দুই half-life; t=2t½।')],
      'chemistry-1-05': [
        (f'{k} kg খাদ্যে 0.02% (ভরভিত্তিক) preservative মেশানো হলো। preservative কত g?',F(k,5),'0.02%=0.0002; k kg×0.0002×1000=0.2k g।'),
        (f'{100*k} g জলভিত্তিক পণ্যে 200 ppm (ভরভিত্তিক) solute আছে। solute কত mg?',20*k,'200 ppm=200 mg/kg। 100k g=0.1k kg; solute=20k mg।')],
      'chemistry-2-01': [
        (f'{k} mol ideal gas 300 K ও 2 atm-এ আছে। R=0.082 L atm mol⁻¹ K⁻¹। আয়তন কত L?',F(123*k,10),'PV=nRT; V=k×0.082×300/2=12.3k L।'),
        (f'O₂ ও N₂-এর molar mass 32 ও 28 g/mol। একই তাপমাত্রায় rN₂/rO₂ অনুপাতের বর্গ কত? নমুনার চাপ {k} atm।',F(8,7),'গ্রাহামের সূত্রে r∝1/√M; অনুপাতের বর্গ=32/28=8/7। চাপ একই হওয়ায় অনুপাত বদলায় না।')],
      'chemistry-2-02': [
        (f'এক open-chain saturated monohydric alcohol-এ carbon atom {k}টি। H atom কতটি?',2*k+2,'এই শ্রেণির সাধারণ সূত্র CnH(2n+2)O; cyclic বা unsaturated alcohol নয়।'),
        (f'এক acyclic alkene-এ একটি মাত্র C=C আছে এবং carbon atom {k+2}টি। H atom কতটি?',2*(k+2),'একটি double bond-সহ open-chain alkene-এর সাধারণ সূত্র CnH2n।')],
      'chemistry-2-03': [
        (f'{k} mL 0.2 M HCl নিরপেক্ষ করতে 0.1 M Ca(OH)₂ কত mL লাগবে?',k,'Ca(OH)₂+2HCl→CaCl₂+2H₂O; 2×0.1V=0.2k, তাই V=k mL।'),
        (f'{k} g NaOH (molar mass 40 g/mol) দিয়ে 250 mL দ্রবণ বানালে molarity কত M?',F(k,10),'mol=k/40, V=0.25 L; M=(k/40)/0.25=k/10।')],
      'chemistry-2-04': [
        (f'Ag⁺+e⁻→Ag। {k} F charge প্রবাহে কত mol Ag জমবে? current efficiency 100%।',k,'এক mol Ag-এর জন্য এক Faraday; n=Q/(zF), z=1।'),
        (f'Cu²⁺+2e⁻→Cu। {k} F charge-এ কত mol Cu জমবে? current efficiency 100%।',F(k,2),'প্রতি mol Cu-তে 2F লাগে; n=k/2 mol।')],
      'chemistry-2-05': [
        (f'{k} kg সারেতে 46% nitrogen (ভরভিত্তিক) আছে। nitrogen কত kg?',F(23*k,50),'nitrogen mass=0.46×fertilizer mass।'),
        (f'এক উৎপাদনে theoretical yield {10*k} kg ও actual yield {8*k} kg। percent yield কত?',80,'percent yield=actual/theoretical×100=(8k)/(10k)×100=80%।')],
    }
    return tables[cid][mode]


def chapter_pool(book, chapter, track):
    cid=chapter['id']; subject=book['subject']; offset=0 if track=='buet' else 40
    questions=[]; seen=set()
    def add(stem,answer,solution,family,level):
        if stem in seen:return
        seen.add(stem)
        if isinstance(answer,str):
            from original_practice import item
            distractors={
              'অ্যাসিডকে জলে':['জলকে অ্যাসিডে','দুটিকে একসঙ্গে ঢালতে হবে','বন্ধ পাত্রে জোরে ঝাঁকাতে হবে'],
              'মেনিস্কাসের সমতলে':['মেনিস্কাসের অনেক উপরে','মেনিস্কাসের অনেক নিচে','যেকোনো উচ্চতায়'],
              'অস্তিত্ব নেই':['0','1','2']}
            q=item(cid,stem,[answer]+distractors[answer],answer,solution,'original_concept',[family])
        else:
            q=numeric(cid,stem,answer,solution,family)
            if 'সম্ভাবনা' in stem:
                # All four options are admissible probabilities; no giveaway by domain.
                from original_practice import item, fmt
                a=F(answer)
                candidates=[a,a/2,(a+1)/2,1-a,(2*a+1)/3,a/3]
                values=[]
                for x in candidates:
                    if 0<=x<=1 and x not in values:values.append(x)
                    if len(values)==4:break
                assert len(values)==4
                q=item(cid,stem,[fmt(x) for x in values],fmt(a),solution+f' তাই উত্তর {fmt(a)}।','worked_numerical',[f'{cid}-numeric-{family+1}'])

        q.update(subject=subject,chapter_id=cid,origin='original_practice',review_status='formula_checked_not_teacher_reviewed',difficulty=level,problem_family_id=family,source_files=['engineering_questions.py','original_practice.py'],book_reference='HSC অধ্যায়ের মৌলিক অনুশীলনী · বিগত পরীক্ষার প্রশ্ন বা বইয়ের উদ্ধৃতি নয়')
        questions.append(q)
    if subject in ('Physics','HigherMath'):
        solver=physics if subject=='Physics' else higher_math
        # 4 foundation and 2 application families; BUET has a larger application share.
        foundation=40 if track=='buet' else 60
        for n in range(foundation):
            mode=n%4; k=2+offset+n//4
            add(*solver(cid,k,mode),mode,'foundation')
        for n in range(100-foundation):
            mode=n%2; k=2+offset+n//2
            add(*application(cid,k,mode),4+mode,'application')
    else:
        # 200 distinct concept pairs + 100 worked applications, shared concept core disclosed.
        rows=read_facts()[cid]
        for q in conceptual(cid,rows,200):
            q.update(subject=subject,chapter_id=cid,review_status='authored_not_teacher_reviewed',difficulty='concept',problem_family_id='two_statement',book_reference='HSC অধ্যায়ের মৌলিক অনুশীলনী · বিগত পরীক্ষার প্রশ্ন বা বইয়ের উদ্ধৃতি নয়')
            questions.append(q);seen.add(q['question_bn'])
        # Safety chapters use the concept core only; artificial sample numbers are not question variety.
        if cid=='chemistry-1-01':
            for q in conceptual(cid,rows,300)[200:]:
                q.update(subject=subject,chapter_id=cid,review_status='authored_not_teacher_reviewed',difficulty='concept',problem_family_id='two_statement')
                questions.append(q)
        else:
            for n in range(100):
                mode=n%2;k=2+offset+n//2
                add(*application(cid,k,mode),4+mode,'application')
    target=300 if subject=='Chemistry' else 100
    assert len(questions)==target,(cid,track,len(questions))
    assert len({q['id'] for q in questions})==target
    return questions
