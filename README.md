# Author Voice

**Write research papers and books in your voice, with the evidence intact.**

Author Voice is a shared editorial skill for Claude, ChatGPT, and Gemini. Use it while drafting to avoid a separate rewriting pass, or apply it to an existing manuscript before export. It removes formulaic expression without imposing a word blacklist, manufacturing personality, or flattening scientific uncertainty.

This is a usable first release, not a validated claim of indistinguishable human authorship. No instruction set can guarantee the absence of model signatures. Quality means clear prose, the author's intended voice, and faithful evidence.

## Start here

Install the Claude Code plugin from this repository:

```text
/plugin marketplace add OmShiv/author-voice
/plugin install author-voice@author-voice
```

Then use `/author-voice:author-voice` in your conversation. For other platforms, download a package from [Releases](https://github.com/OmShiv/author-voice/releases) or build from source below. Curated directory submissions and live platform evaluations are pending; this beta makes no measured cross-model quality claims. Maintainers can follow [the publishing steps](docs/publishing.md).

| Platform | Artifact | Setup |
| --- | --- | --- |
| Claude chat | Uploadable skill ZIP | [Claude setup](platforms/claude/SETUP.md) |
| Claude Code | Native plugin | [Claude setup](platforms/claude/SETUP.md) |
| ChatGPT / Codex | Native plugin and local marketplace bundle | [ChatGPT setup](platforms/chatgpt/SETUP.md) |
| ChatGPT instruction-based workflows | Portable instructions and optional knowledge | [ChatGPT setup](platforms/chatgpt/SETUP.md) |
| Gemini | Custom Gem instructions and optional knowledge | [Gemini setup](platforms/gemini/SETUP.md) |

Build the archives with Python 3.10 or later; no dependencies or API keys:

```sh
python3 scripts/build.py
```

Ready-to-use archives appear in `dist/`. They are generated and excluded from Git. The source, instructions, examples, and evaluations are versioned. Source research files and private manuscripts are not included in the distributable packages.

## Use it

In your configured Gem or instruction-based assistant:

```text
Draft a paper introduction from these notes. Use Author Voice.
Keep proposals distinct from completed experiments.
```

```text
Revise this chapter in Author Voice, book mode, light edit.
Preserve its technical detail and narrator. Return clean Markdown.
```

```text
Audit this methods section. Identify unsupported claims and formulaic prose;
do not rewrite it yet.
```

```text
Build an Author Voice profile from these samples of my own writing.
Use it for manuscript work in this conversation until I turn it off.
```

The modes are natural-language options, not a software command parser. For Claude Code use `/author-voice:author-voice`; in Codex use `$author-voice`. In ChatGPT, select the installed skill with `@` where supported. Explicit activation is the most dependable way to use it before a draft.

A profile is optional. [The starter profile](profiles/starter.md) provides baseline editorial preferences; it does not claim to reproduce your personal voice. For better continuity across services, carry a short profile and one representative sample into the new conversation.

## Editorial principles

- Preserves claim strength, qualifiers, citation associations, numbers, equations, and structure.
- Replaces blanket stylistic prohibitions with decisions based on meaning and genre.
- Keeps needed scientific hedging and established terms such as “robust regression.”
- Forbids invented experimental histories, limitations, measurements, and personal anecdotes.
- Supports a paper, a book, or an author-specific profile without forcing the same voice on all three.
- Checks revisions once and leaves sound prose unchanged.

Read [the research assessment](docs/research-assessment.md) for what the supplied evidence supports and [the design notes](docs/design.md) for tradeoffs and scope.

## Local checks without model tokens

```sh
python3 plugins/author-voice/skills/author-voice/scripts/prosecheck.py lint examples/paper.before.md
python3 plugins/author-voice/skills/author-voice/scripts/prosecheck.py compare examples/paper.before.md examples/paper.after.md --diff
```

`lint` offers editorial candidates. `compare` flags changes to selected protected text and uncertainty language. Exit codes: `0` means no configured mechanical differences were found, `1` means review is needed, and `2` means an input or execution error. A zero result is **not** proof of unchanged meaning. Add exact strings through `--locks path/to/locks.json` for terminology, reference entries, or notation the partial parser does not recognize.

The checker reads UTF-8 Markdown, plain text, and LaTeX. It does not rewrite prose or edit PDFs and Google Docs. The native skill directs the host's available document tools to edit sources and verify exports. Those tools and account permissions remain necessary.

## Development and validation

The canonical instructions live in [SKILL.md](plugins/author-voice/skills/author-voice/SKILL.md). Edit that file and its references, then rebuild; do not hand-edit generated platform instructions. Keep the three plugin manifest versions aligned when releasing.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build.py
python3 scripts/build.py --check
python3 scripts/validate.py
python3 scripts/prepare_submission.py
```

[The evaluation suite](evals/README.md) covers fidelity, restraint, genre, missing evidence, and document boundaries. Packaging and checker tests are automated. Editorial quality across Claude, ChatGPT, and Gemini still requires running the supplied cases on those hosts and reviewing their actual outputs; the included examples are illustrative, not benchmark results.

See [the validation record](docs/validation.md) for the checks performed on this release and the remaining host-level evaluation.

The public Claude marketplace lives in `.claude-plugin/marketplace.json`. GitHub Actions validates the package and can prepare a draft beta release from an existing version tag. The package is available under the [MIT License](LICENSE). See [privacy](docs/privacy.md) and [terms](docs/terms.md) for data handling and use, or [report an issue](https://github.com/OmShiv/author-voice/issues).

Nothing in the build installs into your accounts, publishes a plugin, or changes sharing permissions. The packages contain instructions and an offline Python checker, with no telemetry, API calls, browser interception, or model dependency. Material you submit to a host remains subject to that host's normal handling.
