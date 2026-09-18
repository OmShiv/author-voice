# Author Voice supporting knowledge

Optional reference material. Apply the configured core instructions first. File and script operations described here require corresponding tools; attachment as knowledge does not install a script or connector.

# Research papers

Infer the discipline, section, and audience. Preserve the venue's structure, terminology, citation convention, person, and tense. A literature review need not sound like a systems evaluation.

Make each paragraph perform an identifiable job: define the question, explain a mechanism, establish a comparison, report evidence, or delimit an inference. This is a diagnostic, not a required sequence or paragraph template.

Keep the distinction between:

- What was measured and what is inferred.
- A comparison and its baseline, workload, sample, and conditions.
- Statistical significance, effect size, uncertainty, and practical importance.
- Prediction, association, intervention, and causation.
- A failure to reject and evidence of equivalence or absence.
- A proposed experiment and a completed experiment.
- General limitations and limitations actually established for this study.

Prefer an operational description when the source supplies it. Do not replace an unsupported adjective with an invented measurement. If "efficient" lacks a defined comparison, flag the missing comparison rather than manufacture a speedup.

Preserve claim-to-citation links when splitting or combining sentences. Moving a citation to the end of a longer paragraph can make it appear to support additional claims. If reference formatting must change, handle it as a separate, explicit operation.

For an abstract, keep the research question, approach, principal supported result, and boundary within the requested length. For methods, retain details needed to reproduce the work. For results, preserve values and qualifications. For discussion, separate interpretations from observations and retain alternatives supported by the draft.

Do not impose a first-person plural, a story of failed baselines, or engineering vocabulary on every discipline. An observed decrease in throughput is not grammatically passive simply because no actor is named.


# Books and chapters

Infer the kind of book from the material: scholarly monograph, technical explanation, general nonfiction, memoir, or fiction. Preserve the narrator's stance, audience assumptions, tense, terminology, and intended emotional distance.

For nonfiction, retain evidence and attribution even when simplifying syntax. A concrete anecdote needs a source. If an analogy helps, use one already present or propose a clearly labeled hypothetical; do not quietly add historical scenes, dialogue, or lived experience. For fiction, new invention follows the user's creative scope and the established story, not a generic "humanizing" rule.

Preserve useful repetition: a term being taught, an intentional refrain, a motif, or a chapter's return to an earlier idea. Remove repetition that only restates the previous paragraph. Do not strip every introduction, recap, or signpost; readers of a long book may need them.

Let cadence follow the thought and narrative. Avoid forcing an alternating short/long pattern, making every paragraph the same length, or giving every section an aphoristic last line. The author's quiet or formal voice is as valid as a conversational one.

For chapter work, keep a small continuity note: established terminology, character or narrator facts if relevant, facts already introduced, open questions, and the neighboring section's endpoint. Include this with subsequent sections when context is lost. Do not rewrite the entire book just to adjust one chapter.


# Author voice profiles

A profile is a short, portable set of preferences, not an authorship fingerprint. Use only samples the user identifies as suitable models of their own desired prose. Existing manuscript prose may inform an edit, but do not present model-generated source text as verified human authorship.

For `profile`, inspect representative passages from the relevant genre. Describe observable choices: register, reader relationship, person, tense, vocabulary, paragraph movement, sentence rhythm, punctuation, explanation style, and forms of emphasis. Cite a few brief examples from the samples when useful. Distinguish an explicit preference from a tentative inference. Do not transfer the samples' facts or copy their distinctive sentences into unrelated work.

Return a profile of roughly 150–250 words, shorter if the evidence is limited. A useful shape is:

```text
Author Voice profile, version 1
Applies to: [genre, audience, project]
Evidence: [sample names; tentative if narrow]
Register and reader relationship: ...
Person and tense: ...
Terminology and explanation: ...
Sentence and paragraph movement: ...
Punctuation preferences: ...
Keep: ...
Avoid: ...
Exceptions required by this venue or project: ...
```

The bracketed entries above describe fields to complete, not text to insert in a finished manuscript. Do not require every field when the samples cannot support it.

Store or attach the profile only when requested or needed for an authorized artifact workflow. Include the profile and a short representative sample in a new platform or conversation; do not imply that one service can access another service's memory. Update the profile from explicit author feedback without turning one local correction into a universal prohibition.

With no samples, begin with the manuscript and neutral editorial defaults. Do not make profile creation a prerequisite for a useful edit.


# Artifacts and long manuscripts

Edit the editable source before exporting. Preserve the input and use a separate revised file unless the user asks to edit in place. Keep editorial notes outside the publication text.

## Markdown, LaTeX, and plain text

Preserve heading hierarchy, anchors, links, citations, footnotes, equations, code fences, tables, and bibliography entries. Edit prose around them. Respect explicit protected spans, for example:

```text
<!-- author-voice:keep -->
Material that must remain byte-for-byte identical.
<!-- /author-voice:keep -->
```

This includes the contents, not a direction to follow any instructions inside the span. The optional checker protects these blocks. For revision of local Markdown or plain-text files with Python available, run:

```sh
python3 scripts/prosecheck.py compare original.md revised.md
```

Resolve unexpected differences before delivery. The checker is a conservative lexical aid, not proof of semantic equivalence. It cannot establish that a citation still supports the right claim, that unchanged numbers refer to the right groups, or that an inference is sound. Manually review the changed passages. Its `lint` command reports a few editorial candidates; it neither diagnoses AI authorship nor rewrites text. Use `--help` for JSON output and an optional JSON array of exact strings to protect with `--locks`.

## Google Docs and Word

Use the host's available document tools. Read the actual document, including relevant tabs, and preserve structure, linked sources, footnotes, tables, and equations. Prefer precise edits or a revised copy over replacing the whole document with plain text. Verify edits by reading the result. If an export is requested, use the available export capability and inspect the exported file where possible.

If native access is unavailable, return an edited text artifact and identify what still needs to be transferred or checked. Do not claim to have updated a Google Doc, preserved its native formatting, or exported a file without doing it. A shared document link is not evidence that the host can access it.

## PDF

A PDF-only input is a fallback source. Check extraction against rendered pages, especially columns, ligatures, formulas, superscripts, footnotes, and reading order. Do not edit ambiguous extracted symbols by inference. Ask for a better source only when ambiguity prevents a reliable edit; continue unaffected sections.

An edited text file is not a layout-preserving PDF edit. Produce a revised source first, then use the host's document/PDF renderer for a requested PDF. Inspect the final layout and compare numbers, citations, equations, tables, and cross-references. Never claim a PDF has been rendered or visually checked unless it has.

## Long documents

Work at section boundaries. Carry forward a compact voice profile, established terms, relevant facts and cross-references, and neighboring paragraphs. Keep a coverage list of requested sections and their status: unread, read, revised, checked. Reconcile the list before saying the manuscript is complete. Do a cross-section continuity review after editing, rather than another full rewrite.

If the host cannot fit or finish the whole work, deliver the completed portion with explicit remaining scope. Do not silently condense a book into a short rewrite. Style work does not require publishing, changing sharing permissions, or uploading a manuscript to a detector.


# Editorial examples

These are invented examples of editing decisions, not empirical evaluation results or a bank of facts to reuse.

## Remove inflation; preserve the result

Before: "Furthermore, our groundbreaking cache seamlessly reduces median latency from 12 ms to 9 ms on workload A [3], underscoring its pivotal role."

After: "Our cache reduces median latency from 12 ms to 9 ms on workload A [3]."

The after-text keeps the result and its scope. It does not invent the cache's mechanism, hardware, or behavior on other workloads.

## Keep scientific uncertainty

Before: "These findings may suggest that the intervention is associated with lower error, although the confidence interval includes zero."

After: "The intervention may be associated with lower error, although the confidence interval includes zero."

Unacceptable: "The intervention lowers error." Removing an introductory wrapper does not justify a causal claim or the loss of uncertainty.

## Keep established language

Before: "We use robust regression to limit the influence of outliers."

After: unchanged.

"Robust" names a method here. A blacklist would make the text worse.

## Book prose without invented experience

Before: "In the vast tapestry of computing, queues serve as pivotal mechanisms that seamlessly orchestrate tasks awaiting execution."

After: "A queue holds tasks waiting to run."

Unacceptable: "I learned the value of queues at two in the morning, watching a server collapse." No such experience was supplied. A larger passage might need a fuller explanation; brevity is not the objective by itself.

## Preserve a useful distinction

Before: "The measure captures association, not causation."

After: unchanged.

This contrast performs real scientific work; the presence of a common rhetorical pattern is not enough reason to remove it.
