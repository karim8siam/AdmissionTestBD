"""Fail-closed editorial review rules; not a claim of independent teacher review."""
from collections import Counter
from fractions import Fraction
import re
BLOCKED={
 'chemistry-1-03:formal-charge': 'Unconstrained bond counts permit unphysical nitrogen valence',
 'chemistry-1-03:coordination-ligand-charge': 'Unconstrained complex charges permit unsupported oxidation states',
 'chemistry-1-03:bond-order-molecular-ion': 'Unspecified species and implausible bond orders',
 'chemistry-1-02:subshell-capacity': 'Unbounded hypothetical l is outside the intended HSC examples',
}
MODEL_EXCLUDED={
 'physics-2-10:logic-nand','physics-2-10:logic-de-morgan','physics-2-10:xor-parity','physics-2-10:binary-adder',
 'physics-1-01:significant-subtraction','physics-1-01:instrument-zero','physics-2-11:light-travel-time',
 'chemistry-2-03:empirical-composition','chemistry-2-04:electrolysis-time',
 'math-1-03:orthocentre','math-1-03:centroid-line','math-1-04:point-circle-position',
 'math-2-04:synthetic-value',
}
# Merge visibly equivalent methods even when their authoring IDs differ.
METHOD_ALIASES={
 'math-1-10:absolute-integral-polynomial':'math-1-10:area-crossing',
 'math-2-10:bayes-asymmetric':'math-2-10:bayes',
 'math-2-10:without-replacement-exactly-one':'math-2-10:hypergeometric',
 'physics-2-11:star-distance-luminosity-inference':'physics-2-11:luminosity-flux',
 'physics-2-09:two-stage-decay-account':'physics-2-09:decay-fraction',
}
def method_id(q):return METHOD_ALIASES.get(q['family_id'],q['family_id'])
def review_question(q):
    issues=[]
    if q['family_id'] in BLOCKED:issues.append(BLOCKED[q['family_id']])
    if len(q['options'])!=4 or len(set(q['options']))!=4:issues.append('Options not four distinct choices')
    if not 0<=q['correct_index']<4:issues.append('Answer index invalid')
    if len(q['explanation'])<35:issues.append('Explanation insufficient')
    if any(x in q['question_bn'] for x in ['case label','caselabel','sample mass','multiplesof','coefficients×']):issues.append('Irrelevant filler parameter')
    if q['family_id'].startswith('math-2-10:'):
        for option in q['options']:
            try:
                f=Fraction(option)
                if 'probability' in q['question_bn'].lower() or 'probability' in q['family_id']:
                    if not 0<=f<=1:issues.append('Probability choice outside 0..1')
            except ValueError:pass
    return issues
def model_eligible(q):
    if review_question(q):return False
    if q['family_id'] in MODEL_EXCLUDED:return False
    if q['chapter_id']=='chemistry-1-01':return False
    return True
def review_paper(questions,track):
    assert len(questions)==100
    assert len({q['id'] for q in questions})==100
    assert len({method_id(q) for q in questions})==100,'Repeated method in a model paper'
    assert len({q['question_bn'] for q in questions})==100
    subjects=Counter(q['subject'] for q in questions)
    assert subjects=={'HigherMath':34,'Physics':33,'Chemistry':33},subjects
    for subject,min_chapters in [('HigherMath',14),('Physics',14),('Chemistry',7)]:
        assert len({q['chapter_id'] for q in questions if q['subject']==subject})>=min_chapters
    assert max(Counter(q['chapter_id'] for q in questions).values())<=6
    difficult=Counter(q['difficulty'] for q in questions)
    assert difficult['hard']>= (40 if track=='buet' else 30),difficult
    assert sum(q['question_type'] in ['conceptual','classification'] for q in questions)<=25
    assert all(model_eligible(q) for q in questions)
    return {'passed':True,'method_count':100,'chapters':len({q['chapter_id'] for q in questions}),'difficulty':dict(difficult),'subjects':dict(subjects)}
