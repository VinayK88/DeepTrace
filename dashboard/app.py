import streamlit as st

st.set_page_config(page_title="DeepTrace", page_icon="◉", layout="wide", initial_sidebar_state="expanded")

METRICS=[("Media items","8","synthetic"),("Verdicts matched","8 / 8","fixture"),("Risky flagged","4 / 4","fixture"),("Verified","2","synthetic"),("Likely manipulated","2","synthetic"),("High-risk synthetic","2","synthetic"),("Campaign findings","2","deterministic"),("ML clusters","2","illustrative"),("Modalities","3","image / video / audio"),("Evidence layers","5","provenance + forensic"),("External calls","0","offline"),("Production claims","0","synthetic only")]
SIGNALS=[("Provenance confidence",.86),("Forensic evidence",.78),("Semantic similarity",.82),("Temporal concentration",.69),("Account / domain diversity",.74)]

st.markdown("""<style>
html,body,[class*="css"]{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text","Helvetica Neue",Arial,sans-serif;color:#1d1d1f}.stApp{background:#f5f5f7}[data-testid="stHeader"]{background:transparent}[data-testid="stSidebar"]{background:#fff;border-right:1px solid #e5e5ea}.block-container{max-width:1500px;padding:2rem 2.4rem 4rem}.hero{background:linear-gradient(135deg,#fff,#f7fbff);border:1px solid #e5e5ea;border-radius:32px;padding:38px 42px;margin-bottom:24px;box-shadow:0 14px 36px rgba(0,0,0,.045)}.eyebrow{color:#0071e3;font-size:.78rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase}.hero h1{font-size:3.35rem;letter-spacing:-.052em;margin:.22rem 0 .55rem}.hero p{max-width:900px;color:#6e6e73;font-size:1.12rem;line-height:1.55}.pill{display:inline-block;background:#eef6ff;color:#0066cc;border:1px solid #d8eaff;border-radius:999px;padding:.42rem .78rem;margin:.55rem .35rem 0 0;font-size:.76rem;font-weight:650}[data-testid="stMetric"]{background:#fff;border:1px solid #e5e5ea;border-radius:24px;padding:18px 20px;box-shadow:0 8px 26px rgba(0,0,0,.035);min-height:116px}[data-testid="stMetricLabel"]{color:#6e6e73;font-weight:600}[data-testid="stMetricValue"]{font-size:1.9rem;font-weight:700}.stTabs [data-baseweb="tab"]{background:#fff;border:1px solid #e5e5ea;border-radius:999px;padding:8px 16px}.card{background:#fff;border:1px solid #e5e5ea;border-radius:22px;padding:18px 20px}.note{background:#fff;border:1px solid #e5e5ea;border-radius:18px;padding:14px 18px;color:#6e6e73}</style>""",unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## DeepTrace"); st.caption("Content Integrity Intelligence"); st.divider(); st.markdown("**Overview**\n\nIntegrity posture\n\nCampaign clusters\n\nEvidence fusion\n\nReview queue"); st.divider(); st.caption("Synthetic / offline evaluation")

st.markdown("""<div class="hero"><div class="eyebrow">Content Integrity Intelligence</div><h1>DeepTrace</h1><p>Provenance-aware media assessment and unsupervised narrative clustering for coordinated-content review.</p><span class="pill">Provenance</span><span class="pill">Media forensics</span><span class="pill">TF-IDF + DBSCAN</span><span class="pill">Campaign review</span></div>""",unsafe_allow_html=True)
for s in range(0,len(METRICS),4):
    cols=st.columns(4)
    for c,(l,v,n) in zip(cols,METRICS[s:s+4]): c.metric(l,v,n)

st.subheader("Integrity health")
l,r=st.columns([1.15,.85],gap="large")
with l:
    for name,val in SIGNALS: st.progress(val,text=f"{name} · {val:.0%}")
with r: st.markdown('<div class="card"><b>Evidence-first design</b><br><br><span style="color:#6e6e73">Missing provenance is not treated as proof of manipulation. Semantic clustering is gated by account, domain, temporal, and media-risk evidence.</span></div>',unsafe_allow_html=True)

t1,t2,t3,t4=st.tabs(["Integrity posture","Campaign clusters","Evidence fusion","Review queue"])
with t1: st.dataframe([{"Verdict":"VERIFIED","Count":2},{"Verdict":"LIKELY_MANIPULATED","Count":2},{"Verdict":"HIGH_RISK_SYNTHETIC","Count":2},{"Verdict":"LIKELY_AUTHENTIC","Count":1},{"Verdict":"INCONCLUSIVE","Count":1}],use_container_width=True,hide_index=True)
with t2: st.dataframe([{"Cluster":"ml-camp-01","Items":2,"Accounts":2,"Domains":2,"State":"Review"},{"Cluster":"ml-camp-02","Items":2,"Accounts":2,"Domains":2,"State":"Review"}],use_container_width=True,hide_index=True)
with t3:
    for name,val in SIGNALS: st.progress(val,text=name)
with t4: st.info("All media, narratives, domains, accounts, provenance states and forensic signals are synthetic. No real-world actor attribution is performed.")
st.markdown('<div class="note"><b>Evaluation boundary.</b> KPI values are synthetic fixture outputs or clearly labeled illustrative UI defaults, not production detector accuracy.</div>',unsafe_allow_html=True)
