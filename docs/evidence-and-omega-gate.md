# Evidence profiles and Ω-Gate

The [current boot](../instructions/current-v9.1.md) uses the October v9.1 profile. Sources retain their original labels. A profile is part of the claim record; never migrate a bare letter without its meaning.

## Tag profiles

| Profile | [T] | [V] | [I] | [P] | [F] | Unknown |
|---|---|---|---|---|---|---|
| Current v9.1 compilation | Observed/experimentally demonstrated | Verified by named, traceable source | Inference from T/V | Provisional hypothesis/proposal | Falsified | UNKNOWN |
| Ignition Key v1.0 | Verified truth | To verify, unchecked | Inference | Proposal/speculation | Not defined | Express uncertainty conservatively |
| Working Boot v9.0 | Established/sourced in that record | Verifiable, not yet checked | Inference | Speculative | Falsified | UNKNOWN |
| August v9.1 field document | Directly established in working record | Externally verified/reference supported | Logical inference | Proposed design/parameter | Falsifiable assumption/model | [UNKNOWN] |
| Science Desk reporting | Tested/observed/documented | Not used | Inference | Not used — hypothesis is [H] | Not used — unknown is [U] | [H] hypothesis; [U] unknown |

These are incompatible vocabularies in places, not a single ladder. In particular, do not turn an old unchecked [V] into a current verified [V], or an August [F] assumption into a current falsified claim. The original assertion and its actual evidence must be reviewed first.

## T-Series and V-Series in the v8.1 reference

T0 undefined; T1 observed; T2 logical inference; T3 working hypothesis; T4 speculation/narrative; T5 noise/unsupported. These codes are **not a numeric confidence score**. The recovered inequality for dependency inheritance is unresolved against the source's own ordering. No executable cascade arithmetic is supplied in this edition.

The separate maturity axis is V1 experimental, V2 internal, V3 Operator reviewed, V4 canonical, V5 archived, V6 deprecated. A V4 narrative can still be T4; canonical-as-literature does not make it experimental evidence. Bare [V] is also not V4 or a V-Series lifecycle entry.

## Ω-Gate

1. **Gate 0 — verifiability.** Can a genuinely independent channel check the claim? If none can exist, hold it as provisional/narrative rather than promote it to an observation.
2. **Source.** Record the claim's actual origin and the specific source passage, measurement, or artifact.
3. **Independent verification.** Record the channel. Agreement between generative models may be useful criticism; it is not independent observation.
4. **Falsification.** Specify a disproof attempt, who or what ran it, and the actual result. The technical reference calls for a different agent from the generator. If that condition was not met, say so and hold the proposed promotion; do not fabricate a second reviewer.
5. **Load analysis.** Identify dependents, consequences, uncertainty, reversibility, and the standard required by the decision.
6. **Bounded Operator sign-off.** Approve or hold framework status only after evidence requirements are met. Sign-off cannot override a failed scientific check.

The source names load-dependent cooling-off and re-audit intervals but does not define their values. They remain [FILL]. Documentation publication does not fill them.

## Demotion and quarantine

Contradictory evidence can lower a claim's status immediately. Flag dependencies for re-audit and keep contested or DIRTY inputs out of settled decisions. Preserve the failed assertion and why it failed; do not quietly replace its history with a better story.

The v8.1 reference contains an unusual DIRTY propagation direction and an incompatible numeric inheritance expression. Both are retained in the source, called out in [the conflict register](versions-and-conflicts.md), and left unimplemented. The conservative working rule is to hold affected decisions until the relevant dependency has been checked, not to pretend an unresolved algorithm ran.

## Minimum audit record

Record timestamp, target claim, source/profile, before/after classification, independent channel, falsification method/result, dependencies, actual authorization/sign-off, outcome, open limits, and next review condition. Use null or UNKNOWN for unavailable values. Corrections append a new entry pointing to the original. A blank template or illustrative example is not a completed audit.

An audit procedure is a design intention. Its effectiveness can only be supported by real recorded audits and measured failures caught. See [evaluation requirements](evaluation.md).
