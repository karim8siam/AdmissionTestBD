# Engineering practice: research and implementation plan

**Implementation update:** The plan below is the research snapshot. Engineering practice is now implemented for deployment: 51 PCM chapters per track, 7,100 chapter entries per track, 11,920 distinct question stems across the two tracks, and one 100-question mixed set per track. Chemistry shares a concept core; mixed sets reuse chapter questions. Original numerical variants share problem families. No authenticated ten-year bank or independent teacher verification is claimed. The original “not finished” paragraphs describe the earlier research stage. See ENGINEERING_COVERAGE.md for current coverage.

Research date: 11 October 2026. Scope: Higher Mathematics, Physics and Chemistry only.

## What is finished, and what is still missing

Finished: format research; a source audit; visual inspection of a readable BUET 2023–24 compilation covering numbered questions 1–100; selected earlier BUET pages and CKRUET textbook-match tables; a provisional six-book, 51-chapter catalogue and question-count blueprint.

Not finished: an authenticated ten-year paper collection, all shifts, a complete textbook reading, independently checked historical answers, original engineering questions, chapter tests, or website integration. No engineering question bank has been published. The existing live medical/varsity site is unchanged.

The machine-readable files in `content/engineering/` record this explicitly. A source being found does not mean its questions were verified or imported.

## Exam history changes the product

BUET introduced preliminary screening for academic session 2020–21. Earlier written questions must not be renamed preliminary MCQs. The inspected 2023–24 compilation contains 34 Mathematics, 33 Physics and 33 Chemistry questions, with a printed 60-minute duration and +1/−0.25 scoring.

The BUET-issued 2025–26 prospectus obtained from a third-party mirror specifies a written PCM Module A: 20 questions per subject, 600 marks and three hours. Its page 3 was visually inspected because PDF text extraction lost most Bengali text. The official admission endpoint timed out. This confirms that session's format; it does not establish the next 2026–27 format.

RUET's official 2023–24 combined prospectus specifies Mathematics 25/150 marks, Physics 25/150, Chemistry 25/150 and Functional English 25/50: 100 MCQs, 500 marks and 150 minutes. Wrong answers lose 25% of that question's marks. The English prospectus resolves a conflicting duration in the Bengali document. Removing English makes our requested 100-question PCM test a custom practice test, not a full official CKRUET mock.

RUET has a primary combined-admission notice for session 2020–21. A secondary article claiming the cluster started only in 2021–22 conflicts with that record. Secondary reporting says the combined system ended for 2024–25; the currently observed KUET admission site advertises its own 2026–27 MCQ examination. Neither observation establishes a current common CKRUET pattern.

**Product names:** “BUET preliminary: historical MCQ practice” and “CKRUET: historical PCM practice”. Display the relevant session and explain current-pattern uncertainty. Keep a separate future BUET written track in the design; do not quietly represent MCQs as written preparation.

## Archive coverage audit

Maintain academic session, actual examination date, shift/set and type separately. A ten-year engineering reference archive can include older separate CUET/KUET/RUET and BUET written exams, but these belong in a different archive category.

| Material | Evidence obtained | Remaining work |
|---|---|---|
| BUET before 2020–21 | Written-bank links found; not a preliminary history | Obtain and authenticate individual written papers; analyse separately |
| BUET 2020–21 | Introduction of preliminary format documented | Obtain every preliminary shift and check complete scans |
| BUET 2021–22 | Paper page located; one retrieval met a verification wall | Obtain readable complete shifts |
| BUET 2022–23 | Scan compilation downloaded; selected pages read | Complete all-item tagging; authenticate shifts and answers |
| BUET 2023–24 | 100 numbered compiled items visually read and provisionally tagged | Authenticate against original shifts; independently solve answers |
| BUET 2024–25 | Preliminary format references found | Obtain complete original shifts and solutions |
| BUET 2025–26 | Written format checked in university document on mirror | Obtain actual written paper; verify next session separately |
| CKRUET 2020–21 | Combined examination confirmed by official notice | Obtain actual paper, rules and answers |
| CKRUET 2021–22 / 2022–23 | Archive candidates exist; papers not authenticated | Obtain original papers and session-specific rules |
| CKRUET 2023–24 | Official rules obtained; selected textbook-match tables read | Obtain complete raw paper; check all PCM items independently |
| Subsequent separate CUET/KUET/RUET | Separate-test evidence found | Keep each institution/session distinct; do not label CKRUET |

No archive row above is a claim that all questions from that session have been analysed. Avoid a public “last ten years fully analysed” claim until the inventory supports it.

## Books to align with

AAP's 2021 engineering preparation plan explicitly recommends these authors. That is evidence of recommendations, not a measurement of what every student currently reads. Verify current editions and chapter ordering before quoting page numbers.

| Subject | Main reference candidate | Supplementary candidates |
|---|---|---|
| Physics, papers 1 and 2 | Ishaq | Shahjahan Tapan / Giasuddin |
| Chemistry, papers 1 and 2 | Hazari | Abu Salek / Guha |
| Higher Mathematics, papers 1 and 2 | Ketab Uddin | Rafiqul Islam |

The inspected CKRUET physics matching table names Shahjahan Rahman Selim and Zakaria Touhid. Keep these as additional reference candidates rather than silently treating them as the same author as Tapan.

AAP also lists Udvash and Aspect engineering question banks, engineering MCQ and BUET practice resources. Udvash's own site lists concept/practice books and BUET/CKRUET banks, but two accessed preview links failed. Full books have not been obtained or read. Do not label newly written questions as taken from these books without item-level evidence. Use original wording and solutions; do not republish an entire commercial bank.

## What the readable sample tells us

`buet_2024_sample_tags.json` gives provisional primary/secondary chapter tags for all 100 numbered items in one third-party compilation. It stores no copied question text or answer keys.

The mathematics sample includes transformed integrals, calculus of rational functions, conic properties and tangency, complex-number powers, common polynomial roots, inverse trigonometry, statics and projectile motion. Physics includes vector work, decay/fission, moving-source sound reasoning, diffraction, spring combinations, circuit reduction, Carnot calculations and collisions. Chemistry mixes organic reactions/isomerism, equilibrium, molecular structure, quantitative reactions, gas behaviour and electrochemistry.

These observations support application and multi-step practice. They do not establish ten-year chapter frequencies, calibrated difficulty or a prediction for an upcoming exam. Some questions combine chapters; single-chapter tags alone lose that information. Do not declare a chapter unimportant merely because it is absent from this sample.

Some online results are unsuitable for automatic ingestion. One “BUET MCQ” aggregator displayed 2017 written-style items without four answer choices. CKRUET tables are publisher/book matches rather than raw authenticated exam scans. Solution keys must be checked rather than accepted from votes or titles saying “100% correct”.

## Question bank size and structure

Interpret “100-question set” as 100 questions in each test. Initially prepare one mixed set for each track; the number of mixed tests can grow after the chapter bank is checked. Do not assume this request means 100 separate engineering model tests immediately.

Carry forward the existing requirement of three separate Chemistry sets per chapter. Each Chemistry paper has five chapters in the current project catalogue: ten across both papers.

| Subject | Papers | Chapters in project catalogue | Sets per chapter per track | Questions per track |
|---|---:|---:|---:|---:|
| Higher Mathematics | 2 | 20 | 1 × 100 | 2,000 |
| Physics | 2 | 21 | 1 × 100 | 2,100 |
| Chemistry | 2 | 10 | 3 × 100 | 3,000 |
| Total | 6 | 51 | — | 7,100 |

Two track-specific chapter allocations require 14,200 question entries. This is a content-production target, not a completed question count. If questions are shared between tracks, report the smaller unique-bank count honestly. Three Chemistry sets for the same chapter must be disjoint. Mixed-test reuse of chapter questions must also be disclosed; it does not create new questions.

BUET historical mixed practice can use the observed 34/33/33 and 60-minute template. CKRUET custom PCM practice may also use 34/33/33 for a 100-question product, but it must say that the distribution is custom. Its practice time and normalized +1/−0.25 scoring are product settings, not official marks. A 75-question PCM-only historical mode would preserve the official 25/25/25 subject counts; English remains outside this requested product.

## Content workflow for a solo owner

1. **Inventory and authenticate.** Capture session, actual date, shift, paper type, original source, completeness and answer-key provenance. Keep written papers, coaching mocks and recollections distinct.
2. **Tag and solve.** Record primary chapter, secondary chapters, concept, method, estimated time and intended difficulty. Independently work through each answer. Mark ambiguous text, missing diagrams and conflicting keys for repair.
3. **Author original engineering questions.** Build conceptually varied problems from the syllabus and verified methods. Include conceptual reasoning, calculations, diagrams where needed, and common-mistake distractors. A numerical substitution is a variant of the same problem family, not a new learning outcome. Do not fill a chapter with near-identical stems to reach 100.
4. **Check each batch.** Verify four distinct options, exactly one valid answer under stated assumptions, units, domains, constants, diagram consistency and complete solutions. Check numerical work independently. For Chemistry include conditions, reagents, charge balance and relevant exceptions.
5. **Release in small useful batches.** Start with one checked mixed set per track and a small group of complete chapters. Display actual ready counts. Expand to every chapter and then Chemistry sets 2 and 3. Never advertise 100 questions where fewer are available.

A suitable record includes `id`, `subject`, `paper`, `chapter_id`, `secondary_chapter_ids`, `concept_ids`, `problem_family_id`, `question_bn`, four `options`, `correct_index`, worked `explanation`, `origin`, `source_url`, `source_session`, `source_shift`, `reference_edition`, `review_status`, and track eligibility. Authored practice uses `origin: original_practice`; only authenticated papers use `origin: past_exam`. Unknown source fields stay empty.

Publication gates must exclude unresolved or unchecked items, reject duplicate stems/answer conflicts, and enforce exactly 100 ready questions per published set. Schema checks alone cannot establish scientific correctness. Teacher review is desirable, but an initial self-checked release must describe its review level accurately.

## Website placement and behaviour

Use the existing Engineering navigation item. Opening it should show two clear target cards. After target selection, show “Mixed practice” and “Chapter practice”; chapter practice presents Mathematics, Physics and Chemistry, then paper, chapter and set. Keep the selected track visible during a test and result review.

The same syllabus can share the six-book catalogue. Track-specific question selection, pacing and progress must remain separate. A BUET/CKRUET label by itself does not make two copies of an identical test meaningfully different.

Chapter sets remain directly accessible without sequence locks. Keep Engineering attempts and progress separate from Medical/Varsity and their full-test lock state. Reuse the existing lazy chapter loading, timer, answer review and device progress patterns where appropriate, with explicit engineering storage keys and manifests. Do not touch full-test national rankings.

Show honest ready counts and a short historical-pattern note before starting. Include “Report a question” in answer review so one person can maintain corrections. Keep diagrams legible on mobile, render mathematical notation consistently and avoid ads inside question options or answer controls.

## Next implementation boundary

The next substantive deliverable is a checked 100-question mixed draft for each requested track, backed by the growing paper/source inventory. Website integration should follow a usable, solved bank rather than an empty catalogue or thousands of unreviewed formula variants. The full chapter-count target remains tracked in `blueprint.json`.

## Source links

- [Official CKRUET 2023–24 prospectus](https://www.ruet.ac.bd/public/storage/notices/ckruet-admission-2023-24-brochure-english.pdf)
- [Official RUET combined-admission notice, 2020–21](https://www.ruet.ac.bd/notice/new-date-of-ruet-kuet-cuet-ug-admission-test-session-2020-21)
- [BUET 2025–26 prospectus, third-party mirror](https://eduresultbd.com/wp-content/uploads/2025/10/buet-admission-test-Prospectus-2025-26.pdf)
- [BUET preliminary introduction report](https://www.thedailystar.net/city/news/buet-introduces-preliminary-tests-admission-2084469)
- [BUET 2025–26 format-change reporting](https://english.thedailycampus.com/university-admission/942/no-preliminary-test-in-buet-admission-this-year)
- [Current KUET admission site](https://admission.kuet.ac.bd/)
- [AAP course plan and suggested books](https://aapathshala.com/media/files/resource/Course_PlanChapterwise_Complete_Preparation_ygQqPiX.pdf)
- [Udvash engineering books/course page](https://udvash.com/courseDetailsEngineering)
- [BUET 2023–24 third-party compilation](https://codehorsebd.com/buet-preli-admission-question-solution-2023-24/)
- [BUET 2022–23 third-party compilation](https://codehorsebd.com/buet-preli-admission-question-solution-2022-23/)
- [CKRUET 2023–24 third-party textbook-match compilation](https://codehorsebd.com/cuet-kuet-ruet-question-solution-2023-24/)

Detailed provenance and exclusions are in `content/engineering/sources.json`.
