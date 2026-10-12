# BUET Written, DU A Written and engineering past-paper expansion

Status: implementation plan, researched 12 October 2026. This document does not claim that a written question bank or written grading engine has already been deployed.

## 1. Product decision and limits

Create a new **লিখিত প্রস্তুতি** navigation item immediately before **বিগত বছরের প্রশ্ন**. Its tabs are BUET Written and DU A / Science Written. Preserve the existing chapter practice, MCQ model tests, Medical and Varsity datasets.

Use **20 main questions per original written practice set**, not 100. A multipart question counts once; display the subpart count separately. Chapter sets will also target 20 after their content passes review. Do not promise 100 written papers or immediately populate every chapter.

First content release: one original 20-question PCM practice paper for BUET and one independently authored 20-question PCM practice paper for DU A. These are shortened/custom training papers, clearly labelled **অনুশীলন সেট**, rather than an official complete examination. A proposed balanced starting composition is 7 Mathematics, 7 Physics and 6 Chemistry; this is a product choice, not a measured historical distribution. Change the composition if the verified benchmark demands it. The two tracks must have different questions and different expected answer depth.

Engineering practice remains Mathematics, Physics and Chemistry only. DU Science is a separate track: its complete subject-choice profiles, including Biology or language options where permitted, must be checked against the relevant official Science Unit guide. A PCM-only DU pilot must be labelled as partial subject preparation. Do not silently present it as a full DU A paper.

## 2. What was inspected and what remains uncertain

The existing website past-paper viewer is MCQ-only. data/past_15years_tests.json has Medical and Varsity keys, 15 sessions each and 100 questions per session. Its year selector uses the session as an identifier and its renderer expects four options. Written papers need a separate renderer; multiple engineering institutions/rounds in the same year need unique paper IDs. The displayed statement about 3,000 question papers should say 3,000 questions for the existing data.

DU's official 2025–26 announcement specifies 60 marks of MCQ in 45 minutes and 40 written marks in 45 minutes. A mirrored BUET 2025–26 prospectus was downloaded and visually checked: PDF page 3 specifies 20 questions each in Mathematics, Physics and Chemistry, 600 marks and three hours for Module A. These are session-specific baselines, not verified 2026–27 rules. Our requested 20-question mixed sets are custom practice, not full replicas.

Public BUET 2023–24 and 2024–25 written previews were inspected across the three subjects on Chorcha. Sample methods included constrained geometry, calculus modelling, energy/work and equilibrium reasoning. Several preview entries had incomplete text or a foreign-institution tag; those must not be ingested as authenticated BUET questions. The 2025–26 preview also appears incomplete and cannot establish complete paper counts. DU 2023–2025 public written samples were inspected; some equations and diagrams were missing. These observations support an initial skill blueprint, not a complete frequency analysis.

A linked 2019–20 BUET compilation was downloaded and its first page visually checked as written-format content. The generic Dr. Siddiq 2023–24 PDF was downloaded and checked; its first page is MCQ, so it is rejected as a written benchmark. Some older directory links were discoverable but only displayed a Drive loading/sign-in shell. A listed year is not a verified, available full paper.

Before claiming a track matches previous-year level, assemble at least three complete, readable recent papers for that track, confirm their identities, and independently solve a representative benchmark. Record the precise missing years/subjects rather than filling gaps. Current research is sampled and does not yet meet that full-corpus release gate.

## 3. Past-paper collection and benchmarking

Collect and identify the original paper before authoring model content. Prefer official university documents or genuine exam-page scans. Third-party transcriptions are secondary and must be compared with a scan or another independently sourced copy.

For every paper record institution, unit, session, test date if verified, stage/round, MCQ or written, language, marks, timing, original question count, source URL, page references, completeness and attribution. Use statuses: verified full; verified partial; source-linked compilation; preview only; unavailable; unresolved identity. Do not label publisher-created model tests as past papers.

Tag each benchmark question with chapter, method, concepts, supplied data, requested outputs, proof/reasoning requirements, diagrams, branch/domain issues, units, marks and an estimated solve time. Difficulty is judged through these traits and timed solving, not large numbers or long wording. Exclude incomplete and mixed-institution entries from the difficulty baseline.

Recent papers should guide current style; older papers provide additional methods. Maintain separate format versions. Publish historical years with their actual formats. Never invent a BUET preliminary stage for a year merely to fill the archive.

## 4. Authoring original written questions

Write a problem specification first: the learning objective, intended method, necessary assumptions, expected solution and permissible alternative routes. Then write the Bangla statement, diagrams and marking guide.

Originality must change a meaningful constraint, scenario or inference. Changing coefficients, renaming a particle or removing MCQ options is not enough. Existing MCQ templates must not become the written bank by stripping their choices.

Each question needs a complete statement, subject/chapter, main/subpart marks, appropriate hint, exact or justified approximate answer, worked solution, alternative-answer notes, units/domain constraints, common mistakes, independent checking evidence and benchmark IDs. Any marking guide is our practice rubric, not a claimed official examiner scheme.

Proposed candidate buffer: author 30–40 questions per track, review them, select the best 20 and retain rejected items with reasons. Do not force quantity by promoting unresolved questions. Within each 20-question paper, prohibit equivalent method repeats and near-clone prompts. Across papers disclose reuse and limit it during assembly.

## 5. Criticism and validation engine

This is an editorial and mathematical release pipeline, not an assertion that an AI can certify perfect exam quality.

Workflow: draft -> blind independent solve -> compare answers -> mathematical/physical checks -> benchmark comparison -> originality review -> Bangla/diagram review -> repair and recheck -> eligible pool -> paper assembly -> release audit.

The independent solver receives the question and assumptions without the author's answer or solution. Use symbolic identities, numerical substitution, equation residuals, boundary/domain tests and unit/conservation checks where applicable. Chemistry additionally checks balanced atoms/charge, reaction conditions, species and approximation validity. Conceptual or proof questions need a separately reasoned review; an exact-string answer match is insufficient.

Critical failures cannot be outweighed by a high aggregate score:

- Wrong answer, inconsistent branches or an unjustified approximation.
- Missing data, ambiguous assumptions or more than one unintended interpretation.
- Missing/unreadable diagram required for solving.
- Nonphysical conditions, invalid domains or impossible species.
- Incorrect benchmark institution, stage, subject or year.
- MCQ conversion, numerical clone or copied third-party solution.
- Rubric that does not credit a valid alternative solution.
- Question whose difficulty claim is unsupported by readable benchmarks.

Proposed editorial scoring: correctness 40, solvability/clarity 15, benchmark fit 20, meaningful originality 15, and language/diagram quality 10. Eligibility requires at least 90/100 **and zero critical failures**, with all checks actually completed. This is a proposed rubric, not a measured quality score. Missing evidence yields review_required, never an automatic pass.

Calibrate the critic using known incorrect answers, underdetermined problems, missing diagrams, wrong units, near clones, trivial MCQ conversions and sound past-paper-style problems. It must reject the deliberately bad cases and accept appropriate short DU questions; unnecessary long solutions must not earn a higher quality score. Record reviewer/solver versions and reasons. Automatic checking does not mean independent teacher certification.

## 6. Student experience

Written landing page -> choose BUET or DU A -> choose chapter set or 20-question practice paper -> see scope, marks and estimated time -> start.

Students work on paper. The browser provides a timer, save/resume and optional notes. Practice mode permits a hint after an initial attempt; timed mode hides solutions until submission. On submission show our worked solution and marking guide. Students enter criterion-level self-assessment, with a clear self-assessed label. Do not infer an official grade from their text or place it in a national ranking.

Add bookmark, retry, mark-for-review and question-report controls. Later photo uploads or AI grading are a separate feature requiring accuracy evaluation and operating-cost decisions. They are not required for the first release.

Use mobile-friendly equations and zoomable diagrams. Keep answers hidden during an attempt, handle reloads, distinguish submitted/cancelled work and prevent late fetch responses from overwriting a newer track selection. Written progress must use separate, versioned storage keys.

## 7. Engineering within the existing past-paper section

Add an Engineering tab beside Medical and Varsity. Its filters are institution, session, stage and MCQ/written. Institutions may include BUET, CUET, KUET, RUET and historically combined CKRUET, subject to actual source availability. Preserve historical institution identities rather than merging every paper under CKRUET.

Each available paper card shows the true year, format, scope, completeness and source status. Full verified MCQ data can use timed MCQ answering. Full verified written data uses paper solving plus independently authored solutions/self-assessment. Partial papers show the exact coverage and cannot start a falsely labelled full test. Source-linked compilations remain clearly labelled links/previews, not imported complete tests.

Initial source leads include BUET preliminary 2021–22, 2022–23 and 2023–24 compilations, the 2019–20 written compilation, recent written previews and CKRUET 2023–24. These are acquisition candidates; none gains a verified full status just because a listing exists. Check each link and paper before counting it. Extend backwards only where a genuine readable source can be established. Display the actual number of sessions rather than promising 15 engineering years.

Keep generated original practice questions out of the authentic past-paper archive. Link to third-party compilations instead of copying their entire solution books. Host scans only when redistribution rights are established; write our own solutions for permitted imported questions.

## 8. Technical shape

Separate manifests for written practice and engineering past papers, with content-hashed per-set payloads fetched on demand. Written questions use a type discriminator, statement/parts, solution steps and rubric; MCQ questions retain options and correct_index. A written question must never be padded with dummy MCQ options.

Suggested files: assets/written-practice.js/.css; assets/engineering-archive.js/.css; data/written_practice.json; data/engineering_archive.json; content/written/benchmarks.json; content/written/questions.json; review_written.py; verify_written.py; verify_written_ui.cjs. Mirror deployed assets under the existing public/web layout as applicable.

Paper selection uses paper_id, not just session. Separate provenance from answer review. Schema fields include origin, source_status, completeness, review_status, independent_solver_status, benchmark_refs, method_group, format_version and versioned question IDs.

## 9. Execution order and acceptance criteria

1. Finish source identity checks and recent-paper benchmarks; create the availability matrix.
2. Implement and calibrate the offline review pipeline against good/bad fixtures.
3. Author candidate pools, solve independently, repair and select the first 20 per track. Keep unresolved questions unpublished.
4. Build the separate written section and extend the archive with the verified available engineering papers or clearly labelled source links.
5. Run content, schema, rendering and browser-flow checks, then publish the reviewed release.
6. Expand chapter by chapter to 20-question sets. Add another mixed paper only when enough diverse, passed content exists.

Release checks: both practice tracks render exactly 20 main questions; no equivalent method repeats; all rubric points reconcile with marks; equations/diagrams are complete; solutions remain hidden in timed mode; timer/save/resume/cancel work; valid alternative solutions receive credit; archive filters distinguish multiple papers per session; partial/source-linked papers are not advertised as complete; Medical/Varsity flows still work; root/public/web mirrors match; deployed navigation places Written immediately before Past Papers. Verify the actual live site after deployment.

The plan deliberately prioritises reviewable content over a large initial catalogue. Teacher review and student solve-time data improve calibration, but their absence must remain explicit rather than being replaced by an automated perfect-quality claim.
