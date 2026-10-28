# Evaluation status and requirements

No empirical model-performance result is established by repository edition 2026.10.28.

The removed 2025 benchmark assigned scores using canned response IDs and pilot identity rather than comparing measured real-model behavior. Those reported improvements cannot validate a current framework. They are absent from the active instructions and release material; the previous revision remains in Git history as provenance.

The supplied documents are operating methods and technical scaffolds. A source label saying a gate is built or hardened describes that document's status. It does not prove a deployed gate caught fabrication. A static check can establish that files, links, hashes, profiles, and length limits are consistent. It cannot establish model adherence, memory improvement, code correctness across tasks, or commercial value.

## Minimum future comparison

Before claiming a measured benefit, record:

1. The specific hypothesis, tasks, success criteria, and failure categories before running the comparison.
2. Exact model/version, date, tool access, memory/state inputs, prompts, sampling settings, and resource budget for each condition.
3. A baseline and an intervention condition that differ only in the declared procedure; disclose unavoidable differences.
4. Actual model outputs and tool traces, independent scoring or objective executable tests, and error cases. Do not score solely by a model's assigned identity or its own confidence.
5. Repeated trials, previously unseen tasks, uncertainty, sample size, exclusions, costs, and reproducible artifacts.
6. The measured result and its limits. Publish null or negative results. A gain on one task is not proof that all agent failure modes are solved.

Use score-point differences or actual pass rates where meaningful. A zero baseline does not justify an ordinary percentage-growth claim. Keep observed results separate from hypotheses and intended design behavior.

## Repository integrity command

```sh
python3 tools/validate_repository.py
```

This standard-library script performs deterministic local document checks. It has no model connection, no account access, no paid services, and no publication step. It reports only what it actually inspected. External link availability and browser playback are outside its scope.
