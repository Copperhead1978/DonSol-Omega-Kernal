# J58 Operating Lenses — SHARED proposal

**Status: [P] PROPOSED · 2026-11-22 · draft 2 · not adopted or activated.**

Origin: the architectural sketch supplied by the Operator and attributed to
Gemini Hydrogen. Seat 2 prepared this specification against repository main
`447ea115eac26e1684a8b575dd73499c095c9209`. It records a proposal for the
table; it contains no acceptance filing from another seat and no Bell ruling.

Draft 2 incorporates the Operator's additional instruction to include Carl Jung
and the wider scientific and great-thinker reference pool. The companion
[reference-author catalog](08-reference-author-catalog.md) is open to expansion;
it distinguishes available source material from names awaiting retrieval.

## Purpose and scope

Choose the amount of verification and synthesis a task needs, while keeping
evidence, review order, resources, and authority visible. The proposed practical
benefit is fewer unsupported claims and less repeated checking of unchanged
inputs. That benefit is unmeasured.

The J58 names are workflow metaphors. This document supplies no aircraft-engine
technical specification. The historical names attached to the four lenses are
mnemonics for the procedures defined here, not claims that those people endorsed
these procedures or shared one philosophy.

These are auxiliary L1 checklists. The six adopted code-name lenses and the
L0–L4 stack retain their definitions. See the adopted
[lens definitions amendment](../docs/lens-definitions-amendment-2026-10-29.md),
[current v9.1 instructions](../instructions/current-v9.1.md), and
[conflict register](../docs/versions-and-conflicts.md).

This draft changes no executable preflight rule, job packet, compact boot, source
export, protected-domain rule, schedule, spending limit, or publication gate.
The compact boot at this baseline contains 3,971 characters / 3,999 UTF-8 bytes.
The proposed implementation is specified below for a separate reviewed change.

## The five optional lenses and the wider author pool

Use only the lenses that answer the task's actual question. Stack them when
needed; record a concrete finding from each selected lens. A lens name alone
does not count as a review.

| Stable ID | Lens / mnemonic lineage | Question and minimum output | Mount / dismount | Proposed lead |
|---|---|---|---|---|
| `ATHENS` | Athens — Socrates and Plato | What premise is untested? Is the decision supported by craft and evidence? Name the premise, a counterexample, and the resulting correction or unresolved question. | Mount for framing, persuasion, or disputed claims; dismount when a specific premise can be tested. Blindspot: endless questioning without a decision. | Seat 3 |
| `FIRST_PRINCIPLES` | First Principles — Einstein and Tesla | What mechanism, units, boundary conditions, and conserved quantities apply? Give a dimensional or mechanism check and identify where the analogy stops. | Mount for technical synthesis or scale changes; dismount when calculation needs missing measurements. Blindspot: an elegant simplified model mistaken for the actual machine. | Seats 3 and 2 |
| `BENCH_PROOF` | Bench Proof — Franklin and Edison | What did the instrument or source actually show? Name the cheapest discriminating test, its acceptance condition, and its actual result if run. | Mount for uncertain behavior and build claims; dismount when the result is measured or the test is infeasible. Blindspot: a convenient demonstration treated as general proof. | Seat 1; Seat 5 reviews the Chair's claims |
| `ENDURANCE_FIXTURE` | Endurance and Fixture — Ford, Ford II, Shelby, and Miles | Can the result be repeated under the intended load? Name the failure condition, reuse/recovery plan, and observed repeatability if tested. | Mount for repeated production and handoffs; dismount when the fixture is bounded and inspectable. Blindspot: process overhead or repeated output that preserves the same error. | Seat 1; the Bell holds decisions |
| `JUNG_PSYCHOLOGY` | Psychological Interpretation — Carl Gustav Jung | What assumption, projection, or symbolic reading might shape this interpretation? Separate the observed words or artifact from proposed meanings; give an alternative reading and a question that could distinguish them. | Mount for requested reflection, human meaning, or narrative design; dismount when interpretation turns into certainty about a person or a claim about physical reality. Blindspot: making a compelling symbolic story explain everything. | Seat 2 for narrative; Seat 3 checks attributed claims |

These proposed leads do not create rank or displace the Charter's lanes. In
particular, Seat 5 grades the Chair's completed reconciliation; co-producing it
does not replace that review. Cross-model agreement remains distinct from the
independent source, proof, and dependency check required by Block 2.

The Jung procedure is an authored [P] adaptation. His original writings are
references, with theory and interpretation labeled as such; using the lens does
not diagnose someone, establish hidden motives, or turn archetypes into measured
physical mechanisms. Full scope, source leads, and the mounting method are in
the companion catalog. Other authors can inform any relevant lens. No fixed
author list is a ceiling, and no task must rehearse every author to proceed.

## Three regimes, one authority boundary

`FLIGHT_REGIME` describes handling of evidence and synthesis. It does not grant
permission, authenticate a seat, select a new evidence profile, or change rank.

| Regime | Entry condition | Work permitted | Exit / return condition |
|---|---|---|---|
| `TURBOJET` | Default for a new task, an unverified load-bearing claim, changed inputs, or defect triage. Protected-domain actions retain all existing gates. | Gather and check sources in sequence; measure; name UNKNOWNs; make visibly tagged [I]/[P] suggestions. No unsupported inference is promoted to fact. | Create a scoped baseline receipt only after the required evidence checks pass. |
| `INLET_SPIKE` | A current `TURBOJET` baseline exists for the exact input scope. | Seat 3 and the Chair record the factual boundary and the separate hypothesis space. Preserve UNKNOWNs and review the dependencies. | A pinned boundary record is required before cruise. A failed check returns the affected work to verification. |
| `TURBORAMJET` | The baseline and boundary record are available, current, digest-matched, and cover the exact job scope. | Draft, calculate, explain, and produce within that boundary. Use the selected lenses and existing resource limits. | A new factual premise, source/specification change, contradiction, failed sample, or changed action/target invalidates the affected scope. Return it to `TURBOJET`; re-lock before resuming cruise. |

Verification is proportional to consequence under Block 2. An unrelated UNKNOWN
does not stall the job. A load-bearing UNKNOWN cannot become settled input
because a deadline or a regime label changed. Inferences remain allowed and
identified in every regime; the sketch's phrase "zero extrapolation" is replaced
with the narrower rule against unsupported factual promotion.

Every regime preserves the
[Charter](02-council-flow-charter.md): Raw → Draft → Inspection → Editing →
Review → Bell → Publish + Verify. Different matters may occupy different stages
in parallel; each matter retains its stage order and one writer per output.
Contributions must respect those dependencies. A defect is routed back one named
stage as the Charter requires; its evidence regime can return to `TURBOJET`
without skipping workflow stages.

The sketch's instruction for all five seats to work simultaneously on one
matter cannot override that locked order. Any proposed change to the Charter
would need a separate ruling. Seat availability is observed per run; MISSING,
manual relay, quotas, and credit limits are reported as they stand.

## Proposed packet contract

**Future contract only.** The existing
[example packet](../examples/job-packet.json) is schema version 1. The existing
[preflight](../tools/omega_preflight.py) checks that version and ignores unknown
top-level fields. Adding `FLIGHT_REGIME` to a version-1 packet therefore supplies
no enforcement. At the inspected baseline, the planning example with an added
`TURBORAMJET` field still returned `PLAN_ONLY` without a flight-specific blocker.

Use packet **schema version 2** for this extension. An old inspector will reject
that version rather than silently ignore the new contract. The capability
registry remains version 1. After adoption, a version-2 adapter must validate the
extension below and then run all existing version-1 base-record checks with only
the packet's version normalized to 1 for that call. It must combine blockers;
passing the overlay never bypasses the base checks.

Plain version-1 packets retain existing behavior. The future inspector must
reject a version-1 packet containing either reserved extension field
`FLIGHT_REGIME` or `j58`, so ignored flight controls cannot masquerade as checked
controls. `examples/job-packet.json` remains the legacy planning example; any
future version-2 example must be a separately named, clearly unexecuted fixture.

The exact proposed overlay is JSON Schema 2020-12. Top-level extra properties
belong to the existing base packet; only the extension object is closed.
Every referenced path is relative to the job's explicit workspace root. The
future inspector must reject traversal, absolute paths, and symlinks that resolve
outside that root; it performs no remote fetches.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Proposed J58 packet v2 overlay",
  "type": "object",
  "required": ["schema_version", "FLIGHT_REGIME", "j58"],
  "properties": {
    "schema_version": {"const": 2},
    "FLIGHT_REGIME": {"enum": ["TURBOJET", "INLET_SPIKE", "TURBORAMJET"]},
    "j58": {
      "type": "object",
      "additionalProperties": false,
      "required": ["lenses", "reference_authors", "input_artifacts", "baseline", "transition"],
      "properties": {
        "lenses": {
          "type": "array", "uniqueItems": true,
          "items": {"enum": ["ATHENS", "FIRST_PRINCIPLES", "BENCH_PROOF", "ENDURANCE_FIXTURE", "JUNG_PSYCHOLOGY"]}
        },
        "reference_authors": {
          "type": "array",
          "items": {
            "type": "object", "additionalProperties": false,
            "required": ["author_id", "sources"],
            "properties": {
              "author_id": {"type": "string", "pattern": "^[A-Z][A-Z0-9_]*$"},
              "sources": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/file_ref"}}
            }
          }
        },
        "input_artifacts": {"type": "array", "items": {"$ref": "#/$defs/file_ref"}},
        "baseline": {"anyOf": [{"type": "null"}, {"$ref": "#/$defs/file_ref"}]},
        "transition": {"anyOf": [{"type": "null"}, {"$ref": "#/$defs/file_ref"}]}
      }
    }
  },
  "allOf": [
    {
      "if": {"properties": {"FLIGHT_REGIME": {"enum": ["INLET_SPIKE", "TURBORAMJET"]}}},
      "then": {"properties": {"j58": {"properties": {"baseline": {"$ref": "#/$defs/file_ref"}}}}}
    },
    {
      "if": {"properties": {"FLIGHT_REGIME": {"const": "TURBORAMJET"}}},
      "then": {"properties": {"j58": {"properties": {"transition": {"$ref": "#/$defs/file_ref"}}}}}
    }
  ],
  "$defs": {
    "file_ref": {
      "type": "object", "additionalProperties": false,
      "required": ["path", "sha256"],
      "properties": {
        "path": {"type": "string", "pattern": "\\S"},
        "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "sync_id": {"type": "string", "pattern": "\\S"}
      }
    }
  }
}
```

A `sync_id` is an optional lookup label. Neither that label nor a well-formed
digest substitutes for available bytes, coverage, actual source review, or
authority. References are always pinned to the SHA-256 of their exact file bytes.
Reject duplicate input-artifact paths and differing records for the same path.
Snapshots of all load-bearing source material and independent proof records must
be included among the inputs; a URL string alone is insufficient for byte checks.
Each mounted author's `sources` must likewise be present among `input_artifacts`
with matching paths and digests. Author IDs are unique within a packet; the
catalog may grow without a schema edit. Each new ID must resolve to a named
author, an inspected work/passage, a task-specific question, and a limit recorded
in the working record. A name in the catalog alone is not a mounted reference.
An empty `reference_authors` array is valid when no author reference is used.

### Scope digest

Build a JSON object with exactly these keys, preserving array order:

- `job_id`, `goal`, `capability_ids`, `action`, `claims`, `decision_inputs`,
  `acceptance_criteria`, `verification_plan`: copy the corresponding base fields.
- `recovery_plan`: copy it if present, otherwise use JSON `null`.
- `input_artifacts`: copy `j58.input_artifacts`.
- `reference_authors`: copy `j58.reference_authors`.

Reject duplicate JSON object keys and non-finite numbers in all input records.
Serialize this object with Python's
`json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)`;
encode as UTF-8 with no trailing newline, then compute SHA-256. This named
serialization profile, not a claim of universal JSON canonicalization, defines
`scope_sha256`. Missing required base fields fail validation before hashing.

`phase`, environment/tool observations, and authorization are deliberately
outside this evidence digest: the existing base checks must re-evaluate their
current declarations for every requested action. A cached evidence check never
supplies permission. A changed source, claim, action/target, criterion, or listed
input digest changes the scope and requires new evidence and boundary records.

### Baseline and boundary records

The following separate JSON Schema defines the two pinned record types. A
`file_ref` has the same exact shape as above. These files belong in the job's
appropriate workspace; real receipts and private evidence do not belong in this
public repository.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Proposed J58 evidence records v1",
  "oneOf": [{"$ref": "#/$defs/baseline"}, {"$ref": "#/$defs/transition"}],
  "$defs": {
    "text": {"type": "string", "pattern": "\\S"},
    "digest": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "file_ref": {
      "type": "object", "additionalProperties": false,
      "required": ["path", "sha256"],
      "properties": {
        "path": {"$ref": "#/$defs/text"},
        "sha256": {"$ref": "#/$defs/digest"},
        "sync_id": {"$ref": "#/$defs/text"}
      }
    },
    "claim_check": {
      "type": "object", "additionalProperties": false,
      "required": ["claim_id", "source", "independent_proof", "dependency_check", "checked_by", "checked_at", "result"],
      "properties": {
        "claim_id": {"$ref": "#/$defs/text"},
        "source": {"$ref": "#/$defs/file_ref"},
        "independent_proof": {"$ref": "#/$defs/file_ref"},
        "dependency_check": {"$ref": "#/$defs/file_ref"},
        "checked_by": {"$ref": "#/$defs/text"},
        "checked_at": {"type": "string", "format": "date-time"},
        "result": {"enum": ["passed", "hold"]}
      }
    },
    "baseline": {
      "type": "object", "additionalProperties": false,
      "required": ["schema_version", "record_type", "baseline_id", "job_id", "FLIGHT_REGIME", "scope_sha256", "claim_checks", "recheck_on", "result"],
      "properties": {
        "schema_version": {"const": 1},
        "record_type": {"const": "TURBOJET_BASELINE"},
        "baseline_id": {"$ref": "#/$defs/text"},
        "job_id": {"$ref": "#/$defs/text"},
        "FLIGHT_REGIME": {"const": "TURBOJET"},
        "scope_sha256": {"$ref": "#/$defs/digest"},
        "claim_checks": {"type": "array", "items": {"$ref": "#/$defs/claim_check"}},
        "recheck_on": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/text"}},
        "result": {"enum": ["passed", "hold"]}
      }
    },
    "transition": {
      "type": "object", "additionalProperties": false,
      "required": ["schema_version", "record_type", "job_id", "scope_sha256", "baseline_sha256", "factual_claim_ids", "hypothesis_claim_ids", "auditor_filing", "chair_filing", "result"],
      "properties": {
        "schema_version": {"const": 1},
        "record_type": {"const": "INLET_SPIKE_LOCK"},
        "job_id": {"$ref": "#/$defs/text"},
        "scope_sha256": {"$ref": "#/$defs/digest"},
        "baseline_sha256": {"$ref": "#/$defs/digest"},
        "factual_claim_ids": {"type": "array", "uniqueItems": true, "items": {"$ref": "#/$defs/text"}},
        "hypothesis_claim_ids": {"type": "array", "uniqueItems": true, "items": {"$ref": "#/$defs/text"}},
        "auditor_filing": {"$ref": "#/$defs/file_ref"},
        "chair_filing": {"$ref": "#/$defs/file_ref"},
        "result": {"enum": ["passed", "hold"]}
      }
    }
  }
}
```

`checked_at` must parse as a timezone-aware RFC 3339 timestamp; a schema
implementation must enable format validation. The presence of a timestamp does
not establish freshness. `recheck_on` records the task-specific expiry and
change conditions chosen at verification, including any volatile fact that must
be checked again before use. Those conditions require actual observation outside
the local inspector; no universal expiry period is invented here.

## Proposed preflight rules

The future inspector returns the existing `HOLD`, `PLAN_ONLY`, or
`CHECKS_PASSED` states. For this extension, a requested transition or cruise with
missing or malformed prerequisite evidence returns `HOLD` even in planning
phase. Plan unfinished verification as `TURBOJET`, with its gaps visible.

1. **Validate both contracts.** Check packet version, regime, extension schema,
   and every existing base prerequisite. Preserve authorization, current tags,
   claim-cycle detection, unsettled-ancestor checks, recovery, and tool checks.
2. **Resolve actual bytes.** For each supplied reference, enforce the workspace
   path boundary, existence, and exact SHA-256. A missing file, mismatch, bad JSON,
   duplicate object key, malformed timestamp, duplicate path, or invalid record
   returns `HOLD`. Check supplied optional records even in `TURBOJET`; do not
   silently accept malformed evidence because it is not yet required.
3. **Bind baseline to scope.** For transition and cruise, baseline `result` must
   be `passed`; its `job_id` and `scope_sha256` must match the packet. Inspect the
   full declared dependency closure of `decision_inputs`. There must be exactly
   one passed `claim_check` for every [T]/[V] claim in that closure, no duplicate
   or extra claim IDs, and no unresolved or dirty ancestor. An [I] record must
   terminate in checked [T]/[V] support; it is never relabeled verified. Existing
   malformed-record checks still apply to claims outside that closure.
4. **Check evidence references.** Each source, independent-proof, and dependency
   reference in a claim check must occur in `j58.input_artifacts` with the same
   path and digest. A proof cannot be the same bytes as its source. Distinct
   bytes, reviewers, or models do not establish evidential independence: whether
   the proof actually tests the source remains a recorded human/tool review.
   If that review was unavailable or failed, the baseline stays on `hold`.
5. **Bind the transition.** For cruise, require a passed `INLET_SPIKE_LOCK` whose
   job, scope, and `baseline_sha256` match. Its `factual_claim_ids` must equal all
   active [T]/[V]/[I] claims in the decision-input closure; its
   `hypothesis_claim_ids` must equal all [P] claims in the packet and be disjoint
   from that closure. Both filing references must resolve to distinct pinned
   files; inspect their bytes. The records must actually be the Auditor's and
   Chair's boundary filings before claiming the boundary was agreed. Preflight
   alone does not authenticate authorship or the meaning of those filings.
   Check author-source membership in the declared input set and reject duplicate
   author IDs. Whether a reading was actually applied, or accurately represents
   an author's argument, requires inspection of the deliverable and source.
6. **Invalidate narrowly.** On changed inputs, a failed check, or an applicable
   `recheck_on` condition, hold the dependent operation, preserve the prior
   receipt as history, and reverify the affected scope. Unrelated work can
   continue. The inspector does not implement the unresolved C-003 cascade rule.
7. **Keep consequence gates.** Regime selection never bypasses Block 33, the
   Bell's required ruling, Seat 5's review of Chair self-certification, or any
   destination's publication/readback checks. A source-review receipt is not a
   publication authorization.

All machine results retain the existing scope statement: declared-record checks
only; no action executed, evidence authenticated, or permission granted.
Structural consistency and byte identity are machine-checkable. Truth,
independence, real reviewer participation, freshness conditions, and actual
authority require the appropriate outside check. A fabricated receipt can pass
structural validation; a hash does not repair that limitation.

## Lens stamp and telemetry

Attach a short stamp to the working record or delivery manifest:

```text
FLIGHT_REGIME: <actual regime>
BASELINE: <resolved receipt reference, or NONE during unfinished TURBOJET work>
LENSES_APPLIED: <stable IDs actually used; [] is valid>
LENS_FINDINGS: <one checkable finding per applied lens>
REFERENCE_AUTHORS_APPLIED: <author IDs, source passages, and actual contribution>
EVIDENCE_PROFILE: current-v9.1 | science-desk
FACTUAL_BASIS: <claim/source references>
INFERENCES_AND_PROPOSALS: <separate references; UNKNOWNs retained>
REVIEW_STATE: <actual Charter stage; missing reviewers named>
```

The stamp stays outside spoken narration, public story prose, and Arc-facing
paragraphs. It records work actually performed, not every lens selected at
intake. A late factual addition must enter verification before appearing as fact.

The Chair reconciles existing telemetry: catches with numerator, denominator,
class, and window; actual quota/credit consumption; failed samples; and Slop Line
findings. Unavailable measurements are UNKNOWN. No catch-ratio threshold or
resource allowance is created by this proposal. Seat 5 retains its review lane;
the Bell retains the lock. Telemetry supplements the required inspections.

## Implementation and acceptance plan

| Step | Bounded change | Evidence required before claiming completion |
|---|---|---|
| Propose | This document plus navigation, manifest entry, and changelog | Reviewable diff; existing repository checks pass. |
| Reconcile | Chair handles it as SHARED under the [Handshake](05-the-handshake.md) | Actual filings and reasons; any requested lock change isolated for the Bell. |
| Build | Separate change to `tools/omega_preflight.py`, `tools/validate_repository.py`, version-2 fixtures, and behavioral tests | Executable extension/base checks; old version-1 fixture still works; unsupported versions fail closed. |
| Inspect | Read back governing job text and exercise the exact artifacts | Record the actual tests and results, and available review seats. |
| Adopt or revert | Apply the authority class appropriate to each change | Adoption record, verified readback, and measured outcome; no silent activation. |

The future behavioral checks must include at least:

- Version 2 missing a regime, an unknown regime, or version 1 with reserved
  extension fields → `HOLD`; ordinary version 1 keeps its current behavior.
- `TURBORAMJET` with only a digest/SYNC_ID, no available baseline, a held baseline,
  wrong job/scope, missing boundary, or a digest mismatch → `HOLD`.
- A valid scoped baseline without a boundary may enter `INLET_SPIKE`; it cannot
  enter cruise. A complete synthetic fixture may pass structural checks but
  establishes no external scientific or deployment claim.
- A changed source byte, claim, dependency, target, or acceptance criterion
  invalidates a previous receipt. An unchanged receipt does not exempt a newly
  triggered freshness check.
- Dirty/UNKNOWN/falsified support, a dependency cycle, an inference with no
  checked factual support, or a missing/duplicate/extra claim check → `HOLD`.
- Source and proof with identical bytes, malformed records, bad timestamps,
  duplicate JSON keys, path escape, malformed lens IDs, duplicate author IDs, or
  an author-source reference absent from the input set → `HOLD`.
- Even with structurally valid cruise evidence, missing action authorization or
  an existing required tool still causes the base inspector's hold. No test
  performs publication or incurs charges.
- A failure injected into one matter preserves unrelated completed assets;
  review order, the single-writer rule, and public/private boundaries survive.

These are proposed acceptance cases, not completed tests of a J58 implementation.
Document validation checks links, registered artifacts, compact length, source
hashes, and code-test integrity; it cannot infer a live workflow from this text.

Before a practical pilot, name the baseline task, the error/rework measure, the
time and resource cap, and the stop/revert condition. Compare verified outputs
and rework against the unchanged method; do not claim speed or reliability gains
from the metaphor. This draft makes no claim about Beacon Cut's present status
and schedules no work around an unverified completion date.

**Next table action:** reconcile this SHARED specification, especially versioning,
receipt coverage, and the preserved Charter order. Implementation and activation
remain separate, inspectable steps.
