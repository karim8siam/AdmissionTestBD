"""Published counts/sets/provenance plus independent numerical checks."""
import collections,hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
from engineering_questions import application
ROOT=Path(__file__).parent
m=json.loads((ROOT/'data/engineering_practice.json').read_text())
assert m['tracks']==['buet','ckruet']
entries=0;unique=set();track_counts=collections.Counter()
for b in m['books']:
 assert b['subject'] in ['HigherMath','Physics','Chemistry','Mixed']
 track=b['tracks'][0]
 for c in b['chapters']:
  path=ROOT/c['questions_url'][1:];raw=path.read_bytes();p=json.loads(raw)
  assert raw==(ROOT/'public'/c['questions_url'][1:]).read_bytes()
  assert hashlib.sha256(raw).hexdigest()[:12] in path.name
  assert p['id']==c['id']
  target=300 if b['subject']=='Chemistry' else 100
  assert len(p['questions'])==c['question_count']==target
  ids={q['id'] for q in p['questions']};assert len(ids)==target
  assert len({q['question_bn'] for q in p['questions']})==target
  setids=[]
  for s in p['sets']:
   assert len(s['question_ids'])==s['question_count']==100
   assert s['minutes']>0
   setids+=s['question_ids']
  assert len(setids)==len(set(setids))==target and set(setids)==ids
  for q in p['questions']:
   assert q['subject'] in ['HigherMath','Physics','Chemistry']
   assert len(q['options'])==len(set(q['options']))==4
   assert type(q['correct_index']) is int and 0<=q['correct_index']<4
   assert q['explanation'] and q['origin']=='original_practice'
   assert q['review_status']!='teacher_reviewed'
  if b['kind']=='mixed':
   assert collections.Counter(q['subject'] for q in p['questions'])=={'HigherMath':34,'Physics':33,'Chemistry':33}
  else:
   track_counts[track]+=target;entries+=target;unique|=ids
 assert b['available_questions']==sum(c['question_count'] for c in b['chapters'])
assert track_counts=={'buet':7100,'ckruet':7100}
assert entries==14200 and len(unique)==m['coverage']['unique_questions']==11920
# Independent matrix operations, finite differences, quadrature, inequalities and circuit laws.
for k in [2,3,4,7,19,31,42,61,91]:
 checks=[
  ('math-1-01',0,F(4,k*3-2)),
  ('math-1-02',0,((k* -k)-(2*2))**2),
  ('math-1-03',0,F(abs(k*(k+2)-2*(k+2)-3*k),2)),
  ('math-1-05',1,math.comb(k+1,2)*math.factorial(3)),
  ('math-1-07',0,F(1-k*k,1+k*k)),
  ('math-2-03',0,(complex(k,1)/complex(k,-1)).imag),
  ('math-2-04',0,k*(k*k-2)-k),
  ('math-2-05',0,math.comb(k+3,2)-2*(k+3)+1),
  ('math-2-09',1,abs(-4*k-0)+abs(0-(-4*k))),
  ('math-2-10',0,F(math.comb(k,2),math.comb(k+3,2))),
  ('physics-1-03',0,((2*k)+0)/2*((2*k)/2)),
  ('physics-1-04',0,(k*6+2*k*0)/(3*k)),
  ('physics-1-05',1,(20*k)*(.2**2)/k),
  ('physics-1-07',0,40*k/(2e-6*2e11)*1000),
  ('physics-2-01',0,10*(k+400)*(1-(k+200)/(k+400))),
  ('physics-2-02',1,1/(1/k-1/(3*k))),
  ('physics-2-03',0,1/(1/(2*k)+1/k)),
  ('physics-2-04',0,(k+10)-2*(k+10)/5),
  ('physics-2-06',0,(k+10)*.02*abs(.1-.5)/.2),
  ('physics-2-07',0,500e-9/(4/3)*k/(.5e-3)*1000),
  ('physics-2-10',1,((k+1.7-.7)/1000)**2*1000*1000),
  ('chemistry-1-02',0,-13.6*k*k/4),
  ('chemistry-1-05',1,(100*k)/1000*200),
  ('chemistry-2-01',0,k*.082*300/2),
  ('chemistry-2-03',0,k*.2/(.1*2)),
  ('chemistry-2-03',1,(k/40)/.25),
  ('chemistry-2-04',1,k/2),
 ]
 for cid,mode,expected in checks:
  _,answer,_=application(cid,k,mode)
  assert math.isclose(float(answer),float(expected),rel_tol=1e-10,abs_tol=1e-9),(cid,k,mode,answer,expected)
 # midpoint integration is independent of the closed-form expressions.
 N=5000
 integral=sum(((i+.5)/N)*(1-(i+.5)/N)**k/N for i in range(N))
 assert math.isclose(float(application('math-1-10',k,0)[1]),integral,rel_tol=2e-5)
 h=.0001
 f=lambda x:x**k*math.exp(-x)
 ratio=(f(k+h)-2*f(k)+f(k-h))/(h*h*f(k))
 assert math.isclose(float(application('math-1-09',k,0)[1]),ratio,rel_tol=.02,abs_tol=2e-4)
 # Evaluate linear-programming corners rather than assuming a maximum formula.
 corners=[(0,0),(0,k),((k+2)/2,0),(2,k-2)]
 assert float(application('math-2-02',k,0)[1])==max(3*x+2*y for x,y in corners)
# Mirrors cannot quietly drift.
for filename in ['index.html','assets/engineering-practice.js','assets/engineering-practice.css']:
 assert (ROOT/filename).read_bytes()==(ROOT/'public'/filename).read_bytes()==(ROOT/'web'/filename).read_bytes()
print('PASS: 14,200 chapter entries / 11,920 distinct questions; exact 100-question sets; disjoint Chemistry sets; mixed PCM distribution; independent formula checks; mirrors.')
