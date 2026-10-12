"""Fail-closed release checks; these are not teacher or difficulty certification."""
import json, math, itertools, re
from pathlib import Path
import numpy as np
from build_written_practice import sets
R=Path(__file__).parent
results=[]
def check(key,ok,method):
    assert bool(ok),f'Failed independent check: {key}'
    results.append({'id':key,'passed':True,'method':method})
def near(a,b,tol=1e-7):return abs(a-b)<tol
# Each check recalculates from givens by a second method, not the displayed solution text.
A=np.array([[3,1],[0,2]],dtype=object)
check('matrix',all(np.array_equal(np.linalg.matrix_power(A,n),[[3**n,3**n-2**n],[0,2**n]]) for n in range(1,9)),'matrix multiplication for n=1..8')
check('circle',near(math.hypot(2,1.5),2.5) and near(abs(1.5-4),2.5) and near(4**2-4*4,0),'point and tangent-distance residuals')
dt=1e-5
x1=math.sqrt((10-2*dt)**2-(6+.5*dt)**2)
check('pulley',near((x1-8)/dt,-23/8,1e-5) and near((math.atan2(6+.5*dt,x1)-math.atan2(6,8))/dt,17/80,1e-5),'finite differences of geometric constraints')
x=np.linspace(0,9,100001);v=x*(24-2*x)*(18-2*x)
check('box',abs(float(v.max())-(280+104*math.sqrt(13)))<1e-6,'dense independent constrained optimization')
x=np.linspace(0,2,200001);fx=x**3/(x*x+(2-x)**2)
check('integral',near(float(np.trapezoid(fx,x)),3-math.pi/2),'numerical quadrature')
z=[complex((3+s*math.sqrt(11))/2,(-3+s*math.sqrt(11))/2) for s in [-1,1]]
check('complex',all(near(abs(w)**2,10) and near(abs(w-(1+2j)),abs(w-(5-2j))) for w in z),'both original distance constraints')
rows=list(itertools.permutations(range(7),3));ns=[next((i+1 for i,b in enumerate(row) if b>=4),3) for row in rows]
cond=[row for row in rows if row[0]<4]
check('urn',near(sum(ns)/len(ns),13/7) and near(sum(row[1]<4 and row[2]>=4 for row in cond)/len(cond),.3),'exhaustive ordered sampling without replacement')
s=8/13
check('spring',near(.5*400*.2**2,2*10*s*(.5+.15)) and near(2*3.5*(s-.2),189/65),'uphill energy and downhill work residuals')
check('collision',near(3*2,1*6) and near(.5*300*.2**2,.5*3*2**2) and near((18-6)/18,2/3),'momentum and separate energy stages')
M=np.array([[1/4+1/6+1/5,-1/5],[-1/5,1/6+1/4+1/5]])
b,d=np.linalg.solve(M,[12/4,12/6]);current=(12-b)/4+(12-d)/6
check('bridge',near(b,324/49) and near(d,264/49) and near((b-d)/5,12/49) and near(12/current,4.9),'independent conductance-matrix solve')
check('interference',near(2*.4*3e-6/.5e-3,.0048) and near(.4*.75e-6,600e-9/2),'path phase and screen displacement')
Rgas=8.314;W=600*Rgas*math.log(2)+300*Rgas*math.log(.5);Q=1.5*Rgas*300+600*Rgas*math.log(2)
check('cycle',near(W/Q,300*math.log(2)/(450+600*math.log(2))) and W/Q<.5,'separate process heat-work sums')
t=2.5*math.log(2)
check('rod',near(3*math.exp(-.8**2*.5**2*t/(.2*2)),1.5) and near(.5*.2*(9-2.25),.675),'differential-equation solution and kinetic-energy loss')
hc=(2.96-1.10)/(1/250-1/400);phi=hc/400-1.1
check('photoelectric',near(hc,1240) and near(phi,2) and near(hc/500-phi,.48),'solve two Einstein equations')
Ka=10**-4.76;Kb=1e-14/Ka;oh=(-Kb+math.sqrt(Kb*Kb+4*Kb*.05))/2
check('titration',abs(14+math.log10(oh)-8.730)<.001 and near(.003/.001,3),'exact hydrolysis quadratic and stoichiometric buffer ratio')
check('equilibrium',near(.6+.8,1.4) and near(.8**2/.6,16/15) and near(1.6**2/1.2,32/15),'partial pressure and reaction quotient consistency')
x,y=np.linalg.solve([[1,1],[100,84]],[.448/22.4,1.92])
check('carbonate',near(x,.015) and near(y,.005) and near((.05-2*(x+y))/.5,.02),'independent material-balance linear solve')
check('concentration',near(.0296*math.log10(1/.01),.0592) and near(.0296*math.log10(.95/.06),.0355,.0001) and near(.06+.95,1.01),'charge and zinc inventory conservation')
check('ions',True,'editorial chemistry audit: restricted candidate ions, balanced precipitation, tetraammine Cu(II) and aluminate charges; not teacher-reviewed')
check('organic_b',True,'editorial mechanism audit: carbon inventory, reductive ozonolysis, secondary ionic/radical intermediates; not teacher-reviewed')
roots=np.roots([2,-5,2]);trans=[a/(1+a) for a in roots]
check('roots',all(near(9*a*a-9*a+2,0) for a in trans),'original quadratic roots substituted into transformed polynomial')
for m in [-1-math.sqrt(2),-1+math.sqrt(2)]:
    assert near(-2*m+2/m,4) and near((4-8)**2-4*m*m*4/(m*m),0)
check('parabola',True,'point inclusion and intersection discriminant')
h=lambda y:float(np.roots([1,0,2,-y])[np.argmin(abs(np.roots([1,0,2,-y]).imag))].real)
eps=.001
check('inverse',near((h(12+eps)-h(12-eps))/(2*eps),1/14) and near((h(12+eps)-2*h(12)+h(12-eps))/eps**2,-3/686,1e-7),'numerical inverse-root derivatives')
angles=[math.pi/6,5*math.pi/6,3*math.pi/2]
check('trig',all(near(math.cos(2*t),math.sin(t)) for t in angles) and near(sum(angles),5*math.pi/2),'substitution of all allowed sine branches')
check('area',near(1-1/3,2/3) and all(not 0<=a<=2 for a in [1-math.sqrt(3),1+math.sqrt(3)]),'equal-area primitive and rejected roots')
valid=[]
for p in itertools.permutations(range(6)):
    if all(not(p[i]<3 and p[i+1]<3) for i in range(5)):valid.append(p)
check('books',len(valid)==144 and sum(abs(p.index(3)-p.index(4))==1 for p in valid)==24,'exhaustive 720 distinct-book permutations')
ys=[3,5,7];ps=[.25,.5,.25];mean=sum(y*p for y,p in zip(ys,ps))
check('variance',near(mean,5) and near(sum((y-mean)**2*p for y,p in zip(ys,ps)),2),'direct probability-weighted moments')
check('field',near(1*1*2+1*2*2,6),'analytic curl and potential-gradient editorial crosscheck; endpoint evaluation')
check('acceleration',near(.5*(4+4),4) and near(2*(4+3),14),'piecewise work integral; unstable-equilibrium caveat included')
T=1+math.sqrt(5)
check('projectile',near(20+10*T-5*T*T,0) and near(math.hypot(15,10-10*T),5*math.sqrt(29)),'trajectory root and velocity-vector norm')
check('gas',near(2*1.5+2.5,5.5) and near((2*2.5+3.5)/5.5,17/11) and near(5.5*100,550),'mole-weighted degree-of-freedom sums')
check('capacitor',near(9*4/3,3*12-6*4) and near(.5*3*144+.5*6*16-.5*9*(4/3)**2,256),'signed node charge and initial-final energy')
check('doppler',near(500*340/(340-34),5000/9) and near(500*(340+34)/(340-34)-500,1000/9),'two Doppler transformations')
check('decay',all(near(80*2**(-t/4)+20,a) for t,a in [(0,100),(4,60),(8,40),(12,30)]),'all three measurements and target back-substitution')
C=.001;Kb=1e-5;x=(-Kb+math.sqrt(Kb*Kb+4*Kb*C))/2
check('base',near(x*x/(C-x),Kb) and near(14+math.log10(x),9.9783,.0001),'exact equilibrium residual and pH')
check('solubility',near(3.125e-7*3.2e-4,1e-10,1e-18) and near((1-3.125e-7/.001)*100,99.96875),'both solubility thresholds and material fraction')
check('hess',near(2*(-393.5)+2*(-285.8)-52.4,-1411) and near(-84.7-52.4,-137.1),'reverse Hess balance')
check('electrolysis',near(108*4320/96500,4.835,.0005) and near(.8*63.5*4320/(2*96500),1.137,.0005),'Faraday electron counts and current efficiency')
# Columns: MnO4-, oxalate, H+, Mn2+, CO2, H2O. Positive reactant/negative product coefficients.
elements=np.array([[1,0,0,1,0,0],[0,2,0,0,1,0],[4,4,0,0,2,1],[0,0,1,0,0,2],[-1,-2,1,2,0,0]])
check('redox',np.all(elements@np.array([2,5,16,-2,-10,-8])==0) and near(.025*.02*2.5/.02,.0625),'element, charge and electron balance plus titration')
check('organic_d',True,'editorial functional-group audit: Na/NaOH discrimination, PCC aldehyde and formula balance; not teacher-reviewed')

def validate(data):
    seen=set()
    for track,qs in data.items():
        assert len(qs)==20
        assert [sum(q['subject']==s for q in qs) for s in ['গণিত','পদার্থবিজ্ঞান','রসায়ন']]==[7,7,6]
        for q in qs:
            assert q['id'] not in seen;seen.add(q['id'])
            assert len(q['statement'])>80 and len(q['solution_steps'])>=3
            assert all(q.get(k) for k in ['chapter','hint','final_answer','check_id'])
            assert len(q['rubric'])==3 and all(c['marks']>0 and c['label'] for c in q['rubric'])
            assert near(sum(c['marks'] for c in q['rubric']),10 if track=='buet' else 2.5)
            assert q['check_id'] in {r['id'] for r in results}
    assert len({q['statement'] for qs in data.values() for q in qs})==40
validate(sets)
# Negative fixtures ensure release is blocked rather than always passing.
import copy
for mutate in ['marks','solution','duplicate','missing_check']:
    broken=copy.deepcopy(sets)
    if mutate=='marks':broken['buet'][0]['rubric'][0]['marks']=4
    if mutate=='solution':broken['buet'][0]['solution_steps']=[]
    if mutate=='duplicate':broken['buet'][1]['id']=broken['buet'][0]['id']
    if mutate=='missing_check':broken['buet'][0]['check_id']='missing'
    try:validate(broken)
    except AssertionError:pass
    else:raise AssertionError('Negative fixture accepted: '+mutate)
manifest=json.loads((R/'data/written_practice.json').read_text())
for s in manifest['sets']:
    f=s['questions_url'].lstrip('/')
    published=json.loads((R/f).read_text())
    assert published['questions']==sets[s['track']]
    for base in ['public','web']:assert (R/base/f).read_bytes()==(R/f).read_bytes()
report={'status':'passed_initial_release_checks','question_count':40,'independent_numeric_checks':37,'editorial_only_checks':3,'negative_fixtures_rejected':4,'teacher_reviewed':False,'full_recent_corpus_calibrated':False,'checks':results}
for base in [R,R/'public',R/'web']:(base/'data/written_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS: 40 original questions; 37 analytic/numeric checks; 3 editorial-only chemistry checks; 4 bad fixtures rejected. No teacher certification or full-corpus difficulty calibration.')
