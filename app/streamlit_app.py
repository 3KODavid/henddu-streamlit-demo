"""Main entrypoint for the Henddu Streamlit MVP."""

from __future__ import annotations

import streamlit as st

from src.config.settings import get_settings
from src.utils.logging import configure_logging


settings = get_settings()
configure_logging(settings.log_level)

st.set_page_config(
    page_title="Henddu Air Quality Demo",
    page_icon="H",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Henddu Air Quality Monitoring and Exposure Demo")
st.caption(
    "Live CIV MVP with ADM1 and ADM2 views powered by CAMS data from S3."
)

st.markdown(
    """
    ### What is available now
    - Real CIV administrative boundaries for `ADM1` and `ADM2`
    - Real CAMS pollution data for `PM2.5`, `PM10`, `NO2`, and `O3`
    - Overview KPIs
    - Choropleth map
    - Spatio-temporal animation
    - Time-series exploration
    - Top exposed regions

    ### Suggested navigation
    1. Open **Overview** for KPI snapshots.
    2. Open **Maps** for the choropleth and animation.
    3. Open **Trends** for regional time series.
    4. Open **Exposure** for rankings.

    ### Current scope note
    `Temperature` and `Population Exposure Index` are not wired yet because the ERA5 and WorldPop integration steps are still pending.
    """
)
