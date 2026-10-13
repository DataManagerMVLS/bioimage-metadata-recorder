# REMBI and BioImage Archive interoperability checklist

Status: **draft mapping, not validated submission compatibility**. This is based on the recorder's acquisition/analysis model and the source forms. BioImage Archive requirements and controlled vocabulary identifiers must be checked against current submission documentation before claiming compliance.

| Domain | Recorder data to inspect | Validation needed |
|---|---|---|
| Study | Study name, PI/contact, purpose | Stable study identifier, description, provenance and contributor roles |
| Biosample | Biosample, specimen, organism, preparation | Ontology identifiers, sample relationships, organism/tissue/cell line and biological replicate descriptions |
| Image acquisition | Sessions, dates, microscope, objective/lens, channels, imaging method | Instrument model, acquisition settings, illumination/detector, units and raw image identifiers |
| Image analysis | Multiple analysis records per study, software, input/output paths | Software version, processing parameters, workflows, derived-image lineage |
| Files and access | Local paths, Excel exports | Persistent file identifiers, formats, checksums, access terms and repository-ready file manifests |

## Follow-up tasks

1. Review every existing acquisition and analysis field against REMBI categories; document required, recommended and optional fields without claiming universal requirements.
2. Add ontology CURIE/IRI and label pairs for terms rather than only free-text names.
3. Preserve one acquisition record linked to **multiple analysis records** and their corresponding source images.
4. Design a separate, machine-readable repository export and validate against the **current** BioImage Archive submission schema; XLSX export alone is not a repository submission.
5. Use synthetic data to verify image/file manifests, relationships, provenance and round-trip imports.
6. Review handling of personal/contact details, research-sensitive data, authentication and retention before production.

This checklist supports FAIR-oriented metadata capture. It does **not** establish that a dataset is FAIR, publicly deposited, or BioImage Archive compliant.
