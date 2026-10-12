/* Independent chapter practice. Full-test locks and rankings are never modified. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const bn = value => String(value).replace(/[0-9]/g,d=>'০১২৩৪৫৬৭৮৯'[Number(d)]);
  const trackTitle = track => track === 'medical' ? 'মেডিকেল' : 'ভার্সিটি বিজ্ঞান';
  const subjectNames = {Biology:'জীববিজ্ঞান',Chemistry:'রসায়ন',Physics:'পদার্থবিজ্ঞান',HigherMath:'উচ্চতর গণিত',English:'ইংরেজি', 'General Knowledge':'সাধারণ জ্ঞান',Bangla:'বাংলা',ICT:'তথ্য ও যোগাযোগ প্রযুক্তি'};
  let data = null, loading = null, state = {track:'medical',book:null,search:'',attempt:null}, timer = null;
  const storageKey = 'admission_chapter_attempt_v2';
  function read(key, fallback) { try { return JSON.parse(localStorage.getItem(key)) || fallback; } catch { return fallback; } }
  function save() { try { localStorage.setItem(storageKey,JSON.stringify(state.attempt)); } catch {} }
  function progress() { return read('admission_chapter_progress_v2',{}); }
  function bookById(id) { return data?.books.find(b=>b.id===id); }
  function selection(attempt=state.attempt) {
    const book=bookById(attempt?.book),chapter=book?.chapters.find(c=>c.id===attempt?.chapter),set=chapter?.sets.find(s=>s.id===attempt?.set);
    if(!set) return null;
    const ids=new Set(set.question_ids || []),questions=(chapter.questions || []).filter(q=>ids.has(q.id));
    return {book,chapter,set,questions};
  }
  async function load() {
    if(data) return data;
    if(!loading) loading=fetch('/data/chapter_practice.json?v=2').then(r=>{if(!r.ok) throw new Error('load');return r.json();}).then(d=>{if(!Array.isArray(d.books))throw new Error('shape');data=d;return d;}).finally(()=>{loading=null;});
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
  function focusHeading() { const h=$('cp-content')?.querySelector('h2, h1'); if(h){h.tabIndex=-1;h.focus({preventScroll:true});} }
  function renderHeader() {
    const root=$('view-chapter-practice');root.dataset.track=state.track;
    root.innerHTML=`<div class="cp-head"><div class="cp-eyebrow">অধ্যায়ভিত্তিক অনুশীলন · সম্পূর্ণ ফ্রি</div>
      <h1>একটি অধ্যায়, মনোযোগী প্রস্তুতি</h1><p>তোমার ভর্তি লক্ষ্য বেছে নাও, তারপর বই ও অধ্যায় নির্বাচন করো। যেকোনো উপলব্ধ সেট দিয়ে শুরু করা যাবে—আগের কোনো টেস্ট শেষ করার শর্ত নেই।</p>
      <div class="cp-tabs" role="tablist" aria-label="ভর্তি প্রস্তুতির লক্ষ্য"><button role="tab" aria-selected="${state.track==='medical'}" data-cp-track="medical">🩺 মেডিকেল</button><button role="tab" aria-selected="${state.track==='versity'}" data-cp-track="versity">🏛️ ভার্সিটি বিজ্ঞান</button><button role="tab" aria-selected="${state.track==='engineering'}" data-cp-track="engineering">⚙️ ইঞ্জিনিয়ারিং</button><button role="tab" aria-selected="false" data-cp-track="humanities">মানবিক</button><button role="tab" aria-selected="false" data-cp-track="business">ব্যবসায় শিক্ষা</button></div></div><div id="cp-content"></div>`;
  }
  function renderCatalog() {
    renderHeader();
    if(state.track==='engineering'){ $('cp-content').innerHTML='<section id="view-engineering-chapters"></section>';EngineeringChapters.open();return;}
    const book=bookById(state.book),container=$('cp-content');
    if(book && book.tracks.includes(state.track)) {renderBook(book);return;}
    state.book=null;
    const books=data.books.filter(b=>b.tracks.includes(state.track));
    const subjects=[...new Set(books.map(b=>b.subject))];
    container.innerHTML=`<h2 class="cp-review-title">${trackTitle(state.track)} প্রস্তুতি: বই / বিষয় নির্বাচন</h2>
      <p class="cp-muted">বিজ্ঞান বিষয়গুলো পত্র অনুযায়ী আলাদা। ইংরেজি ও সাধারণ জ্ঞান টপিক অনুযায়ী সাজানো। বিশ্ববিদ্যালয় ও ইউনিটভেদে বিষয়ের চাহিদা আলাদা—নিজের ভর্তি বিজ্ঞপ্তি মিলিয়ে নাও।</p>
      ${subjects.map(subject=>`<section class="cp-book-group"><h2>${esc(subjectNames[subject]||subject)}</h2><div class="cp-grid">${books.filter(b=>b.subject===subject).map(b=>`<button class="cp-card cp-card-button" data-cp-book="${b.id}"><span class="cp-tag ${b.available_questions?'cp-tag-ready':''}">${b.kind==='topics'?'টপিকভিত্তিক':'বই / পত্রভিত্তিক'}</span><h3>${esc(b.title)}</h3><p class="cp-muted">${bn(b.chapters.length)} অধ্যায় / টপিক · ${bn(b.available_questions)} প্রশ্ন</p><p class="cp-muted">${b.available_questions?'অধ্যায় বেছে নাও →':'প্রশ্ন যোগ হলে অনুশীলন চালু হবে'}</p></button>`).join('')}</div></section>`).join('')}`;
  }
  function renderBook(book) {
    const container=$('cp-content');
    container.innerHTML=`<nav class="cp-crumbs" aria-label="অধ্যায়ের পথ"><button data-cp-home>← সব বই / বিষয়</button><span>/ ${trackTitle(state.track)}</span><span>/ ${esc(book.title)}</span></nav>
      <h2 class="cp-review-title">${esc(book.title)}</h2><p class="cp-muted">${book.subject==='Chemistry'?'প্রতি অধ্যায়ে ৩টি পৃথক সেট × ১০০ প্রশ্ন।':'প্রতি অধ্যায়ে ১০০ প্রশ্নের একটি সেট।'} বিদ্যমান প্রশ্নব্যাংক ও নতুন মৌলিক অনুশীলনী মিলিয়ে সাজানো। সেটগুলোর মধ্যে একই প্রশ্ন পুনরাবৃত্তি করা হয়নি।</p>
      ${book.note?`<p class="cp-muted">${esc(book.note)}</p>`:""}<p class="cp-muted">নতুন ধারণাভিত্তিক প্রশ্নে দুটি বক্তব্য বিচার করতে হবে। পদার্থবিজ্ঞান ও গণিতে ভিন্ন সংখ্যার সূত্রভিত্তিক অনুশীলন রয়েছে।</p>
      <div class="cp-toolbar"><label class="cp-muted" for="cp-search">অধ্যায় খুঁজুন</label><input id="cp-search" class="cp-search" type="search" placeholder="অধ্যায়ের নাম লিখুন…" value="${esc(state.search)}"><span class="cp-tag">সব সেটে সরাসরি প্রবেশ</span></div>
      <div id="cp-chapter-grid" class="cp-grid"></div>`;
    renderChapters(book);
  }
  function renderChapters(book) {
    const chapters=book.chapters.filter(c=>c.title.toLocaleLowerCase().includes(state.search.toLocaleLowerCase())),done=progress();
    $('cp-chapter-grid').innerHTML=chapters.length?chapters.map(c=>`<article class="cp-card"><div class="cp-chapter-number">${book.kind==='topics'?'টপিক':'অধ্যায়'} ${bn(c.number)}</div><h3>${esc(c.title)}</h3>
      <p class="cp-muted">${bn(c.question_count)} প্রশ্ন উপলব্ধ${c.question_count<c.target_questions?` · লক্ষ্য ${bn(c.target_questions)}`:''}</p>
      ${c.sets.map(s=>{const count=s.question_count ?? s.question_ids.length,p=done[`${state.track}:${s.id}`];return `<button class="cp-button cp-set ${count?'cp-primary':''}" data-cp-set="${s.id}" data-cp-chapter="${c.id}" ${count?'':'disabled'}><span>সেট ${bn(s.number)} ${p?'✓':''}</span><span>${count?`${bn(count)} প্রশ্ন · শুরু →`:'প্রশ্ন আসছে'}</span></button>${p?`<p class="cp-status">শেষ ফল: ${bn(p.score)}/${bn(p.total)}</p>`:''}`;}).join('')}
      ${!c.question_count?'<p class="cp-muted" style="margin-top:12px">এই অধ্যায়ের প্রশ্ন এখনো প্রস্তুত নয়।</p>':''}</article>`).join(''):`<div class="cp-empty">${book.chapters.length?'এই নামে কোনো অধ্যায় পাওয়া যায়নি।':esc(book.note||'এই বিষয়ে প্রশ্ন এখনো যুক্ত হয়নি।')}</div>`;
  }
  function questionHtml(q,index,review=false) {
    const answer=state.attempt.answers[index],letters=['ক','খ','গ','ঘ'];
    return `<article class="cp-question" id="cp-q-${index}"><span class="cp-tag">প্রশ্ন ${bn(index+1)}</span>${review?` <span class="cp-status">${answer===undefined?'উত্তর দেওয়া হয়নি':answer===q.correct_index?'✓ সঠিক':'✕ ভুল'}</span>`:''}
      <h3>${esc(q.question_bn)}</h3><div class="cp-options" role="group" aria-label="প্রশ্ন ${index+1} এর উত্তর">${q.options.map((option,i)=>`<button class="cp-option ${review&&i===q.correct_index?'cp-correct':review&&answer===i?'cp-wrong':''}" ${review?'disabled':`data-cp-answer="${i}" data-cp-index="${index}"`} aria-pressed="${answer===i}"><span class="cp-letter">${letters[i]}.</span><span>${esc(option)}</span></button>`).join('')}</div>
      ${!review?`<button class="cp-button" style="margin-top:10px" data-cp-clear="${index}">উত্তর মুছুন</button>`:`<div class="cp-explanation"><strong>সঠিক উত্তর: ${letters[q.correct_index]}. ${esc(q.options[q.correct_index])}</strong><p>${esc(q.explanation||'এই প্রশ্নের বিস্তারিত ব্যাখ্যা এখনো যুক্ত হয়নি।')}</p>${q.book_reference?`<p class="cp-muted">রেফারেন্স: ${esc(q.book_reference)}</p>`:''}</div>`}</article>`;
  }
  function math() { if(window.renderMathInElement)window.renderMathInElement($('cp-content'),{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false}); }
  async function start(chapterId,setId) {
    const track=state.track,bookId=state.book;
    if(state.attempt?.status==='running')return;
    const button=$('view-chapter-practice').querySelector(`[data-cp-set="${setId}"]`);
    if(button){button.disabled=true;button.setAttribute('aria-busy','true');}
    try {await loadChapter(bookId,chapterId);} catch {
      if(button){button.disabled=false;button.removeAttribute('aria-busy');}
      confirmAction('প্রশ্ন লোড হয়নি। আবার চেষ্টা করবে?',()=>start(chapterId,setId));return;
    }
    if(button){button.disabled=false;button.removeAttribute('aria-busy');}
    if(state.track!==track||state.book!==bookId||appState.currentStream!=='chapters'||state.attempt?.status==='running')return;
    const attempt={track:state.track,book:state.book,chapter:chapterId,set:setId,answers:{},status:'running'};
    const selected=selection(attempt);if(!selected?.questions.length)return;
    const minutes=Math.max(1,Math.ceil(selected.questions.length*.6));attempt.deadline=Date.now()+minutes*60000;attempt.startedAt=Date.now();state.attempt=attempt;save();renderExam();
  }
  function renderExam() {
    const selected=selection();if(!selected){state.attempt=null;save();renderCatalog();return;}
    state.track=state.attempt.track;state.book=state.attempt.book;renderHeader();
    $('cp-content').innerHTML=`<h2 class="cp-review-title">${esc(selected.chapter.title)} · সেট ${bn(selected.set.number)}</h2><p class="cp-muted">${trackTitle(state.track)} · ${esc(selected.book.title)} · ${bn(selected.questions.length)} প্রশ্ন · সঠিক +১, ভুল −০.২৫</p>
      <div class="cp-exam-bar"><div><div class="cp-muted">অবশিষ্ট সময়</div><div id="cp-timer" class="cp-timer" role="timer"></div></div><p id="cp-answer-count" class="cp-muted" aria-live="polite"></p><button class="cp-button cp-primary" data-cp-submit>পরীক্ষা জমা দিন</button><button class="cp-button" data-cp-cancel>বাতিল করুন</button></div><div>${selected.questions.map((q,i)=>questionHtml(q,i)).join('')}</div><div class="cp-actions"><button class="cp-button cp-primary" data-cp-submit>পরীক্ষা জমা দিন</button></div>`;
    math();clearInterval(timer);tick();if(state.attempt.status==='running')timer=setInterval(tick,1000);
  }
  function tick() {
    if(state.attempt?.status!=='running')return;
    const seconds=Math.max(0,Math.ceil((state.attempt.deadline-Date.now())/1000));
    if($('cp-timer'))$('cp-timer').textContent=`${bn(Math.floor(seconds/60))}:${bn(String(seconds%60).padStart(2,'0'))}`;
    updateCount();if(seconds===0)finish();
  }
  function updateCount() {
    const count=Object.keys(state.attempt.answers).length,total=selection().questions.length;
    if($('cp-answer-count'))$('cp-answer-count').textContent=`${bn(count)}/${bn(total)} উত্তর দেওয়া হয়েছে`;
  }
  function finish() {
    if(state.attempt?.status!=='running')return;clearInterval(timer);state.attempt.status='submitted';state.attempt.finishedAt=Date.now();save();
    const result=score(),done=progress();done[`${state.track}:${state.attempt.set}`]={score:result.score,total:result.total,at:Date.now()};
    try{localStorage.setItem('admission_chapter_progress_v2',JSON.stringify(done));}catch{}
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
    $('cp-content').innerHTML=`<h2 class="cp-review-title">${esc(selected.chapter.title)} · সেট ${bn(selected.set.number)} ফলাফল</h2><p class="cp-muted">${trackTitle(state.track)} · ${esc(selected.book.title)}</p><div class="cp-score-grid">${[[result.score+'/'+result.total,'মোট স্কোর'],[result.correct,'সঠিক'],[result.wrong,'ভুল'],[result.blank,'উত্তরহীন']].map(([v,l])=>`<div class="cp-score"><strong>${bn(v)}</strong><span>${l}</span></div>`).join('')}</div>
      <div class="cp-banner">অধ্যায় অনুশীলনের ফল এই ডিভাইসে সংরক্ষিত। এটি পূর্ণাঙ্গ মডেল টেস্টের জাতীয় র‍্যাংকিং বা ধারাবাহিক অগ্রগতি পরিবর্তন করে না।</div><div class="cp-actions"><button class="cp-button cp-primary" data-cp-retake>একই সেট আবার দিন</button><button class="cp-button" data-cp-back-book>অন্য অধ্যায় / সেট</button></div><h3 class="cp-review-title">উত্তর ও ব্যাখ্যা</h3>${selected.questions.map((q,i)=>questionHtml(q,i,true)).join('')}`;
    math();focusHeading();
  }
  function confirmAction(title,onConfirm) {
    openCustomModal({title,subtitle:'অধ্যায়ভিত্তিক অনুশীলন',icon:'📝',confirmText:'নিশ্চিত করুন',cancelText:'ফিরে যান',showCancel:true,onConfirm});
  }
  function abandon(){clearInterval(timer);state.attempt=null;save();}
  let openRequest=0;
  async function open(track) {
    const request=++openRequest;
    if(track)state.track=track;
    if(state.track==='engineering'){renderCatalog();return;}
    const root=$('view-chapter-practice');root.innerHTML='<div class="cp-empty" role="status">বই ও অধ্যায় লোড হচ্ছে…</div>';
    try {
      await load();
      if(appState.currentStream!=='chapters'||request!==openRequest)return;
      if(!state.attempt){const saved=read(storageKey,null);if(saved&&['medical','versity'].includes(saved.track)&&bookById(saved.book)?.tracks.includes(saved.track)) {await loadChapter(saved.book,saved.chapter);if(!selection(saved)?.questions.length)throw new Error('saved attempt');state.attempt=saved;state.track=saved.track;state.book=saved.book;}}
      if(state.attempt?.status==='running')renderExam();else if(state.attempt?.status==='submitted')renderResult();else renderCatalog();
    } catch {root.innerHTML='<div class="cp-error" role="alert">অধ্যায়ের প্রশ্ন লোড করা যায়নি। সংযোগ পরীক্ষা করে আবার চেষ্টা করুন। <button class="cp-button" data-cp-retry>আবার চেষ্টা</button></div>';}
  }
  function guardNavigation(stream){
    if(appState.currentStream==='chapters'&&stream!=='chapters'&&state.attempt?.status==='running'){
      confirmAction('চলতি অধ্যায় পরীক্ষা বাতিল করে বের হবে?',()=>{abandon();switchStream(stream);});return true;
    }return false;
  }
  document.addEventListener('click',event=>{
    const target=event.target.closest('#view-chapter-practice button');if(!target)return;
    const d=target.dataset;
    if(['humanities','business'].includes(d.cpTrack)){
      const go=()=>{abandon();switchStream(d.cpTrack,'topics');};
      if(window.EngineeringChapters?.guardAction(go))return;
      if(state.attempt?.status==='running'){confirmAction('চলতি পরীক্ষা বাতিল করে লক্ষ্য বদলাবে?',go);return;}go();return;
    }
    if(d.cpTrack){if(window.EngineeringChapters?.guardAction(()=>{abandon();state.track=d.cpTrack;state.book=null;renderCatalog();}))return;if(state.attempt?.status==='running'){confirmAction('চলতি পরীক্ষা বাতিল করে লক্ষ্য বদলাবে?',()=>{abandon();state.track=d.cpTrack;state.book=null;renderCatalog();});return;}abandon();state.track=d.cpTrack;state.book=null;state.search='';renderCatalog();}
    else if(d.cpBook){state.book=d.cpBook;state.search='';renderCatalog();focusHeading();}
    else if('cpHome'in d){state.book=null;state.search='';renderCatalog();focusHeading();}
    else if(d.cpSet)start(d.cpChapter,d.cpSet);
    else if('cpAnswer'in d){const i=Number(d.cpIndex),a=Number(d.cpAnswer);state.attempt.answers[i]=a;save();target.closest('.cp-options').querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b===target)));updateCount();}
    else if('cpClear'in d){delete state.attempt.answers[Number(d.cpClear)];save();$('cp-q-'+d.cpClear).querySelectorAll('.cp-option').forEach(b=>b.setAttribute('aria-pressed','false'));updateCount();}
    else if('cpSubmit'in d)confirmAction('উত্তরপত্র জমা দিয়ে ফলাফল দেখবে?',finish);
    else if('cpCancel'in d)confirmAction('চলতি অধ্যায় পরীক্ষা বাতিল করবে?',()=>{abandon();renderCatalog();});
    else if('cpRetake'in d){const a=state.attempt;abandon();start(a.chapter,a.set);}
    else if('cpBackBook'in d){abandon();renderCatalog();focusHeading();}
    else if('cpRetry'in d)open();
  });
  document.addEventListener('input',event=>{if(event.target.id==='cp-search'){state.search=event.target.value;renderChapters(bookById(state.book));}});
  window.addEventListener('beforeunload',event=>{if(state.attempt?.status==='running'){save();event.preventDefault();event.returnValue='';}});
  document.addEventListener('visibilitychange',()=>{if(state.attempt?.status==='running'){save();if(document.visibilityState==='visible')tick();}});
  window.ChapterPractice={open,guardNavigation,hasRunningAttempt:()=>state.attempt?.status==='running'};
})();
