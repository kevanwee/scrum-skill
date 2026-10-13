# Accountabilities and adaptable profiles

Scrum has Product Owner, Scrum Master and Developers accountabilities. Specialisms
are not additional Scrum accountabilities or sub-team hierarchies. AI execution aids
the accountable human; this package does not create autonomous human responsibility.

| Accountability | Decisions and work | AI assistance |
| --- | --- | --- |
| Product Owner | Product Goal, value, backlog order and stakeholder tradeoffs | Draft/refine options; never invent the person's agreement |
| Scrum Master | Team effectiveness, facilitation, coaching and impediment removal | Maintain inspection evidence and coordinate bounded workers |
| Developers | Plan, size, build, verify and adapt the Sprint Backlog | Collaborate through shared quality criteria and small integrated slices |

Start with the smallest useful team. Software projects often use engineering and QA;
add design, security, operations, data/AI or a domain reviewer when relevant. A legal
project may need counsel; a game or research project may need different expertise.
The Product Owner does not have to be a lawyer. Do not install third-party skills,
select a paid model or create accounts merely because a profile mentions a tool.

## Profile contract

For each specialist record: contribution, owned scope, dependencies, acceptance
criteria, evidence/review expectations, handoff path and collaboration boundaries.
Responsibilities may overlap; avoid conflicting writes and unclear integration owners.
The coordinator facilitates scope negotiation rather than assigning an inflexible plan.

- Engineering: just-enough architecture, implementation, contracts, integration and
  meaningful tests; composition/interface polymorphism where it improves replaceability.
- QA: independently derive critical negative/boundary cases, inspect test oracles,
  maintain evidence/traceability and verify CI/release claims.
- Design: user flows, hierarchy, accessibility, responsive behavior and honest product
  claims; follow the project's chosen design system and tools.
- Security: threat/data-flow review proportional to actual boundaries, controls and
  findings with owners; distinguish source-sharing risk from production-release risk.
- Domain reviewer: project-specific substantive judgments and evidence; do not claim
  regulated human sign-off from an agent review.

Use the optional template in assets/role-profile.md for custom specialisms.
