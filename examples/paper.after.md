# Cache evaluation

Our cache reduces median latency from 12 ms to 9 ms on workload A [3]. The observed improvement may depend on locality; we did not evaluate workload B.

We use robust regression to limit the influence of outliers.

<!-- author-voice:keep -->
The fitted model is $y = \beta_0 + \beta_1 x + \epsilon$.
<!-- /author-voice:keep -->
