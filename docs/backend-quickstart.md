# Minimal Flask backend (development only)

This is a **new reconstruction**, not recovered original source. It implements the routes already used by `index.html`: `/api/health`, `/api/ontology`, and `/api/submit`.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export API_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
python app.py
```

Open http://127.0.0.1:5000 and use fictional test records.

**Important:** In `index.html`, set `CONFIG.apiKey` to the same key **for local testing only**. Do not commit that change: frontend JavaScript is visible to everyone who can access the page. The key header is a prototype compatibility mechanism, **not secure multi-user authentication**.

## Storage and notifications

- Each submission is saved under `data/<timestamp>-<random-id>/` with a JSON record and XLSX attachments.
- The `data/` directory must be excluded from Git and backed up appropriately.
- Ontology requests proxy to EMBL-EBI OLS4.
- SMTP is disabled unless `SMTP_HOST`, `SMTP_FROM` and optional login settings are provided.
- Recipients are restricted to domains in `ALLOWED_EMAIL_DOMAINS`. No domain allowlist means no emails are sent.
- Email failure does not undo saved submissions.

## Limitations

This implementation has **not been tested against a live facility**. It has no individual user authentication, authorisation, audit log, retention policy, encrypted storage or deployment hardening. It is unsuitable for internet exposure, identifiable information or confidential research data. Do not configure SMTP or run outside localhost until security review. The ontology proxy requires network access.

The health endpoint is intentionally unauthenticated for frontend discovery. The backend does not implement a read/list API, nor direct BioImage Archive or OMERO deposition.
