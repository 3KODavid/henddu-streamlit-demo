"""Overview page for the Henddu Streamlit MVP."""

from __future__ import annotations

import streamlit as st

from src.processing.prepare.kpis import build_kpis
from src.processing.prepare.rankings import build_top_exposed_regions
from src.ui.charts import build_top_regions_figure
from src.ui.data_access import get_indicator_daily_data
from src.ui.filters import render_global_filters


st.title("Overview")
filters = render_global_filters()
daily = get_indicator_daily_data(
    filters["indicator"],
    filters["start_date"],
    filters["end_date"],
)
scoped = daily[daily["admin_level"] == filters["admin_level"]].copy()

if scoped.empty:
    st.warning("No data available for the selected filters.")
else:
    unit = scoped["unit"].iloc[0] if "unit" in scoped.columns and not scoped["unit"].dropna().empty else ""
    kpis = build_kpis(scoped, filters["indicator"])
    top_regions = build_top_exposed_regions(scoped, filters["indicator"], limit=10)
    if "unit" not in top_regions.columns:
        top_regions["unit"] = unit

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Mean", f"{kpis['mean_value']:.2f} {unit}".strip() if kpis["mean_value"] is not None else "NA")
    col2.metric("Max", f"{kpis['max_value']:.2f} {unit}".strip() if kpis["max_value"] is not None else "NA")
    col3.metric("Top Region", kpis["top_region"] or "NA")
    col4.metric("Regions Above Threshold", str(kpis["regions_above_threshold"]))
    col5.metric("Latest Date", str(kpis["latest_date"]) if kpis["latest_date"] is not None else "NA")

    st.subheader("Top Exposed Regions")
    top_chart = build_top_regions_figure(top_regions, f"Top {filters['admin_level']} regions for {filters['indicator']}")
    if top_chart is not None:
        st.plotly_chart(top_chart, use_container_width=True)

    st.subheader("Top Regions Table")
    st.dataframe(top_regions, use_container_width=True)
