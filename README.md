# Bioimage Metadata Recorder

Prototype for recording REMBI-aligned light microscopy acquisition and image analysis metadata.

Open `index.html` in a browser to try it. Records are stored locally in the browser; export backups regularly. This is a hackathon prototype and does not directly submit to BioImage Archive.

See `docs/hackathon-plan.md` for the development plan and [GitHub issues](https://github.com/DataManagerMVLS/bioimage-metadata-recorder/issues) for priorities, especially [#12: effortless researcher-led metadata capture and PI buy-in](https://github.com/DataManagerMVLS/bioimage-metadata-recorder/issues/12).

## Why this tool exists

Ann Wheeler's University of Edinburgh presentation, *No Cost, No Tech, No Excuses! Bioimaging Data Management*, sets out the practical challenge: microscopy data is generated across distributed facilities and often lives on network-attached storage (NAS), USB drives or other imperfect infrastructure. A useful metadata workflow must work **without requiring specialist IT support or expensive new systems**, and should scale to better infrastructure later.

The presentation describes the need for a tool that:

- Works for **PIs, postdoctoral researchers and students**, at acquisition time or later when reanalysing older images.
- Captures sufficient contextual information to support **FAIR and REMBI-aligned** imaging data management and preparation for the **BioImage Archive (BIA)**.
- Keeps acquisition and analysis documentation together with clear links to the associated files, regardless of where images are stored.
- Supports **separate, repeatable analysis records**, since the same raw images may be analysed again using different methods.
- Allows metadata to be revised or resubmitted rather than treating a form as a one-off exercise.
- Reduces the scramble to reconstruct metadata just before publication.

### Practical workflow and data organisation

The presentation demonstrates a deliberately low-tech approach: **image acquisition and image analysis forms** accompany image files on NAS or USB storage. The corresponding online workflow can distribute information to the submitter, data owner and data manager. These examples motivate the web prototype; they do **not** mean every notification or storage integration is implemented here.

For BIA-oriented organisation, the presentation uses a hierarchy such as:

`Study → Study component → Biosample/specimen → Image acquisition → Image analysis`

An example covers cell-culture models and HeLa cells, with live epifluorescence and confocal acquisitions followed by analysis. Keeping paths to raw data, analysis inputs, derived outputs, methods and software together helps retain provenance across that lifecycle.

### Research data management considerations

The presentation also highlights institutional information-security and research-data services, and funder expectations around secure retention, documentation and appropriate handling of confidential or identifiable information. **Do not enter confidential patient or participant information into this prototype** without an approved institutional assessment and deployment.

These are the **design motivations from the presentation**, not claims that the current prototype has achieved complete REMBI or BIA compliance. The hackathon priorities are to test usability, metadata completeness, storage-independent workflows and archive mapping.

**Source:** Ann Wheeler, University of Edinburgh / ESRIC, *No Cost, No Tech, No Excuses! Bioimaging Data Management* (slides supplied for the hackathon; especially slides 8, 13–18).

## Collaboration and branch protection

The repository is private; collaborators need a GitHub invitation. Develop on feature branches and open pull requests into `main`. A `Protect main` ruleset has been configured to require pull requests, preventing direct README updates. Recommended settings include blocking force pushes and deletion; verify the actual rules in [repository settings](https://github.com/DataManagerMVLS/bioimage-metadata-recorder/settings/rules). For the hackathon, keep required approvals at zero until collaborators can review, and leave Copilot-specific additional approvals off. Add required CI status checks once the check name and passing state are verified.

The draft BioImage Archive file-list export is not a dataset submission or upload. Backend tests: `python -m pytest -q tests/test_backend.py`.

A provisional Flask backend (`app.py`) is included, but the original GitLab `app.py` still needs to be obtained and compared. This repository was recreated because the original GitLab repository was inaccessible; it was not migrated. Licence, ownership and permissions require agreement with collaborators before public release.

## Background reading

- [Data management for bioimaging: no-cost, easy-access tools for Edinburgh](https://libraryblogs.is.ed.ac.uk/datablog/2026/01/13/data-management-for-bioimaging-no-cost-easy-access-tools-for-edinburgh/) — University of Edinburgh Data Blog (13 January 2026). Context for practical bioimaging data management and metadata recording.
