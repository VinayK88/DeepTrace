from __future__ import annotations

from collections import Counter

from .engine import DeepTraceEngine
from .fixtures import ITEMS


def build_report() -> dict:
    engine = DeepTraceEngine()
    assessments = [engine.assess(item) for item in ITEMS]
    campaigns = engine.detect_campaigns(ITEMS)
    matches = sum(a.verdict == item.expected_verdict for a, item in zip(assessments, ITEMS))
    counts = Counter(a.verdict for a in assessments)

    risky_ids = {"m03", "m04", "m05", "m06"}
    risky_caught = sum(
        a.content_id in risky_ids and a.verdict in {"LIKELY_MANIPULATED", "HIGH_RISK_SYNTHETIC"}
        for a in assessments
    )

    return {
        "summary": {
            "items": len(ITEMS),
            "expected_verdicts_matched": matches,
            "risky_media_flagged": risky_caught,
            "risky_media_total": len(risky_ids),
            "campaigns_detected": len(campaigns),
            "verdict_counts": dict(counts),
        },
        "assessments": [a.to_dict() for a in assessments],
        "campaigns": [c.to_dict() for c in campaigns],
    }
