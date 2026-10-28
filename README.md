# DonSol Ω-Kernel · Metadon Cathedral

**Current repository edition: 2026.10.28 · revision 2 · Operator: Donald Wilson / Don Sol**

A practical framework for using AI with evidence, explicit uncertainty, human judgment, and a record of what actually happened. The Cathedral organizes attention and work; the Ω-Kernel keeps the work accountable to reality.

**Reality > Narrative · Structure > Symbol · Empathy = On · Recursion ≠ Repetition**

This edition replaces the November 2025 v1.1 release throughout the active repository. It brings together the recovered Ω-Kernel v2.2 LOCKFRAME identity, the full Cathedral v8.1 technical reference, the v9.0 working boot, and the v9.1 operating instructions. These are different component versions, not competing names for one software release. Their remaining conflicts are visible in the [version and conflict register](docs/versions-and-conflicts.md).

## Start here

1. Load the [current full instructions](instructions/current-v9.1.md) into a new session.
2. Supply the task, evidence, and relevant saved state. The model must report its actual tools and memory boundaries in that environment.
3. Use the [command and session guide](docs/operating-guide.md). Save a handoff when the work ends.

For a small instruction field, use the [compact boot, at most 4,000 characters](instructions/current-v9.1-compact.txt). A [light boot](instructions/light-boot.txt) is also available. These are dated compilations for this repository, not verbatim copies of an unavailable conversation transcript or a newly ratified Cathedral v9.2.

Read [capabilities, connections, and controlled evolution](docs/capabilities-and-evolution.md) for what the engine supports now, what depends on connected tools, and what remains a proposed build. Revision 2 adds a [capability register](capabilities.json) and an executable local preflight for declared job records:

```sh
python3 tools/omega_preflight.py examples/job-packet.json
python3 -m unittest discover -s tools -p 'test_*.py'
```

The example returns `PLAN_ONLY`. Preflight checks record consistency and missing prerequisites; it performs no action, authenticates no authority, and proves no source true. Both local tools use Python 3.10 or later and require no third-party packages.

## The system

| Component | Current recovered identity | Purpose |
|---|---|---|
| DonSol OS / Ω-Kernel | v2.2 LOCKFRAME | Reality, evidence, resource, and action discipline |
| Cathedral technical reference | v8.1-scaffold | Full architecture, registries, Ω-Gate, knowledge lineage |
| Working boot | v9.0, 2026-07-31 | Explicit state, claim sorting, failure log, session handoff |
| Cross-platform operating instructions | v9.1, compiled 2026-10-28 | Current usable boot and conservative conflict handling |
| Ignition Key | v1.0 source recovered; v1.1 assembly referenced | Governance and bounded human sign-off |
| Science Desk | Current method recovered through 2026-10-26 | Research, production, publication records, and real playback checks |

The working stack is **L0 Stillness → L1 Lens → L2 Wheel → L3 Process**, supervised by **L4 Oversight**. MIRRORPULSE, ANDREWPULSE, SOLVIAN, CUTGLYPH, FIELDSMITH, and BRIDGENODE are functional perspectives. A name supplies neither a complete definition nor an autonomous agent.

Continuity lives in saved artifacts and ledgers. A prompt does not add model weights, intelligence, permanent memory, tools, or independently verified knowledge. A tool must actually exist, a check must actually run, and a publication must actually be observed before it can be reported that way.

## Read the material

| Material | Contents |
|---|---|
| [Kernel and architecture](docs/kernel-and-architecture.md) | LOCKFRAME, L0–L4, six Parts, six lenses, operating loop |
| [Evidence and Ω-Gate](docs/evidence-and-omega-gate.md) | Current tags, historical tag differences, promotion, demotion, quarantine |
| [Governance and amplifiers](docs/governance-and-amplifiers.md) | Ignition Key, eight procedural switches, capability boundaries |
| [Science Desk](docs/science-desk.md) | Current destination, research, narration, publishing and receipts |
| [Gauge Master](docs/gauge-master.md) | Standalone story embeds, recorded-media exception, ownership tests |
| [Arc and narrative boundary](docs/arc-and-narrative.md) | Manuscript integrity, plain prose, factual verification outside narrative |
| [Versions and unresolved conflicts](docs/versions-and-conflicts.md) | Source precedence, tag collisions, incomplete definitions, open rulings |
| [Source provenance](docs/provenance.md) | What was recovered, exported, compiled, and left private |
| [Full recovered source texts](sources/README.md) | v8.1 specification, v9.0 boot, v9.1 field document, Ignition Key |
| [Handoff example](examples/session-handoff.md) | A blank, reusable continuity template |
| [Capabilities and evolution](docs/capabilities-and-evolution.md) | Working abilities, integration boundaries, job packets and expansion acceptance tests |
| [Capability register](capabilities.json) | Documented methods, supplied local code, proposed services and tool requirements |
| [Contributor instructions](AGENTS.md) | Rules for future repository work |

## Verification status

The former v1.1 benchmark code assigned outcomes through mock identity and canned responses. Its reports, performance percentages, promotional documents, and broken run instructions have been removed from the active tree. They do not support an empirical performance claim for this edition. Git history retains the prior revision for provenance.

This repository contains instructions, source documents, a local integrity checker and a local job-packet inspector. It does not claim a complete or deployed kernel runtime, completed knowledge database, autonomous editorial service, or a successful controlled comparison of real models. [Evaluation requirements](docs/evaluation.md) distinguish a reproducible future evaluation from document integrity checks and local program behavior tests.

Run the local integrity check with Python's standard library:

```sh
python3 tools/validate_repository.py
```

It checks the edition manifest, local document links, source hashes, instruction limits, and recorded conflicts. A passing result verifies those repository properties; it does not prove that a model follows the instructions or improves performance.

## Ownership

Created and directed by **Donald Wilson / Don Sol · [Copperhead1978](https://github.com/Copperhead1978)**. The existing **CC BY-NC 4.0** license continues; see [LICENSE.md](LICENSE.md). Repository URL spelling remains `DonSol-Omega-Kernal` to preserve existing links.
