# Engineering editorial revision

The active release contains separate chapter practice and 100 model papers for each of BUET preliminary-style practice and custom CKRUET PCM practice. Biology is excluded. These are original practice questions, not an authenticated past-paper bank.

## Evidence scope

Selected pages of BUET 2021–22, 2022–23 and 2023–24 compilations, and selected CKRUET 2023–24 compilation pages, were visually inspected. The existing 100-item BUET 2024 chapter-tag sample is retained in content/engineering/buet_2024_sample_tags.json. This does not establish ten-year frequency weights or independently verify compiled answer keys. Full textbook editions were not read; chapter organisation follows the existing HSC catalogue, with historical recommended-book candidates documented in sources.json.

## Changes motivated by the review

- Mathematical practice now includes matrix identities, geometric constraints, domains, inverse functions, piecewise behaviour, optimisation, integration, and conditional sampling instead of a small family of arithmetic substitutions.
- Physics includes motion graphs, vector frames, energy constraints, circuit loading, internal resistance, wave path changes, and conservation reasoning.
- Chemistry includes reaction and structure reasoning, limiting reagents, equilibrium, titration, electrolysis, and industrial mass balances. Statement-pair permutations are not used to fill counts.
- Four draft chemistry families were blocked for unconstrained or physically unsupported parameter ranges. Ambiguous pressure and spring-detachment assumptions were corrected.
- Some equivalent authoring families are grouped in the paper review gate. Each model paper contains 100 different reviewed family groups. This is a rule-based diversity constraint, not proof that every learning objective is different.

## Release gates

Every paper has 34 Mathematics, 33 Physics and 33 Chemistry questions, at least 14/14/7 chapters respectively, and at most six questions from one chapter. Exactly repeated questions are capped at five appearances across a track's 100 papers. There are 40 BUET or 30 CKRUET questions labelled hard, but difficulty is an editorial estimate and has not been calibrated against student performance.

verify_engineering_v3.py validates payloads, answer indices, option uniqueness, set coverage, mirrors, and fail-closed review rules. It also checks 144 independent numerical cases from 24 selected families using matrix operations, enumeration, quadrature, energy and circuit equations, and stoichiometry. It does not independently certify the other families. verify_engineering_ui.cjs exercises sequential access, grading, saved attempts, navigation guards, and unrestricted chapter sets. Medical/Varsity's existing chapter audit passes unchanged.

## Outstanding content work

The core bank has 6,549 question stems across 710 authoring families; it includes numerical variants and is shared between tracks. All Mathematics and Physics chapters have 100 questions. Chemistry chapter availability is 22 for laboratory safety, 280 for qualitative chemistry, and 47 for periodic properties and bonding; each other chemistry chapter has 300. These shortfalls are shown in the interface. Independent subject-teacher review, calibrated difficulty, and a complete authenticated past-paper comparison remain unfinished. Automated checks must not be presented as teacher certification.
