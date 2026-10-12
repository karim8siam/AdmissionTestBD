/* Isolated engineering practice; original PCM questions and track-specific progress. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const bn = value => String(value).replace(/[0-9]/g,d=>'০১২৩৪৫৬৭৮৯'[Number(d)]);
  const trackTitle = track => track === 'buet' ? 'BUET প্রিলি অনুশীলন' : 'CKRUET PCM অনুশীলন';
  const subjectNames = {Chemistry:'রসায়ন',Physics:'পদার্থবিজ্ঞান',HigherMath:'উচ্চতর গণিত'};
  let data = null, loading = null, state = {track:'buet',book:null,search:'',attempt:null}, timer = null;
  const storageKey = 'admission_engineering_attempt_chapters_v3';
  function read(key, fallback) { try { return JSON.parse(localStorage.getItem(key)) || fallback; } catch { return fallback; } }
  function save() { try { localStorage.setItem(storageKey,JSON.stringify(state.attempt)); } catch {} }
  function progress() { return read('admission_engineering_progress_chapters_v3',{}); }
  function bookById(id) { return data?.books.find(b=>b.id===id); }
  function selection(attempt=state.attempt) {
    const book=bookById(attempt?.book),chapter=book?.chapters.find(c=>c.id===attempt?.chapter),set=chapter?.sets.find(s=>s.id===attempt?.set);
    if(!set) return null;
    const ids=new Set(set.question_ids || []),questions=(chapter.questions || []).filter(q=>ids.has(q.id));
    return {book,chapter,set,questions};
  }
  async function load() {
    if(data) return data;
    if(!loading) loading=fetch('/data/engineering_practice.json?v=3').then(r=>{if(!r.ok) throw new Error('load');return r.json();}).then(d=>{if(!Array.isArray(d.books))throw new Error('shape');data=d;return d;}).finally(()=>{loading=null;});
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
  function focusHeading() { const h=$('ec-content')?.querySelector('h2, h1'); if(h){h.tabIndex=-1;h.focus({preventScroll:true});} }
  const trackNote = () => state.track==='buet'
    ? 'ঐতিহাসিক প্রিলিমিনারি ধাঁচের MCQ অনুশীলন। ২০২৫–২৬ বুয়েট বিজ্ঞপ্তিতে লিখিত পরীক্ষা ছিল—নিজের সেশনের বিজ্ঞপ্তি মিলিয়ে নাও।'
    : 'ইংরেজি বাদ দিয়ে কাস্টম PCM অনুশীলন। ঐতিহাসিক CKRUET পরীক্ষায় ইংরেজিও ছিল; এটি অফিসিয়াল পূর্ণাঙ্গ মডেলের প্রতিলিপি নয়।';
  let research=null, researchRequest=0;
  function renderHeader() {
    const root=$('view-engineering-chapters');root.dataset.track=state.track;
    root.innerHTML=`<div class="ec-head"><div class="ec-eyebrow">ইঞ্জিনিয়ারিং প্রস্তুতি · সম্পূর্ণ ফ্রি</div>
      <h1>গণিত · পদার্থ · রসায়ন</h1><p>তোমার লক্ষ্য বেছে নাও। বই, পত্র ও অধ্যায় ধরে প্রস্তুতি নাও। সব অধ্যায়ের সেট সরাসরি খোলা—আগের পরীক্ষা শেষ করার শর্ত নেই।</p>
      <div class="ec-tabs" role="tablist" aria-label="ইঞ্জিনিয়ারিং প্রস্তুতির লক্ষ্য"><button role="tab" aria-selected="${state.track==='buet'}" data-ec-track="buet">📐 BUET প্রিলি অনুশীলন</button><button role="tab" aria-selected="${state.track==='ckruet'}" data-ec-track="ckruet">⚙️ CKRUET PCM অনুশীলন</button></div>
      <p class="ec-format-note">${trackNote()}</p></div><div id="ec-content"></div>`;
  }
  function renderCatalog() {
    researchRequest++;renderHeader();
    const book=bookById(state.book),container=$('ec-content');
    if(book && book.tracks.includes(state.track)) {renderBook(book);return;}
    state.book=null;
    const books=data.books.filter(b=>b.tracks.includes(state.track)&&b.kind!=='mixed');
    const subjects=['HigherMath','Physics','Chemistry'];
    container.innerHTML=`<div class="ec-summary"><span>৬ বই / পত্র</span><span>৫১ অধ্যায়</span><span>${bn(data.coverage.chapter_questions_per_track)} প্রশ্ন</span></div>
      <div class="ec-toolbar"><h2 class="ec-review-title">অধ্যায়ভিত্তিক অনুশীলন</h2><button class="ec-button" data-ec-research>প্রস্তুতির তথ্য ও বই ↗</button></div>
      <p class="ec-muted">গণিত ও পদার্থে লক্ষ্য ১০০ প্রশ্ন। রসায়নে লক্ষ্য ৩ × ১০০; কয়েকটি অধ্যায়ে কম প্রশ্ন প্রস্তুত—প্রতিটি কার্ডে আসল সংখ্যা দেখানো আছে। সব উপলব্ধ সেট সরাসরি খোলা।</p>
      ${subjects.map(subject=>`<section class="ec-book-group"><h2>${esc(subjectNames[subject])}</h2><div class="ec-grid">${books.filter(b=>b.subject===subject).map(b=>`<button class="ec-card ec-card-button" data-ec-book="${b.id}"><span class="ec-tag ec-tag-ready">বই / পত্রভিত্তিক</span><h3>${esc(b.title)}</h3><p class="ec-muted">${bn(b.chapters.length)} অধ্যায় · ${bn(b.available_questions)} প্রশ্ন</p><p class="ec-muted">অধ্যায় বেছে নাও →</p></button>`).join('')}</div></section>`).join('')}
      <details class="ec-banner"><summary>প্রশ্নের মান ও উৎস</summary><p>মূল অনুশীলনী, সংখ্যাভিত্তিক ভ্যারিয়েন্টসহ। ${bn(data.coverage.authored_methods)}টি সমস্যা-পদ্ধতি। বিগত বছরের নির্বাচিত প্রশ্নের ধরন পর্যালোচনা করা হয়েছে; দশ বছরের প্রামাণিক প্রশ্নব্যাংক নয়। দুই লক্ষ্য একই মূল ব্যাংক ব্যবহার করে। স্বাধীন শিক্ষক যাচাই হয়নি।</p></details>`;
  }
  async function renderResearch() {
    const request=++researchRequest;renderHeader();$('ec-content').innerHTML='<div class="ec-empty" role="status">প্রস্তুতির তথ্য লোড হচ্ছে…</div>';
    try{
      if(!research){const r=await fetch(data.references_url);if(!r.ok)throw new Error('research');research=await r.json();}
      if(appState.currentStream!=='chapters'||!$('ec-content')||state.book||request!==researchRequest)return;
      $('ec-content').innerHTML=`<button class="ec-button" data-ec-home>← অনুশীলনে ফিরুন</button><h2 class="ec-review-title">বই ও পরীক্ষার ধরন</h2>
        <p class="ec-muted">তথ্য যাচাই: ১১ অক্টোবর ২০২৬। নতুন সেশনের বিজ্ঞপ্তি সবসময় বিশ্ববিদ্যালয়ের নিজস্ব ওয়েবসাইটে মিলিয়ে নাও।</p>
        <div class="ec-grid">${research.book_recommendations.map(b=>`<article class="ec-card"><h3>${esc(b.subject)}</h3><p>প্রধান রেফারেন্স প্রার্থী: ${esc(b.main)}</p><p class="ec-muted">সহায়ক: ${esc(b.supplement)}</p></article>`).join('')}</div>
        <p class="ec-banner">${esc(research.book_note)}</p><h3 class="ec-review-title">BUET</h3><p class="ec-muted">${esc(research.exam_notes.buet)}</p><h3 class="ec-review-title">CKRUET</h3><p class="ec-muted">${esc(research.exam_notes.ckruet)}</p>
        <h3 class="ec-review-title">যা প্রস্তুত আছে</h3><p class="ec-muted">প্রতি লক্ষ্যে ৫১টি অধ্যায়; মোট ${bn(research.coverage.chapter_questions_per_track)}টি প্রশ্ন এবং ${bn(research.coverage.authored_methods)}টি সমস্যা-পদ্ধতি। সংখ্যাভিত্তিক ভ্যারিয়েন্ট আছে; দুই লক্ষ্যে একই মূল ব্যাংক ব্যবহার করা হয়েছে। রসায়নে কিছু অধ্যায় এখনো ৩০০ প্রশ্নে পৌঁছায়নি। স্বাধীন শিক্ষক যাচাই হয়নি। ১০০ মডেল টেস্ট পাবেন মূল ইঞ্জিনিয়ারিং বিভাগে।</p>
        <h3 class="ec-review-title">রেফারেন্স তথ্য</h3><p class="ec-muted">বিজ্ঞপ্তি, বইয়ের সুপারিশ ও নির্বাচিত প্রশ্ন-সংকলন ভিত্তিক প্রস্তুতি কাঠামো।</p>
        <ul class="ec-source-list">${research.sources.filter(x=>!['satt-buet-audit','nonacademy-audit'].includes(x.id)).map(x=>`<li><span class="ec-source-item">${esc(x.id.replace(/-/g,' '))}</span></li>`).join('')}</ul>`;
      focusHeading();
    }catch{$('ec-content').innerHTML='<div class="ec-error">তথ্য লোড হয়নি। <button class="ec-button" data-ec-home>অনুশীলনে ফিরুন</button></div>';}
  }
  function renderBook(book) {
    const container=$('ec-content');
    container.innerHTML=`<nav class="ec-crumbs" aria-label="অধ্যায়ের পথ"><button data-ec-home>← সব বই / বিষয়</button><span>/ ${trackTitle(state.track)}</span><span>/ ${esc(book.title)}</span></nav>
      <h2 class="ec-review-title">${esc(book.title)}</h2><p class="ec-muted">${book.kind==='mixed'?'তিন বিষয়ের ১০০ প্রশ্নের মিশ্র অনুশীলন।':book.subject==='Chemistry'?'লক্ষ্য ৩টি সেট × ১০০ প্রশ্ন; প্রস্তুত প্রশ্নের সংখ্যা নিচে দেখুন।':'প্রতি অধ্যায়ে ১০০ প্রশ্নের একটি সেট।'} মৌলিক অনুশীলনী; বিগত পরীক্ষার প্রশ্নের প্রতিলিপি নয়। একই অধ্যায়ের সেটগুলোর মধ্যে প্রশ্ন পুনরাবৃত্তি নেই।</p>
      ${book.note?`<p class="ec-muted">${esc(book.note)}</p>`:""}<p class="ec-muted">বিভিন্ন সমস্যা-পদ্ধতি ও প্রয়োগের অনুশীলন রয়েছে। একই পদ্ধতির সংখ্যাভিত্তিক ভ্যারিয়েন্ট আসতে পারে।</p>
      <div class="ec-toolbar"><label class="ec-muted" for="ec-search">অধ্যায় খুঁজুন</label><input id="ec-search" class="ec-search" type="search" placeholder="অধ্যায়ের নাম লিখুন…" value="${esc(state.search)}"><span class="ec-tag">সব সেটে সরাসরি প্রবেশ</span></div>
      <div id="ec-chapter-grid" class="ec-grid"></div>`;
    renderChapters(book);
  }
  function renderChapters(book) {
    const chapters=book.chapters.filter(c=>c.title.toLocaleLowerCase().includes(state.search.toLocaleLowerCase())),done=progress();
    $('ec-chapter-grid').innerHTML=chapters.length?chapters.map(c=>`<article class="ec-card"><div class="ec-chapter-number">${book.kind==='mixed'?'মিশ্র অনুশীলন':'অধ্যায়'} ${bn(c.number)}</div><h3>${esc(c.title)}</h3>
      <p class="ec-muted">${bn(c.question_count)} প্রশ্ন উপলব্ধ${c.question_count<c.target_questions?` · লক্ষ্য ${bn(c.target_questions)}`:''}</p>
      ${c.sets.map(s=>{const count=s.question_count ?? s.question_ids.length,p=done[`${state.track}:${s.id}`];return `<button class="ec-button ec-set ${count?'ec-primary':''}" data-ec-set="${s.id}" data-ec-chapter="${c.id}" ${count?'':'disabled'}><span>সেট ${bn(s.number)} ${p?'✓':''}</span><span>${count?`${bn(count)} প্রশ্ন · ${bn(s.minutes||60)} মিনিট →`:'প্রশ্ন আসছে'}</span></button>${p?`<p class="ec-status">শেষ ফল: ${bn(p.score)}/${bn(p.total)}</p>`:''}`;}).join('')}
      ${!c.question_count?'<p class="ec-muted" style="margin-top:12px">এই অধ্যায়ের প্রশ্ন এখনো প্রস্তুত নয়।</p>':''}</article>`).join(''):`<div class="ec-empty">${book.chapters.length?'এই নামে কোনো অধ্যায় পাওয়া যায়নি।':esc(book.note||'এই বিষয়ে প্রশ্ন এখনো যুক্ত হয়নি।')}</div>`;
  }
  function questionHtml(q,index,review=false) {
    const answer=state.attempt.answers[index],letters=['ক','খ','গ','ঘ'];
    return `<article class="ec-question" id="ec-q-${index}"><span class="ec-tag">প্রশ্ন ${bn(index+1)}</span>${review?` <span class="ec-status">${answer===undefined?'উত্তর দেওয়া হয়নি':answer===q.correct_index?'✓ সঠিক':'✕ ভুল'}</span>`:''}
      <h3>${esc(q.question_bn)}</h3><div class="ec-options" role="group" aria-label="প্রশ্ন ${index+1} এর উত্তর">${q.options.map((option,i)=>`<button class="ec-option ${review&&i===q.correct_index?'ec-correct':review&&answer===i?'ec-wrong':''}" ${review?'disabled':`data-ec-answer="${i}" data-ec-index="${index}"`} aria-pressed="${answer===i}"><span class="ec-letter">${letters[i]}.</span><span>${esc(option)}</span></button>`).join('')}</div>
      ${!review?`<button class="ec-button" style="margin-top:10px" data-ec-clear="${index}">উত্তর মুছুন</button>`:`<div class="ec-explanation"><strong>সঠিক উত্তর: ${letters[q.correct_index]}. ${esc(q.options[q.correct_index])}</strong><p>${esc(q.explanation||'এই প্রশ্নের বিস্তারিত ব্যাখ্যা এখনো যুক্ত হয়নি।')}</p>${q.book_reference?`<p class="ec-muted">রেফারেন্স: ${esc(q.book_reference)}</p>`:''}<p class="ec-muted">প্রশ্ন ID: ${esc(q.id)} · ${q.difficulty==='hard'?'প্রয়োগ / চ্যালেঞ্জ':'মাঝারি অনুশীলন'} (সম্পাদকীয় অনুমান)</p><a class="ec-button" href="mailto:shahriyarkarimsiam@gmail.com?subject=${encodeURIComponent('Engineering question review: '+q.id)}&amp;body=${encodeURIComponent(q.question_bn+'\n\nসমস্যা / সংশোধন: ')}">প্রশ্নে সমস্যা জানাও ↗</a></div>`}</article>`;
  }
  function math() { if(window.renderMathInElement)window.renderMathInElement($('ec-content'),{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false}); }
  async function start(chapterId,setId) {
    const track=state.track,bookId=state.book;
    if(state.attempt?.status==='running')return;
    const button=$('view-engineering-chapters').querySelector(`[data-ec-set="${setId}"]`);
    if(button){button.disabled=true;button.setAttribute('aria-busy','true');}
    try {await loadChapter(bookId,chapterId);} catch {
      if(button){button.disabled=false;button.removeAttribute('aria-busy');}
      confirmAction('প্রশ্ন লোড হয়নি। আবার চেষ্টা করবে?',()=>start(chapterId,setId));return;
    }
    if(button){button.disabled=false;button.removeAttribute('aria-busy');}
    if(state.track!==track||state.book!==bookId||appState.currentStream!=='chapters'||!$('view-engineering-chapters')||state.attempt?.status==='running')return;
    const attempt={track:state.track,book:state.book,chapter:chapterId,set:setId,answers:{},status:'running'};
    const selected=selection(attempt);if(!selected?.questions.length)return;
    const minutes=selected.set.minutes || 60;attempt.deadline=Date.now()+minutes*60000;attempt.startedAt=Date.now();state.attempt=attempt;save();renderExam();
  }
  function renderExam() {
    const selected=selection();if(!selected){state.attempt=null;save();renderCatalog();return;}
    state.track=state.attempt.track;state.book=state.attempt.book;renderHeader();
    $('ec-content').innerHTML=`<h2 class="ec-review-title">${esc(selected.chapter.title)} · সেট ${bn(selected.set.number)}</h2><p class="ec-muted">${trackTitle(state.track)} · ${esc(selected.book.title)} · ${bn(selected.questions.length)} প্রশ্ন · সঠিক +১, ভুল −০.২৫</p>
      <div class="ec-exam-bar"><div><div class="ec-muted">অবশিষ্ট সময়</div><div id="ec-timer" class="ec-timer" role="timer"></div></div><p id="ec-answer-count" class="ec-muted" aria-live="polite"></p><button class="ec-button ec-primary" data-ec-submit>পরীক্ষা জমা দিন</button><button class="ec-button" data-ec-cancel>বাতিল করুন</button></div><div>${selected.questions.map((q,i)=>questionHtml(q,i)).join('')}</div><div class="ec-actions"><button class="ec-button ec-primary" data-ec-submit>পরীক্ষা জমা দিন</button></div>`;
    math();clearInterval(timer);tick();if(state.attempt.status==='running')timer=setInterval(tick,1000);
  }
  function tick() {
    if(state.attempt?.status!=='running')return;
    const seconds=Math.max(0,Math.ceil((state.attempt.deadline-Date.now())/1000));
    if($('ec-timer'))$('ec-timer').textContent=`${bn(Math.floor(seconds/60))}:${bn(String(seconds%60).padStart(2,'0'))}`;
    updateCount();if(seconds===0)finish();
  }
  function updateCount() {
    const count=Object.keys(state.attempt.answers).length,total=selection().questions.length;
    if($('ec-answer-count'))$('ec-answer-count').textContent=`${bn(count)}/${bn(total)} উত্তর দেওয়া হয়েছে`;
  }
  function finish() {
    if(state.attempt?.status!=='running')return;clearInterval(timer);state.attempt.status='submitted';state.attempt.finishedAt=Date.now();save();
    const result=score(),done=progress();done[`${state.track}:${state.attempt.set}`]={score:result.score,total:result.total,at:Date.now()};
    try{localStorage.setItem('admission_engineering_progress_chapters_v3',JSON.stringify(done));}catch{}
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
    $('ec-content').innerHTML=`<h2 class="ec-review-title">${esc(selected.chapter.title)} · সেট ${bn(selected.set.number)} ফলাফল</h2><p class="ec-muted">${trackTitle(state.track)} · ${esc(selected.book.title)}</p><div class="ec-score-grid">${[[result.score+'/'+result.total,'মোট স্কোর'],[result.correct,'সঠিক'],[result.wrong,'ভুল'],[result.blank,'উত্তরহীন']].map(([v,l])=>`<div class="ec-score"><strong>${bn(v)}</strong><span>${l}</span></div>`).join('')}</div>
      <div class="ec-banner">ইঞ্জিনিয়ারিং অনুশীলনের ফল এই ডিভাইসে সংরক্ষিত। এটি পূর্ণাঙ্গ মডেল টেস্টের জাতীয় র‍্যাংকিং বা ধারাবাহিক অগ্রগতি পরিবর্তন করে না।</div><div class="ec-actions"><button class="ec-button ec-primary" data-ec-retake>একই সেট আবার দিন</button><button class="ec-button" data-ec-back-book>অন্য অধ্যায় / সেট</button></div><h3 class="ec-review-title">উত্তর ও ব্যাখ্যা</h3>${selected.questions.map((q,i)=>questionHtml(q,i,true)).join('')}`;
    math();focusHeading();
  }
  function confirmAction(title,onConfirm) {
    openCustomModal({title,subtitle:'অধ্যায়ভিত্তিক অনুশীলন',icon:'📝',confirmText:'নিশ্চিত করুন',cancelText:'ফিরে যান',showCancel:true,onConfirm});
  }
  function abandon(){clearInterval(timer);state.attempt=null;save();}
  async function open() {
    const root=$('view-engineering-chapters');root.innerHTML='<div class="ec-empty" role="status">বই ও অধ্যায় লোড হচ্ছে…</div>';
    try {
      await load();
      if(appState.currentStream!=='chapters'||!$('view-engineering-chapters'))return;
      if(!state.attempt){const saved=read(storageKey,null);if(saved&&['buet','ckruet'].includes(saved.track)&&bookById(saved.book)?.tracks.includes(saved.track)) {await loadChapter(saved.book,saved.chapter);if(!selection(saved)?.questions.length)throw new Error('saved attempt');state.attempt=saved;state.track=saved.track;state.book=saved.book;}}
      if(state.attempt?.status==='running')renderExam();else if(state.attempt?.status==='submitted')renderResult();else renderCatalog();
    } catch {root.innerHTML='<div class="ec-error" role="alert">অধ্যায়ের প্রশ্ন লোড করা যায়নি। সংযোগ পরীক্ষা করে আবার চেষ্টা করুন। <button class="ec-button" data-ec-retry>আবার চেষ্টা</button></div>';}
  }
  function guardNavigation(stream){
    if(appState.currentStream==='chapters'&&stream!=='chapters'&&state.attempt?.status==='running'){
      confirmAction('চলতি অধ্যায় পরীক্ষা বাতিল করে বের হবে?',()=>{abandon();switchStream(stream);});return true;
    }return false;
  }
  document.addEventListener('click',event=>{
    const target=event.target.closest('#view-engineering-chapters button');if(!target)return;
    const d=target.dataset;
    if(d.ecTrack){if(state.attempt?.status==='running'){confirmAction('চলতি পরীক্ষা বাতিল করে লক্ষ্য বদলাবে?',()=>{abandon();state.track=d.ecTrack;state.book=null;renderCatalog();});return;}abandon();state.track=d.ecTrack;state.book=null;state.search='';renderCatalog();}
    else if('ecResearch'in d){if(state.attempt?.status==='running')return;state.book=null;renderResearch();}
    else if(d.ecBook){state.book=d.ecBook;state.search='';renderCatalog();focusHeading();}
    else if('ecHome'in d){state.book=null;state.search='';renderCatalog();focusHeading();}
    else if(d.ecSet)start(d.ecChapter,d.ecSet);
    else if('ecAnswer'in d){const i=Number(d.ecIndex),a=Number(d.ecAnswer);state.attempt.answers[i]=a;save();target.closest('.ec-options').querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b===target)));updateCount();}
    else if('ecClear'in d){delete state.attempt.answers[Number(d.ecClear)];save();$('ec-q-'+d.ecClear).querySelectorAll('.ec-option').forEach(b=>b.setAttribute('aria-pressed','false'));updateCount();}
    else if('ecSubmit'in d)confirmAction('উত্তরপত্র জমা দিয়ে ফলাফল দেখবে?',finish);
    else if('ecCancel'in d)confirmAction('চলতি অধ্যায় পরীক্ষা বাতিল করবে?',()=>{abandon();renderCatalog();});
    else if('ecRetake'in d){const a=state.attempt;abandon();start(a.chapter,a.set);}
    else if('ecBackBook'in d){abandon();renderCatalog();focusHeading();}
    else if('ecRetry'in d)open();
  });
  document.addEventListener('input',event=>{if(event.target.id==='ec-search'){state.search=event.target.value;renderChapters(bookById(state.book));}});
  window.addEventListener('beforeunload',event=>{if(state.attempt?.status==='running'){save();event.preventDefault();event.returnValue='';}});
  document.addEventListener('visibilitychange',()=>{if(state.attempt?.status==='running'){save();if(document.visibilityState==='visible')tick();}});
  window.EngineeringChapters={open,guardNavigation,guardAction:callback=>{if(state.attempt?.status==='running'){confirmAction('চলতি অধ্যায় পরীক্ষা বাতিল করে বিভাগ বদলাবে?',()=>{abandon();callback();});return true;}return false;},hasRunningAttempt:()=>state.attempt?.status==='running'};
  window.addEventListener('load',()=>{if(window.location?.hash==='#engineering-chapters')switchStream('chapters','engineering');});
})();
