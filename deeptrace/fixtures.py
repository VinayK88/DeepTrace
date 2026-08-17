from .models import EvidenceEnvelope

ITEMS = [
    EvidenceEnvelope(
        "m01", "image", "wire-service", True, True, True, True,
        0.98, 0.05, 0.04, "storm damages coastal bridge", "acct-news-1", "news.example", 5,
        "VERIFIED",
    ),
    EvidenceEnvelope(
        "m02", "video", "local-journalist", True, True, True, True,
        0.94, 0.08, 0.07, "storm damages coastal bridge", "acct-journalist", "local.example", 8,
        "VERIFIED",
    ),
    EvidenceEnvelope(
        "m03", "image", "social-upload", False, False, False, False,
        0.91, 0.34, 0.82, "bridge collapse caused by secret attack", "acct-x1", "mirror-a.example", 40,
        "LIKELY_MANIPULATED",
    ),
    EvidenceEnvelope(
        "m04", "image", "social-upload", False, False, False, False,
        0.89, 0.39, 0.86, "bridge collapse caused by secret attack", "acct-x2", "mirror-b.example", 44,
        "LIKELY_MANIPULATED",
    ),
    EvidenceEnvelope(
        "m05", "audio", "anonymous-upload", False, False, False, True,
        0.18, 0.93, 0.31, "official admits secret attack", "acct-x3", "mirror-a.example", 47,
        "HIGH_RISK_SYNTHETIC",
    ),
    EvidenceEnvelope(
        "m06", "video", "social-upload", False, False, False, True,
        0.22, 0.88, 0.46, "official admits secret attack", "acct-x4", "mirror-c.example", 50,
        "HIGH_RISK_SYNTHETIC",
    ),
    EvidenceEnvelope(
        "m07", "image", "citizen-upload", False, False, False, True,
        0.63, 0.21, 0.18, "storm response crews arrive", "acct-citizen", "social.example", 60,
        "LIKELY_AUTHENTIC",
    ),
    EvidenceEnvelope(
        "m08", "image", "reposted-screenshot", False, False, False, False,
        0.52, 0.44, 0.49, "storm response crews arrive", "acct-repost", "social.example", 72,
        "INCONCLUSIVE",
    ),
]
