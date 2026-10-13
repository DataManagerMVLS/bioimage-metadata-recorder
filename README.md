# Bioimage Metadata Recorder

Prototype for recording REMBI-aligned light microscopy acquisition and image analysis metadata.

Open `index.html` in a browser to try it. Records are stored locally in the browser; export backups regularly. This is a hackathon prototype and does not directly submit to BioImage Archive.

See `docs/hackathon-plan.md` for the development plan and [GitHub issues](https://github.com/DataManagerMVLS/bioimage-metadata-recorder/issues) for priorities, especially [#12: effortless researcher-led metadata capture and PI buy-in](https://github.com/DataManagerMVLS/bioimage-metadata-recorder/issues/12).

## Collaboration and branch protection

The repository is public; anyone can browse it, while write access requires a collaborator invitation. Develop on feature branches and open pull requests into `main`. A `Protect main` ruleset has been configured to require pull requests, preventing direct README updates. Recommended settings include blocking force pushes and deletion; verify the actual rules in [repository settings](https://github.com/DataManagerMVLS/bioimage-metadata-recorder/settings/rules). For the hackathon, keep required approvals at zero until collaborators can review, and leave Copilot-specific additional approvals off. Add required CI status checks once the check name and passing state are verified.

The draft BioImage Archive file-list export is not a dataset submission or upload. Backend tests: `python -m pytest -q tests/test_backend.py`.

A provisional Flask backend (`app.py`) is included, but the original GitLab `app.py` still needs to be obtained and compared. This repository was recreated because the original GitLab repository was inaccessible; it was not migrated. The repository is public and includes an MIT licence; copyright ownership and the authority to license original project material should be confirmed with the original contributors and any relevant institutions.

## Project origins, authorship and acknowledgements

This GitHub repository is a reconstruction and continuation of the original Bioimage Metadata Recorder project, **not a migration from GitLab**. Access to the original GitLab repository was unavailable during hackathon preparation, and the provisional Flask `app.py` still needs to be compared with the original implementation.

The following contributors should be explicitly recognised for their roles:

- **Ann Wheeler** (University of Edinburgh) — original project concept, scientific and microscopy metadata requirements, methodology and project leadership.
- **Ewan McDowall** — **original application code author and project IT support**.
- **Stephen Fox** (University of Glasgow) — research data management, FAIR alignment, reconstruction of the GitHub project, documentation and further development.

See [CITATION.cff](CITATION.cff) for the software citation. The author order and final attribution should be reviewed and agreed with the contributors. **Software authorship does not itself establish copyright ownership**; the MIT licence and any rights in the original code should be confirmed with the relevant rights holders.

## Background reading

- [Data management for bioimaging: no-cost, easy-access tools for Edinburgh](https://libraryblogs.is.ed.ac.uk/datablog/2026/01/13/data-management-for-bioimaging-no-cost-easy-access-tools-for-edinburgh/) — University of Edinburgh Data Blog (13 January 2026). Context for practical bioimaging data management and metadata recording.
