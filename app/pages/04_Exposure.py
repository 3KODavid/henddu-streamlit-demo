"""Exposure page for rankings and population exposure."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.processing.prepare.rankings import build_top_exposed_regions
from src.ui.charts import build_top_regions_figure
from src.ui.data_access import get_indicator_daily_data
from src.ui.filters import render_global_filters


st.title("Exposure")
filters = render_global_filters()
daily = get_indicator_daily_data(
    filters["indicator"],
    filters["start_date"],
    filters["end_date"],
)
scoped = daily[daily["admin_level"] == filters["admin_level"]].copy()

if scoped.empty:
    st.warning("No exposure data available for the selected filters.")
else:
    unit = scoped["unit"].iloc[0] if "unit" in scoped.columns and not scoped["unit"].dropna().empty else ""
    rankings = build_top_exposed_regions(scoped, filters["indicator"], limit=15)
    if "unit" not in rankings.columns:
        rankings["unit"] = unit
    figure = build_top_regions_figure(
        rankings,
        f"Exposure ranking for {filters['indicator']} ({unit}, {filters['admin_level']})".replace(" (,", " ("),
    )

    if figure is not None:
        st.plotly_chart(figure, use_container_width=True)

    st.dataframe(rankings, use_container_width=True)
    st.info("Population Exposure Index will be added once WorldPop integration is connected.")
