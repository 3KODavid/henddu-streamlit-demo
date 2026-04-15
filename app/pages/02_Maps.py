"""Maps page for choropleth and spatio-temporal animation."""

from __future__ import annotations

import streamlit as st

from src.ui.charts import build_animation_figure, build_choropleth_figure
from src.ui.data_access import get_boundaries, get_indicator_daily_data
from src.ui.filters import render_global_filters


st.title("Maps")
filters = render_global_filters()
boundaries = get_boundaries()
daily = get_indicator_daily_data(
    filters["indicator"],
    filters["start_date"],
    filters["end_date"],
)

boundaries = boundaries[boundaries["admin_level"] == filters["admin_level"]].copy()
daily = daily[daily["admin_level"] == filters["admin_level"]].copy()

if daily.empty or boundaries.empty:
    st.warning("No map data available for the selected filters.")
else:
    unit = daily["unit"].iloc[0] if "unit" in daily.columns and not daily["unit"].dropna().empty else ""
    available_dates = sorted(daily["date"].astype(str).unique())
    selected_date = st.selectbox("Map Date", available_dates, index=len(available_dates) - 1)
    snapshot = daily[daily["date"].astype(str) == selected_date].copy()

    choropleth = build_choropleth_figure(
        boundaries,
        snapshot,
        f"{filters['indicator']} ({unit}) on {selected_date} ({filters['admin_level']})".replace(" ()", ""),
    )
    animation = build_animation_figure(
        boundaries,
        daily,
        f"{filters['indicator']} daily animation ({unit}, {filters['admin_level']})".replace(" (,", " ("),
    )

    if choropleth is not None:
        st.plotly_chart(choropleth, use_container_width=True)
    if animation is not None:
        st.plotly_chart(animation, use_container_width=True)
