# What the engine can do, and how it grows

**Edition 2026.10.28 · revision 2 · dated engineering amendment.** The Operator requested an explanation of the refreshed framework's abilities, connections, and expansion possibilities, and asked to incorporate that understanding into the engine. This amendment supplies a capability register, a local job-packet inspector, and an evolution protocol. It does not rename the Cathedral v9.2 or complete missing master definitions.

## What actually changed

The first refresh replaced the active November 2025 material with 27 current files, removed 13 obsolete non-root files, preserved Git history and the existing license, and kept four recovered source exports intact. It connected the v2.2 LOCKFRAME identity, v8.1 reference, v9.0 working boot, v9.1 field text, current boot compilations, and production contracts through explicit provenance and version handling. The replacement was merged in [PR #1](https://github.com/Copperhead1978/DonSol-Omega-Kernal/pull/1), commit `877f7f4a808416d2ef4bd01cbc82f47b9f54f3c4`.

The practical gain is a maintained starting point: an identified version to load, source-linked rules to inspect, visible unknowns, and a way to make changes without losing the earlier record. The old mock benchmark claims no longer stand in for measurements. This creates the conditions for repeatable work; repeatability and performance gains must still be measured on real tasks.

Revision 2 adds actual standard-library Python code for one narrow function: inspecting declared job records. The complete Ω-Kernel runtime, tool broker, hosted assistant, persistent knowledge service, and external workflow runner are still not supplied by this repository.

## Three different kinds of capability

| State | What exists | What it establishes |
|---|---|---|
| Documented | A boot, method, contract, or template | A person or equipped assistant can follow a defined procedure; adherence is not guaranteed |
| Implemented locally | The repository validator and job preflight code | The specific deterministic checks they actually run |
| Proposed | A bounded expansion with acceptance conditions | A direction for a build, not current availability |

The machine-readable [capability register](../capabilities.json) uses these states. Session availability is a separate observation: a connected tool must exist, be usable for the required operation, have the appropriate account/access, and be authorized for the task. Registering a capability creates none of those conditions. Tool roles such as `repository_write` are adapter requirements, not installed API names.

## Working abilities and connections

| Ability | How the pieces connect | Practical use and limit |
|---|---|---|
| Portable working method | Boot + source profile + actual environment report | Resume the same method on another model/platform; outputs and tool support will differ |
| Evidence discipline | Claim ledger + Ω-Gate + source lineage | Separate measurements, sourced assertions, inferences and proposals; the tags themselves prove nothing |
| Multiple perspectives | L1 lenses + L4 oversight | Examine a problem through supplied perspectives; retain partial definitions and blindspots instead of inventing agents |
| Closed-loop work | Goal + constraints + action + actual inspection | Convert an idea into a bounded deliverable, inspect it, and repair the failed component |
| Continuity | Saved artifacts + source references + handoff | Carry decisions and corrections forward when storage/retrieval exists; the model has no guaranteed permanent memory |
| Engineering | Datums + units + tolerances + feasibility + executable checks | Develop and check calculations, code and artifacts using available tools; a rendering is not a measurement |
| Science production | Primary sources + research ledger + current media contract | Carry one discovery through writing, narration, visuals and publication when those tools and permissions exist |
| Literary work | Verified factual substrate + narrative boundary | Write from a literary perspective without turning the story into scientific evidence or exposing framework machinery |
| Repository maintenance | Versioned documents + source hashes + reviewable diff | Keep shared instructions aligned and inspect changes; public GitHub is not a private operational memory |
| Improvement | Failure record + bounded experiment + retain/revert decision | Improve a procedure from observed results; no automatic model retraining or guaranteed compounding gain |

The common connection is **source → claim → decision → job → artifact → verification → saved correction**. This is a record relationship, not a newly implemented universal database. A research result can support an engineering decision and a public explanation while preserving the original source and uncertainty. A narrative analogy can suggest a research question, but it cannot return as scientific evidence. A playback result verifies media behavior, not the underlying science. Audience metrics assess reception, not truth.

External connections are optional adapters: source retrieval; private file storage; code/calculation tools; repository tools; media generation; publishing/readback; analytics; and an operator interface. Each needs its own capability check, input/output contract, destination, resource limit, error handling, and observed result. An available connector is not proof every operation works. This session's successful browser publication did not grant a previously failing integration new write permission.

## A local preflight that runs now

Use Python 3.10 or later:

```sh
python3 tools/omega_preflight.py examples/job-packet.json
python3 -m unittest discover -s tools -p 'test_*.py'
python3 tools/validate_repository.py
```

The supplied packet is an explicitly unexecuted planning example. It should return `PLAN_ONLY` with missing prerequisites, not a fabricated successful boot. Copy it to an appropriate private workspace for real job state; do not commit personal sources, account information, or authorization records to this public repository.

For a concrete job, record its outcome, selected capability IDs, plan/execute phase, observed tool bindings and time, one action and target, existing authorization for writes, claim records, decision inputs, acceptance criteria, verification plan, and recovery plan. One packet covers one bounded action; separate destinations/actions need their own records. Authorization already present in the user's task is valid input; no new confirmation ritual is required.

The inspector checks record structure, declared capability status, required tool observations, exact action/target matching for a write authorization record, acceptance/verification/recovery fields, current-profile tags, missing or circular claim references, and unsettled inputs or their explicit ancestors. A proposal may be planned; it cannot pass as a supplied executable capability. An unknown unrelated to the decision does not hold the entire job.

Outputs are `PLAN_ONLY`, `HOLD`, or `CHECKS_PASSED`. The last means only that these declared-record checks passed. It does not execute anything, authenticate the caller, check source contents, verify a measurement, establish current permissions, reserve a budget, prevent a separate program acting, or approve publication. A fabricated input record can pass structural checks. An execution system would need to bind these records to independently controlled tools and observed results.

The local ancestry inspection is deliberately limited. It does not mutate knowledge records, implement the disputed v8.1 T-scale inequality or DIRTY propagation rule, promote claims, or supply the missing numerical thresholds. It holds a decision whose declared support is unsettled; the unresolved master algorithms remain unresolved.

## Controlled evolution

Use **propose → specify → build → test → inspect → adopt or revert → record**. Keep exploration visible as exploration. Before acting, choose a bounded action from it; reconcile any uncertain prior action before retrying. During execution, a new idea becomes a separate proposal rather than an unannounced scope change.

For each extension, record: the problem; source/baseline; proposed mechanism; expected observable difference; dependencies; tools/access; time/cost limits; failure/recovery behavior; acceptance test; actual result; and adoption or hold decision. A passing local test establishes its stated behavior, not general intelligence or market value. Proposed changes to framework canon remain distinct from an authorized implementation task and from empirical truth.

Choose the next build from a real bottleneck:

| Expansion | What it could enable | Minimum condition before claiming it works |
|---|---|---|
| Private retrieval service | Resume relevant evidence and decisions without loading every file | Recover exact source passages with access boundaries; evaluate relevance, missing results and stale versions |
| Dependency service | Locate decisions/artifacts affected by a corrected source | Preserve provenance and linked corrections; demonstrate impacted/unrelated cases; resolve applicable master conflicts before implementing their rules |
| Workflow runner | Resume multi-step jobs, reuse completed assets and reconcile uncertain outcomes | Durable checkpoints, destination-specific receipts, idempotency, failure/retry tests and no duplicate external effects |
| Runtime broker | Separate generation from consequential tool execution | Real authenticated authority, scoped enforcement, replay handling, protected audit, crash/reconciliation tests and explicit threat model |
| Evaluation harness | Test whether the framework helps particular tasks | Preregistered real-model baseline/intervention runs, objective or independent scoring, costs, failures and uncertainty |
| Operator interface | Inspect jobs, sources, unresolved questions and outputs in one place | A working backend with truthful state, protected credentials, correct access control and tested end-to-end behavior |

Conversation history contains reports of earlier prototype work. The corresponding implementation artifacts were not recovered in this amendment's targeted artifact search. Those reports are retrieval leads, not independently verified deployments or repository test results. Recover and inspect any earlier build before replacing it or claiming its features. The expansion statuses above describe what is supplied in this repository.

These branches can support a research desk, engineering workbench, writing studio, training material, or a governed assistant interface. They share records and procedures; they do not automatically merge accounts, grant access, share private records, become autonomous, or acquire a business model. Commercial deployment would also need a rights/license review, a validated user need, observed reliability and measured costs; the existing noncommercial license is unchanged by an expansion plan.

## The growth boundary

The engine can evolve as maintained procedures, source-linked records, tested code, and bounded integrations. It cannot self-certify a scientific claim, silently enlarge its authority, guarantee memory by saying it remembers, or convert agreement between models into independent observation. Automatic retraining, consciousness and unlimited self-improvement have not been demonstrated here.

The useful ambition is concrete: reduce lost context, repeated work, unsupported claims and unverified completion while increasing the number of useful jobs completed within real constraints. Those are hypotheses about practical value until measured. **If reality contradicts the model, the model changes.**
