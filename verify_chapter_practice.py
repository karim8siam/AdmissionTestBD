"""Verify the published chapter bank without relying on UI counts."""
import collections
import hashlib
import json
import math
from pathlib import Path
from fractions import Fraction
import original_practice as original

ROOT = Path(__file__).parent
manifest = json.loads((ROOT / 'data/chapter_practice.json').read_text())
counts = collections.Counter()
all_ids = set()
for book in manifest['books']:
    for chapter in book['chapters']:
        path = ROOT / chapter['questions_url'].lstrip('/')
        raw = path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()[:12] in path.name
        assert raw == (ROOT/'public'/chapter['questions_url'].lstrip('/')).read_bytes()
        payload = json.loads(raw)
        target = 300 if book['subject'] == 'Chemistry' else 100
        assert payload['id'] == chapter['id']
        assert len(payload['questions']) == chapter['question_count'] == target
        ids = {q['id'] for q in payload['questions']}
        assert len(ids) == target and not ids & all_ids
        all_ids.update(ids)
        assert len({original.hashlib.sha256(q['question_bn'].strip().encode()).hexdigest() for q in payload['questions']}) == target
        set_ids = []
        assert len(payload['sets']) == (3 if target == 300 else 1)
        for question_set in payload['sets']:
            assert len(question_set['question_ids']) == 100
            set_ids += question_set['question_ids']
        assert len(set_ids) == len(set(set_ids)) == target and set(set_ids) == ids
        for q in payload['questions']:
            assert len(q['options']) == 4 and all(isinstance(o,str) and o.strip() for o in q['options'])
            assert type(q['correct_index']) is int and 0 <= q['correct_index'] < 4
            if q.get('origin') == 'original_practice':
                assert q['explanation'] and q['concept_ids'] and 'উদ্ধৃতি নয়' in q['book_reference']
                assert len(set(q['options'])) == 4
                counts[q['question_type']] += 1
        counts['questions'] += target
        counts['chapters'] += 1
        counts['existing'] += chapter['existing_questions']
        counts['original'] += chapter['original_questions']
    assert book['available_questions'] == sum(c['question_count'] for c in book['chapters'])
assert counts['questions'] == 12700 and counts['chapters'] == 107
assert counts['original'] == manifest['audit']['original_questions_added']
assert (ROOT/'data/chapter_practice.json').read_bytes() == (ROOT/'public/data/chapter_practice.json').read_bytes()
# Independently evaluate representative formula families across all parameter cases.
for k in range(2,27):
    cases = [
        ('physics-1-02',0,math.hypot(3*k,4*k)),
        ('physics-1-03',1,sum(k*(i+.5) for i in range(4))),
        ('physics-1-05',1,(2*k)*3**2/2),
        ('physics-2-01',0,10*k-3*k),
        ('physics-2-05',0,k*6/2),
        ('physics-2-06',0,3/(Fraction(k+1,k))),
        ('physics-2-09',2,Fraction(-68,5)/k**2),
        ('physics-2-10',2,(k+1.7-.7)),
    ]
    for cid,mode,expected in cases:
        q,answer,_ = original.physics(cid,k,mode)
        assert math.isclose(float(answer),float(expected),rel_tol=1e-10,abs_tol=1e-10),(cid,q,answer,expected)
    cases = [
        ('math-1-01',0,k*4-2*3),
        ('math-1-05',0,math.comb(k+2,2)),
        ('math-1-09',1,((k*(2.000001)**2+3*2.000001)-(k*(1.999999)**2+3*1.999999))/0.000002),
        ('math-1-10',0,sum(k*(i+.5)/10000**2 for i in range(10000))),
        ('math-2-02',0,max(2*x+3*y for x,y in [(0,0),(k,0),(0,k)])),
        ('math-2-06',2,math.sqrt((5*k)**2-(4*k)**2)),
        ('math-2-07',2,sum(1 for n in range(2*k) if 0<=(2*n+1)/2<=k)),
        ('math-2-10',2,Fraction(k,k+2)),
    ]
    for cid,mode,expected in cases:
        q,answer,_ = original.higher_math(cid,k,mode)
        assert math.isclose(float(answer),float(expected),rel_tol=1e-6,abs_tol=1e-6),(cid,q,answer,expected)
# Concept generation must use every unordered pair at most once; truth keys must agree.
facts=original.read_facts()
for cid,rows in facts.items():
    target=300 if cid.startswith('chemistry') else 100
    questions=original.conceptual(cid,rows,target)
    pairs=[tuple(sorted(q['concept_ids'])) for q in questions]
    assert len(pairs)==len(set(pairs))
    balance=collections.Counter(q['options'][q['correct_index']] for q in questions)
    assert max(balance.values())-min(balance.values())<=1
print(json.dumps(dict(counts),indent=2))
print('Coverage, disjoint chemistry sets, original provenance, formula checks and mirrored assets passed.')
