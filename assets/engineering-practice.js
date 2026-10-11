/* Isolated engineering practice; original PCM questions and track-specific progress. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const bn = value => String(value).replace(/[0-9]/g,d=>'০১২৩৪৫৬৭৮৯'[Number(d)]);
  const trackTitle = track => track === 'buet' ? 'BUET প্রিলি অনুশীলন' : 'CKRUET PCM অনুশীলন';
  const subjectNames = {Chemistry:'রসায়ন',Physics:'পদার্থবিজ্ঞান',HigherMath:'উচ্চতর গণিত'};
  let data = null, loading = null, state = {track:'buet',book:null,search:'',attempt:null}, timer = null;
  const storageKey = 'admission_engineering_attempt_v1';
  function read(key, fallback) { try { return JSON.parse(localStorage.getItem(key)) || fallback; } catch { return fallback; } }
  function save() { try { localStorage.setItem(storageKey,JSON.stringify(state.attempt)); } catch {} }
  function progress() { return read('admission_engineering_progress_v1',{}); }
  function bookById(id) { return data?.books.find(b=>b.id===id); }
  function selection(attempt=state.attempt) {
    const book=bookById(attempt?.book),chapter=book?.chapters.find(c=>c.id===attempt?.chapter),set=chapter?.sets.find(s=>s.id===attempt?.set);
    if(!set) return null;
    const ids=new Set(set.question_ids || []),questions=(chapter.questions || []).filter(q=>ids.has(q.id));
    return {book,chapter,set,questions};
  }
  async function load() {
    if(data) return data;
    if(!loading) loading=fetch('/data/engineering_practice.json?v=1').then(r=>{if(!r.ok) throw new Error('load');return r.json();}).then(d=>{if(!Array.isArray(d.books))throw new Error('shape');data=d;return d;}).finally(()=>{loading=null;});
    return loading;
  }
  const chapterLoads=new Map();
  async function loadChapter(bookId,chapterId) {
    const chapter=bookById(bookId)?.chapters.find(c=>c.id===chapterId);
    if(!chapter)throw new Error('chapter');
    if(chapter.questions)return chapter;
    if(!chapterLoads.has(chapterId))chapterLoads.set(chapterId,fetch(chapter.questions_url).then(r=>{if(!r.ok)throw new Error('chapter load');return r.json();}).then(payload=>{
      if(payload.id!==chapterId||!Array.isArray(payload.questions)||payload.questions.length!==chapter.question_count)throw new Error('chapter shape');
      chapter.questions=payload.questions;chapter.sets=payload.sets;return chapter;
    }).finally(()=>chapterLoads.delete(chapterId)));
    return chapterLoads.get(chapterId);
  }
  function focusHeading() { const h=$('ep-content')?.querySelector('h2, h1'); if(h){h.tabIndex=-1;h.focus({preventScroll:true});} }
  const trackNote = () => state.track==='buet'
    ? 'ঐতিহাসিক প্রিলিমিনারি ধাঁচের MCQ অনুশীলন। ২০২৫–২৬ বুয়েট বিজ্ঞপ্তিতে লিখিত পরীক্ষা ছিল—নিজের সেশনের বিজ্ঞপ্তি মিলিয়ে নাও।'
    : 'ইংরেজি বাদ দিয়ে কাস্টম PCM অনুশীলন। ঐতিহাসিক CKRUET পরীক্ষায় ইংরেজিও ছিল; এটি অফিসিয়াল পূর্ণাঙ্গ মডেলের প্রতিলিপি নয়।';
  let research=null, researchRequest=0;
  function renderHeader() {
    const root=$('view-engineering');root.dataset.track=state.track;
    root.innerHTML=`<div class="ep-head"><div class="ep-eyebrow">ইঞ্জিনিয়ারিং প্রস্তুতি · সম্পূর্ণ ফ্রি</div>
      <h1>গণিত · পদার্থ · রসায়ন</h1><p>তোমার লক্ষ্য বেছে নাও। মিশ্র অনুশীলন দাও, অথবা বই, পত্র ও অধ্যায় ধরে প্রস্তুতি নাও। সব অধ্যায়ের সেট সরাসরি খোলা—আগের পরীক্ষা শেষ করার শর্ত নেই।</p>
      <div class="ep-tabs" role="tablist" aria-label="ইঞ্জিনিয়ারিং প্রস্তুতির লক্ষ্য"><button role="tab" aria-selected="${state.track==='buet'}" data-ep-track="buet">📐 BUET প্রিলি অনুশীলন</button><button role="tab" aria-selected="${state.track==='ckruet'}" data-ep-track="ckruet">⚙️ CKRUET PCM অনুশীলন</button></div>
      <p class="ep-format-note">${trackNote()}</p></div><div id="ep-content"></div>`;
  }
  function renderCatalog() {
    researchRequest++;renderHeader();
    const book=bookById(state.book),container=$('ep-content');
    if(book && book.tracks.includes(state.track)) {renderBook(book);return;}
    state.book=null;
    const books=data.books.filter(b=>b.tracks.includes(state.track)&&b.kind!=='mixed');
    const mixed=data.books.find(b=>b.tracks.includes(state.track)&&b.kind==='mixed');
    const subjects=['HigherMath','Physics','Chemistry'];
    container.innerHTML=`<div class="ep-summary"><span>৬ বই / পত্র</span><span>৫১ অধ্যায়</span><span>৭,১০০ অধ্যায়-প্রশ্ন</span></div>
      <section class="ep-mixed"><div><span class="ep-tag ep-tag-ready">মিশ্র PCM অনুশীলন</span><h2>১০০ প্রশ্নে তিন বিষয়ের প্রস্তুতি</h2><p class="ep-muted">গণিত ৩৪ · পদার্থ ৩৩ · রসায়ন ৩৩ · ${state.track==='buet'?'৬০':'১২০'} মিনিট। অধ্যায়ব্যাংক থেকে বাছাই করা প্রশ্ন।</p></div><button class="ep-button ep-primary" data-ep-book="${mixed.id}">মিশ্র সেট শুরু →</button></section>
      <div class="ep-toolbar"><h2 class="ep-review-title">অধ্যায়ভিত্তিক অনুশীলন</h2><button class="ep-button" data-ep-research>প্রস্তুতির তথ্য ও বই ↗</button></div>
      <p class="ep-muted">গণিত ও পদার্থে প্রতি অধ্যায়ে ১০০ প্রশ্ন। রসায়নে প্রতি অধ্যায়ে ৩টি পৃথক সেট × ১০০।</p>
      ${subjects.map(subject=>`<section class="ep-book-group"><h2>${esc(subjectNames[subject])}</h2><div class="ep-grid">${books.filter(b=>b.subject===subject).map(b=>`<button class="ep-card ep-card-button" data-ep-book="${b.id}"><span class="ep-tag ep-tag-ready">বই / পত্রভিত্তিক</span><h3>${esc(b.title)}</h3><p class="ep-muted">${bn(b.chapters.length)} অধ্যায় · ${bn(b.available_questions)} প্রশ্ন</p><p class="ep-muted">অধ্যায় বেছে নাও →</p></button>`).join('')}</div></section>`).join('')}
      <details class="ep-banner"><summary>প্রশ্নের উৎস ও অনুশীলনের ধরন</summary><p>এগুলো মৌলিক অধ্যায়ভিত্তিক অনুশীলনী; দশ বছরের যাচাইকৃত বিগত প্রশ্নব্যাংক নয়। গণিত ও পদার্থে ৪টি ভিত্তিমূলক ও ২টি প্রয়োগধর্মী সমস্যা-পদ্ধতির সংখ্যাভিত্তিক ভ্যারিয়েন্ট রয়েছে। রসায়নে ধারণাভিত্তিক বক্তব্য ও প্রয়োগ অনুশীলন আছে। একই পদ্ধতির প্রশ্ন ভিন্ন সংখ্যায় আসতে পারে। দুই লক্ষ্যে কিছু রসায়ন প্রশ্ন শেয়ার করা হয়েছে। স্বাধীন শিক্ষক-পর্যালোচনা হয়নি।</p></details>`;
  }
  async function renderResearch() {
    const request=++researchRequest;renderHeader();$('ep-content').innerHTML='<div class="ep-empty" role="status">প্রস্তুতির তথ্য লোড হচ্ছে…</div>';
    try{
      if(!research){const r=await fetch(data.references_url);if(!r.ok)throw new Error('research');research=await r.json();}
      if(appState.currentStream!=='engineering'||state.book||request!==researchRequest)return;
      $('ep-content').innerHTML=`<button class="ep-button" data-ep-home>← অনুশীলনে ফিরুন</button><h2 class="ep-review-title">বই ও পরীক্ষার ধরন</h2>
        <p class="ep-muted">তথ্য যাচাই: ১১ অক্টোবর ২০২৬। নতুন সেশনের বিজ্ঞপ্তি সবসময় বিশ্ববিদ্যালয়ের নিজস্ব ওয়েবসাইটে মিলিয়ে নাও।</p>
        <div class="ep-grid">${research.book_recommendations.map(b=>`<article class="ep-card"><h3>${esc(b.subject)}</h3><p>প্রধান রেফারেন্স প্রার্থী: ${esc(b.main)}</p><p class="ep-muted">সহায়ক: ${esc(b.supplement)}</p></article>`).join('')}</div>
        <p class="ep-banner">${esc(research.book_note)}</p><h3 class="ep-review-title">BUET</h3><p class="ep-muted">${esc(research.exam_notes.buet)}</p><h3 class="ep-review-title">CKRUET</h3><p class="ep-muted">${esc(research.exam_notes.ckruet)}</p>
        <h3 class="ep-review-title">যা প্রস্তুত আছে</h3><p class="ep-muted">দুই লক্ষ্যে আলাদা অগ্রগতি, ৫১টি অধ্যায় করে ৭,১০০ প্রশ্নের অনুশীলন। মোট ${bn(research.coverage.unique_questions)}টি স্বতন্ত্র প্রশ্নের stem; প্রশ্ন-পদ্ধতির সংখ্যাভিত্তিক ভ্যারিয়েন্ট রয়েছে। রসায়নের কিছু ধারণা-প্রশ্ন দুই লক্ষ্যে শেয়ার করা। মিশ্র সেটে অধ্যায়ের প্রশ্ন পুনরায় আসে। স্বাধীন শিক্ষক যাচাই হয়নি।</p>
        <h3 class="ep-review-title">অনলাইন রেফারেন্স</h3><p class="ep-muted">বিজ্ঞপ্তি, বইয়ের সুপারিশ ও নির্বাচিত প্রশ্ন-সংকলন পড়া হয়েছে। সব বছর / শিফটের পূর্ণাঙ্গ বিশ্লেষণ বা উত্তর যাচাই সম্পন্ন হয়নি।</p>
        <ul class="ep-source-list">${research.sources.filter(x=>!['satt-buet-audit','nonacademy-audit'].includes(x.id)).map(x=>`<li><a href="${esc(x.url)}" target="_blank" rel="noopener noreferrer">${esc(x.id.replace(/-/g,' '))} ↗</a></li>`).join('')}</ul>`;
      focusHeading();
    }catch{$('ep-content').innerHTML='<div class="ep-error">তথ্য লোড হয়নি। <button class="ep-button" data-ep-home>অনুশীলনে ফিরুন</button></div>';}
  }
  function renderBook(book) {
    const container=$('ep-content');
    container.innerHTML=`<nav class="ep-crumbs" aria-label="অধ্যায়ের পথ"><button data-ep-home>← সব বই / বিষয়</button><span>/ ${trackTitle(state.track)}</span><span>/ ${esc(book.title)}</span></nav>
      <h2 class="ep-review-title">${esc(book.title)}</h2><p class="ep-muted">${book.kind==='mixed'?'তিন বিষয়ের ১০০ প্রশ্নের মিশ্র অনুশীলন।':book.subject==='Chemistry'?'প্রতি অধ্যায়ে ৩টি পৃথক সেট × ১০০ প্রশ্ন।':'প্রতি অধ্যায়ে ১০০ প্রশ্নের একটি সেট।'} মৌলিক অনুশীলনী; বিগত পরীক্ষার প্রশ্নের প্রতিলিপি নয়। একই অধ্যায়ের সেটগুলোর মধ্যে প্রশ্ন পুনরাবৃত্তি নেই।</p>
      ${book.note?`<p class="ep-muted">${esc(book.note)}</p>`:""}<p class="ep-muted">নতুন ধারণাভিত্তিক প্রশ্নে দুটি বক্তব্য বিচার করতে হবে। পদার্থবিজ্ঞান ও গণিতে ভিত্তিমূলক ও প্রয়োগধর্মী পদ্ধতির সংখ্যাভিত্তিক অনুশীলন রয়েছে।</p>
      <div class="ep-toolbar"><label class="ep-muted" for="ep-search">অধ্যায় খুঁজুন</label><input id="ep-search" class="ep-search" type="search" placeholder="অধ্যায়ের নাম লিখুন…" value="${esc(state.search)}"><span class="ep-tag">সব সেটে সরাসরি প্রবেশ</span></div>
      <div id="ep-chapter-grid" class="ep-grid"></div>`;
    renderChapters(book);
  }
  function renderChapters(book) {
    const chapters=book.chapters.filter(c=>c.title.toLocaleLowerCase().includes(state.search.toLocaleLowerCase())),done=progress();
    $('ep-chapter-grid').innerHTML=chapters.length?chapters.map(c=>`<article class="ep-card"><div class="ep-chapter-number">${book.kind==='mixed'?'মিশ্র অনুশীলন':'অধ্যায়'} ${bn(c.number)}</div><h3>${esc(c.title)}</h3>
      <p class="ep-muted">${bn(c.question_count)} প্রশ্ন উপলব্ধ${c.question_count<c.target_questions?` · লক্ষ্য ${bn(c.target_questions)}`:''}</p>
      ${c.sets.map(s=>{const count=s.question_count ?? s.question_ids.length,p=done[`${state.track}:${s.id}`];return `<button class="ep-button ep-set ${count?'ep-primary':''}" data-ep-set="${s.id}" data-ep-chapter="${c.id}" ${count?'':'disabled'}><span>সেট ${bn(s.number)} ${p?'✓':''}</span><span>${count?`${bn(count)} প্রশ্ন · ${bn(s.minutes||60)} মিনিট →`:'প্রশ্ন আসছে'}</span></button>${p?`<p class="ep-status">শেষ ফল: ${bn(p.score)}/${bn(p.total)}</p>`:''}`;}).join('')}
      ${!c.question_count?'<p class="ep-muted" style="margin-top:12px">এই অধ্যায়ের প্রশ্ন এখনো প্রস্তুত নয়।</p>':''}</article>`).join(''):`<div class="ep-empty">${book.chapters.length?'এই নামে কোনো অধ্যায় পাওয়া যায়নি।':esc(book.note||'এই বিষয়ে প্রশ্ন এখনো যুক্ত হয়নি।')}</div>`;
  }
  function questionHtml(q,index,review=false) {
    const answer=state.attempt.answers[index],letters=['ক','খ','গ','ঘ'];
    return `<article class="ep-question" id="ep-q-${index}"><span class="ep-tag">প্রশ্ন ${bn(index+1)}</span>${review?` <span class="ep-status">${answer===undefined?'উত্তর দেওয়া হয়নি':answer===q.correct_index?'✓ সঠিক':'✕ ভুল'}</span>`:''}
      <h3>${esc(q.question_bn)}</h3><div class="ep-options" role="group" aria-label="প্রশ্ন ${index+1} এর উত্তর">${q.options.map((option,i)=>`<button class="ep-option ${review&&i===q.correct_index?'ep-correct':review&&answer===i?'ep-wrong':''}" ${review?'disabled':`data-ep-answer="${i}" data-ep-index="${index}"`} aria-pressed="${answer===i}"><span class="ep-letter">${letters[i]}.</span><span>${esc(option)}</span></button>`).join('')}</div>
      ${!review?`<button class="ep-button" style="margin-top:10px" data-ep-clear="${index}">উত্তর মুছুন</button>`:`<div class="ep-explanation"><strong>সঠিক উত্তর: ${letters[q.correct_index]}. ${esc(q.options[q.correct_index])}</strong><p>${esc(q.explanation||'এই প্রশ্নের বিস্তারিত ব্যাখ্যা এখনো যুক্ত হয়নি।')}</p>${q.book_reference?`<p class="ep-muted">রেফারেন্স: ${esc(q.book_reference)}</p>`:''}</div>`}</article>`;
  }
  function math() { if(window.renderMathInElement)window.renderMathInElement($('ep-content'),{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false}); }
  async function start(chapterId,setId) {
    const track=state.track,bookId=state.book;
    if(state.attempt?.status==='running')return;
    const button=$('view-engineering').querySelector(`[data-ep-set="${setId}"]`);
    if(button){button.disabled=true;button.setAttribute('aria-busy','true');}
    try {await loadChapter(bookId,chapterId);} catch {
      if(button){button.disabled=false;button.removeAttribute('aria-busy');}
      confirmAction('প্রশ্ন লোড হয়নি। আবার চেষ্টা করবে?',()=>start(chapterId,setId));return;
    }
    if(button){button.disabled=false;button.removeAttribute('aria-busy');}
    if(state.track!==track||state.book!==bookId||appState.currentStream!=='engineering'||state.attempt?.status==='running')return;
    const attempt={track:state.track,book:state.book,chapter:chapterId,set:setId,answers:{},status:'running'};
    const selected=selection(attempt);if(!selected?.questions.length)return;
    const minutes=selected.set.minutes || 60;attempt.deadline=Date.now()+minutes*60000;attempt.startedAt=Date.now();state.attempt=attempt;save();renderExam();
  }
  function renderExam() {
    const selected=selection();if(!selected){state.attempt=null;save();renderCatalog();return;}
    state.track=state.attempt.track;state.book=state.attempt.book;renderHeader();
    $('ep-content').innerHTML=`<h2 class="ep-review-title">${esc(selected.chapter.title)} · সেট ${bn(selected.set.number)}</h2><p class="ep-muted">${trackTitle(state.track)} · ${esc(selected.book.title)} · ${bn(selected.questions.length)} প্রশ্ন · সঠিক +১, ভুল −০.২৫</p>
      <div class="ep-exam-bar"><div><div class="ep-muted">অবশিষ্ট সময়</div><div id="ep-timer" class="ep-timer" role="timer"></div></div><p id="ep-answer-count" class="ep-muted" aria-live="polite"></p><button class="ep-button ep-primary" data-ep-submit>পরীক্ষা জমা দিন</button><button class="ep-button" data-ep-cancel>বাতিল করুন</button></div><div>${selected.questions.map((q,i)=>questionHtml(q,i)).join('')}</div><div class="ep-actions"><button class="ep-button ep-primary" data-ep-submit>পরীক্ষা জমা দিন</button></div>`;
    math();clearInterval(timer);tick();if(state.attempt.status==='running')timer=setInterval(tick,1000);
  }
  function tick() {
    if(state.attempt?.status!=='running')return;
    const seconds=Math.max(0,Math.ceil((state.attempt.deadline-Date.now())/1000));
    if($('ep-timer'))$('ep-timer').textContent=`${bn(Math.floor(seconds/60))}:${bn(String(seconds%60).padStart(2,'0'))}`;
    updateCount();if(seconds===0)finish();
  }
  function updateCount() {
    const count=Object.keys(state.attempt.answers).length,total=selection().questions.length;
    if($('ep-answer-count'))$('ep-answer-count').textContent=`${bn(count)}/${bn(total)} উত্তর দেওয়া হয়েছে`;
  }
  function finish() {
    if(state.attempt?.status!=='running')return;clearInterval(timer);state.attempt.status='submitted';state.attempt.finishedAt=Date.now();save();
    const result=score(),done=progress();done[`${state.track}:${state.attempt.set}`]={score:result.score,total:result.total,at:Date.now()};
    try{localStorage.setItem('admission_engineering_progress_v1',JSON.stringify(done));}catch{}
    renderResult();window.scrollTo({top:0,behavior:'smooth'});
  }
  function score() {
    const selected=selection();let correct=0,wrong=0,blank=0;
    selected.questions.forEach((q,i)=>{const a=state.attempt.answers[i];if(a===undefined)blank++;else if(a===q.correct_index)correct++;else wrong++;});
    return {correct,wrong,blank,total:selected.questions.length,score:Math.max(0,correct-wrong*.25)};
  }
  function renderResult() {
    const selected=selection();if(!selected){state.attempt=null;save();renderCatalog();return;}
    renderHeader();const result=score();
    $('ep-content').innerHTML=`<h2 class="ep-review-title">${esc(selected.chapter.title)} · সেট ${bn(selected.set.number)} ফলাফল</h2><p class="ep-muted">${trackTitle(state.track)} · ${esc(selected.book.title)}</p><div class="ep-score-grid">${[[result.score+'/'+result.total,'মোট স্কোর'],[result.correct,'সঠিক'],[result.wrong,'ভুল'],[result.blank,'উত্তরহীন']].map(([v,l])=>`<div class="ep-score"><strong>${bn(v)}</strong><span>${l}</span></div>`).join('')}</div>
      <div class="ep-banner">ইঞ্জিনিয়ারিং অনুশীলনের ফল এই ডিভাইসে সংরক্ষিত। এটি পূর্ণাঙ্গ মডেল টেস্টের জাতীয় র‍্যাংকিং বা ধারাবাহিক অগ্রগতি পরিবর্তন করে না।</div><div class="ep-actions"><button class="ep-button ep-primary" data-ep-retake>একই সেট আবার দিন</button><button class="ep-button" data-ep-back-book>অন্য অধ্যায় / সেট</button></div><h3 class="ep-review-title">উত্তর ও ব্যাখ্যা</h3>${selected.questions.map((q,i)=>questionHtml(q,i,true)).join('')}`;
    math();focusHeading();
  }
  function confirmAction(title,onConfirm) {
    openCustomModal({title,subtitle:'অধ্যায়ভিত্তিক অনুশীলন',icon:'📝',confirmText:'নিশ্চিত করুন',cancelText:'ফিরে যান',showCancel:true,onConfirm});
  }
  function abandon(){clearInterval(timer);state.attempt=null;save();}
  async function open() {
    const root=$('view-engineering');root.innerHTML='<div class="ep-empty" role="status">বই ও অধ্যায় লোড হচ্ছে…</div>';
    try {
      await load();
      if(appState.currentStream!=='engineering')return;
      if(!state.attempt){const saved=read(storageKey,null);if(saved&&['buet','ckruet'].includes(saved.track)&&bookById(saved.book)?.tracks.includes(saved.track)) {await loadChapter(saved.book,saved.chapter);if(!selection(saved)?.questions.length)throw new Error('saved attempt');state.attempt=saved;state.track=saved.track;state.book=saved.book;}}
      if(state.attempt?.status==='running')renderExam();else if(state.attempt?.status==='submitted')renderResult();else renderCatalog();
    } catch {root.innerHTML='<div class="ep-error" role="alert">অধ্যায়ের প্রশ্ন লোড করা যায়নি। সংযোগ পরীক্ষা করে আবার চেষ্টা করুন। <button class="ep-button" data-ep-retry>আবার চেষ্টা</button></div>';}
  }
  function guardNavigation(stream){
    if(appState.currentStream==='engineering'&&stream!=='engineering'&&state.attempt?.status==='running'){
      confirmAction('চলতি অধ্যায় পরীক্ষা বাতিল করে বের হবে?',()=>{abandon();switchStream(stream);});return true;
    }return false;
  }
  document.addEventListener('click',event=>{
    const target=event.target.closest('#view-engineering button');if(!target)return;
    const d=target.dataset;
    if(d.epTrack){if(state.attempt?.status==='running'){confirmAction('চলতি পরীক্ষা বাতিল করে লক্ষ্য বদলাবে?',()=>{abandon();state.track=d.epTrack;state.book=null;renderCatalog();});return;}abandon();state.track=d.epTrack;state.book=null;state.search='';renderCatalog();}
    else if('epResearch'in d){if(state.attempt?.status==='running')return;state.book=null;renderResearch();}
    else if(d.epBook){state.book=d.epBook;state.search='';renderCatalog();focusHeading();}
    else if('epHome'in d){state.book=null;state.search='';renderCatalog();focusHeading();}
    else if(d.epSet)start(d.epChapter,d.epSet);
    else if('epAnswer'in d){const i=Number(d.epIndex),a=Number(d.epAnswer);state.attempt.answers[i]=a;save();target.closest('.ep-options').querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b===target)));updateCount();}
    else if('epClear'in d){delete state.attempt.answers[Number(d.epClear)];save();$('ep-q-'+d.epClear).querySelectorAll('.ep-option').forEach(b=>b.setAttribute('aria-pressed','false'));updateCount();}
    else if('epSubmit'in d)confirmAction('উত্তরপত্র জমা দিয়ে ফলাফল দেখবে?',finish);
    else if('epCancel'in d)confirmAction('চলতি অধ্যায় পরীক্ষা বাতিল করবে?',()=>{abandon();renderCatalog();});
    else if('epRetake'in d){const a=state.attempt;abandon();start(a.chapter,a.set);}
    else if('epBackBook'in d){abandon();renderCatalog();focusHeading();}
    else if('epRetry'in d)open();
  });
  document.addEventListener('input',event=>{if(event.target.id==='ep-search'){state.search=event.target.value;renderChapters(bookById(state.book));}});
  window.addEventListener('beforeunload',event=>{if(state.attempt?.status==='running'){save();event.preventDefault();event.returnValue='';}});
  document.addEventListener('visibilitychange',()=>{if(state.attempt?.status==='running'){save();if(document.visibilityState==='visible')tick();}});
  window.EngineeringPractice={open,guardNavigation,hasRunningAttempt:()=>state.attempt?.status==='running'};
  window.addEventListener('load',()=>{if(window.location?.hash==='#engineering')switchStream('engineering');});
})();
