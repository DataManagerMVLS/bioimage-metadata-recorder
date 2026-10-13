"""Minimal local-development Flask backend for the Bioimage Metadata Recorder.

Reconstruction based on the existing index.html API, not the original backend.
Not approved for public deployment or sensitive research data.
"""
import base64
import binascii
import json
import os
import re
import smtplib
import ssl
import uuid
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError

from flask import Flask, jsonify, request, send_from_directory

ROOT = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("DATA_DIR", str(ROOT / "data"))).resolve()
API_KEY = os.environ.get("API_KEY", "")
FACILITY_EMAIL = os.environ.get("FACILITY_EMAIL", "")
MAX_BYTES = 8 * 1024 * 1024
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_BYTES


@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.get("/api/health")
def health():
    return jsonify(app="bioimage-metadata-recorder", facility_email=FACILITY_EMAIL)


@app.get("/api/ontology")
def ontology():
    # Fixed upstream host; no arbitrary URL forwarding.
    ont = request.args.get("ontology", "").strip()
    query = request.args.get("q", "").strip()
    if not re.fullmatch(r"[a-zA-Z0-9_-]{2,32}", ont) or not 1 <= len(query) <= 120:
        return jsonify(error="Invalid ontology or search query"), 400
    params = urlencode(dict(ontology=ont, q=query, type="class", rows=10,
                            fieldList="label,obo_id,description"))
    url = "https://www.ebi.ac.uk/ols4/api/select?" + params
    try:
        with urlopen(Request(url, headers={"User-Agent": "BioimageMetadataRecorder/0.1"}),
                     timeout=8) as response:
            data = response.read(256_000)
        return app.response_class(data, mimetype="application/json")
    except (URLError, TimeoutError, ValueError):
        return jsonify(error="Ontology service unavailable"), 502


def recipients_from(value):
    if not isinstance(value, str):
        return []
    candidates = [v.strip() for v in re.split(r"[;,]", value) if v.strip()]
    valid = [v for v in candidates if re.fullmatch(r"[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+", v)]
    domains = {d.strip().lower() for d in os.environ.get("ALLOWED_EMAIL_DOMAINS", "").split(",") if d.strip()}
    allowed = [v for v in valid if domains and v.rsplit("@", 1)[1].lower() in domains]
    return list(dict.fromkeys(allowed))[:20], list(dict.fromkeys(set(candidates) - set(allowed)))


@app.post("/api/submit")
def submit():
    # Key is required for any write; only run on trusted localhost for development.
    if not API_KEY:
        return jsonify(error="API_KEY must be configured before submissions are enabled"), 503
    if request.headers.get("X-API-Key", "") != API_KEY:
        return jsonify(error="Unauthorized"), 401
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or payload.get("kind") not in ("acquisition", "analysis"):
        return jsonify(error="Invalid submission kind"), 400
    if not isinstance(payload.get("record"), dict):
        return jsonify(error="Missing record"), 400
    attachments = payload.get("attachments", [])
    if not isinstance(attachments, list) or len(attachments) > 3:
        return jsonify(error="Invalid attachments"), 400
    prepared = []
    for attachment in attachments:
        if not isinstance(attachment, dict):
            return jsonify(error="Invalid attachment"), 400
        filename = attachment.get("filename", "")
        encoded = attachment.get("content_base64", "")
        if not isinstance(filename, str) or not filename.lower().endswith(".xlsx"):
            return jsonify(error="Only XLSX attachments are supported"), 400
        if not isinstance(encoded, str):
            return jsonify(error="Invalid attachment data"), 400
        try:
            raw = base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError):
            return jsonify(error="Invalid base64 attachment"), 400
        if len(raw) > 4_000_000 or not raw.startswith(b"PK"):
            return jsonify(error="Invalid or oversized XLSX attachment"), 400
        prepared.append(raw)

    DATA_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    # Never use client-provided filenames or paths for filesystem writes.
    submission_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:12]
    folder = DATA_DIR / submission_id
    folder.mkdir(mode=0o700)
    (folder / "submission.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    for i, raw in enumerate(prepared, start=1):
        (folder / f"attachment-{i}.xlsx").write_bytes(raw)

    allowed, rejected = recipients_from(payload.get("to", ""))
    emailed, email_error = False, ""
    host = os.environ.get("SMTP_HOST", "")
    if host and allowed:
        try:
            port = int(os.environ.get("SMTP_PORT", "587"))
            msg = EmailMessage()
            msg["From"] = os.environ["SMTP_FROM"]
            msg["To"] = ", ".join(allowed)
            msg["Subject"] = str(payload.get("subject", "Bioimage metadata submission"))[:200]
            msg.set_content(str(payload.get("summary", ""))[:10000])
            for i, raw in enumerate(prepared, start=1):
                msg.add_attachment(raw, maintype="application",
                                   subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   filename=f"metadata-{i}.xlsx")
            with smtplib.SMTP(host, port, timeout=15) as server:
                server.starttls(context=ssl.create_default_context())
                user = os.environ.get("SMTP_USER")
                if user:
                    server.login(user, os.environ["SMTP_PASSWORD"])
                server.send_message(msg)
            emailed = True
        except (OSError, smtplib.SMTPException, KeyError, ValueError) as exc:
            email_error = type(exc).__name__

    return jsonify(saved=str(folder.relative_to(DATA_DIR)), emailed=emailed,
                   recipients=allowed if emailed else [], rejected=rejected,
                   email_error=email_error)


@app.errorhandler(413)
def too_large(_error):
    return jsonify(error="Request exceeds 8 MB limit"), 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
