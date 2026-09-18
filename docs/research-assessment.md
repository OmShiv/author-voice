# Research assessment

Reviewed September 12, 2026: the supplied eight-page June 2026 preprint by Fırat Mıhcı, the four-row CSV of writing heuristics, and the existing `prompt.md`. The PDF text was read and its quantitative figures inspected. The published classifier code was also inspected, but the study was not rerun. Original input files remain outside the distributable repository.

## What the paper supports

The study compares 510 short English passages from five GPT/Claude models answering 102 shared prompts. Its reported vendor ROC-AUC is 0.96; five-way model classification accuracy is 50%. These are different metrics. The title's “96% distinguishable” should not be read as 96% classification accuracy, and neither statistic measures human-versus-AI detection for a revised manuscript. The sample excludes Gemini and long books or papers. [Study and released materials](https://github.com/humanizemyai/ai-model-accent-nlp).

The useful design implication is that there is no single vendor-neutral punctuation prescription. The supplied paper's table associates greater sentence-length variation with Claude, contradicting any simplistic claim that increasing “burstiness” necessarily removes model style. Its design does not test that editing intervention. AUC summarizes score ranking across thresholds; it is not a guarantee for an individual passage.

The implementation uses shuffled stratified folds, without grouping by prompt or topic. Standardization is correctly inside the logistic-regression pipeline. My interpretation: these evaluations do not establish transfer to entirely unseen prompt/topic groups; a grouped holdout would test that more directly. This is a limitation of the generalization claim, not proof that the reported scores are wrong. [Classifier implementation](https://github.com/humanizemyai/ai-model-accent-nlp/blob/main/src/accent.py).

The paper is a preprint associated with a writing-humanization service. That context warrants evaluating its claims independently, rather than treating the paper as evidence that a particular product or rewriting recipe works. The release does not validate this project's skill, detector outcomes, or long-document fidelity.

## CSV and previous prompt

The CSV supplies useful editorial hypotheses, but no independent validation of its “how engineers actually write” column. Its four rows concern punctuation, vocabulary, cadence, and research narrative. They are preferences to inspect in context, not measurements that characterize every human author.

| Original idea | Decision in Author Voice | Reason |
| --- | --- | --- |
| Ban em/en dashes | Optional prose preference, protected notation exempt | Quotations, ranges, minus signs, and established terminology must survive. |
| Ban a vocabulary list | Inspect empty or inflated uses | Technical terms can have precise meanings; synonym cycling reduces consistency. |
| Alternate sentence lengths | Let argument and pacing determine length | A compulsory rhythm creates another template. |
| Describe failures and engineering friction | Include only supported limitations/history | A style rule must not invent research. |
| Prefer active author decisions | Preserve actor, genre, and emphasis | Passive voice can be useful. “Throughput degrades” is not grammatically passive. |
| Write for a premier systems venue | Separate paper/book guidance and profiles | A memoir, monograph, and methods section need different choices. |

## What to validate next

Compare baseline generation, the previous prompt, and Author Voice on matched tasks using the same sources and model settings. Include the author's own writing as a voice reference, not as evidence that a detector is correct. Use blind human judgments of clarity, voice fit, and overediting, with factual fidelity as a hard constraint. Record models and versions, repeat runs, and preserve raw outputs.

For stylometric experiments, split at the document/author/topic level as appropriate and report uncertainty. Keep detector scores out of the product's success criteria: reducing a measured feature can simply replace one recognizable style with another.

The [Caveman skill](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md) inspired the small, reusable packaging and explicit activation pattern. Its terse communication goal is different from publication prose. This implementation does not copy its instruction text or remove articles and hedging wholesale.
