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

Run `python build_chapter_practice.py` to rebuild `data/chapter_practice.json` and its public copy from the existing structured question banks. The builder removes repeated question texts, rejects answer/chapter conflicts and excludes broad/unmapped chapter labels. It does not establish factual correctness of every source answer.

Targets: one set of up to 100 questions per chapter; chemistry has three disjoint sets of up to 100 questions per chapter. Short banks remain short. Empty sets are disabled. See `CHAPTER_PRACTICE_COVERAGE.md` for actual coverage.

Shared textbook content is used by both admission tracks; progress is keyed independently by track and set. Chapter progress and active attempts are saved on the current device and do not update full-test sequential progress or national rankings. The active timer uses an absolute deadline and survives reload.

Catalogue references are listed in the generated dataset. No external book PDFs or newly generated questions are included. Bangla and ICT are shown as coverage gaps because the current repository has no questions for them. The varsity section covers science preparation and supplemental admission topics; individual university units may require different subjects.

Chapter JS/CSS copies in assets/, public/assets/ and web/assets/ must remain identical.
