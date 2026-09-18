# Testing and limitations

Run the automated checks from the repository root with Python 3.10 or later:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build.py
python3 scripts/validate.py
python3 scripts/prepare_submission.py --require-release
```

The tests cover the offline checker's handling of protected text, uncertainty markers, and invalid inputs; package reproducibility; generated instruction consistency; evaluation fixtures; and release metadata and archive checks. The build and tests use Python's standard library. GitHub Actions runs the suite on Python 3.10 and 3.14.

For Claude marketplace and plugin structure checks, use the Claude Code CLI:

```sh
claude plugin validate .
claude plugin validate ./plugins/author-voice
```

The [evaluation suite](../evals/README.md) provides synthetic prompts and human review criteria for paper and book editing, source fidelity, author profiles, and tool boundaries. Run each case in a fresh conversation with the skill enabled. Keep actual manuscript samples, raw model responses, and reviewer notes in an ignored private directory.

Mechanical checks cannot establish semantic equivalence, citation support, or editorial quality. A comparison can pass even if a revision changes which experimental group a number describes. Review meaning and evidence alongside the checker's output.

The included before/after examples illustrate editorial choices; they are not benchmark results. No cross-model quality rate, detector outcome, token saving, or whole-book fidelity guarantee is claimed.
