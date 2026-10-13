# Evaluation — 0.1.0

These checks establish a limited, observable baseline. They do not certify Scrum
facilitation or demonstrate a live installed conversation on every host.

## Package and helper

- Offline consistency validator: canonical skill, manifest versions, catalog paths,
  Markdown references and publication boundaries pass.
- Codex skill metadata validator: pass.
- Claude Code native plugin and marketplace validators: pass without warnings.
- Codex native catalog discovery: recognizes the local package at version 0.1.0,
  using temporary process configuration; no user settings or installed plugins changed.
- Eighteen standard-library regression tests cover preservation, idempotence,
  conflicting identity, dry runs, custom roles, malformed pointer blocks, path
  collisions, symlink escape, date limits and repair from existing project decisions.
  Windows passes seventeen and skips the symlink test when privilege is unavailable.
  [Linux CI](https://github.com/kevanwee/scrum-skill/actions/runs/38339579380)
  passed all eighteen tests on Python 3.10 and 3.14, including symlink behavior.
- Five README Mermaid diagrams rendered with Mermaid CLI 11.12.0 and inspected
  for syntax, readable labels and layout.
- No paid model calls, telemetry, external project messages or production deployment.

## Independent behavioral exercise

An independent agent received the skill and a fresh, invented neighborhood garden
planning request. The human was the Product Owner; scope allowed discovery and
planning only. The agent created a substantive proposal, used community research
and planning quality roles instead of mandated software or legal roles, and recorded
unresolved human decisions without claiming an actual ceremony or accepted Increment.

A later simulated instruction changed the cadence to weekly and added horticulture.
The agent resumed, reconciled configuration and summaries, added the role and
preserved existing decisions. Nine evidence checks passed, including preserved
record hashes and explicit preparation status. Private evaluation workspace paths
and raw session artifacts are not distributed.

A subsequent independent QA package review found no blocking defect. Six additional
repair checks confirmed that stale setup inputs do not replace recorded decisions,
role profiles, cadence or manifest bytes, and that repeated repair is a no-op.

## Limits and follow-up

- This is one independent setup/resume scenario, not broad evidence for every domain
  or long-running delivery team. Implementation, integration and Sprint Review behavior
  need additional outcome-based scenarios as the skill evolves.
- The helper creates a scaffold. An agent still must tailor stories, quality standards
  and plans to the project. Resume requires reconciling stale summaries with decisions.
- Plugin metadata validation and discovery do not establish full installed runtime
  activation across Codex and Claude versions or surfaces.
- Source references were reviewed as learning material; supplied PDFs and restricted
  course extracts are not redistributed or covered by this package's MIT license.
