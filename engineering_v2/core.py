"""Explicit problem families. Distractors are authored, never padded with +/-1."""
import hashlib, random, math,re
from fractions import Fraction as F
REGISTRY={}
VOCAB=set('a an the and of to from at in on by for is are with without same different all each per as not only then but so where if after before through initial final total actual theoretical maximum minimum first second third half quarter sample mass volume speed temperature pressure frequency molecule electron reaction coefficient orbital current constant charge energy distance period normal molar limiting complete conversion yield positive negative equilibrium solution concentration hydrogen carbon oxygen nitrogen photon primary secondary tertiary dilution number fixed ideal small optical centre radius length parallel perpendicular combined relative conducting right left load turns density transfer proton product defect forward ground level frictionless phase average peak compound neutral closed formation acidic basic saturated unsaturated principal process carbonyl binding structure lone pair linear nonnegative integer binary independent theorem implies equivalent mechanical useful catalytic generally between growth decay potential displacement container working stated calibrated standard given measured absorbed remaining mixture field circle triangle ellipse hyperbola integral root roots sum difference unit vector force gravity surface two three four sphere cell gas light star planet formula factor ratio capacity alpha beta state model quantum probability conditional population discrete continuous constraint bound point ring bond bonds unpaired shell subshell atomic molecular isotope abundance metal oxide ion cation anion formal coordination ligand dipole angle domain range graph slope axis origin area chord tangent secant radius amplitude wavelength flux coil wire loop rod source listener wave coherent intensity beam support uniform rest moving accelerating acceleration kinetic internal external chemical thermal work power efficiency heat entropy enthalpy electrode reduction oxidation partial refractive index emission bridge capacitor resistor emf bank force strain stress spring elastic stored height horizontal vertical spread molarity ppm molality normality exposure transition current efficiency active extinction emission counting step cell constant input output test text body stop sign ideal constant centre density fraction degrees decomposition recovery purification food wet dry soap salt brine fat oil preservative rinse glass water alcohol ester acid base strong weak buffer indicator endpoint equivalence impurity inert redox solubility soluble insoluble crystal precipitate complex concentrated dilute low high recycle consumption consumed unreacted stoichiometric additive series serial sequential complete graphite return above below exactly upright empirical limiting hypothetical methanol ethanol methane ethane ethene ethyne propane propene propanol aldehyde ketone alkane alkene alkyne one two three acyclic mono carbon metal copper silver sodium calcium potassium iron zinc electron nuclei nuclear photon rate light intensity main scale terminal time moment dipole flux optical path route adiabatic isothermal isobaric isochoric frictionless diameter spherical same level closed open loop laser helium count line linear absorb transmits transmit appears means clearly quantify cross dot outer inner valid invalid geometry shape cation ligand complex oxygen sulfur hydrogen metal radius relevant comparable comparison larger smaller decrease increase increases decreases equivalent coefficient twice single pass cold hot mild room temperature straight chain unsaturation reaction electron lone pair shell charge centre corresponding unit mol litre mole amount celsius kelvin power mechanical ground top bottom mass per nucleus shell valence solid hydrolysis saponification complete original from into before after negligible micro milli nano finite infinite relation ratio percent percentage theoretical actual reverse mixed conserved accepted molar bond electron transfer gas current normal related simple initial final generated measured observer radiating proper net pressure rotational vibrational frozen emitted relative accelerating supports entire identical saturated isotope simultaneous unchanged atmospheric clockwise static dynamic stable faster weaker stronger basicity formal neutralisation ideal maximum variable unpolarised polariser analyser unpaired paired'.split())
VOCAB.update("velocity direction magnitude denominator derivative interval separation resultant harmonic extension electrons component fundamental endpoints absolute opposite resistance momentum addition determinant stationary numerator equality coefficients downward particle initially observed friction magnetic reactance dependent dissolve intercept projection argument function reciprocal enclosed feasible imaginary remainder substitute expansion parabola projectile circular dimension uncertainty stopping resonance rejected electric attraction magnification apparent multiply titration calibration moisture triglyceride polynomial identity reflection coordinate completing complement hypotenuse requires intersection symmetry rectangle symmetric boundary conjugate equation binomial exponent components elevator threshold conservation compression reversible proportional delivered sensitive cyclotron currents converging critical position transitions polarity approximation volumetric protocol desiccator orbitals arrangement intermolecular character products carboxylate molecules thiosulfate microbial available conditions depletion hydrocarbon substitution eigenvalue eigenvalues arithmetic orthogonal adjacent permutation committee shortest integers solutions semiperimeter composition implicit definition inequality resource quadrant possible discriminant differentiate directrix eccentricity nondegenerate complementary distinct contains weightless defective variance multiplier divisions displayed triangular distances inertial nonrelativistic gradient satellite quasistatic material effective submerged pendulum translational monatomic convention isolated dielectric connected inversely solenoid repulsion inverted deviation adjustment corresponds individual intensities saturation blackbody activity activities transistor collector operation parallax arcsecond luminosity redshift exothermic distilled meniscus chloride chlorine immediate estimate dissolution hydroxide distribution absorption antibonding trigonal bipyramidal equatorial tetrahedral alkaline statement monoprotic reactant catalyst pressures hydrogenate balanced iodometry synthetic specified emulsifier hydrophobic nonpolar pollutant hardness correction dissolved destruction produced skeleton cleavage carbocation mechanism nucleophile nitration electrophilic delocalised primarily singular invertible adjugate idempotent characteristic multiplying coordinates foot even intercepts centred tangents combination people neither person separate either double counts committees containing both rule branch coalesces viable angles cauchy composite differentiable continuity logarithmic sensitivity evaluation returns optimum lowers objective mixing pure poles principal attain attainable reversed assumes assumed tension heavier rebounds detaches unstretched uncharged preserves hears reflects receiver reflected wall frame flight throw delayed drop released elapsed released half lives travelled tritium corresponds exactly sloping photon intermediate towards away acoustic proper emitted absorbs beta alpha gamma carry doubles triples decreases increases raises falls turns larger smaller transport indicated negligible negligible dissociation ionisation titrant titrated theoretical endpoint equivalence cell Faraday Faradays ion ions molar molarity molality Faraday efficiencies regulated series n p x y z a b c d e f g h i j k l m o r s t u v w q gives gives need needed already not at has have had required because cancelling cancel cancels needs difference ratio squared square possible zero twice produced molecule molecular series sum solved expected opposite unchanged supplied signed real image object behind before toward less more inside outside after before against next last initially selected determined cannot determine assume accounted accounts standard not dissociates dilute yield yields purity impure percent efficiency ideal obeys within light vacuum speed wavelength emitter base emitter emitter collector unstretched minimum maximum times units".replace('”','').split())
VOCAB={w.lower() for w in VOCAB if len(w)>1 or w in {"a","i"}}
VOCAB.update("block mass spring flight sin cos ln log tan area SHA SHM Atwood conservation transmits conditions count count doublecount doublecounts foreign value small clock end corresponding density spring constant fundamental released rest dropped implied named unchanged half-life any none numerator denominator setup detaches null confined total action only should needs must would also give allows allows wavelength hypothetical orbit wall atwood atom atoms reagent exothermic".replace("”", "").split())
def readable(s):
    s=str(s)
    def segment(m):
        word=m.group();low=word.lower()
        if low in VOCAB or len(word)<7:return word
        memo={len(word):[]}
        def split(i):
            if i in memo:return memo[i]
            for j in range(len(word),i,-1):
                if low[i:j] in VOCAB:
                    tail=split(j)
                    if tail is not None:memo[i]=[word[i:j]]+tail;return memo[i]
            memo[i]=None;return None
        parts=split(0)
        return ' '.join(parts) if parts else word
    s=re.sub(r"([a-z])([A-Z][a-z])",r"\1 \2",s)
    s=re.sub('[A-Za-z]+',segment,s)
    s=re.sub(r'([A-Za-z]{4,})(?=[0-9])',r'\1 ',s)
    s=re.sub(r'([0-9])(?=(?:kg|cm|mL|mol|hours|Hz|kPa|Pa|J|W|K|V|N/m|m/s)(?:[^A-Za-z]|$))',r'\1 ',s)
    s=re.sub(r'([\u0980-\u09ff])([A-Za-z0-9])',r'\1 \2',s)
    s=re.sub(r'([A-Za-z0-9])([\u0980-\u09ff])',r'\1 \2',s)
    return re.sub(' +',' ',s).strip()
def substitute_parameter(s,n):
    # Show a numerical working instead of an unexplained template variable.
    s=re.sub(r'(?<=\d)n(?=[^A-Za-z]|$)',f'×({n})',s)
    s=re.sub(r'(?<![A-Za-z])n(?=\()',f'({n})×',s)
    s=re.sub(r'(?<![A-Za-z])n(?=(?:ln|sin|cos|tan))',f'({n})×',s)
    s=re.sub(r'(?<![A-Za-z0-9])n(?![A-Za-z])',f'({n})',s)
    return s
def fmt(x):
    if isinstance(x,F): return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'
    if isinstance(x,float): return f'{x:.6g}'
    return str(x)
def Q(stem,answer,wrong,solution):
    return stem,[fmt(answer)]+[fmt(x) for x in wrong],solution
def add(cid,name,fn,difficulty='medium',kind='multi_step',steps=2):
    REGISTRY.setdefault(cid,[]).append(dict(id=cid+':'+name,fn=fn,difficulty=difficulty,kind=kind,steps=steps))
def fixed(cid,name,stem,answer,wrong,solution,difficulty='medium',kind='conceptual'):
    add(cid,name,lambda n:Q(stem,answer,wrong,solution),difficulty,kind)
def question(f,k,chapter):
    try: stem,options,solution=f['fn'](k+3)
    except (ZeroDivisionError,ValueError):return None
    if len(options)!=4 or len(set(options))!=4: return None
    dynamic=f['fn'](k+4)[0]!=stem
    if dynamic:solution=f'এই সমাধানে n = {k+3}। '+substitute_parameter(solution,k+3)
    stem,options,solution=readable(stem),[readable(x) for x in options],readable(solution)
    if not stem or len(solution)<35:raise ValueError(f['id']+' explanation')
    # Preserve the authored right option while independently randomising positions.
    answer=options[0]; rng=random.Random(f['id']+stem);rng.shuffle(options)
    return dict(id='eng3-'+hashlib.sha256((f['id']+stem).encode()).hexdigest()[:18],question_bn=stem,options=options,correct_index=options.index(answer),explanation=solution,
      family_id=f['id'],chapter_id=chapter['id'],chapter_title=chapter['title'],difficulty=f['difficulty'],question_type=f['kind'],reasoning_steps=f['steps'],origin='original_authored_practice',review_status='automated_checks_not_teacher_reviewed',book_reference=chapter['title']+' · HSC PCM পাঠ্যক্রম',variant=k)
def pool(chapter,target,offset=0):
    families=REGISTRY[chapter['id']];items=[];seen=set(); counts={}
    # Round robin means no family dominates a chapter set. Constant conceptual
    # questions appear once; parameterised problems supply additional practice.
    for k in range(offset,offset+35):
        for f in families:
            q=question(f,k,chapter)
            if not q or q['question_bn'] in seen:continue
            # Limit a method to 10% of a 300-question chemistry bank, 12% of
            # a 100-question bank. Never fill a short chapter with more clones.
            limit=30 if target==300 else 12
            if chapter['id']=='chemistry-1-01':limit=1
            if counts.get(f['id'],0)>=limit:continue
            seen.add(q['question_bn']);items.append(q);counts[f['id']]=counts.get(f['id'],0)+1
            if len(items)==target:return items
    return items
