from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .engine import DeepTraceEngine
from .models import EvidenceEnvelope
from .report import build_report

app = FastAPI(title="DeepTrace", version="0.1.0")


@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "deeptrace"}


@app.get("/report")
def report():
    return build_report()


@app.post("/assess")
def assess(payload: dict):
    item = EvidenceEnvelope(**payload)
    return DeepTraceEngine().assess(item).to_dict()


@app.get("/", response_class=HTMLResponse)
def dashboard():
    report = build_report()
    summary = report["summary"]
    cards = [
        ("Media items", summary["items"]),
        ("Verdicts matched", f"{summary['expected_verdicts_matched']}/{summary['items']}"),
        ("Risky media flagged", f"{summary['risky_media_flagged']}/{summary['risky_media_total']}"),
        ("Campaigns", summary["campaigns_detected"]),
    ]
    card_html = "".join(
        f"<div class='card'><div class='value'>{v}</div><div class='label'>{k}</div></div>"
        for k, v in cards
    )
    rows = "".join(
        f"<tr><td>{x['content_id']}</td><td>{x['verdict']}</td><td>{x['confidence']:.3f}</td><td>{x['risk_score']}</td></tr>"
        for x in report["assessments"]
    )
    campaign_rows = "".join(
        f"<tr><td>{c['campaign_id']}</td><td>{c['narrative']}</td><td>{len(c['accounts'])}</td><td>{c['coordination_score']:.3f}</td></tr>"
        for c in report["campaigns"]
    )
    return f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
    <title>DeepTrace</title><style>
    body{{font-family:Inter,system-ui;background:#07111f;color:#e6edf7;margin:0}} .wrap{{max-width:1180px;margin:auto;padding:34px}}
    .hero{{background:linear-gradient(135deg,#0c1a2f,#101a33);border:1px solid #223553;border-radius:20px;padding:28px}}
    .hero h1{{margin:0 0 6px;font-size:34px}} .muted{{color:#94a3b8}} .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:20px 0}}
    .card{{background:#0d1728;border:1px solid #223553;border-radius:16px;padding:18px}} .value{{font-size:30px;font-weight:800}} .label{{color:#94a3b8;margin-top:5px}}
    .panel{{background:#0d1728;border:1px solid #223553;border-radius:16px;padding:18px;margin-top:18px}} table{{width:100%;border-collapse:collapse}} th,td{{padding:11px;text-align:left;border-bottom:1px solid #1f2e46}} th{{color:#7dd3fc}} @media(max-width:800px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
    </style></head><body><div class='wrap'><div class='hero'><h1>DeepTrace</h1><div class='muted'>Content authenticity, provenance & influence-analysis workbench</div><p>Fuse provenance, metadata, synthetic-media signals, source similarity, narrative recurrence and temporal coordination into auditable assessments.</p></div>
    <div class='grid'>{card_html}</div><div class='panel'><h2>Content assessments</h2><table><tr><th>ID</th><th>Verdict</th><th>Confidence</th><th>Risk</th></tr>{rows}</table></div>
    <div class='panel'><h2>Campaign findings</h2><table><tr><th>ID</th><th>Narrative</th><th>Accounts</th><th>Coordination</th></tr>{campaign_rows}</table></div></div></body></html>"""
