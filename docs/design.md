# Design decisions

## One editorial method, three hosts

The canonical skill is inside `plugins/author-voice/skills/author-voice/`. Claude and OpenAI use the same directory through their respective manifests. A builder derives portable ChatGPT and Gemini instructions from the same core and combines optional references into a knowledge file. This avoids maintaining three gradually diverging prompts.

The shared core contains every essential fidelity rule. Genre detail and artifact handling live in optional references. Knowledge retrieval is useful but cannot be assumed on every turn, so critical constraints never live only in attachments.

## Apply during generation

A skill or configured Gem can influence the initial draft. This removes the need for a separate service that receives and rewrites every response. It does not make instructions token-free: hosts still process relevant instructions and context, and their accounting and caching differ. No measured token savings are claimed.

For existing prose, make one focused edit and compare the changed passages. The local checker requires no model call. Large documents need section coverage, a voice profile, and continuity review. There is no automatic full-manuscript rewrite loop.

## Fidelity before style

The skill preserves semantic invariants through model instructions and editorial review. The checker supplements those with exact comparisons of selected lexical material. Neither layer proves semantic equivalence.

The checker deliberately reports conservative differences. For example, changing a heading or reformatting a citation can trigger review even when authorized. New prose might legitimately rearrange sentences while preserving all protected tokens; unchanged token inventories can also conceal swapped experimental groups. Human review resolves both cases.

The checker uses a partial Markdown/LaTeX recognizer, not a complete parser. It recognizes common citations, double/curly quotations, fences, math delimiters, pipe tables, and a limited set of units. It does not cover every citation style, single-quoted English quotation, nested construct, arbitrary bibliography, or notation. Use explicit locks and review for unrecognized material. It has no auto-fix mode.

## Artifact boundaries

The first release handles language natively through host models, with instructions for editable source, Google Docs, and PDF workflows. It does not implement its own Google Docs connector, PDF layout engine, or browser extension. Native document operations use the host's actual tools; otherwise the skill returns revised source and names the remaining transfer/export work.

A browser interceptor would add brittle UI dependencies and potentially a second generation pass. A model-backed MCP rewriting server would duplicate the host's generation capability and introduce keys, a service, and token costs. Neither is needed to deliver this editorial method. A connector becomes useful if precise document operations, rather than wording instructions, become the unmet requirement.

## Evaluation and release status

The automated checks test protected material, error handling, package consistency, and build reproducibility. Behavioral cases cover technical prose, books, unsupported claims, profiles, prompt injection in source text, inaccessible files, and unrelated tasks. The examples are hand-authored illustrations.

This release has no measured human preference score, fidelity rate across vendors, detector success rate, or whole-book quality claim. Those require actual host runs and manuscript review. Store private manuscript samples and model responses under ignored `private/` or `evals/responses/`, not in the distributed skill.
