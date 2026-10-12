import json,re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).parent
d=json.loads((ROOT/'data/varsity_expansion.json').read_text())
html=(ROOT/'index.html').read_text()
js=(ROOT/'assets/varsity-expansion.js').read_text()

assert d['version']=='2026-10-12.1'
assert set(d['coverage'])=={'humanities','business'}
assert len(d['questions'])==120
assert d['coverage']['humanities']['questions']==60
assert d['coverage']['business']['questions']==110
assert not d['model_papers']
assert all(c['model_tests']==0 and c['verified_complete_past_papers']==0 and not c['complete'] for c in d['coverage'].values())

ids=[q['id'] for q in d['questions']]
texts=[re.sub(r'\s+',' ',q['question'].casefold()).strip() for q in d['questions']]
knowledge=[re.sub(r'\s+',' ',q['knowledge'].casefold()).strip() for q in d['questions']]
assert len(set(ids))==len(ids)
assert len(set(texts))==len(texts)
assert len(set(knowledge))==len(knowledge)
assert all(len(q['options'])==len(set(q['options']))==4 and 0<=q['correct_index']<4 for q in d['questions'])
assert all(q['provenance']=='original' and q['review']['status']=='author_checked' and not q['review']['teacher_review'] for q in d['questions'])
assert all(q['explanation'] and q['family'] and q['topic'] for q in d['questions'])

for track in ('humanities','business'):
    actual=[q for q in d['questions'] if track in q['tracks']]
    topics=[t for t in d['topics'] if track in t['tracks']]
    archive=[e for e in d['archive'] if e['track']==track]
    c=d['coverage'][track]
    assert len(actual)==c['questions']==c['knowledge_points']
    assert len(topics)==c['topics']
    assert len(archive)==c['archive_entries']
    assert all(t['target']==100 and len(t['question_ids'])<100 for t in topics)

assert len(d['books'])==31
assert sum(len(b['chapters']) for b in d['books'])==98
assert all(b['url'].startswith('https://www.ebookbou.edu.bd/') for b in d['books'])
assert all(not e['complete_verified'] and not e['answer_key_verified'] and e['imported_questions']==0 for e in d['archive'])
assert all(e['url'].startswith('https://') for e in d['archive'])

for marker in ('nav-btn-humanities','nav-btn-business','view-varsity-expansion','VarsityExpansion.open(stream, chapterTrack)','varsity-expansion.js?v=1'):
    assert marker in html,marker
for marker in ('প্রকাশিত: ${bn(papers.length)} / ১০০','verified_complete_past_papers','একটি প্রশ্ন সর্বোচ্চ পাঁচবার','স্বয়ংক্রিয় মূল্যায়ন'):
    assert marker in js,marker

for name in ('index.html','assets/chapter-practice.js','assets/varsity-expansion.js','assets/varsity-expansion.css','data/varsity_expansion.json'):
    root=(ROOT/name).read_bytes()
    assert root==(ROOT/'public'/name).read_bytes()==(ROOT/'web'/name).read_bytes(),name

print('PASS: 120 original author-checked questions, derived track counts, 31 reference links, 98 indexed units, honest zero model/past-paper counts, separate navigation, publication gate, and mirrors.')
