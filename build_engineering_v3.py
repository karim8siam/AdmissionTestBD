"""Build chapter practice separately from 100 reviewed model papers per track."""
import json,hashlib,random,collections,copy
from pathlib import Path
from build_chapter_practice import catalog
from engineering_v2 import mathematics,physics,chemistry,challenges,physics_challenges
from engineering_v2.core import REGISTRY,pool
from engineering_v2.review import BLOCKED,review_question,model_eligible,review_paper,method_id
ROOT=Path(__file__).parent
SUBJECTS=['HigherMath','Physics','Chemistry']
def write(path,obj):
    raw=json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n'
    for root in [ROOT,ROOT/'public']:
        p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(raw)
    return raw
def payload(cid,questions,sets):
    raw=json.dumps({'id':cid,'questions':questions,'sets':sets},ensure_ascii=False,separators=(',',':'))+'\n'
    h=hashlib.sha256(raw.encode()).hexdigest()[:12]
    url=f'/data/engineering_v3/{cid}.{h}.json'
    write(Path(url[1:]),{'id':cid,'questions':questions,'sets':sets})
    return url
def build_bank():
    for cid,fs in REGISTRY.items():REGISTRY[cid]=[f for f in fs if f['id'] not in BLOCKED]
    bank={};summary=[];rejections=collections.Counter()
    books=[b for b in catalog() if b['subject'] in SUBJECTS]
    for b in books:
        for chapter in b['chapters']:
            target=300 if b['subject']=='Chemistry' else 100
            questions=pool(chapter,target)
            accepted=[]
            for q in questions:
                issues=review_question(q)
                if issues:rejections.update(issues);continue
                q['subject']=b['subject'];q['paper']=b['paper'];q['book_title']=b['title'];accepted.append(q)
            # Safety gets a small curated collection, never 300 numeric clones.
            bank[chapter['id']]=accepted
            summary.append({'id':chapter['id'],'subject':b['subject'],'title':chapter['title'],'target':target,'available':len(accepted),'methods':len({q['family_id'] for q in accepted})})
    return books,bank,summary,rejections
def make_models(bank,track):
    groups=collections.defaultdict(list)
    for qs in bank.values():
        for q in qs:
            if model_eligible(q):groups[q['subject']].append(q)
    use=collections.Counter();family_use=collections.Counter();papers=[];previous=set()
    hard_counts={'buet':{'HigherMath':14,'Physics':14,'Chemistry':12},'ckruet':{'HigherMath':10,'Physics':10,'Chemistry':10}}
    for number in range(1,101):
        rng=random.Random('engineering-reviewed-v3:'+track+str(number));selected=[];families=set();chapter_count=collections.Counter()
        for subject,target in [('HigherMath',34),('Physics',33),('Chemistry',33)]:
            for wanted,count in [('hard',hard_counts[track][subject]),('medium',target-hard_counts[track][subject])]:
                for slot in range(count):
                    candidates=[q for q in groups[subject] if method_id(q) not in families and q['difficulty']==wanted and use[q['id']]<5 and chapter_count[q['chapter_id']]<6]
                    if not candidates:raise ValueError(f'Insufficient reviewed {track} {number} {subject} {wanted}')
                    # Diversity in both chapter and method beats arithmetic size.
                    scored=[]
                    for q in candidates:
                        score=chapter_count[q['chapter_id']]*30+use[q['id']]*4+family_use[q['family_id']]*0.3
                        if q['family_id'] in previous:score+=3
                        if q['question_type'] in ['conceptual','classification']:score+=2
                        scored.append((score+rng.random()*2,q))
                    q=min(scored,key=lambda x:x[0])[1]
                    selected.append(copy.deepcopy(q));families.add(method_id(q));chapter_count[q['chapter_id']]+=1
                    use[q['id']]+=1;family_use[q['family_id']]+=1
        # Group subjects in the familiar order; vary questions within each.
        out=[]
        for subject in SUBJECTS:
            rows=[q for q in selected if q['subject']==subject];rng.shuffle(rows);out+=rows
        report=review_paper(out,track)
        previous=families;papers.append((number,out,report))
    return papers,use
def build():
    books,bank,summary,rejections=build_bank()
    manifest={'version':3,'generated_on':'2026-10-11','books':[],'model_books':[],'tracks':['buet','ckruet'],'references_url':'/data/engineering_research.json?v=3','quality_url':'/data/engineering_quality.json?v=3'}
    model_reports=[];model_usage={}
    for track in manifest['tracks']:
        for b in books:
            book={k:copy.deepcopy(b[k]) for k in ['subject','paper','title','kind']};book.update(id=track+'-'+b['id'],tracks=[track],chapters=[])
            for c in b['chapters']:
                questions=copy.deepcopy(bank[c['id']]);random.Random(track+c['id']).shuffle(questions)
                cid=track+'-'+c['id'];sets=[]
                for start in range(0,len(questions),100):
                    subset=questions[start:start+100];number=start//100+1
                    sets.append({'id':cid+'-set-'+str(number),'number':number,'question_ids':[q['id'] for q in subset],'question_count':len(subset),'minutes':max(15,round(len(subset)*(0.75 if track=='buet' else 0.9)))})
                url=payload(cid,questions,sets)
                book['chapters'].append({'id':cid,'number':c['number'],'title':c['title'],'question_count':len(questions),'target_questions':300 if b['subject']=='Chemistry' else 100,'method_count':len({q['family_id'] for q in questions}),'questions_url':url,'sets':[{k:v for k,v in s.items() if k!='question_ids'} for s in sets]})
            book['available_questions']=sum(c['question_count'] for c in book['chapters']);manifest['books'].append(book)
        models,use=make_models(bank,track);model_usage[track]={'question_appearances':sum(use.values()),'distinct_questions_used':len(use),'max_repeat_across_papers':max(use.values())}
        book={'id':track+'-models','title':('BUET প্রিলি' if track=='buet' else 'CKRUET PCM')+' · ১০০ মডেল টেস্ট','tracks':[track],'subject':'Mixed','kind':'models','chapters':[],'available_questions':10000}
        for number,questions,review in models:
            cid=track+f'-model-{number:03d}';sets=[{'id':cid+'-set-1','number':1,'question_count':100,'question_ids':[q['id'] for q in questions],'minutes':60 if track=='buet' else 120}]
            url=payload(cid,questions,sets)
            book['chapters'].append({'id':cid,'number':number,'title':'মডেল টেস্ট '+str(number),'question_count':100,'target_questions':100,'questions_url':url,'sets':[{k:v for k,v in sets[0].items() if k!='question_ids'}],'quality':review})
            model_reports.append({'track':track,'paper':number,**review})
        manifest['model_books'].append(book)
    coverage={'chapter_questions_per_track':sum(len(v) for v in bank.values()),'distinct_questions_in_core':len({q['id'] for v in bank.values() for q in v}),'chapters_per_track':51,'authored_methods':len({q['family_id'] for v in bank.values() for q in v}),'model_tests_per_track':100,'questions_per_model':100,'model_usage':model_usage,'teacher_reviewed':False,'authenticated_past_paper_questions':0,'shared_core_between_tracks':True,'parameter_variants_in_chapters':True,'chapter_targets_complete':all(x['available']==x['target'] for x in summary)}
    manifest['coverage']=coverage;write(Path('data/engineering_practice.json'),manifest)
    sources=json.loads((ROOT/'content/engineering/sources.json').read_text())['sources']
    research={'researched_on':'2026-10-11','coverage':coverage,'sources':sources,'book_recommendations':[{'subject':'পদার্থবিজ্ঞান','main':'ইসহাক','supplement':'শাহজাহান তপন / গিয়াসউদ্দীন'},{'subject':'রসায়ন','main':'হাজারী','supplement':'আবু সালেক / গুহ'},{'subject':'উচ্চতর গণিত','main':'কেতাব উদ্দিন','supplement':'রফিকুল ইসলাম'}],'book_note':'ঐতিহাসিক প্রস্তুতি পরিকল্পনার রেফারেন্স প্রার্থী; বইয়ের পূর্ণ কপি বা সব সংস্করণ পড়া হয়েছে এমন দাবি নয়।','exam_notes':{'buet':'ঐতিহাসিক BUET প্রিলি ধাঁচের MCQ। পরবর্তী লিখিত পরীক্ষার বিকল্প নয়; নিজের সেশনের বিজ্ঞপ্তি দেখো।','ckruet':'ইংরেজি বাদ দিয়ে কাস্টম ১০০ প্রশ্নের PCM মডেল। ঐতিহাসিক পূর্ণাঙ্গ CKRUET distribution-এর হুবহু প্রতিলিপি নয়।'}}
    write(Path('data/engineering_research.json'),research)
    report={'version':3,'coverage':coverage,'chapter_review':summary,'blocked_families':BLOCKED,'rejections':dict(rejections),'paper_checks':{'question_count':100,'distinct_methods_per_paper':100,'distribution':{'HigherMath':34,'Physics':33,'Chemistry':33},'minimum_difficult_questions':{'buet':40,'ckruet':30},'max_same_chapter_questions':6},'limitations':['Difficulty is an editorial estimate, not calibrated student performance.','Rules and numerical spot checks are not independent teacher review.','Chapter questions include parameter variants; model papers sample the bank and can reuse questions across papers.','Some chemistry chapters have a shorter curated set rather than padding their counts.','Past-paper inspection is sampled and includes third-party compilations, not an authenticated ten-year corpus.'],'papers':model_reports}
    write(Path('data/engineering_quality.json'),report)
    (ROOT/'ENGINEERING_COVERAGE.md').write_text('# Engineering revision 3\n\n'+json.dumps(coverage,ensure_ascii=False,indent=2)+'\n\nChapter practice is separate from model tests. All 200 model papers pass the structural review gate. No model repeats a problem family within itself. Chemistry shortfalls are displayed rather than filled with fact-pair permutations. See data/engineering_quality.json for actual coverage and limits.\n')
    print(json.dumps(coverage));print('Short chapters:',[(x['id'],x['available']) for x in summary if x['available']<x['target']])
if __name__=='__main__':build()
