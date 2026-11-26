# J58 local implementation and inspection boundary

Prepared 2026-11-26 against the [draft-2 contract at its pinned commit](https://github.com/Copperhead1978/DonSol-Omega-Kernal/blob/d2785a6d53573c581ba66da39b7cb90add807bb6/advanced-ai-edition/07-j58-operating-lenses.md).

The local inspector now accepts schema version 2 and enforces the draft's
extension, scope digest, pinned file bytes, baseline, boundary and decision
closure checks. Valid legacy version-1 records retain their existing behavior;
version 1 with reserved J58 fields holds. The capability registry stays at
version 1. This implementation does not adopt optional lenses, authenticate
records or reviewers, or activate a production service.

Run the read-only inspector with an explicit job workspace:

```sh
python3 tools/omega_preflight.py examples/job-packet-v2.json --workspace-root .
python3 tools/validate_repository.py
python3 -m unittest discover -s tools -p 'test_*.py'
```

The version-2 example is an unexecuted planning fixture. A missing, changed,
malformed or escaping evidence file holds the affected operation. Scope changes
invalidate cached evidence. Current environment and action authorization are
always checked separately; they are deliberately outside the evidence digest.
Malformed supplied optional records also hold. Unknown freshness conditions
require an external observation; the inspector invents no universal expiry.

## Implemented contract checks

| Requirement | Local implementation |
| - | - |
| Versioning and base checks | `omega_preflight.assess` combines v2 blockers with the existing v1 checks; reserved extension fields on v1 hold. |
| Strict records and bytes | `j58_preflight` rejects duplicate JSON keys, non-finite numbers, closed-record extras, duplicate/aliased input paths, missing files, digest mismatches and workspace escapes. |
| Scope | The exact named Python JSON serialization profile pins the specified base fields, recovery plan, inputs and author references. Array order is preserved. |
| Baseline | Exact passed claim-check coverage of the full factual decision closure; checked source/proof/dependency membership, distinct proof bytes, timestamp format and current declared support. |
| Boundary | Matching job, scope and baseline digest; exact factual/hypothesis partitions; distinct pinned Auditor/Chair files. |
| Mounted references | Unique author IDs and declared input membership; source interpretation and actual lens use remain external checks. |
| Local fixture effect | `j58_runner` rechecks preflight and requires a separate host permit with matching scope/target and explicit byte ceiling. It implements one text artifact operation. |
| Duplicate and crash recovery | A durable SQLite reservation, unique job/target identities and atomic no-overwrite publication allow recovery before or after publication, with exact readback. |

## Local fixture gateway

`FixturePermit` is supplied by trusted host code, never read from the packet.
The host remains responsible for authenticating its authority and observing
freshness. The CLI has a separate `--allow-local-fixture-write` opt-in and
requires `--max-bytes`; absent opt-in denies execution. A packet declaring its
own authorization cannot supply that permit. The only implemented effect is
UTF-8 text written to the packet action's relative target, with content included
in the scope digest. External writes and arbitrary commands are unsupported.

The journal and effects must share a trusted workspace with one runner journal.
Other actors must not write its files or replace its directory structure while
a job runs. Write directories are opened without following symlinks; targets
are never overwritten. A changed completed artifact holds instead of being
silently repaired. Crash recovery adopts matching bytes only for a known
reservation. This is a bounded local filesystem fixture, not a general
exactly-once guarantee for external services, network filesystems or hostile
concurrent workspace writers.

Tests exercise interruption both before and after artifact publication,
including actual subprocess death, concurrent duplicate deliveries, changed
scope, stale inputs, missing host permits and conflicting outputs. Synthetic
evidence proves these program behaviors only. Distinct bytes, model agreement,
metadata shapes and passing tests establish neither factual truth nor genuine
reviewer independence. Reviewer participation, source meaning, owner sign-off,
production landing and public playback each require their own evidence.

Original source exports, compact boot, owner inspection holds and protected
decisions are unchanged. The broader runtime broker, live retrieval, sealed
inspection intake, resource telemetry and production adapters remain separate
unimplemented services.
