# AdmissionTestBD — Free Admission Practice

Medical and varsity model tests are free. Full model tests unlock sequentially after completing the preceding test. Completed tests can be retaken. Past questions and revision resources have no sequential lock. Chapter tests are planned separately and will not use a sequence lock.

## Run locally

```bash
python3 server.py
```

Open http://localhost:8080. Configure `DATABASE_URL` for Neon PostgreSQL to enable accounts and rankings. Static test practice works independently of payment.

## Deployment

Deploy this repository to Vercel using the existing `vercel.json`, and configure `DATABASE_URL` in the project environment.

The public admin panel, payment routes, SMS webhook and paid-access checks have been removed. Existing historical enrollment and payment records are retained in the database; no migration deletes student records.

The root, public and web copies of index.html must remain identical.
