"""Build honest coverage from authored material. Never pad or fabricate exam sessions."""
import hashlib,json,random,re,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'content/varsity_expansion'
def read(name):return json.loads((SRC/name).read_text())
def norm(s):return re.sub(r'\s+',' ',s.casefold()).strip()
SHARED={'English','Bangla','Economics'}
LABELS={'English':'ইংরেজি','Bangla':'বাংলা','Logic':'যুক্তি ও বিশ্লেষণ','Economics':'অর্থনীতি','Accounting':'হিসাববিজ্ঞান','Management':'ব্যবসায় সংগঠন ও ব্যবস্থাপনা','Finance':'ফিন্যান্স'}
BOOK_CODES={'English':['2852'],'Bangla':['2851'],'Logic':['1860','2860'],'Economics':['1858'],'Accounting':['1886','2886'],'Management':['2885'],'Finance':['1887']}
TRANSLATE=str.maketrans('০১২৩৪৫৬৭৮৯','0123456789')
def validate_question(q):
    errors=[]
    for key in ['id','subject','topic','family','question','explanation','knowledge','provenance','review']:
        if not q.get(key):errors.append('missing_'+key)
    options=q.get('options',[])
    if len(options)!=4 or len(set(norm(x) for x in options))!=4:errors.append('invalid_options')
    if type(q.get('correct_index')) is not int or not 0<=q['correct_index']<len(options):errors.append('answer_index')
    if len(q.get('explanation',''))<20:errors.append('explanation_too_short')
    if q.get('provenance')!='original':errors.append('unsupported_provenance')
    return errors

def validate_paper(paper,questions):
    errors=[];ids=paper.get('question_ids',[])
    if len(ids)!=100:errors.append('requires_100_questions')
    if len(set(ids))!=len(ids):errors.append('duplicate_question_ids')
    if any(i not in questions for i in ids):return errors+['missing_question']
    qs=[questions[i] for i in ids]
    if any(paper.get('track') not in q['tracks'] for q in qs):errors.append('wrong_track')
    if len({norm(q['question']) for q in qs})!=len(qs):errors.append('duplicate_text')
    if any(n>2 for n in Counter(q['family'] for q in qs).values()):errors.append('repeated_family')
    if len({q['family'] for q in qs})<80:errors.append('insufficient_method_variety')
    expected=paper.get('subject_counts',{})
    if not expected or dict(Counter(q['subject'] for q in qs))!=expected:errors.append('subject_distribution')
    if paper.get('kind')!='custom_practice':errors.append('unsupported_official_format')
    if not paper.get('benchmark_review',{}).get('complete'):errors.append('benchmark_review_pending')
    if any(q['review'].get('status')!='independently_checked' for q in qs):errors.append('independent_review_pending')
    return errors

def validate_series(papers,questions):
    errors=[]
    for p in papers:errors += [p['id']+':'+e for e in validate_paper(p,questions)]
    sigs=[tuple(sorted(p['question_ids'])) for p in papers]
    if len(set(sigs))!=len(sigs):errors.append('same_paper_reordered')
    exposure=Counter(i for p in papers for i in p['question_ids'])
    if any(n>5 for n in exposure.values()):errors.append('question_exposure_exceeds_5')
    return errors

def build():
    books=read('books.json');questions=[];topics={}
    for line in (SRC/'questions.tsv').read_text().splitlines():
        if not line or line.startswith('#'):continue
        subject,topic,family,question,answer,w1,w2,w3,explanation,knowledge=line.split('|')
        tracks=['humanities','business'] if subject in SHARED else ['humanities' if subject=='Logic' else 'business']
        tid=subject.lower()+'-'+hashlib.sha256(topic.encode()).hexdigest()[:8]
        qid=subject.lower()+'-'+family
        options=[answer,w1,w2,w3];random.Random(qid).shuffle(options)
        refs=[b['id'] for b in books['books'] if any(code in b['title'].translate(TRANSLATE) for code in BOOK_CODES[subject])]
        q=dict(id=qid,subject=subject,topic=tid,family=family,question=question,options=options,correct_index=options.index(answer),explanation=explanation,knowledge=knowledge,tracks=tracks,reference_books=refs,provenance='original',difficulty='uncalibrated',review={'status':'author_checked','teacher_review':False,'past_paper_calibration':False})
        assert not validate_question(q),(qid,validate_question(q))
        questions.append(q)
        topics.setdefault(tid,dict(id=tid,title=topic,subject=subject,tracks=tracks,target=100,kind='admission_topic',question_ids=[]))['question_ids'].append(qid)
    assert len({q['id'] for q in questions})==len(questions)
    assert len({norm(q['question']) for q in questions})==len(questions)
    assert len({norm(q['knowledge']) for q in questions})==len(questions)
    papers=read('model_papers.json') if (SRC/'model_papers.json').exists() else []
    assert not validate_series(papers,{q['id']:q for q in questions})
    archive=read('archive.json')
    for e in archive:
        assert e['url'].startswith('https://')
        assert not e['complete_verified'] and e['imported_questions']==0
    coverage={}
    for track in ['humanities','business']:
        qs=[q for q in questions if track in q['tracks']]
        ts=[t for t in topics.values() if track in t['tracks']]
        ps=[p for p in papers if p['track']==track]
        coverage[track]=dict(questions=len(qs),knowledge_points=len(qs),knowledge_target=2000,topics=len(ts),complete_chapter_sets=sum(len(t['question_ids'])==100 for t in ts),model_tests=len(ps),model_target=100,archive_entries=sum(e['track']==track for e in archive),verified_complete_past_papers=0,complete=False)
    payload=dict(version='2026-10-12.1',subjects=LABELS,coverage=coverage,topics=list(topics.values()),questions=questions,model_papers=papers,books=books['books'],archive=archive,**read('profiles.json'))
    out=ROOT/'data/varsity_expansion.json';out.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')))
    (SRC/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2))
    print(json.dumps(coverage,ensure_ascii=False,indent=2))
    if '--require-complete' in sys.argv and not all(c['complete'] for c in coverage.values()):
        print('FULL RELEASE BLOCKED: source/benchmark review, chapter coverage, 100 model papers per track and 2000 knowledge points per track remain incomplete.',file=sys.stderr);sys.exit(1)
if __name__=='__main__':build()
