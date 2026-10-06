# zdb-ingest-fixture

**Deliberately vulnerable. Do not deploy.** A test fixture for z-day-break's
scanner-import validation: GitHub CodeQL reports the two flaws in `app.py`,
the platform imports those alerts, validates them with codex-security, and
mirrors the fix back through the alert state.
