from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Literal

Verdict = Literal[
    "VERIFIED",
    "LIKELY_AUTHENTIC",
    "INCONCLUSIVE",
    "LIKELY_MANIPULATED",
    "HIGH_RISK_SYNTHETIC",
]


@dataclass(frozen=True)
class EvidenceEnvelope:
    content_id: str
    media_type: str
    source: str
    c2pa_present: bool
    c2pa_valid: bool
    signer_trusted: bool
    metadata_consistent: bool
    known_source_similarity: float
    synthetic_signal: float
    manipulation_signal: float
    narrative: str
    account_id: str
    domain: str
    minute: int
    expected_verdict: Verdict


@dataclass
class Assessment:
    content_id: str
    verdict: Verdict
    confidence: float
    risk_score: int
    evidence: list[str] = field(default_factory=list)
    cautions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CampaignFinding:
    campaign_id: str
    narrative: str
    accounts: list[str]
    domains: list[str]
    content_ids: list[str]
    time_span_minutes: int
    coordination_score: float

    def to_dict(self) -> dict:
        return asdict(self)
