# Gauge Master — story embed preservation contract

The master method is the user-approved **September 4, 2026 Ω Daily Discovery Brief**. Its complete byte-exact fixture was not recovered. This document preserves the working contract; it does not claim to contain the original HTML or an exact visual reconstruction.

## Scope

Standalone text-story embeds use browser-native `speechSynthesis` and `SpeechSynthesisUtterance`. The recorded Omega briefing series uses its approved recorded MP4/native media player instead. Preserve the latter; do not apply the standalone speech default to it.

For an embed change, recover the target/master and keep a recovery copy. Substitute authorized content and identifiers; keep approved DOM, styles, spacing, typography, controls, and audio architecture. If the master is unavailable, label a requested reconstruction honestly. Do not promote a later edition to the original master by implication.

## Namespace and state

- Use a collision-resistant article namespace consistently across container, spoken region, controls, status, CSS, handlers, and JavaScript references.
- Keep per-story speaking, paused, utterance, and callback state isolated. Reuse a namespace only when replacing that same deployed instance; allocate a fresh one for another instance.
- Scope CSS and keep the fragment self-contained. Do not add a backend, external JavaScript, autoplay, paid speech, a new avatar, or a redesign without task authority.

## Speech and controls

Use a direct user gesture. Retain live utterance references, approved language/rate, and asynchronous voice loading without autoplay. Narrate only the dedicated story region, excluding controls, source URLs, and marked exclusions.

The main toggle is **Listen → Pause → Resume**; **Stop** stays separate. Stop, natural completion, and real errors restore coherent idle/replay state. Keep native accessible buttons, useful unsupported-speech/error status, and `aria-live` feedback.

The browser speech queue is shared. Namespaced variables do not isolate `cancel()`, `pause()`, or `resume()`. Check actual ownership: starting B must reset A correctly; obsolete A callbacks must not alter B; stopping inactive A must not cancel active B. Preserve the approved ownership architecture or repair the concrete failure within scope. Never cancel the shared queue during initialization.

## Required observations

| Case | Expected behavior |
|---|---|
| Listen A | Only A narrates; A shows Pause |
| Pause/Resume A | Approved behavior and matching labels |
| Stop A | Reset and replay work |
| Natural end/error | Coherent idle state and useful status |
| A then B | Defined handoff, no stale UI or overlap |
| Stop inactive A while B plays | B continues |
| Rapid switches/delayed events | Obsolete callbacks cannot overwrite the active owner |
| Two copies of one story | Distinct IDs, handlers, and narration targets |
| Unsupported speech/delayed voices | Clear status, no exception or autoplay |
| Long article on phone | Actual phone result recorded; no extrapolation from mocks |

Compare the changed fragment with the selected fixture after normalizing permitted content/namespace substitutions. Report static inspection, mocked execution, browser observation, and live-site audible tests separately.

When copy/paste HTML is requested, deliver the entire fragment in one HTML code block without omissions. An embed request alone does not authorize publication. An authorized replacement changes the intended block, preserves unrelated working stories, and verifies the served result.
