# Engineering and delivery evidence

Use this for software projects, not as compulsory machinery for every Scrum use case.

## Architecture and collaboration

Model just enough to communicate a risky boundary or decision. Use editable C4
context/container diagrams, then component/class/sequence views where they add value.
Keep implemented and proposed elements distinct and link decisions to code or an ADR.
Composition and protocol/interface polymorphism can make collaborators replaceable;
inheritance is not required. Isomorphism is a structure-preserving correspondence,
not a generic OOP feature to add to satisfy a checklist.

Integrate small scoped changes frequently. Use explicit file ownership in a shared
checkout, serialize index/branch/stash operations and inspect staged paths. A stash
is local parking, not remote backup. Do not stash ignored private records with --all.
Worktrees help isolate parallel branches. Review the integrated result even when Git
can merge text without conflicts. Keep reviewer and revision evidence honest.

## Tests and CI

Derive assertions from acceptance outcomes, including meaningful negative and boundary
cases. Ask which plausible wrong implementation each test rejects. Control state/time;
use doubles at collaborators, not to replace the behavior being tested. Mocks agreeing
with themselves, generated counts and coverage alone do not prove the requirement.
Add contract/real-infrastructure evidence when database dialects or provider contracts
matter. Default tests should not accidentally call paid or live services.

Record suite, environment, revision and limitations. Local success is not hosted CI,
a skipped scanner is not a pass, and automated accessibility is not full certification.
Fix actual failures; do not weaken assertions or quarantine without visible ownership
and gate impact. Apply the project's required lint/types/build/security gates.

## Delivery and release

CI integrates/checks source; continuous delivery maintains deployable versions;
automatic production deployment is a separate choice. A green workflow does not
establish a staging/production deployment. If deploying, promote the same identified
artifact, record configuration/health evidence and rehearse rollback or forward recovery.
Source-sharing, Done, product acceptance, deployment and release have separate evidence.
Apply domain/privacy/security review to actual affected boundaries, not hypothetical ones.
