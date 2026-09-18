# Validation record

Validation date: September 17, 2026. Version: 0.1.0.

## Completed locally

- Eighteen automated tests pass. They exercise numbers, units, signs, citations, duplicate values, literal content, explicit locks, qualifiers, linter exclusions, checker limitations, archive reproducibility, portable instruction fidelity, missing/changed evaluation responses, release metadata gates, reviewer fixtures, and detection of tampered/unlicensed archives and unsafe archive paths.
- Claude Code 2.1.269 accepts the public marketplace and plugin manifests through `claude plugin validate`. The skill directory also passed the earlier validation.
- The bundled OpenAI plugin validator accepts `.codex-plugin/plugin.json`, its metadata, and skill resources.
- The bundled skill creator's `quick_validate.py` accepts the canonical skill.
- The repository validator checks manifest identity/version alignment, resource links, evaluation inputs, the marketplace target, and generated instructions.
- All five distribution ZIPs pass CRC checks. Their names are relative, and they contain no source PDF, CSV, Python bytecode, or private manuscript files. The marketplace's plugin path resolves within the generated bundle.
- The paper and book before/after examples retain the checker's recognized protected material. The examples are hand-authored editorial illustrations, not sampled model results.
- The 512-pixel listing icon was visually inspected. Its SVG source and PNG output are included in the plugin.
- The generated reviewer pack contains five positive and three negative cases with exact synthetic inputs, expected behavior, result shapes, and explicit `not_run` status.
- The strict release command passes with the MIT license, matching manifest metadata, public URLs for `OmShiv/author-voice`, and checksummed archives. Tests also confirm that missing metadata and invalid archives block a release. Local URL checks do not establish remote reachability.

PyYAML was installed only under ignored `.work/validation-deps` to run the bundled OpenAI validators. Building, using the checker, and running repository tests require only Python's standard library. Regenerating the optional tracked brand assets with `scripts/build_logo.py` requires Pillow; normal package builds use the committed assets.

## Not yet measured

No Claude chat upload, ChatGPT account installation, Gemini Gem creation, or live model response evaluation was performed. No cross-model fidelity rate, reader preference, whole-book result, or token-cost reduction has been measured. `evals/cases.json` supplies the 15 host-neutral prompts and review criteria for that work.

Public repository distribution, GitHub Actions, and curated directory publication are separate from these local checks. Consult the repository's [Actions](https://github.com/OmShiv/author-voice/actions) and [Releases](https://github.com/OmShiv/author-voice/releases) for remote results and distributed packages. Curated directory submissions remain pending; publisher portal access has not been verified in this environment.

There is no detector score. The product is an editorial method, and a clean mechanical comparison is not a semantic or publication-readiness certificate.
