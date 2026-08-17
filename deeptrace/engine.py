from __future__ import annotations

from collections import defaultdict

from .models import Assessment, CampaignFinding, EvidenceEnvelope


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


class DeepTraceEngine:
    """Deterministic evidence-fusion engine for synthetic media envelopes."""

    def assess(self, item: EvidenceEnvelope) -> Assessment:
        evidence: list[str] = []
        cautions: list[str] = []
        authenticity = 0.0
        risk = 0.0

        if item.c2pa_present and item.c2pa_valid and item.signer_trusted:
            authenticity += 0.52
            evidence.append("valid provenance credential from trusted synthetic signer")
        elif item.c2pa_present and not item.c2pa_valid:
            risk += 0.30
            cautions.append("provenance credential present but validation failed")
        else:
            cautions.append("no verifiable provenance credential in fixture")

        if item.metadata_consistent:
            authenticity += 0.12
            evidence.append("metadata is internally consistent")
        else:
            risk += 0.15
            cautions.append("metadata consistency check failed")

        if item.known_source_similarity >= 0.85:
            authenticity += 0.18
            evidence.append("strong similarity to a known-source asset")
        elif item.known_source_similarity >= 0.60:
            authenticity += 0.15
            evidence.append("moderate similarity to a known-source asset")
        elif item.known_source_similarity <= 0.30:
            risk += 0.08
            cautions.append("weak similarity to known-source assets")

        risk += 0.42 * item.synthetic_signal
        risk += 0.48 * item.manipulation_signal

        if item.synthetic_signal >= 0.80:
            evidence.append("high synthetic-media signal in fixture")
        if item.manipulation_signal >= 0.70:
            evidence.append("high manipulation signal in fixture")

        net = _clamp(risk - 0.45 * authenticity)
        risk_score = round(net * 100)

        if item.c2pa_valid and item.signer_trusted and authenticity >= 0.70 and net < 0.20:
            verdict = "VERIFIED"
            confidence = 0.96
        elif item.synthetic_signal >= 0.80 and net >= 0.45:
            verdict = "HIGH_RISK_SYNTHETIC"
            confidence = _clamp(0.70 + 0.25 * item.synthetic_signal)
        elif item.manipulation_signal >= 0.70 and net >= 0.40:
            verdict = "LIKELY_MANIPULATED"
            confidence = _clamp(0.68 + 0.25 * item.manipulation_signal)
        elif authenticity >= 0.25 and net < 0.25:
            verdict = "LIKELY_AUTHENTIC"
            confidence = _clamp(0.66 + 0.25 * authenticity)
        else:
            verdict = "INCONCLUSIVE"
            confidence = 0.58

        return Assessment(
            item.content_id,
            verdict,
            round(confidence, 3),
            risk_score,
            evidence or ["no single signal dominated the assessment"],
            cautions,
        )

    def detect_campaigns(self, items: list[EvidenceEnvelope]) -> list[CampaignFinding]:
        groups: dict[str, list[EvidenceEnvelope]] = defaultdict(list)
        for item in items:
            groups[item.narrative].append(item)

        findings: list[CampaignFinding] = []
        index = 1
        for narrative, group in groups.items():
            accounts = sorted({x.account_id for x in group})
            domains = sorted({x.domain for x in group})
            span = max(x.minute for x in group) - min(x.minute for x in group)
            risky = sum(1 for x in group if x.synthetic_signal >= 0.8 or x.manipulation_signal >= 0.7)

            temporal = 1.0 if span <= 15 else max(0.0, 1.0 - (span - 15) / 60)
            account_factor = min(1.0, len(accounts) / 4)
            risky_factor = min(1.0, risky / 2)
            score = round(0.45 * temporal + 0.30 * account_factor + 0.25 * risky_factor, 3)

            if len(accounts) >= 2 and score >= 0.62:
                findings.append(
                    CampaignFinding(
                        f"camp-{index:02d}", narrative, accounts, domains,
                        [x.content_id for x in group], span, score,
                    )
                )
                index += 1

        return sorted(findings, key=lambda x: x.coordination_score, reverse=True)
