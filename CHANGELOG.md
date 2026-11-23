# Changelog

## 2026-11-22 — J58 Operating Lenses specification proposed

Added `advanced-ai-edition/07-j58-operating-lenses.md` as a [P] SHARED proposal
based on the Operator-supplied sketch attributed to Gemini Hydrogen. It defines
five auxiliary checklists, three evidence-handling regimes, a proposed version-2
packet overlay, scoped baseline/boundary records, and future preflight acceptance
cases. It preserves the locked Charter order and distinguishes digest checks
from independent verification. The actual lens-amendment link is supplied.

Draft 2 incorporates the Operator's additional request for Carl Jung psychology
and the wider scientific author pool. The companion
`advanced-ai-edition/08-reference-author-catalog.md` supplies an expandable
cross-domain reference catalog and a detailed Jung mounting procedure. Actual
author applications require inspected source passages and an explicit
contribution; reading leads are separated from the sources inspected for this
draft. The proposed packet overlay binds mounted authors to input sources.

This documentation change registers and links the proposal only. Existing packet
fixtures, executable preflight and validator behavior, compact boot, recovered
source exports, edition labels, and protected-domain locks are unchanged. No
other seat's acceptance, Bell ruling, implementation, activation, or performance
gain is claimed.


## 2026-11-11 — Documentation consistency patch (no edition change)


Four wording alignments, documentation only; the repository edition and revision labels (2026.10.28, revision 2) are unchanged, and no source export was altered.


- **Publication status.** The 2026-11-04 entry below no longer reads "working copy; not yet published": that change is on main (PR #6, merge 7e5057a), and its heading and closing sentence now say so.
- **T5 wording.** `docs/evidence-and-omega-gate.md` now states beside the v8.1 T-series line that the T5 inversion is intentional under the Operator's 2026-10-29 ruling (register C-003) — T5 is the top grade in the current profile — while the inheritance inequality and DIRTY propagation elements remain open.
- **Boot reference.** The full boot names the Independence Rule and points to its full text and proportionality limiter in `docs/evidence-and-omega-gate.md`; the compact boot labels its gate with the rule's name (at 3,971 of its 4,000 characters, the compact has no room for the limiter sentence, which the full boot carries).
- **Validator registration.** `capabilities.json` now registers the repository validator (`tools/validate_repository.py`) as implemented_local, matching `docs/capabilities-and-evolution.md`, which already listed it as implemented.


Verified locally after the change: `tools/validate_repository.py` PASS, and the preflight suite passes 15/15. Stronger source checking (whether a named source actually supports a claim) is unchanged by this patch and remains a separate, tested change for a later date.


## 2026-11-04 — Independence Rule adopted as standing law; checker strengthened (published to main 2026-11-04 — PR #6, merge 7e5057a)


The Operator adopted the Independence Rule as standing law on 2026-11-04; it is recorded in `docs/evidence-and-omega-gate.md` beside the Ω-Gate it binds. At the Operator's order the same day ("test our existing TruthGate with a deliberately false claim"), a plant test was run against a scratch copy of this repository: a false claim ("Letters and Papers from Prison was first published in 1945") tagged [V] with no source passed the checker untouched — the checker validated the tag vocabulary and the profile definition, never the claim's evidence. `tools/validate_repository.py` now enforces the profile's own definition: in authored documents (source exports and instruction/vocabulary files excluded), a [V] tag in claim position must name its source on the same line (a section reference, versioned artifact, URL, DOI, register ID, or the word "source"). Vocabulary and meta uses are exempt by position and wording. Verified after the change: the plant FAILS with "[V] claim without a named source"; the unmodified corpus still PASSes with zero false positives; the preflight suite remains 15/15. Scope is unchanged and stated plainly: the checker now enforces that a source is NAMED — whether the named source supports the claim remains the L4 verification act, not a machine judgment. The repository edition and revision labels are unchanged; this change was published to the public repository on 2026-11-04 through the Operator's signed-in session, as with prior writes (PR #6, merge 7e5057a). The same morning, at the Operator's further ruling, the rule gained its proportionality limiter (recorded in the same section of `docs/evidence-and-omega-gate.md`): the gate is proportional to consequence, and when verification would cost more than a claim is worth the claim is graded UNKNOWN and the work moves on — checking protects substance and is never the deliverable.


## 2026-10-29 — Operator rulings recorded; lens definitions amendment; full license text


At the Operator's ruling on 2026-10-29, following an independent audit of this edition. The repository edition and revision labels (2026.10.28, revision 2) are unchanged; this entry records governance decisions and documentation repairs within that edition.


- **Precedence ratified.** The Operator ratified the conflict register's precedence rule: the v9.1 compilation governs c
