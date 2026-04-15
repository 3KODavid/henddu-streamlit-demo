"""Streamlit-cached access to processed demo datasets."""

from __future__ import annotations

import geopandas as gpd
import pandas as pd
import streamlit as st

from src.services.demo_data_service import DemoDataService


@st.cache_data(show_spinner="Loading CIV administrative boundaries...")
def get_boundaries() -> gpd.GeoDataFrame:
    return DemoDataService().load_boundaries()


@st.cache_data(show_spinner="Aggregating CAMS data across CIV regions...")
def get_indicator_daily_data(indicator: str, start_date: str, end_date: str) -> pd.DataFrame:
    return DemoDataService().build_daily_series(indicator, start_date, end_date)
