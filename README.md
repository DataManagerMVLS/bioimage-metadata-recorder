# Bioimage Metadata Recorder
**[▶ LAUNCH THE WEB APPLICATION](https://datamanagermvls.github.io/bioimage-metadata-recorder/)** · [View the HTML source](index.html)

> **Hackathon prototype.** The browser link uses GitHub Pages; deployment and full functionality have not yet been independently verified. If the link is unavailable, download `index.html` and open it locally in a browser. Offline operation and exports still require testing. Records may be held in browser storage: export backups regularly. No direct BioImage Archive submission is provided.


Prototype for recording REMBI-aligned light microscopy acquisition and image analysis metadata.

Use the prominent launch link above to try the prototype, or open the local `index.html` file.

See `docs/hackathon-plan.md` for the development plan and [GitHub issues](https://github.com/DataManagerMVLS/bioimage-metadata-recorder/issues) for priorities, especially [#12: effortless researcher-led metadata capture and PI buy-in](https://github.com/DataManagerMVLS/bioimage-metadata-recorder/issues/12).

## Collaboration and branch protection

The repository is public; anyone can browse it, while write access requires a collaborator invitation. Develop on feature branches and open pull requests into `main`. A `Protect main` ruleset has been configured to require pull requests, preventing direct README updates. Recommended settings include blocking force pushes and deletion; verify the actual rules in [repository settings](https://github.com/DataManagerMVLS/bioimage-metadata-recorder/settings/rules). For the hackathon, keep required approvals at zero until collaborators can review, and leave Copilot-specific additional approvals off. Add required CI status checks once the check name and passing state are verified.

The draft BioImage Archive file-list export is not a dataset submission or upload. Backend tests: `python -m pytest -q tests/test_backend.py`.

A provisional Flask backend (`app.py`) is included, but the original GitLab `app.py` still needs to be obtained and compared. This repository was recreated because the original GitLab repository was inaccessible; it was not migrated. The repository is public, but no current open-source licence is offered pending agreement on copyright ownership and reuse permissions with the original contributors and relevant institutions. Earlier versions included an MIT licence; removing it does not necessarily revoke previously granted permissions.

## Project origins, authorship and acknowledgements

This GitHub repository is a reconstruction and continuation of the original Bioimage Metadata Recorder project, **not a migration from GitLab**. Access to the original GitLab repository was unavailable during hackathon preparation, and the provisional Flask `app.py` still needs to be compared with the original implementation.

The following contributors should be explicitly recognised for their roles:

- **Ann Wheeler** (University of Edinburgh) — original project concept, scientific and microscopy metadata requirements, methodology and project leadership.
- **Ewan McDowall** (University of Edinburgh) — **original application code author and project IT support**.
- **Stephen Fox** (University of Glasgow) — research data management, FAIR alignment, reconstruction of the GitHub project, documentation and further development.

See [CITATION.cff](CITATION.cff) for the software citation. The author order and final attribution should be reviewed and agreed with the contributors. **Software authorship does not itself establish copyright ownership**; rights in the original code and any future licence should be confirmed with the relevant rights holders.

## Background reading

- [Data management for bioimaging: no-cost, easy-access tools for Edinburgh](https://libraryblogs.is.ed.ac.uk/datablog/2026/01/13/data-management-for-bioimaging-no-cost-easy-access-tools-for-edinburgh/) — University of Edinburgh Data Blog (13 January 2026). Context for practical bioimaging data management and metadata recording.
