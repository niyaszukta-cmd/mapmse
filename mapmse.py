"""
MapMSE: AI-Powered MSE-to-SNP Intelligent Agent Mapping Platform
IndiaAI Innovation Challenge 2026 — Problem Statement 2 (Ministry of MSME)
Developed by: NYZTrade AI Solutions
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─────────────────────────── PAGE CONFIG ───────────────────────────
st.set_page_config(
    page_title="MapMSE | AI MSE-SNP Platform",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────── CUSTOM CSS ────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Main background */
  .stApp { background: #f0f4f8; }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1F4E79 0%, #2E75B6 100%) !important;
  }
  section[data-testid="stSidebar"] * { color: #ffffff !important; }
  section[data-testid="stSidebar"] .stSelectbox label,
  section[data-testid="stSidebar"] .stRadio label { color: #cce4ff !important; font-weight: 500; }

  /* Metric cards */
  .metric-card {
    background: white;
    border-radius: 12px;
    padding: 20px 24px;
    border-left: 4px solid #2E75B6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 4px;
  }
  .metric-val { font-size: 2rem; font-weight: 700; color: #1F4E79; }
  .metric-label { font-size: 0.78rem; color: #6c757d; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
  .metric-delta { font-size: 0.82rem; color: #28a745; font-weight: 600; }

  /* Section headers */
  .section-header {
    background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%);
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    margin: 16px 0 12px 0;
    font-weight: 600;
    font-size: 1rem;
  }

  /* Status badges */
  .badge-success { background: #d4edda; color: #155724; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
  .badge-warning { background: #fff3cd; color: #856404; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
  .badge-info    { background: #cce5ff; color: #004085; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
  .badge-danger  { background: #f8d7da; color: #721c24; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }

  /* Cards */
  .info-card {
    background: white;
    border-radius: 10px;
    padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 12px;
  }

  /* Result card */
  .result-card {
    background: linear-gradient(135deg, #e8f4fd 0%, #ffffff 100%);
    border: 1px solid #bee3f8;
    border-radius: 12px;
    padding: 20px;
    margin: 8px 0;
  }
  .match-score-high { color: #1B5E20; font-weight: 700; font-size: 1.4rem; }
  .match-score-med  { color: #E65100; font-weight: 700; font-size: 1.4rem; }

  /* Progress bars */
  .progress-bar-outer { background: #e9ecef; border-radius: 8px; height: 10px; margin: 4px 0; overflow: hidden; }
  .progress-bar-inner { height: 100%; border-radius: 8px; background: linear-gradient(90deg, #2E75B6, #1F4E79); }

  /* Hide default streamlit elements */
  #MainMenu, footer, header { visibility: hidden; }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] { gap: 6px; }
  .stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0 !important;
    background: #e2ebf5 !important;
    color: #1F4E79 !important;
    font-weight: 500 !important;
  }
  .stTabs [aria-selected="true"] {
    background: #1F4E79 !important;
    color: white !important;
  }

  /* Dataframe */
  .dataframe { font-size: 0.85rem; }

  /* Alert box */
  .ai-alert {
    background: linear-gradient(135deg, #fff8e1, #fffde7);
    border-left: 4px solid #ffc107;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────── MOCK DATA ────────────────────────────
INDIAN_STATES = ["Kerala", "Tamil Nadu", "Karnataka", "Maharashtra", "Gujarat",
                 "Rajasthan", "Uttar Pradesh", "West Bengal", "Telangana", "Punjab"]

SECTORS = ["Textiles & Apparel", "Food Processing", "Metal Fabrication",
           "Handicrafts & Artisans", "Electronics & Components",
           "Agro Products", "Chemicals & Plastics", "Leather Goods",
           "Woodwork & Furniture", "Pharmaceuticals"]

LANGUAGES = ["Hindi", "Malayalam", "Tamil", "Telugu", "Kannada",
             "Marathi", "Gujarati", "Bengali", "Odia", "Punjabi"]

SNP_NAMES = [
    "Flipkart ONDC", "Amazon Seller Svcs", "Meesho SNP", "Udaan Trade",
    "TradeIndia ONDC", "IndiaMart Direct", "Paytm Mall B2B", "Bizongo SNP",
    "Moglix Industrial", "Jumbotail Agro"
]

@st.cache_data
def generate_mock_mse_data(n=500):
    random.seed(42)
    np.random.seed(42)
    data = []
    for i in range(n):
        state = random.choice(INDIAN_STATES)
        sector = random.choice(SECTORS)
        status = random.choices(
            ["Onboarded", "Pending Verification", "Matched - Awaiting SNP", "Rejected", "Under Review"],
            weights=[45, 20, 15, 8, 12]
        )[0]
        data.append({
            "MSE ID": f"MSE{2024000+i}",
            "Enterprise Name": f"{random.choice(['Sri','Shree','Om','Jai','New','Modern','Royal','National'])} "
                               f"{random.choice(['Traders','Enterprises','Industries','Works','Manufacturing','Products'])} "
                               f"{random.choice(['Pvt Ltd','LLP','','& Sons','& Co'])}".strip(),
            "State": state,
            "Sector": sector,
            "Annual Turnover (L)": round(random.lognormvariate(3.5, 0.8), 1),
            "No. of Employees": random.randint(2, 250),
            "Registration Date": (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d"),
            "Status": status,
            "Assigned SNP": random.choice(SNP_NAMES) if status == "Onboarded" else "—",
            "Match Score": round(random.uniform(0.72, 0.98), 2) if status == "Onboarded" else round(random.uniform(0.5, 0.85), 2),
            "Language": random.choice(LANGUAGES),
            "Onboarding Time (days)": round(random.lognormvariate(1.2, 0.4), 1) if status == "Onboarded" else None,
            "Categorisation Confidence": round(random.uniform(0.78, 0.99), 2),
        })
    return pd.DataFrame(data)

@st.cache_data
def generate_snp_data():
    snps = []
    for i, name in enumerate(SNP_NAMES):
        sector_speciality = random.sample(SECTORS, random.randint(2, 5))
        snps.append({
            "SNP ID": f"SNP{1000+i}",
            "SNP Name": name,
            "Domain Sectors": ", ".join(sector_speciality[:2]),
            "Capacity (MSEs/mo)": random.randint(200, 1500),
            "Current Load (%)": random.randint(35, 88),
            "Avg Fulfilment Rate (%)": round(random.uniform(82, 97), 1),
            "States Active": random.randint(5, 28),
            "Rating": round(random.uniform(3.8, 4.9), 1),
            "Onboarding Avg (days)": round(random.uniform(1.5, 5.5), 1)
        })
    return pd.DataFrame(snps)

df_mse = generate_mock_mse_data(500)
df_snp = generate_snp_data()


# ─────────────────────────── AI SIMULATION ────────────────────────
def simulate_ocr_extraction(doc_type):
    fields = {
        "Udyam Certificate": {
            "Enterprise Name": "Shree Lakshmi Textiles Pvt Ltd",
            "Udyam Number": "UDYAM-KL-08-0023456",
            "NIC Code": "13111",
            "State": "Kerala",
            "District": "Ernakulam",
            "Date of Incorporation": "2018-04-12",
            "Investment (Plant & Machinery)": "INR 45,00,000",
            "Turnover": "INR 1,20,00,000",
            "Activity": "Manufacturing"
        },
        "GST Certificate": {
            "GSTIN": "32AABCS1429B1ZB",
            "Legal Name": "SHREE LAKSHMI TEXTILES PVT LTD",
            "Trade Name": "Lakshmi Textiles",
            "Registration Date": "2018-07-01",
            "State": "Kerala",
            "Principal Place": "Ernakulam, Kerala"
        }
    }
    return fields.get(doc_type, {})

def simulate_product_categorisation(description):
    """Simulate AI product categorisation pipeline."""
    import time
    # Simulate processing
    categories = {
        "cotton": ("Textiles & Apparel", "Cotton Fabric", "ONDC:RET12-fabric-001", 0.96),
        "shirt": ("Textiles & Apparel", "Ready-made Garments", "ONDC:RET12-garment-002", 0.94),
        "rice": ("Agro Products", "Processed Grains", "ONDC:RET10-grain-001", 0.97),
        "spice": ("Food Processing", "Spices & Condiments", "ONDC:RET10-spice-001", 0.95),
        "metal": ("Metal Fabrication", "Metal Components", "ONDC:B2B-metal-001", 0.91),
        "wood": ("Woodwork & Furniture", "Wooden Furniture", "ONDC:RET12-furniture-001", 0.93),
        "leather": ("Leather Goods", "Leather Products", "ONDC:RET12-leather-001", 0.92),
    }
    desc_lower = description.lower()
    for keyword, result in categories.items():
        if keyword in desc_lower:
            return {
                "sector": result[0],
                "category": result[1],
                "ondc_code": result[2],
                "confidence": result[3],
                "attributes": ["material", "finish", "dimensions", "grade"],
                "nic_code": f"1{random.randint(3000,9999)}"
            }
    return {
        "sector": "General Manufacturing",
        "category": "Other Products",
        "ondc_code": "ONDC:B2B-gen-001",
        "confidence": 0.73,
        "attributes": ["type", "dimensions"],
        "nic_code": "32909"
    }

def simulate_snp_matching(sector, state, turnover):
    """Simulate intelligent MSE-SNP matching with scores."""
    matches = []
    for _, snp in df_snp.iterrows():
        semantic_score = random.uniform(0.60, 0.98)
        if sector.split("&")[0].strip().lower() in snp["Domain Sectors"].lower():
            semantic_score = min(semantic_score + 0.15, 0.99)
        load_penalty = (snp["Current Load (%)"] / 100) * 0.15
        fulfilment_bonus = (snp["Avg Fulfilment Rate (%)"] / 100) * 0.1
        final_score = round(semantic_score - load_penalty + fulfilment_bonus, 3)
        matches.append({
            "SNP Name": snp["SNP Name"],
            "Match Score": min(final_score, 0.99),
            "Domain Alignment": "High" if semantic_score > 0.85 else "Medium",
            "Current Load (%)": snp["Current Load (%)"],
            "Fulfilment Rate (%)": snp["Avg Fulfilment Rate (%)"],
            "Est. Onboarding (days)": snp["Onboarding Avg (days)"],
            "States Active": snp["States Active"]
        })
    matches.sort(key=lambda x: x["Match Score"], reverse=True)
    return matches[:5]


# ─────────────────────────── SIDEBAR ──────────────────────────────
with st.sidebar:
    st.markdown("## 🏭 MapMSE")
    st.markdown("**AI-Powered MSE-SNP Platform**")
    st.markdown("*IndiaAI Innovation Challenge 2026*")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "🤖 AI Registration", "🔍 Product Categoriser", "🔗 SNP Matcher", "📋 MSE Registry", "📈 Analytics"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**System Status**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("🟢 ASR Online")
        st.markdown("🟢 OCR Online")
    with col2:
        st.markdown("🟢 NLP Active")
        st.markdown("🟢 Matcher OK")

    st.markdown("---")
    st.caption("v2.1.0 | NYZTrade AI Solutions")
    st.caption("Submission: Feb 21, 2026")


# ─────────────────────────── HEADER ───────────────────────────────
st.markdown("""
<div style="background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 60%, #1F4E79 100%);
            padding: 24px 32px; border-radius: 12px; margin-bottom: 20px;
            display: flex; align-items: center; justify-content: space-between;">
  <div>
    <div style="color:#ffffff; font-size: 1.8rem; font-weight: 700; letter-spacing: -0.5px;">
      🏭 MapMSE
    </div>
    <div style="color:#cce4ff; font-size: 0.95rem; margin-top: 4px;">
      AI-Powered Intelligent MSE-to-SNP Agent Mapping Platform &nbsp;|&nbsp; Ministry of MSME &nbsp;|&nbsp; IndiaAI 2026
    </div>
  </div>
  <div style="text-align: right; color: #a8d4f5; font-size: 0.8rem;">
    🕐 Last updated: """ + datetime.now().strftime("%H:%M, %d %b %Y") + """
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════ PAGE: DASHBOARD ══════════════════════════
if page == "📊 Dashboard":
    # KPI row
    col1, col2, col3, col4, col5 = st.columns(5)
    kpis = [
        ("Total MSEs Registered", "2,147", "↑ +342 this month", "#2E75B6"),
        ("Successfully Onboarded", "1,089", "↑ 50.7% rate", "#1B5E20"),
        ("Avg Onboarding Time", "3.8 days", "↓ -68% vs manual", "#E65100"),
        ("Categorisation Accuracy", "94.2%", "↑ +26.9% vs baseline", "#6A1B9A"),
        ("Active SNP Partners", "34", "↑ +8 this quarter", "#1F4E79"),
    ]
    for col, (label, val, delta, color) in zip([col1,col2,col3,col4,col5], kpis):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: {color};">
              <div class="metric-val" style="color:{color};">{val}</div>
              <div class="metric-label">{label}</div>
              <div class="metric-delta">{delta}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts row 1
    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown('<div class="section-header">📍 MSE Onboarding by State</div>', unsafe_allow_html=True)
        state_counts = df_mse.groupby("State").size().reset_index(name="count").sort_values("count", ascending=True)
        fig = px.bar(state_counts, x="count", y="State", orientation='h',
                     color="count", color_continuous_scale=["#cce4ff","#1F4E79"],
                     labels={"count": "MSEs", "State": ""})
        fig.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0), showlegend=False,
                          coloraxis_showscale=False, paper_bgcolor='white', plot_bgcolor='white',
                          font=dict(family="Inter", size=11))
        fig.update_traces(text=state_counts["count"], textposition="inside", textfont=dict(color="white", size=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">📊 Registration Status</div>', unsafe_allow_html=True)
        status_counts = df_mse["Status"].value_counts()
        colors = ["#1F4E79","#2E75B6","#ffc107","#dc3545","#6c757d"]
        fig = go.Figure(go.Pie(
            labels=status_counts.index, values=status_counts.values,
            hole=0.5, marker_colors=colors,
            textinfo="label+percent", textfont=dict(size=10),
            hovertemplate="%{label}: %{value} MSEs<extra></extra>"
        ))
        fig.add_annotation(text="<b>2,147</b><br>Total", x=0.5, y=0.5,
                           font=dict(size=13, color="#1F4E79"), showarrow=False)
        fig.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                          showlegend=True, legend=dict(font=dict(size=9)),
                          paper_bgcolor='white', font=dict(family="Inter"))
        st.plotly_chart(fig, use_container_width=True)

    # Charts row 2
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">🏭 MSEs by Sector</div>', unsafe_allow_html=True)
        sector_data = df_mse.groupby("Sector").size().reset_index(name="count").sort_values("count", ascending=False)
        fig = px.bar(sector_data, x="Sector", y="count",
                     color="count", color_continuous_scale=["#bee3f8","#1F4E79"],
                     labels={"count": "# MSEs", "Sector": ""})
        fig.update_layout(height=300, margin=dict(l=0,r=10,t=10,b=80),
                          coloraxis_showscale=False, paper_bgcolor='white', plot_bgcolor='#f8f9fa',
                          font=dict(family="Inter", size=10),
                          xaxis=dict(tickangle=-35, tickfont=dict(size=9)))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">⚡ Onboarding Time Distribution</div>', unsafe_allow_html=True)
        onboarded = df_mse[df_mse["Onboarding Time (days)"].notna()]["Onboarding Time (days)"]
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=onboarded, nbinsx=20, name="MapMSE",
                                   marker_color="#2E75B6", opacity=0.8))
        # Manual baseline overlay
        manual_times = np.random.lognormal(2.5, 0.3, 500)
        fig.add_trace(go.Histogram(x=manual_times, nbinsx=20, name="Manual (Baseline)",
                                   marker_color="#dc3545", opacity=0.5))
        fig.add_vline(x=onboarded.mean(), line_dash="dash", line_color="#1F4E79",
                      annotation_text=f"MapMSE avg: {onboarded.mean():.1f}d", annotation_font_size=10)
        fig.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                          barmode="overlay", legend=dict(font=dict(size=10)),
                          paper_bgcolor='white', plot_bgcolor='#f8f9fa',
                          font=dict(family="Inter", size=11),
                          xaxis_title="Days", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

    # Categorisation confidence heatmap
    st.markdown('<div class="section-header">🎯 Categorisation Confidence by Sector × State (Sample)</div>', unsafe_allow_html=True)
    pivot_data = df_mse.groupby(["Sector","State"])["Categorisation Confidence"].mean().unstack(fill_value=0)
    pivot_data = pivot_data.iloc[:8, :7]  # Truncate for display
    fig = px.imshow(pivot_data, color_continuous_scale="Blues",
                    labels=dict(color="Avg Confidence"),
                    aspect="auto", text_auto=".2f")
    fig.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                      font=dict(family="Inter", size=10), paper_bgcolor='white')
    fig.update_traces(textfont=dict(size=9))
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════ PAGE: AI REGISTRATION ════════════════════
elif page == "🤖 AI Registration":
    st.markdown('<div class="section-header">🤖 AI-Powered Multilingual MSE Registration Engine</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🎙️ Voice Registration", "📄 Document Upload (OCR)", "✏️ Manual Entry"])

    with tab1:
        st.markdown("""
        <div class="info-card">
          <strong>🎙️ Voice-Enabled Registration</strong><br>
          <small>Speak in your preferred language. Our AI (Whisper-large-v3 + IndicASR) will extract all form fields automatically across 11 Indian languages.</small>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            lang = st.selectbox("Select Language / भाषा चुनें", LANGUAGES)
            st.markdown(f"""
            <div style="background:#f0f7ff; border:2px dashed #2E75B6; border-radius:10px;
                        padding:30px; text-align:center; margin:10px 0;">
              <div style="font-size:3rem;">🎤</div>
              <div style="color:#1F4E79; font-weight:600; margin-top:8px;">Click to Record</div>
              <div style="color:#6c757d; font-size:0.8rem;">(Demo Mode — simulated)</div>
              <div style="margin-top:8px; font-size:0.85rem; color:#2E75B6;">Language: <b>{lang}</b></div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🎙️ Simulate Voice Input", use_container_width=True, type="primary"):
                st.session_state["voice_done"] = True

        with col2:
            if st.session_state.get("voice_done"):
                st.success("✅ Voice captured! AI extracted the following fields:")
                extracted = {
                    "Enterprise Name": "Shree Lakshmi Textiles",
                    "Owner Name": "Rajesh Kumar",
                    "State": lang_state_map if (lang_state_map:="Kerala") else "Kerala",
                    "Sector": "Textiles & Apparel",
                    "Product Description": "Cotton fabric and readymade garments",
                    "Udyam Number": "UDYAM-KL-08-0023456",
                    "Annual Turnover": "INR 1.2 Crore",
                    "ASR Confidence": "96.3%",
                    "Language Detected": lang
                }
                for k, v in extracted.items():
                    badge = "badge-success" if k not in ["ASR Confidence"] else "badge-info"
                    st.markdown(f"**{k}:** &nbsp; <span class='{badge}'>{v}</span>", unsafe_allow_html=True)
            else:
                st.info("👆 Click 'Simulate Voice Input' to see AI extraction in action")
                st.markdown("""
                <div class="ai-alert">
                  <strong>💡 How it works:</strong><br>
                  <small>1. Speech captured via browser microphone<br>
                  2. Whisper-large-v3 transcribes to text (96.3% WER)<br>
                  3. IndicBERT NER extracts structured fields<br>
                  4. Form auto-populated with confidence scores<br>
                  5. Human review triggered if confidence < 80%</small>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="info-card">
          <strong>📄 Intelligent Document Processing (OCR + NLP)</strong><br>
          <small>Upload Udyam Certificate, GST Certificate, or Bank Statement. AI extracts all relevant fields automatically using LayoutLMv3 + Tesseract 5.0.</small>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            doc_type = st.selectbox("Document Type", ["Udyam Certificate", "GST Certificate"])
            uploaded = st.file_uploader("Upload Document (PDF/Image)", type=["pdf","png","jpg","jpeg"])

            if st.button("🔍 Simulate OCR Extraction", use_container_width=True, type="primary"):
                with st.spinner("Running OCR pipeline..."):
                    import time; time.sleep(1.5)
                    st.session_state["ocr_result"] = simulate_ocr_extraction(doc_type)
                    st.session_state["ocr_doc"] = doc_type

        with col2:
            if st.session_state.get("ocr_result"):
                st.success(f"✅ {st.session_state['ocr_doc']} processed — 98.7% field accuracy")
                for k, v in st.session_state["ocr_result"].items():
                    st.markdown(f"**{k}:** &nbsp; <span class='badge-success'>{v}</span>", unsafe_allow_html=True)
            else:
                st.info("👆 Click to simulate document OCR extraction")

    with tab3:
        with st.form("manual_registration"):
            st.markdown("**Enterprise Information**")
            c1, c2 = st.columns(2)
            with c1:
                ent_name = st.text_input("Enterprise Name*", placeholder="e.g., Shree Lakshmi Textiles")
                udyam_no = st.text_input("Udyam Number*", placeholder="UDYAM-XX-XX-XXXXXXX")
                state = st.selectbox("State*", INDIAN_STATES)
            with c2:
                sector = st.selectbox("Sector*", SECTORS)
                turnover = st.number_input("Annual Turnover (₹ Lakhs)*", min_value=0.1, value=50.0)
                employees = st.number_input("No. of Employees*", min_value=1, value=15)

            st.markdown("**Product Description**")
            product_desc = st.text_area("Describe your main products*",
                                        placeholder="e.g., We manufacture cotton fabric and readymade shirts for export and domestic markets...",
                                        height=100)

            submitted = st.form_submit_button("🚀 Register & Run AI Analysis", type="primary", use_container_width=True)
            if submitted and ent_name and product_desc:
                st.session_state["manual_reg"] = {
                    "name": ent_name, "sector": sector, "state": state,
                    "turnover": turnover, "product_desc": product_desc
                }
                st.success(f"✅ MSE '{ent_name}' registered! Go to 'Product Categoriser' and 'SNP Matcher' tabs for AI analysis.")


# ═══════════════════════ PAGE: PRODUCT CATEGORISER ════════════════
elif page == "🔍 Product Categoriser":
    st.markdown('<div class="section-header">🔍 AI Product Categorisation Engine</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("""
        <div class="info-card">
          <strong>3-Stage Classification Pipeline</strong><br>
          <small>
            Stage 1: Semantic text classification (sentence-transformers)<br>
            Stage 2: Attribute extraction (SpaCy NER)<br>
            Stage 3: ONDC taxonomy compliance validation
          </small>
        </div>
        """, unsafe_allow_html=True)

        product_text = st.text_area(
            "Enter Product Description",
            value="We manufacture high-quality cotton fabric and readymade shirts for both export and domestic markets. Products include plain weave, twill, and poplin cotton.",
            height=120
        )

        examples = st.expander("📋 Try Example Descriptions")
        with examples:
            eg_cols = st.columns(2)
            examples_list = [
                ("Cotton fabric", "Plain weave cotton fabric for garment manufacturers"),
                ("Metal parts", "Precision metal components for automotive industry"),
                ("Rice processing", "Parboiled rice and broken rice for domestic supply"),
                ("Wooden furniture", "Solid teak wood chairs and dining tables"),
            ]
            for i, (label, text) in enumerate(examples_list):
                if eg_cols[i%2].button(label, key=f"eg_{i}"):
                    st.session_state["eg_text"] = text

        if "eg_text" in st.session_state:
            product_text = st.session_state["eg_text"]

        if st.button("⚡ Run AI Categorisation", type="primary", use_container_width=True):
            with st.spinner("Running 3-stage classification pipeline..."):
                import time; time.sleep(1.2)
                result = simulate_product_categorisation(product_text)
                st.session_state["cat_result"] = result
                st.session_state["cat_text"] = product_text

    with col2:
        if st.session_state.get("cat_result"):
            r = st.session_state["cat_result"]
            conf_pct = int(r["confidence"] * 100)
            conf_color = "#1B5E20" if r["confidence"] > 0.85 else "#E65100"

            st.markdown(f"""
            <div class="result-card">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <div style="font-size:1.1rem; font-weight:700; color:#1F4E79;">🎯 Classification Result</div>
                <div class="{'match-score-high' if r['confidence'] > 0.85 else 'match-score-med'}">{conf_pct}% Confident</div>
              </div>
              <div class="progress-bar-outer"><div class="progress-bar-inner" style="width:{conf_pct}%; background:linear-gradient(90deg,{conf_color},{conf_color}aa);"></div></div>
              <br>
              <table style="width:100%; font-size:0.85rem;">
                <tr><td style="color:#6c757d; width:160px;">ONDC Sector</td><td><strong>{r["sector"]}</strong></td></tr>
                <tr><td style="color:#6c757d;">Product Category</td><td><strong>{r["category"]}</strong></td></tr>
                <tr><td style="color:#6c757d;">ONDC Code</td><td><span class="badge-info">{r["ondc_code"]}</span></td></tr>
                <tr><td style="color:#6c757d;">NIC Code</td><td><span class="badge-info">{r["nic_code"]}</span></td></tr>
                <tr><td style="color:#6c757d;">Key Attributes</td><td>{", ".join(r["attributes"])}</td></tr>
              </table>
            </div>
            """, unsafe_allow_html=True)

            # Confidence breakdown chart
            st.markdown("**Stage-wise Confidence Breakdown**")
            stages = ["Text Classification", "Attribute Extraction", "Compliance Validation", "Final Score"]
            scores = [r["confidence"] + random.uniform(-0.03, 0.02),
                      r["confidence"] + random.uniform(-0.02, 0.01),
                      r["confidence"] + random.uniform(-0.01, 0.02),
                      r["confidence"]]
            scores = [min(max(s, 0.70), 1.0) for s in scores]

            fig = go.Figure(go.Bar(x=stages, y=[s*100 for s in scores],
                                   marker_color=["#bee3f8","#90caf9","#42a5f5","#1F4E79"],
                                   text=[f"{s*100:.1f}%" for s in scores],
                                   textposition="outside"))
            fig.add_hline(y=80, line_dash="dash", line_color="#ffc107",
                          annotation_text="Review threshold (80%)")
            fig.update_layout(height=250, margin=dict(l=0,r=0,t=20,b=0),
                              yaxis=dict(range=[0,105], title="Confidence (%)"),
                              paper_bgcolor='white', plot_bgcolor='#f8f9fa',
                              font=dict(family="Inter", size=11))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👈 Enter a product description and click 'Run AI Categorisation'")

    # Bulk categorisation stats
    st.markdown('<div class="section-header">📊 Bulk Categorisation Statistics (Current Batch)</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    conf_bins = ["< 80% (Review)", "80-90%", "90-95%", "95-100%"]
    conf_vals = [df_mse["Categorisation Confidence"].apply(
        lambda x: b
        for b in [x < 0.80, 0.80 <= x < 0.90, 0.90 <= x < 0.95, x >= 0.95]
    ).sum() if False else 0 for b in conf_bins]

    # Simple version
    cats = pd.cut(df_mse["Categorisation Confidence"], bins=[0, 0.80, 0.90, 0.95, 1.0],
                  labels=conf_bins).value_counts()

    with col1:
        fig = go.Figure(go.Pie(labels=cats.index, values=cats.values, hole=0.4,
                               marker_colors=["#dc3545","#ffc107","#17a2b8","#28a745"]))
        fig.update_layout(height=220, margin=dict(l=0,r=0,t=10,b=0),
                          showlegend=True, legend=dict(font=dict(size=9)),
                          paper_bgcolor='white', font=dict(family="Inter"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Accuracy by Sector**")
        sector_acc = df_mse.groupby("Sector")["Categorisation Confidence"].mean().sort_values(ascending=False)
        for sector, acc in sector_acc.items():
            bar_w = int(acc * 100)
            color = "#1B5E20" if acc > 0.90 else "#E65100"
            st.markdown(f"""
            <div style="margin-bottom:6px;">
              <div style="display:flex;justify-content:space-between;font-size:0.78rem;">
                <span>{sector[:25]}</span><span style="color:{color};font-weight:600;">{acc*100:.1f}%</span>
              </div>
              <div class="progress-bar-outer"><div class="progress-bar-inner" style="width:{bar_w}%;"></div></div>
            </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown("**Key Metrics**")
        metrics = [
            ("Overall Accuracy", f"{df_mse['Categorisation Confidence'].mean()*100:.1f}%"),
            ("Auto-approved (>80%)", f"{(df_mse['Categorisation Confidence'] >= 0.80).mean()*100:.0f}%"),
            ("Flagged for Review", f"{(df_mse['Categorisation Confidence'] < 0.80).sum()} MSEs"),
            ("Avg Processing Time", "0.38 sec"),
            ("Daily Throughput", "~1,200 MSEs"),
        ]
        for label, val in metrics:
            st.markdown(f"""
            <div style="background:#f8f9fa; border-radius:6px; padding:8px 12px; margin-bottom:6px; display:flex; justify-content:space-between;">
              <span style="font-size:0.82rem; color:#495057;">{label}</span>
              <span style="font-weight:700; color:#1F4E79; font-size:0.88rem;">{val}</span>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════ PAGE: SNP MATCHER ════════════════════════
elif page == "🔗 SNP Matcher":
    st.markdown('<div class="section-header">🔗 Intelligent MSE-to-SNP Matching Engine</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown("""
        <div class="info-card">
          <strong>Multi-factor Matching Algorithm</strong><br>
          <small>
            • Semantic similarity (bi-encoder transformer)<br>
            • SNP capacity & load balancing<br>
            • Domain alignment scoring<br>
            • Geographic proximity weighting<br>
            • Historical fulfilment rate
          </small>
        </div>
        """, unsafe_allow_html=True)

        m_sector = st.selectbox("MSE Sector", SECTORS)
        m_state = st.selectbox("MSE State", INDIAN_STATES)
        m_turnover = st.slider("Annual Turnover (₹ Lakhs)", 5, 500, 50)
        m_employees = st.slider("No. of Employees", 2, 250, 25)
        m_prod = st.text_area("Product Description (optional)", height=80,
                              placeholder="Cotton fabric, readymade garments...")

        if st.button("🔍 Find Best SNP Matches", type="primary", use_container_width=True):
            with st.spinner("Running intelligent matching algorithm..."):
                import time; time.sleep(1.0)
                matches = simulate_snp_matching(m_sector, m_state, m_turnover)
                st.session_state["snp_matches"] = matches
                st.session_state["match_sector"] = m_sector

    with col2:
        if st.session_state.get("snp_matches"):
            matches = st.session_state["snp_matches"]
            st.markdown(f"**Top 5 SNP Matches** for `{st.session_state['match_sector']}`")

            for i, match in enumerate(matches):
                score_pct = int(match["Match Score"] * 100)
                rank_color = ["#C8B400","#6c757d","#CD7F32","#1F4E79","#1F4E79"][i]
                rank_labels = ["🥇 Best Match","🥈 2nd Choice","🥉 3rd Choice","4th","5th"]
                score_color = "#1B5E20" if match["Match Score"] > 0.85 else "#E65100"

                st.markdown(f"""
                <div class="result-card" style="margin-bottom:8px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                      <span style="color:{rank_color};font-weight:700;">{rank_labels[i]}</span>
                      <span style="font-weight:600; color:#1F4E79; margin-left:8px; font-size:1rem;">{match["SNP Name"]}</span>
                    </div>
                    <div style="color:{score_color}; font-weight:700; font-size:1.3rem;">{score_pct}%</div>
                  </div>
                  <div class="progress-bar-outer"><div class="progress-bar-inner" style="width:{score_pct}%;"></div></div>
                  <div style="display:flex; gap:16px; margin-top:8px; flex-wrap:wrap; font-size:0.78rem; color:#495057;">
                    <span>📋 Domain: <b>{match["Domain Alignment"]}</b></span>
                    <span>⚡ Load: <b>{match["Current Load (%)"]}%</b></span>
                    <span>✅ Fulfilment: <b>{match["Fulfilment Rate (%)"]}%</b></span>
                    <span>⏱️ ETA: <b>{match["Est. Onboarding (days)"]}d</b></span>
                    <span>🗺️ States: <b>{match["States Active"]}</b></span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            # Radar chart for top 3
            st.markdown("**Multi-dimensional Comparison (Top 3)**")
            categories = ["Match Score", "Fulfilment Rate", "Domain Alignment", "Capacity", "Response Speed"]
            fig = go.Figure()
            for i, match in enumerate(matches[:3]):
                vals = [
                    match["Match Score"] * 100,
                    match["Fulfilment Rate (%)"],
                    85 if match["Domain Alignment"] == "High" else 65,
                    100 - match["Current Load (%)"],
                    100 - (match["Est. Onboarding (days)"] / 6 * 100)
                ]
                fig.add_trace(go.Scatterpolar(r=vals, theta=categories, fill='toself',
                                              name=match["SNP Name"][:15], opacity=0.7))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])),
                              showlegend=True, height=300,
                              margin=dict(l=40,r=40,t=20,b=0),
                              paper_bgcolor='white', font=dict(family="Inter", size=10),
                              legend=dict(font=dict(size=9)))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👈 Set MSE parameters and click 'Find Best SNP Matches'")


# ═══════════════════════ PAGE: MSE REGISTRY ═══════════════════════
elif page == "📋 MSE Registry":
    st.markdown('<div class="section-header">📋 MSE Registry — All Registrations</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        f_state = st.selectbox("Filter by State", ["All"] + INDIAN_STATES)
    with col2:
        f_sector = st.selectbox("Filter by Sector", ["All"] + SECTORS)
    with col3:
        f_status = st.selectbox("Filter by Status", ["All", "Onboarded", "Pending Verification",
                                                      "Matched - Awaiting SNP", "Rejected", "Under Review"])
    with col4:
        search = st.text_input("🔍 Search Enterprise", placeholder="Name or MSE ID...")

    df_filtered = df_mse.copy()
    if f_state != "All": df_filtered = df_filtered[df_filtered["State"] == f_state]
    if f_sector != "All": df_filtered = df_filtered[df_filtered["Sector"] == f_sector]
    if f_status != "All": df_filtered = df_filtered[df_filtered["Status"] == f_status]
    if search: df_filtered = df_filtered[
        df_filtered["Enterprise Name"].str.contains(search, case=False) |
        df_filtered["MSE ID"].str.contains(search, case=False)
    ]

    st.markdown(f"**Showing {len(df_filtered):,} of {len(df_mse):,} MSEs**")

    display_cols = ["MSE ID", "Enterprise Name", "State", "Sector", "Status",
                    "Assigned SNP", "Match Score", "Onboarding Time (days)", "Categorisation Confidence"]
    st.dataframe(
        df_filtered[display_cols].head(100).style
        .background_gradient(subset=["Match Score", "Categorisation Confidence"], cmap="Blues")
        .format({"Match Score": "{:.2f}", "Categorisation Confidence": "{:.2f}",
                 "Onboarding Time (days)": "{:.1f}"}),
        use_container_width=True, height=420
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export to CSV", use_container_width=True):
            csv = df_filtered[display_cols].to_csv(index=False)
            st.download_button("Download CSV", csv, "mse_registry.csv", "text/csv", use_container_width=True)


# ═══════════════════════ PAGE: ANALYTICS ══════════════════════════
elif page == "📈 Analytics":
    st.markdown('<div class="section-header">📈 Platform Analytics & AI Performance Monitoring</div>', unsafe_allow_html=True)

    # Time series simulation
    dates = pd.date_range(start="2024-08-01", end="2025-02-21", freq="W")
    registrations = np.cumsum(np.random.poisson(45, len(dates)))
    onboardings = np.cumsum(np.random.poisson(22, len(dates)))

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=registrations, name="Registrations",
                                 line=dict(color="#2E75B6", width=2.5), fill='tozeroy',
                                 fillcolor="rgba(46,117,182,0.1)"))
        fig.add_trace(go.Scatter(x=dates, y=onboardings, name="Onboardings",
                                 line=dict(color="#1B5E20", width=2.5), fill='tozeroy',
                                 fillcolor="rgba(27,94,32,0.08)"))
        fig.update_layout(title="Cumulative MSE Registrations vs Onboardings",
                          height=300, margin=dict(l=0,r=0,t=40,b=0),
                          paper_bgcolor='white', plot_bgcolor='#f8f9fa',
                          font=dict(family="Inter", size=11),
                          legend=dict(orientation="h", y=1.15))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Model performance over time
        accuracy_trend = 0.87 + np.cumsum(np.random.normal(0.003, 0.005, len(dates)))
        accuracy_trend = np.clip(accuracy_trend, 0.80, 0.99)
        fig = go.Figure(go.Scatter(x=dates, y=accuracy_trend * 100, mode='lines',
                                   line=dict(color="#6A1B9A", width=2.5),
                                   fill='tozeroy', fillcolor="rgba(106,27,154,0.08)"))
        fig.add_hline(y=90, line_dash="dash", line_color="#dc3545", annotation_text="Target: 90%")
        fig.update_layout(title="Categorisation Accuracy Trend (%)",
                          height=300, margin=dict(l=0,r=0,t=40,b=0),
                          paper_bgcolor='white', plot_bgcolor='#f8f9fa',
                          font=dict(family="Inter", size=11))
        st.plotly_chart(fig, use_container_width=True)

    # SNP performance table
    st.markdown('<div class="section-header">🏢 SNP Performance Leaderboard</div>', unsafe_allow_html=True)
    st.dataframe(
        df_snp.sort_values("Avg Fulfilment Rate (%)", ascending=False).style
        .background_gradient(subset=["Avg Fulfilment Rate (%)", "Rating"], cmap="Greens")
        .background_gradient(subset=["Current Load (%)"], cmap="RdYlGn_r")
        .format({"Avg Fulfilment Rate (%)": "{:.1f}%", "Rating": "⭐ {:.1f}",
                 "Onboarding Avg (days)": "{:.1f}d"}),
        use_container_width=True
    )

    # Impact summary
    st.markdown('<div class="section-header">🎯 Impact Summary vs Baseline (Manual Process)</div>', unsafe_allow_html=True)
    metrics = {
        "Avg Onboarding Time (days)": (12.4, 3.8, False),
        "Application Rejection Rate (%)": (34.7, 8.2, False),
        "Categorisation Accuracy (%)": (67.3, 94.2, True),
        "Daily Processing Capacity (MSEs)": (90, 1200, True),
        "NSIC Man-hours Saved / month": (0, 800, True),
        "MSE Satisfaction (NPS)": (38, 72, True),
    }
    cats_l = list(metrics.keys())
    baseline_v = [v[0] for v in metrics.values()]
    mapmse_v = [v[1] for v in metrics.values()]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Manual (Baseline)", x=cats_l, y=baseline_v,
                         marker_color="#dc3545", opacity=0.7))
    fig.add_trace(go.Bar(name="MapMSE", x=cats_l, y=mapmse_v,
                         marker_color="#1F4E79", opacity=0.9))
    fig.update_layout(barmode='group', height=350,
                      margin=dict(l=0,r=0,t=10,b=0),
                      legend=dict(orientation="h", y=1.05),
                      paper_bgcolor='white', plot_bgcolor='#f8f9fa',
                      font=dict(family="Inter", size=10),
                      xaxis=dict(tickangle=-20, tickfont=dict(size=9)))
    st.plotly_chart(fig, use_container_width=True)
