# AdmissionTestBD — Free Admission Practice

Medical and varsity model tests are free. Full model tests unlock sequentially after completing the preceding test. Completed tests can be retaken. Past questions and revision resources have no sequential lock. Chapter practice is available in a separate navigation section with independent Medical and Varsity Science tracks, textbook/paper selection, chapter search, timed practice and explanations. Chapter sets have no sequence lock.

## Run locally

```bash
python3 server.py
```

Open http://localhost:8080. Configure `DATABASE_URL` for Neon PostgreSQL to enable accounts and rankings. Static test practice works independently of payment.

## Deployment

Deploy this repository to Vercel using the existing `vercel.json`, and configure `DATABASE_URL` in the project environment.

The public admin panel, payment routes, SMS webhook and paid-access checks have been removed. Existing historical enrollment and payment records are retained in the database; no migration deletes student records.

The root, public and web copies of index.html must remain identical.

## Chapter practice

Run `python build_chapter_practice.py` to rebuild the small catalogue and chapter payloads in `data/` and `public/data/`. Existing structured banks are retained after deduplication and conflict checks. Deficits are filled by `original_practice.py` using author-written concept/misconception pairs in `content/original_facts.txt` and worked numerical templates.

Every listed chapter/topic has exactly 100 questions. Each chemistry chapter has three disjoint sets of exactly 100 questions. Coverage: 107 chapters/topics, 12,700 questions, including 1,308 retained bank items and 11,392 original practice items. See `CHAPTER_PRACTICE_COVERAGE.md` for per-chapter figures.

Original concept questions combine two distinct statements; each unordered concept pair is used once in a chapter. Numerical questions use distinct input cases across four exercise families per chapter. Distinct questions may share concepts: these counts are not counts of distinct learning outcomes. New questions are labelled original practice, not quoted textbooks or past exams. Arithmetic/structure checks are not independent subject-specialist verification. The repository's nominal 2,000-entry knowledge file contains repeated content and is not treated as 2,000 unique source facts.

Only catalogue metadata loads when browsing. Question data is fetched on demand for the chosen chapter using content-hashed URLs. Medical and Varsity Science share suitable textbook content but save progress independently. Chapter practice is unrestricted and never updates full-test locks or rankings. Attempts/progress use v2 storage keys so old short-set scores are not presented as completion of new 100-question sets.

Bangla contains eight admission-preparation topics, not a complete first-paper literature textbook. ICT contains six chapters. Individual university units may require different subjects. Catalogue sources are references for chapter organisation, not claims that every original question was checked against those books.

Chapter JS/CSS copies in assets/, public/assets/ and web/assets/ must remain identical. Run `python verify_chapter_practice.py` for coverage, uniqueness, payload/provenance and numerical sanity checks.

## Engineering practice

The Engineering navigation item provides separate BUET historical preliminary and CKRUET custom PCM tracks. Each has six book/paper groups and 51 chapters: 100 questions per Mathematics/Physics chapter and three disjoint 100-question Chemistry sets per chapter. One 100-question mixed set per track reuses its chapter bank. Questions are original parameterised practice; a shared Chemistry concept core means 14,200 chapter entries represent 11,920 distinct question stems, not 14,200 distinct learning outcomes. Independent teacher review and a complete authenticated ten-year archive are not claimed. References and session-specific format notes are available directly in the site.

Rebuild with `python build_engineering.py`; validate with `python verify_engineering.py`. UI assets and HTML are mirrored in root/public/web, and hashed chapter payloads load on demand. Engineering attempts/progress have independent local-storage keys and never change Medical/Varsity test unlocks.
