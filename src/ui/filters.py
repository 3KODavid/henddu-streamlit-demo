"""Shared Streamlit filter controls for the Henddu demo."""

from __future__ import annotations

from datetime import date

import streamlit as st

from src.config.constants import ADMIN_LEVEL_OPTIONS, CAMS_DATA_END_DATE, CAMS_DATA_START_DATE, DEMO_INDICATOR_OPTIONS


def render_global_filters() -> dict[str, str]:
    min_date = date.fromisoformat(CAMS_DATA_START_DATE)
    max_date = date.fromisoformat(CAMS_DATA_END_DATE)
    default_start = date(2025, 8, 25)
    default_end = max_date

    with st.sidebar:
        st.header("Global Filters")
        st.text_input("Country", value="CIV", disabled=True)
        admin_level = st.selectbox("Administrative Level", ADMIN_LEVEL_OPTIONS, key="admin_level")
        indicator = st.selectbox("Indicator", DEMO_INDICATOR_OPTIONS, key="indicator")
        start_date, end_date = st.date_input(
            "Date Range",
            value=(default_start, default_end),
            min_value=min_date,
            max_value=max_date,
            format="YYYY-MM-DD",
            key="date_range",
        )
        time_aggregation = st.selectbox("Time Aggregation", ["daily"], disabled=True, key="time_agg")

    return {
        "country": "CIV",
        "admin_level": admin_level,
        "indicator": indicator,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "time_aggregation": time_aggregation,
    }
