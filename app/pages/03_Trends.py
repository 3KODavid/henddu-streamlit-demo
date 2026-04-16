"""Trends page for time-series analysis."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from app.bootstrap import ensure_project_root_on_path

ensure_project_root_on_path()

from src.ui.charts import build_timeseries_figure
from src.ui.data_access import get_indicator_daily_data
from src.ui.filters import render_global_filters


st.title("Trends")
filters = render_global_filters()
daily = get_indicator_daily_data(
    filters["indicator"],
    filters["start_date"],
    filters["end_date"],
)
scoped = daily[daily["admin_level"] == filters["admin_level"]].copy()

if scoped.empty:
    st.warning("No trend data available for the selected filters.")
else:
    unit = scoped["unit"].iloc[0] if "unit" in scoped.columns and not scoped["unit"].dropna().empty else ""
    region_options = sorted(scoped["admin_name"].dropna().unique())
    selected_region = st.selectbox("Region", region_options)

    region_series = scoped[scoped["admin_name"] == selected_region].copy()
    national_series = (
        scoped.groupby(["date", "indicator"], dropna=False)["value"]
        .mean()
        .reset_index()
    )
    national_series["admin_name"] = "National mean"

    combined = pd.concat(
        [
            region_series[["date", "admin_name", "value"]],
            national_series[["date", "admin_name", "value"]],
        ],
        ignore_index=True,
    )

    figure = build_timeseries_figure(
        combined,
        f"{filters['indicator']} trend ({unit}) for {selected_region} vs national mean".replace(" ()", ""),
    )
    if figure is not None:
        st.plotly_chart(figure, use_container_width=True)

    st.dataframe(region_series, use_container_width=True)
