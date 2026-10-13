"""API contract tests with fictional records and no network or SMTP calls."""
import base64
import importlib
import io
import json
import os
import zipfile

import pytest


def sample_xlsx():
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as z:
        z.writestr("[Content_Types].xml", "<Types/>")
    return base64.b64encode(stream.getvalue()).decode("ascii")


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("API_KEY", "local-test-secret")
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    monkeypatch.setenv("ALLOWED_EMAIL_DOMAINS", "example.org")
    monkeypatch.delenv("SMTP_HOST", raising=False)
    import app as backend
    importlib.reload(backend)
    backend.app.config.update(TESTING=True)
    return backend.app.test_client(), tmp_path


def payload(kind):
    return {
        "kind": kind,
        "analysis_index": 0 if kind == "analysis" else None,
        "study": "Fictional microscopy study",
        "to": "tester@example.org; outsider@other.test",
        "subject": "Test metadata",
        "summary": "Synthetic example",
        "record": {
            "id": "fake-study-1",
            "acquisition": {"study_name": "Fictional microscopy study"},
            "analyses": [{"software": "Fictional software"}],
        },
        "attachments": [{"filename": "test.xlsx", "content_base64": sample_xlsx()}],
    }


def test_health_and_frontend(client):
    http, _ = client
    health = http.get("/api/health")
    assert health.status_code == 200
    assert health.json["app"] == "bioimage-metadata-recorder"
    assert http.get("/").status_code == 200


@pytest.mark.parametrize("kind", ["acquisition", "analysis"])
def test_submission_persists_json_and_attachment(client, kind):
    http, data_dir = client
    result = http.post("/api/submit", json=payload(kind),
                       headers={"X-API-Key": "local-test-secret"})
    assert result.status_code == 200
    assert result.json["saved"]
    assert result.json["emailed"] is False
    assert "outsider@other.test" in result.json["rejected"]
    folder = data_dir / result.json["saved"]
    saved = json.loads((folder / "submission.json").read_text())
    assert saved["kind"] == kind
    assert (folder / "attachment-1.xlsx").read_bytes().startswith(b"PK")


def test_unauthorized_submission(client):
    http, data_dir = client
    result = http.post("/api/submit", json=payload("acquisition"))
    assert result.status_code == 401
    assert list(data_dir.iterdir()) == []


def test_bad_payload_and_attachment(client):
    http, _ = client
    headers = {"X-API-Key": "local-test-secret"}
    assert http.post("/api/submit", json={"kind": "wrong"}, headers=headers).status_code == 400
    bad = payload("acquisition")
    bad["attachments"][0]["content_base64"] = "not-base64!"
    assert http.post("/api/submit", json=bad, headers=headers).status_code == 400


def test_missing_recipient_is_safe(client):
    http, _ = client
    body = payload("analysis")
    body["to"] = None
    result = http.post("/api/submit", json=body,
                       headers={"X-API-Key": "local-test-secret"})
    assert result.status_code == 200
    assert result.json["recipients"] == []


def test_ontology_input_validation(client):
    http, _ = client
    assert http.get("/api/ontology?ontology=bad%2Furl&q=test").status_code == 400
    assert http.get("/api/ontology?ontology=ncbitaxon&q=").status_code == 400


@pytest.mark.parametrize("kind", ["acquisition", "analysis"])
def test_browser_contract_with_realistic_record(client, kind):
    """Simulate the exact JSON payload posted by index.html, including XLSX."""
    http, data_dir = client
    body = payload(kind)
    body["record"]["acquisition"].update({
        "biosample": "Synthetic fixed cells",
        "specimen": "Fictional slide A",
        "sessions": [{"date": "2026-10-13", "microscope": "Confocal",
                      "lens": "40x", "channels": "DAPI"}],
    })
    body["record"]["analyses"] = [{
        "software": "ImageJ", "input_path": "fictional/input",
        "output_path": "fictional/output", "description": "Synthetic segmentation"
    }]
    response = http.post("/api/submit", json=body,
                         headers={"X-API-Key": "local-test-secret"})
    assert response.status_code == 200
    folder = data_dir / response.json["saved"]
    saved = json.loads((folder / "submission.json").read_text(encoding="utf-8"))
    assert saved["record"]["acquisition"]["sessions"][0]["microscope"] == "Confocal"
    assert saved["record"]["analyses"][0]["software"] == "ImageJ"
    assert zipfile.is_zipfile(folder / "attachment-1.xlsx")
    assert response.json["emailed"] is False
