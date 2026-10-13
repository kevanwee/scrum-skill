# scrum-skill

> An experiment in applying Scrum principles with AI teammates. A human remains accountable for product decisions.

A project-neutral skill for **Codex and Claude Code**. Invoke it to create or resume a Scrum workspace, refine a backlog, plan and deliver a bounded slice, inspect outcomes, improve the process and leave a reliable handoff.

The human Product Owner can work in any domain. Engineering, QA, design, security and domain reviewers are selected for the project. Legal counsel, specific models, frontend packages and vendor plugins are **optional**, not built-in requirements.

Version **0.1.0** · MIT · One canonical [`SKILL.md`](skills/scrum-skill/SKILL.md). No bundled MCP server, lifecycle hook, telemetry or automatic cross-project synchronization. The optional workspace helper uses Python 3.10+ and the standard library.

## Start here

Choose **one** installation route to avoid duplicate skill names.

### Codex plugin

```sh
codex plugin marketplace add kevanwee/scrum-skill --ref v0.1.0
codex plugin add scrum-skill@scrum-skills
```

Reload/start a session if needed, then invoke:

```text
$scrum-skill Set up Scrum for this project. I am the Product Owner.
Our goal is a small inventory app. Use engineering, QA and design agents
where available. Create the artifacts and propose the first usable slice.
```

The repo catalog is a distribution source, not an official OpenAI directory listing. Host/plugin availability varies by surface. See [official package/catalog guidance](https://developers.openai.com/plugins/build/plugins).

### Claude Code plugin

```sh
claude plugin marketplace add kevanwee/scrum-skill
claude plugin install scrum-skill@scrum-skills
```

Reload/start a session if needed. Plugin skills use a namespace:

```text
/scrum-skill:scrum-skill Set up Scrum for this project and propose a first Sprint.
```

For local development after cloning, `claude --plugin-dir /path/to/scrum-skill` loads the plugin for that session. See [Claude plugin guidance](https://code.claude.com/docs/en/plugins) for supported surfaces, scopes and trust settings.

### Direct skill folder

Install just `skills/scrum-skill/` if you do not need a plugin catalog. For Codex, ask `$skill-installer` to install that path from this repository at `v0.1.0`, or copy it into your project's `.agents/skills/scrum-skill/`. For Claude Code, copy it into `.claude/skills/scrum-skill/` and invoke `/scrum-skill`. Preserve its scripts, references and assets. Do not overwrite an existing installation without reviewing the change.

Skills-only installation does not register a plugin, hooks or an agent runtime. See [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills). This repo publishes compatible metadata; it does not install anything into your account automatically.

## What you can ask

```text
$scrum-skill Resume from the project's latest handoff and reconcile the actual state.
$scrum-skill Refine these stories, identify evidence gaps and plan the next Sprint.
$scrum-skill Plan and start the next authorized slice; coordinate specialists and verify it.
$scrum-skill Prepare a Sprint Review using actual results and separate unfinished work.
$scrum-skill Run a retrospective and propose a few measurable improvements.
```

Use `/scrum-skill:scrum-skill` for the plugin version in Claude Code. Setup/planning creates artifacts; it does not by itself authorize implementation, pushes, deployment or messages. If your host cannot delegate, the coordinator works sequentially and records that mode.

## Scrum at a glance

Scrum uses transparency, inspection and adaptation to work toward a Product Goal. These diagrams summarize the framework; [source attribution and packaging references](SOURCES.md) distinguish Scrum rules from this package's AI/project conventions. Using only selected practices is **Scrum-informed**, not a claim of full Scrum implementation or certification.

```mermaid
flowchart TB
  Goal["Product Goal"] --> PB["Ordered Product Backlog"]
  PB --> Plan["Sprint Planning: why, what, how"]
  Plan --> SB["Sprint Goal and Sprint Backlog"]
  SB --> Work["Developers build, verify and adapt"]
  Daily["Daily Scrum: inspect Goal progress"] --> Work
  Work --> Quality{"Meets shared Definition of Done?"}
  Quality -->|Yes| Inc["Usable integrated Increment"]
  Quality -->|No: unfinished| PB
  Inc --> Review["Sprint Review: inspect product and adapt backlog"]
  Review --> PB
  Review --> Retro["Retrospective: improve quality and effectiveness"]
  Retro --> Plan
  Inc -.->|When release policy permits| Delivery["Delivery; Review is not a release gate"]
```

One active Sprint, fixed length of one month or less. The team chooses a useful cadence; two weeks is a starting convention. The Developers own their plan and estimates. A timebox ending does not turn unfinished work into a Done Increment.

## Who does what?

```mermaid
flowchart TB
  PO["Human Product Owner: value, Product Goal, backlog order"]
  SM["Scrum Master facilitation: effectiveness and impediments"]
  Dev["Developers: one cross-functional, self-managing team"]
  PO -->|Direction and tradeoffs| Dev
  SM -->|Facilitate, coach and unblock| Dev
  Dev -->|Evidence and feedback| PO
  Profiles["Optional specialisms: engineering, QA, design,<br/>security and domain expertise as needed"]
  Dev --- Profiles
```

AI workers assist these accountabilities; a generated role profile is not a human appointment, real stakeholder participation or regulated professional sign-off. The skill coordinates bounded tasks with file ownership, acceptance evidence and handoffs instead of pretending every agent is an independent employee.

## Artifacts and commitments

```mermaid
flowchart TB
  PB["Product Backlog: ordered work and refinement"] --> PG["Commitment: Product Goal"]
  SB["Sprint Backlog: selected work and adaptable plan"] --> SG["Commitment: Sprint Goal"]
  INC["Increment: usable integrated outcome"] --> DOD["Commitment: Definition of Done"]
  AC["Item acceptance criteria"] -.->|Behavior to verify| INC
  Evidence["Revision-specific evidence"] -.->|Quality to demonstrate| DOD
```

Acceptance criteria describe each item's behavior. The Definition of Done describes shared product quality. CI, architecture, accessibility, security/privacy and domain review are chosen for the actual project. Local tests, mocks and coverage do not establish every integration or human decision.

## Events are different conversations

| Event | Inspect/adapt | Record actual participation or label preparation |
| --- | --- | --- |
| Sprint Planning | Why this Sprint matters, what is feasible, how to deliver | Goal, selected items, capacity/uncertainty and plan |
| Daily Scrum | Progress toward the Goal and the Developers' next plan | Evidence, plan changes and impediments |
| Sprint Review | Product outcome, real stakeholder feedback and backlog order | Done results; unfinished work listed separately |
| Retrospective | Collaboration, tools, quality and assumptions | Owned improvements with observable success measures |

Review is not merely a demo; retrospective is not product acceptance. Async agent notes help prepare events but do not prove a human ceremony occurred. Never fabricate attendance, velocity, passed tests or approval.

## What one invocation sets up

```mermaid
flowchart TB
  Invoke["Invoke skill with project outcome"] --> Inspect["Inspect instructions, repo and existing state"]
  Inspect --> Existing{"Existing Scrum records?"}
  Existing -->|Yes| Resume["Resume and reconcile; preserve decisions"]
  Existing -->|No| Init["Create adaptable local workspace"]
  Resume --> Refine["Refine Goal, team, quality and first slice"]
  Init --> Refine
  Refine --> Scope{"Delivery requested and authorized?"}
  Scope -->|No| Artifacts["Reviewable plan and open questions"]
  Scope -->|Yes| Deliver["Bounded build, verification and integration"]
  Artifacts --> Handoff["Evidence-linked handoff and next action"]
  Deliver --> Handoff
```

The optional helper creates these records, all initially **proposed/preparatory**:

```text
project/
  AGENTS.md                 Preserved; a small marked resume pointer is appended
  CLAUDE.md                 Preserved; the same pointer is appended
  .gitignore                Preserved; .scrum/ ignored by default
  .scrum/
    workspace.json          Skill version and project configuration
    TEAM.md, roles/         Adaptable specialist profiles
    PRODUCT_GOAL.md, PRODUCT_BACKLOG.md, DEFINITION_OF_DONE.md
    DECISIONS.md, IMPEDIMENTS.md, EVIDENCE.md
    sprints/                Forecast, planning, review and retrospective
    handoffs/INITIAL.md, handoffs/LATEST.md
    MASTER_PROMPT.md         Fresh-session resume instructions
```

For a manual setup preview from a clone:

```sh
python skills/scrum-skill/scripts/init_workspace.py --root /path/to/project --name inventory --goal "Staff can track stock changes" --specialists engineering,qa,design --dry-run
```

Run without `--dry-run` only when you intend setup. Use `--specialists none` for a sequential generalist. Existing records are not overwritten; malformed pointer blocks, conflicting project identity and path escapes fail before writes. Choose an explicit `--start-date YYYY-MM-DD` in the project's timezone when dates matter. The helper does not run tests, create a Git repo, push, spawn agents or deploy; the skill guides authorized work afterward.

## Improve it from real projects

```mermaid
flowchart TB
  Observe["Observed project friction"] --> Sanitize["Generalize; keep private facts local"]
  Sanitize --> Repro["Invented minimal reproduction"]
  Repro --> Change["Narrow skill or template change"]
  Change --> Review["Scrum Master or QA review"]
  Review --> Check["Behavior and package checks"]
  Check --> Version["Versioned release"]
  Version --> Adopt["Consumer reviews migration; no silent sync"]
```

Keep one canonical skill under `skills/scrum-skill`. Both host manifests and catalogs point to it; there are no generated copies to drift. A project's domain safeguard or tool choice becomes an optional profile, not a universal rule. See [maintenance guidance](skills/scrum-skill/references/maintenance.md) and [contributing](CONTRIBUTING.md).

## Validation and limits

```sh
python scripts/validate_package.py
python -m unittest discover -s tests -v
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
```

Package tests check manifest paths/versions, references and helper behavior. They do not certify facilitation quality or claim a live installed session on every host. The [evaluation record](EVALUATION.md) describes what was actually exercised. Mermaid README sources are rendered during authoring to catch syntax/layout failures. No supplied PDFs or project-specific backlog content is part of this repo.
