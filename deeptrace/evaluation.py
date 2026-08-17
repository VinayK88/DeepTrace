from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .fixtures import ITEMS
from .ml import MODEL_NAME, cluster_campaigns
from .models import EvidenceEnvelope

MODEL_VERSION = "deeptrace-tfidf-dbscan-v1"
FEATURE_SCHEMA_VERSION = "narrative-char-ngram-v1"
CENTROID_ALERT_THRESHOLD = 0.75
VOCABULARY_ALERT_THRESHOLD = 0.55


def _vectorizer(texts: list[str]) -> TfidfVectorizer:
    model = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        lowercase=True,
        sublinear_tf=True,
    )
    model.fit(texts)
    return model


def narrative_drift_report(
    reference_items: list[EvidenceEnvelope],
    current_items: list[EvidenceEnvelope],
) -> dict[str, object]:
    reference_texts = [item.narrative for item in reference_items]
    current_texts = [item.narrative for item in current_items]
    if not reference_texts or not current_texts:
        return {
            "centroid_cosine_similarity": 1.0,
            "vocabulary_overlap": 1.0,
            "drift_alert": False,
            "reasons": [],
        }

    reference_vocab = set(_vectorizer(reference_texts).vocabulary_)
    current_vocab = set(_vectorizer(current_texts).vocabulary_)
    union = reference_vocab | current_vocab
    vocabulary_overlap = len(reference_vocab & current_vocab) / max(1, len(union))

    shared = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        lowercase=True,
        sublinear_tf=True,
    )
    matrix = shared.fit_transform([*reference_texts, *current_texts])
    ref_matrix = matrix[: len(reference_texts)]
    cur_matrix = matrix[len(reference_texts) :]
    ref_centroid = np.asarray(ref_matrix.mean(axis=0))
    cur_centroid = np.asarray(cur_matrix.mean(axis=0))
    centroid_similarity = float(cosine_similarity(ref_centroid, cur_centroid)[0, 0])

    reasons = []
    if centroid_similarity < CENTROID_ALERT_THRESHOLD:
        reasons.append("narrative centroid shifted")
    if vocabulary_overlap < VOCABULARY_ALERT_THRESHOLD:
        reasons.append("character n-gram vocabulary overlap fell")

    return {
        "metric": "tfidf_distribution_drift",
        "centroid_cosine_similarity": round(centroid_similarity, 3),
        "centroid_alert_threshold": CENTROID_ALERT_THRESHOLD,
        "vocabulary_overlap": round(vocabulary_overlap, 3),
        "vocabulary_alert_threshold": VOCABULARY_ALERT_THRESHOLD,
        "drift_alert": bool(reasons),
        "reasons": reasons,
    }


def simulate_shifted_narratives(items: list[EvidenceEnvelope]) -> list[EvidenceEnvelope]:
    shifted = []
    replacements = (
        "fabricated logistics disruption rumor",
        "synthetic market panic narrative",
        "coordinated emergency-services impersonation claim",
        "AI generated diplomatic crisis allegation",
    )
    for index, item in enumerate(items):
        shifted.append(
            replace(item, narrative=replacements[index % len(replacements)])
        )
    return shifted


def _adversarial_items() -> list[EvidenceEnvelope]:
    base = ITEMS[2]
    synthetic = ITEMS[4]
    return [
        replace(
            base,
            content_id="adv-m01",
            account_id="adv-acct-1",
            domain="adv-a.example",
            minute=100,
            narrative="secret attack allegedly caused the bridge collapse",
        ),
        replace(
            base,
            content_id="adv-m02",
            account_id="adv-acct-2",
            domain="adv-b.example",
            minute=104,
            narrative="bridge collapse was allegedly caused by a secret attack",
        ),
        replace(
            synthetic,
            content_id="adv-m03",
            account_id="adv-acct-3",
            domain="adv-c.example",
            minute=130,
            narrative="official admits a secret covert attack",
        ),
        replace(
            synthetic,
            content_id="adv-m04",
            account_id="adv-acct-4",
            domain="adv-d.example",
            minute=134,
            narrative="secret covert attack admitted by official",
        ),
    ]


def adversarial_evaluation() -> dict[str, object]:
    items = _adversarial_items()
    clusters = cluster_campaigns(items)
    clustered_ids = {content_id for row in clusters for content_id in row.content_ids}
    covered = sum(item.content_id in clustered_ids for item in items)
    return {
        "cases": len(items),
        "clusters_detected": len(clusters),
        "items_clustered": covered,
        "synthetic_cluster_coverage": round(covered / len(items), 3),
        "clusters": [row.to_dict() for row in clusters],
        "meaning": "Paraphrase robustness exercise on synthetic risky narratives; not real-world influence-operation recall or actor attribution.",
    }


def evaluation_summary(items: list[EvidenceEnvelope] | None = None) -> dict[str, object]:
    baseline = list(items or ITEMS)
    shifted = simulate_shifted_narratives(baseline)
    return {
        "model_metadata": {
            "model": MODEL_NAME,
            "model_version": MODEL_VERSION,
            "feature_schema_version": FEATURE_SCHEMA_VERSION,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "steady_state_monitoring": narrative_drift_report(baseline, baseline),
        "synthetic_shift_monitoring": narrative_drift_report(baseline, shifted),
        "adversarial_evaluation": adversarial_evaluation(),
    }
