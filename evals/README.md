# Evaluate Author Voice

The 15 cases in `cases.json` are a behavioral test set. They are not pre-scored results. Run them separately in each configured platform, preferably in fresh conversations to avoid carrying one case's facts into another.

```sh
python3 scripts/evaluate.py prepare --out .work/eval-prompts
```

Use `--with-instructions` for an unconfigured chat; omit it when testing native skill activation or a configured Gem. Never paste the `review` criteria into the model prompt: they are for the reviewer.

Save each complete model response as `evals/responses/<run-name>/<case-id>.md`. Record platform, actual model/version if visible, date, instruction/skill version, settings, and whether the skill activated in a separate `run.json`. Do not claim a specific model if the UI conceals it.

```sh
python3 scripts/evaluate.py inspect --responses evals/responses/my-run
```

The inspector reports missing files, mechanical differences in revision cases, and the manual review criteria. It never awards an automatic editorial-quality score. Exit `1` means missing responses or mechanical review candidates, not necessarily a failed edit. Every nonempty response still needs human review.

For each case, record:

- **Fidelity:** pass/fail, with the changed or invented proposition if it fails.
- **Clarity:** worse / same / better, justified with one passage.
- **Voice and genre:** inappropriate / acceptable / strong, relative to the provided sample and task.
- **Restraint:** needless changes, omitted content, or unnecessary questions.
- **Task completion:** requested mode, format, and coverage fulfilled or explicitly limited.

Any changed result, citation misassociation, invented experiment, or concealed omission fails fidelity even if the prose sounds better. A checker flag can be an acceptable formatting change; a clean checker result can conceal a semantic failure.

To compare methods, use the same cases, sources, and settings for a baseline, the previous prompt, and Author Voice. Randomize the response labels for a reader who does not know the condition. Repeat runs before claiming an improvement. Keep model outputs private if they contain manuscript material; the response/results directories are ignored by Git.

Long-book validation additionally needs an actual chapter sequence and continuity review. This short suite cannot establish whole-manuscript quality, detector evasion, or publication readiness.
