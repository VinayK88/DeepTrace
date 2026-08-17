from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import EvidenceEnvelope

MODEL_NAME = "TFIDF+DBSCAN"


@dataclass(frozen=True)
class MLClusterFinding:
    cluster_id: str
    content_ids: tuple[str, ...]
    accounts: tuple[str, ...]
    domains: tuple[str, ...]
    time_span_minutes: int
    semantic_similarity: float
    risky_items: int
    coordination_score: float

    def to_dict(self) -> dict:
        return asdict(self)


def _semantic_matrix(items: list[EvidenceEnvelope]):
    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        lowercase=True,
        sublinear_tf=True,
    )
    return vectorizer.fit_transform(item.narrative for item in items)


def cluster_campaigns(items: list[EvidenceEnvelope]) -> list[MLClusterFinding]:
    """Cluster semantically similar narratives, then apply coordination evidence gates."""
    if len(items) < 2:
        return []

    matrix = _semantic_matrix(items)
    labels = DBSCAN(eps=0.35, min_samples=2, metric="cosine").fit_predict(matrix)
    findings: list[MLClusterFinding] = []
    cluster_index = 1

    for label in sorted(set(int(x) for x in labels if int(x) >= 0)):
        indices = [i for i, value in enumerate(labels) if int(value) == label]
        group = [items[i] for i in indices]
        accounts = tuple(sorted({item.account_id for item in group}))
        domains = tuple(sorted({item.domain for item in group}))
        span = max(item.minute for item in group) - min(item.minute for item in group)
        risky = sum(
            item.synthetic_signal >= 0.80 or item.manipulation_signal >= 0.70
            for item in group
        )

        similarity = cosine_similarity(matrix[indices])
        if len(indices) == 2:
            semantic_similarity = float(similarity[0, 1])
        else:
            upper = similarity[np.triu_indices(len(indices), k=1)]
            semantic_similarity = float(upper.mean()) if len(upper) else 1.0

        temporal = 1.0 if span <= 15 else max(0.0, 1.0 - (span - 15) / 60.0)
        account_diversity = min(1.0, len(accounts) / 3.0)
        domain_diversity = min(1.0, len(domains) / 3.0)
        risky_fraction = risky / len(group)
        score = round(
            0.35 * semantic_similarity
            + 0.25 * temporal
            + 0.15 * account_diversity
            + 0.10 * domain_diversity
            + 0.15 * risky_fraction,
            3,
        )

        # ML supplies semantic grouping. Explicit evidence gates prevent a benign
        # repeated news narrative from being labeled a coordinated influence campaign.
        if len(accounts) >= 2 and risky >= 2 and score >= 0.70:
            findings.append(
                MLClusterFinding(
                    cluster_id=f"ml-camp-{cluster_index:02d}",
                    content_ids=tuple(item.content_id for item in group),
                    accounts=accounts,
                    domains=domains,
                    time_span_minutes=span,
                    semantic_similarity=round(semantic_similarity, 3),
                    risky_items=risky,
                    coordination_score=score,
                )
            )
            cluster_index += 1

    return sorted(findings, key=lambda row: (row.coordination_score, row.cluster_id), reverse=True)


def ml_summary(items: list[EvidenceEnvelope]) -> dict[str, object]:
    findings = cluster_campaigns(items)
    return {
        "model": MODEL_NAME,
        "representation": "character n-gram TF-IDF",
        "clusterer": "DBSCAN with cosine distance",
        "campaign_clusters": len(findings),
        "meaning": "Unsupervised semantic grouping plus explicit temporal/account/risk evidence gates; not attribution or intent inference.",
    }
