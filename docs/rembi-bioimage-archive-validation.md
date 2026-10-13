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

## Verified against official guidance (13 October 2026)

- REMBI describes separate **Study, Study Component, Biosample, Specimen, Image Acquisition, Image Data, and Analysed Data** metadata areas. It distinguishes semantic metadata recommendations from any one archive's submission schema. Reference: https://www.nature.com/articles/s41592-021-01166-8
- BioImage Archive uses the **BioStudies submission service**. Submission involves a registered account, uploaded data, at least one study component, file lists and study metadata entered in the submission form. Reference: https://www.ebi.ac.uk/bioimage-archive/submit/
- The official BIA file-list guide specifies a **Files** first column, one file per row, exact case-sensitive relative paths with forward slashes, and **source_image** for annotations. It supports TSV or XLSX. Reference: https://www.ebi.ac.uk/bioimage-archive/help-file-list/
- The new `POST /api/bia-file-list` endpoint generates **draft TSV file lists** for study components or annotations. It accepts explicit paths and optional per-file metadata. It **does not** upload image files, infer files from workstation paths, validate against a live submission, or submit data to BioStudies.

### Draft export request

```json
{
  "component": "annotations",
  "files": [
    {
      "path": "annotations/mask-001.tif",
      "source_image": "images/raw-001.tif",
      "metadata": {
        "Annotation type": "segmentation",
        "Software": "ImageJ"
      }
    }
  ]
}
```

Send as JSON to `POST /api/bia-file-list` with the `X-API-Key` header. The response is `bia-file-list.tsv`. Paths must match **files uploaded into the BioStudies user space**; local acquisition/analysis paths are not interchangeable with repository paths.

### Outstanding gaps

- Formal field-by-field validation against the REMBI model reference and each imaging modality's recommended fields.
- Automatic derivation of file manifests from actual image datasets with explicit source-image lineage.
- Frontend workflow to collect file-list rows and trigger draft export.
- Real browser-based submission test and real BIA template validation, both requiring an appropriate local/browser or authenticated test environment.
