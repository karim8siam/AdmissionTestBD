const fs=require('fs'),vm=require('vm'),assert=require('assert');
function fixture(saved={}){
const elements=new Map(),events={},stores={...saved},pending=[];let failFetch=false;
class El{constructor(id){this.id=id;this.dataset={};this.textContent='';this._html='';}set innerHTML(s){this._html=s;for(const m of s.matchAll(/id="([^"]+)"/g))elements.set(m[1],new El(m[1]));}get innerHTML(){return this._html;}contains(){return true;}}
for(const id of ['view-written','engineering-archive'])elements.set(id,new El(id));
const ctx={console,URL,Date,Set,JSON,Number,String,Math,Error,Promise,setInterval:()=>1,clearInterval(){},document:{getElementById:id=>elements.get(id),addEventListener:(e,f)=>(events[e]??=[]).push(f)},localStorage:{getItem:k=>stores[k]??null,setItem:(k,v)=>stores[k]=v},window:{scrollTo(){},confirm:()=>true,openCustomModal:c=>pending.push(c.onConfirm),switchStream:s=>ctx.stream=s},fetch:async url=>{if(failFetch)throw Error('fixture outage');return {ok:true,json:async()=>JSON.parse(fs.readFileSync(url.slice(1),'utf8'))};}};
vm.createContext(ctx);for(const file of ['assets/written-practice.js','assets/engineering-archive.js'])vm.runInContext(fs.readFileSync(file,'utf8'),ctx);
const settle=async()=>{for(let i=0;i<15;i++)await new Promise(r=>setImmediate(r));};
const fire=async(event,dataset={},value='',checked=false)=>{const t={dataset,value,checked};t.closest=()=>t;for(const f of events[event]||[])f({target:t});await settle();};
return {ctx,elements,stores,pending,fire,settle,outage:v=>failFetch=v};
}
(async()=>{
let f=fixture();await f.ctx.window.WrittenPractice.open();assert(f.elements.get('view-written').innerHTML.includes('BUET · PCM'));await f.fire('click',{action:'timed'});let h=f.elements.get('view-written').innerHTML;assert.equal((h.match(/class="wp-question"/g)||[]).length,20);assert(!h.includes('wp-hint'));assert(!h.includes('wp-solution'));
await f.fire('input',{note:'buet-w1-01'},'<img src=x onerror=alert(1)>');assert.equal(JSON.parse(f.stores.admission_written_attempt_v1).buet.notes['buet-w1-01'],'<img src=x onerror=alert(1)>');
let g=fixture(f.stores);await g.ctx.window.WrittenPractice.open();h=g.elements.get('view-written').innerHTML;assert(h.includes('&lt;img'));assert(!h.includes('<img src=x'));
assert(g.ctx.window.WrittenPractice.guardNavigation('chapters'));assert(!g.ctx.stream);g.pending.pop()();assert.equal(g.ctx.stream,'chapters');
await g.fire('click',{action:'submit'});assert.equal(JSON.parse(g.stores.admission_written_attempt_v1).buet.status,'running');g.pending.pop()();assert.equal(JSON.parse(g.stores.admission_written_attempt_v1).buet.status,'submitted');assert.equal((g.elements.get('view-written').innerHTML.match(/class="wp-solution"/g)||[]).length,20);
await g.fire('change',{criterion:'buet-w1-01',index:'0'},'',true);assert(g.elements.get('wp-score').textContent.includes('৩/২০০'));
await g.fire('click',{track:'du'});await g.fire('click',{action:'practice'});h=g.elements.get('view-written').innerHTML;assert.equal((h.match(/class="wp-hint"/g)||[]).length,20);assert(!h.includes('wp-solution'));
// Both track attempts persist independently.
assert(JSON.parse(g.stores.admission_written_attempt_v1).buet.criteria['buet-w1-01']['0']);assert(JSON.parse(g.stores.admission_written_attempt_v1).du);
let expired=JSON.parse(f.stores.admission_written_attempt_v1);expired.buet.endsAt=Date.now()-1000;let e=fixture({admission_written_attempt_v1:JSON.stringify(expired)});await e.ctx.window.WrittenPractice.open();assert.equal(JSON.parse(e.stores.admission_written_attempt_v1).buet.status,'submitted');
await g.ctx.window.EngineeringArchive.open();h=g.elements.get('engineering-archive').innerHTML;assert.equal((h.match(/class="ea-card"/g)||[]).length,8);assert(h.includes('আংশিক প্রকাশ্য প্রিভিউ'));assert(!h.includes('startPastYearExam'));
await g.fire('change',{filter:'institution'},'ckruet');h=g.elements.get('engineering-archive').innerHTML;assert.equal((h.match(/class="ea-card"/g)||[]).length,1);await g.fire('change',{filter:'kind'},'written');assert(g.elements.get('engineering-archive').innerHTML.includes('এই ফিল্টারে কোনো উৎস নেই'));
let outage=fixture();outage.outage(true);await outage.ctx.window.WrittenPractice.open();assert(outage.elements.get('view-written').innerHTML.includes('আবার চেষ্টা'));outage.outage(false);await outage.fire('click',{action:'retry'});assert(outage.elements.get('view-written').innerHTML.includes('BUET · PCM'));
console.log('PASS: 20 questions per track, timed hints hidden, safe notes, reload, navigation guard, submission, rubric self-score, independent tracks, expiry, archive filters and loading recovery.');
})().catch(e=>{console.error(e);process.exitCode=1});
