"""Original chapter practice: explicit concept/misconception pairs and worked numericals.

All generated items are labelled original_practice. Concept pairs are combined once
per chapter; changing statement order alone never creates a new question. Numerical
items are parameterised exercises, not claimed to test 100 different concepts.
"""
import hashlib
import itertools
import math
import random
from fractions import Fraction
from pathlib import Path


def fmt(n):
    if isinstance(n, Fraction):
        return str(n)
    if isinstance(n, str):
        return n
    return f'{n:.8g}'


def item(cid, stem, options, answer, explanation, kind, concepts):
    uid = hashlib.sha256(('original:' + cid + ':' + stem).encode()).hexdigest()[:16]
    opts = list(options)
    assert len(opts) == len(set(opts)) == 4, (cid, stem, opts)
    random.Random(uid).shuffle(opts)
    return {'id': uid, 'question_bn': stem, 'options': opts,
            'correct_index': opts.index(answer), 'explanation': explanation,
            'book_reference': 'অধ্যায়ভিত্তিক মৌলিক অনুশীলনী · বইয়ের সরাসরি উদ্ধৃতি নয়',
            'source_files': ['original_practice.py', 'content/original_facts.txt'],
            'origin': 'original_practice', 'question_type': kind, 'concept_ids': concepts}


def read_facts():
    facts = {}
    cid = None
    for line in (Path(__file__).parent / 'content/original_facts.txt').read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('['):
            cid = line[1:-1]
            assert cid not in facts
            facts[cid] = []
        else:
            parts = line.rsplit('|', 2)
            assert len(parts) == 3 and all(parts) and parts[1] != parts[2], (cid, line)
            assert parts[0] not in [r[0] for r in facts[cid]], (cid, line)
            facts[cid].append(parts)
    return facts


def conceptual(cid, rows, count):
    pairs = list(itertools.combinations(range(len(rows)), 2))
    assert len(pairs) >= count, (cid, len(rows), count)
    random.Random(cid).shuffle(pairs)
    choices = ['শুধু i সঠিক', 'শুধু ii সঠিক', 'i ও ii উভয়ই সঠিক', 'i ও ii কোনোটিই সঠিক নয়']
    result = []
    for n, (a, b) in enumerate(pairs[:count]):
        # Four truth patterns alternate; each unordered concept pair appears once.
        mask = n % 4
        t1, t2 = bool(mask & 1), bool(mask & 2)
        r1, r2 = rows[a], rows[b]
        s1, s2 = r1[1 if t1 else 2], r2[1 if t2 else 2]
        stem = f'নিচের দুটি বক্তব্য বিচার করো।\ni. {r1[0]}: {s1}।\nii. {r2[0]}: {s2}।\nকোন উত্তরটি সঠিক?'
        answer = choices[{1: 0, 2: 1, 3: 2, 0: 3}[mask]]
        explanation = f'i {"সঠিক" if t1 else "ভুল"}; {r1[0]}: {r1[1]}। ii {"সঠিক" if t2 else "ভুল"}; {r2[0]}: {r2[1]}।'
        result.append(item(cid, stem, choices, answer, explanation, 'two_statement',
                           [f'{cid}-concept-{a+1:02}', f'{cid}-concept-{b+1:02}']))
    return result


def numeric(cid, stem, answer, solution, family):
    answer = Fraction(answer) if isinstance(answer, int) else answer
    if isinstance(answer, Fraction):
        values = [answer, answer + 1, answer + 2, answer - 1]
    else:
        delta = max(abs(answer) * .15, .5)
        values = [answer, answer + delta, answer + 2*delta, answer + 3*delta]
    options = [fmt(v) for v in values]
    return item(cid, stem, options, fmt(answer), solution + f' তাই উত্তর {fmt(answer)}।',
                'worked_numerical', [f'{cid}-numeric-{family+1}'])


def physics(cid, k, m):
    g = 10
    tables = {
        'physics-1-01': [
            (f'{k} cm দৈর্ঘ্য কত m?', Fraction(k,100), '1 cm = 0.01 m; দৈর্ঘ্যকে 100 দিয়ে ভাগ করতে হয়।'),
            (f'একটি মাপ {k*10} mm এবং পরম ত্রুটি 1 mm। শতকরা ত্রুটি কত?', Fraction(10,k), 'শতকরা ত্রুটি = পরম ত্রুটি/মাপ ×100।'),
            (f'{k} kg ভর কত g?', k*1000, '1 kg = 1000 g।'),
            (f'{k} cm বাহুর বর্গের ক্ষেত্রফল কত cm²?', k*k, 'ক্ষেত্রফল = বাহু²।')],
        'physics-1-02': [
            (f'পরস্পর লম্ব {3*k} N ও {4*k} N বলের লব্ধির মান কত N?',5*k,'R=√(A²+B²); 3:4:5 ত্রিভুজ।'),
            (f'একই দিকে {k} m ও {k+5} m সরণের লব্ধি কত m?',2*k+5,'একই দিকের ভেক্টরের মান যোগ হয়।'),
            (f'{2*k} N বল ও {3*k} m সরণের মধ্যবর্তী কোণ 60°। ডট গুণফল কত J?',3*k*k,'F·s=Fs cos60°=Fs/2।'),
            (f'{2*k} ও {3*k} মানের দুটি ভেক্টর পরস্পর লম্ব। ক্রস গুণফলের মান কত?',6*k*k,'|A×B|=AB sin90°=AB।')],
        'physics-1-03': [
            (f'স্থির অবস্থা থেকে {k} m/s² ত্বরণে 4 s চললে বেগ কত m/s?',4*k,'v=u+at; u=0।'),
            (f'স্থির অবস্থা থেকে {k} m/s² ত্বরণে 4 s চললে সরণ কত m?',8*k,'s=ut+½at²; u=0।'),
            (f'{k} m/s সমবেগে 12 s চললে দূরত্ব কত m?',12*k,'দূরত্ব = বেগ × সময়।'),
            (f'{2*k} m/s বেগে সোজা উপরে নিক্ষেপে শীর্ষে পৌঁছাতে কত s? g=10 m/s²।',Fraction(k,5),'শীর্ষে v=0; t=u/g।')],
        'physics-1-04': [
            (f'{k} kg ভরের বস্তুর ত্বরণ 3 m/s²। লব্ধি বল কত N?',3*k,'F=ma।'),
            (f'{k} kg ভরের বস্তু 5 m/s বেগে চলে। ভরবেগ কত kg·m/s?',5*k,'p=mv।'),
            (f'{k} N ধ্রুব বল 4 s কাজ করলে ইমপালস কত N·s?',4*k,'J=FΔt।'),
            (f'অনুভূমিক তলে {k} kg বস্তুর μ=0.2। সীমান্ত ঘর্ষণ কত N? g=10।',2*k,'f=μN=μmg।')],
        'physics-1-05': [
            (f'{k} N বলের দিকে 8 m সরণে কাজ কত J?',8*k,'W=Fs cos0°।'),
            (f'{2*k} kg ভরের বস্তুর বেগ 3 m/s। গতিশক্তি কত J?',9*k,'K=½mv²।'),
            (f'{k} kg ভর 4 m উঁচু করলে বিভবশক্তি বৃদ্ধি কত J? g=10।',40*k,'ΔU=mgh।'),
            (f'{120*k} J কাজ 6 s-এ সম্পন্ন হলে ক্ষমতা কত W?',20*k,'P=W/t।')],
        'physics-1-06': [
            (f'পৃথিবীপৃষ্ঠে {k} kg ভরের ওজন কত N? g=10।',10*k,'ওজন = mg।'),
            (f'দুটি ভরের মহাকর্ষীয় বল {16*k} N। দূরত্ব দ্বিগুণ করলে বল কত N?',4*k,'F∝1/r²; দ্বিগুণ দূরত্বে এক-চতুর্থাংশ।'),
            (f'পৃথিবীর পৃষ্ঠে g={4*k} m/s² ধরা হলে কেন্দ্র থেকে 2R দূরে g কত m/s²?',k,'g(r)=g(R)(R/r)²।'),
            (f'এক গ্রহে কক্ষীয় বেগ {k} km/s। একই ব্যাসার্ধে মুক্তিবেগের বর্গ কত (km/s)²?',2*k*k,'ve=√2 vc; তাই ve²=2vc²।')],
        'physics-1-07': [
            (f'{10*k} N বল {2*k} m² ক্ষেত্রফলে লম্বভাবে কাজ করে। পীড়ন কত Pa?',5,'পীড়ন = বল/ক্ষেত্রফল।'),
            (f'মূল দৈর্ঘ্য 100 cm, দৈর্ঘ্য বৃদ্ধি {k} cm। বিকৃতি কত?',Fraction(k,100),'বিকৃতি = দৈর্ঘ্য বৃদ্ধি/মূল দৈর্ঘ্য।'),
            (f'স্প্রিং ধ্রুবক {20*k} N/m; প্রসারণ 0.1 m। বলের মান কত N?',2*k,'হুকের সূত্র F=kx।'),
            (f'ঘনত্ব {100*k} kg/m³ তরলে 2 m গভীরে গেজ চাপ কত Pa? g=10।',2000*k,'p=ρgh।')],
        'physics-1-08': [
            (f'SHM-এ A={k} cm। এক পূর্ণ চক্রে মোট চলা দূরত্ব কত cm?',4*k,'এক চক্রে মোট পথ 4A।'),
            (f'কম্পাঙ্ক {k} Hz হলে পর্যায়কাল কত s?',Fraction(1,k),'T=1/f।'),
            (f'SHM-এ ω=4 rad/s ও A={k} m। সর্বোচ্চ বেগ কত m/s?',4*k,'vmax=ωA।'),
            (f'SHM-এ ω=3 rad/s ও x={k} m। ত্বরণের মান কত m/s²?',9*k,'a=−ω²x; মান ω²|x|।')],
        'physics-1-09': [
            (f'কম্পাঙ্ক {k} Hz ও তরঙ্গদৈর্ঘ্য 4 m। তরঙ্গবেগ কত m/s?',4*k,'v=fλ।'),
            (f'তরঙ্গবেগ {10*k} m/s ও কম্পাঙ্ক 5 Hz। তরঙ্গদৈর্ঘ্য কত m?',2*k,'λ=v/f।'),
            (f'বদ্ধ নলের দৈর্ঘ্য {k} m ও শব্দবেগ 320 m/s। মূল কম্পাঙ্ক কত Hz?',Fraction(80,k),'একপ্রান্ত বদ্ধ নলে f=v/(4L)।'),
            (f'খোলা নলের দৈর্ঘ্য {k} m ও শব্দবেগ 320 m/s। মূল কম্পাঙ্ক কত Hz?',Fraction(160,k),'দুইপ্রান্ত খোলা নলে f=v/(2L)।')],
        'physics-1-10': [
            (f'স্থির T-তে V দ্বিগুণ হলে প্রাথমিক {4*k} Pa চাপের শেষ মান কত Pa?',2*k,'বয়েলের সূত্র PV=ধ্রুবক।'),
            (f'স্থির P-তে গ্যাসের T 300 K থেকে 600 K; প্রাথমিক V={k} L। শেষ V কত L?',2*k,'চার্লসের সূত্র V/T=ধ্রুবক।'),
            (f'গ্যাসের n={k} mol, RT=1000 J/mol। PV কত J?',1000*k,'আদর্শ গ্যাসে PV=nRT।'),
            (f'গ্যাসের rms বেগ প্রথমে {k} m/s। পরম তাপমাত্রা চারগুণ হলে rms বেগ কত m/s?',2*k,'vrms∝√T।')],
        'physics-2-01': [
            (f'গ্যাসকে Q={10*k} J তাপ দেওয়া হয়, গ্যাস W={3*k} J কাজ করে। ΔU কত J?',7*k,'ΔU=Q−W; W হলো গ্যাসের করা কাজ।'),
            (f'এক ইঞ্জিন Qh={10*k} J নেয় ও Qc={6*k} J ছাড়ে। কাজ কত J?',4*k,'W=Qh−Qc।'),
            (f'কার্নো ইঞ্জিনে Th=600 K ও Tc=300 K। {10*k} J তাপ নিলে কাজ কত J?',5*k,'η=1−Tc/Th=½; W=ηQh।'),
            (f'{k} kg পদার্থের c=200 J/(kg·K), ΔT=5 K। তাপ কত J?',1000*k,'Q=mcΔT।')],
        'physics-2-02': [
            (f'চার্জ {k} C-এর ওপর 4 N/C ক্ষেত্র। বল কত N?',4*k,'F=qE।'),
            (f'{k} C চার্জ 12 V বিভব পার্থক্য অতিক্রমে বিভবশক্তির মান কত J?',12*k,'|ΔU|=|qΔV|।'),
            (f'ধারক C={k} μF, V=10 V। চার্জ কত μC?',10*k,'Q=CV।'),
            (f'ধারক C={2*k} F, V=3 V। সঞ্চিত শক্তি কত J?',9*k,'U=½CV²।')],
        'physics-2-03': [
            (f'রোধ {k} Ω-এর মধ্যে I=3 A। বিভব পার্থক্য কত V?',3*k,'V=IR।'),
            (f'I={k} A ধারা 8 s চললে চার্জ কত C?',8*k,'Q=It।'),
            (f'R={k} Ω ও I=2 A। তাপীয় ক্ষমতা কত W?',4*k,'P=I²R।'),
            (f'{k} Ω ও {2*k} Ω রোধ শ্রেণিতে। তুল্য রোধ কত Ω?',3*k,'শ্রেণিতে R=R1+R2।')],
        'physics-2-04': [
            (f'B=2 T-তে লম্বভাবে {k} m/s বেগে q=3 C। চৌম্বক বলের মান কত N?',6*k,'F=qvB sin90°।'),
            (f'B=0.5 T-তে লম্ব L=2 m তারে I={k} A। বল কত N?',k,'F=BIL sin90°।'),
            (f'এক লুপের I={k} A ও ক্ষেত্রফল 3 m²। চৌম্বক দ্বিমেরু মুহূর্ত কত A·m²?',3*k,'μ=IA।'),
            (f'μ={k} A·m², B=2 T, কোণ 90°। টর্ক কত N·m?',2*k,'τ=μB sinθ।')],
        'physics-2-05': [
            (f'N={k} পাক; প্রতি পাকে ফ্লাক্স 0 থেকে 6 Wb হয় 2 s-এ। emf-এর মান কত V?',3*k,'|ε|=N|ΔΦ|/Δt।'),
            (f'L={k} H; ধারা পরিবর্তনের হার 4 A/s। আবিষ্ট emf-এর মান কত V?',4*k,'|ε|=L|dI/dt|।'),
            (f'L={2*k} H ও I=3 A। সঞ্চিত চৌম্বক শক্তি কত J?',9*k,'U=½LI²।'),
            (f'আদর্শ ট্রান্সফরমারে Ns/Np=3 ও Vp={k} V। Vs কত V?',3*k,'Vs/Vp=Ns/Np।')],
        'physics-2-06': [
            (f'প্রতিসরাঙ্ক n={k+1}/{k} মাধ্যমের আলোর বেগ কত ×10^8 m/s? c=3×10^8।',Fraction(3*k,k+1),'v=c/n।'),
            (f'উত্তল লেন্সের f={k} cm। বস্তু 2f দূরে; বাস্তব প্রতিবিম্ব দূরত্ব কত cm?',2*k,'1/f=1/u+1/v; u=2f হলে v=2f (দূরত্বের মান)।'),
            (f'অবতল দর্পণের বক্রতার ব্যাসার্ধ {2*k} cm। ফোকাস দূরত্বের মান কত cm?',k,'f=R/2।'),
            (f'লেন্সের ফোকাস দূরত্ব {k} m। ক্ষমতার মান কত D?',Fraction(1,k),'P=1/f; f মিটারে।')],
        'physics-2-07': [
            (f'ইয়ং পরীক্ষায় λ=500 nm, D={k} m, d=1 mm। ফ্রিঞ্জ প্রস্থ কত mm?',Fraction(k,2),'β=λD/d; nm ও mm-কে SI-তে রূপান্তর।'),
            (f'ফ্রিঞ্জ প্রস্থ প্রথমে {k} mm। পর্দার দূরত্ব দ্বিগুণ করলে কত mm?',2*k,'β∝D।'),
            (f'ফ্রিঞ্জ প্রস্থ প্রথমে {2*k} mm। চিরের ব্যবধান দ্বিগুণ করলে কত mm?',k,'β∝1/d।'),
            (f'ম্যালাসের সূত্রে I0={4*k} W/m² ও θ=60°। I কত W/m²?',k,'I=I0 cos²θ=I0/4।')],
        'physics-2-08': [
            (f'এক ফোটনের E={k} eV ও কাজ ফাংশন 1 eV। সর্বোচ্চ ইলেকট্রন গতিশক্তি কত eV?',k-1,'Kmax=hf−φ=E−φ।'),
            (f'এক ফোটনের শক্তি {k} eV। একই কম্পাঙ্কের 5 ফোটনের শক্তি কত eV?',5*k,'মোট শক্তি = ফোটন সংখ্যা × এক ফোটনের শক্তি।'),
            (f'ডি ব্রগলি তরঙ্গদৈর্ঘ্য {2*k} nm। ভরবেগ দ্বিগুণ করলে λ কত nm?',k,'λ=h/p।'),
            (f'এক ইলেকট্রন {k} V বিভব পার্থক্যে ত্বরিত হলে অর্জিত শক্তি কত eV?',k,'এক ইলেকট্রন 1 V-এ 1 eV অর্জন করে।')],
        'physics-2-09': [
            (f'নিউক্লিয়াসের A={3*k}, Z={k}। নিউট্রন কতটি?',2*k,'N=A−Z।'),
            (f'প্রাথমিক {8*k} টি নিউক্লিয়াস তিন অর্ধায়ু পরে অবশিষ্ট কতটি?',k,'N=N0/2³।'),
            (f'হাইড্রোজেনের En=−13.6/n² eV। n={k} স্তরে শক্তি কত eV?',Fraction(-68,5*k*k),'En=−13.6/n²; প্রদত্ত n বসাতে হবে।'),
            (f'প্রাথমিক সক্রিয়তা {4*k} Bq। দুই অর্ধায়ু পরে কত Bq?',k,'A=A0/2²।')],
        'physics-2-10': [
            (f'ট্রানজিস্টরে IB={k} μA ও β=50। IC কত μA?',50*k,'IC=βIB।'),
            (f'ট্রানজিস্টরে IC={9*k} mA ও IB={k} mA। IE কত mA?',10*k,'IE=IC+IB।'),
            (f'ডায়োডের সরল মডেলে VD=0.7 V। উৎস {k+1.7:g} V ও সিরিজ রোধ 1 kΩ। I কত mA?',k+1,'I=(Vs−VD)/R; 1 V/1 kΩ=1 mA।'),
            (f'পূর্ণতরঙ্গ রেকটিফায়ারের ইনপুট কম্পাঙ্ক {k*10} Hz। আউটপুট রিপল কম্পাঙ্ক কত Hz?',k*20,'পূর্ণতরঙ্গ রেকটিফিকেশনে রিপল কম্পাঙ্ক 2f।')],
        'physics-2-11': [
            (f'কেপলারের নিয়মে P²=a³, P বছরে ও a AU-তে। a={k*k} AU হলে P কত বছর?',k**3,'P=a^(3/2)।'),
            (f'Hubble সম্পর্ক v=H0d; H0=70 km/s/Mpc ও d={k} Mpc। v কত km/s?',70*k,'v=H0d।'),
            (f'আলো 1 s-এ 3×10^8 m যায়। {k} s-এ কত ×10^8 m যাবে?',3*k,'দূরত্ব = আলোর বেগ × সময়।'),
            (f'এক নক্ষত্রের আলোকক্ষমতা অপরিবর্তিত; {k} একক দূরত্বে তীব্রতা {4*k}। {2*k} একক দূরে তীব্রতা কত?',k,'I∝1/r²; দ্বিগুণ দূরত্বে এক-চতুর্থাংশ।')],
    }
    return tables[cid][m]


def higher_math(cid, k, m):
    tables = {
        'math-1-01': [
            (f'A=[[{k},2],[3,4]] হলে det(A) কত?',4*k-6,'2×2 নির্ণায়ক = ad−bc।'),
            (f'A=[[{k},1],[2,3]] হলে trace(A) কত?',k+3,'ট্রেস = প্রধান কর্ণের যোগফল।'),
            (f'2×2 ম্যাট্রিক্সের det(A)={k}। det(3A) কত?',9*k,'n×n ম্যাট্রিক্সে det(cA)=c^n det(A)।'),
            (f'det(A)={k} ও det(B)=5। det(AB) কত?',5*k,'det(AB)=det(A)det(B)।')],
        'math-1-02': [
            (f'a=({k},2), b=(3,4)। a·b কত?',3*k+8,'ডট গুণফল = a1b1+a2b2।'),
            (f'a=({3*k},{4*k}) হলে |a| কত?',5*k,'|a|=√(a1²+a2²)।'),
            (f'a=({k},2), b=(3,4)। a+b-এর প্রথম উপাংশ কত?',k+3,'ভেক্টর যোগে সমস্থানীয় উপাংশ যোগ হয়।'),
            (f'a=({k},2,0), b=(1,3,0)। a×b-এর z উপাংশ কত?',3*k-2,'z উপাংশ = a1b2−a2b1।')],
        'math-1-03': [
            (f'y={k}x+4 রেখার ঢাল কত?',k,'y=mx+c রূপে ঢাল m।'),
            (f'({k},0) ও (0,{k+2}) রেখার x ও y অক্ষখণ্ডের যোগ কত?',2*k+2,'দেওয়া বিন্দু দুটি অক্ষখণ্ড নির্ধারণ করে।'),
            (f'({k},2) ও ({k+4},6) বিন্দুর মধ্যবিন্দুর x স্থানাঙ্ক কত?',k+2,'মধ্যবিন্দুর x=(x1+x2)/2।'),
            (f'y={k}x+2 রেখার লম্ব রেখার ঢাল কত?',Fraction(-1,k),'লম্ব রেখার ঢালের গুণফল −1।')],
        'math-1-04': [
            (f'x²+y²={k*k} বৃত্তের ব্যাসার্ধ কত?',k,'কেন্দ্র মূলবিন্দু হলে x²+y²=r²।'),
            (f'(x−{k})²+(y−2)²=9 বৃত্তের কেন্দ্রের x স্থানাঙ্ক কত?',k,'(x−h)²+(y−v)²=r²-এ কেন্দ্র (h,v)।'),
            (f'বৃত্তের ব্যাসার্ধ {k} হলে ব্যাস কত?',2*k,'ব্যাস = 2r।'),
            (f'x²+y²−{2*k}x+4y+{k*k-5}=0 বৃত্তের ব্যাসার্ধ কত?',3,'পূর্ণবর্গে (x−k)²+(y+2)²=9।')],
        'math-1-05': [
            (f'{k+2}টি ভিন্ন বস্তু থেকে 2টি নির্বাচন কতভাবে?',(k+2)*(k+1)//2,'nC2=n(n−1)/2।'),
            (f'{k+2}টি ভিন্ন বস্তু থেকে 2টি ক্রমসহ সাজানো কতভাবে?',(k+2)*(k+1),'nP2=n(n−1)।'),
            (f'{k+1}টি শার্ট ও 3টি প্যান্ট থেকে একটি করে বাছাই কতভাবে?',3*(k+1),'গুণন নীতি: প্রথম পছন্দ × দ্বিতীয় পছন্দ।'),
            (f'{k+1}টি ভিন্ন বই থেকে একটি অথবা 4টি ভিন্ন কলম থেকে একটি বাছাই কতভাবে?',k+5,'বিকল্প বিচ্ছিন্ন হলে যোগন নীতি।')],
        'math-1-06': [
            (f'{2*k}sin30°-এর মান কত?',k,'sin30°=½।'),
            (f'{2*k}cos60°-এর মান কত?',k,'cos60°=½।'),
            (f'{k}tan45°-এর মান কত?',k,'tan45°=1।'),
            (f'sin²θ+cos²θ=1 ব্যবহার করে {k}(sin²θ+cos²θ) কত?',k,'মৌলিক অভেদ sin²θ+cos²θ=1।')],
        'math-1-07': [
            (f'{2*k}sin(30°+60°)-এর মান কত?',2*k,'sin(30°+60°)=sin90°=1।'),
            (f'{k}cos(60°−60°)-এর মান কত?',k,'cos0°=1।'),
            (f'sinθ=3/5 ও cosθ=4/5। {25*k}sin2θ কত?',24*k,'sin2θ=2sinθcosθ=24/25।'),
            (f'cosθ=4/5। {25*k}cos2θ কত?',7*k,'cos2θ=2cos²θ−1=7/25।')],
        'math-1-08': [
            (f'f(x)={k}x+3 হলে f(2) কত?',2*k+3,'ফাংশনে x=2 বসাতে হবে।'),
            (f'f(x)=x²+{k} হলে f(3) কত?',k+9,'f(3)=3²+k।'),
            (f'f(x)=x+{k}, g(x)=2x। f(g(4)) কত?',k+8,'প্রথমে g(4)=8, তারপর f(8)=8+k।'),
            (f'f(x)=x+{k} হলে f⁻¹(0) কত?',-k,'y=x+k থেকে x=y−k।')],
        'math-1-09': [
            (f'y=x^{k} হলে x=1-এ dy/dx কত?',k,'d(x^n)/dx=nx^(n−1)।'),
            (f'y={k}x²+3x হলে x=2-এ dy/dx কত?',4*k+3,'dy/dx=2kx+3।'),
            (f'y=sin({k}x) হলে x=0-এ dy/dx কত? x রেডিয়ানে।',k,'চেইন রুল: dy/dx=k cos(kx)।'),
            (f'y=e^({k}x) হলে x=0-এ dy/dx কত?',k,'dy/dx=k e^(kx)।')],
        'math-1-10': [
            (f'∫₀¹ {k}x dx-এর মান কত?',Fraction(k,2),'আদিম ফাংশন kx²/2; সীমা 0 থেকে 1।'),
            (f'∫₀² {k} dx-এর মান কত?',2*k,'ধ্রুবক k-এর যোগজ kx।'),
            (f'∫₀¹ {k+1}x^{k} dx-এর মান কত?',1,'আদিম ফাংশন x^(k+1); সীমা 0 থেকে 1।'),
            (f'∫₀^{k} 2x dx-এর মান কত?',k*k,'আদিম ফাংশন x²; সীমা 0 থেকে k।')],
        'math-2-01': [
            (f'|x|={k} সমীকরণের ধনাত্মক সমাধান কত?',k,'|x|=a>0 হলে x=±a।'),
            (f'2x+3<{2*k+3} হলে x-এর ঊর্ধ্বসীমা (বাদ যায়) কত?',k,'দুইপাশ থেকে 3 বিয়োগ, তারপর 2 দিয়ে ভাগ।'),
            (f'−2x>{-2*k} হলে x-এর ঊর্ধ্বসীমা (বাদ যায়) কত?',k,'ঋণাত্মক সংখ্যা দিয়ে ভাগ করলে অসমতার দিক বদলায়।'),
            (f'−{k}≤x≤{k} ব্যবধানে পূর্ণসংখ্যা কতটি?',2*k+1,'−k থেকে k পর্যন্ত সীমাসহ সংখ্যা 2k+1।')],
        'math-2-02': [
            (f'x,y≥0 ও x+y≤{k} হলে 2x+3y-এর সর্বোচ্চ মান কত?',3*k,'শীর্ষবিন্দু (0,0),(k,0),(0,k); মান 0,2k,3k।'),
            (f'0≤x≤{k}, 0≤y≤2 হলে x+2y-এর সর্বোচ্চ মান কত?',k+4,'ধনাত্মক সহগে x=k,y=2-এ সর্বোচ্চ।'),
            (f'x,y≥0 ও x+y≥{k} হলে 3x+4y-এর সর্বনিম্ন মান কত?',3*k,'3x+4y=3(x+y)+y≥3k; (k,0)-তে অর্জিত।'),
            (f'0≤x≤2, 0≤y≤{k} হলে 5x+y-এর সর্বোচ্চ মান কত?',k+10,'x=2,y=k-এ উদ্দেশ্য ফাংশনের সর্বোচ্চ মান।')],
        'math-2-03': [
            (f'z={k}+4i হলে Re(z) কত?',k,'বাস্তব অংশ হলো i-বিহীন সহগ।'),
            (f'z=3+{k}i হলে Im(z) কত?',k,'কাল্পনিক অংশ i-এর বাস্তব সহগ।'),
            (f'z={3*k}+{4*k}i হলে |z| কত?',5*k,'|z|=√(a²+b²)।'),
            (f'z={k}+2i হলে z+z̄ কত?',2*k,'অনুবন্ধী যোগে কাল্পনিক অংশ বাতিল হয়।')],
        'math-2-04': [
            (f'x²−{k}x+3=0-এর মূলদ্বয়ের যোগ কত?',k,'ax²+bx+c=0-এ মূলের যোগ −b/a।'),
            (f'x²+2x+{k}=0-এর মূলদ্বয়ের গুণফল কত?',k,'মূলের গুণফল c/a।'),
            (f'f(x)=x³+{k}x+2। x−1 দিয়ে ভাগের ভাগশেষ কত?',k+3,'ভাগশেষ উপপাদ্য: ভাগশেষ f(1)।'),
            (f'f(x)=x²−{k}x+4। x+1 দিয়ে ভাগের ভাগশেষ কত?',k+5,'ভাগশেষ f(−1)=1+k+4।')],
        'math-2-05': [
            (f'(1+x)^{k+1}-এ x-এর সহগ কত?',k+1,'x-এর সহগ nC1=n।'),
            (f'(1+x)^{k+2}-এ x²-এর সহগ কত?',(k+2)*(k+1)//2,'x²-এর সহগ nC2।'),
            (f'(1+2x)^{k}-এ x-এর সহগ কত?',2*k,'সহগ nC1×2।'),
            (f'(2+x)²-এর বিস্তৃতিতে x={k} বসালে মান কত?',(k+2)**2,'(2+x)²=4+4x+x²।')],
        'math-2-06': [
            (f'y²={4*k}x পরাবৃত্তে a কত?',k,'প্রমিত রূপ y²=4ax।'),
            (f'y²={4*k}x পরাবৃত্তের উপকেন্দ্রের x স্থানাঙ্ক কত?',k,'উপকেন্দ্র (a,0)।'),
            (f'x²/{25*k*k}+y²/{16*k*k}=1 উপবৃত্তে উপকেন্দ্র দূরত্ব c কত?',3*k,'c²=a²−b²=25k²−16k²।'),
            (f'x²/{25*k*k}−y²/{144*k*k}=1 অধিবৃত্তে c কত?',13*k,'c²=a²+b²=25k²+144k²।')],
        'math-2-07': [
            (f'0≤x≤{k}π-এ sinx=0-এর সমাধান কতটি?',k+1,'x=nπ; n=0,1,...,k।'),
            (f'0<x<{k}π-এ sinx=0-এর সমাধান কতটি?',k-1,'সীমা বাদে n=1,...,k−1।'),
            (f'0≤x≤{k}π-এ cosx=0-এর সমাধান কতটি?',k,'x=(2n+1)π/2; প্রতি π-তে একটি।'),
            (f'{2*k}sin⁻¹(1)/π-এর মান কত? প্রধান মান রেডিয়ানে।',k,'sin⁻¹(1)=π/2।')],
        'math-2-08': [
            (f'এক বিন্দুতে একই দিকে {k} N ও 4 N বল। সাম্যকারী বলের মান কত N?',k+4,'সাম্যকারী লব্ধির সমান মানের বিপরীত বল।'),
            (f'{k} N বলের লম্ব বাহু 3 m। মুহূর্তের মান কত N·m?',3*k,'মুহূর্ত = বল × লম্ব দূরত্ব।'),
            (f'দুটি বিপরীত সমান্তরাল {k} N বলের দূরত্ব 2 m। কাপলের মুহূর্ত কত N·m?',2*k,'কাপল = Fd।'),
            (f'অনুভূমিক মসৃণ তলে {k} kg স্থির বস্তু। অভিলম্ব প্রতিক্রিয়া কত N? g=10।',10*k,'উল্লম্ব সাম্যে N=mg।')],
        'math-2-09': [
            (f'x(t)={k}t²+2t হলে t=1 s-এ বেগ কত m/s?',2*k+2,'v=dx/dt=2kt+2।'),
            (f'v(t)={k}t+3 হলে ত্বরণ কত m/s²?',k,'a=dv/dt=k।'),
            (f'স্থির অবস্থা থেকে a={k} m/s²-এ 2 s-এ সরণ কত m?',2*k,'s=½at²।'),
            (f'প্রক্ষেপকের ux={k} m/s ও মোট উড্ডয়ন 4 s। পাল্লা কত m?',4*k,'পাল্লা = অনুভূমিক বেগ × মোট সময়।')],
        'math-2-10': [
            (f'{k}, {k+2}, {k+4} সংখ্যার গড় কত?',k+2,'গড় = সংখ্যার যোগ/3।'),
            (f'{k}, {k+2}, {k+4} সংখ্যার মধ্যক কত?',k+2,'সাজানো তিন সংখ্যার মাঝেরটি মধ্যক।'),
            (f'ব্যাগে {k} লাল ও 2 নীল বল। দৈবভাবে একটি তুললে লাল পাওয়ার সম্ভাবনা কত?',Fraction(k,k+2),'সম্ভাবনা = অনুকূল ফল/মোট সমসম্ভাব্য ফল।'),
            (f'ব্যাগে {k} লাল ও 3 নীল বল। একটি তুললে নীল পাওয়ার সম্ভাবনা কত?',Fraction(3,k+3),'অনুকূল নীল 3, মোট k+3।')],
    }
    return tables[cid][m]


def make_original_questions(books):
    facts = read_facts()
    valid_ids = {c['id'] for b in books for c in b['chapters']}
    assert not set(facts) - valid_ids, set(facts) - valid_ids
    result = {}
    for book in books:
        for chapter in book['chapters']:
            cid = chapter['id']
            target = 300 if book['subject'] == 'Chemistry' else 100
            if book['subject'] in ('Physics', 'HigherMath'):
                solver = physics if book['subject'] == 'Physics' else higher_math
                questions = []
                seen = set()
                # Each family receives 25 distinct input cases, interleaved for variety.
                for k in range(2, 32):
                    for mode in range(4):
                        stem, answer, solution = solver(cid, k, mode)
                        if stem in seen:
                            continue
                        seen.add(stem)
                        questions.append(numeric(cid, stem, answer, solution, mode))
                        if len(questions) == target:
                            break
                    if len(questions) == target:
                        break
            else:
                assert cid in facts, f'Missing original material: {cid}'
                questions = conceptual(cid, facts[cid], target)
            assert len(questions) == target, (cid, len(questions), target)
            assert len({q['id'] for q in questions}) == target
            result[cid] = questions
    return result
