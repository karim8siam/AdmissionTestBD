"""Build isolated, lazy-loaded engineering practice for the existing static site."""
import copy,hashlib,json,random,collections
from pathlib import Path
from build_chapter_practice import catalog
from engineering_questions import chapter_pool
ROOT=Path(__file__).parent

def write_json(path, data):
    raw=json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n'
    for prefix in [ROOT,ROOT/'public']:
        file=prefix/path;file.parent.mkdir(parents=True,exist_ok=True);file.write_text(raw)
    return raw

def build():
    manifest={'version':1,'generated_on':'2026-10-11','books':[],
      'provenance':'original_practice_not_authenticated_past_papers',
      'references_url':'/data/engineering_research.json?v=1',
      'tracks':['buet','ckruet']}
    all_items=[]; all_stems=set(); subjects=collections.defaultdict(list)
    books=[b for b in catalog() if b['subject'] in ['HigherMath','Physics','Chemistry']]
    for track in ['buet','ckruet']:
        for source in books:
            b={k:copy.deepcopy(source[k]) for k in ['subject','paper','title','kind']}
            b.update(id=track+'-'+source['id'],tracks=[track],chapters=[])
            for c in source['chapters']:
                q=chapter_pool(source,c,track)
                random.Random(track+c['id']).shuffle(q)
                # Chemistry applications spread over all 3 sets rather than isolated in set 3.
                if source['subject']=='Chemistry' and c['id']!='chemistry-1-01':
                    concepts=[x for x in q if x['difficulty']=='concept']; apps=[x for x in q if x['difficulty']=='application']
                    q=[]
                    while concepts or apps:
                        q.extend(concepts[:2]);del concepts[:2]
                        q.extend(apps[:1]);del apps[:1]
                cid=track+'-'+c['id']
                sets=[]
                for n in range(3 if source['subject']=='Chemistry' else 1):
                    ids=[x['id'] for x in q[n*100:(n+1)*100]]
                    assert len(ids)==100
                    sets.append({'id':cid+'-set-'+str(n+1),'number':n+1,'question_ids':ids,'question_count':100,'minutes':60 if track=='buet' else 90})
                payload={'id':cid,'questions':q,'sets':sets}
                raw=json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n'
                digest=hashlib.sha256(raw.encode()).hexdigest()[:12]
                url=f'/data/engineering_chapters/{cid}.{digest}.json'
                write_json(Path(url[1:]),payload)
                b['chapters'].append({'id':cid,'number':c['number'],'title':c['title'],'question_count':len(q),'target_questions':len(q),'questions_url':url,'sets':[{k:v for k,v in s.items() if k!='question_ids'} for s in sets]})
                all_items+=q;all_stems.update(x['question_bn'] for x in q)
                subjects[(track,source['subject'])].append((c['id'],q))
            b['available_questions']=sum(c['question_count'] for c in b['chapters'])
            manifest['books'].append(b)
        # One 100-question mixed test per track; chapter-bank reuse explicitly disclosed.
        mixed=[]
        for subject,count in [('HigherMath',34),('Physics',33),('Chemistry',33)]:
            groups=subjects[(track,subject)]
            rng=random.Random(track+subject+'mixed-v1')
            shuffled=[]
            for cid,pool in groups:
                options=[x for x in pool if x['difficulty']=='application'] or list(pool)
                rng.shuffle(options);shuffled.append(options)
            for n in range(count):
                mixed.append(shuffled[n%len(groups)][n//len(groups)])
        assert len(mixed)==len({x['id'] for x in mixed})==100
        mid=track+'-mixed-01'
        minutes=60 if track=='buet' else 120
        sets=[{'id':mid+'-set-1','number':1,'question_count':100,'question_ids':[q['id'] for q in mixed],'minutes':minutes}]
        payload={'id':mid,'questions':mixed,'sets':sets}
        raw=json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n'
        digest=hashlib.sha256(raw.encode()).hexdigest()[:12]
        url=f'/data/engineering_chapters/{mid}.{digest}.json';write_json(Path(url[1:]),payload)
        manifest['books'].append({'id':track+'-mixed','subject':'Mixed','paper':'','title':'১০০ প্রশ্নের মিশ্র PCM অনুশীলন','kind':'mixed','tracks':[track],'available_questions':100,'note':'অধ্যায়ব্যাংক থেকে বাছাই করা প্রশ্ন; গণিত ৩৪, পদার্থ ৩৩, রসায়ন ৩৩।','chapters':[{'id':mid,'number':1,'title':'মিশ্র অনুশীলন ১','question_count':100,'target_questions':100,'questions_url':url,'sets':[{k:v for k,v in sets[0].items() if k!='question_ids'}]}]})
    counts={'chapter_entries':len(all_items),'unique_questions':len({x['id'] for x in all_items}),'unique_stems':len(all_stems),'chapter_questions_per_track':7100,'mixed_tests':2,'question_families':'4 foundation and 2 application families per math/physics chapter; Chemistry concept-pair and application families. Numerical variants share methods.','shared_chemistry_core':True,'teacher_reviewed':False,'authenticated_past_paper_questions':0}
    manifest['coverage']=counts
    write_json(Path('data/engineering_practice.json'),manifest)
    audit=json.loads((ROOT/'content/engineering/sources.json').read_text())
    research={'researched_on':'2026-10-11','coverage':counts,'sources':audit['sources'],'book_recommendations':[
      {'subject':'পদার্থবিজ্ঞান','main':'ইসহাক','supplement':'শাহজাহান তপন / গিয়াসউদ্দীন; CKRUET মিল-তালিকায় শাহজাহান রহমান সেলিম ও জাকারিয়া তৌহিদও রয়েছে।'},
      {'subject':'রসায়ন','main':'হাজারী','supplement':'আবু সালেক / গুহ'},
      {'subject':'উচ্চতর গণিত','main':'কেতাব উদ্দিন','supplement':'রফিকুল ইসলাম'}],
      'book_note':'AAP-এর ২০২১ প্রস্তুতি পরিকল্পনার সুপারিশ। বইয়ের পূর্ণ কপি বা বর্তমান সংস্করণ পড়া হয়েছে এমন দাবি নয়।',
      'exam_notes':{'buet':'প্রিলিমিনারি ২০২০–২১ থেকে চালু ছিল। ২০২৫–২৬ বিজ্ঞপ্তিতে PCM লিখিত পরীক্ষা: প্রতি বিষয়ে ২০ প্রশ্ন, মোট ৬০০ নম্বর, ৩ ঘণ্টা। পরবর্তী সেশনের বিজ্ঞপ্তি মিলিয়ে নাও। এখানে ঐতিহাসিক প্রিলি ধাঁচের MCQ অনুশীলন।','ckruet':'২০২৩–২৪ সমন্বিত পরীক্ষায় গণিত, পদার্থ, রসায়ন ও ইংরেজি—প্রতিটি ২৫টি প্রশ্ন, মোট ৫০০ নম্বর, ১৫০ মিনিট। এখানে ইংরেজি বাদ দিয়ে কাস্টম PCM অনুশীলন; এটি হুবহু অফিসিয়াল মডেল নয়। পরবর্তী পৃথক বিশ্ববিদ্যালয়ের বিজ্ঞপ্তি মিলিয়ে নাও।'}}
    write_json(Path('data/engineering_research.json'),research)
    (ROOT/'ENGINEERING_COVERAGE.md').write_text('# Engineering practice coverage\n\n'+json.dumps(counts,ensure_ascii=False,indent=2)+'\n\nAll 51 PCM chapters per track are available. Mathematics/Physics: 100 per chapter. Chemistry: three disjoint sets of 100 per chapter. Mixed practice reuses chapter questions. Track progress is separate; Chemistry shares an authored concept core. No authentic past-paper question bank or full ten-year analysis is claimed.\n')
    print(json.dumps(counts))

if __name__=='__main__':build()
