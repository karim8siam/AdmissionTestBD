/* Exercise the actual browser modules with deterministic DOM/fetch/storage adapters. */
const fs=require('fs'),vm=require('vm'),assert=require('assert');
function fixture(file,stream,saved={}){
 const elements=new Map(),events={},stores={...saved},pending=[];
 class Element{
  constructor(id){this.id=id;this.dataset={};this._html='';this.textContent='';}
  set innerHTML(s){this._html=s;for(const m of s.matchAll(/id=["']([^"']+)["']/g))elements.set(m[1],new Element(m[1]));}
  get innerHTML(){return this._html;}
  querySelector(){return {disabled:false,setAttribute(){},removeAttribute(){},focus(){}};}
 }
 for(const id of ['view-engineering','view-chapter-practice','view-engineering-chapters'])elements.set(id,new Element(id));
 const ctx={console,URL,Date,Set,Map,JSON,Number,String,Boolean,Math,Promise,Error,appState:{currentStream:stream},document:{getElementById:id=>elements.get(id),addEventListener:(name,fn)=>(events[name]??=[]).push(fn),visibilityState:'visible'},localStorage:{getItem:k=>stores[k]??null,setItem:(k,v)=>stores[k]=v},setInterval:()=>1,clearInterval(){},openCustomModal:config=>pending.push(config.onConfirm),switchStream:s=>ctx.appState.currentStream=s,fetch:async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(url.split('?')[0].replace(/^\//,''),'utf8'))}),window:{addEventListener(){},scrollTo(){},location:{hash:''}}};
 vm.createContext(ctx);vm.runInContext(fs.readFileSync(file,'utf8'),ctx);
 const click=async dataset=>{const target={dataset,setAttribute(){},closest:selector=>selector.includes('options')?{querySelectorAll:()=>[target]}:target};for(const fn of events.click||[])fn({target});await settle();};
 async function settle(){for(let i=0;i<12;i++)await new Promise(resolve=>setImmediate(resolve));}
 return {ctx,elements,stores,pending,click,settle};
}
(async()=>{
 let f=fixture('assets/engineering-practice.js','engineering');await f.ctx.window.EngineeringPractice.open();
 assert.equal((f.elements.get('ep-chapter-grid').innerHTML.match(/data-ep-set/g)||[]).length,100);
 assert(f.elements.get('ep-chapter-grid').innerHTML.includes('disabled'));
 await f.click({epChapter:'buet-model-002',epSet:'buet-model-002-set-1'});assert(!f.stores.admission_engineering_attempt_v3);
 await f.click({epChapter:'buet-model-001',epSet:'buet-model-001-set-1'});assert.equal(JSON.parse(f.stores.admission_engineering_attempt_v3).status,'running');
 const m=JSON.parse(fs.readFileSync('data/engineering_practice.json'));const p=JSON.parse(fs.readFileSync(m.model_books[0].chapters[0].questions_url.slice(1)));
 await f.click({epAnswer:String(p.questions[0].correct_index),epIndex:'0'});
 await f.click({epSubmit:''});f.pending.pop()();
 assert.equal(JSON.parse(f.stores.admission_engineering_progress_v3)['buet:buet-model-001-set-1'].score,1);
 await f.click({epBackBook:''});await f.click({epChapter:'buet-model-002',epSet:'buet-model-002-set-1'});
 assert.equal(JSON.parse(f.stores.admission_engineering_attempt_v3).chapter,'buet-model-002');
 let resume=fixture('assets/engineering-practice.js','engineering',f.stores);await resume.ctx.window.EngineeringPractice.open();assert(resume.elements.get('ep-content').innerHTML.includes('ep-timer'));
 assert(resume.ctx.window.EngineeringPractice.guardNavigation('medical'));resume.pending.pop()();assert.equal(resume.ctx.appState.currentStream,'medical');
 f=fixture('assets/engineering-chapters.js','chapters');await f.ctx.window.EngineeringChapters.open();
 const book=m.books.find(b=>b.id==='buet-chemistry-2');assert(book);
 await f.click({ecBook:book.id});const chapter=book.chapters.find(c=>c.sets.length===3);await f.click({ecChapter:chapter.id,ecSet:chapter.sets[2].id});
 assert(f.ctx.window.EngineeringChapters.hasRunningAttempt());let changed=false;assert(f.ctx.window.EngineeringChapters.guardAction(()=>changed=true));assert(!changed);f.pending.pop()();assert(changed&&!f.ctx.window.EngineeringChapters.hasRunningAttempt());
 const cp=fixture('assets/chapter-practice.js','chapters');let opened=0;cp.ctx.EngineeringChapters={open:()=>opened++};await cp.ctx.window.ChapterPractice.open('engineering');assert.equal(opened,1);assert(cp.elements.get('view-chapter-practice').innerHTML.includes('data-cp-track="engineering"'));
 console.log('PASS: 100 model cards, sequential access, grading, model 2 unlock, resume, navigation guard, unrestricted chapter set 3, shared chapter tab.');
})().catch(e=>{console.error(e);process.exitCode=1});
