# MapMSE Streamlit Dashboard
# ------------------------------------------------------------
# Run:
#   pip install -r requirements.txt
#   streamlit run app.py
#
# Notes:
# - This dashboard is a UI/analytics layer aligned to the MapMSE proposal:
#   Intelligent Registration -> AI Product Categorisation -> Semantic SNP Matching,
#   plus Responsible AI monitoring and immutable audit logs.
# - By default it runs on generated demo data. To use real data, upload CSVs
#   from the Admin page, or wire the `src/api_client.py` helpers to your FastAPI.
# ------------------------------------------------------------

from __future__ import annotations

import streamlit as st
import pandas as pd

from src.data import (
    AppDataStore,
    ensure_demo_data,
)
from src.components import (
    inject_global_css,
    kpi_row,
    section_header,
    footer,
)
from src.pages import (
    page_overview,
    page_registration,
    page_categorisation,
    page_matching,
    page_responsible_ai,
    page_audit_logs,
    page_admin,
)

APP_TITLE = "MapMSE • AI-Powered MSE→SNP Onboarding"
APP_ICON = "🧭"


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_global_css()

    # ---------- Sidebar ----------
    st.sidebar.markdown(
        """
        <div style="font-weight:700; font-size: 1.05rem; line-height:1.2;">
          🧭 MapMSE Dashboard
        </div>
        <div style="color:#6b7280; font-size: 0.85rem; margin-top:0.15rem;">
          MSE→SNP onboarding intelligence
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.divider()

    # Data store (session-scoped)
    if "store" not in st.session_state:
        ensure_demo_data()
        st.session_state["store"] = AppDataStore()

    store: AppDataStore = st.session_state["store"]

    # Navigation
    page = st.sidebar.radio(
        "Navigate",
        [
            "Overview",
            "Intelligent Registration",
            "AI Product Categorisation",
            "Semantic SNP Matching",
            "Responsible AI & Monitoring",
            "Audit Logs",
            "Admin",
        ],
        index=0,
    )

    # Global filters
    with st.sidebar.expander("Global filters", expanded=True):
        date_min, date_max = store.applications["submitted_at"].min(), store.applications["submitted_at"].max()
        date_range = st.date_input(
            "Submission date range",
            value=(date_min.date(), date_max.date()),
            min_value=date_min.date(),
            max_value=date_max.date(),
        )
        states = ["All"] + sorted(store.applications["state"].unique().tolist())
        state = st.selectbox("State", states, index=0)

        sectors = ["All"] + sorted(store.applications["sector"].unique().tolist())
        sector = st.selectbox("Sector", sectors, index=0)

    # Apply global filters
    apps = store.applications.copy()
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    apps = apps[(apps["submitted_at"] >= start_date) & (apps["submitted_at"] <= end_date)]
    if state != "All":
        apps = apps[apps["state"] == state]
    if sector != "All":
        apps = apps[apps["sector"] == sector]

    # KPI strip (top)
    kpi_row(store, apps)

    st.divider()

    # ---------- Pages ----------
    if page == "Overview":
        page_overview(store, apps)
    elif page == "Intelligent Registration":
        page_registration(store, apps)
    elif page == "AI Product Categorisation":
        page_categorisation(store, apps)
    elif page == "Semantic SNP Matching":
        page_matching(store, apps)
    elif page == "Responsible AI & Monitoring":
        page_responsible_ai(store, apps)
    elif page == "Audit Logs":
        page_audit_logs(store, apps)
    elif page == "Admin":
        page_admin(store)
    else:
        st.info("Select a page from the sidebar.")

    footer()


if __name__ == "__main__":
    main()
