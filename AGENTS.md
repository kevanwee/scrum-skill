# Maintaining scrum-skill

This repository contains a project-neutral Scrum skill and plugin packaging.
Keep one canonical skill under skills/scrum-skill; host manifests must reference it.
No supplied PDFs, restricted course extracts, project backlogs, stakeholder identities,
credentials or private handoffs belong in this public repository.

Make instructions useful to Codex and Claude without requiring host-specific tools,
model names, legal counsel, a particular frontend stack or external services.
Preserve human Product Owner accountability and project-specific authorization.

Run python scripts/validate_package.py and python -m unittest discover -s tests -v.
Validate changed Mermaid diagrams with the renderer before publishing.
Document behavioral validation limits; passing a metadata check is not an end-to-end skill evaluation.
Keep commits scoped and identify agent authors honestly. Scrum Master or QA reviews
and merges PRs after required checks pass; do not bypass protected main.
Learnings from real projects become anonymized regression cases and reviewable changes,
not automatic cross-repository synchronization or confidential prompt uploads.
