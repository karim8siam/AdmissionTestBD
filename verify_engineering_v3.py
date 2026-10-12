"""Structural release gate and independent numerical checks, not teacher certification."""
import collections,hashlib,json,math,copy
from pathlib import Path
from fractions import Fraction
import numpy as np
from engineering_v2 import mathematics,physics,chemistry,challenges,physics_challenges
from engineering_v2.core import REGISTRY
from engineering_v2.review import review_question,review_paper
ROOT=Path(__file__).parent
m=json.loads((ROOT/'data/engineering_practice.json').read_text())
counts=collections.Counter();methods=set();core=set();papers=[]
for b in m['books']+m['model_books']:
 for c in b['chapters']:
  path=ROOT/c['questions_url'][1:];raw=path.read_bytes();p=json.loads(raw)
  assert raw==(ROOT/'public'/c['questions_url'][1:]).read_bytes()
  assert hashlib.sha256(raw).hexdigest()[:12] in path.name
  assert p['id']==c['id'] and len(p['questions'])==c['question_count']
  ids={q['id'] for q in p['questions']};assert len(ids)==len(p['questions'])
  assert len({q['question_bn'] for q in p['questions']})==len(ids)
  sets=[i for s in p['sets'] for i in s['question_ids']]
  assert len(sets)==len(set(sets))==len(ids) and set(sets)==ids
  for s in p['sets']:assert len(s['question_ids'])==s['question_count'] and 0<s['question_count']<=100 and s['minutes']>0
  assert all(not review_question(q) for q in p['questions'])
  if b['kind']=='models':
   assert len(p['questions'])==100
   review_paper(p['questions'],b['tracks'][0]);papers.append(p['questions'])
  else:
   counts[b['tracks'][0]]+=len(ids);core|=ids;methods.update(q['family_id'] for q in p['questions'])
 assert b['available_questions']==sum(c['question_count'] for c in b['chapters'])
assert len(papers)==200 and len(core)==m['coverage']['distinct_questions_in_core']
assert len(methods)==m['coverage']['authored_methods']
assert all(count==m['coverage']['chapter_questions_per_track'] for count in counts.values())
# Reject altered questions and papers rather than merely exercising the happy path.
p=copy.deepcopy(papers[0]);p[1]['family_id']=p[0]['family_id']
try:review_paper(p,'buet');raise RuntimeError('Repeated methods accepted')
except AssertionError:pass
q=copy.deepcopy(papers[0][0]);q['options'][1]=q['options'][0];assert review_question(q)
fs={f['id']:f for rows in REGISTRY.values() for f in rows}
def right(fid,n):return fs[fid]['fn'](n)[1][0]
def numeric(x):return float(Fraction(str(x)))
checks=0
for n in [3,4,7,12,24,30]:
 independent={
 'math-1-01:inverse-of-linear-transform':(np.linalg.inv(2*np.array([[1,n],[0,1]])-np.eye(2))@np.array([[1,n],[0,1]]))[0,1],
 'math-1-01:matrix-polynomial-det':np.linalg.det(np.diag([1,n])@np.diag([1,n])+np.eye(2)),
 'math-1-02:orthogonal-cross-norm':np.dot(np.cross([math.sqrt(n),0,0],[1/math.sqrt(n),math.sqrt(n+1-1/n),0]),np.cross([math.sqrt(n),0,0],[1/math.sqrt(n),math.sqrt(n+1-1/n),0])),
 'math-1-05:bounded-stars-bars':sum(x+y+z==n and x<=1 for x in range(n+1) for y in range(n+1) for z in range(n+1)),
 'math-2-02:vertex-objective':max(3*x+2*y for x,y in [(0,0),(0,n),((n+2)/2,0),(2,n-2)]),
 'math-2-02:integer-knapsack':max(3*x+2*y for x in range(n+1) for y in range(2*n+2) if 2*x+y<=2*n+1),
 'math-2-04:root-cubes':sum(complex(r)**3 for r in np.roots([1,-n,2])).real,
 'math-2-10:without-replacement-exactly-one':sum(a//n!=b//n for a in range(2*n) for b in range(2*n) if a!=b)/(2*n*(2*n-1)),
 'math-2-10:variance-pair':np.var([0,n,2*n]),
 'physics-1-02:cross-vector-double':np.cross([n,1,0],np.cross([0,0,1],[n,1,0]))[2],
 'physics-1-04:pulley-tension':np.linalg.solve([[1,-n],[1,3*n]],[10*n,30*n])[0],
 'physics-1-05:spring-block-rough':(.5*100*n*.2**2)/(.2*n*10),
 'physics-1-05:variable-force-work':2*sum(2*(i+.5)*3/10000*3/10000 for i in range(10000))/n,
 'physics-2-03:cell-parallel-internal':n/(1+1/(1/2+1/2)),
 'physics-2-03:heater-temperature-energy':n*4200*10/(100**2/10),
 'physics-2-05:rlc-nonresonant-power':(5*n/abs(complex(3,5-1)))**2*3,
 'physics-2-05:motional-energy-balance':(2*.5*n/2)**2*2,
 'physics-2-07:three-polarisers':8*n/2*math.cos(math.pi/4)**4,
 'physics-2-09:bohr-wavelength-ratio':(1-1/4)/(1/4-1/9),
 'chemistry-2-03:back-titration':(4*n-n)/2,
 'chemistry-2-04:hydrogen-charge':n/2,
 'chemistry-2-05:iron-ore-purity':10*n*.8*(2*56/160),
 'chemistry-2-05:process-recovery':10*n*.8*.9,
 }
 for fid,expected in independent.items():
  answer=numeric(right(fid,n));assert math.isclose(answer,float(expected),rel_tol=1e-5,abs_tol=1e-7),(fid,n,answer,expected);checks+=1
 # Integrate without the authored algebraic solution.
 x=(np.arange(20000)+.5)*n/20000
 quadrature=np.sum(x*x/(x*x+(n-x)**2))*n/20000
 assert math.isclose(numeric(right('math-1-10:symmetry-split',n)),quadrature,rel_tol=1e-8);checks+=1
for filename in ['index.html','assets/engineering-practice.js','assets/engineering-practice.css','assets/engineering-chapters.js','assets/engineering-chapters.css','assets/chapter-practice.js']:
 assert (ROOT/filename).read_bytes()==(ROOT/'public'/filename).read_bytes()==(ROOT/'web'/filename).read_bytes(),filename
print(f'PASS: {len(papers)} papers, {len(core)} bank questions, {len(methods)} families; {checks} independent numerical cases (24 families); mirrors and rejection gates.')
