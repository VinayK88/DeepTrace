# Model Monitoring and Robustness Testing

DeepTrace monitors the input distribution used by its TF-IDF plus DBSCAN campaign layer separately from deterministic provenance and content-evidence logic.

## Narrative drift monitoring

`deeptrace.evaluation.narrative_drift_report` compares a reference content window with a current window using two signals:

- TF-IDF centroid cosine similarity;
- character n-gram vocabulary overlap.

The default thresholds are `0.75` for centroid similarity and `0.55` for vocabulary overlap. A steady-state comparison should remain stable. A deterministic synthetic shifted window replaces baseline narratives with unrelated synthetic themes and should trigger a monitoring alert.

The report also publishes the model version, feature-schema version, and report-generation timestamp.

A monitoring alert means the language distribution changed enough to deserve re-evaluation. It does not establish manipulation, coordination, malicious intent, or attribution.

## Robustness testing

The synthetic robustness suite rewrites risky fixture narratives with alternate wording while changing account and domain identifiers. It then checks whether the clustering layer still groups sufficiently similar risky content under the same temporal, account-diversity, and risk-evidence gates used by the project.

The suite reports cluster count and synthetic item coverage for reproducibility. These values are not estimates of performance on real-world campaigns.

## Safety boundary

All narratives, accounts, domains, media evidence, and timings are synthetic. The test suite does not publish or interact with real-world content or accounts.
