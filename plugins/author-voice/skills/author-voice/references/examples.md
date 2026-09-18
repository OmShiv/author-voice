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
