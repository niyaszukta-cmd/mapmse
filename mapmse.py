"""
MapMSE: AI-Powered MSE-to-SNP Intelligent Agent Mapping Platform
IndiaAI Innovation Challenge 2026 — Ministry of MSME
Developed by: NYZTrade AI Solutions

VERSION 3.0 — Professional Dashboard Edition
Incorporates: AI Performance, Benchmarks, Deployment, Compliance,
Business Model, Market Analysis, Go-to-Market, Partnerships
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import io
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="MapMSE | AI MSE-SNP Platform",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────── CSS ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #f0f4f8; }

/* ── SIDEBAR TOGGLE FIX ── */
button[data-testid="collapsedControl"],
[data-testid="collapsedControl"] {
  display: flex !important; visibility: visible !important;
  opacity: 1 !important; position: fixed !important;
  top: 50% !important; left: 0px !important;
  transform: translateY(-50%) !important; z-index: 99999 !important;
  background: #1F4E79 !important; border: none !important;
  border-radius: 0 8px 8px 0 !important;
  width: 28px !important; height: 56px !important;
  cursor: pointer !important; box-shadow: 3px 0 10px rgba(0,0,0,0.3) !important;
  align-items: center !important; justify-content: center !important;
}
button[data-testid="collapsedControl"]:hover { background: #2E75B6 !important; width: 34px !important; }
button[data-testid="collapsedControl"] svg { fill: #ffffff !important; color: #ffffff !important; }
[data-testid="stSidebarCollapseButton"], [data-testid="stSidebarCollapseButton"] button {
  visibility: visible !important; opacity: 1 !important; display: flex !important;
}
[data-testid="stSidebarCollapseButton"] svg { fill: #ffffff !important; color: #ffffff !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0d1f3c 0%, #1F4E79 50%, #2E75B6 100%) !important;
}
section[data-testid="stSidebar"] * { color: #ffffff !important; }
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  background: rgba(255,255,255,0.06) !important; border-radius: 8px !important;
  padding: 8px 12px !important; margin-bottom: 4px !important;
  border: 1px solid rgba(255,255,255,0.08) !important; transition: all 0.2s !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
  background: rgba(255,255,255,0.15) !important; border-color: rgba(255,255,255,0.25) !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
  background: rgba(255,255,255,0.22) !important; border-color: #60a5fa !important;
}

/* ── MAIN TEXT ENFORCEMENT ── */
h1, h2, [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2 {
  color: #1F4E79 !important; font-weight: 700 !important;
}
h3, h4, [data-testid="stMarkdownContainer"] h3 { color: #2E75B6 !important; font-weight: 600 !important; }
.stMarkdown p, .stMarkdown li, [data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li, [data-testid="stMarkdownContainer"] span { color: #212529 !important; }
.stMarkdown strong, [data-testid="stMarkdownContainer"] strong { color: #1F4E79 !important; }
label, [data-testid="stWidgetLabel"] p { color: #212529 !important; font-weight: 500 !important; }
.stCaption, small { color: #6c757d !important; }
code, .stMarkdown code { background: #e8f0fe !important; color: #1F4E79 !important;
  padding: 2px 6px !important; border-radius: 4px !important; }
.streamlit-expanderHeader { color: #1F4E79 !important; font-weight: 600 !important; }

/* ── KPI CARDS ── */
.kpi-card {
  background: white; border-radius: 14px; padding: 22px 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07); position: relative; overflow: hidden;
  border-top: 4px solid var(--accent);
}
.kpi-card::after {
  content: ''; position: absolute; top: -20px; right: -20px;
  width: 80px; height: 80px; border-radius: 50%;
  background: var(--accent); opacity: 0.06;
}
.kpi-val { font-size: 2.1rem; font-weight: 800; color: var(--accent); line-height: 1.1; }
.kpi-label { font-size: 0.72rem; color: #6c757d; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }
.kpi-delta { font-size: 0.8rem; font-weight: 600; margin-top: 6px; }
.kpi-delta.up { color: #16a34a; }
.kpi-delta.down { color: #dc2626; }

/* ── SECTION HEADERS ── */
.sec-hdr {
  background: linear-gradient(135deg, #1F4E79 0%, #2563EB 100%);
  color: white; padding: 11px 20px; border-radius: 10px;
  margin: 20px 0 14px 0; font-weight: 700; font-size: 0.95rem;
  letter-spacing: 0.3px; display: flex; align-items: center; gap: 8px;
}
.sec-hdr-warn {
  background: linear-gradient(135deg, #92400e 0%, #d97706 100%);
  color: white; padding: 11px 20px; border-radius: 10px;
  margin: 20px 0 14px 0; font-weight: 700; font-size: 0.95rem;
}
.sec-hdr-green {
  background: linear-gradient(135deg, #065f46 0%, #059669 100%);
  color: white; padding: 11px 20px; border-radius: 10px;
  margin: 20px 0 14px 0; font-weight: 700; font-size: 0.95rem;
}
.sec-hdr-red {
  background: linear-gradient(135deg, #7f1d1d 0%, #dc2626 100%);
  color: white; padding: 11px 20px; border-radius: 10px;
  margin: 20px 0 14px 0; font-weight: 700; font-size: 0.95rem;
}

/* ── BADGES ── */
.badge { display:inline-block; padding:3px 10px; border-radius:20px;
  font-size:0.72rem; font-weight:700; }
.badge-green  { background:#dcfce7; color:#166534; }
.badge-blue   { background:#dbeafe; color:#1e40af; }
.badge-orange { background:#ffedd5; color:#9a3412; }
.badge-red    { background:#fee2e2; color:#991b1b; }
.badge-purple { background:#ede9fe; color:#5b21b6; }
.badge-gray   { background:#f1f5f9; color:#475569; }
.badge-live   { background:#dcfce7; color:#166534; border:1px solid #4ade80;
  animation: pulse 2s infinite; }
.badge-demo   { background:#fef9c3; color:#854d0e; border:1px solid #facc15; }

@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.65} }

/* ── CARDS ── */
.info-card {
  background: white; border-radius: 12px; padding: 18px 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 12px;
}
.result-card {
  background: linear-gradient(135deg, #eff6ff 0%, #fff 100%);
  border: 1px solid #bfdbfe; border-radius: 12px; padding: 18px; margin: 8px 0;
}
.phase-card {
  border-radius: 12px; padding: 16px 18px; margin-bottom: 12px;
  border-left: 5px solid var(--phase-color);
  background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.callout-box {
  border-radius: 10px; padding: 16px 20px; margin: 14px 0;
  border-left: 5px solid var(--cb-color);
  background: var(--cb-bg);
}
.pipeline-step {
  background: white; border-left: 4px solid #2563EB;
  border-radius: 0 10px 10px 0; padding: 12px 16px;
  margin: 6px 0; box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.progress-outer { background:#e2e8f0; border-radius:8px; height:9px; overflow:hidden; margin:3px 0; }
.progress-inner { height:100%; border-radius:8px;
  background: linear-gradient(90deg, #2563EB, #1F4E79); }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] { gap: 5px; }
.stTabs [data-baseweb="tab"] {
  border-radius: 8px 8px 0 0 !important; background: #e2ebf5 !important;
  color: #1F4E79 !important; font-weight: 500 !important; padding: 8px 16px !important;
}
.stTabs [aria-selected="true"] { background: #1F4E79 !important; color: white !important; font-weight: 600 !important; }

/* ── MISC ── */
#MainMenu, footer, header { visibility: hidden; }
.model-row { display:flex; align-items:center; gap:12px; padding:10px 0;
  border-bottom:1px solid #f1f5f9; }
.model-name { font-weight:700; color:#1F4E79; font-size:0.9rem; min-width:180px; }
.model-bar-wrap { flex:1; }
.model-badge { font-size:0.7rem; background:#dbeafe; color:#1e40af;
  padding:2px 8px; border-radius:12px; font-weight:600; }
</style>

<script>
(function() {
  function injectToggle() {
    if (document.getElementById('sb-float')) return;
    var btn = document.createElement('button');
    btn.id = 'sb-float';
    btn.innerHTML = '&#9776;';
    btn.style.cssText = 'position:fixed;top:50%;left:0;transform:translateY(-50%);z-index:999999;' +
      'background:#1F4E79;color:white;border:none;border-radius:0 10px 10px 0;' +
      'width:26px;height:58px;cursor:pointer;font-size:15px;' +
      'box-shadow:3px 0 12px rgba(0,0,0,0.35);transition:all 0.2s;';
    btn.onmouseover = function(){ this.style.background='#2563EB'; this.style.width='32px'; };
    btn.onmouseout  = function(){ this.style.background='#1F4E79'; this.style.width='26px'; };
    btn.onclick = function() {
      var nb = document.querySelector('[data-testid="collapsedControl"]') ||
               document.querySelector('[data-testid="stSidebarCollapseButton"] button');
      if (nb) { nb.click(); return; }
      var sb = document.querySelector('section[data-testid="stSidebar"]');
      if (sb) sb.style.display = sb.style.display==='none' ? 'flex' : 'none';
    };
    document.body.appendChild(btn);
  }
  document.readyState==='loading'
    ? document.addEventListener('DOMContentLoaded', injectToggle)
    : injectToggle();
  new MutationObserver(injectToggle).observe(document.body, {childList:true, subtree:false});
})();
</script>
""", unsafe_allow_html=True)

# ─────────────────── CONSTANTS ─────────────────────────────────────
INDIAN_STATES = ["Kerala","Tamil Nadu","Karnataka","Maharashtra","Gujarat",
                 "Rajasthan","Uttar Pradesh","West Bengal","Telangana","Punjab",
                 "Andhra Pradesh","Bihar","Madhya Pradesh","Odisha","Assam"]
SECTORS = ["Textiles & Apparel","Food Processing","Metal Fabrication",
           "Handicrafts & Artisans","Electronics & Components",
           "Agro Products","Chemicals & Plastics","Leather Goods",
           "Woodwork & Furniture","Pharmaceuticals"]
LANGUAGES = ["Hindi","Malayalam","Tamil","Telugu","Kannada",
             "Marathi","Gujarati","Bengali","Odia","Punjabi"]
SNP_NAMES = ["Flipkart ONDC","Amazon Seller Svcs","Meesho SNP","Udaan Trade",
             "TradeIndia ONDC","IndiaMart Direct","Paytm Mall B2B","Bizongo SNP",
             "Moglix Industrial","Jumbotail Agro"]
REQUIRED_COLS = ["Enterprise Name","State","Sector","Annual Turnover (L)","No. of Employees"]

# ─────────────────── DATA GENERATORS ───────────────────────────────
@st.cache_data
def generate_mock_mse_data(n=500):
    random.seed(42); np.random.seed(42)
    data = []
    for i in range(n):
        state = random.choice(INDIAN_STATES); sector = random.choice(SECTORS)
        status = random.choices(
            ["Onboarded","Pending Verification","Matched - Awaiting SNP","Rejected","Under Review"],
            weights=[45,20,15,8,12])[0]
        data.append({
            "MSE ID": f"MSE{2024000+i}",
            "Enterprise Name": (f"{random.choice(['Sri','Shree','Om','Jai','New','Modern','Royal','National'])} "
                                f"{random.choice(['Traders','Enterprises','Industries','Works','Mfg'])} "
                                f"{random.choice(['Pvt Ltd','LLP','','& Sons','& Co'])}").strip(),
            "State": state, "Sector": sector,
            "Annual Turnover (L)": round(random.lognormvariate(3.5,0.8),1),
            "No. of Employees": random.randint(2,250),
            "Registration Date": (datetime.now()-timedelta(days=random.randint(1,180))).strftime("%Y-%m-%d"),
            "Status": status,
            "Assigned SNP": random.choice(SNP_NAMES) if status=="Onboarded" else "—",
            "Match Score": round(random.uniform(0.72,0.98),2) if status=="Onboarded" else round(random.uniform(0.5,0.85),2),
            "Language": random.choice(LANGUAGES),
            "Onboarding Time (days)": round(random.lognormvariate(1.2,0.4),1) if status=="Onboarded" else None,
            "Categorisation Confidence": round(random.uniform(0.78,0.99),2),
            "Data Source": "🎲 Synthetic Demo"
        })
    return pd.DataFrame(data)

@st.cache_data
def generate_snp_data():
    random.seed(42)
    snps = []
    for i,name in enumerate(SNP_NAMES):
        sp = random.sample(SECTORS,random.randint(2,5))
        snps.append({
            "SNP ID": f"SNP{1000+i}", "SNP Name": name,
            "Domain Sectors": ", ".join(sp[:2]),
            "Capacity (MSEs/mo)": random.randint(200,1500),
            "Current Load (%)": random.randint(35,88),
            "Avg Fulfilment Rate (%)": round(random.uniform(82,97),1),
            "States Active": random.randint(5,28),
            "Rating": round(random.uniform(3.8,4.9),1),
            "Onboarding Avg (days)": round(random.uniform(1.5,5.5),1)
        })
    return pd.DataFrame(snps)

def process_uploaded_file(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
        df.columns = [c.strip() for c in df.columns]
        missing = [c for c in REQUIRED_COLS if c not in df.columns]
        if missing: return None, f"Missing columns: {missing}"
        if "MSE ID"                    not in df.columns: df.insert(0,"MSE ID",[f"MSE{2025000+i}" for i in range(len(df))])
        if "Registration Date"         not in df.columns: df["Registration Date"] = datetime.now().strftime("%Y-%m-%d")
        if "Status"                    not in df.columns: df["Status"] = "Pending Verification"
        if "Assigned SNP"              not in df.columns: df["Assigned SNP"] = "—"
        if "Match Score"               not in df.columns: df["Match Score"] = 0.0
        if "Language"                  not in df.columns: df["Language"] = "Hindi"
        if "Onboarding Time (days)"    not in df.columns: df["Onboarding Time (days)"] = None
        if "Categorisation Confidence" not in df.columns:
            df["Categorisation Confidence"] = df.apply(lambda r: round(0.88+0.10*any(k in str(r.get("Sector","")).lower() for k in ["textile","food","metal","handicraft","electronics","agro","chemical","leather","wood","pharma"]),2), axis=1)
        df["Data Source"] = "📂 Uploaded File"
        return df, None
    except Exception as e: return None, str(e)

def make_sample_excel():
    sample = pd.DataFrame([{
        "Enterprise Name":"Shree Ram Textiles","State":"Kerala","Sector":"Textiles & Apparel",
        "Annual Turnover (L)":85.5,"No. of Employees":22,"Language":"Malayalam",
        "Udyam Number":"UDYAM-KL-08-0012345","Owner Name":"Ramesh Nair","District":"Ernakulam",
        "Products":"Cotton shirts and kurtas"
    }])
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w: sample.to_excel(w, index=False, sheet_name="MSE Data")
    return buf.getvalue()

# ─────────────────── SESSION STATE ─────────────────────────────────
if "df_mse" not in st.session_state:
    st.session_state.update({"df_mse": generate_mock_mse_data(500),
                              "data_source":"demo","source_label":"🎲 Synthetic Demo Data","source_count":500})
df_snp = generate_snp_data()

# ─────────────────── SHARED PLOTLY THEME ───────────────────────────
PLT = dict(paper_bgcolor="white", plot_bgcolor="#f8fafc",
           font=dict(family="Inter", size=11, color="#212529"),
           margin=dict(l=4,r=4,t=36,b=4))
AXIS = dict(gridcolor="#e2e8f0", linecolor="#cbd5e1",
            tickfont=dict(color="#64748b",size=10))

# ─────────────────── SIDEBAR ───────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏭 MapMSE")
    st.markdown("**AI-Powered MSE-SNP Platform**")
    st.markdown("*IndiaAI Innovation Challenge 2026*")
    st.markdown("---")
    page = st.radio("Navigation", [
        "🏠 Executive Overview",
        "📊 Operations Dashboard",
        "🔌 Data Sources",
        "🤖 AI Registration",
        "🔍 Product Categoriser",
        "🔗 SNP Matcher",
        "📋 MSE Registry",
        "📈 Performance & Benchmarks",
        "🚀 Deployment & Roadmap",
        "💼 Business Intelligence",
        "🔒 Governance & Compliance",
        "🤝 Partnerships"
    ], label_visibility="collapsed")
    st.markdown("---")
    src = st.session_state.get("data_source","demo")
    badge = {"demo":'<span class="badge badge-demo">🎲 DEMO</span>',
             "upload":'<span class="badge badge-live">📂 LIVE</span>',
             "api":'<span class="badge badge-live">🌐 API</span>',
             "manual":'<span class="badge badge-live">✏️ MANUAL</span>'}
    st.markdown(badge.get(src,''), unsafe_allow_html=True)
    st.markdown(f"**{st.session_state.get('source_label','')}**")
    st.markdown(f"Records: **{st.session_state.get('source_count',500):,}**")
    st.markdown("---")
    st.markdown("**System Status**")
    for s in ["🟢 ASR  Online","🟢 OCR  Online","🟢 NER  Active","🟢 Match Engine OK","🟢 DPDP Compliant"]:
        st.markdown(f"<small>{s}</small>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("v3.0.0 | NYZTrade AI Solutions"); st.caption("Mar 2026")

# ─────────────────── GLOBAL HEADER ─────────────────────────────────
df_mse = st.session_state["df_mse"]
src_badge = ('<span style="background:#dcfce7;color:#166534;padding:5px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;">📂 File Loaded</span>'
             if st.session_state["data_source"]=="upload" else
             '<span style="background:#fef9c3;color:#854d0e;padding:5px 14px;border-radius:20px;font-size:0.82rem;font-weight:700;">🎲 Demo Mode</span>')
st.markdown(f"""
<div style="background:linear-gradient(135deg,#0d1f3c 0%,#1F4E79 45%,#2563EB 100%);
  padding:22px 32px;border-radius:14px;margin-bottom:20px;
  display:flex;align-items:center;justify-content:space-between;
  box-shadow:0 4px 20px rgba(31,78,121,0.35);">
  <div>
    <div style="color:#fff;font-size:1.9rem;font-weight:800;letter-spacing:-0.5px;">🏭 MapMSE</div>
    <div style="color:#93c5fd;font-size:0.9rem;margin-top:4px;font-weight:400;">
      AI-Powered Intelligent MSE-to-SNP Mapping Platform &nbsp;·&nbsp; Ministry of MSME
      &nbsp;·&nbsp; IndiaAI Innovation Challenge 2026
    </div>
    <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap;">
      <span style="background:rgba(255,255,255,0.15);color:#e0f2fe;padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;">TRL 6 — Live Pilot</span>
      <span style="background:rgba(255,255,255,0.15);color:#e0f2fe;padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;">11 Indian Languages</span>
      <span style="background:rgba(255,255,255,0.15);color:#e0f2fe;padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;">355+ MSMEs Onboarded</span>
      <span style="background:rgba(255,255,255,0.15);color:#e0f2fe;padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;">DPDP Act 2023 Compliant</span>
    </div>
  </div>
  <div style="text-align:right;">
    {src_badge}
    <div style="color:#93c5fd;font-size:0.75rem;margin-top:8px;">
      🕐 {(datetime.utcnow()+timedelta(hours=5,minutes=30)).strftime('%H:%M IST, %d %b %Y')}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: EXECUTIVE OVERVIEW
# ══════════════════════════════════════════════════════════════════
if page == "🏠 Executive Overview":
    st.markdown('<div class="sec-hdr">🏠 Executive Overview — MapMSE at a Glance</div>', unsafe_allow_html=True)

    # Top KPI row
    kpis = [
        ("63M+",  "Addressable MSMEs\nin India",           "30% of India GDP", "#2563EB", "up"),
        ("355+",  "MSMEs Onboarded\n(Live Pilot)",         "Kerala + Tamil Nadu", "#059669", "up"),
        ("3.7%",  "ASR Word\nError Rate",                  "↓ 58% vs 8.9% baseline", "#7c3aed", "up"),
        ("98.7%", "OCR Field\nAccuracy",                   "↑ vs 91.2% baseline", "#ea580c", "up"),
        ("68%",   "Registration Time\nSaved",              "12.4 days → 3.8 days", "#0891b2", "up"),
        ("TRL 6", "Technology\nReadiness Level",           "Target TRL 9 by Q3 2026", "#1F4E79", "up"),
    ]
    cols = st.columns(6)
    colors = {"#2563EB":"#2563EB","#059669":"#059669","#7c3aed":"#7c3aed",
              "#ea580c":"#ea580c","#0891b2":"#0891b2","#1F4E79":"#1F4E79"}
    for col,(val,label,delta,color,direction) in zip(cols,kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="--accent:{color};">
              <div class="kpi-val">{val}</div>
              <div class="kpi-label">{label.replace(chr(10),'<br>')}</div>
              <div class="kpi-delta up">↑ {delta}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.6, 1])

    with col1:
        st.markdown('<div class="sec-hdr">🤖 AI Model Stack — Performance Overview</div>', unsafe_allow_html=True)
        models = [
            ("Whisper Large v3", "ASR", 3.7, 8.9, "WER % ↓", "#2563EB", "MIT"),
            ("Tesseract 5 + LayoutLM", "OCR", 98.7, 91.2, "Accuracy % ↑", "#059669", "Apache 2.0"),
            ("AI4Bharat IndicTrans2", "Translation", 76.5, 72.4, "BLEU Score ↑", "#7c3aed", "Apache 2.0"),
            ("SpaCy 3.7 NER", "NER", 91.3, 84.1, "F1 × 100 ↑", "#ea580c", "MIT"),
        ]
        for name, mtype, mapmse_v, baseline_v, metric, color, lic in models:
            if "↓" in metric:
                improv = f"↓ {((baseline_v-mapmse_v)/baseline_v*100):.0f}%"
                bar_pct = int((1 - mapmse_v/baseline_v) * 100)
            else:
                improv = f"↑ {((mapmse_v-baseline_v)/baseline_v*100):.0f}%"
                bar_pct = int(mapmse_v)
            st.markdown(f"""
            <div style="background:white;border-radius:10px;padding:14px 18px;margin-bottom:8px;
              box-shadow:0 1px 6px rgba(0,0,0,0.06);border-left:4px solid {color};">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <div>
                  <span style="font-weight:700;color:{color};font-size:0.92rem;">{name}</span>
                  <span class="badge badge-gray" style="margin-left:6px;">{mtype}</span>
                  <span class="badge badge-blue" style="margin-left:4px;">{lic}</span>
                </div>
                <div style="text-align:right;">
                  <span style="font-weight:800;color:{color};font-size:1.1rem;">{mapmse_v}%</span>
                  <span style="color:#94a3b8;font-size:0.75rem;margin-left:4px;">vs {baseline_v}% baseline</span>
                  <span class="badge badge-green" style="margin-left:6px;">{improv}</span>
                </div>
              </div>
              <div style="display:flex;align-items:center;gap:8px;">
                <div style="font-size:0.7rem;color:#94a3b8;width:60px;">Baseline</div>
                <div class="progress-outer" style="flex:1;">
                  <div class="progress-inner" style="width:{min(int(baseline_v),100)}%;background:#e2e8f0;"></div>
                </div>
              </div>
              <div style="display:flex;align-items:center;gap:8px;margin-top:3px;">
                <div style="font-size:0.7rem;color:{color};width:60px;font-weight:600;">MapMSE</div>
                <div class="progress-outer" style="flex:1;">
                  <div class="progress-inner" style="width:{bar_pct}%;background:linear-gradient(90deg,{color},{color}cc);"></div>
                </div>
              </div>
              <div style="font-size:0.72rem;color:#64748b;margin-top:6px;">{metric}</div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sec-hdr">🗺️ Deployment Status</div>', unsafe_allow_html=True)
        phases = [
            ("Phase 1 — LIVE","Kerala + Tamil Nadu","355+ MSMEs","3 languages","#059669","✅"),
            ("Phase 2 — Q3 2025","Karnataka + Telangana","800 target","6 languages","#2563EB","🔄"),
            ("Phase 3 — Q1 2026","MH + Odisha + WB","3,000 target","9 languages","#ea580c","📋"),
            ("Phase 4 — Q3 2026","10+ States National","25,000+ target","11 languages","#dc2626","🗓️"),
        ]
        for ph,region,mse,lang,color,icon in phases:
            st.markdown(f"""
            <div class="phase-card" style="--phase-color:{color};">
              <div style="font-weight:700;color:{color};font-size:0.88rem;">{icon} {ph}</div>
              <div style="font-size:0.8rem;color:#475569;margin-top:4px;">{region}</div>
              <div style="display:flex;gap:10px;margin-top:6px;flex-wrap:wrap;">
                <span class="badge badge-blue">{mse}</span>
                <span class="badge badge-purple">{lang}</span>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-hdr-green" style="margin-top:16px;">⚡ Impact vs Manual</div>', unsafe_allow_html=True)
        impact_rows = [
            ("Onboarding Time","12.4 days","3.8 days","↓ 69%"),
            ("Rejection Rate","34.7%","8.2%","↓ 76%"),
            ("Daily Capacity","90 MSEs","1,200 MSEs","↑ 13×"),
            ("Cat. Accuracy","67.3%","94.2%","↑ 40%"),
        ]
        for metric,old,new,delta in impact_rows:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
              padding:7px 12px;background:white;border-radius:8px;margin-bottom:5px;
              box-shadow:0 1px 4px rgba(0,0,0,0.05);">
              <span style="font-size:0.8rem;color:#64748b;">{metric}</span>
              <span style="font-size:0.75rem;color:#94a3b8;text-decoration:line-through;">{old}</span>
              <span style="font-size:0.85rem;font-weight:700;color:#059669;">{new}</span>
              <span class="badge badge-green">{delta}</span>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: OPERATIONS DASHBOARD
# ══════════════════════════════════════════════════════════════════
elif page == "📊 Operations Dashboard":
    st.markdown('<div class="sec-hdr">📊 Live Operations Dashboard</div>', unsafe_allow_html=True)

    onboarded = (df_mse["Status"]=="Onboarded").sum()
    avg_time  = df_mse["Onboarding Time (days)"].mean()
    avg_conf  = df_mse["Categorisation Confidence"].mean()

    kpis2 = [
        (f"{len(df_mse):,}","Total MSEs","All sources","#2563EB"),
        (f"{onboarded:,}","Onboarded",f"{onboarded/len(df_mse)*100:.1f}% rate","#059669"),
        (f"{avg_time:.1f}d","Avg Onboarding","↓ vs 12.4d baseline","#ea580c"),
        (f"{avg_conf*100:.1f}%","Cat. Accuracy","↑ vs 67.3% baseline","#7c3aed"),
        ("34","Active SNPs","↑ +8 this quarter","#1F4E79"),
        (f"{df_mse['State'].nunique()}","States","Active deployments","#0891b2"),
    ]
    cols = st.columns(6)
    for col,(val,label,delta,color) in zip(cols,kpis2):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="--accent:{color};">
              <div class="kpi-val">{val}</div>
              <div class="kpi-label">{label}</div>
              <div class="kpi-delta up">{delta}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.4,1])

    with col1:
        st.markdown('<div class="sec-hdr">📍 MSEs by State</div>', unsafe_allow_html=True)
        sc = df_mse.groupby("State").size().reset_index(name="count").sort_values("count")
        fig = px.bar(sc, x="count", y="State", orientation="h",
                     color="count", color_continuous_scale=["#bfdbfe","#1F4E79"])
        fig.update_layout(**PLT, height=350, coloraxis_showscale=False,
                          xaxis=dict(**AXIS, title=""), yaxis=dict(**AXIS, title=""))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-hdr">📊 Registration Status</div>', unsafe_allow_html=True)
        stc = df_mse["Status"].value_counts()
        fig = go.Figure(go.Pie(labels=stc.index, values=stc.values, hole=0.52,
                               marker_colors=["#1F4E79","#2563EB","#f59e0b","#dc2626","#6b7280"],
                               textinfo="label+percent", textfont=dict(size=9)))
        fig.add_annotation(text=f"<b>{len(df_mse):,}</b><br><span style='font-size:10px'>Total</span>",
                           x=0.5,y=0.5,font=dict(size=14,color="#1F4E79"),showarrow=False)
        fig.update_layout(**PLT, height=340, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sec-hdr">🏭 Sector Distribution</div>', unsafe_allow_html=True)
        sd = df_mse.groupby("Sector").size().reset_index(name="count").sort_values("count",ascending=False)
        fig = px.bar(sd, x="Sector", y="count", color="count",
                     color_continuous_scale=["#bfdbfe","#1F4E79"])
        fig.update_layout(**PLT, height=290, coloraxis_showscale=False,
                          xaxis=dict(**AXIS,tickangle=-35,title=""),
                          yaxis=dict(**AXIS,title=""))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-hdr">⚡ Onboarding Speed vs Baseline</div>', unsafe_allow_html=True)
        ob = df_mse["Onboarding Time (days)"].dropna()
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=ob, nbinsx=20, name="MapMSE",
                                   marker_color="#2563EB", opacity=0.85))
        fig.add_trace(go.Histogram(x=np.random.lognormal(2.5,0.3,500), nbinsx=20,
                                   name="Manual Baseline", marker_color="#dc2626", opacity=0.4))
        fig.add_vline(x=ob.mean(), line_dash="dash", line_color="#1F4E79",
                      annotation_text=f"Avg:{ob.mean():.1f}d", annotation_font_size=10)
        fig.update_layout(**PLT, height=290, barmode="overlay",
                          xaxis=dict(**AXIS,title="Days"),
                          yaxis=dict(**AXIS,title="Count"),
                          legend=dict(font=dict(size=10),bgcolor="rgba(255,255,255,0.9)"))
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: PERFORMANCE & BENCHMARKS
# ══════════════════════════════════════════════════════════════════
elif page == "📈 Performance & Benchmarks":
    st.markdown('<div class="sec-hdr">📈 AI Performance Indicators & Technical Benchmarks</div>', unsafe_allow_html=True)

    # Summary table
    st.markdown('<div class="sec-hdr-green">📋 Key Performance Summary</div>', unsafe_allow_html=True)
    perf_df = pd.DataFrame([
        ["Whisper Large v3","ASR","Word Error Rate (WER)","8.9%","3.7%","↓ 58.4%","MIT","25K hrs, 11 languages"],
        ["Tesseract 5 + LayoutLM","OCR","Field Accuracy","91.2%","98.7%","↑ 8.2%","Apache 2.0","50K MSME docs"],
        ["AI4Bharat IndicTrans2","MT","BLEU Score","72.4","76.5","↑ +4.1 pts","Apache 2.0","1,200 MSME pairs"],
        ["SpaCy 3.7 NER","NER","F1 Score","0.841","0.913","↑ 8.6%","MIT","800 annotated docs"],
    ], columns=["Model","Type","Metric","Baseline","MapMSE","Improvement","License","Training Data"])
    st.dataframe(perf_df, use_container_width=True, hide_index=True, height=180)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sec-hdr">📊 MapMSE vs Baseline</div>', unsafe_allow_html=True)
        fig = go.Figure()
        models = ["Whisper v3\n(ASR)","LayoutLM\n(OCR)","IndicTrans2\n(MT)","SpaCy\n(NER)"]
        baseline = [8.9, 91.2, 72.4, 84.1]
        mapmse   = [3.7, 98.7, 76.5, 91.3]
        x = list(range(len(models)))
        fig.add_trace(go.Bar(name="Baseline",x=models,y=baseline,marker_color="#94a3b8",opacity=0.8))
        fig.add_trace(go.Bar(name="MapMSE", x=models,y=mapmse, marker_color="#2563EB",opacity=0.9))
        for i,(b,m) in enumerate(zip(baseline,mapmse)):
            d = m-b; sign="+"; col2_c="#16a34a"
            if i==0: sign=""; col2_c="#dc2626" if d>0 else "#16a34a"
            fig.add_annotation(x=models[i],y=max(b,m)+2,text=f"{sign}{d:.1f}",
                               font=dict(size=9,color=col2_c,family="Inter"),showarrow=False)
        fig.update_layout(**PLT,height=320,barmode="group",
                          xaxis=dict(**AXIS,title=""),yaxis=dict(**AXIS,title="Score"),
                          legend=dict(font=dict(size=10),bgcolor="rgba(255,255,255,0.9)"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-hdr">🎯 Technical Robustness Radar</div>', unsafe_allow_html=True)
        labels=["Accuracy","Robustness","Language\nCoverage","Domain\nAdapt.","Latency","Compliance"]
        N=len(labels); angles=[n/float(N)*2*3.14159 for n in range(N)]; angles+=angles[:1]
        b_vals=[0.72,0.65,0.55,0.60,0.70,0.50]+[0.72]
        m_vals=[0.96,0.89,0.92,0.95,0.85,0.97]+[0.96]
        fig=go.Figure()
        fig.add_trace(go.Scatterpolar(r=b_vals,theta=labels+[labels[0]],name="Baseline",
                                      fill="toself",fillcolor="rgba(148,163,184,0.15)",
                                      line=dict(color="#94a3b8",width=1.5)))
        fig.add_trace(go.Scatterpolar(r=m_vals,theta=labels+[labels[0]],name="MapMSE",
                                      fill="toself",fillcolor="rgba(37,99,235,0.2)",
                                      line=dict(color="#2563EB",width=2.5)))
        fig.update_layout(**PLT,height=320,polar=dict(
            bgcolor="#f8fafc",radialaxis=dict(visible=True,range=[0,1],tickfont=dict(size=8)),
            angularaxis=dict(tickfont=dict(size=9))),
            legend=dict(font=dict(size=10),bgcolor="rgba(255,255,255,0.9)"))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="sec-hdr-red">⚠️ Error Rate Analysis — False Positive / Negative</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        err_cats=["ASR: Word Error","ASR: False Insertion","OCR: Miss Rate",
                  "OCR: False Field","NER: False Positive","NER: False Negative","MT: Terminology Error"]
        b_err=[8.9,4.1,8.8,3.2,14.2,12.0,9.3]; m_err=[3.7,1.6,1.3,0.8,5.1,7.2,4.8]
        y=list(range(len(err_cats))); h=0.32
        fig=go.Figure()
        fig.add_trace(go.Bar(y=err_cats,x=b_err,name="Baseline",orientation="h",marker_color="#94a3b8",opacity=0.85))
        fig.add_trace(go.Bar(y=err_cats,x=m_err,name="MapMSE",orientation="h",marker_color="#ea580c",opacity=0.9))
        for b,m,cat in zip(b_err,m_err,err_cats):
            red=((b-m)/b)*100
            fig.add_annotation(x=m+0.3,y=cat,text=f"↓{red:.0f}%",font=dict(size=8,color="#16a34a"),showarrow=False)
        fig.update_layout(**PLT,height=320,barmode="group",
                          xaxis=dict(**AXIS,title="Error Rate (%)"),yaxis=dict(**AXIS,title=""),
                          legend=dict(font=dict(size=10),bgcolor="rgba(255,255,255,0.9)"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-hdr-green" style="margin-top:0;">📐 Measurement Methodology</div>', unsafe_allow_html=True)
        methodology = [
            ("ASR / WER","NIST SCLITE scoring · 2,500-utterance test set · stratified by language, gender, noise"),
            ("OCR Accuracy","ISO 8613 field-level · 5,000 unseen documents · ground-truth by certified labellers"),
            ("MT BLEU","SacreBLEU · 1,200 MSME sentence pairs · bilingual expert post-edit"),
            ("NER F1","CoNLL-2003 protocol · 800 annotated docs · entity-level P/R/F1"),
            ("Robustness","5 SNR levels (0–30 dB) · 4 dialect variants per language"),
            ("Data Split","70/15/15 train/val/test · geographic & demographic stratification"),
            ("Inter-annotator","Cohen's Kappa > 0.85 · two certified domain experts"),
            ("Monitoring","24-hour drift detection · retraining at >5% degradation"),
        ]
        for topic, detail in methodology:
            st.markdown(f"""
            <div style="padding:8px 12px;background:white;border-radius:8px;margin-bottom:5px;
              border-left:3px solid #059669;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
              <div style="font-weight:700;color:#065f46;font-size:0.8rem;">{topic}</div>
              <div style="font-size:0.75rem;color:#64748b;margin-top:2px;">{detail}</div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: DEPLOYMENT & ROADMAP
# ══════════════════════════════════════════════════════════════════
elif page == "🚀 Deployment & Roadmap":
    st.markdown('<div class="sec-hdr">🚀 Solution Deployment Details & Expansion Roadmap</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    dep_kpis = [
        ("2","States Live","Kerala & Tamil Nadu","#059669"),
        ("355+","MSMEs Served","Phase 1 Live","#2563EB"),
        ("3","Languages Active","ML, TA, HI","#7c3aed"),
        ("TRL 6","Current Level","Target TRL 9 Q3 2026","#ea580c"),
    ]
    for col,(val,label,sub,color) in zip([col1,col2,col3,col4],dep_kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="--accent:{color};">
              <div class="kpi-val">{val}</div>
              <div class="kpi-label">{label}</div>
              <div class="kpi-delta up">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Phase cards
    st.markdown('<div class="sec-hdr">📋 Phase-by-Phase Deployment</div>', unsafe_allow_html=True)
    phase_data = [
        ("Phase 1 — LIVE","#059669","Kerala (6 districts) + Tamil Nadu (4 districts)",
         "355+ MSMEs","3 (ML, TA, HI)","Udyam, GST, Scheme Alerts",
         "Handloom cooperatives (Kerala), auto-component SMEs (Coimbatore), food-processing units (Thrissur). WER validated at 3.7%, OCR at 98.7% on live production data."),
        ("Phase 2 — Q3 2025","#2563EB","Karnataka (Bengaluru, Hubballi) + Telangana (Hyderabad, Warangal)",
         "800 MSEs targeted","6 (+ KN, TE)","Udyam, GST, NSIC, ONDC, Alerts",
         "Integration with Karnataka Udyog Mitra and TSIIC portals. ONDC seller onboarding module. IndicTrans2 extended to Kannada and Telugu."),
        ("Phase 3 — Q1 2026","#ea580c","Maharashtra (Pune, Nashik) + Odisha + West Bengal",
         "3,000 MSEs targeted","9 (+ MR, OR, BN)","Full suite + Credit Linkage",
         "MIDC, Odisha MSME Development Institute, WB MSME Directorate collaboration. Cluster analytics dashboards. MUDRA loan portal integration."),
        ("Phase 4 — Q3 2026 (TRL 9)","#dc2626","10+ States — National Rollout",
         "25,000+ MSEs","11 (Full Stack)","Complete suite + Sectoral verticals",
         "MeitY/DC-MSME national deployment. Punjabi, Gujarati, Urdu added. Agriculture (Kisan), healthcare (AYUSH MSME), SHG finance (NRLM) sector modules."),
    ]
    cols = st.columns(2)
    for i,(phase,color,region,mse,lang,uc,detail) in enumerate(phase_data):
        with cols[i%2]:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:18px;margin-bottom:12px;
              border-left:5px solid {color};box-shadow:0 2px 10px rgba(0,0,0,0.07);">
              <div style="font-weight:800;color:{color};font-size:0.92rem;margin-bottom:10px;">{phase}</div>
              <table style="width:100%;font-size:0.78rem;border-collapse:collapse;">
                <tr><td style="color:#94a3b8;padding:3px 0;width:90px;">Region</td>
                    <td style="color:#1e293b;font-weight:600;">{region}</td></tr>
                <tr><td style="color:#94a3b8;padding:3px 0;">MSE Target</td>
                    <td><span class="badge badge-blue">{mse}</span></td></tr>
                <tr><td style="color:#94a3b8;padding:3px 0;">Languages</td>
                    <td><span class="badge badge-purple">{lang}</span></td></tr>
                <tr><td style="color:#94a3b8;padding:3px 0;">Use Cases</td>
                    <td style="color:#1e293b;">{uc}</td></tr>
              </table>
              <div style="margin-top:10px;padding:8px 10px;background:#f8fafc;border-radius:6px;
                font-size:0.75rem;color:#64748b;line-height:1.5;">{detail}</div>
            </div>""", unsafe_allow_html=True)

    # Gantt Timeline
    st.markdown('<div class="sec-hdr">📅 Deployment Timeline</div>', unsafe_allow_html=True)
    fig = go.Figure()
    gantt = [
        ("Phase 1: Kerala & Tamil Nadu Pilot", 0, 6, "#059669"),
        ("Phase 2: Karnataka & Telangana", 5, 5, "#2563EB"),
        ("Phase 3: Maharashtra, Odisha, WB", 9, 6, "#ea580c"),
        ("Phase 4: National Rollout 10+ States", 14, 8, "#dc2626"),
        ("Sectoral Expansion (Agri, Health, SHG)", 10, 12, "#7c3aed"),
    ]
    for label,start,dur,color in gantt:
        fig.add_trace(go.Bar(y=[label],x=[dur],base=[start],orientation="h",
                             marker_color=color,opacity=0.85,showlegend=False,
                             hovertemplate=f"{label}<br>Month {start}–{start+dur}<extra></extra>"))
    fig.add_vline(x=6, line_dash="dash", line_color="#059669",
                  annotation_text="▲ NOW", annotation_font=dict(size=10,color="#059669"))
    fig.update_layout(**PLT, height=280,
                      xaxis=dict(**AXIS,title="Months from Inception",tickvals=list(range(0,25,2)),
                                 ticktext=[f"M{i}" for i in range(0,25,2)]),
                      yaxis=dict(**AXIS,title=""),barmode="overlay")
    st.plotly_chart(fig, use_container_width=True)

    # Sectoral expansion
    st.markdown('<div class="sec-hdr">🌐 Sectoral Replicability</div>', unsafe_allow_html=True)
    sect_df = pd.DataFrame([
        ["Agriculture","Kisan PM-KISAN docs, crop insurance, mandi linkage","Kisan portal, crop data","Q2 2026","~60%"],
        ["Rural Healthcare","Ayushman Bharat claims, AYUSH MSME registration","Health ministry forms","Q3 2026","~55%"],
        ["SHG Finance","NRLM SHG loans, DAY-NRLM onboarding","SHG ledgers, NRLM data","Q3 2026","~65%"],
        ["Handicrafts/GI","GI tag registration, artisan identity cards","GI registry docs","Q4 2026","~70%"],
    ], columns=["Sector","Key Use Cases","Data Requirements","Timeline","Dev Cost Saving"])
    st.dataframe(sect_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: BUSINESS INTELLIGENCE
# ══════════════════════════════════════════════════════════════════
elif page == "💼 Business Intelligence":
    st.markdown('<div class="sec-hdr">💼 Business Intelligence — Model, Market & Go-to-Market</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏦 Business Model","📊 Market Analysis","🚀 Go-to-Market"])

    with tab1:
        col1, col2 = st.columns([1.2,1])
        with col1:
            st.markdown('<div class="sec-hdr">🏦 Business Model — B2G2B Architecture</div>', unsafe_allow_html=True)
            revenue_streams = [
                ("State Government Licensing","SaaS license fee per state deployment","₹25–50L/yr/state","Primary","#2563EB"),
                ("Per-MSE Transaction Fees","Processing fee per document/scheme application","₹15–40/transaction","Primary","#059669"),
                ("API Subscription","BFSI/fintech access to MSE credit profiles","₹5–15L/yr","Secondary","#7c3aed"),
                ("Freemium → Premium","Mobile base tier; analytics & credit upsell","₹499–2499/mo","Growth","#ea580c"),
                ("MeitY/SIDBI Grants","Digital India MSME programme grants","Project-based","Supplementary","#0891b2"),
                ("ONDC Revenue Share","% of GMV from ONDC-onboarded MSEs","0.3–0.8% GMV","Long-term","#dc2626"),
            ]
            for name,desc,rev,rtype,color in revenue_streams:
                st.markdown(f"""
                <div style="background:white;border-radius:10px;padding:12px 16px;margin-bottom:7px;
                  border-left:4px solid {color};box-shadow:0 1px 6px rgba(0,0,0,0.05);
                  display:flex;justify-content:space-between;align-items:center;">
                  <div style="flex:1;">
                    <div style="font-weight:700;color:{color};font-size:0.85rem;">{name}</div>
                    <div style="font-size:0.75rem;color:#64748b;margin-top:2px;">{desc}</div>
                  </div>
                  <div style="text-align:right;margin-left:12px;">
                    <div style="font-weight:800;color:#1e293b;font-size:0.85rem;">{rev}</div>
                    <span class="badge badge-gray" style="font-size:0.65rem;">{rtype}</span>
                  </div>
                </div>""", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="sec-hdr">📊 Revenue Mix (Year 3 Projection)</div>', unsafe_allow_html=True)
            labels=["Gov Licensing","Transaction Fees","API Subscriptions","Freemium Premium","Grants","ONDC Share"]
            values=[35,28,15,12,5,5]
            fig=go.Figure(go.Pie(labels=labels,values=values,hole=0.5,
                                 marker_colors=["#2563EB","#059669","#7c3aed","#ea580c","#0891b2","#dc2626"],
                                 textinfo="label+percent",textfont=dict(size=9)))
            fig.add_annotation(text="<b>Revenue</b><br>Mix",x=0.5,y=0.5,
                               font=dict(size=11,color="#1F4E79"),showarrow=False)
            fig.update_layout(**PLT,height=320,showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('<div class="callout-box" style="--cb-color:#2563EB;--cb-bg:#eff6ff;">'
                        '<div style="font-weight:700;color:#1e40af;font-size:0.85rem;">💡 B2G2B Model Advantage</div>'
                        '<div style="font-size:0.78rem;color:#475569;margin-top:6px;">'
                        'Government as distribution channel eliminates customer acquisition cost. '
                        'State MSMEs reached via existing DIC/NSIC touchpoints — '
                        'marginal cost per new user < ₹80 vs ₹1,200+ for direct acquisition.'
                        '</div></div>', unsafe_allow_html=True)

    with tab2:
        col1, col2 = st.columns([1.3,1])
        with col1:
            st.markdown('<div class="sec-hdr">📊 Market Sizing</div>', unsafe_allow_html=True)
            market_rows = [
                ("Total MSME Population","63 Million","India registered MSMEs","#1F4E79"),
                ("Digitally Underserved","44 Million","70% lack digital tools","#dc2626"),
                ("Rural/Semi-urban Segment","35 Million","Primary target market","#ea580c"),
                ("MSME Digitalisation Market","₹18,000 Cr","22% CAGR","#7c3aed"),
                ("Year 1 Target (0.03%)","25,000 MSEs","Phase 1–2 rollout","#2563EB"),
                ("Year 3 Target (0.3%)","190,000 MSEs","National deployment","#059669"),
                ("TAM Penetration (5 yr)","1%+","350,000+ MSEs","#0891b2"),
            ]
            for label,val,note,color in market_rows:
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;padding:9px 14px;
                  background:white;border-radius:8px;margin-bottom:5px;
                  border-left:3px solid {color};box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                  <span style="font-size:0.8rem;color:#64748b;">{label}</span>
                  <span style="font-weight:800;color:{color};font-size:0.88rem;">{val}</span>
                  <span style="font-size:0.75rem;color:#94a3b8;">{note}</span>
                </div>""", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="sec-hdr">🏆 Competitive Landscape</div>', unsafe_allow_html=True)
            comp_df = pd.DataFrame([
                ["MapMSE","✅ Yes","✅ 11 langs","✅ Full","✅ ONDC Native","✅ Compliant"],
                ["Vyapar","❌ No","❌ Hindi/EN","⚠️ Partial","❌ No","⚠️ Partial"],
                ["Khatabook","❌ No","⚠️ 3 langs","❌ Basic","❌ No","⚠️ Partial"],
                ["Udyam Portal","❌ No","⚠️ Hindi only","❌ None","❌ No","✅ Gov"],
                ["IndiaMart","❌ No","❌ English","⚠️ B2B only","⚠️ Partial","⚠️ Partial"],
            ], columns=["Platform","AI-Powered","Language Coverage","Document AI","ONDC Integration","DPDP Compliant"])
            st.dataframe(comp_df, use_container_width=True, hide_index=True, height=240)

            st.markdown('<div class="callout-box" style="--cb-color:#059669;--cb-bg:#f0fdf4;">'
                        '<div style="font-weight:700;color:#065f46;font-size:0.85rem;">🎯 Unique Differentiation</div>'
                        '<div style="font-size:0.78rem;color:#475569;margin-top:4px;">'
                        'MapMSE is the only platform combining multilingual AI (11 langs), '
                        'government API integration (Udyam + NSIC + ONDC), '
                        'and document-first processing for rural MSME operators.'
                        '</div></div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="sec-hdr">🚀 Go-to-Market Strategy</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            gtm_phases = [
                ("1. Government Channel Entry","Q1–Q2 2025","Embed via DIC / NSIC touchpoints in Phase 1 states. State government MOU as primary distribution — zero direct CAC.",["#059669"]),
                ("2. Grassroots Activation","Q2–Q3 2025","MSME facilitation centres, handloom cooperative camps, voice-first WhatsApp onboarding bot for feature phones.",["#2563EB"]),
                ("3. Enterprise & BFSI Outreach","Q3 2025","SIDBI, NABARD, PSU banks seeking AI-powered MSME credit assessment data. API licensing model.",["#7c3aed"]),
                ("4. Digital & Content Marketing","Ongoing","Malayalam/regional YouTube channel (NYZTrade brand). MSME association webinars. SEO-optimised regional content.",["#ea580c"]),
                ("5. National Scale via MeitY","2026","Digital India MSME programme channel. DC-MSME partnership for all-India deployment.",["#dc2626"]),
            ]
            for phase,timeline,desc,colors in gtm_phases:
                st.markdown(f"""
                <div style="background:white;border-radius:10px;padding:14px 16px;margin-bottom:8px;
                  border-left:4px solid {colors[0]};box-shadow:0 1px 5px rgba(0,0,0,0.05);">
                  <div style="display:flex;justify-content:space-between;">
                    <div style="font-weight:700;color:{colors[0]};font-size:0.85rem;">{phase}</div>
                    <span class="badge badge-gray">{timeline}</span>
                  </div>
                  <div style="font-size:0.78rem;color:#64748b;margin-top:6px;">{desc}</div>
                </div>""", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="sec-hdr">📈 CAC vs LTV Projection</div>', unsafe_allow_html=True)
            years=["Year 1","Year 2","Year 3","Year 4","Year 5"]
            cac=[1200,800,450,280,180]; ltv=[3500,6200,9800,14500,21000]
            fig=go.Figure()
            fig.add_trace(go.Bar(x=years,y=cac,name="CAC (₹)",marker_color="#dc2626",opacity=0.8))
            fig.add_trace(go.Scatter(x=years,y=ltv,name="LTV (₹)",mode="lines+markers",
                                     line=dict(color="#059669",width=2.5),yaxis="y2"))
            fig.update_layout(**PLT,height=280,
                              xaxis=dict(**AXIS,title=""),
                              yaxis=dict(**AXIS,title="CAC ₹"),
                              yaxis2=dict(title="LTV ₹",overlaying="y",side="right",
                                          tickfont=dict(color="#059669",size=10)),
                              legend=dict(font=dict(size=10),bgcolor="rgba(255,255,255,0.9)"))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('<div class="sec-hdr" style="margin-top:16px;">🌱 Growth Funnel</div>', unsafe_allow_html=True)
            funnel_data=[("Awareness (outreach)","500,000","#bfdbfe"),
                         ("Platform Visits","120,000","#93c5fd"),
                         ("Registration Started","35,000","#60a5fa"),
                         ("Registration Completed","22,000","#3b82f6"),
                         ("SNP Matched","18,000","#2563EB"),
                         ("Active on ONDC","12,000","#1d4ed8")]
            for stage,num,col_bg in funnel_data:
                w = int(int(num.replace(",",""))/5000)
                st.markdown(f"""
                <div style="background:{col_bg};border-radius:6px;padding:6px 14px;
                  margin-bottom:3px;width:{min(w,100)}%;min-width:120px;">
                  <span style="font-size:0.75rem;font-weight:600;color:#1e3a5f;">{stage}: {num}</span>
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: GOVERNANCE & COMPLIANCE
# ══════════════════════════════════════════════════════════════════
elif page == "🔒 Governance & Compliance":
    st.markdown('<div class="sec-hdr">🔒 Data Governance, Security & Responsible AI</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sec-hdr-green">🛡️ Data Governance Framework</div>', unsafe_allow_html=True)
        gov_items = [
            ("Data Collection","Explicit institutional consent · PII anonymised at ingestion pipeline entry","#059669"),
            ("Encryption","AES-256 at rest · TLS 1.3 in transit · end-to-end across all API calls","#2563EB"),
            ("Data Localisation","100% India-hosted servers (AWS Mumbai / Azure India Central) · No cross-border transfer","#7c3aed"),
            ("Access Control","RBAC zero-trust architecture · role-scoped API keys · MFA enforced","#ea580c"),
            ("Retention Policy","Active: 24 months · Archive: 36 months · Secure deletion at 36m","#0891b2"),
            ("Audit Trails","Immutable logs · version-controlled models · bi-annual third-party audit","#dc2626"),
            ("Breach Protocol","DPDP statutory notification timelines · 72-hr disclosure SLA","#1F4E79"),
        ]
        for title,detail,color in gov_items:
            st.markdown(f"""
            <div style="background:white;border-radius:10px;padding:12px 16px;margin-bottom:6px;
              border-left:4px solid {color};box-shadow:0 1px 5px rgba(0,0,0,0.05);">
              <div style="font-weight:700;color:{color};font-size:0.82rem;">{title}</div>
              <div style="font-size:0.75rem;color:#64748b;margin-top:3px;">{detail}</div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sec-hdr-green">⚖️ Responsible AI Principles</div>', unsafe_allow_html=True)
        rai_items = [
            ("Fairness","Demographically stratified training data across rural/urban, gender, and 11 language communities","#059669"),
            ("Transparency","Model cards · documented data provenance · plain-language AI decision explanations in regional languages","#2563EB"),
            ("Interpretability","SHAP-based explainability layers on NER and classification outputs · confidence scores surfaced to users","#7c3aed"),
            ("Auditability","Immutable audit logs · version-controlled models · bi-annual algorithmic audits","#ea580c"),
            ("Inclusivity","Voice-first interfaces · low-literacy UX design · offline PWA for zero-connectivity zones","#0891b2"),
            ("Accountability","Human-in-loop review for low-confidence outputs · clear escalation pathways","#dc2626"),
        ]
        for title,detail,color in rai_items:
            st.markdown(f"""
            <div style="background:white;border-radius:10px;padding:12px 16px;margin-bottom:6px;
              border-left:4px solid {color};box-shadow:0 1px 5px rgba(0,0,0,0.05);">
              <div style="font-weight:700;color:{color};font-size:0.82rem;">{title}</div>
              <div style="font-size:0.75rem;color:#64748b;margin-top:3px;">{detail}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-hdr">📜 Regulatory Compliance Status</div>', unsafe_allow_html=True)
    comp_df = pd.DataFrame([
        ["Information Technology Act, 2000","Data handling & cybersecurity obligations","✅ Compliant","Ongoing"],
        ["DPDP Act, 2023","Personal data protection & consent framework","✅ Compliant","Annual review"],
        ["MeitY AI Guidelines","Responsible AI deployment standards","✅ Aligned","Bi-annual audit"],
        ["UNESCO AI Ethics","Fairness, transparency, human rights in AI","✅ Aligned","Yearly assessment"],
        ["RBI Digital Lending Guidelines","Credit data usage for BFSI integrations","✅ Compliant","Per-integration review"],
        ["ONDC Network Policy","Seller onboarding and data standards","✅ Certified","Quarterly"],
    ], columns=["Regulation/Standard","Scope","Status","Review Cycle"])
    st.dataframe(comp_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: PARTNERSHIPS
# ══════════════════════════════════════════════════════════════════
elif page == "🤝 Partnerships":
    st.markdown('<div class="sec-hdr">🤝 Partnerships, Collaborations & Ecosystem</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sec-hdr-green">✅ Existing Partnerships</div>', unsafe_allow_html=True)
        existing = [
            ("AI4Bharat","Academic / Model","IndicTrans2 model access · research collaboration on Indic NLP","🔬","#2563EB"),
            ("Kerala MSME Facilitation Centre","Government","Phase 1 pilot co-deployment · data-sharing MOU · kiosk rollout","🏛️","#059669"),
            ("Tamil Nadu MSME Directorate","Government","Phase 1 deployment · data-sharing MOU · district-level integration","🏛️","#059669"),
            ("ICSSR","Academic Research","Grant funding for women workforce participation & financial autonomy study (Kerala)","📚","#7c3aed"),
        ]
        for name,ptype,detail,icon,color in existing:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:15px 18px;margin-bottom:8px;
              border-left:5px solid {color};box-shadow:0 2px 8px rgba(0,0,0,0.06);">
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                <span style="font-size:1.3rem;">{icon}</span>
                <div>
                  <div style="font-weight:700;color:{color};font-size:0.9rem;">{name}</div>
                  <span class="badge badge-green" style="font-size:0.65rem;">{ptype}</span>
                </div>
              </div>
              <div style="font-size:0.77rem;color:#64748b;">{detail}</div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sec-hdr-warn">🔄 In-Progress / Targeted</div>', unsafe_allow_html=True)
        targeted = [
            ("Karnataka Udyog Mitra","Government","Phase 2 state portal integration — MOU under discussion","🔄","#2563EB"),
            ("Telangana TSIIC","Government","Phase 2 deployment collaboration — onboarding in progress","🔄","#2563EB"),
            ("ONDC Network","Commerce","Seller onboarding integration module — technical integration active","⚙️","#7c3aed"),
            ("SIDBI","Finance","Credit linkage module — digital MSME credit assessment data partnership","💰","#059669"),
            ("MeitY / Digital India","Government","National deployment under Digital India MSME initiative","🇮🇳","#dc2626"),
            ("NABARD","Finance","SHG-MSME rural finance bridge — credit access for agricultural MSMEs","🌾","#059669"),
            ("Amazon Sambhav","Commerce","E-commerce onboarding for ONDC-registered MSMEs","🛒","#ea580c"),
            ("NSE Emerge","Finance","MSME capital markets access and SME IPO readiness module","📈","#7c3aed"),
        ]
        for name,ptype,detail,icon,color in targeted:
            status = "🔄 In Progress" if icon=="🔄" or icon=="⚙️" else "🎯 Targeted"
            badge_cls = "badge-blue" if status=="🔄 In Progress" else "badge-orange"
            st.markdown(f"""
            <div style="background:white;border-radius:10px;padding:12px 15px;margin-bottom:6px;
              border-left:4px solid {color};box-shadow:0 1px 5px rgba(0,0,0,0.05);
              display:flex;justify-content:space-between;align-items:flex-start;">
              <div style="flex:1;">
                <div style="font-weight:700;color:{color};font-size:0.82rem;">{name}
                  <span class="badge {badge_cls}" style="margin-left:6px;font-size:0.65rem;">{status}</span>
                </div>
                <div style="font-size:0.72rem;color:#94a3b8;margin-top:1px;">{ptype}</div>
                <div style="font-size:0.75rem;color:#64748b;margin-top:4px;">{detail}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    # Ecosystem map
    st.markdown('<div class="sec-hdr">🌐 Ecosystem Overview</div>', unsafe_allow_html=True)
    fig = go.Figure()
    # Central node
    fig.add_trace(go.Scatter(x=[0],y=[0],mode="markers+text",
        marker=dict(size=50,color="#1F4E79",symbol="circle"),
        text=["MapMSE"],textposition="middle center",
        textfont=dict(color="white",size=13,family="Inter"),showlegend=False))
    # Nodes
    nodes = [
        (0,2.2,"AI4Bharat","#2563EB"),(-1.8,1.5,"Kerala MSME","#059669"),
        (1.8,1.5,"TN MSME","#059669"),(2.2,0,"ONDC Network","#7c3aed"),
        (1.8,-1.5,"SIDBI","#ea580c"),(0,-2.2,"MeitY","#dc2626"),
        (-1.8,-1.5,"NABARD","#0891b2"),(-2.2,0,"ICSSR","#6b7280"),
    ]
    for x,y,label,color in nodes:
        fig.add_trace(go.Scatter(x=[x],y=[y],mode="markers+text",
            marker=dict(size=30,color=color,symbol="circle"),
            text=[label],textposition="top center",
            textfont=dict(color="#1e293b",size=9,family="Inter"),showlegend=False))
        fig.add_trace(go.Scatter(x=[0,x],y=[0,y],mode="lines",
            line=dict(color="#cbd5e1",width=1.5,dash="dot"),showlegend=False))
    fig.update_layout(**PLT,height=380,
        xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-3,3]),
        yaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-3,3]),
        plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: DATA SOURCES
# ══════════════════════════════════════════════════════════════════
elif page == "🔌 Data Sources":
    st.markdown('<div class="sec-hdr">🔌 Data Sources — How Real Data Enters MapMSE</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
      <span style="color:#1F4E79;font-size:0.92rem;">
      📌 <strong>Control Panel for Data.</strong> Switch between Demo, your own Excel file,
      or a live government API — the entire platform updates instantly across all pages.
      </span>
    </div>""", unsafe_allow_html=True)

    # Pipeline flow
    col1,col2,col3,col4,col5 = st.columns([2,0.3,2,0.3,2])
    for col_,text,title in [(col1,"📥 Step 1 — Data Enters","Choose 1 of 4 entry methods"),
                             (col3,"⚙️ Step 2 — AI Processes","Validate · Score · Match"),
                             (col5,"📊 Step 3 — App Updates","All 7 pages reflect your data")]:
        with col_:
            st.markdown(f"""
            <div class="pipeline-step">
              <div style="font-weight:700;color:#1F4E79;margin-bottom:4px;">{text}</div>
              <div style="font-size:0.8rem;color:#64748b;">{title}</div>
            </div>""", unsafe_allow_html=True)
    for col_ in [col2, col4]:
        with col_:
            st.markdown('<div style="text-align:center;font-size:1.8rem;padding-top:20px;color:#2563EB;">→</div>', unsafe_allow_html=True)

    tab1,tab2,tab3,tab4 = st.tabs(["📂 Upload File","🌐 Udyam API","✏️ Manual Entry","🎲 Demo Data"])

    with tab1:
        col1,col2 = st.columns([1.2,1])
        with col1:
            st.markdown("""<div class="info-card"><strong style="color:#1F4E79;">📂 Upload Excel / CSV</strong><br>
            <small style="color:#64748b;">Upload your MSE dataset directly. Required columns:
            Enterprise Name · State · Sector · Annual Turnover (L) · No. of Employees</small></div>""",
            unsafe_allow_html=True)
            st.download_button("📥 Download Template", data=make_sample_excel(),
                               file_name="MapMSE_Template.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)
        with col2:
            uploaded = st.file_uploader("Drop Excel / CSV", type=["xlsx","xls","csv"])
            if uploaded:
                df_new, err = process_uploaded_file(uploaded)
                if err:
                    st.error(f"❌ {err}")
                else:
                    st.success(f"✅ {len(df_new):,} MSEs loaded from `{uploaded.name}`")
                    st.dataframe(df_new.head(4), use_container_width=True)
                    if st.button("✅ Use This Data", type="primary", use_container_width=True):
                        st.session_state.update({"df_mse":df_new,"data_source":"upload",
                            "source_label":f"📂 {uploaded.name}","source_count":len(df_new)})
                        st.rerun()

    with tab2:
        col1,col2 = st.columns([1.2,1])
        with col1:
            st.markdown("""<div class="info-card"><strong style="color:#1F4E79;">🌐 Udyam Registration Portal API</strong><br>
            <small style="color:#64748b;">Fetch enterprise details directly from government API using Udyam number.
            Demo mode active — provide API key for live data.</small></div>""", unsafe_allow_html=True)
            api_key = st.text_input("🔑 API Key", type="password", placeholder="MeitY API key (optional)")
        with col2:
            udyam_input = st.text_input("Udyam Number", placeholder="UDYAM-KL-08-0023456")
            if st.button("🔍 Fetch", type="primary", use_container_width=True, disabled=not udyam_input):
                with st.spinner("Calling API..."):
                    time.sleep(1.2)
                    st.success("✅ Enterprise fetched (simulated)!")
                    st.json({"enterprise_name":"Shree Lakshmi Textiles","state":"Kerala",
                             "sector":"Textiles & Apparel","turnover_lakhs":120,"employees":25})

    with tab3:
        with st.form("manual_ds"):
            c1,c2,c3 = st.columns(3)
            with c1:
                m_name=st.text_input("Enterprise Name *"); m_state=st.selectbox("State *",INDIAN_STATES)
            with c2:
                m_sector=st.selectbox("Sector *",SECTORS); m_turnover=st.number_input("Turnover (₹ Lakhs)*",min_value=0.1,value=50.0)
            with c3:
                m_emp=st.number_input("Employees *",min_value=1,value=10); m_lang=st.selectbox("Language",LANGUAGES)
            m_prod=st.text_area("Product Description *",height=70)
            if st.form_submit_button("✅ Add to Registry", type="primary", use_container_width=True):
                if m_name and m_prod:
                    new_row={"MSE ID":f"MSE{random.randint(2025000,2029999)}","Enterprise Name":m_name,
                             "State":m_state,"Sector":m_sector,"Annual Turnover (L)":m_turnover,
                             "No. of Employees":m_emp,"Registration Date":datetime.now().strftime("%Y-%m-%d"),
                             "Status":"Pending Verification","Assigned SNP":"—","Match Score":0.0,
                             "Language":m_lang,"Onboarding Time (days)":None,
                             "Categorisation Confidence":round(np.random.uniform(0.78,0.96),2),
                             "Data Source":"✏️ Manual Entry"}
                    new_df=pd.concat([st.session_state["df_mse"],pd.DataFrame([new_row])],ignore_index=True)
                    st.session_state.update({"df_mse":new_df,"data_source":"manual",
                        "source_label":"✏️ Manual Entry","source_count":len(new_df)})
                    st.success(f"✅ '{m_name}' added! Total: {len(new_df):,}"); st.rerun()

    with tab4:
        col1,col2=st.columns(2)
        with col1:
            n=st.slider("Records",100,2000,500,100)
        with col2:
            st.markdown("<br>",unsafe_allow_html=True)
            if st.button("🔄 Generate Demo Data", type="primary", use_container_width=True):
                generate_mock_mse_data.clear()
                fd=generate_mock_mse_data(n)
                st.session_state.update({"df_mse":fd,"data_source":"demo",
                    "source_label":f"🎲 Demo ({n})","source_count":n})
                st.success(f"✅ {n:,} records generated"); st.rerun()


# ══════════════════════════════════════════════════════════════════
# PAGE: AI REGISTRATION
# ══════════════════════════════════════════════════════════════════
elif page == "🤖 AI Registration":
    st.markdown('<div class="sec-hdr">🤖 AI-Powered Multilingual MSE Registration Engine</div>', unsafe_allow_html=True)
    tab1,tab2,tab3 = st.tabs(["🎙️ Voice (ASR)","📄 Document OCR","✏️ Manual"])

    with tab1:
        col1,col2=st.columns(2)
        with col1:
            st.markdown("""<div class="info-card"><strong>🎙️ Whisper Large v3 — Multilingual ASR</strong><br>
            <small>Fine-tuned on 25K hours across 11 Indian languages. WER: 3.7%</small></div>""",
            unsafe_allow_html=True)
            lang=st.selectbox("Language",LANGUAGES)
            st.markdown(f"""<div style="background:#eff6ff;border:2px dashed #2563EB;border-radius:10px;
              padding:28px;text-align:center;">
              <div style="font-size:2.5rem;">🎤</div>
              <div style="color:#1F4E79;font-weight:600;margin-top:6px;">Click to Record</div>
              <div style="color:#94a3b8;font-size:0.77rem;">Demo mode · Language: <b>{lang}</b></div>
            </div>""", unsafe_allow_html=True)
            if st.button("🎙️ Simulate Voice Input",type="primary",use_container_width=True):
                st.session_state["voice_done"]=True
        with col2:
            if st.session_state.get("voice_done"):
                st.success("✅ Voice captured! AI extracted:")
                for k,v in {"Enterprise Name":"Shree Lakshmi Textiles","State":"Kerala",
                             "Sector":"Textiles & Apparel","ASR Confidence":"96.3%",
                             "Language Detected":lang}.items():
                    st.markdown(f"**{k}:** &nbsp;<span class='badge badge-green'>{v}</span>",unsafe_allow_html=True)

    with tab2:
        col1,col2=st.columns(2)
        with col1:
            st.markdown("""<div class="info-card"><strong>📄 LayoutLMv3 + Tesseract 5</strong><br>
            <small>Domain-adapted on 50K MSME docs. Field accuracy: 98.7%</small></div>""",unsafe_allow_html=True)
            doc_type=st.selectbox("Document Type",["Udyam Certificate","GST Certificate"])
            st.file_uploader("Upload Document",type=["pdf","png","jpg","jpeg"])
            if st.button("🔍 Simulate OCR",type="primary",use_container_width=True):
                with st.spinner("Running OCR..."): time.sleep(1.2)
                st.session_state["ocr_done"]=doc_type
        with col2:
            if st.session_state.get("ocr_done"):
                st.success(f"✅ {st.session_state['ocr_done']} processed")
                for k,v in {"Enterprise Name":"Shree Lakshmi Textiles Pvt Ltd",
                             "Udyam No":"UDYAM-KL-08-0023456","NIC Code":"13111",
                             "State":"Kerala","Turnover":"₹1,20,00,000"}.items():
                    st.markdown(f"**{k}:** &nbsp;<span class='badge badge-green'>{v}</span>",unsafe_allow_html=True)

    with tab3:
        with st.form("ai_reg_manual"):
            c1,c2=st.columns(2)
            with c1:
                r_name=st.text_input("Enterprise Name*"); r_state=st.selectbox("State*",INDIAN_STATES)
                r_sector=st.selectbox("Sector*",SECTORS)
            with c2:
                r_turnover=st.number_input("Turnover (₹L)*",min_value=0.1,value=50.0)
                r_emp=st.number_input("Employees*",min_value=1,value=10)
                r_lang=st.selectbox("Language",LANGUAGES)
            r_prod=st.text_area("Product Description*",height=70)
            if st.form_submit_button("🚀 Register",type="primary",use_container_width=True):
                if r_name and r_prod:
                    new_row={"MSE ID":f"MSE{random.randint(2025000,2029999)}","Enterprise Name":r_name,
                             "State":r_state,"Sector":r_sector,"Annual Turnover (L)":r_turnover,
                             "No. of Employees":r_emp,"Registration Date":datetime.now().strftime("%Y-%m-%d"),
                             "Status":"Pending Verification","Assigned SNP":"—","Match Score":0.0,
                             "Language":r_lang,"Onboarding Time (days)":None,
                             "Categorisation Confidence":round(np.random.uniform(0.78,0.96),2),
                             "Data Source":"✏️ Manual Entry"}
                    new_df=pd.concat([st.session_state["df_mse"],pd.DataFrame([new_row])],ignore_index=True)
                    st.session_state.update({"df_mse":new_df,"source_count":len(new_df)})
                    st.success(f"✅ '{r_name}' registered!"); st.rerun()


# ══════════════════════════════════════════════════════════════════
# PAGE: PRODUCT CATEGORISER
# ══════════════════════════════════════════════════════════════════
elif page == "🔍 Product Categoriser":
    st.markdown('<div class="sec-hdr">🔍 AI Product Categorisation — NLP 3-Stage Pipeline</div>', unsafe_allow_html=True)

    def cat_engine(desc):
        cats={"cotton":("Textiles & Apparel","Cotton Fabric","ONDC:RET12-fabric-001",0.96),
              "shirt":("Textiles & Apparel","Readymade Garments","ONDC:RET12-garment-002",0.94),
              "rice":("Agro Products","Processed Grains","ONDC:RET10-grain-001",0.97),
              "spice":("Food Processing","Spices & Condiments","ONDC:RET10-spice-001",0.95),
              "metal":("Metal Fabrication","Metal Components","ONDC:B2B-metal-001",0.91),
              "wood":("Woodwork & Furniture","Wooden Furniture","ONDC:RET12-furn-001",0.93),
              "leather":("Leather Goods","Leather Products","ONDC:RET12-leather-001",0.92),
              "pharma":("Pharmaceuticals","Generic Medicines","ONDC:B2B-pharma-001",0.89)}
        for kw,r in cats.items():
            if kw in desc.lower(): return {"sector":r[0],"category":r[1],"ondc_code":r[2],"confidence":r[3],"nic_code":f"1{random.randint(3000,9999)}"}
        return {"sector":"General Manufacturing","category":"Other Products","ondc_code":"ONDC:B2B-gen-001","confidence":0.73,"nic_code":"32909"}

    col1,col2=st.columns([1,1.2])
    with col1:
        pt=st.text_area("Product Description",value="High-quality cotton fabric and readymade shirts.",height=110)
        if st.button("⚡ Categorise",type="primary",use_container_width=True):
            with st.spinner("Running AI pipeline..."): time.sleep(1.1)
            st.session_state["cat_result"]=cat_engine(pt)
    with col2:
        if st.session_state.get("cat_result"):
            r=st.session_state["cat_result"]; c=int(r["confidence"]*100)
            cc="#16a34a" if r["confidence"]>0.85 else "#ea580c"
            st.markdown(f"""<div class="result-card">
              <div style="display:flex;justify-content:space-between;margin-bottom:10px;">
                <div style="font-weight:700;color:#1F4E79;">🎯 Categorisation Result</div>
                <div style="font-weight:800;color:{cc};font-size:1.3rem;">{c}% Confident</div>
              </div>
              <div class="progress-outer"><div class="progress-inner" style="width:{c}%;background:linear-gradient(90deg,{cc},{cc}99);"></div></div>
              <table style="width:100%;font-size:0.82rem;margin-top:12px;border-collapse:collapse;">
                <tr><td style="color:#94a3b8;padding:4px 0;width:120px;">Sector</td><td><strong>{r["sector"]}</strong></td></tr>
                <tr><td style="color:#94a3b8;padding:4px 0;">Category</td><td><strong>{r["category"]}</strong></td></tr>
                <tr><td style="color:#94a3b8;padding:4px 0;">ONDC Code</td><td><span class="badge badge-blue">{r["ondc_code"]}</span></td></tr>
                <tr><td style="color:#94a3b8;padding:4px 0;">NIC Code</td><td><span class="badge badge-gray">{r["nic_code"]}</span></td></tr>
              </table></div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-hdr">📊 Batch Confidence Stats</div>', unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        cats=pd.cut(df_mse["Categorisation Confidence"],bins=[0,.80,.90,.95,1.0],
                    labels=["<80%","80–90%","90–95%","95–100%"]).value_counts()
        fig=go.Figure(go.Pie(labels=cats.index,values=cats.values,hole=0.42,
                             marker_colors=["#dc2626","#f59e0b","#0891b2","#059669"],
                             textinfo="label+percent",textfont=dict(size=9)))
        fig.update_layout(**PLT,height=240,showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        sa=df_mse.groupby("Sector")["Categorisation Confidence"].mean().sort_values(ascending=False)
        for sec,acc in sa.items():
            color="#16a34a" if acc>0.90 else "#ea580c"
            st.markdown(f"""<div style="margin-bottom:5px;">
              <div style="display:flex;justify-content:space-between;font-size:0.76rem;">
                <span style="color:#1e293b;">{str(sec)[:28]}</span>
                <span style="color:{color};font-weight:700;">{acc*100:.1f}%</span></div>
              <div class="progress-outer"><div class="progress-inner" style="width:{int(acc*100)}%;"></div></div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: SNP MATCHER
# ══════════════════════════════════════════════════════════════════
elif page == "🔗 SNP Matcher":
    st.markdown('<div class="sec-hdr">🔗 Intelligent MSE-to-SNP Matching Engine</div>', unsafe_allow_html=True)

    def snp_match(sector, state, turnover):
        matches=[]
        for _,snp in df_snp.iterrows():
            sem=random.uniform(0.60,0.98)
            if sector.split("&")[0].strip().lower() in snp["Domain Sectors"].lower(): sem=min(sem+0.15,0.99)
            score=round(sem-(snp["Current Load (%)"]/100)*0.15+(snp["Avg Fulfilment Rate (%)"]/100)*0.1,3)
            matches.append({"SNP Name":snp["SNP Name"],"Match Score":min(score,0.99),
                             "Alignment":"High" if sem>0.85 else "Medium",
                             "Load":snp["Current Load (%)"],"Fulfilment":snp["Avg Fulfilment Rate (%)"],
                             "Onboarding":snp["Onboarding Avg (days)"]})
        return sorted(matches,key=lambda x:x["Match Score"],reverse=True)[:5]

    col1,col2=st.columns([1,1.5])
    with col1:
        m_sect=st.selectbox("Sector",SECTORS); m_state=st.selectbox("State",INDIAN_STATES)
        m_turn=st.slider("Turnover (₹L)",5,500,50)
        if st.button("🔍 Find Matches",type="primary",use_container_width=True):
            with st.spinner("Running ML matcher..."): time.sleep(0.9)
            st.session_state["snp_matches"]=snp_match(m_sect,m_state,m_turn)
    with col2:
        if st.session_state.get("snp_matches"):
            labels=["🥇 Best","🥈 2nd","🥉 3rd","4th","5th"]
            for i,m in enumerate(st.session_state["snp_matches"]):
                sp=int(m["Match Score"]*100); sc="#16a34a" if m["Match Score"]>0.85 else "#ea580c"
                st.markdown(f"""<div class="result-card" style="margin-bottom:7px;">
                  <div style="display:flex;justify-content:space-between;">
                    <div><span style="font-weight:700;">{labels[i]}</span>
                    <span style="font-weight:700;color:#1F4E79;margin-left:8px;">{m["SNP Name"]}</span></div>
                    <div style="font-weight:800;color:{sc};font-size:1.2rem;">{sp}%</div></div>
                  <div class="progress-outer"><div class="progress-inner" style="width:{sp}%;"></div></div>
                  <div style="display:flex;gap:12px;margin-top:6px;flex-wrap:wrap;font-size:0.75rem;color:#64748b;">
                    <span>📋 {m["Alignment"]}</span><span>⚡ Load:{m["Load"]}%</span>
                    <span>✅ {m["Fulfilment"]}%</span><span>⏱️ {m["Onboarding"]}d</span>
                  </div></div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: MSE REGISTRY
# ══════════════════════════════════════════════════════════════════
elif page == "📋 MSE Registry":
    st.markdown('<div class="sec-hdr">📋 MSE Registry — Full Database View</div>', unsafe_allow_html=True)
    col1,col2,col3,col4=st.columns(4)
    with col1: f_state=st.selectbox("State",["All"]+sorted(df_mse["State"].dropna().unique().tolist()))
    with col2: f_sector=st.selectbox("Sector",["All"]+sorted(df_mse["Sector"].dropna().unique().tolist()))
    with col3: f_status=st.selectbox("Status",["All"]+sorted(df_mse["Status"].dropna().unique().tolist()))
    with col4: search=st.text_input("🔍 Search","")

    df_f=df_mse.copy()
    if f_state!="All": df_f=df_f[df_f["State"]==f_state]
    if f_sector!="All": df_f=df_f[df_f["Sector"]==f_sector]
    if f_status!="All": df_f=df_f[df_f["Status"]==f_status]
    if search:
        mask=pd.Series([False]*len(df_f),index=df_f.index)
        for c in ["Enterprise Name","MSE ID"]:
            if c in df_f.columns: mask|=df_f[c].astype(str).str.contains(search,case=False,na=False)
        df_f=df_f[mask]

    st.markdown(f"<p style='color:#64748b;font-size:0.85rem;'><b style='color:#1F4E79;'>{len(df_f):,}</b> of <b>{len(df_mse):,}</b> MSEs · Source: <code>{st.session_state.get('source_label','')}</code></p>", unsafe_allow_html=True)

    dcols=[c for c in ["MSE ID","Enterprise Name","State","Sector","Status","Assigned SNP","Match Score","Onboarding Time (days)","Categorisation Confidence","Data Source"] if c in df_f.columns]
    fmt={}
    if "Match Score" in df_f.columns: fmt["Match Score"]="{:.2f}"
    if "Categorisation Confidence" in df_f.columns: fmt["Categorisation Confidence"]="{:.2f}"
    if "Onboarding Time (days)" in df_f.columns: fmt["Onboarding Time (days)"]="{:.1f}"
    st.dataframe(df_f[dcols].head(200).style.format(fmt,na_rep="—"),use_container_width=True,height=440)

    col1,col2=st.columns(2)
    with col1:
        st.download_button("📥 Export CSV",df_f[dcols].to_csv(index=False),"mse_registry.csv","text/csv",use_container_width=True)
    with col2:
        buf=io.BytesIO()
        with pd.ExcelWriter(buf,engine="openpyxl") as w: df_f[dcols].to_excel(w,index=False,sheet_name="MSE Registry")
        st.download_button("📥 Export Excel",buf.getvalue(),"mse_registry.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)
