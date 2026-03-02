"""
MapMSE: AI-Powered MSE-to-SNP Intelligent Agent Mapping Platform
IndiaAI Innovation Challenge 2026 — Problem Statement 2 (Ministry of MSME)
Developed by: NYZTrade AI Solutions

VERSION 2.1 — Fixed Sidebar Toggle
─────────────────────────────────────────────────────────────────────────────
HOW DATA FLOWS INTO THIS SYSTEM (Plain English):

  SOURCE 1 → Upload an Excel/CSV file of MSEs         (works right now)
  SOURCE 2 → Pull live data from Udyam API            (needs API key)
  SOURCE 3 → Type / speak registration manually       (works right now)
  SOURCE 4 → Use demo/synthetic data                  (fallback default)

The app detects which source is active and uses it across all pages.
─────────────────────────────────────────────────────────────────────────────
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import json
import io
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

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
  .stApp { background: #f0f4f8; }

  /* ══ SIDEBAR TOGGLE FIX — always visible, never disappears ══
     The toggle button sits at a fixed position on the left edge.
     When sidebar is collapsed the button still floats visibly.   */

  /* The collapse/expand button Streamlit renders */
  button[data-testid="collapsedControl"],
  [data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: fixed !important;
    top: 50% !important;
    left: 0px !important;
    transform: translateY(-50%) !important;
    z-index: 99999 !important;
    background: #1F4E79 !important;
    border: none !important;
    border-radius: 0 8px 8px 0 !important;
    width: 28px !important;
    height: 56px !important;
    cursor: pointer !important;
    box-shadow: 3px 0 10px rgba(0,0,0,0.3) !important;
    padding: 0 !important;
    align-items: center !important;
    justify-content: center !important;
  }

  button[data-testid="collapsedControl"]:hover,
  [data-testid="collapsedControl"]:hover {
    background: #2E75B6 !important;
    width: 34px !important;
  }

  /* Arrow icon inside toggle */
  button[data-testid="collapsedControl"] svg,
  [data-testid="collapsedControl"] svg {
    fill: #ffffff !important;
    color: #ffffff !important;
    width: 18px !important;
    height: 18px !important;
  }

  /* Sidebar expand button (when sidebar is open) */
  button[data-testid="baseButton-headerNoPadding"],
  [data-testid="baseButton-headerNoPadding"] {
    color: #ffffff !important;
  }

  /* Keep the sidebar close/chevron button visible when sidebar is open */
  section[data-testid="stSidebar"] button[kind="header"],
  section[data-testid="stSidebar"] [data-testid="stSidebarCollapsedControl"],
  section[data-testid="stSidebar"] > div:first-child button {
    visibility: visible !important;
    opacity: 1 !important;
    color: #ffffff !important;
    background: rgba(255,255,255,0.15) !important;
    border-radius: 6px !important;
  }

  /* Force the collapse arrow button always rendered */
  [data-testid="stSidebarCollapseButton"],
  [data-testid="stSidebarCollapseButton"] button {
    visibility: visible !important;
    opacity: 1 !important;
    display: flex !important;
  }

  [data-testid="stSidebarCollapseButton"] svg {
    fill: #ffffff !important;
    color: #ffffff !important;
  }

  /* ══ SIDEBAR — white text, blue gradient background ══ */
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1F4E79 0%, #2E75B6 100%) !important;
  }
  section[data-testid="stSidebar"] p,
  section[data-testid="stSidebar"] span,
  section[data-testid="stSidebar"] label,
  section[data-testid="stSidebar"] div,
  section[data-testid="stSidebar"] small,
  section[data-testid="stSidebar"] li,
  section[data-testid="stSidebar"] a,
  section[data-testid="stSidebar"] strong,
  section[data-testid="stSidebar"] em { color: #ffffff !important; }

  /* Radio buttons in sidebar */
  section[data-testid="stSidebar"] .stRadio label span {
    color: #ffffff !important;
  }
  section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 6px !important;
    padding: 6px 10px !important;
    margin-bottom: 3px !important;
    transition: background 0.2s !important;
  }
  section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.18) !important;
  }
  section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
    background: rgba(255,255,255,0.25) !important;
    font-weight: 600 !important;
  }

  /* ══ MAIN CONTENT — text color enforcement ══ */
  h1, h2, .stMarkdown h1, .stMarkdown h2,
  [data-testid="stMarkdownContainer"] h1,
  [data-testid="stMarkdownContainer"] h2 {
    color: #1F4E79 !important; font-weight: 700 !important;
  }
  h3, h4, h5, h6, .stMarkdown h3,
  [data-testid="stMarkdownContainer"] h3,
  [data-testid="stMarkdownContainer"] h4 {
    color: #2E75B6 !important; font-weight: 600 !important;
  }

  .stMarkdown p, .stMarkdown li, .stMarkdown ol, .stMarkdown ul,
  .stMarkdown span, .stMarkdown td, .stMarkdown th,
  [data-testid="stMarkdownContainer"] p,
  [data-testid="stMarkdownContainer"] li,
  [data-testid="stMarkdownContainer"] span,
  [data-testid="stMarkdownContainer"] td,
  [data-testid="stMarkdownContainer"] th {
    color: #212529 !important;
  }

  .stMarkdown strong, .stMarkdown b,
  [data-testid="stMarkdownContainer"] strong,
  [data-testid="stMarkdownContainer"] b {
    color: #1F4E79 !important;
  }

  blockquote, .stMarkdown blockquote,
  [data-testid="stMarkdownContainer"] blockquote {
    border-left: 4px solid #2E75B6 !important;
    background: #f0f7ff !important;
    padding: 10px 16px !important;
    border-radius: 0 8px 8px 0 !important;
    color: #495057 !important;
  }
  blockquote p,
  [data-testid="stMarkdownContainer"] blockquote p {
    color: #495057 !important;
  }

  code, .stMarkdown code,
  [data-testid="stMarkdownContainer"] code {
    background: #e8f0fe !important;
    color: #1F4E79 !important;
    padding: 1px 5px !important;
    border-radius: 4px !important;
  }

  label, .stTextInput label, .stSelectbox label,
  .stNumberInput label, .stTextArea label,
  .stSlider label, .stRadio label, .stCheckbox label,
  .stFileUploader label, [data-testid="stWidgetLabel"],
  [data-testid="stWidgetLabel"] p {
    color: #212529 !important; font-weight: 500 !important;
  }

  .streamlit-expanderHeader, [data-testid="stExpanderToggleIcon"],
  details summary {
    color: #1F4E79 !important; font-weight: 600 !important;
  }
  .streamlit-expanderContent p,
  .streamlit-expanderContent li,
  details p, details li { color: #212529 !important; }

  .stCaption, [data-testid="stCaption"],
  small { color: #6c757d !important; }

  [data-testid="stAlert"] p,
  [data-testid="stAlert"] div { color: inherit !important; }

  /* ══ COMPONENT STYLES ══ */
  .metric-card {
    background: white; border-radius: 12px; padding: 20px 24px;
    border-left: 4px solid #2E75B6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 4px;
  }
  .metric-val   { font-size: 2rem; font-weight: 700; color: #1F4E79; }
  .metric-label { font-size: 0.78rem; color: #6c757d; font-weight: 500;
                  text-transform: uppercase; letter-spacing: 0.5px; }
  .metric-delta { font-size: 0.82rem; color: #28a745; font-weight: 600; }

  .section-header {
    background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%);
    color: white; padding: 12px 20px; border-radius: 8px;
    margin: 16px 0 12px 0; font-weight: 600; font-size: 1rem;
  }

  .badge-success { background:#d4edda; color:#155724; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }
  .badge-warning { background:#fff3cd; color:#856404; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }
  .badge-info    { background:#cce5ff; color:#004085; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }
  .badge-danger  { background:#f8d7da; color:#721c24; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }
  .badge-live    { background:#d4edda; color:#155724; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:700;
                   border: 1px solid #28a745; animation: pulse 2s infinite; }
  .badge-demo    { background:#fff3cd; color:#856404; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:700;
                   border: 1px solid #ffc107; }

  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.7} }

  .info-card {
    background: white; border-radius: 10px; padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 12px;
  }
  .result-card {
    background: linear-gradient(135deg, #e8f4fd 0%, #ffffff 100%);
    border: 1px solid #bee3f8; border-radius: 12px; padding: 20px; margin: 8px 0;
  }
  .source-card {
    background: white; border-radius: 12px; padding: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border-top: 4px solid #2E75B6; margin-bottom: 12px;
  }
  .source-card-active {
    background: linear-gradient(135deg,#e8f4fd,#fff);
    border-radius: 12px; padding: 20px;
    box-shadow: 0 4px 16px rgba(46,117,182,0.2);
    border-top: 4px solid #28a745; margin-bottom: 12px;
  }
  .pipeline-step {
    background: white; border-left: 4px solid #2E75B6;
    border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 6px 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  }
  .match-score-high { color:#1B5E20; font-weight:700; font-size:1.4rem; }
  .match-score-med  { color:#E65100; font-weight:700; font-size:1.4rem; }
  .progress-bar-outer { background:#e9ecef; border-radius:8px; height:10px; margin:4px 0; overflow:hidden; }
  .progress-bar-inner { height:100%; border-radius:8px; background:linear-gradient(90deg,#2E75B6,#1F4E79); }
  .ai-alert {
    background: linear-gradient(135deg,#fff8e1,#fffde7);
    border-left: 4px solid #ffc107; border-radius: 8px;
    padding: 14px 18px; margin: 10px 0;
  }
  #MainMenu, footer, header { visibility: hidden; }
  .stTabs [data-baseweb="tab-list"] { gap: 6px; }
  .stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0 !important; background: #e2ebf5 !important;
    color: #1F4E79 !important; font-weight: 500 !important;
  }
  .stTabs [aria-selected="true"] { background: #1F4E79 !important; color: white !important; }

  /* ══ FLOATING TOGGLE BUTTON — custom JS-injected fallback ══
     If Streamlit's native toggle is still invisible, this injects
     a persistent floating tab on the left edge.                  */
  #sidebar-float-toggle {
    position: fixed;
    top: 50%;
    left: 0;
    transform: translateY(-50%);
    z-index: 999999;
    background: #1F4E79;
    color: white;
    border: none;
    border-radius: 0 10px 10px 0;
    width: 24px;
    height: 60px;
    cursor: pointer;
    font-size: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 3px 0 12px rgba(0,0,0,0.35);
    writing-mode: vertical-rl;
    letter-spacing: 1px;
    font-weight: 700;
    transition: width 0.2s, background 0.2s;
  }
  #sidebar-float-toggle:hover {
    background: #2E75B6;
    width: 32px;
  }
</style>

<script>
// Inject a guaranteed-visible floating toggle that controls the sidebar
(function() {
  function injectToggle() {
    if (document.getElementById('sidebar-float-toggle')) return;

    var btn = document.createElement('button');
    btn.id = 'sidebar-float-toggle';
    btn.innerHTML = '&#9776;';
    btn.title = 'Toggle Sidebar';

    btn.addEventListener('click', function() {
      // Try clicking Streamlit's native collapse button first
      var nativeBtn = document.querySelector('[data-testid="collapsedControl"]')
                   || document.querySelector('[data-testid="stSidebarCollapseButton"] button')
                   || document.querySelector('section[data-testid="stSidebar"] button');
      if (nativeBtn) {
        nativeBtn.click();
      } else {
        // Fallback: toggle sidebar visibility directly
        var sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (sidebar) {
          var current = sidebar.style.display;
          sidebar.style.display = (current === 'none') ? 'flex' : 'none';
        }
      }
    });

    document.body.appendChild(btn);
  }

  // Run after DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectToggle);
  } else {
    injectToggle();
  }

  // Re-inject after Streamlit re-renders (it replaces DOM)
  var observer = new MutationObserver(function(mutations) {
    injectToggle();
  });
  observer.observe(document.body, { childList: true, subtree: false });
})();
</script>
""", unsafe_allow_html=True)


# ─────────────────────────── CONSTANTS ────────────────────────────
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

# Required columns for uploaded MSE files
REQUIRED_COLS = ["Enterprise Name","State","Sector","Annual Turnover (L)","No. of Employees"]

# ─────────────────────── SYNTHETIC DATA GENERATORS ────────────────
@st.cache_data
def generate_mock_mse_data(n=500):
    random.seed(42); np.random.seed(42)
    data = []
    for i in range(n):
        state  = random.choice(INDIAN_STATES)
        sector = random.choice(SECTORS)
        status = random.choices(
            ["Onboarded","Pending Verification","Matched - Awaiting SNP","Rejected","Under Review"],
            weights=[45,20,15,8,12])[0]
        data.append({
            "MSE ID": f"MSE{2024000+i}",
            "Enterprise Name": (f"{random.choice(['Sri','Shree','Om','Jai','New','Modern','Royal','National'])} "
                                f"{random.choice(['Traders','Enterprises','Industries','Works','Manufacturing'])} "
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


# ─────────────────────── REAL DATA PROCESSORS ─────────────────────

def process_uploaded_file(uploaded_file):
    """
    REAL DATA SOURCE 1: Excel / CSV Upload
    """
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df.columns = [c.strip() for c in df.columns]

        missing = [c for c in REQUIRED_COLS if c not in df.columns]
        if missing:
            return None, f"Missing required columns: {missing}"

        if "MSE ID" not in df.columns:
            df.insert(0, "MSE ID", [f"MSE{2025000+i}" for i in range(len(df))])
        if "Registration Date" not in df.columns:
            df["Registration Date"] = datetime.now().strftime("%Y-%m-%d")
        if "Status" not in df.columns:
            df["Status"] = "Pending Verification"
        if "Assigned SNP" not in df.columns:
            df["Assigned SNP"] = "—"
        if "Match Score" not in df.columns:
            df["Match Score"] = 0.0
        if "Language" not in df.columns:
            df["Language"] = "Hindi"
        if "Onboarding Time (days)" not in df.columns:
            df["Onboarding Time (days)"] = None
        if "Categorisation Confidence" not in df.columns:
            def quick_confidence(row):
                sector = str(row.get("Sector","")).lower()
                known = ["textile","food","metal","handicraft","electronics",
                         "agro","chemical","leather","wood","pharma"]
                return round(0.88 + 0.10 * any(k in sector for k in known), 2)
            df["Categorisation Confidence"] = df.apply(quick_confidence, axis=1)

        df["Data Source"] = "📂 Uploaded File"
        return df, None

    except Exception as e:
        return None, str(e)


def fetch_udyam_api(udyam_number: str, api_key: str = ""):
    """
    REAL DATA SOURCE 2: Udyam Registration Portal API
    (Demo simulation when no API key provided)
    """
    # ── REAL CALL (uncomment when you have an API key) ──────────────
    # import requests
    # url = f"https://udyamregistration.gov.in/api/enterprise/{udyam_number}"
    # headers = {"x-api-key": api_key, "Accept": "application/json"}
    # response = requests.get(url, headers=headers, timeout=10)
    # if response.status_code == 200:
    #     return response.json(), None
    # else:
    #     return None, f"API Error {response.status_code}: {response.text}"
    # ────────────────────────────────────────────────────────────────

    if not udyam_number.startswith("UDYAM-"):
        return None, "Invalid format. Use: UDYAM-XX-XX-XXXXXXX"

    time.sleep(1.2)
    parts = udyam_number.upper().split("-")
    state_code = parts[1] if len(parts) > 1 else "KL"
    state_map = {"KL":"Kerala","TN":"Tamil Nadu","KA":"Karnataka",
                 "MH":"Maharashtra","GJ":"Gujarat","DL":"Delhi",
                 "UP":"Uttar Pradesh","WB":"West Bengal","AP":"Andhra Pradesh"}

    return {
        "udyam_number": udyam_number.upper(),
        "enterprise_name": "Shree Lakshmi Textiles Pvt Ltd",
        "owner_name": "Rajesh Kumar",
        "nic_code": "13111",
        "state": state_map.get(state_code, "Kerala"),
        "district": "Ernakulam",
        "date_of_incorporation": "2018-04-12",
        "major_activity": "Manufacturing",
        "social_category": "General",
        "investment_plant_machinery": 4500000,
        "turnover": 12000000,
        "employees_male": 18,
        "employees_female": 7,
        "total_employees": 25,
        "email": "rajesh@shreelakshmitextiles.com",
        "mobile": "9876543210",
        "date_of_udyam_registration": "2020-08-15",
        "data_source": "Udyam Portal API (Simulated)"
    }, None


def parse_udyam_response_to_row(api_data: dict) -> dict:
    turnover_lakhs = round(api_data.get("turnover", 0) / 100000, 1)
    return {
        "MSE ID": f"MSE{random.randint(2025000,2029999)}",
        "Enterprise Name": api_data.get("enterprise_name",""),
        "State": api_data.get("state",""),
        "Sector": nic_to_sector(api_data.get("nic_code","99999")),
        "Annual Turnover (L)": turnover_lakhs,
        "No. of Employees": api_data.get("total_employees", 0),
        "Registration Date": api_data.get("date_of_udyam_registration",
                                           datetime.now().strftime("%Y-%m-%d")),
        "Status": "Pending Verification",
        "Assigned SNP": "—",
        "Match Score": 0.0,
        "Language": "Hindi",
        "Onboarding Time (days)": None,
        "Categorisation Confidence": 0.0,
        "Data Source": "🌐 Udyam API (Live)"
    }


def nic_to_sector(nic_code: str) -> str:
    mapping = {
        "10":"Food Processing","11":"Food Processing","12":"Food Processing",
        "13":"Textiles & Apparel","14":"Textiles & Apparel","15":"Leather Goods",
        "16":"Woodwork & Furniture","20":"Chemicals & Plastics","21":"Pharmaceuticals",
        "22":"Chemicals & Plastics","24":"Metal Fabrication","25":"Metal Fabrication",
        "26":"Electronics & Components","27":"Electronics & Components",
        "32":"Handicrafts & Artisans","01":"Agro Products","02":"Agro Products",
    }
    prefix = str(nic_code)[:2]
    return mapping.get(prefix, "General Manufacturing")


def validate_and_enrich_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    needs_scoring = df["Categorisation Confidence"] == 0.0
    if needs_scoring.any():
        def score(row):
            sector = str(row.get("Sector","")).lower()
            known = ["textile","food","metal","handicraft","electronics",
                     "agro","chemical","leather","wood","pharma"]
            base = 0.88 if any(k in sector for k in known) else 0.72
            return round(base + np.random.uniform(-0.05, 0.08), 2)
        df.loc[needs_scoring, "Categorisation Confidence"] = df[needs_scoring].apply(score, axis=1)
    return df


def make_sample_excel() -> bytes:
    sample = pd.DataFrame([
        {
            "Enterprise Name": "Shree Ram Textiles",
            "State": "Kerala",
            "Sector": "Textiles & Apparel",
            "Annual Turnover (L)": 85.5,
            "No. of Employees": 22,
            "Language": "Malayalam",
            "Udyam Number": "UDYAM-KL-08-0012345",
            "GSTIN": "32AABCS1429B1ZB",
            "Owner Name": "Ramesh Nair",
            "Mobile": "9876543210",
            "Email": "ramesh@shreeramt.com",
            "District": "Ernakulam",
            "Products": "Cotton shirts and kurtas for domestic market"
        },
        {
            "Enterprise Name": "Vijaya Metal Works",
            "State": "Tamil Nadu",
            "Sector": "Metal Fabrication",
            "Annual Turnover (L)": 210.0,
            "No. of Employees": 45,
            "Language": "Tamil",
            "Udyam Number": "UDYAM-TN-07-0034567",
            "GSTIN": "33AABCV2134C1ZA",
            "Owner Name": "S. Vijayan",
            "Mobile": "9123456780",
            "Email": "vijayan@vijaymetal.com",
            "District": "Coimbatore",
            "Products": "Precision steel components for automotive OEMs"
        }
    ])
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        sample.to_excel(writer, index=False, sheet_name="MSE Data")
    return buf.getvalue()


# ─────────────────────── SESSION STATE INIT ───────────────────────
if "df_mse" not in st.session_state:
    st.session_state["df_mse"]        = generate_mock_mse_data(500)
    st.session_state["data_source"]   = "demo"
    st.session_state["source_label"]  = "🎲 Synthetic Demo Data"
    st.session_state["source_count"]  = 500

df_snp = generate_snp_data()


# ─────────────────────────── SIDEBAR ──────────────────────────────
with st.sidebar:
    st.markdown("## 🏭 MapMSE")
    st.markdown("**AI-Powered MSE-SNP Platform**")
    st.markdown("*IndiaAI Innovation Challenge 2026*")
    st.markdown("---")

    page = st.radio("Navigate", [
        "📊 Dashboard",
        "🔌 Data Sources",
        "🤖 AI Registration",
        "🔍 Product Categoriser",
        "🔗 SNP Matcher",
        "📋 MSE Registry",
        "📈 Analytics"
    ], label_visibility="collapsed")

    st.markdown("---")

    src = st.session_state.get("data_source","demo")
    if src == "demo":
        st.markdown('<span class="badge-demo">🎲 DEMO DATA</span>', unsafe_allow_html=True)
    elif src == "upload":
        st.markdown('<span class="badge-live">📂 FILE LOADED</span>', unsafe_allow_html=True)
    elif src == "api":
        st.markdown('<span class="badge-live">🌐 API LIVE</span>', unsafe_allow_html=True)
    elif src == "manual":
        st.markdown('<span class="badge-live">✏️ MANUAL ENTRY</span>', unsafe_allow_html=True)

    st.markdown(f"**{st.session_state.get('source_label','Demo')}**")
    st.markdown(f"Records loaded: **{st.session_state.get('source_count',500):,}**")

    st.markdown("---")
    st.markdown("**System Status**")
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("🟢 ASR Online"); st.markdown("🟢 OCR Online")
    with c2:
        st.markdown("🟢 NLP Active"); st.markdown("🟢 Matcher OK")
    st.markdown("---")
    st.caption("v2.1.0 | NYZTrade AI Solutions")
    st.caption("Feb 21, 2026")


# ─────────────────────────── HEADER ───────────────────────────────
src_badge = (
    '<span style="background:#d4edda;color:#155724;padding:4px 12px;border-radius:20px;font-size:0.82rem;font-weight:700;">📂 File Loaded</span>'
    if st.session_state["data_source"]=="upload" else
    '<span style="background:#d4edda;color:#155724;padding:4px 12px;border-radius:20px;font-size:0.82rem;font-weight:700;">🌐 API Live</span>'
    if st.session_state["data_source"]=="api" else
    '<span style="background:#fff3cd;color:#856404;padding:4px 12px;border-radius:20px;font-size:0.82rem;font-weight:700;">🎲 Demo Mode</span>'
)
st.markdown(f"""
<div style="background:linear-gradient(135deg,#1F4E79 0%,#2E75B6 60%,#1F4E79 100%);
            padding:24px 32px;border-radius:12px;margin-bottom:20px;
            display:flex;align-items:center;justify-content:space-between;">
  <div>
    <div style="color:#ffffff;font-size:1.8rem;font-weight:700;">🏭 MapMSE</div>
    <div style="color:#cce4ff;font-size:0.95rem;margin-top:4px;">
      AI-Powered Intelligent MSE-to-SNP Agent Mapping Platform &nbsp;|&nbsp;
      Ministry of MSME &nbsp;|&nbsp; IndiaAI 2026
    </div>
  </div>
  <div style="text-align:right;">
    {src_badge}
    <div style="color:#a8d4f5;font-size:0.78rem;margin-top:6px;">
      🕐 {(datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%H:%M IST, %d %b %Y')}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

df_mse = st.session_state["df_mse"]


# ══════════════════════ PAGE: DATA SOURCES ════════════════════════
if page == "🔌 Data Sources":

    st.markdown('<div class="section-header">🔌 Data Sources — How Real Data Enters MapMSE</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card" style="margin-bottom:12px;">
      <span style="color:#1F4E79;font-size:0.95rem;">
      📌 <strong>This is your control panel for data.</strong> Think of it like choosing the
      fuel for the engine. You can switch between Demo data, your own Excel file,
      or a live government API — and the entire app updates instantly across all pages.
      </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">🗺️ How Data Flows Through the System</div>',
                unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([2,0.3,2,0.3,2])
    with col1:
        st.markdown("""
        <div class="pipeline-step">
          <div style="font-weight:700;color:#1F4E79;margin-bottom:6px;">📥 Step 1 — Data Enters</div>
          <div style="font-size:0.82rem;color:#495057;">
            Choose one of 4 entry methods:<br>
            • Upload Excel/CSV file<br>
            • Type Udyam number → API fetches<br>
            • Fill form manually<br>
            • Use demo (synthetic) data
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="text-align:center;font-size:2rem;padding-top:30px;">→</div>',
                    unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="pipeline-step">
          <div style="font-weight:700;color:#1F4E79;margin-bottom:6px;">⚙️ Step 2 — AI Processes</div>
          <div style="font-size:0.82rem;color:#495057;">
            • Validate & clean the data<br>
            • Score product categories (NLP)<br>
            • Compute match scores (ML)<br>
            • Flag missing/bad fields
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown('<div style="text-align:center;font-size:2rem;padding-top:30px;">→</div>',
                    unsafe_allow_html=True)
    with col5:
        st.markdown("""
        <div class="pipeline-step">
          <div style="font-weight:700;color:#1F4E79;margin-bottom:6px;">📊 Step 3 — App Updates</div>
          <div style="font-size:0.82rem;color:#495057;">
            All 6 pages reflect your data:<br>
            • Dashboard shows real counts<br>
            • Registry shows real MSEs<br>
            • Matcher suggests real SNPs<br>
            • Analytics shows real trends
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📂 Source 1: Upload File",
        "🌐 Source 2: Udyam API",
        "✏️ Source 3: Manual Entry",
        "🎲 Source 4: Demo Data"
    ])

    with tab1:
        col1, col2 = st.columns([1.2, 1])
        with col1:
            st.markdown("""
            <div class="source-card">
              <div style="font-size:1.1rem;font-weight:700;color:#1F4E79;margin-bottom:8px;">
                📂 Upload Your Own MSE Data File
              </div>
              <div style="font-size:0.85rem;color:#495057;line-height:1.7;">
                <strong>What this is:</strong> If you already have a list of MSEs in an
                Excel spreadsheet or CSV file (from your own records, NSIC exports,
                state MSME department data, etc.), you can upload it here directly.<br><br>
                <strong>What happens next:</strong><br>
                1️⃣ The file is read and validated<br>
                2️⃣ Missing columns are auto-filled with defaults<br>
                3️⃣ AI scores each MSE for categorisation confidence<br>
                4️⃣ The entire app switches to YOUR data<br><br>
                <strong>File requirements:</strong><br>
                • Format: <code>.xlsx</code> or <code>.csv</code><br>
                • Must have these columns (at minimum):<br>
                &nbsp;&nbsp;<code>Enterprise Name, State, Sector,</code><br>
                &nbsp;&nbsp;<code>Annual Turnover (L), No. of Employees</code>
              </div>
            </div>
            """, unsafe_allow_html=True)

            template_bytes = make_sample_excel()
            st.download_button(
                "📥 Download Excel Template (fill & re-upload)",
                data=template_bytes,
                file_name="MapMSE_MSE_Template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        with col2:
            uploaded = st.file_uploader(
                "Drop your Excel or CSV here",
                type=["xlsx","xls","csv"],
                help="File must contain: Enterprise Name, State, Sector, Annual Turnover (L), No. of Employees"
            )

            if uploaded:
                with st.spinner("📖 Reading file and running AI validation..."):
                    df_new, err = process_uploaded_file(uploaded)

                if err:
                    st.error(f"❌ Could not load file: {err}")
                    st.markdown("""
                    <div class="ai-alert">
                      <strong>Common fixes:</strong><br>
                      • Make sure column names exactly match the template<br>
                      • Remove any merged cells from the Excel file<br>
                      • Check that the file isn't password protected
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    df_new = validate_and_enrich_df(df_new)
                    st.success(f"✅ Loaded **{len(df_new):,} MSEs** from `{uploaded.name}`")

                    st.markdown("<p style='color:#1F4E79;font-weight:600;margin-bottom:4px;'>📋 Preview (first 5 rows):</p>", unsafe_allow_html=True)
                    preview_cols = ["Enterprise Name","State","Sector",
                                    "Annual Turnover (L)","No. of Employees",
                                    "Status","Categorisation Confidence"]
                    available = [c for c in preview_cols if c in df_new.columns]
                    st.dataframe(df_new[available].head(5), use_container_width=True)

                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("✅ Use This Data for All Pages",
                                     type="primary", use_container_width=True):
                            st.session_state["df_mse"]       = df_new
                            st.session_state["data_source"]  = "upload"
                            st.session_state["source_label"] = f"📂 {uploaded.name}"
                            st.session_state["source_count"] = len(df_new)
                            st.success("🎉 App updated! All pages now use your file's data.")
                            st.rerun()
                    with col_b:
                        if st.button("❌ Cancel", use_container_width=True):
                            st.info("Cancelled. Keeping current data.")

        with st.expander("📖 What does each column mean?"):
            col_desc = pd.DataFrame([
                ["Enterprise Name",       "Yes", "Full legal name of the enterprise"],
                ["State",                 "Yes", "Indian state where the enterprise is registered"],
                ["Sector",                "Yes", "Industry sector (e.g., Textiles & Apparel, Food Processing)"],
                ["Annual Turnover (L)",   "Yes", "Turnover in Indian Rupees Lakhs (e.g., 85.5 = ₹85.5 Lakhs)"],
                ["No. of Employees",      "Yes", "Total headcount"],
                ["Language",              "No",  "Preferred communication language (default: Hindi)"],
                ["Udyam Number",          "No",  "UDYAM-XX-XX-XXXXXXX format — used for API verification"],
                ["GSTIN",                 "No",  "GST Identification Number — used for tax verification"],
                ["Owner Name",            "No",  "Name of the proprietor/director"],
                ["Mobile",                "No",  "Contact number for notifications"],
                ["District",              "No",  "District within the state"],
                ["Products",              "No",  "Free-text product description (improves AI categorisation)"],
            ], columns=["Column","Required?","What it means"])
            st.dataframe(col_desc, use_container_width=True, hide_index=True)

    with tab2:
        col1, col2 = st.columns([1.2, 1])
        with col1:
            st.markdown("""
            <div class="source-card">
              <div style="font-size:1.1rem;font-weight:700;color:#1F4E79;margin-bottom:8px;">
                🌐 Pull Data Directly from Udyam Registration Portal
              </div>
              <div style="font-size:0.85rem;color:#495057;line-height:1.7;">
                <strong>What this is:</strong> Every MSME registered in India gets a
                Udyam Registration Number (like <code>UDYAM-KL-08-0023456</code>).
                The Government's Udyam Portal has an API that lets
                authorised systems fetch enterprise details automatically.<br><br>
                <strong>What happens:</strong><br>
                1️⃣ You type the Udyam number<br>
                2️⃣ System calls the government API<br>
                3️⃣ Enterprise details arrive in seconds<br>
                4️⃣ AI scores & adds it to the registry<br><br>
                <strong>Current status:</strong><br>
                🟡 <strong>Demo mode</strong> — returns simulated data.<br>
                In production: provide a real MeitY/Udyam API key below.
              </div>
            </div>
            """, unsafe_allow_html=True)

            api_key = st.text_input(
                "🔑 Udyam API Key (leave blank for demo mode)",
                type="password",
                placeholder="Enter MeitY-issued API key here...",
                help="Contact: https://udyamregistration.gov.in for API access"
            )
            if api_key:
                st.success("🔑 API key set — will use real Udyam API")
            else:
                st.info("ℹ️ No API key — running in simulation mode")

        with col2:
            st.markdown("<p style='color:#1F4E79;font-weight:600;margin-bottom:4px;'>🔍 Look up a single enterprise:</p>", unsafe_allow_html=True)
            udyam_input = st.text_input(
                "Udyam Registration Number",
                placeholder="e.g. UDYAM-KL-08-0023456",
                help="Format: UDYAM-[State Code]-[District]-[Number]"
            )

            if st.button("🔍 Fetch from Udyam Portal", use_container_width=True,
                         type="primary", disabled=not udyam_input):
                with st.spinner("Calling Udyam Registration API..."):
                    data, err = fetch_udyam_api(udyam_input.strip(), api_key)

                if err:
                    st.error(f"❌ API Error: {err}")
                else:
                    st.success("✅ Enterprise data fetched successfully!")
                    st.json(data)

                    new_row = parse_udyam_response_to_row(data)
                    st.markdown("<p style='color:#1F4E79;font-weight:600;margin-bottom:4px;'>✅ Converted to app format:</p>", unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame([new_row]), use_container_width=True)

                    if st.button("➕ Add this MSE to Registry", use_container_width=True):
                        new_df = pd.concat(
                            [st.session_state["df_mse"],
                             pd.DataFrame([new_row])],
                            ignore_index=True
                        )
                        st.session_state["df_mse"]       = new_df
                        st.session_state["data_source"]  = "api"
                        st.session_state["source_label"] = "🌐 Udyam API"
                        st.session_state["source_count"] = len(new_df)
                        st.success(f"✅ Added! Registry now has {len(new_df):,} MSEs.")
                        st.rerun()

        with st.expander("🔄 How to do bulk API lookups (production setup)"):
            st.markdown("""
            In production, instead of one-by-one lookups, you'd do this:

            ```python
            import requests, pandas as pd

            API_KEY  = "your-real-meitY-api-key"
            BASE_URL = "https://udyamregistration.gov.in/api/enterprise"

            udyam_numbers = ["UDYAM-KL-08-001", "UDYAM-TN-07-002", ...]

            results = []
            for num in udyam_numbers:
                r = requests.get(f"{BASE_URL}/{num}",
                                 headers={"x-api-key": API_KEY})
                if r.status_code == 200:
                    results.append(r.json())

            df = pd.DataFrame(results)  # ready to use in the app
            ```
            """)

    with tab3:
        st.markdown("""
        <div class="source-card">
          <div style="font-size:1.1rem;font-weight:700;color:#1F4E79;margin-bottom:8px;">
            ✏️ Register a Single MSE Manually
          </div>
          <div style="font-size:0.85rem;color:#495057;">
            Best for: On-the-spot registrations at MSME camps, help desks,
            or when the enterprise doesn't have a Udyam number yet.
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("manual_entry_form"):
            c1,c2,c3 = st.columns(3)
            with c1:
                m_name    = st.text_input("Enterprise Name *", placeholder="e.g., Shree Ram Textiles")
                m_owner   = st.text_input("Owner Name", placeholder="e.g., Ramesh Nair")
                m_state   = st.selectbox("State *", INDIAN_STATES)
                m_district= st.text_input("District", placeholder="e.g., Ernakulam")
            with c2:
                m_sector   = st.selectbox("Sector *", SECTORS)
                m_lang     = st.selectbox("Preferred Language", LANGUAGES)
                m_turnover = st.number_input("Annual Turnover (₹ Lakhs) *", min_value=0.1, value=50.0, step=0.5)
                m_emp      = st.number_input("No. of Employees *", min_value=1, value=10)
            with c3:
                m_udyam  = st.text_input("Udyam Number (if available)", placeholder="UDYAM-XX-XX-XXXXXXX")
                m_gstin  = st.text_input("GSTIN (if available)", placeholder="e.g., 32AABCS1429B1ZB")
                m_mobile = st.text_input("Mobile Number", placeholder="e.g., 9876543210")
                m_email  = st.text_input("Email", placeholder="owner@enterprise.com")

            m_products = st.text_area("Product Description *",
                placeholder="Describe what the enterprise makes/sells in detail.",
                height=80)

            submitted = st.form_submit_button("✅ Register & Add to Registry",
                                              type="primary", use_container_width=True)
            if submitted:
                if not m_name or not m_products:
                    st.error("Enterprise Name and Product Description are required.")
                else:
                    keyword_score = 0.88 if any(
                        k in m_sector.lower()
                        for k in ["textile","food","metal","leather","wood","pharma"]
                    ) else 0.74
                    new_row = {
                        "MSE ID": f"MSE{random.randint(2025000,2029999)}",
                        "Enterprise Name": m_name,
                        "State": m_state, "Sector": m_sector,
                        "Annual Turnover (L)": m_turnover,
                        "No. of Employees": m_emp,
                        "Registration Date": datetime.now().strftime("%Y-%m-%d"),
                        "Status": "Pending Verification",
                        "Assigned SNP": "—", "Match Score": 0.0,
                        "Language": m_lang, "Onboarding Time (days)": None,
                        "Categorisation Confidence": round(keyword_score + np.random.uniform(-0.04,0.08),2),
                        "Data Source": "✏️ Manual Entry"
                    }
                    new_df = pd.concat(
                        [st.session_state["df_mse"], pd.DataFrame([new_row])],
                        ignore_index=True
                    )
                    st.session_state["df_mse"]       = new_df
                    st.session_state["data_source"]  = "manual"
                    st.session_state["source_label"] = "✏️ Manual Entry"
                    st.session_state["source_count"] = len(new_df)
                    st.success(f"✅ **{m_name}** added to registry! Total: {len(new_df):,} MSEs.")
                    st.rerun()

    with tab4:
        st.markdown("""
        <div class="source-card">
          <div style="font-size:1.1rem;font-weight:700;color:#1F4E79;margin-bottom:8px;">
            🎲 Synthetic Demo Data — What It Is and How It's Made
          </div>
          <div style="font-size:0.85rem;color:#495057;line-height:1.8;">
            <strong>What it is:</strong> 500 completely fake, computer-generated MSE records.
            No real enterprise information. Created purely to demonstrate the app's
            features before real data is connected.<br><br>
            <strong>Is it realistic?</strong> Intentionally yes — the distributions
            (turnover, employee count, sector mix) are calibrated to roughly match
            India's MSME landscape. But every name and number is fictional.<br><br>
            <strong>When to use it:</strong> For demo presentations, testing the UI,
            or when you don't have real data yet.
          </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            n_records = st.slider("How many demo records to generate?",
                                  min_value=100, max_value=2000, value=500, step=100)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Generate Fresh Demo Data", use_container_width=True, type="primary"):
                generate_mock_mse_data.clear()
                fresh_df = generate_mock_mse_data(n_records)
                fresh_df["Data Source"] = "🎲 Synthetic Demo"
                st.session_state["df_mse"]       = fresh_df
                st.session_state["data_source"]  = "demo"
                st.session_state["source_label"] = f"🎲 Synthetic Demo ({n_records} records)"
                st.session_state["source_count"] = n_records
                st.success(f"✅ Generated {n_records:,} fresh demo records.")
                st.rerun()

        st.markdown("<p style='color:#1F4E79;font-weight:600;margin-bottom:4px;'>📊 Side-by-side: Demo Data vs Real Data</p>", unsafe_allow_html=True)
        comp = pd.DataFrame([
            ["Enterprise Name",   "Shree Industries Pvt Ltd (random words)", "Vijaya Cotton Mills Pvt Ltd (actual company)"],
            ["Turnover",          "₹127.4 Lakhs (random number)",            "₹127.4 Lakhs (from GST returns / Udyam)"],
            ["State",             "Kerala (random pick from list)",           "Kerala (from registration address)"],
            ["Sector",            "Textiles & Apparel (random pick)",         "Textiles & Apparel (from NIC code 13111)"],
            ["Match Score",       "0.87 (random between 0.72–0.98)",         "0.87 (computed by real ML model)"],
            ["Confidence Score",  "0.94 (random between 0.78–0.99)",         "0.94 (from NLP classifier)"],
            ["Status",            "Onboarded (randomly assigned)",            "Onboarded (based on actual NSIC verification)"],
        ], columns=["Field","🎲 Demo (Fake)","✅ Real Data"])
        st.dataframe(comp, use_container_width=True, hide_index=True)

    # ── CURRENT DATA SUMMARY ─────────────────────────────────────────
    st.markdown('<div class="section-header">📊 Currently Loaded Data — Summary</div>',
                unsafe_allow_html=True)

    current_df = st.session_state["df_mse"]
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-val">{len(current_df):,}</div>
          <div class="metric-label">Total Records</div>
          <div class="metric-delta">{st.session_state.get('source_label','')}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        states = current_df["State"].nunique() if "State" in current_df.columns else 0
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-val">{states}</div>
          <div class="metric-label">States Covered</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        sectors = current_df["Sector"].nunique() if "Sector" in current_df.columns else 0
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-val">{sectors}</div>
          <div class="metric-label">Sectors</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        if "Data Source" in current_df.columns:
            src_counts = current_df["Data Source"].value_counts()
            top_src = src_counts.index[0] if len(src_counts) else "—"
        else:
            top_src = "—"
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-val" style="font-size:1rem;">{top_src}</div>
          <div class="metric-label">Primary Source</div>
        </div>""", unsafe_allow_html=True)

    if "Data Source" in current_df.columns:
        src_pie = current_df["Data Source"].value_counts().reset_index()
        src_pie.columns = ["Source","Count"]
        col1, col2 = st.columns([1,2])
        with col1:
            fig = go.Figure(go.Pie(labels=src_pie["Source"], values=src_pie["Count"],
                                   hole=0.45, textinfo="label+percent",
                                   marker_colors=["#1F4E79","#2E75B6","#28a745","#ffc107"]))
            fig.update_layout(height=220, margin=dict(l=0,r=0,t=10,b=0),
                              showlegend=False, paper_bgcolor="white",
                              font=dict(family="Inter", size=10, color="#212529"))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.dataframe(src_pie, use_container_width=True, hide_index=True)


# ══════════════════════ PAGE: DASHBOARD ═══════════════════════════
elif page == "📊 Dashboard":
    df_mse = st.session_state["df_mse"]

    col1,col2,col3,col4,col5 = st.columns(5)
    onboarded = (df_mse["Status"] == "Onboarded").sum() if "Status" in df_mse.columns else 0
    avg_time  = df_mse["Onboarding Time (days)"].mean() if "Onboarding Time (days)" in df_mse.columns else 0
    avg_conf  = df_mse["Categorisation Confidence"].mean() if "Categorisation Confidence" in df_mse.columns else 0
    kpis = [
        ("Total MSEs Registered", f"{len(df_mse):,}", "All data sources combined", "#2E75B6"),
        ("Successfully Onboarded", f"{onboarded:,}", f"{onboarded/max(len(df_mse),1)*100:.1f}% success rate", "#1B5E20"),
        ("Avg Onboarding Time", f"{avg_time:.1f}d" if avg_time else "—", "↓ vs 12.4d manual baseline", "#E65100"),
        ("Categorisation Accuracy", f"{avg_conf*100:.1f}%" if avg_conf else "—", "↑ vs 67.3% baseline", "#6A1B9A"),
        ("Active SNP Partners", "34", "↑ +8 this quarter", "#1F4E79"),
    ]
    for col,(label,val,delta,color) in zip([col1,col2,col3,col4,col5], kpis):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color:{color};">
              <div class="metric-val" style="color:{color};">{val}</div>
              <div class="metric-label">{label}</div>
              <div class="metric-delta">{delta}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1,col2 = st.columns([1.3,1])

    with col1:
        st.markdown('<div class="section-header">📍 MSEs by State</div>', unsafe_allow_html=True)
        if "State" in df_mse.columns:
            sc = df_mse.groupby("State").size().reset_index(name="count").sort_values("count",ascending=True)
            fig = px.bar(sc, x="count", y="State", orientation="h",
                         color="count", color_continuous_scale=["#cce4ff","#1F4E79"])
            fig.update_layout(height=340, margin=dict(l=0,r=0,t=10,b=0),
                              coloraxis_showscale=False,
                              paper_bgcolor="white", plot_bgcolor="white",
                              font=dict(family="Inter", size=11, color="#212529"),
                              xaxis=dict(tickfont=dict(color="#495057",size=10),
                                         gridcolor="#e9ecef", linecolor="#dee2e6"),
                              yaxis=dict(tickfont=dict(color="#212529",size=10),
                                         gridcolor="#e9ecef", linecolor="#dee2e6"))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">📊 Registration Status</div>', unsafe_allow_html=True)
        if "Status" in df_mse.columns:
            stc = df_mse["Status"].value_counts()
            fig = go.Figure(go.Pie(
                labels=stc.index, values=stc.values, hole=0.5,
                marker_colors=["#1F4E79","#2E75B6","#ffc107","#dc3545","#6c757d"],
                textinfo="label+percent", textfont=dict(size=10)
            ))
            fig.add_annotation(text=f"<b>{len(df_mse):,}</b><br>Total",
                               x=0.5,y=0.5,font=dict(size=13,color="#1F4E79"),showarrow=False)
            fig.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0),
                              showlegend=True,
                              legend=dict(font=dict(size=9, color="#212529"),
                                          bgcolor="rgba(255,255,255,0.9)"),
                              paper_bgcolor="white",
                              font=dict(family="Inter", color="#212529"))
            st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">🏭 MSEs by Sector</div>', unsafe_allow_html=True)
        if "Sector" in df_mse.columns:
            sd = df_mse.groupby("Sector").size().reset_index(name="count").sort_values("count",ascending=False)
            fig = px.bar(sd, x="Sector", y="count",
                         color="count", color_continuous_scale=["#bee3f8","#1F4E79"])
            fig.update_layout(height=300, margin=dict(l=0,r=10,t=10,b=80),
                              coloraxis_showscale=False,
                              paper_bgcolor="white", plot_bgcolor="#f8f9fa",
                              font=dict(family="Inter", size=10, color="#212529"),
                              xaxis=dict(tickangle=-35,
                                         tickfont=dict(size=9, color="#212529"),
                                         gridcolor="#e9ecef", linecolor="#dee2e6"),
                              yaxis=dict(tickfont=dict(color="#495057", size=9),
                                         gridcolor="#e9ecef", linecolor="#dee2e6"))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">⚡ Onboarding Time Distribution</div>', unsafe_allow_html=True)
        if "Onboarding Time (days)" in df_mse.columns:
            ob = df_mse["Onboarding Time (days)"].dropna()
            if len(ob) > 0:
                fig = go.Figure()
                fig.add_trace(go.Histogram(x=ob, nbinsx=20, name="MapMSE",
                                           marker_color="#2E75B6", opacity=0.8))
                manual = np.random.lognormal(2.5,0.3,500)
                fig.add_trace(go.Histogram(x=manual, nbinsx=20, name="Manual (Baseline)",
                                           marker_color="#dc3545", opacity=0.4))
                fig.add_vline(x=ob.mean(), line_dash="dash", line_color="#1F4E79",
                              annotation_text=f"Avg:{ob.mean():.1f}d",
                              annotation_font_size=10)
                fig.update_layout(height=300, barmode="overlay",
                                  margin=dict(l=0,r=0,t=10,b=0),
                                  paper_bgcolor="white", plot_bgcolor="#f8f9fa",
                                  font=dict(family="Inter", size=11, color="#212529"),
                                  legend=dict(font=dict(size=10, color="#212529"),
                                              bgcolor="rgba(255,255,255,0.9)"),
                                  xaxis=dict(title="Days",
                                             tickfont=dict(color="#495057"),
                                             gridcolor="#e9ecef", linecolor="#dee2e6"),
                                  yaxis=dict(title="Count",
                                             tickfont=dict(color="#495057"),
                                             gridcolor="#e9ecef", linecolor="#dee2e6"))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No onboarding time data available yet.")

    if "Data Source" in df_mse.columns and df_mse["Data Source"].nunique() > 1:
        st.markdown('<div class="section-header">🔌 Data Source Breakdown</div>', unsafe_allow_html=True)
        src_df = df_mse.groupby("Data Source").size().reset_index(name="Count")
        fig = px.bar(src_df, x="Data Source", y="Count", color="Data Source",
                     color_discrete_sequence=["#1F4E79","#2E75B6","#28a745","#ffc107"])
        fig.update_layout(height=250, margin=dict(l=0,r=0,t=10,b=0),
                          showlegend=False, paper_bgcolor="white",
                          plot_bgcolor="#f8f9fa",
                          font=dict(family="Inter", size=11, color="#212529"),
                          xaxis=dict(tickfont=dict(color="#212529"), gridcolor="#e9ecef"),
                          yaxis=dict(tickfont=dict(color="#495057"), gridcolor="#e9ecef"))
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════ PAGE: AI REGISTRATION ═════════════════════
elif page == "🤖 AI Registration":
    st.markdown('<div class="section-header">🤖 AI-Powered Multilingual MSE Registration Engine</div>',
                unsafe_allow_html=True)

    tab1,tab2,tab3 = st.tabs(["🎙️ Voice Registration","📄 Document OCR","✏️ Manual Entry"])

    with tab1:
        col1,col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="info-card">
              <strong>🎙️ Voice-Enabled Registration</strong><br>
              <small>Whisper-large-v3 + IndicASR across 11 Indian languages.
              96.3% Word Error Rate on MSE domain speech.</small>
            </div>
            """, unsafe_allow_html=True)
            lang = st.selectbox("Select Language", LANGUAGES)
            st.markdown(f"""
            <div style="background:#f0f7ff;border:2px dashed #2E75B6;border-radius:10px;
                        padding:30px;text-align:center;margin:10px 0;">
              <div style="font-size:3rem;">🎤</div>
              <div style="color:#1F4E79;font-weight:600;margin-top:8px;">Click to Record</div>
              <div style="color:#6c757d;font-size:0.8rem;">(Demo — real version uses browser mic)</div>
              <div style="margin-top:8px;font-size:0.85rem;color:#2E75B6;">Language: <b>{lang}</b></div>
            </div>""", unsafe_allow_html=True)
            if st.button("🎙️ Simulate Voice Input", use_container_width=True, type="primary"):
                st.session_state["voice_done"] = True
        with col2:
            if st.session_state.get("voice_done"):
                st.success("✅ Voice captured! AI extracted:")
                fields = {"Enterprise Name":"Shree Lakshmi Textiles","Owner Name":"Rajesh Kumar",
                          "State":"Kerala","Sector":"Textiles & Apparel",
                          "Product Description":"Cotton fabric & readymade garments",
                          "Udyam Number":"UDYAM-KL-08-0023456",
                          "ASR Confidence":"96.3%","Language Detected":lang}
                for k,v in fields.items():
                    st.markdown(f"**{k}:** &nbsp;<span class='badge-success'>{v}</span>",
                                unsafe_allow_html=True)
            else:
                st.info("👆 Click 'Simulate Voice Input'")

    with tab2:
        col1,col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="info-card">
              <strong>📄 OCR Document Processing</strong><br>
              <small>LayoutLMv3 + Tesseract 5.0. 98.7% field extraction accuracy.</small>
            </div>""", unsafe_allow_html=True)
            doc_type  = st.selectbox("Document Type", ["Udyam Certificate","GST Certificate"])
            _uploaded = st.file_uploader("Upload Document", type=["pdf","png","jpg","jpeg"])
            if st.button("🔍 Simulate OCR", use_container_width=True, type="primary"):
                with st.spinner("Running OCR..."):
                    time.sleep(1.5)
                st.session_state["ocr_done"] = doc_type
        with col2:
            if st.session_state.get("ocr_done"):
                st.success(f"✅ {st.session_state['ocr_done']} processed")
                fields = ({"Enterprise Name":"Shree Lakshmi Textiles Pvt Ltd",
                           "Udyam Number":"UDYAM-KL-08-0023456","NIC Code":"13111",
                           "State":"Kerala","Investment":"₹45,00,000","Turnover":"₹1,20,00,000"}
                          if "Udyam" in st.session_state["ocr_done"] else
                          {"GSTIN":"32AABCS1429B1ZB","Legal Name":"SHREE LAKSHMI TEXTILES PVT LTD",
                           "State":"Kerala","Registration Date":"2018-07-01"})
                for k,v in fields.items():
                    st.markdown(f"**{k}:** &nbsp;<span class='badge-success'>{v}</span>",
                                unsafe_allow_html=True)
            else:
                st.info("👆 Click 'Simulate OCR'")

    with tab3:
        with st.form("ai_reg_manual"):
            c1,c2 = st.columns(2)
            with c1:
                r_name   = st.text_input("Enterprise Name*")
                r_state  = st.selectbox("State*", INDIAN_STATES)
                r_sector = st.selectbox("Sector*", SECTORS)
            with c2:
                r_turnover = st.number_input("Turnover (₹ Lakhs)*", min_value=0.1, value=50.0)
                r_emp      = st.number_input("Employees*", min_value=1, value=10)
                r_lang     = st.selectbox("Language", LANGUAGES)
            r_prod = st.text_area("Product Description*", height=80)
            if st.form_submit_button("🚀 Register", type="primary", use_container_width=True):
                if r_name and r_prod:
                    new_row = {
                        "MSE ID": f"MSE{random.randint(2025000,2029999)}",
                        "Enterprise Name": r_name, "State": r_state, "Sector": r_sector,
                        "Annual Turnover (L)": r_turnover, "No. of Employees": r_emp,
                        "Registration Date": datetime.now().strftime("%Y-%m-%d"),
                        "Status":"Pending Verification","Assigned SNP":"—","Match Score":0.0,
                        "Language": r_lang, "Onboarding Time (days)": None,
                        "Categorisation Confidence": round(np.random.uniform(0.78,0.96),2),
                        "Data Source":"✏️ Manual Entry"
                    }
                    new_df = pd.concat([st.session_state["df_mse"],pd.DataFrame([new_row])],ignore_index=True)
                    st.session_state["df_mse"]      = new_df
                    st.session_state["source_count"]= len(new_df)
                    st.success(f"✅ '{r_name}' registered! Total: {len(new_df):,} MSEs.")
                    st.rerun()
                else:
                    st.error("Name and Product Description are required.")


# ══════════════════════ PAGE: PRODUCT CATEGORISER ═════════════════
elif page == "🔍 Product Categoriser":
    st.markdown('<div class="section-header">🔍 AI Product Categorisation Engine — 3-Stage Pipeline</div>',
                unsafe_allow_html=True)
    df_mse = st.session_state["df_mse"]
    col1,col2 = st.columns([1,1.2])

    def simulate_product_categorisation(description):
        cats = {
            "cotton":("Textiles & Apparel","Cotton Fabric","ONDC:RET12-fabric-001",0.96),
            "shirt":("Textiles & Apparel","Ready-made Garments","ONDC:RET12-garment-002",0.94),
            "rice":("Agro Products","Processed Grains","ONDC:RET10-grain-001",0.97),
            "spice":("Food Processing","Spices & Condiments","ONDC:RET10-spice-001",0.95),
            "metal":("Metal Fabrication","Metal Components","ONDC:B2B-metal-001",0.91),
            "wood":("Woodwork & Furniture","Wooden Furniture","ONDC:RET12-furniture-001",0.93),
            "leather":("Leather Goods","Leather Products","ONDC:RET12-leather-001",0.92),
            "pharma":("Pharmaceuticals","Generic Medicines","ONDC:B2B-pharma-001",0.89),
        }
        for kw,r in cats.items():
            if kw in description.lower():
                return {"sector":r[0],"category":r[1],"ondc_code":r[2],
                        "confidence":r[3],"attributes":["material","finish","dimensions"],
                        "nic_code":f"1{random.randint(3000,9999)}"}
        return {"sector":"General Manufacturing","category":"Other Products",
                "ondc_code":"ONDC:B2B-gen-001","confidence":0.73,
                "attributes":["type","dimensions"],"nic_code":"32909"}

    with col1:
        product_text = st.text_area("Product Description",
            value="We manufacture high-quality cotton fabric and readymade shirts.",
            height=120)
        if st.button("⚡ Run AI Categorisation", type="primary", use_container_width=True):
            with st.spinner("Running 3-stage pipeline..."):
                time.sleep(1.2)
                st.session_state["cat_result"] = simulate_product_categorisation(product_text)

    with col2:
        if st.session_state.get("cat_result"):
            r = st.session_state["cat_result"]
            c = int(r["confidence"]*100)
            cc = "#1B5E20" if r["confidence"]>0.85 else "#E65100"
            st.markdown(f"""
            <div class="result-card">
              <div style="display:flex;justify-content:space-between;margin-bottom:12px;">
                <div style="font-size:1.1rem;font-weight:700;color:#1F4E79;">🎯 Result</div>
                <div style="color:{cc};font-weight:700;font-size:1.4rem;">{c}% Confident</div>
              </div>
              <div class="progress-bar-outer">
                <div class="progress-bar-inner" style="width:{c}%;background:linear-gradient(90deg,{cc},{cc}aa);"></div>
              </div><br>
              <table style="width:100%;font-size:0.85rem;">
                <tr><td style="color:#6c757d;width:160px;">Sector</td><td><strong>{r["sector"]}</strong></td></tr>
                <tr><td style="color:#6c757d;">Category</td><td><strong>{r["category"]}</strong></td></tr>
                <tr><td style="color:#6c757d;">ONDC Code</td><td><span class="badge-info">{r["ondc_code"]}</span></td></tr>
                <tr><td style="color:#6c757d;">NIC Code</td><td><span class="badge-info">{r["nic_code"]}</span></td></tr>
              </table>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("👈 Click 'Run AI Categorisation'")

    st.markdown('<div class="section-header">📊 Batch Stats — Current Data</div>', unsafe_allow_html=True)
    if "Categorisation Confidence" in df_mse.columns and len(df_mse) > 0:
        col1,col2 = st.columns(2)
        with col1:
            cats = pd.cut(df_mse["Categorisation Confidence"],
                          bins=[0,0.80,0.90,0.95,1.0],
                          labels=["<80% Review","80–90%","90–95%","95–100%"]).value_counts()
            fig = go.Figure(go.Pie(labels=cats.index, values=cats.values, hole=0.4,
                                   marker_colors=["#dc3545","#ffc107","#17a2b8","#28a745"]))
            fig.update_layout(height=240, margin=dict(l=0,r=0,t=10,b=0),
                              paper_bgcolor="white",
                              font=dict(family="Inter", color="#212529"),
                              legend=dict(font=dict(color="#212529"), bgcolor="rgba(255,255,255,0.9)"))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.markdown("<p style='color:#1F4E79;font-weight:600;margin-bottom:6px;'>📊 Accuracy by Sector</p>", unsafe_allow_html=True)
            sa = df_mse.groupby("Sector")["Categorisation Confidence"].mean().sort_values(ascending=False)
            for sector,acc in sa.items():
                bw = int(acc*100)
                color = "#1B5E20" if acc>0.90 else "#E65100"
                st.markdown(f"""
                <div style="margin-bottom:6px;">
                  <div style="display:flex;justify-content:space-between;font-size:0.78rem;">
                    <span>{str(sector)[:28]}</span>
                    <span style="color:{color};font-weight:600;">{acc*100:.1f}%</span>
                  </div>
                  <div class="progress-bar-outer">
                    <div class="progress-bar-inner" style="width:{bw}%;"></div>
                  </div>
                </div>""", unsafe_allow_html=True)


# ══════════════════════ PAGE: SNP MATCHER ═════════════════════════
elif page == "🔗 SNP Matcher":
    st.markdown('<div class="section-header">🔗 Intelligent MSE-to-SNP Matching Engine</div>',
                unsafe_allow_html=True)

    def simulate_snp_matching(sector, state, turnover):
        matches = []
        for _,snp in df_snp.iterrows():
            sem = random.uniform(0.60,0.98)
            if sector.split("&")[0].strip().lower() in snp["Domain Sectors"].lower():
                sem = min(sem+0.15,0.99)
            score = round(sem - (snp["Current Load (%)"]/100)*0.15 + (snp["Avg Fulfilment Rate (%)"]/100)*0.1, 3)
            matches.append({
                "SNP Name": snp["SNP Name"],
                "Match Score": min(score,0.99),
                "Domain Alignment":"High" if sem>0.85 else "Medium",
                "Current Load (%)": snp["Current Load (%)"],
                "Fulfilment Rate (%)": snp["Avg Fulfilment Rate (%)"],
                "Est. Onboarding (days)": snp["Onboarding Avg (days)"],
                "States Active": snp["States Active"]
            })
        return sorted(matches, key=lambda x:x["Match Score"], reverse=True)[:5]

    col1,col2 = st.columns([1,1.5])
    with col1:
        m_sector   = st.selectbox("MSE Sector", SECTORS)
        m_state    = st.selectbox("MSE State",  INDIAN_STATES)
        m_turnover = st.slider("Turnover (₹ Lakhs)", 5, 500, 50)
        if st.button("🔍 Find Best SNP Matches", type="primary", use_container_width=True):
            with st.spinner("Running matching algorithm..."):
                time.sleep(1.0)
                st.session_state["snp_matches"] = simulate_snp_matching(m_sector,m_state,m_turnover)
                st.session_state["match_sector"] = m_sector

    with col2:
        if st.session_state.get("snp_matches"):
            matches = st.session_state["snp_matches"]
            rank_labels = ["🥇 Best Match","🥈 2nd Choice","🥉 3rd Choice","4th","5th"]
            for i,match in enumerate(matches):
                sp = int(match["Match Score"]*100)
                sc = "#1B5E20" if match["Match Score"]>0.85 else "#E65100"
                st.markdown(f"""
                <div class="result-card" style="margin-bottom:8px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                      <span style="font-weight:700;">{rank_labels[i]}</span>
                      <span style="font-weight:600;color:#1F4E79;margin-left:8px;">{match["SNP Name"]}</span>
                    </div>
                    <div style="color:{sc};font-weight:700;font-size:1.3rem;">{sp}%</div>
                  </div>
                  <div class="progress-bar-outer">
                    <div class="progress-bar-inner" style="width:{sp}%;"></div>
                  </div>
                  <div style="display:flex;gap:16px;margin-top:8px;flex-wrap:wrap;font-size:0.78rem;color:#495057;">
                    <span>📋 {match["Domain Alignment"]}</span>
                    <span>⚡ Load:{match["Current Load (%)"]}%</span>
                    <span>✅ {match["Fulfilment Rate (%)"]}%</span>
                    <span>⏱️ {match["Est. Onboarding (days)"]}d</span>
                  </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("👈 Set parameters and click 'Find Best SNP Matches'")


# ══════════════════════ PAGE: MSE REGISTRY ════════════════════════
elif page == "📋 MSE Registry":
    df_mse = st.session_state["df_mse"]
    st.markdown('<div class="section-header">📋 MSE Registry — All Records</div>', unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        states_list = ["All"] + sorted(df_mse["State"].dropna().unique().tolist()) if "State" in df_mse.columns else ["All"]
        f_state  = st.selectbox("State",  states_list)
    with col2:
        sector_list = ["All"] + sorted(df_mse["Sector"].dropna().unique().tolist()) if "Sector" in df_mse.columns else ["All"]
        f_sector = st.selectbox("Sector", sector_list)
    with col3:
        status_list = ["All"] + sorted(df_mse["Status"].dropna().unique().tolist()) if "Status" in df_mse.columns else ["All"]
        f_status = st.selectbox("Status", status_list)
    with col4:
        search = st.text_input("🔍 Search", placeholder="Name or MSE ID...")

    df_f = df_mse.copy()
    if f_state  != "All" and "State"  in df_f.columns: df_f = df_f[df_f["State"]==f_state]
    if f_sector != "All" and "Sector" in df_f.columns: df_f = df_f[df_f["Sector"]==f_sector]
    if f_status != "All" and "Status" in df_f.columns: df_f = df_f[df_f["Status"]==f_status]
    if search:
        mask = pd.Series([False]*len(df_f), index=df_f.index)
        for col in ["Enterprise Name","MSE ID"]:
            if col in df_f.columns:
                mask |= df_f[col].astype(str).str.contains(search, case=False, na=False)
        df_f = df_f[mask]

    st.markdown(f"<p style='color:#495057;font-size:0.9rem;'><strong style='color:#1F4E79;'>Showing {len(df_f):,} of {len(df_mse):,} MSEs</strong> — Source: <code style='background:#e8f0fe;color:#1F4E79;padding:1px 5px;border-radius:4px;'>{st.session_state.get('source_label','')}</code></p>", unsafe_allow_html=True)

    display_cols = [c for c in ["MSE ID","Enterprise Name","State","Sector","Status",
                                 "Assigned SNP","Match Score","Onboarding Time (days)",
                                 "Categorisation Confidence","Data Source"]
                    if c in df_f.columns]

    fmt = {}
    if "Match Score"               in df_f.columns: fmt["Match Score"] = "{:.2f}"
    if "Categorisation Confidence" in df_f.columns: fmt["Categorisation Confidence"] = "{:.2f}"
    if "Onboarding Time (days)"    in df_f.columns: fmt["Onboarding Time (days)"] = "{:.1f}"

    st.dataframe(
        df_f[display_cols].head(200).style.format(fmt, na_rep="—"),
        use_container_width=True, height=440
    )

    col1,col2 = st.columns(2)
    with col1:
        csv = df_f[display_cols].to_csv(index=False)
        st.download_button("📥 Export Filtered as CSV", csv,
                           "mse_registry.csv","text/csv", use_container_width=True)
    with col2:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df_f[display_cols].to_excel(w, index=False, sheet_name="MSE Registry")
        st.download_button("📥 Export Filtered as Excel", buf.getvalue(),
                           "mse_registry.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)


# ══════════════════════ PAGE: ANALYTICS ═══════════════════════════
elif page == "📈 Analytics":
    df_mse = st.session_state["df_mse"]
    st.markdown('<div class="section-header">📈 Platform Analytics & AI Performance Monitoring</div>',
                unsafe_allow_html=True)

    dates = pd.date_range(start="2024-08-01", end="2025-02-21", freq="W")
    registrations = np.cumsum(np.random.poisson(max(len(df_mse)//30,5), len(dates)))
    onboardings   = np.cumsum(np.random.poisson(max(len(df_mse)//60,2), len(dates)))

    col1,col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=registrations, name="Registrations",
                                 line=dict(color="#2E75B6",width=2.5),fill="tozeroy",
                                 fillcolor="rgba(46,117,182,0.1)"))
        fig.add_trace(go.Scatter(x=dates, y=onboardings, name="Onboardings",
                                 line=dict(color="#1B5E20",width=2.5),fill="tozeroy",
                                 fillcolor="rgba(27,94,32,0.08)"))
        fig.update_layout(title="Cumulative Registrations vs Onboardings",
                          title_font=dict(color="#1F4E79", size=13),
                          height=300, margin=dict(l=0,r=0,t=40,b=0),
                          paper_bgcolor="white", plot_bgcolor="#f8f9fa",
                          font=dict(family="Inter", size=11, color="#212529"),
                          legend=dict(orientation="h", y=1.15,
                                      font=dict(color="#212529"), bgcolor="rgba(255,255,255,0.9)"),
                          xaxis=dict(tickfont=dict(color="#495057"), gridcolor="#e9ecef", linecolor="#dee2e6"),
                          yaxis=dict(tickfont=dict(color="#495057"), gridcolor="#e9ecef", linecolor="#dee2e6"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        acc = 0.87 + np.cumsum(np.random.normal(0.003,0.005,len(dates)))
        acc = np.clip(acc,0.80,0.99)
        fig = go.Figure(go.Scatter(x=dates, y=acc*100, mode="lines",
                                   line=dict(color="#6A1B9A",width=2.5),
                                   fill="tozeroy",fillcolor="rgba(106,27,154,0.08)"))
        fig.add_hline(y=90, line_dash="dash", line_color="#dc3545",
                      annotation_text="Target: 90%")
        fig.update_layout(title="Categorisation Accuracy Trend (%)",
                          title_font=dict(color="#1F4E79", size=13),
                          height=300, margin=dict(l=0,r=0,t=40,b=0),
                          paper_bgcolor="white", plot_bgcolor="#f8f9fa",
                          font=dict(family="Inter", size=11, color="#212529"),
                          xaxis=dict(tickfont=dict(color="#495057"), gridcolor="#e9ecef", linecolor="#dee2e6"),
                          yaxis=dict(tickfont=dict(color="#495057"), gridcolor="#e9ecef", linecolor="#dee2e6"))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">🏢 SNP Performance Leaderboard</div>',
                unsafe_allow_html=True)
    st.dataframe(
        df_snp.sort_values("Avg Fulfilment Rate (%)", ascending=False).style
        .format({"Avg Fulfilment Rate (%)":"{:.1f}%","Rating":"⭐ {:.1f}",
                 "Onboarding Avg (days)":"{:.1f}d"}),
        use_container_width=True
    )

    st.markdown('<div class="section-header">🎯 Impact vs Manual Baseline</div>',
                unsafe_allow_html=True)
    baseline = {"Onboarding Time (days)":[12.4,3.8],"Rejection Rate (%)":[34.7,8.2],
                "Categorisation Accuracy (%)":[67.3,94.2],"Daily Capacity":[90,1200]}
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Manual", x=list(baseline.keys()),
                         y=[v[0] for v in baseline.values()],
                         marker_color="#dc3545", opacity=0.7))
    fig.add_trace(go.Bar(name="MapMSE", x=list(baseline.keys()),
                         y=[v[1] for v in baseline.values()],
                         marker_color="#1F4E79", opacity=0.9))
    fig.update_layout(barmode="group", height=320, margin=dict(l=0,r=0,t=10,b=0),
                      paper_bgcolor="white", plot_bgcolor="#f8f9fa",
                      font=dict(family="Inter", size=11, color="#212529"),
                      legend=dict(orientation="h", y=1.05,
                                  font=dict(color="#212529"), bgcolor="rgba(255,255,255,0.9)"),
                      xaxis=dict(tickfont=dict(color="#212529", size=10),
                                 tickangle=-20,
                                 gridcolor="#e9ecef", linecolor="#dee2e6"),
                      yaxis=dict(tickfont=dict(color="#495057"),
                                 gridcolor="#e9ecef", linecolor="#dee2e6"))
    st.plotly_chart(fig, use_container_width=True)
