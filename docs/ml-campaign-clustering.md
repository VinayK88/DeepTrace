# ML campaign clustering

DeepTrace keeps content-authenticity evidence and campaign-level ML separate. The media verdict engine remains deterministic and provenance-aware; the ML layer is used to discover groups of semantically related risky narratives that may warrant analyst review.

## Representation

Narratives are transformed with character n-gram TF-IDF. Character n-grams are useful in the synthetic exercise because they retain similarity across small wording changes without requiring a downloaded embedding model or external API.

## Clustering

DBSCAN clusters narratives with cosine distance. It does not require the number of campaigns to be specified in advance and can leave isolated items as noise.

A semantic cluster is not automatically called a coordinated campaign. DeepTrace also requires:

- at least two distinct accounts;
- at least two high synthetic/manipulation-risk items;
- sufficient combined semantic, temporal, account/domain-diversity, and risk evidence.

This prevents a legitimate repeated news narrative from being escalated only because several publishers describe the same event.

## Boundary

The ML output is a triage signal. It does not establish authorship, attribution, malicious intent, or state sponsorship. All data in this repository is synthetic.
